import os
from datetime import datetime, timedelta, timezone

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from textblob import TextBlob
import secrets
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SESSION_SECRET', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///feedback.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', '')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', '')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')

db = SQLAlchemy(app)
mail = Mail(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='user')
    reset_token = db.Column(db.String(100), nullable=True)
    reset_token_expiry = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    feedbacks = db.relationship('Feedback', backref='user', lazy=True)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    guest_name = db.Column(db.String(100), nullable=True)
    guest_email = db.Column(db.String(120), nullable=True)
    category = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=True)
    sentiment = db.Column(db.String(20), nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        return 'Positive'
    elif polarity < -0.1:
        return 'Negative'
    else:
        return 'Neutral'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('login'))
        user = User.query.get(session['user_id'])
        if user.role != 'admin':
            flash('Admin access required.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('user_id'):
        if session.get('user_role') == 'admin':
            return redirect(url_for('index'))
        else:
            return redirect(url_for('index'))
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered!', 'danger')
            return redirect(url_for('register'))
        
        hashed_password = generate_password_hash(password)
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user_id'):
        if session.get('user_role') == 'admin':
            return redirect(url_for('index'))
        else:
            return redirect(url_for('index'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['user_role'] = user.role.strip().lower()
            session.modified = True
            flash(f'Welcome back, {user.name}!', 'success')
            
            if user.role == 'user':
                return redirect(url_for('index'))
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password!', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if session.get('user_id'):
        if session.get('user_role') == 'admin':
            return redirect(url_for('index'))
        else:
            return redirect(url_for('index'))
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            token = secrets.token_urlsafe(32)
            user.reset_token = token
            # use timezone-aware datetime
            user.reset_token_expiry = datetime.now() + timedelta(hours=1)

            db.session.commit()

            reset_link = url_for('reset_password', token=token, _external=True)
            try:
                msg = Message('Password Reset Request', recipients=[user.email])
                msg.body = f'''Hello {user.name},

You requested a password reset. Click the link below to reset your password:

{reset_link}

This link will expire in 1 hour.

If you did not request this, please ignore this email.

Best regards,
Your App Team
'''
                mail.send(msg)
                flash('Password reset instructions sent to your email.', 'success')
            except Exception as e:
                flash(f'Email could not be sent. Error: {str(e)}', 'danger')
        else:
            flash('If an account with that email exists, reset instructions have been sent.', 'info')
        return redirect(url_for('login'))
    return render_template('forgot_password.html')


# Reset password route
@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.query.filter_by(reset_token=token).first()

    # Check for valid user and token expiry
    if not user or not user.reset_token_expiry or user.reset_token_expiry < datetime.now():
     flash('Invalid or expired reset link.', 'danger')
     return redirect(url_for('forgot_password'))
    if request.method == 'POST':
        password = request.form.get('password')
        user.password = generate_password_hash(password)
        user.reset_token = None
        user.reset_token_expiry = None
        db.session.commit()
        flash('Password has been reset successfully!', 'success')
        return redirect(url_for('login'))

    return render_template('reset_password.html', token=token)
@app.route('/guest-feedback', methods=['GET', 'POST'])
def guest_feedback():
    if session.get('user_role') == 'admin' or session.get('user_role') == 'user':
            return redirect(url_for('index'))
    if request.method == 'POST':
        guest_name = request.form.get('name')
        guest_email = request.form.get('email')
        category = request.form.get('category')
        message = request.form.get('message')
        rating = request.form.get('rating')
        
        sentiment = analyze_sentiment(message)
        
        feedback = Feedback(
            guest_name=guest_name,
            guest_email=guest_email,
            category=category,
            message=message,
            rating=int(rating) if rating else None,
            sentiment=sentiment
        )
        db.session.add(feedback)
        db.session.commit()
        
        flash(f'Thank you for your feedback! Sentiment: {sentiment}', 'success')
        return redirect(url_for('index'))
    
    return render_template('guest_feedback.html')

@app.route('/user-feedback', methods=['GET', 'POST'])
@login_required
def user_feedback():
    if session.get('user_role') == 'admin':
        flash("Admins cannot submit feedback.", "warning")
        return redirect(url_for('admin_dashboard'))
    if request.method == 'POST':
        category = request.form.get('category')
        message = request.form.get('message')
        rating = request.form.get('rating')
        
        sentiment = analyze_sentiment(message)
        
        feedback = Feedback(
            user_id=session['user_id'],
            category=category,
            message=message,
            rating=int(rating) if rating else None,
            sentiment=sentiment
        )
        db.session.add(feedback)
        db.session.commit()
        
        flash(f'Feedback submitted successfully! Sentiment: {sentiment}', 'success')
        return redirect(url_for('user_dashboard'))
    
    return render_template('user_feedback.html')

@app.route('/user-dashboard')
@login_required
def user_dashboard():
    if session.get('user_role') == 'admin':
        return redirect(url_for('index'))

    # Get query parameters
    limit = request.args.get('limit', default=10, type=int)
    sentiment_filter = request.args.get('sentiment', default='all')
    sort_order = request.args.get('sort', default='new_to_old')

    # Base query: user's own feedback
    query = Feedback.query.filter_by(user_id=session['user_id'])

    # Apply sentiment filter
    if sentiment_filter.lower() in ['positive', 'neutral', 'negative']:
        query = query.filter(Feedback.sentiment == sentiment_filter.capitalize())

    # Apply sort order
    if sort_order == 'old_to_new':
        query = query.order_by(Feedback.timestamp.asc())
    else:
        query = query.order_by(Feedback.timestamp.desc())

    feedbacks = query.limit(limit).all()

    return render_template('user_dashboard.html', feedbacks=feedbacks,
                           limit=limit, sentiment_filter=sentiment_filter,
                           sort_order=sort_order)

@app.route('/offline')
def offline():
    return render_template('offline.html')
@app.route('/admin-dashboard')
@admin_required
def admin_dashboard():
    if session.get('user_id') and session.get('user_role') == 'user':
        return redirect(url_for('index'))

    # Get filter parameters
    limit = request.args.get('limit', default=10, type=int)
    sentiment_filter = request.args.get('sentiment', default='all')
    type_filter = request.args.get('type', default='all')
    sort_order = request.args.get('sort', default='new_to_old')  # default: newest first

    # Start query
    query = Feedback.query

    # Apply sentiment filter
    if sentiment_filter.lower() in ['positive', 'neutral', 'negative']:
        query = query.filter(Feedback.sentiment == sentiment_filter.capitalize())

    # Apply type filter
    if type_filter.lower() == 'user':
        query = query.filter(Feedback.user_id.isnot(None))
    elif type_filter.lower() == 'guest':
        query = query.filter(Feedback.user_id.is_(None))

    # Apply sort order
    if sort_order == 'old_to_new':
        query = query.order_by(Feedback.timestamp.asc())
    else:
        query = query.order_by(Feedback.timestamp.desc())

    # Apply limit
    feedbacks = query.limit(limit).all()

    # Stats (all feedbacks)
    total_feedbacks = Feedback.query.count()
    positive = Feedback.query.filter_by(sentiment='Positive').count()
    negative = Feedback.query.filter_by(sentiment='Negative').count()
    neutral = Feedback.query.filter_by(sentiment='Neutral').count()
    
    stats = {
        'total': total_feedbacks,
        'positive': positive,
        'negative': negative,
        'neutral': neutral
    }

    return render_template('admin_dashboard.html', feedbacks=feedbacks, stats=stats,
                           limit=limit, sentiment_filter=sentiment_filter,
                           type_filter=type_filter, sort_order=sort_order)


@app.route('/admin/delete-feedback/<int:id>', methods=['POST'])
@admin_required
def delete_feedback(id):
    feedback = Feedback.query.get_or_404(id)
    db.session.delete(feedback)
    db.session.commit()
    flash('Feedback deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/api/sentiment-stats')
def sentiment_stats():
    feedbacks = Feedback.query.all()
    positive = len([f for f in feedbacks if f.sentiment == 'Positive'])
    negative = len([f for f in feedbacks if f.sentiment == 'Negative'])
    neutral = len([f for f in feedbacks if f.sentiment == 'Neutral'])
    
    return jsonify({
        'positive': positive,
        'negative': negative,
        'neutral': neutral
    })

@app.route('/api/chart-data')
def chart_data():
    feedbacks = Feedback.query.all()
    
    sentiment_data = {
        'Positive': len([f for f in feedbacks if f.sentiment == 'Positive']),
        'Negative': len([f for f in feedbacks if f.sentiment == 'Negative']),
        'Neutral': len([f for f in feedbacks if f.sentiment == 'Neutral'])
    }
    
    category_data = {}
    for feedback in feedbacks:
        category = feedback.category
        if category in category_data:
            category_data[category] += 1
        else:
            category_data[category] = 1
    
    from collections import defaultdict
    category_sentiment = defaultdict(lambda: {'Positive': 0, 'Negative': 0, 'Neutral': 0})
    for feedback in feedbacks:
        category_sentiment[feedback.category][feedback.sentiment] += 1
    
    rating_data = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0}
    for feedback in feedbacks:
        if feedback.rating:
            rating_data[str(feedback.rating)] += 1
    
    timeline_data = defaultdict(int)
    for feedback in feedbacks:
        date_key = feedback.timestamp.strftime('%Y-%m-%d')
        timeline_data[date_key] += 1
    
    sorted_timeline = dict(sorted(timeline_data.items()))
    
    return jsonify({
        'sentiment': sentiment_data,
        'categories': category_data,
        'category_sentiment': dict(category_sentiment),
        'ratings': rating_data,
        'timeline': sorted_timeline
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        admin_email = os.environ.get('ADMIN_EMAIL')
        admin_password = os.environ.get('ADMIN_PASSWORD')
        
        if admin_email and admin_password:
            admin = User.query.filter_by(email=admin_email).first()
            if not admin:
                admin_user = User(
                    name='Admin',
                    email=admin_email,
                    password=generate_password_hash(admin_password),
                    role='admin'
                )
                db.session.add(admin_user)
                db.session.commit()
                print(f"Admin user created: {admin_email}")
        else:
            print(" WARNING: No admin user configured. Set ADMIN_EMAIL and ADMIN_PASSWORD environment variables to create an admin account.")
            print("   Alternatively, register a normal user and manually update their role to 'admin' in the database.")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
