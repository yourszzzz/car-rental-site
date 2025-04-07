from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# View available cars
@app.route('/cars')
def cars():
    conn = sqlite3.connect('rental.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM cars WHERE available = 1")
    car_data = cur.fetchall()
    conn.close()
    return render_template('cars.html', cars=car_data)

# Book a car
@app.route('/book', methods=['GET', 'POST'])
def book():
    conn = sqlite3.connect('rental.db')
    cur = conn.cursor()

    if request.method == 'POST':
        car_id = request.form['car_id']
        name = request.form['name']
        start = request.form['start_date']
        end = request.form['end_date']

        cur.execute("INSERT INTO bookings (car_id, customer_name, start_date, end_date) VALUES (?, ?, ?, ?)",
                    (car_id, name, start, end))
        cur.execute("UPDATE cars SET available = 0 WHERE id = ?", (car_id,))
        conn.commit()
        conn.close()
        return render_template('booked.html', name=name)

    cur.execute("SELECT id, name FROM cars WHERE available = 1")
    car_options = cur.fetchall()
    conn.close()
    return render_template('book.html', cars=car_options)

# View bookings
@app.route('/bookings')
def view_bookings():
    conn = sqlite3.connect('rental.db')
    cur = conn.cursor()
    cur.execute('''
        SELECT bookings.id, cars.name, customer_name, start_date, end_date 
        FROM bookings 
        JOIN cars ON bookings.car_id = cars.id
    ''')
    bookings = cur.fetchall()
    conn.close()
    return render_template('bookings.html', bookings=bookings)

# Delete a booking
@app.route('/delete_booking/<int:booking_id>', methods=['POST'])
def delete_booking(booking_id):
    conn = sqlite3.connect('rental.db')
    cur = conn.cursor()
    cur.execute("SELECT car_id FROM bookings WHERE id = ?", (booking_id,))
    result = cur.fetchone()
    if result:
        car_id = result[0]
        cur.execute("DELETE FROM bookings WHERE id = ?", (booking_id,))
        cur.execute("UPDATE cars SET available = 1 WHERE id = ?", (car_id,))
        conn.commit()
    conn.close()
    return redirect('/bookings')

if __name__ == '__main__':
    app.run(debug=True)
