import sqlite3
from csv_handler import get_products, process_orders

db = sqlite3.connect("../db.sqlite")
orders = []
customers = {}
company_name_to_id = {}

def populate_companies():
    c = db.cursor()
    company_ids = {}
    for company in transform_customers():
        company_name, nbr_of_orders, order_total, email_marketing = company[:4]
        c.execute(
            """
            INSERT OR IGNORE INTO companies(company_name, nbr_of_orders, order_total, email_marketing)
            VALUES (?, ?, ?, ?)
            RETURNING company_id
            """,
            (company_name, nbr_of_orders, order_total, email_marketing)
        )
        company_id = c.fetchone()[0]
        company_ids[company_name] = company_id
        populate_contacts(company_id, company[5])
        populate_locations(company_id, company[4])
    
    db.commit()

def populate_locations(company_id, locations):
    locations_data = [
        (
            company_id,
            location['address'],
            location['address2'],
            location['zipcode'],
            location['city'],
            location['country']
        )
        for location in locations
    ] 
    c = db.cursor()
    c.executemany(
        """
        INSERT OR IGNORE
        INTO locations(company_id, address, address2, zipcode, city, country)
        VALUES (?, ?, ?, ?, ?, ?)   
        """,
        locations_data
    )
    
def populate_contacts(company_id, contacts):
    c = db.cursor()
    for contact in contacts:
        email_address = contact['email_address'].strip().lower()
        first_name = contact['firstname']
        last_name = contact['lastname']
        email_marketing = contact['email_marketing']
        phone_number = contact['phonenumber']
        sources = contact['source']
        
        for source in sources:
                c.execute(
                    """
                    INSERT OR IGNORE INTO contact_sources(email_address, source_id)
                    VALUES (?,?)
                    """,
                    (email_address, source)
                )
     
        c.execute(
            """
            INSERT OR IGNORE INTO contacts(company_id, email_address, first_name, last_name, email_marketing)
            VALUES (?, ?, ?, ?, ?)

            """,
            (company_id, email_address, first_name, last_name, email_marketing)
        )
        
        if phone_number:
            c.execute(
                """
                INSERT OR IGNORE INTO phonenumbers(phonenumber)
                VALUES (?)
                """,
                (phone_number,)
            )
            c.execute(
                    """
                    INSERT OR IGNORE INTO contact_phonenumbers(email_address, phonenumber)
                    VALUES (?, ?)
                    """,
                    (email_address, phone_number)
                )
    db.commit()


def populate_products():
    c = db.cursor()
    for product in get_products('../data/products.csv'):
        c.execute(
            """
            INSERT OR IGNORE INTO products(sku, price, vid, title, description, purchase_price, images, sold, product_sku, original_price)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (product['sku'], product['price'], product['variant_id'], product['title'], product['description'], product['purchase_price'], product['images'], 0, product['product_sku'], product['before_price'])
        )
    db.commit()
    
def populate_orders():
    c = db.cursor()
    for order in orders:
        company_id = c.execute(
            """
            SELECT company_id
            FROM companies
            WHERE company_name = ?
            """,
            (order['company_name'],)

        ).fetchone()
        if company_id:
            company_id = company_id[0]
        
        location_id = c.execute(
            """
            SELECT DISTINCT location_id
            FROM locations
            WHERE company_id = ? AND city = ? AND address = ?
            """,
            (
                company_id,
                order['city'],
                order['address']
            )
        ).fetchone()
        if location_id:
            location_id = location_id[0]
        print(order['city'])
        print(order['address'])
        print("location id from db:",location_id)
        print("company id", company_id)
        for product in order['products']:
            c.execute(
                """
                INSERT INTO orderlines(order_id, sku, qty, item_price, total_price, desc, orderline_status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    order['order_id'],
                    product['sku'],
                    product['qty'],
                    product['price'],
                    product['total_price'],
                    product['desc'],
                    'done'
                )
            )
        (total_amount,) = c.execute(
            """
            SELECT sum(total_price) FROM orderlines WHERE order_id = ?      
            """,
            (order['order_id'],)
        ).fetchone()
        c.execute(
            """
            INSERT OR IGNORE INTO orders(
                order_id,
                date_created,
                date_paid,
                date_shipped, 
                currency, 
                total_qty, 
                total_amount, 
                discount_amount, 
                tax_amount, 
                payment_method, 
                shipping_amount, 
                email_address, 
                location_id,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                order['order_id'],
                order['date_created'],
                order['date_paid'],
                order['date_shipped'],
                order['currency'],
                order['total_qty'],
                total_amount,
                order['discount_amount'],
                order['tax_amount'],
                order['payment_method'],
                order['shipping_amount'],
                order['email_address'] if order['email_address'] else 'no email',
                location_id,
                'done'
            )
        )
    db.commit()
    

def transform_customers():
    transformed_customers = [
        (
            customer_dict['company_name'],
            customer_dict['nbr_of_orders'],
            customer_dict['order_total'],
            customer_dict['email_marketing'],
            customer_dict['locations'],
            customer_dict['contact_persons']
        )
        for (_, customer_dict) in customers.items()
    ]
    print(transformed_customers[0])
    return transformed_customers


if __name__ == "__main__":
    orders, customers, company_name_to_id = process_orders('../data/orders.csv')
    populate_companies()
    populate_products()
    populate_orders()

