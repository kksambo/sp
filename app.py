from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DATABASE = 'users.db'

# Initialize database with full profile fields
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                securityPhrase TEXT NOT NULL,
                password TEXT NOT NULL,
                homeAddress TEXT,
                contactNumber TEXT,
                serviceName TEXT,
                serviceDescription TEXT,
                servicePrice REAL,
                availableTimes TEXT,
                promotionalDeal TEXT,
                serviceImage TEXT
            )
            
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                time TEXT,
                serviceProvider INTEGER,
                client INTEGER
            )
            
        ''')
        conn.commit()

# Create User (basic info + empty profile fields)
@app.route('/api/create-user', methods=['POST'])
def create_user():
    print("create user")
    data = request.get_json()
    role = data.get('createRole')
    name = data.get('name')
    email = data.get('email')
    securityPhrase = data.get('securityPhrase')
    password = data.get('password')

    # Optional extra fields (null initially)
    homeAddress = data.get('homeAddress', None)
    contactNumber = data.get('contactNumber', None)
    serviceName = data.get('serviceName', None)
    serviceDescription = data.get('serviceDescription', None)
    servicePrice = data.get('servicePrice', None)
    availableTimes = data.get('availableTimes', None)
    promotionalDeal = data.get('promotionalDeal', None)
    serviceImage = data.get('serviceImage', None)

    if not all([role, name, email, password, securityPhrase]):
        return jsonify({'message': 'Missing required fields'}), 400

    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (
                    role, name, email, securityPhrase, password,
                    homeAddress, contactNumber, serviceName, serviceDescription,
                    servicePrice, availableTimes, promotionalDeal, serviceImage
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (role, name, email, securityPhrase, password,
                  homeAddress, contactNumber, serviceName, serviceDescription,
                  servicePrice, availableTimes, promotionalDeal, serviceImage))
            conn.commit()
        return jsonify({'message': 'User created successfully'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'message': 'Email already exists'}), 409
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# Login user
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return jsonify({'message': 'Missing required fields'}), 400

    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
            user = cursor.fetchone()
            if user:
                user_data = {
                    'id': user[0],
                    'role': user[1],
                    'name': user[2],
                    'email': user[3],
                    'homeAddress': user[6],
                    'contactNumber': user[7],
                    'serviceName': user[8],
                    'serviceDescription': user[9],
                    'servicePrice': user[10],
                    'availableTimes': user[11],
                    'promotionalDeal': user[12],
                    'serviceImage': user[13]
                }
                return jsonify({'message': 'Login successful', 'user': user_data}), 200
            else:
                return jsonify({'message': 'Invalid email or password'}), 401
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# Get all users (for admin maybe)
@app.route('/api/get-users', methods=['GET'])
def get_users():
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users')
            users = cursor.fetchall()
            users_list = [
                {
                    'id': user[0],
                    'role': user[1],
                    'name': user[2],
                    'email': user[3],
                    'homeAddress': user[6],
                    'contactNumber': user[7],
                    'serviceName': user[8],
                    'serviceDescription': user[9],
                    'servicePrice': user[10],
                    'availableTimes': user[11],
                    'promotionalDeal': user[12],
                    'serviceImage': user[13]
                }
                for user in users
            ]
        return jsonify(users_list), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# Reset password
@app.route('/api/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    email = data.get('email')
    new_password = data.get('newPassword')
    security_phrase = data.get('securityPhrase')

    if not all([email, new_password, security_phrase]):
        return jsonify({'message': 'Missing required fields'}), 400

    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE email = ? AND securityPhrase = ?', (email, security_phrase))
            user = cursor.fetchone()
            if user:
                cursor.execute('UPDATE users SET password = ? WHERE email = ?', (new_password, email))
                conn.commit()
                return jsonify({'message': 'Password reset successfully'}), 200
            else:
                return jsonify({'message': 'Invalid email or security phrase'}), 401
    except Exception as e:
        return jsonify({'message': str(e)}), 500
@app.route('/api/update_profile', methods=['POST'])
def update_profile():
    data = request.get_json()
    user_id = data.get('serviceProviderID')  # ID of the user to update
    print(user_id)
    print("sambo")

    if not user_id:
        return jsonify({'message': 'Missing user ID'}), 400

    # Only fields allowed to be updated
    allowed_fields = [
        'homeAddress', 'contactNumber', 'serviceName', 'serviceDescription',
        'servicePrice', 'availableTimes', 'promotionalDeal', 'serviceImage'
    ]

    # Prepare the fields to update
    fields_to_update = {field: data.get(field) for field in allowed_fields if data.get(field) is not None}

    if not fields_to_update:
        return jsonify({'message': 'No fields to update'}), 400

    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            for field, value in fields_to_update.items():
                cursor.execute(f'UPDATE users SET {field} = ? WHERE id = ?', (value, user_id))
            conn.commit()

        return jsonify({'message': 'Profile updated successfully'}), 200
    except sqlite3.Error as e:
        return jsonify({'message': f'Database error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'message': f'Unexpected error: {str(e)}'}), 500

@app.route('/api/get_profile', methods=['GET'])
def get_profile():
    try:
        # Assuming the service provider's ID is passed as a query parameter
        service_provider_id = request.args.get('id')
        if not service_provider_id:
            return jsonify({'error': 'Service provider ID is required'}), 400

        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE id = ?', (service_provider_id,))
            row = cursor.fetchone()

            if not row:
                return jsonify({'error': 'Profile not found'}), 404

            profile = {
                'serviceProviderID': row[0],
                'fullName': row[2],
                'homeAddress': row[6],
                'contactNumber': row[7],
                'serviceName': row[8],
                'serviceDescription': row[9],
                'servicePrice': row[10],
                'availableTimes': row[11],
                'promotionalDeal': row[12]

                
            }

        return jsonify(profile), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/get-services', methods=['GET'])
def get_services():
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            # Fetch users who provide services (serviceName is not null)
            cursor.execute('''
                SELECT name, serviceName, serviceDescription, servicePrice, serviceImage, id
                FROM users
                WHERE serviceName IS NOT NULL
            ''')
            services = cursor.fetchall()

            # Format the data into a list of dictionaries
            services_list = [
                {
                    'serviceProviderName': service[0],
                    'serviceName': service[1],
                    'serviceDescription': service[2],
                    'servicePrice': service[3],
                    'serviceImage': service[4] if service[4] else 'images/one.png' , # Default image if none provided
                    'id':service[5]
                }
                for service in services
            ]

        return jsonify(services_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Create User (basic info + empty profile fields)
@app.route('/api/create-booking', methods=['POST'])
def create_booking():
    print("create booking")
    data = request.get_json()
    serviceProvider = data.get('serviceProvider')
    client = data.get('client')


    # Optional extra fields (null initially)
    time = ""


    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO bookings(time, serviceProvider, client) VALUES (?, ?,?)
            ''', (time, serviceProvider, client))
            conn.commit()
        return jsonify({'message': 'booking created successfully'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'message': 'Email already exists'}), 409
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/api/get-bookings', methods=['GET'])
def get_bookings():
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM bookings')
            users = cursor.fetchall()
            users_list = [
                {
                    'id': user[0],
                    'time': user[1],
                    'serviceProvider': user[2],
                    'client': user[3]

                }
                for user in users
            ]
        return jsonify(users_list), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# Test route
@app.route('/', methods=['GET'])
def get_user():
    return '<h1>Service Provider Portal Backend Running</h1>'

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
