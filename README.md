Inventory Management System
   
A web-based Inventory Management System built using Python, Streamlit, SQLite, and Plotly. This application allows users to manage products, track stock levels, record sales, and generate insightful sales reports with visualizations. It includes user authentication for secure access and a user-friendly interface for efficient inventory management.
Table of Contents

Features
Technologies Used
Installation
Usage
File Structure
Database Schema
Screenshots
Contributing
License
Contact

Features

User Authentication: Secure login and registration system for admin access.
Dashboard: Displays key metrics like total products, sales value, and stock value.
Product Management: Add new products with details like name, category, price, and stock.
Stock Updates: Update stock quantities for existing products.
Sales Recording: Record sales transactions and automatically update stock levels.
Sales Reports: Generate reports with date filters and visualize sales trends and product performance using line and bar charts.
Inventory View: View all products in a tabular format.
Responsive UI: Built with Streamlit for a clean, interactive web interface.

Technologies Used

Python 3.8+: Core programming language.
Streamlit: For building the web-based user interface.
SQLite: Lightweight database for storing products, sales, and user data.
Pandas: For data manipulation and table display.
Plotly: For creating interactive sales visualizations.
SQLite3: Python library for database operations.

Installation
Prerequisites

Python 3.8 or higher
pip (Python package manager)

Steps

Clone the Repository:
git clone https://github.com/nadheemcr7/inventory_management.git
cd inventory_management


Create a Virtual Environment (optional but recommended):
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install Dependencies:Create a requirements.txt file with the following content:
streamlit==1.28.0
pandas==2.0.3
plotly==5.15.0
sqlite3

Then run:
pip install -r requirements.txt


Run the Application:
streamlit run app.py


Access the App:Open your browser and navigate to http://localhost:8501.


Default Credentials
For initial testing, a sample user is created:

Username: admin
Password: admin123

Usage

Login or Register:

Use the default credentials or register a new user.
After login, you'll be redirected to the dashboard.


Dashboard:

View key metrics like total products, sales value, and stock value.


Sidebar Menu:

Add Product: Enter product details to add to the inventory.
Update Stock: Select a product and update its stock quantity.
Record Sale: Select a product, specify quantity sold, and record the transaction.
Sales Report: Filter sales by date range and view tables and charts.
View Inventory: See all products in a table.


Logout:

Click the "Logout" button to end the session.



File Structure
inventory_management/
│
├── app.py              # Main application file with Streamlit UI and logic
├── db.py               # Database connection and table creation
├── utils.py            # Placeholder for utility functions (currently empty)
├── inventory.db        # SQLite database file (created on first run)
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation



Note: For production use, consider hashing passwords for security.
Screenshots
To be added: Screenshots of the login page, dashboard, and sales report.
Contributing
Contributions are welcome! Please follow these steps:

Fork the repository.
Create a new branch (git checkout -b feature-name).
Make your changes and commit (git commit -m "Add feature").
Push to the branch (git push origin feature-name).
Open a Pull Request.

Guidelines

Follow PEP 8 for Python code style.
Test changes locally before submitting.
Update the README if new features are added.

License
This project is licensed under the MIT License. See the LICENSE file for details.
Contact
For questions or feedback, reach out to:

GitHub: nadheemcr7
Email: mdnadheem7@gmail.com


Built with ❤️ by nadheemcr7
