import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime

# Initialize DB
def create_tables():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Products (
                        product_id INTEGER PRIMARY KEY,
                        name TEXT,
                        category TEXT,
                        price REAL,
                        stock INTEGER)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Sales (
                        sale_id INTEGER PRIMARY KEY,
                        product_id INTEGER,
                        quantity_sold INTEGER,
                        date TEXT,
                        FOREIGN KEY (product_id) REFERENCES Products (product_id))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
                        username TEXT PRIMARY KEY,
                        password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def get_connection():
    return sqlite3.connect('inventory.db')

# Create necessary tables
create_tables()

# Add a sample user (for initial testing)
def create_sample_user():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO Users (username, password) VALUES (?, ?)", ('admin', 'admin123'))
    conn.commit()
    conn.close()

create_sample_user()

# User Authentication
def check_credentials(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE username = ? AND password = ?", (username, password))
    return cursor.fetchone()

# User Registration Page (if needed)
def register_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

# User login
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("Login to Inventory Management System")
    login_mode = st.radio("Select Login or Register", ("Login", "Register"))

    if login_mode == "Register":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")

        if password == confirm_password:
            if st.button("Register"):
                try:
                    register_user(username, password)
                    st.success("User registered successfully! Now you can log in.")
                except Exception as e:
                    st.error(f"Error registering user: {e}")
        else:
            st.error("Passwords do not match.")
    
    elif login_mode == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            if check_credentials(username, password):
                st.session_state.authenticated = True
                st.success("Logged in successfully!")
            else:
                st.error("Invalid credentials. Please try again.")
else:
    # If logged in, display the app UI
    st.title("Welcome to the Inventory Management System")
    st.subheader("📊 Dashboard")

    # Logout Option
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.success("Logged out successfully!")
        st.rerun()  # Rerun the app to reflect the logout

    # Your app functionality continues here...
    conn = get_connection()
    cursor = conn.cursor()

    # Total number of products
    cursor.execute("SELECT COUNT(*) FROM Products")
    total_products = cursor.fetchone()[0]

    # Total sales value
    cursor.execute("""
        SELECT SUM(p.price * s.quantity_sold) 
        FROM Sales s JOIN Products p ON s.product_id = p.product_id
    """)
    total_sales_value = cursor.fetchone()[0] or 0

    # Total stock value
    cursor.execute("SELECT SUM(price * stock) FROM Products")
    total_stock_value = cursor.fetchone()[0] or 0

    # Display Dashboard Stats
    st.metric("Total Products", total_products)
    st.metric("Total Sales Value", f"₹ {total_sales_value:,.2f}")
    st.metric("Total Stock Value", f"₹ {total_stock_value:,.2f}")

    # Sidebar Menu
    menu = ["Add Product", "Update Stock", "Record Sale", "Sales Report", "View Inventory"]
    choice = st.sidebar.selectbox("Menu", menu)

    # Add Product Section
    if choice == "Add Product":
        st.subheader("Add New Product")
        name = st.text_input("Product Name")
        category = st.text_input("Category")
        price = st.number_input("Price", min_value=0.0)
        stock = st.number_input("Initial Stock", min_value=0)

        if st.button("Add Product"):
            cursor.execute("INSERT INTO Products (name, category, price, stock) VALUES (?, ?, ?, ?)",
                           (name, category, price, stock))
            conn.commit()
            st.success("Product added successfully.")

    # Update Stock Section
    elif choice == "Update Stock":
        st.subheader("Update Stock")
        cursor.execute("SELECT product_id, name FROM Products")
        products = cursor.fetchall()
        product_dict = {f"{name} (ID: {pid})": pid for pid, name in products}
        selected = st.selectbox("Select Product", list(product_dict.keys()))

        new_stock = st.number_input("New Stock Quantity", min_value=0)
        if st.button("Update"):
            pid = product_dict[selected]
            cursor.execute("UPDATE Products SET stock = ? WHERE product_id = ?", (new_stock, pid))
            conn.commit()
            st.success("Stock updated.")

    # Record Sale Section
    elif choice == "Record Sale":
        st.subheader("Record Sale")
        cursor.execute("SELECT product_id, name, stock FROM Products")
        products = cursor.fetchall()
        product_dict = {f"{name} (Stock: {stock})": (pid, stock) for pid, name, stock in products}
        selected = st.selectbox("Select Product", list(product_dict.keys()))

        pid, available_stock = product_dict[selected]
        qty = st.number_input("Quantity Sold", min_value=1, max_value=available_stock)
        if st.button("Record Sale"):
            date = datetime.now().strftime("%Y-%m-%d")
            cursor.execute("INSERT INTO Sales (product_id, quantity_sold, date) VALUES (?, ?, ?)",
                           (pid, qty, date))
            cursor.execute("UPDATE Products SET stock = stock - ? WHERE product_id = ?", (qty, pid))
            conn.commit()
            st.success("Sale recorded.")

    # Sales Report Section with Filter
    elif choice == "Sales Report":
        st.subheader("Sales Report")
        start_date = st.date_input("Start Date", datetime(2025, 1, 1))
        end_date = st.date_input("End Date", datetime.now())

        cursor.execute("""
            SELECT p.name, s.quantity_sold, s.date 
            FROM Sales s JOIN Products p ON s.product_id = p.product_id
            WHERE s.date BETWEEN ? AND ?
            ORDER BY s.date DESC
        """, (start_date, end_date))
        rows = cursor.fetchall()

        if rows:
            df = pd.DataFrame(rows, columns=["Product", "Quantity Sold", "Date"])
            st.table(df)

            # Sales Trend Line Chart
            sales_trend = df.groupby("Date")["Quantity Sold"].sum().reset_index()
            sales_trend_fig = px.line(sales_trend, x="Date", y="Quantity Sold", title="Sales Trend Over Time")
            st.plotly_chart(sales_trend_fig)

            # Sales Per Product Bar Chart
            sales_per_product = df.groupby("Product")["Quantity Sold"].sum().reset_index()
            sales_per_product_fig = px.bar(sales_per_product, x="Product", y="Quantity Sold", title="Sales Per Product")
            st.plotly_chart(sales_per_product_fig)

        else:
            st.info("No sales data available.")

    # View Inventory Section
    elif choice == "View Inventory":
        st.subheader("Inventory")
        cursor.execute("SELECT * FROM Products")
        inventory_data = cursor.fetchall()

        # Check the length of each row to debug
        if inventory_data:
            st.write(f"Number of columns in each row: {len(inventory_data[0])}")

            # Adjust the DataFrame columns according to the actual number of columns in the query result
            if len(inventory_data[0]) == 5:  # If missing store_location column
                df = pd.DataFrame(inventory_data, columns=["Product ID", "Name", "Category", "Price", "Stock"])
            elif len(inventory_data[0]) == 6:  # If all columns are present
                df = pd.DataFrame(inventory_data, columns=["Product ID", "Name", "Category", "Price", "Stock", "Store Location"])

            st.table(df)
        else:
            st.warning("No products in inventory.")

    conn.close()