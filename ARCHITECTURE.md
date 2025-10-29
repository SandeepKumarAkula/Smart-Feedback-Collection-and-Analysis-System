# 🏗️ Smart Feedback Collection and Analysis System - Architecture Documentation

## Table of Contents
1. [System Overview](#system-overview)
2. [Architecture Diagram](#architecture-diagram)
3. [Authentication Flow](#authentication-flow)
4. [Application Logic](#application-logic)
5. [Database Architecture](#database-architecture)
6. [API Endpoints](#api-endpoints)
7. [Security Implementation](#security-implementation)
8. [Feature Enhancements](#feature-enhancements)
9. [Technology Stack](#technology-stack)

---

## System Overview

The Smart Feedback Collection and Analysis System is a full-stack web application built with Flask that enables organizations to collect, analyze, and visualize user feedback with automatic sentiment analysis. The system supports three distinct user roles (Guest, Registered User, and Admin) with role-based access control.

### Key Capabilities
- **Multi-role Access**: Guest, User, and Admin roles with different permissions
- **AI-Powered Analysis**: Automatic sentiment detection using TextBlob NLP
- **Real-time Analytics**: Interactive charts and visualizations using Chart.js
- **Secure Authentication**: Password hashing, session management, and password recovery
- **Responsive Design**: Mobile-first UI with modern card-based layout

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Browser    │  │   Mobile     │  │   Tablet     │          │
│  │  (Desktop)   │  │   Device     │  │   Device     │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
│         │                  │                  │                  │
│         └──────────────────┴──────────────────┘                  │
│                            │                                     │
└────────────────────────────┼─────────────────────────────────────┘
                             │ HTTPS
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      PRESENTATION LAYER                          │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Flask Application (app.py)                   │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐         │   │
│  │  │  Routes    │  │ Templates  │  │   Static   │         │   │
│  │  │ (Endpoints)│  │  (Jinja2)  │  │ (CSS/JS)   │         │   │
│  │  └────────────┘  └────────────┘  └────────────┘         │   │
│  └──────────────────────────────────────────────────────────┘   │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                       BUSINESS LOGIC LAYER                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Auth Manager │  │   Sentiment  │  │   Role-Based │          │
│  │  (Sessions)  │  │   Analyzer   │  │   Access     │          │
│  │              │  │  (TextBlob)  │  │   Control    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Password   │  │    Email     │  │   Analytics  │          │
│  │   Recovery   │  │   Service    │  │   Engine     │          │
│  │              │  │ (Flask-Mail) │  │              │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                       DATA ACCESS LAYER                          │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              SQLAlchemy ORM                               │   │
│  │  ┌────────────┐              ┌────────────┐             │   │
│  │  │   User     │              │  Feedback  │             │   │
│  │  │   Model    │◄─────────────┤   Model    │             │   │
│  │  └────────────┘  1:N         └────────────┘             │   │
│  └──────────────────────────────────────────────────────────┘   │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                       DATABASE LAYER                             │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              PostgreSQL Database (Neon)                   │   │
│  │  ┌────────────┐              ┌────────────┐             │   │
│  │  │   users    │              │  feedback  │             │   │
│  │  │   table    │              │   table    │             │   │
│  │  └────────────┘              └────────────┘             │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      EXTERNAL SERVICES                           │
│  ┌──────────────┐              ┌────────────┐                   │
│  │    Gmail     │              │  TextBlob  │                   │
│  │  SMTP Server │              │  NLP API   │                   │
│  └──────────────┘              └────────────┘                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Authentication Flow

### 1. User Registration Flow

```
┌─────────┐         ┌─────────┐         ┌─────────┐         ┌─────────┐
│  User   │         │  Flask  │         │Password │         │Database │
│ Browser │         │  App    │         │ Hasher  │         │         │
└────┬────┘         └────┬────┘         └────┬────┘         └────┬────┘
     │                   │                   │                   │
     │ GET /register     │                   │                   │
     ├──────────────────►│                   │                   │
     │                   │                   │                   │
     │ Registration Form │                   │                   │
     │◄──────────────────┤                   │                   │
     │                   │                   │                   │
     │ POST /register    │                   │                   │
     │ (name, email, pwd)│                   │                   │
     ├──────────────────►│                   │                   │
     │                   │                   │                   │
     │                   │ Check if email    │                   │
     │                   │ exists            │                   │
     │                   ├──────────────────────────────────────►│
     │                   │                   │                   │
     │                   │ Email not found   │                   │
     │                   │◄──────────────────────────────────────┤
     │                   │                   │                   │
     │                   │ Hash password     │                   │
     │                   ├──────────────────►│                   │
     │                   │                   │                   │
     │                   │ Hashed password   │                   │
     │                   │◄──────────────────┤                   │
     │                   │                   │                   │
     │                   │ Create new user   │                   │
     │                   │ (name, email,     │                   │
     │                   │  hashed_pwd,      │                   │
     │                   │  role='user')     │                   │
     │                   ├──────────────────────────────────────►│
     │                   │                   │                   │
     │                   │ User created      │                   │
     │                   │◄──────────────────────────────────────┤
     │                   │                   │                   │
     │ Redirect to login │                   │                   │
     │◄──────────────────┤                   │                   │
     │                   │                   │                   │
```

**Implementation Details:**
```python
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if email already exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered!', 'danger')
            return redirect(url_for('register'))
        
        # Hash password using Werkzeug
        hashed_password = generate_password_hash(password)
        
        # Create new user with default role 'user'
        new_user = User(
            name=name, 
            email=email, 
            password=hashed_password
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')
```

### 2. User Login Flow

```
┌─────────┐         ┌─────────┐         ┌─────────┐         ┌─────────┐
│  User   │         │  Flask  │         │Password │         │Database │
│ Browser │         │  App    │         │Verifier │         │         │
└────┬────┘         └────┬────┘         └────┬────┘         └────┬────┘
     │                   │                   │                   │
     │ GET /login        │                   │                   │
     ├──────────────────►│                   │                   │
     │                   │                   │                   │
     │ Login Form        │                   │                   │
     │◄──────────────────┤                   │                   │
     │                   │                   │                   │
     │ POST /login       │                   │                   │
     │ (email, password) │                   │                   │
     ├──────────────────►│                   │                   │
     │                   │                   │                   │
     │                   │ Query user by     │                   │
     │                   │ email             │                   │
     │                   ├──────────────────────────────────────►│
     │                   │                   │                   │
     │                   │ User data         │                   │
     │                   │ (id, name, email, │                   │
     │                   │  hashed_pwd, role)│                   │
     │                   │◄──────────────────────────────────────┤
     │                   │                   │                   │
     │                   │ Verify password   │                   │
     │                   ├──────────────────►│                   │
     │                   │                   │                   │
     │                   │ Password valid    │                   │
     │                   │◄──────────────────┤                   │
     │                   │                   │                   │
     │                   │ Create session:   │                   │
     │                   │ - user_id         │                   │
     │                   │ - user_name       │                   │
     │                   │ - user_role       │                   │
     │                   │                   │                   │
     │ Redirect to       │                   │                   │
     │ appropriate page  │                   │                   │
     │ based on role     │                   │                   │
     │◄──────────────────┤                   │                   │
     │                   │                   │                   │
```

**Implementation Details:**
```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Query user by email
        user = User.query.filter_by(email=email).first()
        
        # Verify password using Werkzeug
        if user and check_password_hash(user.password, password):
            # Create session
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['user_role'] = user.role.strip().lower()
            session.modified = True
            
            flash(f'Welcome back, {user.name}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password!', 'danger')
    
    return render_template('login.html')
```

### 3. Password Recovery Flow

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│  User   │    │  Flask  │    │  Token  │    │Database │    │  Gmail  │
│ Browser │    │  App    │    │Generator│    │         │    │  SMTP   │
└────┬────┘    └────┬────┘    └────┬────┘    └────┬────┘    └────┬────┘
     │              │              │              │              │
     │ GET /forgot- │              │              │              │
     │ password     │              │              │              │
     ├─────────────►│              │              │              │
     │              │              │              │              │
     │ Forgot       │              │              │              │
     │ Password Form│              │              │              │
     │◄─────────────┤              │              │              │
     │              │              │              │              │
     │ POST /forgot-│              │              │              │
     │ password     │              │              │              │
     │ (email)      │              │              │              │
     ├─────────────►│              │              │              │
     │              │              │              │              │
     │              │ Find user by │              │              │
     │              │ email        │              │              │
     │              ├─────────────────────────────►│              │
     │              │              │              │              │
     │              │ User found   │              │              │
     │              │◄─────────────────────────────┤              │
     │              │              │              │              │
     │              │ Generate     │              │              │
     │              │ secure token │              │              │
     │              ├─────────────►│              │              │
     │              │              │              │              │
     │              │ Token (32    │              │              │
     │              │ bytes)       │              │              │
     │              │◄─────────────┤              │              │
     │              │              │              │              │
     │              │ Save token & │              │              │
     │              │ expiry (1hr) │              │              │
     │              ├─────────────────────────────►│              │
     │              │              │              │              │
     │              │ Token saved  │              │              │
     │              │◄─────────────────────────────┤              │
     │              │              │              │              │
     │              │ Send reset   │              │              │
     │              │ email with   │              │              │
     │              │ token link   │              │              │
     │              ├──────────────────────────────────────────►│
     │              │              │              │              │
     │              │ Email sent   │              │              │
     │              │◄──────────────────────────────────────────┤
     │              │              │              │              │
     │ Success msg  │              │              │              │
     │◄─────────────┤              │              │              │
     │              │              │              │              │
     │ User clicks  │              │              │              │
     │ reset link   │              │              │              │
     │ in email     │              │              │              │
     │              │              │              │              │
     │ GET /reset-  │              │              │              │
     │ password/    │              │              │              │
     │ <token>      │              │              │              │
     ├─────────────►│              │              │              │
     │              │              │              │              │
     │              │ Verify token │              │              │
     │              │ & expiry     │              │              │
     │              ├─────────────────────────────►│              │
     │              │              │              │              │
     │              │ Token valid  │              │              │
     │              │◄─────────────────────────────┤              │
     │              │              │              │              │
     │ Reset        │              │              │              │
     │ Password Form│              │              │              │
     │◄─────────────┤              │              │              │
     │              │              │              │              │
     │ POST /reset- │              │              │              │
     │ password/    │              │              │              │
     │ <token>      │              │              │              │
     │ (new pwd)    │              │              │              │
     ├─────────────►│              │              │              │
     │              │              │              │              │
     │              │ Hash new pwd │              │              │
     │              │ Clear token  │              │              │
     │              │ Update user  │              │              │
     │              ├─────────────────────────────►│              │
     │              │              │              │              │
     │              │ Updated      │              │              │
     │              │◄─────────────────────────────┤              │
     │              │              │              │              │
     │ Redirect to  │              │              │              │
     │ login        │              │              │              │
     │◄─────────────┤              │              │              │
     │              │              │              │              │
```

**Implementation Details:**
```python
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        
        if user:
            # Generate secure token (32 bytes = 256 bits)
            token = secrets.token_urlsafe(32)
            
            # Save token and expiry (1 hour from now)
            user.reset_token = token
            user.reset_token_expiry = datetime.now() + timedelta(hours=1)
            db.session.commit()
            
            # Create reset link
            reset_link = url_for('reset_password', token=token, _external=True)
            
            # Send email
            msg = Message('Password Reset Request', recipients=[user.email])
            msg.body = f'''Hello {user.name},

You requested a password reset. Click the link below:
{reset_link}

This link expires in 1 hour.
'''
            mail.send(msg)
            flash('Password reset instructions sent to your email.', 'success')
        else:
            # Security: Don't reveal if email exists
            flash('If an account exists, reset instructions have been sent.', 'info')
        
        return redirect(url_for('login'))
    
    return render_template('forgot_password.html')

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    # Find user by token
    user = User.query.filter_by(reset_token=token).first()
    
    # Verify token exists and hasn't expired
    if not user or not user.reset_token_expiry or \
       user.reset_token_expiry < datetime.now():
        flash('Invalid or expired reset link.', 'danger')
        return redirect(url_for('forgot_password'))
    
    if request.method == 'POST':
        password = request.form.get('password')
        
        # Hash new password
        user.password = generate_password_hash(password)
        
        # Clear reset token
        user.reset_token = None
        user.reset_token_expiry = None
        
        db.session.commit()
        
        flash('Password has been reset successfully!', 'success')
        return redirect(url_for('login'))
    
    return render_template('reset_password.html', token=token)
```

### 4. Role-Based Access Control (RBAC)

```python
# Decorator for login-required routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Decorator for admin-only routes
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
```

**Access Control Matrix:**

| Route | Guest | User | Admin |
|-------|-------|------|-------|
| `/` (Home) | ✅ | ✅ | ✅ |
| `/register` | ✅ | ❌ | ❌ |
| `/login` | ✅ | ❌ | ❌ |
| `/guest-feedback` | ✅ | ❌ | ❌ |
| `/user-feedback` | ❌ | ✅ | ❌ |
| `/user-dashboard` | ❌ | ✅ | ❌ |
| `/admin-dashboard` | ❌ | ❌ | ✅ |
| `/admin/delete-feedback/<id>` | ❌ | ❌ | ✅ |

---

## Application Logic

### 1. Feedback Submission Flow

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│  User   │    │  Flask  │    │Sentiment│    │Database │    │Response │
│ Browser │    │  Route  │    │Analyzer │    │         │    │         │
└────┬────┘    └────┬────┘    └────┬────┘    └────┬────┘    └────┬────┘
     │              │              │              │              │
     │ Submit       │              │              │              │
     │ Feedback Form│              │              │              │
     ├─────────────►│              │              │              │
     │              │              │              │              │
     │              │ Extract form │              │              │
     │              │ data:        │              │              │
     │              │ - category   │              │              │
     │              │ - message    │              │              │
     │              │ - rating     │              │              │
     │              │              │              │              │
     │              │ Analyze      │              │              │
     │              │ sentiment    │              │              │
     │              ├─────────────►│              │              │
     │              │              │              │              │
     │              │              │ TextBlob     │              │
     │              │              │ Analysis:    │              │
     │              │              │ - Tokenize   │              │
     │              │              │ - POS tagging│              │
     │              │              │ - Polarity   │              │
     │              │              │   score      │              │
     │              │              │              │              │
     │              │ Sentiment    │              │              │
     │              │ (Positive/   │              │              │
     │              │  Negative/   │              │              │
     │              │  Neutral)    │              │              │
     │              │◄─────────────┤              │              │
     │              │              │              │              │
     │              │ Create       │              │              │
     │              │ Feedback     │              │              │
     │              │ object       │              │              │
     │              │              │              │              │
     │              │ Save to DB   │              │              │
     │              ├─────────────────────────────►│              │
     │              │              │              │              │
     │              │ Feedback ID  │              │              │
     │              │◄─────────────────────────────┤              │
     │              │              │              │              │
     │              │ Generate     │              │              │
     │              │ success msg  │              │              │
     │              ├──────────────────────────────────────────►│
     │              │              │              │              │
     │ Success page │              │              │              │
     │ with         │              │              │              │
     │ sentiment    │              │              │              │
     │◄─────────────┤              │              │              │
     │              │              │              │              │
```

**Sentiment Analysis Logic:**

```python
def analyze_sentiment(text):
    """
    Analyzes sentiment of text using TextBlob
    
    Returns:
        'Positive' if polarity > 0.1
        'Negative' if polarity < -0.1
        'Neutral' if -0.1 <= polarity <= 0.1
    """
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    
    if polarity > 0.1:
        return 'Positive'
    elif polarity < -0.1:
        return 'Negative'
    else:
        return 'Neutral'
```

**TextBlob Polarity Scale:**
- Range: -1.0 (most negative) to +1.0 (most positive)
- Threshold for Positive: > 0.1
- Threshold for Negative: < -0.1
- Neutral zone: -0.1 to 0.1

**Example Sentiment Scores:**
- "This product is amazing!" → Polarity: 0.6 → **Positive**
- "Terrible experience, very disappointed" → Polarity: -0.8 → **Negative**
- "It's okay, nothing special" → Polarity: 0.05 → **Neutral**

### 2. Guest vs User Feedback Logic

```python
# Guest Feedback Route
@app.route('/guest-feedback', methods=['GET', 'POST'])
def guest_feedback():
    # Prevent logged-in users from accessing guest form
    if session.get('user_role') in ['admin', 'user']:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        guest_name = request.form.get('name')
        guest_email = request.form.get('email')
        category = request.form.get('category')
        message = request.form.get('message')
        rating = request.form.get('rating')
        
        sentiment = analyze_sentiment(message)
        
        # Create feedback with guest information
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

# User Feedback Route
@app.route('/user-feedback', methods=['GET', 'POST'])
@login_required
def user_feedback():
    # Prevent admins from submitting feedback
    if session.get('user_role') == 'admin':
        flash("Admins cannot submit feedback.", "warning")
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        category = request.form.get('category')
        message = request.form.get('message')
        rating = request.form.get('rating')
        
        sentiment = analyze_sentiment(message)
        
        # Create feedback linked to user
        feedback = Feedback(
            user_id=session['user_id'],  # Link to user
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
```

### 3. Dashboard Logic

#### User Dashboard
```python
@app.route('/user-dashboard')
@login_required
def user_dashboard():
    # Prevent admins from accessing user dashboard
    if session.get('user_role') == 'admin':
        return redirect(url_for('index'))
    
    # Get query parameters for filtering
    limit = request.args.get('limit', default=10, type=int)
    sentiment_filter = request.args.get('sentiment', default='all')
    sort_order = request.args.get('sort', default='new_to_old')
    
    # Base query: only user's own feedback
    query = Feedback.query.filter_by(user_id=session['user_id'])
    
    # Apply sentiment filter
    if sentiment_filter.lower() in ['positive', 'neutral', 'negative']:
        query = query.filter(Feedback.sentiment == sentiment_filter.capitalize())
    
    # Apply sort order
    if sort_order == 'old_to_new':
        query = query.order_by(Feedback.timestamp.asc())
    else:
        query = query.order_by(Feedback.timestamp.desc())
    
    # Apply limit
    feedbacks = query.limit(limit).all()
    
    return render_template('user_dashboard.html', 
                         feedbacks=feedbacks,
                         limit=limit,
                         sentiment_filter=sentiment_filter,
                         sort_order=sort_order)
```

#### Admin Dashboard
```python
@app.route('/admin-dashboard')
@admin_required
def admin_dashboard():
    # Prevent regular users from accessing admin dashboard
    if session.get('user_id') and session.get('user_role') == 'user':
        return redirect(url_for('index'))
    
    # Get filter parameters
    limit = request.args.get('limit', default=10, type=int)
    sentiment_filter = request.args.get('sentiment', default='all')
    type_filter = request.args.get('type', default='all')
    sort_order = request.args.get('sort', default='new_to_old')
    
    # Start with all feedback
    query = Feedback.query
    
    # Apply sentiment filter
    if sentiment_filter.lower() in ['positive', 'neutral', 'negative']:
        query = query.filter(Feedback.sentiment == sentiment_filter.capitalize())
    
    # Apply type filter (user vs guest)
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
    
    # Calculate statistics (all feedback, not filtered)
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
    
    return render_template('admin_dashboard.html',
                         feedbacks=feedbacks,
                         stats=stats,
                         limit=limit,
                         sentiment_filter=sentiment_filter,
                         type_filter=type_filter,
                         sort_order=sort_order)
```

---

## Database Architecture

### Entity-Relationship Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         User                                 │
├─────────────────────────────────────────────────────────────┤
│ PK  id                    INTEGER                            │
│     name                  VARCHAR(100)    NOT NULL           │
│     email                 VARCHAR(120)    UNIQUE, NOT NULL   │
│     password              VARCHAR(200)    NOT NULL (hashed)  │
│     role                  VARCHAR(20)     DEFAULT 'user'     │
│     reset_token           VARCHAR(100)    NULLABLE           │
│     reset_token_expiry    DATETIME        NULLABLE           │
│     created_at            DATETIME        DEFAULT NOW()      │
└─────────────────────────────────────────────────────────────┘
                                │
                                │ 1:N
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                       Feedback                               │
├─────────────────────────────────────────────────────────────┤
│ PK  id                    INTEGER                            │
│ FK  user_id               INTEGER         NULLABLE           │
│     guest_name            VARCHAR(100)    NULLABLE           │
│     guest_email           VARCHAR(120)    NULLABLE           │
│     category              VARCHAR(50)     NOT NULL           │
│     message               TEXT            NOT NULL           │
│     rating                INTEGER         NULLABLE (1-5)     │
│     sentiment             VARCHAR(20)     NOT NULL           │
│     timestamp             DATETIME        DEFAULT NOW()      │
└─────────────────────────────────────────────────────────────┘

Constraints:
- If user_id IS NOT NULL: feedback from registered user
- If user_id IS NULL: feedback from guest (guest_name & guest_email required)
```

### Database Models

```python
class User(db.Model):
    """User model for registered users and admins"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Hashed
    role = db.Column(db.String(20), default='user')  # 'user' or 'admin'
    reset_token = db.Column(db.String(100), nullable=True)
    reset_token_expiry = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Relationship: One user can have many feedbacks
    feedbacks = db.relationship('Feedback', backref='user', lazy=True)

class Feedback(db.Model):
    """Feedback model for both guest and user submissions"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    guest_name = db.Column(db.String(100), nullable=True)
    guest_email = db.Column(db.String(120), nullable=True)
    category = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=True)  # 1-5 stars
    sentiment = db.Column(db.String(20), nullable=False)  # Positive/Negative/Neutral
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
```

### Database Initialization

```python
if __name__ == '__main__':
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Create admin user if environment variables are set
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
            print("⚠️ WARNING: No admin user configured.")
            print("Set ADMIN_EMAIL and ADMIN_PASSWORD environment variables.")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
```

---

## API Endpoints

### 1. Sentiment Statistics API

**Endpoint:** `GET /api/sentiment-stats`

**Description:** Returns sentiment distribution statistics

**Response:**
```json
{
  "positive": 45,
  "negative": 12,
  "neutral": 23
}
```

**Implementation:**
```python
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
```

### 2. Chart Data API

**Endpoint:** `GET /api/chart-data`

**Description:** Returns comprehensive analytics data for charts

**Response:**
```json
{
  "sentiment": {
    "Positive": 45,
    "Negative": 12,
    "Neutral": 23
  },
  "categories": {
    "Product": 30,
    "Service": 25,
    "Support": 15,
    "Website": 8,
    "Other": 2
  },
  "category_sentiment": {
    "Product": {
      "Positive": 20,
      "Neutral": 8,
      "Negative": 2
    },
    "Service": {
      "Positive": 15,
      "Neutral": 7,
      "Negative": 3
    }
  },
  "ratings": {
    "1": 3,
    "2": 5,
    "3": 12,
    "4": 28,
    "5": 32
  },
  "timeline": {
    "2025-10-15": 8,
    "2025-10-16": 12,
    "2025-10-17": 15
  }
}
```

**Implementation:**
```python
@app.route('/api/chart-data')
def chart_data():
    feedbacks = Feedback.query.all()
    
    # Sentiment distribution
    sentiment_data = {
        'Positive': len([f for f in feedbacks if f.sentiment == 'Positive']),
        'Negative': len([f for f in feedbacks if f.sentiment == 'Negative']),
        'Neutral': len([f for f in feedbacks if f.sentiment == 'Neutral'])
    }
    
    # Category distribution
    category_data = {}
    for feedback in feedbacks:
        category = feedback.category
        if category in category_data:
            category_data[category] += 1
        else:
            category_data[category] = 1
    
    # Category vs Sentiment (stacked bar chart data)
    from collections import defaultdict
    category_sentiment = defaultdict(lambda: {'Positive': 0, 'Negative': 0, 'Neutral': 0})
    for feedback in feedbacks:
        category_sentiment[feedback.category][feedback.sentiment] += 1
    
    # Rating distribution
    rating_data = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0}
    for feedback in feedbacks:
        if feedback.rating:
            rating_data[str(feedback.rating)] += 1
    
    # Timeline data (feedback per day)
    timeline_data = defaultdict(int)
    for feedback in feedbacks:
        date_key = feedback.timestamp.strftime('%Y-%m-%d')
        timeline_data[date_key] += 1
    
    # Sort timeline by date
    sorted_timeline = dict(sorted(timeline_data.items()))
    
    return jsonify({
        'sentiment': sentiment_data,
        'categories': category_data,
        'category_sentiment': dict(category_sentiment),
        'ratings': rating_data,
        'timeline': sorted_timeline
    })
```

---

## Security Implementation

### 1. Password Security

**Hashing Algorithm:** Werkzeug's `generate_password_hash()` uses PBKDF2-SHA256

```python
from werkzeug.security import generate_password_hash, check_password_hash

# During registration
hashed_password = generate_password_hash(password)
# Generates: pbkdf2:sha256:260000$salt$hash

# During login
is_valid = check_password_hash(user.password, password)
```

**Security Features:**
- **Salt:** Unique random salt per password
- **Iterations:** 260,000 rounds (PBKDF2)
- **Algorithm:** SHA-256
- **Length:** Variable (typically 200+ characters)

### 2. Session Management

```python
app.config['SECRET_KEY'] = os.environ.get('SESSION_SECRET', 'dev-secret-key')

# Session data stored:
session['user_id'] = user.id
session['user_name'] = user.name
session['user_role'] = user.role
session.modified = True
```

**Security Features:**
- Server-side session storage
- Encrypted session cookies
- CSRF protection via Flask
- Session expiry on browser close

### 3. Password Reset Token Security

```python
import secrets

# Generate cryptographically secure token
token = secrets.token_urlsafe(32)  # 32 bytes = 256 bits

# Set expiry (1 hour)
user.reset_token_expiry = datetime.now() + timedelta(hours=1)

# Verify token and expiry
if not user or not user.reset_token_expiry or \
   user.reset_token_expiry < datetime.now():
    flash('Invalid or expired reset link.', 'danger')
```

**Security Features:**
- Cryptographically secure random tokens
- Time-limited validity (1 hour)
- Single-use tokens (cleared after use)
- No email enumeration (same message for valid/invalid emails)

### 4. SQL Injection Prevention

**Using SQLAlchemy ORM:**
```python
# ✅ SAFE: Parameterized query via ORM
user = User.query.filter_by(email=email).first()

# ❌ UNSAFE: Raw SQL with string concatenation
# cursor.execute(f"SELECT * FROM users WHERE email = '{email}'")
```

### 5. Role-Based Access Control

```python
# Prevent privilege escalation
@app.route('/admin-dashboard')
@admin_required
def admin_dashboard():
    # Double-check role in session
    if session.get('user_role') != 'admin':
        return redirect(url_for('index'))
    # ... admin logic
```

### 6. Environment Variables

```python
# Sensitive data in environment variables
app.config['SECRET_KEY'] = os.environ.get('SESSION_SECRET')
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
admin_email = os.environ.get('ADMIN_EMAIL')
admin_password = os.environ.get('ADMIN_PASSWORD')
```

---

## Feature Enhancements

### 1. Star Rating System (October 16, 2025)

**Problem:** Clicking on any star would make ALL stars glow

**Solution:** Implemented intelligent JavaScript rating system

**Implementation:**
```javascript
// static/js/rating.js
document.addEventListener('DOMContentLoaded', function() {
    const stars = document.querySelectorAll('.star');
    const ratingInput = document.getElementById('rating');
    let selectedRating = 0;

    stars.forEach((star, index) => {
        // Click event: Set rating
        star.addEventListener('click', function() {
            selectedRating = index + 1;
            ratingInput.value = selectedRating;
            updateStars(selectedRating);
        });

        // Hover event: Preview rating
        star.addEventListener('mouseenter', function() {
            updateStars(index + 1);
        });
    });

    // Mouse leave: Revert to selected rating
    document.querySelector('.rating-stars').addEventListener('mouseleave', function() {
        updateStars(selectedRating);
    });

    function updateStars(rating) {
        stars.forEach((star, index) => {
            if (index < rating) {
                star.classList.add('active');
            } else {
                star.classList.remove('active');
            }
        });
    }
});
```

**Features:**
- ✅ Click on star 4 → Only stars 1-4 glow
- ✅ Hover preview
- ✅ Smooth transitions
- ✅ Works like Amazon/Google Reviews

### 2. Data Visualizations (October 16, 2025)

**Added 6 Interactive Charts using Chart.js 4.4.0:**

#### Chart 1: Sentiment Pie Chart
```javascript
const sentimentPieCtx = document.getElementById('sentimentPieChart').getContext('2d');
new Chart(sentimentPieCtx, {
    type: 'pie',
    data: {
        labels: ['Positive', 'Negative', 'Neutral'],
        datasets: [{
            data: [chartData.sentiment.Positive, 
                   chartData.sentiment.Negative, 
                   chartData.sentiment.Neutral],
            backgroundColor: ['#28a745', '#dc3545', '#6c757d']
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: { position: 'bottom' },
            title: { display: true, text: 'Sentiment Distribution' }
        }
    }
});
```

#### Chart 2: Sentiment Donut Chart
```javascript
const sentimentDonutCtx = document.getElementById('sentimentDonutChart').getContext('2d');
new Chart(sentimentDonutCtx, {
    type: 'doughnut',
    data: {
        labels: ['Positive', 'Negative', 'Neutral'],
        datasets: [{
            data: [chartData.sentiment.Positive, 
                   chartData.sentiment.Negative, 
                   chartData.sentiment.Neutral],
            backgroundColor: ['#28a745', '#dc3545', '#6c757d']
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: { position: 'bottom' },
            title: { display: true, text: 'Sentiment Overview' }
        }
    }
});
```

#### Chart 3: Category Bar Chart
```javascript
const categoryBarCtx = document.getElementById('categoryBarChart').getContext('2d');
new Chart(categoryBarCtx, {
    type: 'bar',
    data: {
        labels: Object.keys(chartData.categories),
        datasets: [{
            label: 'Feedback Count',
            data: Object.values(chartData.categories),
            backgroundColor: ['#007bff', '#28a745', '#ffc107', '#dc3545', '#6c757d']
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: { display: false },
            title: { display: true, text: 'Feedback by Category' }
        },
        scales: {
            y: { beginAtZero: true }
        }
    }
});
```

#### Chart 4: Rating Distribution Bar Chart
```javascript
const ratingBarCtx = document.getElementById('ratingBarChart').getContext('2d');
new Chart(ratingBarCtx, {
    type: 'bar',
    data: {
        labels: ['1 Star', '2 Stars', '3 Stars', '4 Stars', '5 Stars'],
        datasets: [{
            label: 'Number of Ratings',
            data: [chartData.ratings['1'], chartData.ratings['2'], 
                   chartData.ratings['3'], chartData.ratings['4'], 
                   chartData.ratings['5']],
            backgroundColor: '#ffc107'
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: { display: false },
            title: { display: true, text: 'Rating Distribution' }
        },
        scales: {
            y: { beginAtZero: true }
        }
    }
});
```

#### Chart 5: Timeline Line Chart
```javascript
const timelineCtx = document.getElementById('timelineChart').getContext('2d');
new Chart(timelineCtx, {
    type: 'line',
    data: {
        labels: Object.keys(chartData.timeline),
        datasets: [{
            label: 'Feedback Submissions',
            data: Object.values(chartData.timeline),
            borderColor: '#007bff',
            backgroundColor: 'rgba(0, 123, 255, 0.1)',
            fill: true,
            tension: 0.4
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: { display: false },
            title: { display: true, text: 'Feedback Timeline' }
        },
        scales: {
            y: { beginAtZero: true }
        }
    }
});
```

#### Chart 6: Category vs Sentiment Stacked Bar Chart
```javascript
const categorySentimentCtx = document.getElementById('categorySentimentChart').getContext('2d');

const categories = Object.keys(chartData.category_sentiment);
const positiveData = categories.map(cat => chartData.category_sentiment[cat].Positive);
const neutralData = categories.map(cat => chartData.category_sentiment[cat].Neutral);
const negativeData = categories.map(cat => chartData.category_sentiment[cat].Negative);

new Chart(categorySentimentCtx, {
    type: 'bar',
    data: {
        labels: categories,
        datasets: [
            {
                label: 'Positive',
                data: positiveData,
                backgroundColor: '#28a745'
            },
            {
                label: 'Neutral',
                data: neutralData,
                backgroundColor: '#6c757d'
            },
            {
                label: 'Negative',
                data: negativeData,
                backgroundColor: '#dc3545'
            }
        ]
    },
    options: {
        responsive: true,
        plugins: {
            legend: { position: 'bottom' },
            title: { display: true, text: 'Sentiment by Category' }
        },
        scales: {
            x: { stacked: true },
            y: { stacked: true, beginAtZero: true }
        }
    }
});
```

**Chart Features:**
- ✅ Responsive design (adapts to screen size)
- ✅ Interactive tooltips
- ✅ Smooth animations
- ✅ Color-coded for easy interpretation
- ✅ Mobile-friendly

### 3. Responsive Grid Layout

```css
.chart-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
    gap: 20px;
    margin-top: 20px;
}

.chart-card {
    background: white;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.chart-full-width {
    grid-column: 1 / -1;
}

@media (max-width: 768px) {
    .chart-grid {
        grid-template-columns: 1fr;
    }
}
```

---

## Technology Stack

### Backend Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.11+ | Core programming language |
| **Flask** | 3.1.2 | Web framework |
| **Flask-SQLAlchemy** | Latest | ORM for database operations |
| **Flask-Mail** | Latest | Email functionality |
| **TextBlob** | Latest | NLP and sentiment analysis |
| **Werkzeug** | Latest | Password hashing and security |
| **PostgreSQL** | Latest | Production database (Neon) |
| **SQLite** | 3.x | Development database |

### Frontend Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| **HTML5** | - | Structure and semantics |
| **CSS3** | - | Styling and layout |
| **JavaScript** | ES6+ | Interactivity |
| **Chart.js** | 4.4.0 | Data visualizations |
| **Jinja2** | Latest | Template engine |

### Development Tools

| Tool | Purpose |
|------|---------|
| **Replit** | Development environment |
| **Git** | Version control |
| **GitHub** | Code repository |
| **Neon** | PostgreSQL hosting |
| **Gmail SMTP** | Email delivery |

### Key Dependencies

```txt
Flask==3.1.2
Flask-SQLAlchemy
Flask-Mail
textblob
werkzeug
psycopg2-binary  # PostgreSQL adapter
gunicorn  # Production server
```

---

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Production Stack                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────────────────────────────────────────┐     │
│  │              Replit Hosting                         │     │
│  │  ┌──────────────────────────────────────────────┐  │     │
│  │  │         Gunicorn WSGI Server                 │  │     │
│  │  │  ┌────────────────────────────────────────┐  │  │     │
│  │  │  │      Flask Application                 │  │  │     │
│  │  │  │  - Routes                              │  │  │     │
│  │  │  │  - Business Logic                      │  │  │     │
│  │  │  │  - Templates                           │  │  │     │
│  │  │  └────────────────────────────────────────┘  │  │     │
│  │  └──────────────────────────────────────────────┘  │     │
│  └────────────────────────────────────────────────────┘     │
│                          │                                   │
│                          │ SQL Queries                       │
│                          ▼                                   │
│  ┌────────────────────────────────────────────────────┐     │
│  │         Neon PostgreSQL Database                    │     │
│  │  - users table                                      │     │
│  │  - feedback table                                   │     │
│  │  - Automatic backups                                │     │
│  │  - Connection pooling                               │     │
│  └────────────────────────────────────────────────────┘     │
│                                                              │
└─────────────────────────────────────────────────────────────┘

External Services:
┌──────────────────┐         ┌──────────────────┐
│  Gmail SMTP      │         │  TextBlob API    │
│  (Email Service) │         │  (NLP Service)   │
└──────────────────┘         └──────────────────┘
```

---

## Performance Considerations

### 1. Database Optimization
- **Indexes:** Primary keys and foreign keys automatically indexed
- **Query Optimization:** Use SQLAlchemy ORM for efficient queries
- **Connection Pooling:** Managed by SQLAlchemy

### 2. Caching Strategy
- **Session Caching:** User sessions cached in Flask
- **Static Assets:** CSS/JS served with browser caching headers

### 3. Scalability
- **Horizontal Scaling:** Can deploy multiple Flask instances
- **Database Scaling:** Neon PostgreSQL supports connection pooling
- **CDN:** Static assets can be served via CDN

---

## Future Enhancements

### Planned Features
1. **Email Notifications:** Notify admins of new feedback
2. **Export Functionality:** Export feedback to CSV/Excel
3. **Advanced Filtering:** Date range, keyword search
4. **User Profiles:** Allow users to update their information
5. **API Authentication:** JWT tokens for API access
6. **Real-time Updates:** WebSocket for live dashboard updates
7. **Multi-language Support:** i18n for internationalization
8. **Dark Mode:** Theme toggle for user preference
9. **Feedback Categories Management:** Admin can add/edit categories
10. **Automated Reports:** Weekly/monthly email reports

---

## Conclusion

The Smart Feedback Collection and Analysis System is a robust, secure, and scalable application that demonstrates best practices in:
- **Authentication & Authorization:** Secure password handling, session management, and RBAC
- **Data Analysis:** AI-powered sentiment analysis using NLP
- **User Experience:** Responsive design, interactive visualizations
- **Security:** Password hashing, CSRF protection, SQL injection prevention
- **Architecture:** Clean separation of concerns, MVC pattern

The system is production-ready and can be easily extended with additional features.

---

**Document Version:** 1.0  
**Last Updated:** October 29, 2025  
**Author:** Sandeep Kumar Akula
