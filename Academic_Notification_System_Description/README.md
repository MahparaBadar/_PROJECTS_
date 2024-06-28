# Academic Notification System

This Academic Notification System is designed to provide timely notifications to students, teachers, and parents within educational institutions. The primary goal is to ensure that important academic events and updates are communicated efficiently and effectively.

## Technologies Used

The system utilizes a combination of advanced technologies:
- **Backend**: FastAPI for building APIs, SQLite for database management, SQLAlchemy for ORM, Kafka for message brokering, and Kong for API management.
- **Frontend**: Streamlit for creating interactive web applications.
- **Deployment**: Docker for containerization and Poetry for dependency management.

## System Overview

The project consists of two main parts:
1. **Backend**: Responsible for user management (signing up and logging in users) and handling notifications.
2. **Frontend**: Includes producer and consumer interfaces for creating and viewing notifications.

## Workflow

Users sign up and securely log in. Admins or teachers can then create notifications using the producer interface. These notifications are stored and distributed via Kafka. On the consumer side, notifications are retrieved from the database and displayed in a user-friendly format on the frontend.

## Usage Example

- **Notifications**: Students, teachers, or parents receive updates about course changes, assignment deadlines, and school events.
- **Producer Interface**: Admins or teachers create notifications through a simple form.
- **Consumer Interface**: Notifications appear in a clear, readable format for users to view.

## Key Benefits

The system enhances communication within educational institutions by providing timely and personalized notifications, ensuring everyone stays informed and engaged. Strong security measures, such as JWT for authentication, protect user data.

## Challenges and Solutions

Challenges addressed during development included secure authentication with JWT, designing a flexible notification system, and managing high traffic. These were mitigated by implementing robust security measures, designing intuitive user interfaces with Streamlit, and leveraging Kafka and Kong for reliable message handling.
