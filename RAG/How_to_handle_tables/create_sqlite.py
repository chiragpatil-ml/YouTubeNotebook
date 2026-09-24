
import sqlite3
from datetime import date, timedelta
from pathlib import Path


DB_FILE = "data/customer_analytics.db"

NUM_CUSTOMERS = 100


# ============================================================
# Create database directory
# ============================================================

Path(DB_FILE).parent.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# Create Database
# ============================================================

def create_database():

    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON")

    # Drop existing tables
    cursor.executescript("""
        DROP TABLE IF EXISTS order_items;
        DROP TABLE IF EXISTS orders;
        DROP TABLE IF EXISTS payments;
        DROP TABLE IF EXISTS support_tickets;
        DROP TABLE IF EXISTS subscriptions;
        DROP TABLE IF EXISTS products;
        DROP TABLE IF EXISTS categories;
        DROP TABLE IF EXISTS customers;
    """)

    # ========================================================
    # Customers
    # ========================================================

    cursor.execute("""
        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            signup_date DATE NOT NULL,
            country TEXT NOT NULL
        )
    """)

    # ========================================================
    # Categories
    # ========================================================

    cursor.execute("""
        CREATE TABLE categories (
            category_id INTEGER PRIMARY KEY,
            category_name TEXT NOT NULL
        )
    """)

    # ========================================================
    # Products
    # ========================================================

    cursor.execute("""
        CREATE TABLE products (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT NOT NULL,
            category_id INTEGER NOT NULL,
            price REAL NOT NULL,

            FOREIGN KEY (category_id)
                REFERENCES categories(category_id)
        )
    """)

    # ========================================================
    # Subscriptions
    # ========================================================

    cursor.execute("""
        CREATE TABLE subscriptions (
            subscription_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            plan TEXT NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE,
            status TEXT NOT NULL,

            FOREIGN KEY (customer_id)
                REFERENCES customers(customer_id)
        )
    """)

    # ========================================================
    # Support Tickets
    # ========================================================

    cursor.execute("""
        CREATE TABLE support_tickets (
            ticket_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            created_at DATE NOT NULL,
            status TEXT NOT NULL,
            priority TEXT NOT NULL,

            FOREIGN KEY (customer_id)
                REFERENCES customers(customer_id)
        )
    """)

    # ========================================================
    # Payments
    # ========================================================

    cursor.execute("""
        CREATE TABLE payments (
            payment_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            payment_date DATE NOT NULL,
            amount REAL NOT NULL,
            status TEXT NOT NULL,

            FOREIGN KEY (customer_id)
                REFERENCES customers(customer_id)
        )
    """)

    # ========================================================
    # Orders
    # ========================================================

    cursor.execute("""
        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            order_date DATE NOT NULL,
            status TEXT NOT NULL,
            total_amount REAL NOT NULL,

            FOREIGN KEY (customer_id)
                REFERENCES customers(customer_id)
        )
    """)

    # ========================================================
    # Order Items
    # ========================================================

    cursor.execute("""
        CREATE TABLE order_items (
            order_item_id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,

            FOREIGN KEY (order_id)
                REFERENCES orders(order_id),

            FOREIGN KEY (product_id)
                REFERENCES products(product_id)
        )
    """)

    conn.commit()

    return conn


# ============================================================
# Categories
# ============================================================

def insert_categories(cursor):

    categories = [
        (1, "Electronics"),
        (2, "Home & Kitchen"),
        (3, "Sports"),
        (4, "Books"),
        (5, "Fashion"),
        (6, "Beauty"),
        (7, "Toys"),
        (8, "Office"),
    ]

    cursor.executemany("""
        INSERT INTO categories
        (
            category_id,
            category_name
        )
        VALUES (?, ?)
    """, categories)


# ============================================================
# Products
# ============================================================

def insert_products(cursor):

    products = [

        (1, "MacBook Pro", 1, 1999.00),
        (2, "Dell XPS 15", 1, 1799.00),
        (3, "iPhone 16", 1, 999.00),
        (4, "Samsung Galaxy S25", 1, 899.00),
        (5, "iPad Air", 1, 699.00),
        (6, "Dell Monitor 27", 1, 349.00),
        (7, "Sony Headphones", 1, 299.00),
        (8, "Apple Watch", 1, 499.00),

        (9, "Air Fryer", 2, 149.00),
        (10, "Coffee Maker", 2, 199.00),
        (11, "Kitchen Blender", 2, 129.00),
        (12, "Robot Vacuum", 2, 399.00),

        (13, "Running Shoes", 3, 120.00),
        (14, "Yoga Mat", 3, 45.00),
        (15, "Dumbbells Set", 3, 90.00),
        (16, "Basketball", 3, 35.00),

        (17, "Python Programming", 4, 55.00),
        (18, "Machine Learning Book", 4, 70.00),
        (19, "Data Science Handbook", 4, 65.00),

        (20, "Premium T-Shirt", 5, 40.00),
        (21, "Denim Jeans", 5, 80.00),
        (22, "Winter Jacket", 5, 150.00),

        (23, "Face Wash", 6, 25.00),
        (24, "Skin Care Kit", 6, 75.00),

        (25, "Board Game", 7, 45.00),
        (26, "Toy Car", 7, 30.00),

        (27, "Office Chair", 8, 450.00),
        (28, "Standing Desk", 8, 600.00),
        (29, "Desk Lamp", 8, 70.00),
        (30, "Mechanical Keyboard", 8, 130.00),
    ]

    cursor.executemany("""
        INSERT INTO products
        (
            product_id,
            product_name,
            category_id,
            price
        )
        VALUES (?, ?, ?, ?)
    """, products)


