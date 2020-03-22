CREATE TABLE Users (
 user_id SERIAL PRIMARY KEY,
 email_address VARCHAR(50) NOT NULL UNIQUE,
 firstname VARCHAR(30) NOT NULL,
 lastname VARCHAR(30) NOT NULL,
 phone_number VARCHAR(30),
 password_hash VARCHAR(64) NOT NULL,
 is_verified BOOLEAN NOT NULL,
 is_owner BOOLEAN NOT NULL
);

CREATE TABLE Shops (
 shop_id SERIAL PRIMARY KEY,
 owner_id VARCHAR(30) NOT NULL REFERENCES Users(user_id),
 street VARCHAR(50) NOT NULL,
 zip_code VARCHAR(10) NOT NULL,
 city VARCHAR(10) NOT NULL,
 website_url VARCHAR(150),
 phone_number VARCHAR(50) NOT NULL,
 name VARCHAR(30) NOT NULL,
 logo_url VARCHAR(150),
 description_short VARCHAR(500) NOT NULL,
 description VARCHAR(3000) NOT NULL
);

CREATE TABLE Offers (
 offer_id SERIAL PRIMARY KEY,
 shop_id INT UNSIGNED NOT NULL REFERENCES Shops(shop_ID),
 offer_type ENUM('DONATION', 'VALUE', 'PRODUCT') NOT NULL,
 name VARCHAR(50) NOT NULL,
 description VARCHAR(50) NOT NULL,
 value DECIMAL(6,4)
);

CREATE TABLE Coupons (
 coupons_id SERIAL PRIMARY KEY,
 offer_id INT UNSIGNED NOT NULL REFERENCES Offers(offer_ID),
 customer_id INT UNSIGNED NOT NULL REFERENCES Customers(customer_id),
 original_value DECIMAL(6,4) NOT NULL,
 current_value DECIMAL(6,4) NOT NULL,
 status ENUM('PAYMENT_PENDING','ACTIVATE','USED_UP') NOT NULL,
 date_of_purchase TIMESTAMP NOT NULL
);

CREATE TABLE Sessions (
user_id INT REFERENCES Users(user_id),
session_token VARCHAR(64) UNIQUE,
end_date TIMESTAMP NOT NULL
);