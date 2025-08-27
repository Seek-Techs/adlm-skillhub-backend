# Data Models

## User
- `email`: Unique email address
- `password`: Hashed password
- `role`: 'Learner' or 'Admin'
- `login_count`: Integer tracking logins
- `last_login_time`: Last login timestamp
- `resources_viewed`: Integer tracking views

## AnalyticsEvent
- `user`: Reference to User
- `event_type`: 'login', 'resource_view', 'forum_post'
- `details`: JSON metadata
- `timestamp`: Event time