# ============================================================
# Customers
# ============================================================

def insert_customers(cursor):

    customers = [

        (1, "Alex Carter", "alex.carter@example.com", "2024-01-15", "USA"),
        (2, "Sarah Miller", "sarah.miller@example.com", "2024-02-10", "USA"),
        (3, "Michael Brown", "michael.brown@example.com", "2024-02-21", "Canada"),
        (4, "Emma Wilson", "emma.wilson@example.com", "2024-03-05", "UK"),
        (5, "Daniel Smith", "daniel.smith@example.com", "2024-03-18", "USA"),
        (6, "Olivia Davis", "olivia.davis@example.com", "2024-04-02", "Australia"),
        (7, "James Taylor", "james.taylor@example.com", "2024-04-15", "USA"),
        (8, "Sophia Anderson", "sophia.anderson@example.com", "2024-05-01", "Canada"),
        (9, "William Thomas", "william.thomas@example.com", "2024-05-20", "UK"),
        (10, "Ava Moore", "ava.moore@example.com", "2024-06-01", "USA"),

        (11, "Noah Martin", "noah.martin@example.com", "2024-06-12", "Germany"),
        (12, "Mia Jackson", "mia.jackson@example.com", "2024-06-25", "USA"),
        (13, "Lucas White", "lucas.white@example.com", "2024-07-04", "Canada"),
        (14, "Isabella Harris", "isabella.harris@example.com", "2024-07-18", "USA"),
        (15, "Ethan Clark", "ethan.clark@example.com", "2024-08-01", "UK"),
        (16, "Amelia Lewis", "amelia.lewis@example.com", "2024-08-14", "USA"),
        (17, "Mason Walker", "mason.walker@example.com", "2024-08-29", "Australia"),
        (18, "Harper Hall", "harper.hall@example.com", "2024-09-10", "USA"),
        (19, "Logan Allen", "logan.allen@example.com", "2024-09-25", "Canada"),
        (20, "Evelyn Young", "evelyn.young@example.com", "2024-10-05", "USA"),

        (21, "Alexander King", "alexander.king@example.com", "2024-10-18", "UK"),
        (22, "Ella Wright", "ella.wright@example.com", "2024-11-01", "USA"),
        (23, "Henry Scott", "henry.scott@example.com", "2024-11-15", "Germany"),
        (24, "Camila Green", "camila.green@example.com", "2024-12-01", "USA"),
        (25, "Sebastian Baker", "sebastian.baker@example.com", "2024-12-15", "Canada"),
        (26, "Luna Adams", "luna.adams@example.com", "2025-01-05", "USA"),
        (27, "Jack Nelson", "jack.nelson@example.com", "2025-01-20", "UK"),
        (28, "Aria Hill", "aria.hill@example.com", "2025-02-02", "USA"),
        (29, "Owen Ramirez", "owen.ramirez@example.com", "2025-02-17", "Australia"),
        (30, "Scarlett Campbell", "scarlett.campbell@example.com", "2025-03-01", "USA"),

        (31, "Theodore Mitchell", "theodore.mitchell@example.com", "2025-03-15", "Canada"),
        (32, "Penelope Roberts", "penelope.roberts@example.com", "2025-04-01", "USA"),
        (33, "Mateo Carter", "mateo.carter@example.com", "2025-04-15", "UK"),
        (34, "Chloe Phillips", "chloe.phillips@example.com", "2025-05-01", "USA"),
        (35, "James Evans", "james.evans@example.com", "2025-05-15", "Germany"),
        (36, "Layla Turner", "layla.turner@example.com", "2025-06-01", "USA"),
        (37, "Benjamin Torres", "benjamin.torres@example.com", "2025-06-15", "Canada"),
        (38, "Riley Parker", "riley.parker@example.com", "2025-07-01", "USA"),
        (39, "Lucas Collins", "lucas.collins@example.com", "2025-07-15", "UK"),
        (40, "Nora Edwards", "nora.edwards@example.com", "2025-08-01", "USA"),

        (41, "Elijah Stewart", "elijah.stewart@example.com", "2025-08-15", "Australia"),
        (42, "Lily Sanchez", "lily.sanchez@example.com", "2025-09-01", "USA"),
        (43, "Oliver Morris", "oliver.morris@example.com", "2025-09-15", "Canada"),
        (44, "Grace Rogers", "grace.rogers@example.com", "2025-10-01", "USA"),
        (45, "Jacob Reed", "jacob.reed@example.com", "2025-10-15", "UK"),
        (46, "Zoey Cook", "zoey.cook@example.com", "2025-11-01", "USA"),
        (47, "Levi Morgan", "levi.morgan@example.com", "2025-11-15", "Germany"),
        (48, "Hannah Bell", "hannah.bell@example.com", "2025-12-01", "USA"),
        (49, "Sebastian Murphy", "sebastian.murphy@example.com", "2025-12-15", "Canada"),
        (50, "Victoria Bailey", "victoria.bailey@example.com", "2026-01-05", "USA"),

        (51, "Samuel Rivera", "samuel.rivera@example.com", "2026-01-15", "UK"),
        (52, "Addison Cooper", "addison.cooper@example.com", "2026-01-25", "USA"),
        (53, "Daniel Richardson", "daniel.richardson@example.com", "2026-02-05", "Canada"),
        (54, "Aubrey Cox", "aubrey.cox@example.com", "2026-02-15", "USA"),
        (55, "Matthew Howard", "matthew.howard@example.com", "2026-02-25", "Australia"),
        (56, "Stella Ward", "stella.ward@example.com", "2026-03-05", "USA"),
        (57, "David Peterson", "david.peterson@example.com", "2026-03-15", "UK"),
        (58, "Hazel Gray", "hazel.gray@example.com", "2026-03-25", "USA"),
        (59, "Joseph James", "joseph.james@example.com", "2026-04-05", "Germany"),
        (60, "Ellie Watson", "ellie.watson@example.com", "2026-04-15", "USA"),

        (61, "John Brooks", "john.brooks@example.com", "2026-04-25", "Canada"),
        (62, "Violet Kelly", "violet.kelly@example.com", "2026-05-05", "USA"),
        (63, "Andrew Sanders", "andrew.sanders@example.com", "2026-05-15", "UK"),
        (64, "Aurora Price", "aurora.price@example.com", "2026-05-25", "USA"),
        (65, "Christopher Bennett", "christopher.bennett@example.com", "2026-06-01", "Australia"),
        (66, "Lucy Wood", "lucy.wood@example.com", "2026-06-10", "USA"),
        (67, "Anthony Barnes", "anthony.barnes@example.com", "2026-06-20", "Canada"),
        (68, "Paisley Ross", "paisley.ross@example.com", "2026-07-01", "USA"),
        (69, "Ryan Henderson", "ryan.henderson@example.com", "2026-07-05", "UK"),
        (70, "Naomi Coleman", "naomi.coleman@example.com", "2026-07-10", "USA"),

        (71, "Joshua Jenkins", "joshua.jenkins@example.com", "2026-07-15", "Germany"),
        (72, "Maya Perry", "maya.perry@example.com", "2026-07-20", "USA"),
        (73, "Nathan Powell", "nathan.powell@example.com", "2026-07-25", "Canada"),
        (74, "Isla Long", "isla.long@example.com", "2026-08-01", "USA"),
        (75, "Thomas Patterson", "thomas.patterson@example.com", "2026-08-03", "UK"),
        (76, "Elena Hughes", "elena.hughes@example.com", "2026-08-05", "USA"),
        (77, "Charles Flores", "charles.flores@example.com", "2026-08-07", "Australia"),
        (78, "Ruby Washington", "ruby.washington@example.com", "2026-08-10", "USA"),
        (79, "Isaac Butler", "isaac.butler@example.com", "2026-08-12", "Canada"),
        (80, "Clara Simmons", "clara.simmons@example.com", "2026-08-14", "USA"),

        (81, "Christopher Foster", "christopher.foster@example.com", "2026-08-15", "UK"),
        (82, "Alice Gonzales", "alice.gonzales@example.com", "2026-08-16", "USA"),
        (83, "Dylan Bryant", "dylan.bryant@example.com", "2026-08-17", "Germany"),
        (84, "Sofia Alexander", "sofia.alexander@example.com", "2026-08-18", "USA"),
        (85, "Andrew Russell", "andrew.russell@example.com", "2026-08-19", "Canada"),
        (86, "Eva Griffin", "eva.griffin@example.com", "2026-08-20", "USA"),
        (87, "Gabriel Diaz", "gabriel.diaz@example.com", "2026-08-21", "UK"),
        (88, "Madeline Hayes", "madeline.hayes@example.com", "2026-08-22", "USA"),
        (89, "Julian Myers", "julian.myers@example.com", "2026-08-23", "Australia"),
        (90, "Sarah Ford", "sarah.ford@example.com", "2026-08-24", "USA"),

        (91, "Isaac Hamilton", "isaac.hamilton@example.com", "2026-08-25", "Canada"),
        (92, "Peyton Graham", "peyton.graham@example.com", "2026-08-25", "USA"),
        (93, "Charles Sullivan", "charles.sullivan@example.com", "2026-08-26", "UK"),
        (94, "Madison Wallace", "madison.wallace@example.com", "2026-08-26", "USA"),
        (95, "Christian Woods", "christian.woods@example.com", "2026-08-27", "Germany"),
        (96, "Savannah Cole", "savannah.cole@example.com", "2026-08-27", "USA"),
        (97, "Jonathan West", "jonathan.west@example.com", "2026-08-28", "Canada"),
        (98, "Bella Jordan", "bella.jordan@example.com", "2026-08-28", "USA"),
        (99, "Aaron Owens", "aaron.owens@example.com", "2026-08-28", "UK"),
        (100, "Samantha Reynolds", "samantha.reynolds@example.com", "2026-08-28", "USA"),
    ]

    cursor.executemany("""
        INSERT INTO customers
        (
            customer_id,
            name,
            email,
            signup_date,
            country
        )
        VALUES (?, ?, ?, ?, ?)
    """, customers)


