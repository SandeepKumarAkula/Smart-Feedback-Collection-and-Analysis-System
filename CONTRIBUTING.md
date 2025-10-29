# 🤝 Contributing to Smart Feedback Collection and Analysis System

Thank you for your interest in contributing to the Smart Feedback Collection and Analysis System! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Workflow](#development-workflow)
4. [Coding Standards](#coding-standards)
5. [Testing Guidelines](#testing-guidelines)
6. [Pull Request Process](#pull-request-process)
7. [Feature Requests](#feature-requests)
8. [Bug Reports](#bug-reports)
9. [Documentation](#documentation)

---

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors, regardless of:
- Experience level
- Gender identity and expression
- Sexual orientation
- Disability
- Personal appearance
- Body size
- Race
- Ethnicity
- Age
- Religion
- Nationality

### Expected Behavior

- Use welcoming and inclusive language
- Be respectful of differing viewpoints
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards other community members

### Unacceptable Behavior

- Harassment or discriminatory language
- Trolling or insulting comments
- Public or private harassment
- Publishing others' private information
- Other conduct inappropriate in a professional setting

---

## Getting Started

### Prerequisites

Before contributing, ensure you have:
- Python 3.11 or higher installed
- Git installed and configured
- A GitHub account
- Basic knowledge of Flask and SQLAlchemy
- Familiarity with HTML, CSS, and JavaScript

### Fork and Clone

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/Smart-Feedback-Collection-and-Analysis-System.git
   cd Smart-Feedback-Collection-and-Analysis-System
   ```

3. **Add upstream remote:**
   ```bash
   git remote add upstream https://github.com/SandeepKumarAkula/Smart-Feedback-Collection-and-Analysis-System.git
   ```

### Setup Development Environment

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   python -m textblob.download_corpora
   ```

3. **Create `.env` file:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Initialize database:**
   ```bash
   python
   >>> from app import app, db
   >>> with app.app_context():
   ...     db.create_all()
   >>> exit()
   ```

5. **Run the application:**
   ```bash
   python app.py
   ```

---

## Development Workflow

### Branch Naming Convention

Use descriptive branch names following this pattern:

- **Feature:** `feature/description-of-feature`
- **Bug Fix:** `bugfix/description-of-bug`
- **Enhancement:** `enhancement/description-of-enhancement`
- **Documentation:** `docs/description-of-changes`
- **Refactor:** `refactor/description-of-refactor`

**Examples:**
```bash
git checkout -b feature/export-to-csv
git checkout -b bugfix/fix-rating-validation
git checkout -b enhancement/add-dark-mode
git checkout -b docs/update-api-reference
```

### Commit Message Guidelines

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

**Format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```bash
feat(feedback): add export to CSV functionality

- Added export button to admin dashboard
- Implemented CSV generation logic
- Added download endpoint

Closes #42

---

fix(auth): resolve password reset token expiry issue

The token expiry was not being checked correctly, allowing
expired tokens to be used. This fix adds proper datetime
comparison.

Fixes #38

---

docs(api): update API reference with new endpoints

- Added documentation for /api/export endpoint
- Updated response examples
- Added error handling section
```

### Keep Your Fork Updated

Regularly sync your fork with the upstream repository:

```bash
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

---

## Coding Standards

### Python Style Guide

Follow [PEP 8](https://pep8.org/) style guide:

**Good:**
```python
def analyze_sentiment(text):
    """
    Analyzes sentiment of text using TextBlob.
    
    Args:
        text (str): The text to analyze
        
    Returns:
        str: 'Positive', 'Negative', or 'Neutral'
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

**Bad:**
```python
def analyzeSentiment(t):
    b=TextBlob(t)
    p=b.sentiment.polarity
    if p>0.1:return 'Positive'
    elif p<-0.1:return 'Negative'
    else:return 'Neutral'
```

### Code Formatting

Use consistent formatting:

```bash
# Install black (Python formatter)
pip install black

# Format code
black app.py

# Check formatting
black --check app.py
```

### Import Organization

Organize imports in this order:

1. Standard library imports
2. Third-party imports
3. Local application imports

```python
# Standard library
import os
from datetime import datetime, timedelta

# Third-party
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from textblob import TextBlob

# Local
from config import Config
from models import User, Feedback
```

### Naming Conventions

- **Variables/Functions:** `snake_case`
- **Classes:** `PascalCase`
- **Constants:** `UPPER_SNAKE_CASE`
- **Private methods:** `_leading_underscore`

```python
# Good
MAX_FEEDBACK_LENGTH = 1000
user_email = "user@example.com"

class FeedbackAnalyzer:
    def analyze_sentiment(self, text):
        return self._calculate_polarity(text)
    
    def _calculate_polarity(self, text):
        # Private method
        pass
```

### HTML/CSS Guidelines

**HTML:**
- Use semantic HTML5 elements
- Proper indentation (2 spaces)
- Include alt text for images
- Use ARIA labels for accessibility

```html
<!-- Good -->
<section class="feedback-form">
  <h2>Submit Feedback</h2>
  <form method="POST" action="/user-feedback">
    <label for="message">Your Feedback:</label>
    <textarea id="message" name="message" required></textarea>
    <button type="submit">Submit</button>
  </form>
</section>
```

**CSS:**
- Use meaningful class names
- Follow BEM methodology when appropriate
- Group related properties
- Use CSS variables for colors

```css
/* Good */
:root {
  --primary-color: #007bff;
  --success-color: #28a745;
  --danger-color: #dc3545;
}

.feedback-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.feedback-card__header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
}
```

### JavaScript Guidelines

- Use ES6+ features
- Use `const` and `let` (avoid `var`)
- Use arrow functions when appropriate
- Add comments for complex logic

```javascript
// Good
const updateStars = (rating) => {
  const stars = document.querySelectorAll('.star');
  
  stars.forEach((star, index) => {
    if (index < rating) {
      star.classList.add('active');
    } else {
      star.classList.remove('active');
    }
  });
};

// Event listener with proper error handling
document.addEventListener('DOMContentLoaded', () => {
  try {
    initializeRatingSystem();
    initializeCharts();
  } catch (error) {
    console.error('Initialization error:', error);
  }
});
```

---

## Testing Guidelines

### Writing Tests

Create tests for new features and bug fixes:

```python
# tests/test_sentiment.py
import unittest
from app import analyze_sentiment

class TestSentimentAnalysis(unittest.TestCase):
    
    def test_positive_sentiment(self):
        """Test that positive text returns 'Positive'"""
        text = "This is an amazing product! I love it!"
        result = analyze_sentiment(text)
        self.assertEqual(result, 'Positive')
    
    def test_negative_sentiment(self):
        """Test that negative text returns 'Negative'"""
        text = "Terrible experience. Very disappointed."
        result = analyze_sentiment(text)
        self.assertEqual(result, 'Negative')
    
    def test_neutral_sentiment(self):
        """Test that neutral text returns 'Neutral'"""
        text = "It's okay, nothing special."
        result = analyze_sentiment(text)
        self.assertEqual(result, 'Neutral')

if __name__ == '__main__':
    unittest.main()
```

### Running Tests

```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_sentiment.py

# Run with coverage
python -m pytest --cov=app tests/
```

### Test Coverage

Aim for at least 80% code coverage:

```bash
# Generate coverage report
coverage run -m pytest
coverage report
coverage html  # Generate HTML report
```

---

## Pull Request Process

### Before Submitting

1. **Update your branch:**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run tests:**
   ```bash
   python -m pytest
   ```

3. **Check code style:**
   ```bash
   black --check app.py
   flake8 app.py
   ```

4. **Update documentation** if needed

5. **Test manually** in browser

### Creating Pull Request

1. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create PR on GitHub:**
   - Go to your fork on GitHub
   - Click "New Pull Request"
   - Select your branch
   - Fill in the PR template

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Enhancement
- [ ] Documentation update
- [ ] Refactoring

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
- [ ] All existing tests pass
- [ ] Added new tests for changes
- [ ] Manually tested in browser

## Screenshots (if applicable)
Add screenshots here

## Related Issues
Closes #issue_number

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
```

### Review Process

1. **Automated checks** must pass (if configured)
2. **Code review** by maintainer
3. **Address feedback** if requested
4. **Approval** and merge by maintainer

---

## Feature Requests

### Suggesting Features

1. **Check existing issues** to avoid duplicates
2. **Create new issue** with "Feature Request" label
3. **Use feature request template:**

```markdown
## Feature Description
Clear description of the feature

## Problem It Solves
What problem does this feature address?

## Proposed Solution
How should this feature work?

## Alternatives Considered
What other solutions did you consider?

## Additional Context
Any other relevant information
```

### Priority Features

Current priority areas for contributions:

1. **Export Functionality**
   - CSV export
   - Excel export
   - PDF reports

2. **Advanced Analytics**
   - Keyword extraction
   - Trend analysis
   - Comparative analytics

3. **Email Notifications**
   - Admin notifications for new feedback
   - User notifications for responses
   - Weekly summary emails

4. **User Experience**
   - Dark mode
   - Multi-language support
   - Accessibility improvements

5. **API Enhancements**
   - RESTful API expansion
   - API authentication (JWT)
   - API rate limiting

---

## Bug Reports

### Reporting Bugs

1. **Check existing issues** first
2. **Create new issue** with "Bug" label
3. **Use bug report template:**

```markdown
## Bug Description
Clear description of the bug

## Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. Scroll down to '...'
4. See error

## Expected Behavior
What should happen?

## Actual Behavior
What actually happens?

## Screenshots
Add screenshots if applicable

## Environment
- OS: [e.g., Windows 10, macOS 12, Ubuntu 22.04]
- Browser: [e.g., Chrome 120, Firefox 121]
- Python Version: [e.g., 3.11.5]
- Database: [e.g., PostgreSQL 15, SQLite 3.40]

## Additional Context
Any other relevant information
```

### Bug Fix Process

1. **Reproduce the bug** locally
2. **Create branch:** `bugfix/description`
3. **Fix the bug** with tests
4. **Submit PR** with reference to issue

---

## Documentation

### Documentation Standards

- Use clear, concise language
- Include code examples
- Add diagrams where helpful
- Keep documentation up-to-date

### Documentation Structure

```
docs/
├── README.md              # Overview and quick start
├── ARCHITECTURE.md        # System architecture
├── API_REFERENCE.md       # API documentation
├── SETUP.md              # Setup and configuration
├── DEPLOYMENT_GUIDE.md   # Deployment instructions
└── CONTRIBUTING.md       # This file
```

### Updating Documentation

When making changes that affect documentation:

1. Update relevant `.md` files
2. Update code comments
3. Update docstrings
4. Update README if needed

---

## Recognition

### Contributors

All contributors will be recognized in:
- README.md contributors section
- GitHub contributors page
- Release notes

### Significant Contributions

Major contributions may result in:
- Collaborator status
- Mention in project announcements
- LinkedIn recommendation (if requested)

---

## Questions?

If you have questions about contributing:

1. **Check documentation** first
2. **Search existing issues**
3. **Create discussion** on GitHub
4. **Email maintainer:** kumarakula44@gmail.com

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to the Smart Feedback Collection and Analysis System!** 🎉

Your contributions help make this project better for everyone.

---

**Document Version:** 1.0  
**Last Updated:** October 29, 2025  
**Author:** Sandeep Kumar Akula
