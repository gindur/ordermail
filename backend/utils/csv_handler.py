import csv
import sys
import uuid
from utils import load_and_dump, normalize_row

no_marketing_file_path = '../data/no_marketing'
cold_file_path = '../data/cold'
standard_file_path = '../data/standard'
returning_file_path = '../data/returning'
sources = [cold_file_path, standard_file_path, returning_file_path]

no_marketing_customers = []
cold_emails = []
standard_emails = []
returning_emails = []

def load_no_marketing():
    load_and_dump(no_marketing_file_path, no_marketing_customers)
    
def load_sources():
    load_and_dump(cold_file_path, cold_emails)
    load_and_dump(returning_file_path, returning_emails)
    load_and_dump(standard_file_path, standard_emails)
            

def load_from_csv(csv_file_path):
    orders = []
    company_name_to_id = {}
    customers = {}
    try:
        with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file,  delimiter=';')
            for row in csv_reader:
                normalize_row(row)
                row['products'] = parse_products(row['products'])
                create_customer(row, company_name_to_id, customers)
                orders.append(row)
    except OSError as e:
        print(f"Unable to open {csv_file_path}: {e}", file=sys.stderr)
        return
    return orders, customers, company_name_to_id

def parse_products(products_str):
    products = []
    for product_str in products_str.split('%NN%'):
        attr = product_str.split('#=#')
        product = {
            'sku': attr[0],
            'price': attr[1],
            'qty': attr[2],
            'total_price': attr[3],
            'desc': attr[4]
        }
        products.append(product)
    return products

def create_customer(order_row, company_name_to_id, customers):
    company_id = None
    company_name: str = order_row['company_name']
    cn = company_name.strip().lower()
    if cn in company_name_to_id:
        company_id = company_name_to_id[cn]
        # increase nbr of orders
        customers[company_id]['nbr_of_orders'] += 1
        customers[company_id]['order_total'] += float(order_row['total_paid'])*0.8
        
    else:
        #Add company_id to index
        company_id = str(uuid.uuid4())
        company_name_to_id[cn] = company_id
        customers[company_id] = {
            'company_id' : company_id,
            'company_name' : company_name,
            'nbr_of_orders' : 1,
            'order_total' : float(order_row['total_paid'])*0.8,
            'locations' : [],
            'contact_persons' : [],
            'email_marketing': True
        }
    customers[company_id]['email_marketing'] = get_company_email_status(cn)
    
    location_header = ['address', 'address2', 'zipcode', 'city', 'country']
    location = {label: order_row[label] for label in location_header}
    
    contact_header = ['email_address', 'firstname', 'lastname', 'phonenumber']
    contact = {label: order_row[label] for label in contact_header}
    contact['email_address'] = contact['email_address'].lower()
    contact['email_marketing'] = get_email_status(customers[company_id])
    contact['source'] = get_customer_source(contact['email_address'])
    
    if location not in customers[company_id]['locations']:
        customers[company_id]['locations'].append(location)
    if contact not in customers[company_id]['contact_persons']:
        customers[company_id]['contact_persons'].append(contact)


def get_email_status(company):
    #check emails instead in future
    load_no_marketing()
    return company['email_marketing'] and company['company_name'] not in no_marketing_customers

def get_company_email_status(company_name):
    return company_name not in no_marketing_customers

def get_customer_source(email):
    sources = []
    if email in cold_emails: sources.append(1)
    if email in returning_emails: sources.append(2)
    if email in standard_emails: sources.append(3)
    return sources

def get_products(file_path: str):
    products = []
    try:
        with open(file_path, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file,  delimiter=';')
            for row in csv_reader:
                products.append(row)
    except OSError as e:
        print(f"Unable to open {file_path}: {e}", file=sys.stderr)
        return
    return products
                  
                  
#creates ordertable and customers
def process_orders(csv_file_path: str):
    load_sources()
    load_no_marketing()
    orders, customers, company_name_to_id = load_from_csv(csv_file_path)
    return orders, customers, company_name_to_id