# ============================================================
# Subscriptions
# ============================================================

def insert_subscriptions(cursor):

    subscriptions = []

    subscription_id = 1

    # Customers 1-70 have realistic subscription history
    for customer_id in range(1, 71):

        # ----------------------------
        # July churn demo customers
        # ----------------------------

        if customer_id == 1:

            subscriptions.append((
                subscription_id,
                customer_id,
                "Pro",
                "2025-01-15",
                "2026-07-15",
                "cancelled"
            ))

        elif customer_id == 2:

            subscriptions.append((
                subscription_id,
                customer_id,
                "Enterprise",
                "2024-06-01",
                "2026-07-22",
                "cancelled"
            ))

        elif customer_id == 3:

            subscriptions.append((
                subscription_id,
                customer_id,
                "Basic",
                "2025-04-10",
                "2026-07-05",
                "cancelled"
            ))

        # ----------------------------
        # June churn
        # ----------------------------

        elif customer_id in [4, 5, 6]:

            subscriptions.append((
                subscription_id,
                customer_id,
                "Pro",
                "2025-01-01",
                f"2026-06-{10 + customer_id:02d}",
                "cancelled"
            ))

        # ----------------------------
        # August churn
        # ----------------------------

        elif customer_id in [7, 8]:

            subscriptions.append((
                subscription_id,
                customer_id,
                "Basic",
                "2025-03-01",
                f"2026-08-{10 + customer_id:02d}",
                "cancelled"
            ))

        # ----------------------------
        # Active customers
        # ----------------------------

        else:

            plan = (
                "Basic"
                if customer_id % 3 == 0
                else "Pro"
                if customer_id % 3 == 1
                else "Enterprise"
            )

            subscriptions.append((
                subscription_id,
                customer_id,
                plan,
                "2025-01-01",
                None,
                "active"
            ))

        subscription_id += 1

    cursor.executemany("""
        INSERT INTO subscriptions
        (
            subscription_id,
            customer_id,
            plan,
            start_date,
            end_date,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, subscriptions)


# ============================================================
# Support Tickets
# ============================================================

def insert_support_tickets(cursor):

    tickets = []

    ticket_id = 1

    # ========================================================
    # Carefully designed July churn examples
    # ========================================================

    demo_tickets = {

        # Alex Carter - 3 tickets
        1: [
            "2026-07-02",
            "2026-07-05",
            "2026-07-10"
        ],

        # Sarah Miller - 4 tickets
        2: [
            "2026-07-03",
            "2026-07-08",
            "2026-07-12",
            "2026-07-18"
        ],

        # Michael Brown - 2 tickets
        # Should NOT qualify
        3: [
            "2026-07-02",
            "2026-07-11"
        ],

        # June churn - many tickets
        4: [
            "2026-06-02",
            "2026-06-05",
            "2026-06-08"
        ],

        # August churn - many tickets
        7: [
            "2026-08-10",
            "2026-08-12",
            "2026-08-15"
        ]
    }

    for customer_id, dates in demo_tickets.items():

        for created_at in dates:

            tickets.append((
                ticket_id,
                customer_id,
                created_at,
                "closed",
                "high"
            ))

            ticket_id += 1

    # ========================================================
    # Other customers
    # ========================================================

    for customer_id in range(9, 71):

        number_of_tickets = 1 + (customer_id % 4)

        for i in range(number_of_tickets):

            # Spread tickets across 2025/2026
            month = (customer_id + i) % 8 + 1

            created_at = (
                f"2026-{month:02d}-{10 + i:02d}"
            )

            status = (
                "closed"
                if i % 2 == 0
                else "open"
            )

            priority = (
                "high"
                if i % 3 == 0
                else "medium"
            )

            tickets.append((
                ticket_id,
                customer_id,
                created_at,
                status,
                priority
            ))

            ticket_id += 1

    cursor.executemany("""
        INSERT INTO support_tickets
        (
            ticket_id,
            customer_id,
            created_at,
            status,
            priority
        )
        VALUES (?, ?, ?, ?, ?)
    """, tickets)


# ============================================================
# Payments
# ============================================================

def insert_payments(cursor):

    payments = []

    payment_id = 1

    for customer_id in range(1, 71):

        # Three payments per customer
        for month, amount in [
            (4, 99.00),
            (5, 149.00),
            (6, 199.00)
        ]:

            payments.append((
                payment_id,
                customer_id,
                f"2026-{month:02d}-15",
                amount,
                "completed"
            ))

            payment_id += 1

    cursor.executemany("""
        INSERT INTO payments
        (
            payment_id,
            customer_id,
            payment_date,
            amount,
            status
        )
        VALUES (?, ?, ?, ?, ?)
    """, payments)


# ============================================================
# Orders
# ============================================================

def insert_orders(cursor):

    orders = []

    order_id = 1

    # --------------------------------------------------------
    # Deterministic orders
    # --------------------------------------------------------

    order_data = {

        1: [
            ("2026-07-01", "completed", 1999),
            ("2026-07-15", "completed", 699),
        ],

        2: [
            ("2026-07-05", "completed", 999),
            ("2026-07-20", "completed", 399),
        ],

        3: [
            ("2026-07-03", "completed", 1799),
        ],

        4: [
            ("2026-06-10", "completed", 499),
        ],

        5: [
            ("2026-06-15", "completed", 349),
        ]
    }

    for customer_id, customer_orders in order_data.items():

        for order_date, status, total_amount in customer_orders:

            orders.append((
                order_id,
                customer_id,
                order_date,
                status,
                total_amount
            ))

            order_id += 1

    # --------------------------------------------------------
    # Orders for remaining customers
    # --------------------------------------------------------

    for customer_id in range(6, 71):

        orders.append((
            order_id,
            customer_id,
            "2026-07-10",
            "completed",
            250 + customer_id * 10
        ))

        order_id += 1

        orders.append((
            order_id,
            customer_id,
            "2026-08-05",
            "completed",
            300 + customer_id * 8
        ))

        order_id += 1

    cursor.executemany("""
        INSERT INTO orders
        (
            order_id,
            customer_id,
            order_date,
            status,
            total_amount
        )
        VALUES (?, ?, ?, ?, ?)
    """, orders)


# ============================================================
# Order Items
# ============================================================

def insert_order_items(cursor):

    items = []

    order_item_id = 1

    cursor.execute("""
        SELECT
            order_id,
            total_amount
        FROM orders
    """)

    orders = cursor.fetchall()

    for order_id, total_amount in orders:

        # One simple product per order
        if total_amount >= 1000:
            product_id = 1
            quantity = 1

        elif total_amount >= 500:
            product_id = 5
            quantity = 1

        elif total_amount >= 300:
            product_id = 27
            quantity = 1

        else:
            product_id = 13
            quantity = 1

        cursor.execute("""
            SELECT price
            FROM products
            WHERE product_id = ?
        """, (product_id,))

        unit_price = cursor.fetchone()[0]

        items.append((
            order_item_id,
            order_id,
            product_id,
            quantity,
            unit_price
        ))

        order_item_id += 1

    cursor.executemany("""
        INSERT INTO order_items
        (
            order_item_id,
            order_id,
            product_id,
            quantity,
            unit_price
        )
        VALUES (?, ?, ?, ?, ?)
    """, items)


# ============================================================
# Indexes
# ============================================================

def create_indexes(cursor):

    cursor.executescript("""

        CREATE INDEX idx_subscriptions_customer
        ON subscriptions(customer_id);

        CREATE INDEX idx_subscriptions_status
        ON subscriptions(status);

        CREATE INDEX idx_subscriptions_end_date
        ON subscriptions(end_date);

        CREATE INDEX idx_tickets_customer
        ON support_tickets(customer_id);

        CREATE INDEX idx_tickets_created
        ON support_tickets(created_at);

        CREATE INDEX idx_payments_customer
        ON payments(customer_id);

        CREATE INDEX idx_payments_date
        ON payments(payment_date);

        CREATE INDEX idx_orders_customer
        ON orders(customer_id);

        CREATE INDEX idx_orders_date
        ON orders(order_date);

        CREATE INDEX idx_order_items_order
        ON order_items(order_id);

        CREATE INDEX idx_order_items_product
        ON order_items(product_id);

        CREATE INDEX idx_products_category
        ON products(category_id);

    """)


# ============================================================
# Verify Database
# ============================================================

def verify_database(cursor):

    print("\n" + "=" * 60)
    print("DATABASE STATISTICS")
    print("=" * 60)

    tables = [
        "customers",
        "categories",
        "products",
        "subscriptions",
        "support_tickets",
        "payments",
        "orders",
        "order_items"
    ]

    for table in tables:

        cursor.execute(
            f"SELECT COUNT(*) FROM {table}"
        )

        count = cursor.fetchone()[0]

        print(
            f"{table:20} {count:,} rows"
        )

    # ========================================================
    # Verify July churn demo
    # ========================================================

    print("\n" + "=" * 60)
    print("JULY CHURN DEMO")
    print("=" * 60)

    cursor.execute("""
        SELECT
            c.name,
            s.status,
            s.end_date,
            COUNT(st.ticket_id) AS ticket_count

        FROM customers c

        JOIN subscriptions s
            ON c.customer_id = s.customer_id

        LEFT JOIN support_tickets st
            ON c.customer_id = st.customer_id

        WHERE s.status = 'cancelled'
          AND s.end_date >= '2026-07-01'
          AND s.end_date < '2026-08-01'

        GROUP BY
            c.customer_id,
            c.name,
            s.status,
            s.end_date

        ORDER BY
            s.end_date
    """)

    rows = cursor.fetchall()

    for row in rows:
        print(row)


# ============================================================
# Main
# ============================================================

def main():

    print("Creating SQL Agent demo database...")

    conn = create_database()

    cursor = conn.cursor()

    print("Adding categories...")
    insert_categories(cursor)

    print("Adding products...")
    insert_products(cursor)

    print("Adding customers...")
    insert_customers(cursor)

    print("Adding subscriptions...")
    insert_subscriptions(cursor)

    print("Adding support tickets...")
    insert_support_tickets(cursor)

    print("Adding payments...")
    insert_payments(cursor)

    print("Adding orders...")
    insert_orders(cursor)

    print("Adding order items...")
    insert_order_items(cursor)

    print("Creating indexes...")
    create_indexes(cursor)

    conn.commit()

    verify_database(cursor)

    conn.close()

    print("\n" + "=" * 60)
    print("DATABASE READY")
    print("=" * 60)

    print(f"Location: {DB_FILE}")


if __name__ == "__main__":
    main()


# import random
# import sqlite3
# from datetime import date, timedelta


# DB_FILE = "data/customer_analytics.db"

# random.seed(42)


# # ============================================================
# # Configuration
# # ============================================================

# NUM_CUSTOMERS = 10_000
# NUM_SUBSCRIPTIONS = 15_000
# NUM_TICKETS = 50_000
# NUM_PAYMENTS = 30_000
# NUM_ORDERS = 50_000
# NUM_ORDER_ITEMS = 120_000


# # ============================================================
# # Helper functions
# # ============================================================

# def random_date(start_date, end_date):

#     delta = end_date - start_date

#     return start_date + timedelta(
#         days=random.randint(0, delta.days)
#     )


# def random_email(name, customer_id):

#     username = name.lower().replace(" ", ".")

#     return f"{username}{customer_id}@example.com"


# # ============================================================
# # Create database
# # ============================================================

# def create_database():

#     conn = sqlite3.connect(DB_FILE)

#     cursor = conn.cursor()

#     # Improve SQLite insertion performance
#     cursor.execute("PRAGMA journal_mode = WAL")
#     cursor.execute("PRAGMA synchronous = NORMAL")

#     # Drop existing tables
#     cursor.executescript("""
#         DROP TABLE IF EXISTS order_items;
#         DROP TABLE IF EXISTS orders;
#         DROP TABLE IF EXISTS payments;
#         DROP TABLE IF EXISTS support_tickets;
#         DROP TABLE IF EXISTS subscriptions;
#         DROP TABLE IF EXISTS products;
#         DROP TABLE IF EXISTS categories;
#         DROP TABLE IF EXISTS customers;
#     """)

#     # ========================================================
#     # Customers
#     # ========================================================

#     cursor.execute("""
#         CREATE TABLE customers (
#             customer_id INTEGER PRIMARY KEY,
#             name TEXT NOT NULL,
#             email TEXT NOT NULL,
#             signup_date DATE NOT NULL,
#             country TEXT NOT NULL
#         )
#     """)

#     # ========================================================
#     # Categories
#     # ========================================================

#     cursor.execute("""
#         CREATE TABLE categories (
#             category_id INTEGER PRIMARY KEY,
#             category_name TEXT NOT NULL
#         )
#     """)

#     # ========================================================
#     # Products
#     # ========================================================

#     cursor.execute("""
#         CREATE TABLE products (
#             product_id INTEGER PRIMARY KEY,
#             product_name TEXT NOT NULL,
#             category_id INTEGER NOT NULL,
#             price REAL NOT NULL,
#             FOREIGN KEY (category_id)
#                 REFERENCES categories(category_id)
#         )
#     """)

#     # ========================================================
#     # Subscriptions
#     # ========================================================

#     cursor.execute("""
#         CREATE TABLE subscriptions (
#             subscription_id INTEGER PRIMARY KEY,
#             customer_id INTEGER NOT NULL,
#             plan TEXT NOT NULL,
#             start_date DATE NOT NULL,
#             end_date DATE,
#             status TEXT NOT NULL,
#             FOREIGN KEY (customer_id)
#                 REFERENCES customers(customer_id)
#         )
#     """)

#     # ========================================================
#     # Support Tickets
#     # ========================================================

#     cursor.execute("""
#         CREATE TABLE support_tickets (
#             ticket_id INTEGER PRIMARY KEY,
#             customer_id INTEGER NOT NULL,
#             created_at DATE NOT NULL,
#             status TEXT NOT NULL,
#             priority TEXT NOT NULL,
#             FOREIGN KEY (customer_id)
#                 REFERENCES customers(customer_id)
#         )
#     """)

#     # ========================================================
#     # Payments
#     # ========================================================

#     cursor.execute("""
#         CREATE TABLE payments (
#             payment_id INTEGER PRIMARY KEY,
#             customer_id INTEGER NOT NULL,
#             payment_date DATE NOT NULL,
#             amount REAL NOT NULL,
#             status TEXT NOT NULL,
#             FOREIGN KEY (customer_id)
#                 REFERENCES customers(customer_id)
#         )
#     """)

#     # ========================================================
#     # Orders
#     # ========================================================

#     cursor.execute("""
#         CREATE TABLE orders (
#             order_id INTEGER PRIMARY KEY,
#             customer_id INTEGER NOT NULL,
#             order_date DATE NOT NULL,
#             status TEXT NOT NULL,
#             total_amount REAL NOT NULL,
#             FOREIGN KEY (customer_id)
#                 REFERENCES customers(customer_id)
#         )
#     """)

#     # ========================================================
#     # Order Items
#     # ========================================================

#     cursor.execute("""
#         CREATE TABLE order_items (
#             order_item_id INTEGER PRIMARY KEY,
#             order_id INTEGER NOT NULL,
#             product_id INTEGER NOT NULL,
#             quantity INTEGER NOT NULL,
#             unit_price REAL NOT NULL,
#             FOREIGN KEY (order_id)
#                 REFERENCES orders(order_id),
#             FOREIGN KEY (product_id)
#                 REFERENCES products(product_id)
#         )
#     """)

#     conn.commit()

#     return conn


# # ============================================================
# # Generate Categories
# # ============================================================

# def generate_categories(cursor):

#     categories = [
#         (1, "Electronics"),
#         (2, "Home & Kitchen"),
#         (3, "Sports"),
#         (4, "Books"),
#         (5, "Fashion"),
#         (6, "Beauty"),
#         (7, "Toys"),
#         (8, "Office")
#     ]

#     cursor.executemany("""
#         INSERT INTO categories (
#             category_id,
#             category_name
#         )
#         VALUES (?, ?)
#     """, categories)


# # ============================================================
# # Generate Products
# # ============================================================

# def generate_products(cursor):

#     products = []

#     product_names = [
#         "Laptop",
#         "Smartphone",
#         "Tablet",
#         "Monitor",
#         "Keyboard",
#         "Mouse",
#         "Headphones",
#         "Smart Watch",
#         "Coffee Maker",
#         "Air Fryer",
#         "Blender",
#         "Running Shoes",
#         "Yoga Mat",
#         "Dumbbells",
#         "Football",
#         "Basketball",
#         "Programming Book",
#         "Data Science Book",
#         "T-Shirt",
#         "Jeans",
#         "Jacket",
#         "Face Wash",
#         "Shampoo",
#         "Toy Car",
#         "Board Game",
#         "Office Chair",
#         "Desk Lamp"
#     ]

#     for product_id in range(1, 101):

#         category_id = random.randint(1, 8)

#         product_name = (
#             f"{random.choice(product_names)} "
#             f"Model {product_id}"
#         )

#         price = round(
#             random.uniform(500, 100000),
#             2
#         )

#         products.append(
#             (
#                 product_id,
#                 product_name,
#                 category_id,
#                 price
#             )
#         )

#     cursor.executemany("""
#         INSERT INTO products (
#             product_id,
#             product_name,
#             category_id,
#             price
#         )
#         VALUES (?, ?, ?, ?)
#     """, products)

#     return {
#         product[0]: product[3]
#         for product in products
#     }


# # ============================================================
# # Generate Customers
# # ============================================================

# def generate_customers(cursor):

#     first_names = [
#         "John",
#         "Sarah",
#         "Michael",
#         "David",
#         "Emma",
#         "Olivia",
#         "James",
#         "Robert",
#         "Daniel",
#         "Sophia",
#         "William",
#         "Emily",
#         "Matthew",
#         "Ava",
#         "Andrew",
#         "Mia"
#     ]

#     last_names = [
#         "Smith",
#         "Johnson",
#         "Brown",
#         "Williams",
#         "Jones",
#         "Miller",
#         "Davis",
#         "Wilson",
#         "Taylor",
#         "Anderson",
#         "Thomas",
#         "Moore"
#     ]

#     countries = [
#         "USA",
#         "Canada",
#         "UK",
#         "Germany",
#         "Australia",
#         "India",
#         "Singapore"
#     ]

#     customers = []

#     start_date = date(2023, 1, 1)
#     end_date = date(2026, 8, 1)

#     for customer_id in range(1, NUM_CUSTOMERS + 1):

#         name = (
#             f"{random.choice(first_names)} "
#             f"{random.choice(last_names)}"
#         )

#         signup_date = random_date(
#             start_date,
#             end_date
#         )

#         country = random.choice(countries)

#         customers.append(
#             (
#                 customer_id,
#                 name,
#                 random_email(name, customer_id),
#                 signup_date.isoformat(),
#                 country
#             )
#         )

#     cursor.executemany("""
#         INSERT INTO customers (
#             customer_id,
#             name,
#             email,
#             signup_date,
#             country
#         )
#         VALUES (?, ?, ?, ?, ?)
#     """, customers)


# # ============================================================
# # Generate Subscriptions
# # ============================================================

# def generate_subscriptions(cursor):

#     plans = [
#         "Basic",
#         "Pro",
#         "Enterprise"
#     ]

#     subscriptions = []

#     start_date = date(2024, 1, 1)
#     today = date(2026, 8, 28)

#     for subscription_id in range(
#         1,
#         NUM_SUBSCRIPTIONS + 1
#     ):

#         customer_id = random.randint(
#             1,
#             NUM_CUSTOMERS
#         )

#         plan = random.choice(plans)

#         subscription_start = random_date(
#             start_date,
#             today - timedelta(days=30)
#         )

#         # Create some churned customers
#         if random.random() < 0.25:

#             end_date = random_date(
#                 subscription_start + timedelta(days=30),
#                 today
#             )

#             status = "cancelled"

#         else:

#             end_date = None
#             status = "active"

#         subscriptions.append(
#             (
#                 subscription_id,
#                 customer_id,
#                 plan,
#                 subscription_start.isoformat(),
#                 end_date.isoformat()
#                 if end_date else None,
#                 status
#             )
#         )

#     cursor.executemany("""
#         INSERT INTO subscriptions (
#             subscription_id,
#             customer_id,
#             plan,
#             start_date,
#             end_date,
#             status
#         )
#         VALUES (?, ?, ?, ?, ?, ?)
#     """, subscriptions)


# # ============================================================
# # Generate Support Tickets
# # ============================================================

# def generate_support_tickets(cursor):

#     statuses = [
#         "open",
#         "closed",
#         "pending"
#     ]

#     priorities = [
#         "low",
#         "medium",
#         "high",
#         "critical"
#     ]

#     tickets = []

#     start_date = date(2024, 1, 1)
#     end_date = date(2026, 8, 28)

#     for ticket_id in range(
#         1,
#         NUM_TICKETS + 1
#     ):

#         customer_id = random.randint(
#             1,
#             NUM_CUSTOMERS
#         )

#         created_at = random_date(
#             start_date,
#             end_date
#         )

#         tickets.append(
#             (
#                 ticket_id,
#                 customer_id,
#                 created_at.isoformat(),
#                 random.choice(statuses),
#                 random.choice(priorities)
#             )
#         )

#     cursor.executemany("""
#         INSERT INTO support_tickets (
#             ticket_id,
#             customer_id,
#             created_at,
#             status,
#             priority
#         )
#         VALUES (?, ?, ?, ?, ?)
#     """, tickets)


# # ============================================================
# # Generate Payments
# # ============================================================

# def generate_payments(cursor):

#     statuses = [
#         "completed",
#         "failed",
#         "refunded"
#     ]

#     payments = []

#     start_date = date(2024, 1, 1)
#     end_date = date(2026, 8, 28)

#     for payment_id in range(
#         1,
#         NUM_PAYMENTS + 1
#     ):

#         customer_id = random.randint(
#             1,
#             NUM_CUSTOMERS
#         )

#         payment_date = random_date(
#             start_date,
#             end_date
#         )

#         amount = round(
#             random.uniform(20, 10000),
#             2
#         )

#         payments.append(
#             (
#                 payment_id,
#                 customer_id,
#                 payment_date.isoformat(),
#                 amount,
#                 random.choice(statuses)
#             )
#         )

#     cursor.executemany("""
#         INSERT INTO payments (
#             payment_id,
#             customer_id,
#             payment_date,
#             amount,
#             status
#         )
#         VALUES (?, ?, ?, ?, ?)
#     """, payments)


# # ============================================================
# # Generate Orders
# # ============================================================

# def generate_orders(cursor):

#     statuses = [
#         "completed",
#         "shipped",
#         "processing",
#         "cancelled"
#     ]

#     orders = []

#     start_date = date(2024, 1, 1)
#     end_date = date(2026, 8, 28)

#     for order_id in range(
#         1,
#         NUM_ORDERS + 1
#     ):

#         customer_id = random.randint(
#             1,
#             NUM_CUSTOMERS
#         )

#         order_date = random_date(
#             start_date,
#             end_date
#         )

#         total_amount = round(
#             random.uniform(500, 50000),
#             2
#         )

#         orders.append(
#             (
#                 order_id,
#                 customer_id,
#                 order_date.isoformat(),
#                 random.choice(statuses),
#                 total_amount
#             )
#         )

#     cursor.executemany("""
#         INSERT INTO orders (
#             order_id,
#             customer_id,
#             order_date,
#             status,
#             total_amount
#         )
#         VALUES (?, ?, ?, ?, ?)
#     """, orders)


# # ============================================================
# # Generate Order Items
# # ============================================================

# def generate_order_items(cursor, product_prices):

#     items = []

#     for order_item_id in range(
#         1,
#         NUM_ORDER_ITEMS + 1
#     ):

#         order_id = random.randint(
#             1,
#             NUM_ORDERS
#         )

#         product_id = random.randint(
#             1,
#             100
#         )

#         quantity = random.randint(
#             1,
#             5
#         )

#         unit_price = product_prices[
#             product_id
#         ]

#         items.append(
#             (
#                 order_item_id,
#                 order_id,
#                 product_id,
#                 quantity,
#                 unit_price
#             )
#         )

#         # Insert in batches
#         if len(items) >= 5000:

#             cursor.executemany("""
#                 INSERT INTO order_items (
#                     order_item_id,
#                     order_id,
#                     product_id,
#                     quantity,
#                     unit_price
#                 )
#                 VALUES (?, ?, ?, ?, ?)
#             """, items)

#             items.clear()

#     if items:

#         cursor.executemany("""
#             INSERT INTO order_items (
#                 order_item_id,
#                 order_id,
#                 product_id,
#                 quantity,
#                 unit_price
#             )
#             VALUES (?, ?, ?, ?, ?)
#         """, items)


# # ============================================================
# # Create indexes
# # ============================================================

# def create_indexes(cursor):

#     cursor.executescript("""

#         CREATE INDEX idx_subscriptions_customer
#         ON subscriptions(customer_id);

#         CREATE INDEX idx_subscriptions_status
#         ON subscriptions(status);

#         CREATE INDEX idx_subscriptions_end_date
#         ON subscriptions(end_date);

#         CREATE INDEX idx_tickets_customer
#         ON support_tickets(customer_id);

#         CREATE INDEX idx_tickets_created
#         ON support_tickets(created_at);

#         CREATE INDEX idx_payments_customer
#         ON payments(customer_id);

#         CREATE INDEX idx_orders_customer
#         ON orders(customer_id);

#         CREATE INDEX idx_orders_date
#         ON orders(order_date);

#         CREATE INDEX idx_order_items_order
#         ON order_items(order_id);

#         CREATE INDEX idx_order_items_product
#         ON order_items(product_id);

#         CREATE INDEX idx_products_category
#         ON products(category_id);

#     """)


# # ============================================================
# # Main
# # ============================================================

# def main():

#     print("Creating database...")

#     conn = create_database()

#     cursor = conn.cursor()

#     print("Generating categories...")
#     generate_categories(cursor)

#     print("Generating products...")
#     product_prices = generate_products(cursor)

#     print("Generating customers...")
#     generate_customers(cursor)

#     print("Generating subscriptions...")
#     generate_subscriptions(cursor)

#     print("Generating support tickets...")
#     generate_support_tickets(cursor)

#     print("Generating payments...")
#     generate_payments(cursor)

#     print("Generating orders...")
#     generate_orders(cursor)

#     print("Generating order items...")
#     generate_order_items(
#         cursor,
#         product_prices
#     )

#     print("Creating indexes...")
#     create_indexes(cursor)

#     conn.commit()

#     # Show row counts
#     print("\nDatabase statistics:")

#     tables = [
#         "customers",
#         "categories",
#         "products",
#         "subscriptions",
#         "support_tickets",
#         "payments",
#         "orders",
#         "order_items"
#     ]

#     for table in tables:

#         cursor.execute(
#             f"SELECT COUNT(*) FROM {table}"
#         )

#         count = cursor.fetchone()[0]

#         print(
#             f"{table:20} {count:,} rows"
#         )

#     conn.close()

#     print(
#         f"\nDatabase created: {DB_FILE}"
#     )


# if __name__ == "__main__":
#     main()