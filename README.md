# Daily Expenses Sharing Application

## Overview
The Daily Expenses Sharing Application is a backend service that allows users to add expenses and split them using three different methods: equal amounts, exact amounts, and percentages. It supports user management, expense tracking, and balance sheet generation.

### Key Features:
- **User Management**: Users can register, and their details include email (used as the unique identifier), name, and mobile number.
- **Expense Splitting**: Expenses can be split among participants in three ways:
  1. **Equal Split**: The total is divided equally among participants.
  2. **Exact Split**: Specify the exact amount each participant owes.
  3. **Percentage Split**: Split based on the percentage specified by each participant (ensuring total percentage sums up to 100%).
- **Balance Sheet**: Individual and overall expense tracking with an option to download a balance sheet.

## Installation

### Prerequisites:
- Python 3.8+
- Django 3.x or higher
- Django REST framework
- PostgreSQL (or any other supported database)

### Clone the Repository:
```bash
git clone https://github.com/daily-expenses.git
cd daily-expenses
```

### Setup a Virtual Environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Install Dependencies:
```bash
pip install -r requirements.txt
```

### Database Setup:
1. Set up PostgreSQL or your preferred database, here we are using SQLite.
2. Update the `DATABASES` section in `settings.py` to match your database configuration.
3. Run migrations:
   ```bash
   python manage.py migrate
   ```

### Run the Application:
```bash
python manage.py runserver
```

## API Endpoints

### User Endpoints:
- **Create User**: `POST /api/users/`
- **Get User Details**: `GET /api/users/<int:pk>/`

### Expense Endpoints:
- **Add Expense**: `POST /api/expenses/`
- **Get User Expenses**: `GET /api/expenses/user/`
- **Get All Expenses**: `GET /api/expenses/all/`
- **Download Balance Sheet**: `GET /api/balance-sheet/`

## Testing
To run tests, use the following command:
```bash
python manage.py test
```

## Project Structure:
```
daily_expenses/
 └── expenses/
     ├── migrations/
     ├── __init__.py
     ├── admin.py
     ├── apps.py
     ├── models.py
     ├── serializers.py
     ├── tests.py
     ├── urls.py
     └── views.py
```

## License
This project is licensed under the MIT License.

---

You can adjust the placeholders and include any additional details specific to your project.
