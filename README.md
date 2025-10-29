# 📚 Smart Feedback Collection and Analysis System - Complete Documentation

Welcome to the comprehensive documentation for the Smart Feedback Collection and Analysis System!

## 📖 Documentation Structure

This documentation package includes detailed information about every aspect of the system:

### 1. **ARCHITECTURE.md** - System Architecture & Technical Details
   - Complete system architecture with diagrams
   - Authentication flow (Registration, Login, Password Recovery)
   - Application logic and business rules
   - Database architecture and ER diagrams
   - API endpoints documentation
   - Security implementation details
   - Feature enhancements timeline
   - Technology stack breakdown

### 2. **SETUP.md** - Setup & Configuration Guide
   - Quick start instructions
   - Environment variable configuration
   - Admin account setup
   - Email service configuration
   - Database setup
   - Deployment instructions

### 3. **FEATURES.md** - Feature Documentation
   - Star rating system enhancement
   - Data visualization charts (6 types)
   - Technical improvements
   - UI/UX enhancements
   - Performance optimizations

### 4. **API_REFERENCE.md** - API Documentation
   - Complete API endpoint reference
   - Request/response examples
   - Authentication requirements
   - Error handling

## 🎯 Quick Navigation

### For Developers
- **Getting Started:** Start with `SETUP.md`
- **Understanding the System:** Read `ARCHITECTURE.md`
- **API Integration:** Check `API_REFERENCE.md`

### For System Administrators
- **Deployment:** See `SETUP.md` → Deployment section
- **Configuration:** See `SETUP.md` → Configuration section
- **Security:** See `ARCHITECTURE.md` → Security Implementation

### For Project Managers
- **Features Overview:** Read `FEATURES.md`
- **System Capabilities:** See `ARCHITECTURE.md` → System Overview
- **Technology Stack:** See `ARCHITECTURE.md` → Technology Stack

## 🏗️ System Overview

The Smart Feedback Collection and Analysis System is a full-stack web application that enables organizations to:

- ✅ Collect feedback from guests and registered users
- ✅ Automatically analyze sentiment using AI (TextBlob NLP)
- ✅ Visualize data with 6 interactive charts
- ✅ Manage feedback with role-based access control
- ✅ Secure authentication with password recovery
- ✅ Export and analyze feedback trends

## 🚀 Key Features

### Three User Roles
1. **Guest Users** - Submit anonymous feedback
2. **Registered Users** - Track personal feedback history
3. **Admin Users** - Full analytics and management dashboard

### AI-Powered Analysis
- Automatic sentiment detection (Positive/Negative/Neutral)
- Real-time analysis using TextBlob NLP
- Visual sentiment indicators

### Interactive Visualizations
- Sentiment Pie Chart
- Sentiment Donut Chart
- Category Bar Chart
- Rating Distribution Chart
- Timeline Line Chart
- Category vs Sentiment Stacked Bar Chart

### Security Features
- Password hashing with PBKDF2-SHA256
- Secure session management
- Role-based access control (RBAC)
- Time-limited password reset tokens
- SQL injection prevention via ORM

## 📊 Technology Stack

### Backend
- **Flask 3.1.2** - Web framework
- **SQLAlchemy** - ORM
- **TextBlob** - Sentiment analysis
- **PostgreSQL** - Database (Neon)
- **Flask-Mail** - Email service

### Frontend
- **HTML5/CSS3** - Structure and styling
- **JavaScript ES6+** - Interactivity
- **Chart.js 4.4.0** - Data visualizations
- **Jinja2** - Template engine

## 📁 Project Structure

```
Smart-Feedback-Collection-and-Analysis-System/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── instance/                   # Instance-specific files
│   └── feedback.db            # SQLite database (dev)
├── static/                     # Static assets
│   ├── css/
│   │   └── style.css          # Main stylesheet
│   └── js/
│       └── rating.js          # Star rating functionality
├── templates/                  # HTML templates
│   ├── base.html              # Base template
│   ├── index.html             # Home page
│   ├── login.html             # Login page
│   ├── register.html          # Registration page
│   ├── forgot_password.html   # Password recovery
│   ├── reset_password.html    # Password reset
│   ├── guest_feedback.html    # Guest feedback form
│   ├── user_feedback.html     # User feedback form
│   ├── user_dashboard.html    # User dashboard
│   └── admin_dashboard.html   # Admin dashboard
└── docs/                       # Documentation
    ├── README.md              # This file
    ├── ARCHITECTURE.md        # Architecture documentation
    ├── SETUP.md               # Setup guide
    ├── FEATURES.md            # Feature documentation
    └── API_REFERENCE.md       # API documentation
```

## 🔐 Security Highlights

### Password Security
- **Algorithm:** PBKDF2-SHA256
- **Iterations:** 260,000 rounds
- **Salt:** Unique per password
- **Storage:** Never stored in plain text

### Session Security
- Server-side session storage
- Encrypted session cookies
- CSRF protection
- Automatic expiry

### Password Reset Security
- Cryptographically secure tokens (256-bit)
- Time-limited validity (1 hour)
- Single-use tokens
- No email enumeration

