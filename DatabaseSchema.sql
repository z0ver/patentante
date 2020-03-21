CREATE TABLE Customers (
 customer_id SERIAL PRIMARY KEY,
 emailAddress VARCHAR(50) NOT NULL, UNIQUE,
 firstname VARCHAR(30) NOT NULL,
 lastname VARCHAR(30) NOT NULL,
 phoneNumber VARCHAR(30),
 passwordHash VARCHAR(64) NOT NULL,
 passwordSalt VARCHAR(64) NOT NULL,
 token VARCHAR(64) NOT NULL,
 sessionKey VARCHAR(64) NOT NULL,
 isVerified BOOLEAN NOT NULL
);

CREATE TABLE Owners (
 owner_id SERIAL PRIMARY KEY,
 emailAddress VARCHAR(50) NOT NULL, UNIQUE,
 lastname VARCHAR(30) NOT NULL,
 phoneNumber VARCHAR(30) NOT NULL,
 passwordHash VARCHAR(64) NOT NULL,
 passwordSalt VARCHAR(64) NOT NULL,
 token VARCHAR(64) NOT NULL,
 sessionKey VARCHAR(64) NOT NULL,
 isVerified BOOLEAN NOT NULL
);

CREATE TABLE Shops (
 shop_ID SERIAL PRIMARY KEY,
 owner_email VARCHAR(30) NOT NULL REFERENCES Owners(owner_id),
 name VARCHAR(30) NOT NULL,
 zipCode VARCHAR(10) NOT NULL,
 city VARCHAR(10) NOT NULL,
 street VARCHAR(50) NOT NULL,
 description VARCHAR(3000) NOT NULL,
 Logo_URL VARCHAR(150),
 Link_Website VARCHAR(150),
 phoneNumber VARCHAR(50) NOT NULL
);

CREATE TABLE coupons (
 coupon_ID SERIAL PRIMARY KEY REFERENCES Coupons(coupon_ID),
 shop_ID INT UNSIGNED NOT NULL REFERENCES Shops(shop_ID),
 couponType ENUM('DONATION', 'VALUE', 'PRODUCT') NOT NULL,
 name VARCHAR(50) NOT NULL,
 description VARCHAR(50) NOT NULL,
 value DECIMAL(6,4)
);

CREATE TABLE used_coupons (
 used_coupons_ID SERIAL PRIMARY KEY,
 coupon_ID INT UNSIGNED NOT NULL REFERENCES Coupons(coupon_ID),
 customer_id INT UNSIGNED NOT NULL REFERENCES Customers(customer_id),
 original_value DECIMAL(6,4) NOT NULL,
 current_value DECIMAL(6,4) NOT NULL,
 status ENUM('PAYMENT_PENDING','ACTIVATE','USED_UP') NOT NULL,
 date_of_purchase TIMESTAMP NOT NULL
);