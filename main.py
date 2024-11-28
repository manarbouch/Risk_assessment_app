from flask import Flask, Blueprint, render_template, redirect, url_for, request, flash, session
from app import db, create_app  # Import db and create_app from app.py
from models import User, RiskAssessment
from flask_bcrypt import Bcrypt
import matplotlib.pyplot as plt
import pandas as pd
import os

# Initialize Flask app using the factory function
app = create_app()
app.config['DEBUG'] = True
app.config['ENV'] = 'development'

bcrypt = Bcrypt(app)  # Initialize Bcrypt with app

# Initialize Blueprint
main_blueprint = Blueprint('main', __name__)

@main_blueprint.before_app_request
def create_tables():
    """
    Create database tables if they don't already exist.
    """
    # Moved to create_app(), so this can be removed from here
    pass

@main_blueprint.route('/')
def index():
    return render_template('index.html')

@main_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            if user.completed_questionnaire:
                return redirect(url_for('main.dashboard'))
            else:
                return redirect(url_for('main.result'))
        else:
            error = "Invalid credentials. Please try again."
            return render_template('login.html', error=error)
    return render_template('login.html')

@main_blueprint.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        if User.query.filter_by(email=email).first():
            flash("Email already in use. Please log in.")
            return redirect(url_for('main.login'))

        user = User(email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash('Account created successfully! You can now complete the questionnaire.')
        return redirect(url_for('main.result'))

    return render_template('create_account.html')

@main_blueprint.route('/result', methods=['GET', 'POST'])
def result():
    user_id = session.get('user_id')
    if user_id is None:
        flash("You need to log in to complete the questionnaire.")
        return redirect(url_for('main.login'))

    user = User.query.get(user_id)
    if not user:
        flash("User not found.")
        return redirect(url_for('main.login'))

    # Risk calculation for the result page
    if request.method == 'POST':
        goal = request.form['goal']
        time_horizon = request.form['time_horizon']
        reaction = request.form['reaction']
        savings_rate = request.form['savings_rate']
        experience = request.form['experience']

        # Calculate the risk score
        risk_score = calculate_risk_score(goal, time_horizon, reaction, savings_rate, experience)
        risk_category = categorize_risk(risk_score)

        # Create and save the risk assessment
        risk_assessment = RiskAssessment(
            user_id=user.id,
            goal=goal,
            time_horizon=time_horizon,
            reaction=reaction,
            savings_rate=savings_rate,
            experience=experience,
            risk_score=risk_score,
            risk_category=risk_category
        )

        # Mark user as having completed the questionnaire
        user.completed_questionnaire = True
        db.session.add(risk_assessment)
        db.session.commit()

        flash("Questionnaire completed successfully!")
        return redirect(url_for('main.dashboard'))

    # Default view for result page if GET request
    return render_template('result.html')

@main_blueprint.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    if user_id is None:
        flash("You need to log in to access the dashboard.")
        return redirect(url_for('main.login'))

    user = User.query.get(user_id)
    if not user:
        flash("User not found.")
        return redirect(url_for('main.login'))

    # Fetching historical risk assessments from the database
    risk_assessments = RiskAssessment.query.filter_by(user_id=user_id).all()

    # Example: Dynamic time labels and risk scores
    time_labels = [ra.time_horizon for ra in risk_assessments]  # Example: use time_horizon as labels
    risk_scores_over_time = [ra.risk_score for ra in risk_assessments]  # Example: collect risk scores over time

    return render_template('dashboard.html', user=user, time_labels=time_labels, risk_scores_over_time=risk_scores_over_time)

@main_blueprint.route('/generate_report')
def generate_report():
    user_id = session.get('user_id')
    if user_id is None:
        flash("You need to log in to access the report.")
        return redirect(url_for('main.login'))

    user = User.query.get(user_id)
    if not user:
        flash("User not found.")
        return redirect(url_for('main.login'))

    risk_assessments = RiskAssessment.query.filter_by(user_id=user_id).all()

    # Example: Dynamic time labels and risk scores
    time_labels = [ra.time_horizon for ra in risk_assessments]  # Example: use time_horizon as labels
    risk_scores = [ra.risk_score for ra in risk_assessments]  # Example: collect risk scores

    # Create the plot using matplotlib
    fig, ax = plt.subplots()
    ax.plot(time_labels, risk_scores, marker='o')

    ax.set(xlabel='Time', ylabel='Risk Score', title='Risk Score Over Time')
    plt.xticks(rotation=45)

    # Save the plot to the static directory
    chart_path = os.path.join('static', 'chart.png')
    fig.savefig(chart_path)

    return render_template('generate_report.html', chart_path=chart_path)

@main_blueprint.route('/profile')
def profile():
    user_id = session.get('user_id')
    if not user_id:
        flash("You need to log in to view your profile.")
        return redirect(url_for('main.login'))

    user = User.query.get(user_id)
    return render_template('profile.html', user=user)

@main_blueprint.route('/notifications')
def notifications():
    return render_template('notifications.html')

@main_blueprint.route('/settings')
def settings():
    return render_template('settings.html')

@main_blueprint.route('/investment-suggestions')
def investment_suggestions():
    return render_template('investment_suggestions.html')

@main_blueprint.route('/risk-assessment')
def risk_assessment():
    return render_template('risk_assessment.html')

@main_blueprint.route('/logout')
def logout():
    session.clear()  # This will clear all data stored in the session, like logged-in user info
    return redirect(url_for('main.index'))

def calculate_risk_score(goal, time_horizon, reaction, savings_rate, experience):
    # Placeholder for calculating the risk score
    score = 0
    if goal == 'Retirement':
        score += 30
    if time_horizon == 'Long':
        score += 20
    if reaction == 'Aggressive':
        score += 25
    if savings_rate == 'High':
        score += 15
    if experience == 'High':
        score += 10
    return score

def categorize_risk(score):
    if score > 60:
        return 'High Risk'
    elif score > 40:
        return 'Moderate Risk'
    else:
        return 'Low Risk'

# Register the blueprint
app.register_blueprint(main_blueprint, url_prefix='/')

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)

