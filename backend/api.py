import sqlite3
from flask import Flask, g, jsonify, request
from flask_cors import CORS
import logging
from urllib.parse import unquote
from app.app_utils import response
from app.decorators import catch
from app.database import cursor

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)

# Flask setup
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})

@app.teardown_appcontext
def close_db(error):
    """Closes the database connection at the end of the request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

# API endpoints
@catch()
@app.route('/api/orders', methods=['GET'])
def get_orders():    
    params = []
    query = """
        SELECT *
        FROM orders
        WHERE TRUE 
        """

    if request.args:
        if order_id := request.args.get('order_id'):
            query += "AND order_id = ? "
            params.append(order_id)
        if email_address := request.args.get('email_address'):
            query += "AND email_address = ? "
            params.append(unquote(email_address))
        if from_date_paid := request.args.get('from_date_paid'):
            query += "AND date_paid >= ? "
            params.append(from_date_paid)
        if to_date_paid := request.args.get('to_date_paid'):
            query += "AND date_paid <= ? "
            params.append(to_date_paid)

    orders = cursor().execute(query, params).fetchall()
    return response(orders)

@app.route('/api/orders/<order_id>', methods=['GET'])
@catch()
def get_order(order_id):
    logger.info(f"Fetching order {order_id}")
    order = cursor().execute(
        """
        SELECT sku
        FROM orders
        JOIN orderlines USING (order_id)
        WHERE order_id = ?
        """,
        (order_id,)
    ).fetchall()
    logger.info(order)
    return response(order)

@catch()
@app.route('/api/contacts', methods=['GET'])
def get_customers():
    contacts = cursor().execute("SELECT * FROM contacts").fetchall()
    return response(contacts)

@app.route('/api/companies', methods=['GET'])
def get_companies():
    companies = cursor().execute("SELECT * FROM companies").fetchall()
    return response(companies)

@app.route('/api/products', methods=['GET'])
def get_products():
    products = cursor().execute("SELECT * FROM products").fetchall()
    return response(products)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
