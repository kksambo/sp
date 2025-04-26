# Service Provider Portal

This project is a Flask application that serves as a backend for a service provider portal. It includes functionalities for user management, service handling, and booking management.

## Project Structure

```
shpy
├── app.py                # Main application file containing Flask routes and logic
├── Dockerfile            # Dockerfile to build the application image
├── requirements.txt      # Python dependencies required for the application
└── README.md             # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd shpy
   ```

2. **Create a virtual environment (optional but recommended):**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Initialize the database:**
   The database will be initialized automatically when you run the application for the first time.

5. **Run the application:**
   ```
   python app.py
   ```

   The application will be accessible at `http://127.0.0.1:5000`.

## Docker Instructions

To build and run the application using Docker, follow these steps:

1. **Build the Docker image:**
   ```
   docker build -t service-provider-portal .
   ```

2. **Run the Docker container:**
   ```
   docker run -p 5000:5000 service-provider-portal
   ```

   The application will be accessible at `http://127.0.0.1:5000`.

## Usage

- **Create User:** POST `/api/create-user`
- **Login User:** POST `/api/login`
- **Get Users:** GET `/api/get-users`
- **Reset Password:** POST `/api/reset-password`
- **Update Profile:** POST `/api/update_profile`
- **Get Profile:** GET `/api/get_profile?id=<user_id>`
- **Get Services:** GET `/api/get-services`
- **Create Booking:** POST `/api/create-booking`
- **Get Bookings:** GET `/api/get-bookings`

## License

This project is licensed under the MIT License.