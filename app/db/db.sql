create database uploadproject;
use uploadproject

CREATE TABLE business (
    business_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    billing_account VARCHAR(200));

CREATE TABLE vendor (
    vendor_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    vendor_name VARCHAR(100),
    business_id INT
);

CREATE TABLE uom (
    uom_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    uom_name VARCHAR(100),
    business_id INT
);

CREATE TABLE expense_group (
    expense_group_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    group_name VARCHAR(25),
    business_id INT
);

CREATE TABLE tax_class (
    tax_class_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    class_name VARCHAR(25),
    business_id INT
);
CREATE TABLE product_group (
    product_group_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    group_name VARCHAR(25),
    business_id INT
);

// all tables created except product TABLE

CREATE TABLE product (
    product_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    reference_number INT NOT NULL,
    business_id INT NOT NULL,
    product_name VARCHAR (100) NOT NULL,
    product_code VARCHAR(100) NOT NULL,
    cost INT NOT NULL,
    price FLOAT NOT NULL, 
    alert_quantity INT NOT NULL,
    product_type ENUM('simple','composite'),
    product_nature ENUM('good','service'),
    allow_purchase TINYINT DEFAULT 1,
    allow_sale TINYINT DEFAULT 1, 
    notes VARCHAR(200),
    track_inventory TINYINT DEFAULT 1 NOT NULL,
    earn_commission TINYINT DEFAULT 0 NOT NULL, 
    media_id INT NOT NULL,
    commission_type_id INT NOT NULL,
    vendor_id INT NOT NULL,
    uom_id INT NOT NULL,
    expense_group_id INT NOT NULL, 
    tax_class_id INT NOT NULL,
    product_group_id INT NOT NULL,
    item_status_id INT DEFAULT 1

);

-- clean table structure
CREATE TABLE product (
    product_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    reference_number INT NOT NULL,
    business_id INT NOT NULL,
    product_name VARCHAR (100) NOT NULL,
    product_code VARCHAR(100) NOT NULL,
    cost INT NOT NULL,
    price FLOAT NOT NULL, 
    allow_purchase TINYINT DEFAULT 1,
    allow_sale TINYINT DEFAULT 1, 
    track_inventory TINYINT DEFAULT 1 NOT NULL,
    vendor_id INT NOT NULL,
    uom_id INT NOT NULL,
    expense_group_id INT NOT NULL, 
    product_group_id INT NOT NULL

);





