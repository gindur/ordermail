DROP TABLE IF EXISTS companies;
DROP TABLE IF EXISTS contacts;
DROP TABLE IF EXISTS sources;
DROP TABLE IF EXISTS locations;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS orderlines;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS contact_sources;
DROP TABLE IF EXISTS phonenumbers;
DROP TABLE IF EXISTS contact_phonenumbers;
DROP TABLE IF EXISTS orderline;

CREATE TABLE IF NOT EXISTS companies(
    company_id TEXT DEFAULT (lower(hex(randomblob(16)))),
    company_name TEXT,
    nbr_of_orders INT,
    order_total REAL,
    email_marketing BIT,
    PRIMARY KEY(company_id),
    UNIQUE(company_name)
);

CREATE TABLE IF NOT EXISTS contacts(
    email_address TEXT,
    first_name TEXT,
    last_name TEXT,
    phonenumber TEXT,
    email_marketing BIT,
    company_id TEXT,
    PRIMARY KEY(email_address),
    FOREIGN KEY(company_id) REFERENCES companies(company_id)
);

CREATE TABLE IF NOT EXISTS phonenumbers (
    phonenumber TEXT,
    PRIMARY KEY (phonenumber)
);

CREATE TABLE IF NOT EXISTS contact_phonenumbers (
    email_address TEXT,
    phonenumber TEXT,
    FOREIGN KEY (email_address) REFERENCES contacts(email_address),
    FOREIGN KEY (phonenumber) REFERENCES phonenumbers(phonenumber),
    UNIQUE (email_address, phonenumber)
);

CREATE TABLE IF NOT EXISTS sources (
    source_id INT,
    source_name TEXT,
    PRIMARY KEY (source_id)
);

CREATE TABLE IF NOT EXISTS contact_sources (
    source_id INT,
    email_address TEXT,
    FOREIGN KEY (source_id) REFERENCES sources(source_id),
    FOREIGN KEY (email_address) REFERENCES contacts(email_address)
    UNIQUE (source_id, email_address)
);

CREATE TABLE IF NOT EXISTS locations (
    company_id TEXT,
    location_id TEXT DEFAULT (lower(hex(randomblob(16)))),
    address TEXT,
    address2 TEXT,
    zipcode INT,
    city TEXT,
    country TEXT,
    UNIQUE (address, address2, zipcode, city, country),
    PRIMARY KEY (location_id),
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT,
    location_id TEXT,
    email_address TEXT,
    date_created DATETIME,
    date_paid DATETIME,
    date_shipped DATETIME,
    currency TEXT,
    total_qty INT,
    total_amount REAL,
    discount_amount REAL,
    tax_amount REAL,
    payment_method TEXT,
    shipping_amount REAL,
    status TEXT,
    PRIMARY KEY (order_id),
    FOREIGN KEY (location_id) REFERENCES locations(location_id),
    FOREIGN KEY (email_address) REFERENCES contacts(email_address)
);

CREATE TABLE IF NOT EXISTS products (
    sku TEXT,
    title TEXT,
    price REAL,
    original_price REAL,
    vid TEXT,
    description TEXT,
    sold INT,
    purchase_price REAL,
    images TEXT,
    product_sku TEXT,
    PRIMARY KEY (sku)
);

CREATE TABLE IF NOT EXISTS orderlines (
    sku TEXT,
    order_id TEXT,
    item_price REAL,
    total_price REAL,
    qty INT,
    desc TEXT,
    orderline_status TEXT,
    FOREIGN KEY (sku) REFERENCES products(sku),
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

INSERT
INTO sources (source_id, source_name)
VALUES (1, 'COLD'),
       (2, 'RETURNING'),
       (3, 'STANDARD');