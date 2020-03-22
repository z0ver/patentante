CREATE TABLE Users (
 user_id SERIAL,
 emailAddress VARCHAR(50) NOT NULL UNIQUE,
 firstname VARCHAR(30) NOT NULL,
 lastname VARCHAR(30) NOT NULL,
 phoneNumber VARCHAR(30),
 passwordHash VARCHAR(64) NOT NULL,
 passwordSalt VARCHAR(64) NOT NULL,
 token VARCHAR(64) NOT NULL,
 isVerified BOOLEAN NOT NULL,
 isOwner BOOLEAN NOT NULL,
 CONSTRAINT pk_Users_user_id PRIMARY KEY ( user_id )
);

CREATE TABLE Shops (
 shop_id SERIAL,
 owner_id INT UNSIGNED NOT NULL,
 name VARCHAR(30) NOT NULL,
 zipCode VARCHAR(10) NOT NULL,
 city VARCHAR(10) NOT NULL,
 street VARCHAR(50) NOT NULL,
 description VARCHAR(3000) NOT NULL,
 Logo_URL VARCHAR(150),
 Link_Website VARCHAR(150),
 phoneNumber VARCHAR(50) NOT NULL,
 CONSTRAINT pk_Shops_shop_id PRIMARY KEY ( shop_id ),
 CONSTRAINT fk_Users FOREIGN KEY (owner_id) REFERENCES Users(user_id) ON DELETE NO ACTION ON UPDATE NO ACTION
);

CREATE TABLE Offers (
 offer_id SERIAL,
 shop_id INT UNSIGNED NOT NULL,
 offerType ENUM('DONATION', 'VALUE', 'PRODUCT') NOT NULL,
 name VARCHAR(50) NOT NULL,
 description VARCHAR(50) NOT NULL,
 value DECIMAL(6,4),
 CONSTRAINT pk_Offers_offer_id PRIMARY KEY ( offer_id ),
 CONSTRAINT fk_Shops FOREIGN KEY ( shop_id ) REFERENCES Shops( shop_id ) ON DELETE NO ACTION ON UPDATE NO ACTION
);

CREATE TABLE Coupons (
 coupons_ID SERIAL PRIMARY KEY,
 offer_ID INT UNSIGNED NOT NULL REFERENCES Offers(offer_ID),
 customer_id INT UNSIGNED NOT NULL REFERENCES Customers(customer_id),
 original_value DECIMAL(6,4) NOT NULL,
 current_value DECIMAL(6,4) NOT NULL,
 status ENUM('PAYMENT_PENDING','ACTIVATE','USED_UP') NOT NULL,
 date_of_purchase TIMESTAMP NOT NULL
 CONSTRAINT pk_Coupons_coupon_id PRIMARY KEY ( coupons_id ),
 CONSTRAINT fk_Offers FOREIGN KEY ( offer_id ) REFERENCES Offers(offer_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
 CONSTRAINT fk_Customers FOREIGN KEY ( customer_id ) REFERENCES Customers(customer_id) ON DELETE NO ACTION ON UPDATE NO ACTION
);

CREATE TABLE Sessions (
user_ID INT REFERENCES Users(user_id),
session_token VARCHAR(64) UNIQUE,
end_date TIMESTAMP NOT NULL
CONSTRAINT fk_Users FOREIGN KEY ( user_id ) REFERENCES Users(user_id) ON DELETE NO ACTION ON UPDATE NO ACTION
);