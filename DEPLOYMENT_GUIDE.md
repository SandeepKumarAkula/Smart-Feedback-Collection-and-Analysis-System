# 🚀 Deployment Guide - Smart Feedback Collection and Analysis System

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Database Configuration](#database-configuration)
4. [Email Service Setup](#email-service-setup)
5. [Deployment Platforms](#deployment-platforms)
6. [Production Checklist](#production-checklist)
7. [Monitoring & Maintenance](#monitoring--maintenance)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements

- **Python:** 3.11 or higher
- **Database:** PostgreSQL 12+ (production) or SQLite 3+ (development)
- **Memory:** Minimum 512MB RAM
- **Storage:** Minimum 1GB disk space
- **Network:** HTTPS support recommended

### Required Accounts

1. **GitHub Account** - For code repository
2. **Neon Account** - For PostgreSQL database (or alternative PostgreSQL provider)
3. **Gmail Account** - For email service (with 2FA enabled)
4. **Deployment Platform Account** - Replit, Heroku, AWS, etc.

---

## Environment Setup

### 1. Clone the Repository

```bash
git clone https://github.com/SandeepKumarAkula/Smart-Feedback-Collection-and-Analysis-System.git
cd Smart-Feedback-Collection-and-Analysis-System
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt:**
```txt
Flask==3.1.2
Flask-SQLAlchemy
Flask-Mail
textblob
werkzeug
psycopg2-binary
gunicorn
python-dotenv
```

### 4. Download TextBlob Corpora

```bash
python -m textblob.download_corpora
```

---

## Database Configuration

### Option 1: PostgreSQL (Production - Recommended)

#### Using Neon (Serverless PostgreSQL)

1. **Create Neon Account**
   - Visit: https://neon.tech
   - Sign up for free account
   - Create new project

2. **Get Connection String**
   ```
   postgresql://username:password@host.neon.tech/dbname?sslmode=require
   ```

3. **Set Environment Variable**
   ```bash
   export DATABASE_URL="postgresql://username:password@host.neon.tech/dbname?sslmode=require"
   ```

#### Using Other PostgreSQL Providers

**AWS RDS:**
```bash
export DATABASE_URL="postgresql://username:password@your-rds-endpoint.amazonaws.com:5432/dbname"
```

**Heroku Postgres:**
```bash
# Automatically set by Heroku
heroku addons:create heroku-postgresql:mini
```

**DigitalOcean Managed Database:**
```bash
export DATABASE_URL="postgresql://username:password@your-db.db.ondigitalocean.com:25060/dbname?sslmode=require"
```

### Option 2: SQLite (Development Only)

```bash
# SQLite is used by default if DATABASE_URL is not set
# Database file: instance/feedback.db
```

**⚠️ Warning:** SQLite is NOT recommended for production due to:
- Limited concurrent write operations
- No built-in replication
- File-based storage limitations

---

## Email Service Setup

### Gmail SMTP Configuration

#### Step 1: Enable 2-Factor Authentication

1. Go to Google Account settings
2. Navigate to Security
3. Enable 2-Step Verification

#### Step 2: Generate App Password

1. Go to: https://myaccount.google.com/apppasswords
2. Select "Mail" and "Other (Custom name)"
3. Enter "Feedback System"
4. Click "Generate"
5. Copy the 16-character password

#### Step 3: Set Environment Variables

```bash
export MAIL_USERNAME="your-email@gmail.com"
export MAIL_PASSWORD="your-16-char-app-password"
```

### Alternative Email Providers

#### SendGrid

```python
app.config['MAIL_SERVER'] = 'smtp.sendgrid.net'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'apikey'
app.config['MAIL_PASSWORD'] = os.environ.get('SENDGRID_API_KEY')
```

#### AWS SES

```python
app.config['MAIL_SERVER'] = 'email-smtp.us-east-1.amazonaws.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.environ.get('AWS_SES_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('AWS_SES_PASSWORD')
```

#### Mailgun

```python
app.config['MAIL_SERVER'] = 'smtp.mailgun.org'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.environ.get('MAILGUN_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAILGUN_PASSWORD')
```

---

## Deployment Platforms

### Option 1: Replit (Recommended for Beginners)

#### Advantages
- ✅ Zero configuration
- ✅ Built-in IDE
- ✅ Automatic HTTPS
- ✅ Free tier available
- ✅ Easy environment variable management

#### Deployment Steps

1. **Import from GitHub**
   - Go to https://replit.com
   - Click "Create Repl"
   - Select "Import from GitHub"
   - Enter repository URL

2. **Configure Environment Variables**
   - Click "Secrets" (lock icon) in left sidebar
   - Add the following secrets:
     ```
     SESSION_SECRET=your-secret-key-here
     DATABASE_URL=your-postgresql-connection-string
     MAIL_USERNAME=your-email@gmail.com
     MAIL_PASSWORD=your-app-password
     ADMIN_EMAIL=admin@yourdomain.com
     ADMIN_PASSWORD=secure-admin-password
     ```

3. **Configure Replit**
   - Create `.replit` file:
     ```toml
     run = "python app.py"
     
     [nix]
     channel = "stable-23_11"
     
     [deployment]
     run = ["sh", "-c", "gunicorn app:app --bind 0.0.0.0:5000"]
     ```

4. **Run the Application**
   - Click "Run" button
   - Application will be available at: `https://your-repl-name.your-username.repl.co`

5. **Deploy to Production**
   - Click "Deploy" button
   - Choose deployment type (Reserved VM recommended)
   - Configure custom domain (optional)

---

### Option 2: Heroku

#### Advantages
- ✅ Easy deployment via Git
- ✅ Automatic scaling
- ✅ Add-ons marketplace
- ✅ Free tier available

#### Deployment Steps

1. **Install Heroku CLI**
   ```bash
   # Mac
   brew tap heroku/brew && brew install heroku
   
   # Ubuntu
   curl https://cli-assets.heroku.com/install.sh | sh
   
   # Windows
   # Download from: https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku App**
   ```bash
   heroku create your-app-name
   ```

4. **Add PostgreSQL**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

5. **Set Environment Variables**
   ```bash
   heroku config:set SESSION_SECRET="your-secret-key"
   heroku config:set MAIL_USERNAME="your-email@gmail.com"
   heroku config:set MAIL_PASSWORD="your-app-password"
   heroku config:set ADMIN_EMAIL="admin@yourdomain.com"
   heroku config:set ADMIN_PASSWORD="secure-password"
   ```

6. **Create Procfile**
   ```bash
   echo "web: gunicorn app:app" > Procfile
   ```

7. **Deploy**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

8. **Open Application**
   ```bash
   heroku open
   ```

---

### Option 3: AWS EC2

#### Advantages
- ✅ Full control over infrastructure
- ✅ Highly scalable
- ✅ Integration with AWS services
- ✅ Free tier available (12 months)

#### Deployment Steps

1. **Launch EC2 Instance**
   - Go to AWS Console → EC2
   - Click "Launch Instance"
   - Choose Ubuntu Server 22.04 LTS
   - Select t2.micro (free tier eligible)
   - Configure security group (allow ports 22, 80, 443)
   - Launch and download key pair

2. **Connect to Instance**
   ```bash
   chmod 400 your-key.pem
   ssh -i your-key.pem ubuntu@your-ec2-ip
   ```

3. **Install Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv nginx -y
   ```

4. **Clone Repository**
   ```bash
   cd /home/ubuntu
   git clone https://github.com/SandeepKumarAkula/Smart-Feedback-Collection-and-Analysis-System.git
   cd Smart-Feedback-Collection-and-Analysis-System
   ```

5. **Setup Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python -m textblob.download_corpora
   ```

6. **Create Environment File**
   ```bash
   nano .env
   ```
   
   Add:
   ```
   SESSION_SECRET=your-secret-key
   DATABASE_URL=your-postgresql-url
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   ADMIN_EMAIL=admin@yourdomain.com
   ADMIN_PASSWORD=secure-password
   ```

7. **Create Systemd Service**
   ```bash
   sudo nano /etc/systemd/system/feedback.service
   ```
   
   Add:
   ```ini
   [Unit]
   Description=Feedback System
   After=network.target
   
   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu/Smart-Feedback-Collection-and-Analysis-System
   Environment="PATH=/home/ubuntu/Smart-Feedback-Collection-and-Analysis-System/venv/bin"
   EnvironmentFile=/home/ubuntu/Smart-Feedback-Collection-and-Analysis-System/.env
   ExecStart=/home/ubuntu/Smart-Feedback-Collection-and-Analysis-System/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 app:app
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```

8. **Configure Nginx**
   ```bash
   sudo nano /etc/nginx/sites-available/feedback
   ```
   
   Add:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

9. **Enable and Start Services**
   ```bash
   sudo ln -s /etc/nginx/sites-available/feedback /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   sudo systemctl enable feedback
   sudo systemctl start feedback
   ```

10. **Setup SSL with Let's Encrypt**
    ```bash
    sudo apt install certbot python3-certbot-nginx -y
    sudo certbot --nginx -d your-domain.com
    ```

---

### Option 4: DigitalOcean App Platform

#### Advantages
- ✅ Simple deployment
- ✅ Automatic HTTPS
- ✅ Built-in monitoring
- ✅ Easy scaling

#### Deployment Steps

1. **Create App**
   - Go to DigitalOcean Console
   - Click "Create" → "Apps"
   - Connect GitHub repository

2. **Configure Build**
   - Build Command: `pip install -r requirements.txt && python -m textblob.download_corpora`
   - Run Command: `gunicorn app:app --bind 0.0.0.0:8080`

3. **Add Environment Variables**
   - Add all required environment variables in App settings

4. **Deploy**
   - Click "Deploy"
   - Application will be available at: `https://your-app.ondigitalocean.app`

---

## Production Checklist

### Security

- [ ] Change `SESSION_SECRET` to a strong random value
- [ ] Use HTTPS (SSL/TLS certificate)
- [ ] Set strong `ADMIN_PASSWORD`
- [ ] Enable database SSL connections
- [ ] Configure CORS if needed
- [ ] Implement rate limiting
- [ ] Enable security headers
- [ ] Regular security updates

### Performance

- [ ] Use production WSGI server (Gunicorn)
- [ ] Configure multiple workers
- [ ] Enable database connection pooling
- [ ] Implement caching (Redis/Memcached)
- [ ] Optimize database queries
- [ ] Enable gzip compression
- [ ] Use CDN for static assets

### Monitoring

- [ ] Setup error logging (Sentry)
- [ ] Configure application monitoring (New Relic, DataDog)
- [ ] Setup uptime monitoring (UptimeRobot)
- [ ] Configure database backups
- [ ] Setup log aggregation
- [ ] Monitor disk space
- [ ] Track performance metrics

### Backup

- [ ] Automated database backups
- [ ] Backup retention policy
- [ ] Test restore procedures
- [ ] Backup environment variables
- [ ] Document recovery procedures

---

## Monitoring & Maintenance

### Application Monitoring

#### Using Sentry for Error Tracking

1. **Install Sentry SDK**
   ```bash
   pip install sentry-sdk[flask]
   ```

2. **Configure in app.py**
   ```python
   import sentry_sdk
   from sentry_sdk.integrations.flask import FlaskIntegration
   
   sentry_sdk.init(
       dsn=os.environ.get('SENTRY_DSN'),
       integrations=[FlaskIntegration()],
       traces_sample_rate=1.0
   )
   ```

### Database Backups

#### Automated PostgreSQL Backups

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"
DB_URL="your-database-url"

pg_dump $DB_URL > $BACKUP_DIR/backup_$DATE.sql
gzip $BACKUP_DIR/backup_$DATE.sql

# Keep only last 7 days
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +7 -delete
```

**Setup Cron Job:**
```bash
crontab -e

# Add: Daily backup at 2 AM
0 2 * * * /path/to/backup.sh
```

### Log Management

#### Configure Logging

```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('logs/feedback.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Feedback System startup')
```

---

## Troubleshooting

### Common Issues

#### Issue 1: Database Connection Errors

**Symptoms:**
```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Solutions:**
1. Verify `DATABASE_URL` is correct
2. Check database server is running
3. Verify firewall allows connections
4. Check SSL requirements (`?sslmode=require`)

#### Issue 2: Email Not Sending

**Symptoms:**
- Password reset emails not received
- No error messages

**Solutions:**
1. Verify Gmail app password is correct
2. Check 2FA is enabled on Gmail account
3. Verify `MAIL_USERNAME` and `MAIL_PASSWORD` are set
4. Check spam folder
5. Test with different email provider

#### Issue 3: Admin Dashboard Not Accessible

**Symptoms:**
- "Admin access required" message
- Can't login as admin

**Solutions:**
1. Verify `ADMIN_EMAIL` and `ADMIN_PASSWORD` are set
2. Check admin user exists in database:
   ```python
   from app import db, User
   admin = User.query.filter_by(role='admin').first()
   print(admin.email if admin else "No admin found")
   ```
3. Manually create admin user:
   ```python
   from app import db, User, app
   from werkzeug.security import generate_password_hash
   
   with app.app_context():
       admin = User(
           name='Admin',
           email='admin@example.com',
           password=generate_password_hash('SecurePassword123!'),
           role='admin'
       )
       db.session.add(admin)
       db.session.commit()
   ```

#### Issue 4: Charts Not Displaying

**Symptoms:**
- Blank chart areas
- JavaScript errors in console

**Solutions:**
1. Check Chart.js CDN is accessible
2. Verify `/api/chart-data` returns valid JSON
3. Check browser console for errors
4. Clear browser cache
5. Test in different browser

#### Issue 5: High Memory Usage

**Symptoms:**
- Application crashes
- Out of memory errors

**Solutions:**
1. Reduce Gunicorn workers:
   ```bash
   gunicorn app:app --workers 2 --bind 0.0.0.0:5000
   ```
2. Implement database connection pooling
3. Add pagination to large queries
4. Upgrade server resources

---

## Performance Optimization

### 1. Database Optimization

```python
# Add indexes
class Feedback(db.Model):
    __table_args__ = (
        db.Index('idx_sentiment', 'sentiment'),
        db.Index('idx_timestamp', 'timestamp'),
        db.Index('idx_user_id', 'user_id'),
    )
```

### 2. Caching with Redis

```python
from flask_caching import Cache

cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': os.environ.get('REDIS_URL')
})

@app.route('/api/chart-data')
@cache.cached(timeout=300)  # Cache for 5 minutes
def chart_data():
    # ... implementation
```

### 3. Gunicorn Configuration

```python
# gunicorn.conf.py
workers = 3
worker_class = 'sync'
worker_connections = 1000
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 50
```

---

## Scaling Strategies

### Horizontal Scaling

1. **Load Balancer Setup**
   - Use Nginx or AWS ELB
   - Distribute traffic across multiple instances
   - Implement session affinity

2. **Database Replication**
   - Setup read replicas
   - Use connection pooling
   - Implement caching layer

3. **CDN for Static Assets**
   - Use CloudFlare or AWS CloudFront
   - Cache CSS, JS, images
   - Reduce server load

---

## Security Hardening

### 1. Security Headers

```python
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response
```

### 2. Rate Limiting

```python
from flask_limiter import Limiter

limiter = Limiter(
    app,
    key_func=lambda: request.remote_addr,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/guest-feedback', methods=['POST'])
@limiter.limit("10 per hour")
def guest_feedback():
    # ... implementation
```

---

## Conclusion

This deployment guide covers multiple deployment options and best practices for running the Smart Feedback Collection and Analysis System in production. Choose the deployment platform that best fits your needs and follow the security and performance recommendations for a robust production deployment.

For additional support, refer to:
- **ARCHITECTURE.md** - Technical architecture details
- **API_REFERENCE.md** - API documentation
- **SETUP.md** - Configuration guide

---

**Document Version:** 1.0  
**Last Updated:** October 29, 2025  
**Author:** Sandeep Kumar Akula
