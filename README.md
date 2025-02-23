# Simple Booking System

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```

2. Build and start the containers:
   ```bash
   docker-compose up --build
   ```

## Accessing the Application

- The application will be available at `http://localhost:8001`

- The application will be loaded with sample data for testing purposes.
    - username: admin
    - password: admin

## Features

- Authentication with Custom User model using AbstractUser
- Booking system for facilities with date and time slots
- User can book a facility for a specific date and time slot
- Celery tasks for sending confirmation and cancellation emails
- Admin panel for managing facilities and bookings
- Healthcheck endpoint for monitoring the application
- Testing
- Dockerization

## Area of Improvement

- Split views like (booking, facility) into separate files in views folder
- Split facility locations into another model so a facility can have multiple locations
