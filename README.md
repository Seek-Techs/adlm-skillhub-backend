# ADLM SkillHub Backend

## Overview
The ADLM SkillHub Backend is a Django-based REST API platform designed to support lifelong learning and career development. It offers user management, learning resources, community forums, job listings, analytics, and AI/ML-powered features such as career coaching, personalized recommendations, natural language search, and predictive analytics. This project is currently in Phase 3, with plans for deployment and frontend integration in Phase 4.

## Project Aim
To develop a scalable, intelligent backend platform that empowers users with personalized learning resources, community engagement, job opportunities, and actionable insights, preparing for production deployment and user-facing integration.

## Features
- **User Management**: Secure registration, login, and profile management with role-based access.
- **Learning Resources**: Repository with engagement tracking.
- **Community Interaction**: Forum for discussions and knowledge sharing.
- **Job Opportunities**: Platform for job listings and applications.
- **Analytics**: Insights into user activity and predictive engagement forecasting.
- **AI/ML Integration**:
  - AI Career Coach for personalized advice.
  - Recommendation Engine for learning resources.
  - Natural Language Search for forum content.
  - Predictive Analytics for user engagement trends.

## Requirements
- Python 3.13
- Django 4.x
- Django REST Framework
- PostgreSQL 15 (default) or MongoDB (optional local setup)
- Additional libraries: `transformers`, `sentence-transformers`, `faiss-cpu`, `scikit-learn`, `drf-yasg`, `gunicorn`

## Installation

### Prerequisites
- Install Python 3.13 and pip.
- Install PostgreSQL 15 and create a database named `adlm_skillhub`, or install MongoDB for a local alternative (see below).
- Ensure `git` is installed for cloning the repository.

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/adlm-skillhub-backend.git
   cd adlm-skillhub-backend
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   (Generate `requirements.txt` with `pip freeze > requirements.txt` after installing dependencies.)
4. Configure the database:
   - For PostgreSQL (default):
     - Update `core/settings.py` with your credentials:
       ```python
       DATABASES = {
           'default': {
               'ENGINE': 'django.db.backends.postgresql',
               'NAME': 'adlm_skillhub',
               'USER': 'your_username',
               'PASSWORD': 'your_password',
               'HOST': 'localhost',
               'PORT': '5432',
           }
       }
       ```
     - Apply migrations:
       ```bash
       python manage.py migrate
       ```
   - For MongoDB (optional local setup):
     - Install MongoDB and start it with `mongod`.
     - Install `djongo`: `pip install djongo`.
     - Update `core/settings.py`:
       ```python
       DATABASES = {
           'default': {
               'ENGINE': 'djongo',
               'NAME': 'adlm_skillhub',
               'HOST': 'localhost',
               'PORT': 27017,
               'USER': '',  # Optional
               'PASSWORD': '',  # Optional
           }
       }
       ```
     - Create the database: `use adlm_skillhub` in the MongoDB shell.
5. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Usage

### Accessing the API
- Open `http://127.0.0.1:8000/` in a browser.
- Explore endpoints via Swagger UI at `http://127.0.0.1:8000/swagger/`.

### Key Endpoints
- `/auth/api/register/`: Register a new user.
- `/auth/api/login/`: Obtain JWT token.
- `/auth/api/forum-posts/`: Manage forum posts (CRUD).
- `/auth/api/job-listings/`: Manage job listings (CRUD).
- `/auth/api/analytics/summary/`: Get usage analytics.
- `/ai/career-coach/`: Get personalized career advice.
- `/ai/recommendations/`: Get resource recommendations.
- `/ai/search/`: Perform natural language search.
- `/ai/predictive/`: Get engagement forecasts.

### Running Tests
- Individual app tests (working):
  ```bash
  python manage.py test accounts.tests
  python manage.py test ai.tests
  ```
- Note: Global `python manage.py test` is currently broken due to a test discovery issue (to be fixed in Phase 4).

## Documentation
- **API Specification**: Available at `http://127.0.0.1:8000/openapi.json` (to be saved as `docs/api/openapi.json` in Phase 4).
- **Data Models**: To be documented in `docs/models.md`.
- **Design Decisions**: To be documented in `docs/decisions.md`.
- **AEC Integration**: Potential use cases in `docs/aec_integration.md` (e.g., BIM job linking).

## Contributing
1. Fork the repository.
2. Create a branch: `git checkout -b feature-branch`.
3. Commit changes: `git commit -m "Add new feature"`.
4. Push to the branch: `git push origin feature-branch`.
5. Submit a pull request.

## Known Issues
- Global test command (`python manage.py test`) fails due to `accounts/tests` discovery. Use individual app tests for now.
- MongoDB setup is optional and local; main branch uses PostgreSQL.

## Future Plans (Phase 4)
- Deploy to a production environment (e.g., Heroku).
- Integrate a frontend (e.g., React).
- Optimize tests and add scalability features (e.g., indexing, async tasks).
- Enhance documentation with static API specs and model details.

## License


## Contact
For questions or support, contact [sikiru.yusuff@yahoo.com].