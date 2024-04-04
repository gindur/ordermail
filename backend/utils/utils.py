import sqlite3

def load_and_dump(file_path: str, target: list[str] ):
    with open(file_path, mode='r', encoding='utf-8') as file:
        Lines = file.readlines()
        for line in Lines:
            target.append(line.strip().lower())
            
def normalized_number(number):
    number = ''.join(filter(str.isdigit, number))
    return number

def normalize_string(string):
    #remove duplicate spaces, strip, lowercase
    return ' '.join(string.split()).strip().lower()

def normalize_order_row(row):
    if row['email_address'].startswith('_'):
            row['email_address'] = row['email_address'][1:]
    row['company_name'] = normalize_string(row['company_name'])
    row['email_address'] = normalize_string(row['email_address'])
    row['firstname'] = normalize_string(row['firstname'])
    row['lastname'] = normalize_string(row['lastname'])
    row['phonenumber'] = normalized_number(row['phonenumber'])
    row['zipcode'] = normalized_number(row['zipcode'])
    row['city'] = normalize_string(row['city'])
    row['country'] = normalize_string(row['country'])
    row['address'] = normalize_string(row['address'])
    row['address2'] = normalize_string(row['address2'])
