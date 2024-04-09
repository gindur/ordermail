from flask import Flask, g
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
         LEFT JOIN contacts USING (email_address)
         LEFT JOIN companies USING (company_id)
         LEFT JOIN contact_phonenumbers USING (email_address)
        GROUP BY order_id
        """

    orders = cursor().execute(query, params).fetchall()
    return response(orders)

@app.route('/api/orders/<order_id>', methods=['GET'])
@catch()
def get_order(order_id):
    logger.info(f"Fetching order {order_id}")
    order = cursor().execute(
        """
        SELECT desc, sku, item_price, qty, total_price, orderline_status, images
        FROM orders
         JOIN orderlines USING (order_id)
         JOIN products USING (sku)
        WHERE order_id = ?  
        """,
        (order_id,)
    ).fetchall()
    return response(order)

@catch()
@app.route('/api/orders/<from_date>/<to_date>/<divOption>', methods=['GET'])
def get_orders_between_dates(from_date, to_date, divOption):
    """Gets orders between two dates, grouped by week, month or year"""
    divisions = {
        'week': '%Y-%W',
        'month': '%Y-%m',
        'year': '%Y'
    }
    division = divisions.get(divOption)
    if not division:
        return response('Invalid division option', 400)
    
    # Construct the query with parameter placeholders
    query = """
        SELECT strftime(:division, date_paid) as date, SUM(total_amount) as revenue
        FROM orders
        WHERE date_paid BETWEEN strftime('%Y-%m-%d',:from_date) AND strftime('%Y-%m-%d',:to_date)
        GROUP BY strftime(:division, date_paid)
        ORDER BY date
    """
    orders = cursor().execute(query, {'division': division, 'from_date': from_date, 'to_date': to_date}).fetchall()
    return response(orders)
    
    
            
    

@catch()
@app.route('/api/contacts', methods=['GET'])
def get_customers():
    contacts = cursor().execute("SELECT * FROM contacts JOIN companies USING (company_id) LEFT JOIN contact_phonenumbers USING(email_address)").fetchall()
    return response(contacts)

@catch()
@app.route('/api/companies', methods=['GET'])
def get_companies():
    companies = cursor().execute("SELECT * FROM companies").fetchall()
    return response(companies)

@catch()
@app.route('/api/products', methods=['GET'])
def get_products():
    products = cursor().execute("SELECT * FROM products").fetchall()
    return response(products)

@catch()
@app.route('/api/locations', methods=['GET'])
def get_locations():
    locations = cursor().execute("SELECT * FROM locations JOIN companies USING (company_id)").fetchall()
    return response(locations)




if __name__ == '__main__':
    app.run(debug=True, port=5000)
