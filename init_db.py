import sqlite3

# Connect to SQLite DB (this will create the file if it doesn't exist)
conn = sqlite3.connect('rental.db')
cur = conn.cursor()

# Create 'cars' table
cur.execute('''
    CREATE TABLE IF NOT EXISTS cars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        price INTEGER,
        image TEXT,
        available INTEGER DEFAULT 1
    )
''')

# Create 'bookings' table
cur.execute('''
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        car_id INTEGER,
        customer_name TEXT,
        start_date TEXT,
        end_date TEXT,
        FOREIGN KEY(car_id) REFERENCES cars(id)
    )
''')

# Insert some sample cars (only if table is empty)
cur.execute("SELECT COUNT(*) FROM cars")
if cur.fetchone()[0] == 0:
    cars = [
        ('Hyundai i10', 'Compact city car, great for mileage.', 1500, 'i10.jpg', 1),
        ('Toyota Innova', 'Spacious family SUV.', 2500, 'innova.jpg', 1),
        ('Honda City', 'Premium sedan with comfort.', 2000, 'city.jpg', 1),
    ]
    cur.executemany("INSERT INTO cars (name, description, price, image, available) VALUES (?, ?, ?, ?, ?)", cars)
    print("Inserted default car data.")

conn.commit()
conn.close()
print("Database initialized successfully.")
