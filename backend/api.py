import sqlite3
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from utils import *
import app.qb_fetch as qb

db = sqlite3.connect("db.sqlite")

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})

@app.route('/api/orders', methods=['GET'])
def get_orders():
    c = db.cursor()
    orders = c.execute(
        """
        SELECT order_id, company_name, order_date, order_total
        FROM orders
        """
    ).fetchall()
    return jsonify(orders)

@app.route('/api/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    return qb.fetch_order(order_id)
    

@app.route('/api/customers', methods=['GET'])
def get_customers():
    return jsonify(customers)

if __name__ == '__main__':
    app.run(debug=True, port=5000)