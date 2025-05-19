from flask import Flask 
from flask import jsonify, request
from flask_cors import CORS
from mysql.connector import pooling

app = Flask(__name__)
CORS(app)

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Hsiang9922",
    "database": "product_tracking_db"
}
pool = pooling.MySQLConnectionPool(pool_name="mypool", pool_size=5, **db_config)

def setup_database():
    con = pool.get_connection()
    cursor = con.cursor()
    cursor.execute("DROP TABLE IF EXISTS orders")
    cursor.execute("DROP TABLE IF EXISTS merchandisers")
    cursor.execute("DROP TABLE IF EXISTS shoes")
    cursor.execute("DROP TABLE IF EXISTS clothing")
    cursor.execute("DROP TABLE IF EXISTS accessories")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS merchandisers (
        merchandiser_id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(100) NOT NULL,
        region VARCHAR(50) NOT NULL, 
        country VARCHAR(50) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        phone VARCHAR(20) UNIQUE NOT NULL);
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id INT PRIMARY KEY AUTO_INCREMENT,
        merchandiser_id INT NOT NULL,
        product_id INT NOT NULL, 
        quantity INT NOT NULL CHECK (quantity > 0),
        order_date DATE NOT NULL DEFAULT (CURRENT_DATE),
        status ENUM('Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled') DEFAULT 'Pending',
        total_cost DECIMAL(10,2) NOT NULL,
        FOREIGN KEY (merchandiser_id) REFERENCES merchandisers(merchandiser_id) ON DELETE CASCADE);
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS shoes (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(255) NOT NULL,
        type VARCHAR(255) NOT NULL,
        age_group VARCHAR(255) NOT NULL,
        gender VARCHAR(255) NOT NULL,
        year INT NOT NULL,
        retail_price INT NOT NULL,
        factory_cost INT NOT NULL,
        target_cost INT NOT NULL,
        sold INT NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clothing (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(255) NOT NULL,
        type VARCHAR(255) NOT NULL,
        age_group VARCHAR(255) NOT NULL,
        gender VARCHAR(255) NOT NULL,
        year INT NOT NULL,
        retail_price INT NOT NULL,
        factory_cost INT NOT NULL,
        target_cost INT NOT NULL,
        sold INT NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS accessories (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(255) NOT NULL,
        type VARCHAR(255) NOT NULL,
        age_group VARCHAR(255) NOT NULL,
        gender VARCHAR(255) NOT NULL,
        year INT NOT NULL,
        retail_price INT NOT NULL,
        factory_cost INT NOT NULL,
        target_cost INT NOT NULL,
        sold INT NOT NULL
    )
    """)

    cursor.execute("""
    INSERT INTO merchandisers (merchandiser_id, name, region, country, email, phone) VALUES
    (1, 'Puma Singapore Official Store', 'Southeast Asia', 'Singapore', 'support.sg@puma.com', '+65 91234567'),
    (2, 'Puma Japan Retail Group', 'East Asia', 'Japan', 'support.jp@puma.com', '+81 9034567890'),
    (3, 'Puma Hong Kong Limited', 'East Asia', 'Hong Kong', 'support.hk@puma.com', '+852 67890123'),
    (4, 'Puma India Distributors', 'South Asia', 'India', 'support.in@puma.com', '+91 9876543210'),
    (5, 'Puma Malaysia Official', 'Southeast Asia', 'Malaysia', 'support.my@puma.com', '+60 123456789'),
    (6, 'Puma Vietnam Group', 'Southeast Asia', 'Vietnam', 'support.vn@puma.com', '+84 987654321'),
    (7, 'Puma China Regional HQ', 'East Asia', 'China', 'support.cn@puma.com', '+86 13567891234'),
    (8, 'Puma Indonesia Partners', 'Southeast Asia', 'Indonesia', 'support.id@puma.com', '+62 81234567890'),
    (9, 'Puma Korea Corporation', 'East Asia', 'South Korea', 'support.kr@puma.com', '+82 1023456789'),
    (10, 'Puma Bangladesh Distribution', 'South Asia', 'Bangladesh', 'support.bd@puma.com', '+880 1776543210');
    """)
    print("Merchandisers data inserted successfully")
    cursor.execute("""
    INSERT INTO orders (order_id, merchandiser_id, product_id, quantity, order_date, status, total_cost) VALUES
    (1, 1, 1, 50, '2025-01-10', 'Pending', 7500.00),
    (2, 2, 2, 30, '2025-01-12', 'Processing', 4500.00),
    (3, 3, 3, 20, '2025-01-15', 'Shipped', 3200.00),
    (4, 4, 4, 25, '2025-01-18', 'Delivered', 5000.00),
    (5, 5, 5, 40, '2025-01-20', 'Pending', 6400.00),
    (6, 6, 6, 15, '2025-01-22', 'Cancelled', 2250.00),
    (7, 7, 7, 60, '2025-01-25', 'Processing', 9600.00),
    (8, 8, 8, 10, '2025-01-28', 'Shipped', 1800.00),
    (9, 9, 9, 35, '2025-01-30', 'Pending', 5600.00),
    (10, 10, 10, 45, '2025-02-02', 'Delivered', 7200.00),
    (11, 1, 201, 20, '2025-02-05', 'Pending', 500.00),
    (12, 2, 202, 25, '2025-02-07', 'Processing', 500.00),
    (13, 3, 203, 15, '2025-02-10', 'Shipped', 900.00),
    (14, 4, 204, 30, '2025-02-12', 'Delivered', 1650.00),
    (15, 5, 205, 10, '2025-02-15', 'Pending', 400.00),
    (16, 6, 206, 20, '2025-02-17', 'Cancelled', 700.00),
    (17, 7, 207, 25, '2025-02-20', 'Processing', 750.00),
    (18, 8, 208, 30, '2025-02-22', 'Shipped', 750.00),
    (19, 9, 209, 15, '2025-02-25', 'Pending', 750.00),
    (20, 10, 210, 20, '2025-02-28', 'Delivered', 900.00),
    (21, 1, 301, 10, '2025-03-01', 'Pending', 350.00),
    (22, 2, 302, 15, '2025-03-03', 'Processing', 270.00),
    (23, 3, 303, 20, '2025-03-05', 'Shipped', 900.00),
    (24, 4, 304, 25, '2025-03-07', 'Delivered', 750.00),
    (25, 5, 305, 30, '2025-03-09', 'Pending', 1650.00),
    (26, 6, 306, 35, '2025-03-11', 'Cancelled', 2800.00),
    (27, 7, 307, 40, '2025-03-13', 'Processing', 3600.00),
    (28, 8, 308, 45, '2025-03-15', 'Shipped', 1890.00),
    (29, 9, 309, 50, '2025-03-17', 'Pending', 1100.00),
    (30, 10, 310, 55, '2025-03-19', 'Delivered', 1045.00);
    """)

    cursor.execute("""
    INSERT INTO shoes (id, name, type, age_group, gender, year, retail_price, factory_cost, target_cost, sold) VALUES
    (1, 'Puma Suede Classic', 'Sneakers', 'Adult', 'Unisex', 2021, 70, 30, 50, 100),
    (2, 'Puma RS-X', 'Running', 'Adult', 'Unisex', 2022, 110, 50, 80, 150),
    (3, 'Puma Cali', 'Casual', 'Adult', 'Female', 2021, 90, 40, 60, 200),
    (4, 'Puma Future Rider', 'Sneakers', 'Adult', 'Male', 2022, 80, 35, 55, 120),
    (5, 'Puma Smash', 'Casual', 'Adult', 'Unisex', 2021, 60, 25, 45, 90),
    (6, 'Puma Ignite', 'Running', 'Adult', 'Unisex', 2022, 100, 45, 70, 130),
    (7, 'Puma Roma', 'Sneakers', 'Adult', 'Unisex', 2021, 75, 32, 52, 110),
    (8, 'Puma Enzo', 'Training', 'Kid', 'Male', 2022, 85, 38, 58, 140),
    (9, 'Puma Cell', 'Running', 'Kid', 'Female', 2021, 95, 42, 65, 160),
    (10, 'Puma Thunder', 'Casual', 'Kid', 'Unisex', 2022, 120, 55, 85, 170),
    (11, 'Puma RS Dreamer', 'Basketball', 'Adult', 'Unisex', 2023, 125, 55, 90, 180),
    (12, 'Puma Deviate Nitro', 'Running', 'Adult', 'Male', 2023, 160, 70, 110, 140),
    (13, 'Puma Fierce', 'Training', 'Adult', 'Female', 2022, 90, 40, 65, 200),
    (14, 'Puma Soft Ride', 'Casual', 'Kid', 'Unisex', 2021, 55, 22, 40, 120),
    (15, 'Puma Evospeed', 'Football', 'Adult', 'Male', 2023, 130, 60, 95, 100),
    (16, 'Puma Axelion', 'Training', 'Adult', 'Unisex', 2022, 85, 38, 60, 150),
    (17, 'Puma Drift Cat', 'Casual', 'Adult', 'Unisex', 2021, 75, 32, 55, 90),
    (18, 'Puma RBD Game', 'Sneakers', 'Kid', 'Male', 2022, 65, 28, 48, 130),
    (19, 'Puma Court Rider', 'Basketball', 'Kid', 'Female', 2023, 110, 50, 85, 160),
    (20, 'Puma Future Z', 'Football', 'Adult', 'Unisex', 2022, 145, 65, 100, 175),
    (21, 'Puma Velocity Nitro', 'Running', 'Adult', 'Female', 2023, 150, 68, 105, 140),
    (22, 'Puma Viz Runner', 'Running', 'Kid', 'Unisex', 2021, 70, 30, 50, 90),
    (23, 'Puma Tazon 6', 'Training', 'Adult', 'Male', 2022, 95, 42, 70, 125),
    (24, 'Puma Retaliate', 'Casual', 'Kid', 'Female', 2023, 80, 35, 60, 110),
    (25, 'Puma Speedcat', 'Sneakers', 'Adult', 'Unisex', 2022, 100, 45, 75, 130),
    (26, 'Puma EvoTouch', 'Football', 'Adult', 'Male', 2021, 140, 62, 98, 95),
    (27, 'Puma Clyde', 'Sneakers', 'Adult', 'Unisex', 2023, 110, 50, 80, 140),
    (28, 'Puma Ultra', 'Football', 'Kid', 'Male', 2023, 120, 55, 90, 115),
    (29, 'Puma Anzarun', 'Casual', 'Kid', 'Female', 2021, 75, 32, 55, 125),
    (30, 'Puma California', 'Sneakers', 'Adult', 'Unisex', 2022, 95, 40, 70, 170),
    (31, 'Puma Smash V2', 'Casual', 'Adult', 'Unisex', 2020, 60, 25, 45, 85),
    (32, 'Puma Mirage Sport', 'Sneakers', 'Adult', 'Male', 2024, 120, 50, 90, 135),
    (33, 'Puma RS-Fast', 'Running', 'Adult', 'Unisex', 2023, 140, 65, 100, 125),
    (34, 'Puma Softride Sophia', 'Training', 'Adult', 'Female', 2022, 85, 38, 60, 175),
    (35, 'Puma Evopower', 'Football', 'Adult', 'Male', 2021, 135, 60, 95, 110),
    (36, 'Puma Suede VTG', 'Sneakers', 'Adult', 'Unisex', 2020, 80, 35, 55, 150),
    (37, 'Puma Cali Star', 'Casual', 'Kid', 'Female', 2023, 95, 42, 70, 140),
    (38, 'Puma Grip Fusion', 'Golf', 'Adult', 'Male', 2024, 110, 50, 85, 95),
    (39, 'Puma Deviate Elite', 'Running', 'Adult', 'Unisex', 2022, 160, 75, 120, 130),
    (40, 'Puma Super Liga', 'Sneakers', 'Kid', 'Unisex', 2021, 70, 30, 50, 120),
    (41, 'Puma King Platinum', 'Football', 'Adult', 'Male', 2024, 150, 70, 110, 100),
    (42, 'Puma Anzarun Lite', 'Casual', 'Adult', 'Unisex', 2020, 65, 28, 50, 90),
    (43, 'Puma RS-X3', 'Running', 'Adult', 'Unisex', 2021, 130, 60, 95, 135),
    (44, 'Puma Proadapt', 'Golf', 'Adult', 'Male', 2023, 145, 68, 110, 105),
    (45, 'Puma Electron', 'Training', 'Kid', 'Female', 2024, 90, 40, 65, 125),
    (46, 'Puma Sky Dreamer', 'Basketball', 'Adult', 'Unisex', 2022, 125, 55, 90, 160),
    (47, 'Puma Hybrid NX', 'Running', 'Kid', 'Male', 2020, 85, 38, 60, 140),
    (48, 'Puma Thunder Spectra', 'Casual', 'Adult', 'Unisex', 2024, 120, 55, 85, 130),
    (49, 'Puma Carina', 'Sneakers', 'Kid', 'Female', 2021, 75, 32, 55, 145),
    (50, 'Puma Future 5.1', 'Football', 'Kid', 'Male', 2023, 110, 50, 85, 115)
    """)

    cursor.execute("""
    INSERT INTO clothing (id, name, type, age_group, gender, year, retail_price, factory_cost, target_cost, sold) VALUES
    (201, 'Puma T-shirt 1', 'T-shirt', 'Adult', 'Unisex', 2023, 25, 10, 15, 100),
    (202, 'Puma T-shirt 2', 'T-shirt', 'Kid', 'Unisex', 2023, 20, 8, 12, 150),
    (203, 'Puma Jacket 1', 'Jacket', 'Adult', 'Male', 2023, 60, 30, 40, 200),
    (204, 'Puma Jacket 2', 'Jacket', 'Kid', 'Female', 2023, 55, 25, 35, 180),
    (205, 'Puma Trousers 1', 'Trousers', 'Adult', 'Female', 2023, 40, 20, 25, 120),
    (206, 'Puma Trousers 2', 'Trousers', 'Kid', 'Male', 2023, 35, 15, 20, 140),
    (207, 'Puma Shorts 1', 'Shorts', 'Adult', 'Unisex', 2023, 30, 12, 18, 130),
    (208, 'Puma Shorts 2', 'Shorts', 'Kid', 'Unisex', 2020, 25, 10, 15, 160),
    (209, 'Puma Hoodie 1', 'Hoodie', 'Adult', 'Male', 2021, 50, 22, 30, 110),
    (210, 'Puma Hoodie 2', 'Hoodie', 'Kid', 'Female', 2020, 45, 20, 28, 170),
    (211, 'Puma T-shirt 3', 'T-shirt', 'Adult', 'Unisex', 2020, 22, 9, 14, 90),
    (212, 'Puma Jacket 3', 'Jacket', 'Kid', 'Male', 2020, 50, 28, 38, 130),
    (213, 'Puma Shorts 3', 'Shorts', 'Adult', 'Female', 2020, 28, 11, 17, 120),
    (214, 'Puma Hoodie 3', 'Hoodie', 'Kid', 'Unisex', 2020, 40, 18, 26, 140),
    (215, 'Puma Trousers 3', 'Trousers', 'Adult', 'Male', 2021, 42, 21, 27, 100),
    (216, 'Puma T-shirt 4', 'T-shirt', 'Kid', 'Unisex', 2021, 19, 7, 11, 80),
    (217, 'Puma Jacket 4', 'Jacket', 'Adult', 'Female', 2020, 58, 27, 37, 150),
    (218, 'Puma Hoodie 4', 'Hoodie', 'Kid', 'Male', 2021, 48, 20, 29, 160),
    (219, 'Puma T-shirt 5', 'T-shirt', 'Adult', 'Male', 2022, 24, 10, 14, 95),
    (220, 'Puma Jacket 5', 'Jacket', 'Kid', 'Female', 2021, 53, 26, 34, 135),
    (221, 'Puma Shorts 4', 'Shorts', 'Adult', 'Unisex', 2022, 29, 12, 18, 125),
    (222, 'Puma Hoodie 5', 'Hoodie', 'Kid', 'Unisex', 2022, 42, 19, 27, 145),
    (223, 'Puma Trousers 4', 'Trousers', 'Adult', 'Female', 2023, 38, 19, 24, 115),
    (224, 'Puma T-shirt 6', 'T-shirt', 'Kid', 'Male', 2024, 21, 9, 13, 85),
    (225, 'Puma Jacket 6', 'Jacket', 'Adult', 'Unisex', 2021, 65, 33, 43, 175),
    (226, 'Puma Hoodie 6', 'Hoodie', 'Kid', 'Female', 2022, 47, 21, 30, 165),
    (227, 'Puma T-shirt 7', 'T-shirt', 'Adult', 'Female', 2024, 27, 11, 16, 105),
    (228, 'Puma Shorts 5', 'Shorts', 'Kid', 'Unisex', 2024, 26, 10, 15, 150),
    (229, 'Puma Hoodie 7', 'Hoodie', 'Adult', 'Male', 2024, 55, 23, 32, 130),
    (230, 'Puma Jacket 7', 'Jacket', 'Kid', 'Male', 2024, 52, 24, 33, 145),
    (231, 'Puma Trousers 5', 'Trousers', 'Adult', 'Unisex', 2025, 44, 22, 28, 140),
    (232, 'Puma T-shirt 8', 'T-shirt', 'Kid', 'Female', 2025, 23, 10, 14, 90),
    (233, 'Puma Jacket 8', 'Jacket', 'Adult', 'Male', 2025, 67, 34, 45, 185),
    (234, 'Puma Hoodie 8', 'Hoodie', 'Kid', 'Unisex', 2025, 50, 22, 31, 170),
    (235, 'Puma Tank Top 1', 'Tank Top', 'Adult', 'Unisex', 2020, 20, 7, 12, 80),
    (236, 'Puma Sweatpants 1', 'Sweatpants', 'Kid', 'Male', 2021, 37, 16, 22, 125),
    (237, 'Puma Track Jacket 1', 'Track Jacket', 'Adult', 'Female', 2022, 60, 29, 38, 140),
    (238, 'Puma Vest 1', 'Vest', 'Kid', 'Unisex', 2023, 35, 14, 20, 135),
    (239, 'Puma Polo Shirt 1', 'Polo Shirt', 'Adult', 'Male', 2024, 32, 12, 18, 110),
    (240, 'Puma Windbreaker 1', 'Windbreaker', 'Kid', 'Female', 2025, 58, 28, 36, 155);
    """)
    cursor.execute("""
    INSERT INTO accessories (id, name, type, age_group, gender, year, retail_price, factory_cost, target_cost, sold) VALUES
    (301, 'Leather Gloves', 'Handwear', 'Adult', 'Unisex', 2020, 35, 14, 22, 95),
    (302, 'Sports Cap', 'Headwear', 'Kid', 'Unisex', 2020, 18, 7, 11, 120),
    (303, 'Silk Scarf', 'Neckwear', 'Adult', 'Female', 2020, 45, 18, 28, 85),
    (304, 'Canvas Belt', 'Waistwear', 'Adult', 'Male', 2020, 30, 12, 18, 100),
    (305, 'Aviator Sunglasses', 'Eyewear', 'Adult', 'Male', 2021, 55, 22, 32, 70),
    (306, 'Digital Watch', 'Wristwear', 'Kid', 'Unisex', 2021, 80, 35, 50, 90),
    (307, 'Travel Backpack', 'Bag', 'Adult', 'Unisex', 2021, 90, 38, 55, 60),
    (308, 'Leather Wallet', 'Accessory', 'Adult', 'Unisex', 2021, 42, 17, 26, 110),
    (309, 'Beanie', 'Headwear', 'Adult', 'Unisex', 2022, 22, 9, 14, 125),
    (310, 'Winter Scarf', 'Neckwear', 'Kid', 'Unisex', 2022, 19, 8, 12, 150),
    (311, 'Touchscreen Gloves', 'Handwear', 'Adult', 'Unisex', 2022, 32, 12, 20, 140),
    (312, 'Casual Belt', 'Waistwear', 'Adult', 'Female', 2022, 28, 11, 17, 105),
    (313, 'Sport Sunglasses', 'Eyewear', 'Adult', 'Unisex', 2023, 48, 19, 28, 95),
    (314, 'Smart Watch', 'Wristwear', 'Adult', 'Unisex', 2023, 120, 50, 75, 50),
    (315, 'Laptop Backpack', 'Bag', 'Adult', 'Unisex', 2023, 85, 34, 50, 80),
    (316, 'Minimalist Wallet', 'Accessory', 'Adult', 'Male', 2023, 38, 15, 22, 100),
    (317, 'Flat Cap', 'Headwear', 'Adult', 'Male', 2024, 24, 10, 15, 130),
    (318, 'Fashion Scarf', 'Neckwear', 'Adult', 'Female', 2024, 26, 11, 16, 110),
    (319, 'Winter Gloves', 'Handwear', 'Kid', 'Unisex', 2024, 28, 10, 16, 115),
    (320, 'Reversible Belt', 'Waistwear', 'Adult', 'Unisex', 2024, 34, 14, 21, 95),
    (321, 'Designer Sunglasses', 'Eyewear', 'Adult', 'Unisex', 2025, 65, 30, 40, 75),
    (322, 'Analog Watch', 'Wristwear', 'Adult', 'Male', 2025, 110, 45, 70, 65),
    (323, 'Hiking Backpack', 'Bag', 'Adult', 'Unisex', 2025, 100, 42, 60, 55),
    (324, 'RFID Wallet', 'Accessory', 'Adult', 'Unisex', 2025, 45, 18, 28, 90),
    (325, 'Snapback Cap', 'Headwear', 'Adult', 'Unisex', 2020, 20, 8, 12, 140),
    (326, 'Silk Tie', 'Neckwear', 'Adult', 'Male', 2021, 30, 12, 18, 100),
    (327, 'Fleece Gloves', 'Handwear', 'Adult', 'Unisex', 2022, 33, 14, 20, 120),
    (328, 'Stretch Belt', 'Waistwear', 'Adult', 'Female', 2023, 36, 15, 22, 85),
    (329, 'Wayfarer Sunglasses', 'Eyewear', 'Adult', 'Unisex', 2024, 50, 20, 30, 90),
    (330, 'Luxury Watch', 'Wristwear', 'Adult', 'Unisex', 2025, 200, 80, 120, 30),
    (331, 'Hat', 'Headwear', 'Adult', 'Unisex', 2021, 25, 10, 15, 100),
    (332, 'Scarf', 'Neckwear', 'Adult', 'Unisex', 2021, 20, 8, 12, 150),
    (333, 'Gloves', 'Handwear', 'Adult', 'Unisex', 2021, 30, 12, 18, 200),
    (334, 'Belt', 'Waistwear', 'Adult', 'Unisex', 2021, 35, 14, 21, 120),
    (335, 'Sunglasses', 'Eyewear', 'Adult', 'Unisex', 2023, 50, 20, 30, 80),
    (336, 'Watch', 'Wristwear', 'Adult', 'Unisex', 2023, 100, 40, 60, 60),
    (337, 'Backpack', 'Bag', 'Adult', 'Unisex', 2023, 75, 30, 45, 90),
    (338, 'Wallet', 'Accessory', 'Adult', 'Unisex', 2023, 40, 16, 24, 110),
    (339, 'Cap', 'Headwear', 'Adult', 'Unisex', 2023, 20, 8, 12, 130),
    (340, 'Tie', 'Neckwear', 'Adult', 'Unisex', 2023, 25, 10, 15, 140);
    """)
    con.commit()
    cursor.close()
    con.close()

@app.route('/get_merchandisers', methods=['GET'])
def get_merchandisers():
    con = pool.get_connection()
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM merchandisers")
    merchandisers = cursor.fetchall()
    cursor.close()
    con.close()
    return jsonify(merchandisers)

@app.route('/add_merchandiser', methods=['POST'])
def add_merchandiser():
    con = pool.get_connection()
    data = request.get_json()
    cursor = con.cursor()
    cursor.execute("""
        INSERT INTO merchandisers (name, region, country, email, phone)
        VALUES (%s, %s, %s, %s, %s)
    """, (data['name'], data['region'], data['country'], data['email'], data['phone']))
    con.commit()
    cursor.close()
    con.close()
    return jsonify({'message': 'Merchandiser added successfully'}), 201

@app.route('/update_merchandiser/<int:id>', methods=['PUT'])
def update_merchandiser(id):
    con = pool.get_connection()
    data = request.get_json()
    cursor = con.cursor()
    cursor.execute("""
        UPDATE merchandisers
        SET name=%s, region=%s, country=%s, email=%s, phone=%s
        WHERE merchandiser_id=%s
    """, (data['name'], data['region'], data['country'], data['email'], data['phone'], id))
    con.commit()
    cursor.close()
    con.close()
    return jsonify({'message': 'Merchandiser updated successfully'})

@app.route('/delete_merchandiser/<int:id>', methods=['DELETE'])
def delete_merchandiser(id):
    con = pool.get_connection()
    cursor = con.cursor()
    cursor.execute("DELETE FROM merchandisers WHERE merchandiser_id=%s", (id,))
    con.commit()
    cursor.close()
    con.close()
    return jsonify({'message': 'Merchandiser deleted successfully'})

@app.route('/get_orders', methods=['GET'])
def get_orders():
    con = pool.get_connection()
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    cursor.close()
    con.close()
    return jsonify(orders)

@app.route('/add_order', methods=['POST'])
def add_order():
    con = pool.get_connection()
    data = request.get_json()
    cursor = con.cursor()
    cursor.execute("""
        INSERT INTO orders (merchandiser_id, product_id, quantity, order_date, status, total_cost)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (data['merchandiser_id'], data['product_id'], data['quantity'], data['order_date'], data['status'], data['total_cost']))
    con.commit()
    cursor.close()
    con.close()
    return jsonify({'message': 'Order added successfully'}), 201

@app.route('/update_order/<int:id>', methods=['PUT'])
def update_order(id):
    con = pool.get_connection()
    data = request.get_json()
    cursor = con.cursor()
    cursor.execute("""
        UPDATE orders
        SET merchandiser_id=%s, product_id=%s, quantity=%s, order_date=%s, status=%s, total_cost=%s
        WHERE order_id=%s
    """, (data['merchandiser_id'], data['product_id'], data['quantity'], data['order_date'], data['status'], data['total_cost'], id))
    con.commit()
    cursor.close()
    con.close()
    return jsonify({'message': 'Order updated successfully'})

@app.route('/delete_order/<int:id>', methods=['DELETE'])
def delete_order(id):
    con = pool.get_connection()
    cursor = con.cursor()
    cursor.execute("DELETE FROM orders WHERE order_id=%s", (id,))
    con.commit()
    cursor.close()
    con.close()
    return jsonify({'message': 'Order deleted successfully'})

@app.route('/get_shoe_sale', methods=['GET'])
def get_shoe_sale():
    con = pool.get_connection()
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT retail_price, sold FROM shoes")
    shoes = cursor.fetchall()
    total_revenue = sum(shoe['retail_price'] * shoe['sold'] for shoe in shoes)
    cursor.close()
    con.close()
    return jsonify({'total_revenue': total_revenue})

@app.route('/get_shoe', methods=['GET'])
def get_shoe():
    con = pool.get_connection()
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM shoes")
    shoes = cursor.fetchall()
    cursor.close()
    con.close()
    return jsonify(shoes)

@app.route('/add_shoe', methods=['POST'])
def add_shoe():
    con = pool.get_connection()
    data = request.get_json()
    cursor = con.cursor()
    cursor.execute("""
        INSERT INTO shoes (name, type, age_group, gender, year, retail_price, factory_cost, target_cost, sold)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (data['name'], data['type'], data['age_group'], data['gender'], data['year'], data['retail_price'], data['factory_cost'], data['target_cost'], data['sold']))
    con.commit()
    cursor.close()
    con.close()
    return jsonify({'message': 'Shoe added successfully'}), 201

@app.route('/update_shoe/<int:id>', methods=['PUT'])
def update_shoe(id):
    con = pool.get_connection()
    data = request.get_json()
    cursor = con.cursor()
    cursor.execute("""
        UPDATE shoes
        SET name=%s, type=%s, age_group=%s, gender=%s, year=%s, retail_price=%s, factory_cost=%s, target_cost=%s, sold=%s
        WHERE id=%s
    """, (data['name'], data['type'], data['age_group'], data['gender'], data['year'], data['retail_price'], data['factory_cost'], data['target_cost'], data['sold'], id))
    con.commit()
    cursor.close()
    con.close()
    return jsonify({'message': 'Shoe updated successfully'})

@app.route('/delete_shoe/<int:id>', methods=['DELETE'])
def delete_shoe(id):
    con = pool.get_connection()
    cursor = con.cursor()
    cursor.execute("DELETE FROM shoes WHERE id=%s", (id,))
    con.commit()
    cursor.close()
    con.close()
    return jsonify({'message': 'Shoe deleted successfully'})

@app.route('/get_clothing_sale', methods=['GET'])
def get_clothing_sale():
    con = pool.get_connection()
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT retail_price, sold FROM clothing")
    shoes = cursor.fetchall()
    total_revenue = sum(shoe['retail_price'] * shoe['sold'] for shoe in shoes)
    cursor.close()
    con.close()
    return jsonify({'total_revenue': total_revenue})

@app.route('/get_clothing', methods=['GET'])
def get_clothing():
    con = pool.get_connection()
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clothing")
    clothing = cursor.fetchall()
    cursor.close()
    con.close()
    return jsonify(clothing)

@app.route('/add_clothing', methods=['POST'])
def add_clothing():
    con = pool.get_connection()
    data = request.get_json()
    cursor = con.cursor()
    cursor.execute("""
        INSERT INTO clothing (name, type, age_group, gender, year, retail_price, factory_cost, target_cost, sold)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (data['name'], data['type'], data['age_group'], data['gender'], data['year'], data['retail_price'], data['factory_cost'], data['target_cost'], data['sold']))
    con.commit()
    cursor.close()
    con.close()
    return jsonify({'message': 'Clothing added successfully'}), 201

@app.route('/update_clothing/<int:id>', methods=['PUT'])
def update_clothing(id):
    con = pool.get_connection()
    data = request.get_json()
    cursor = con.cursor()
    cursor.execute("""
        UPDATE clothing
        SET name=%s, type=%s, age_group=%s, gender=%s, year=%s, retail_price=%s, factory_cost=%s, target_cost=%s, sold=%s
        WHERE id=%s
    """, (data['name'], data['type'], data['age_group'], data['gender'], data['year'], data['retail_price'], data['factory_cost'], data['target_cost'], data['sold'], id))
    con.commit()
    cursor.close()
    con.close()
    return jsonify({'message': 'Clothing updated successfully'})

@app.route('/get_accessory_sale', methods=['GET'])
def get_accessories_sale():
    con = pool.get_connection()
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT retail_price, sold FROM accessories")
    shoes = cursor.fetchall()
    total_revenue = sum(shoe['retail_price'] * shoe['sold'] for shoe in shoes)
    cursor.close()
    con.close()
    return jsonify({'total_revenue': total_revenue})

@app.route('/get_accessory', methods=['GET'])
def get_accessories():
    con = pool.get_connection()
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM accessories")
    accessories = cursor.fetchall()
    cursor.close()
    con.close()
    return jsonify(accessories)

@app.route('/delete_clothing/<int:id>', methods=['DELETE'])
def delete_clothing(id):
    con = pool.get_connection()
    cursor = con.cursor()
    cursor.execute("DELETE FROM clothing WHERE id=%s", (id,))
    con.commit()
    cursor.close()
    con.close()
    return jsonify({'message': 'Clothing deleted successfully'})

@app.route('/add_accessory', methods=['POST'])
def add_accessory():
    con = pool.get_connection()
    data = request.get_json()
    cursor = con.cursor()
    cursor.execute("""
        INSERT INTO accessories (name, type, age_group, gender, year, retail_price, factory_cost, target_cost, sold)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (data['name'], data['type'], data['age_group'], data['gender'], data['year'], data['retail_price'], data['factory_cost'], data['target_cost'], data['sold']))
    con.commit()
    cursor.close()
    con.close()
    return jsonify({'message': 'Accessory added successfully'}), 201

@app.route('/update_accessory/<int:id>', methods=['PUT'])
def update_accessory(id):
    con = pool.get_connection()
    data = request.get_json()
    cursor = con.cursor()
    cursor.execute("""
        UPDATE accessories
        SET name=%s, type=%s, age_group=%s, gender=%s, year=%s, retail_price=%s, factory_cost=%s, target_cost=%s, sold=%s
        WHERE id=%s
    """, (data['name'], data['type'], data['age_group'], data['gender'], data['year'], data['retail_price'], data['factory_cost'], data['target_cost'], data['sold'], id))
    con.commit()
    cursor.close()
    con.close()
    return jsonify({'message': 'Accessory updated successfully'})

@app.route('/delete_accessory/<int:id>', methods=['DELETE'])
def delete_accessory(id):
    con = pool.get_connection()
    cursor = con.cursor()
    cursor.execute("DELETE FROM accessories WHERE id=%s", (id,))
    con.commit()
    cursor.close()
    con.close()
    return jsonify({'message': 'Accessory deleted successfully'})


if __name__ == '__main__':
    print('Server is running')
    setup_database()
    app.run(debug=True)