## 📈 Database Schema

### Users Table
```sql
CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(200) NOT NULL,
    role VARCHAR(20) DEFAULT 'user',
    reset_token VARCHAR(100),
    reset_token_expiry DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Feedback Table
```sql
CREATE TABLE feedback (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES user(id),
    guest_name VARCHAR(100),
    guest_email VARCHAR(120),
    category VARCHAR(50) NOT NULL,
    message TEXT NOT NULL,
    rating INTEGER CHECK(rating >= 1 AND rating <= 5),
    sentiment VARCHAR(20) NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 🌐 API Endpoints

### Public Routes
- `GET /` - Home page
- `GET /register` - Registration page
- `POST /register` - Create new user
- `GET /login` - Login page
- `POST /login` - Authenticate user
- `GET /guest-feedback` - Guest feedback form
- `POST /guest-feedback` - Submit guest feedback

### Protected Routes (Login Required)
- `GET /user-feedback` - User feedback form
- `POST /user-feedback` - Submit user feedback
- `GET /user-dashboard` - User's feedback history
- `GET /logout` - Logout user

### Admin Routes (Admin Only)
- `GET /admin-dashboard` - Admin analytics dashboard
- `POST /admin/delete-feedback/<id>` - Delete feedback

### API Routes
- `GET /api/sentiment-stats` - Sentiment statistics (JSON)
- `GET /api/chart-data` - Comprehensive chart data (JSON)

## 🎨 UI/UX Features

### Responsive Design
- Mobile-first approach
- Breakpoints: 320px, 768px, 1024px, 1200px+
- Touch-friendly interactions
- Optimized for all devices

### Modern UI Elements
- Card-based layout
- Gradient backgrounds
- Smooth animations
- Color-coded sentiment badges
- Interactive star ratings
- Dynamic charts

## 📊 Analytics & Insights

### Available Metrics
- Total feedback count
- Sentiment distribution (Positive/Negative/Neutral)
- Category breakdown
- Rating distribution (1-5 stars)
- Feedback timeline
- Category vs Sentiment analysis

### Filtering Options
- By sentiment (Positive/Negative/Neutral/All)
- By type (User/Guest/All)
- By date (Newest/Oldest)
- By limit (10/25/50/100/All)

## 🚀 Deployment

### Environment Variables Required
```bash
# Session Security
SESSION_SECRET=your-secret-key-here

# Database
DATABASE_URL=postgresql://user:pass@host:port/dbname

# Email Service (Optional)
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Admin Account
ADMIN_EMAIL=admin@yourdomain.com
ADMIN_PASSWORD=secure-admin-password
```

### Deployment Platforms
- ✅ Replit (Recommended)
- ✅ Heroku
- ✅ AWS EC2
- ✅ Google Cloud Platform
- ✅ DigitalOcean
- ✅ Any platform supporting Python/Flask

## 📝 Usage Examples

### Creating an Admin Account
```bash
# Set environment variables
export ADMIN_EMAIL="admin@example.com"
export ADMIN_PASSWORD="SecurePassword123!"

# Run the application
python app.py
```

### Submitting Feedback (Guest)
1. Navigate to `/guest-feedback`
2. Fill in name, email, category, message
3. Optionally add star rating
4. Submit → Automatic sentiment analysis

### Viewing Analytics (Admin)
1. Login with admin credentials
2. Navigate to `/admin-dashboard`
3. View 6 interactive charts
4. Filter by sentiment, type, date
5. Delete inappropriate feedback

## 🔧 Troubleshooting

### Common Issues

**Issue:** Can't access admin dashboard
- **Solution:** Ensure `ADMIN_EMAIL` and `ADMIN_PASSWORD` are set in environment variables

**Issue:** Password reset emails not working
- **Solution:** Verify Gmail app password is correct and 2FA is enabled

**Issue:** Database errors
- **Solution:** Run `db.create_all()` to initialize tables

**Issue:** Charts not displaying
- **Solution:** Check browser console for JavaScript errors, ensure Chart.js CDN is accessible

## 📚 Additional Resources

### External Documentation
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [TextBlob Documentation](https://textblob.readthedocs.io/)
- [Chart.js Documentation](https://www.chartjs.org/docs/)

### Related Files
- `requirements.txt` - Python dependencies
- `LICENSE` - MIT License
- `.gitignore` - Git ignore rules

## 🤝 Contributing

This project is open for contributions! Areas for improvement:
- Additional chart types
- Export functionality (CSV/Excel)
- Email notifications
- Advanced filtering
- Multi-language support
- Dark mode theme

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**Sandeep Kumar Akula**
- GitHub: [@SandeepKumarAkula](https://github.com/SandeepKumarAkula)
- Email: kumarakula44@gmail.com

## 🎉 Acknowledgments

- Flask community for excellent documentation
- TextBlob for NLP capabilities
- Chart.js for beautiful visualizations
- Replit for hosting platform

---

**Last Updated:** October 29, 2025  
**Version:** 1.0  
**Status:** Production Ready ✅

For detailed technical information, please refer to `ARCHITECTURE.md`.
