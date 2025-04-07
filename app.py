from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Home Page
@app.route('/')
def home():
    return render_template('index.html')

# Show Cars
@app.route('/cars')
def cars():
    conn = sqlite3.connect('cars.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM cars")
    car_list = cur.fetchall()
    conn.close()
    return render_template('cars.html', cars=car_list)

# Booking Page
@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        name = request.form['name']
        car_id = request.form['car_id']
        date = request.form['date']

        conn = sqlite3.connect('cars.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO bookings (name, car_id, date) VALUES (?, ?, ?)", (name, car_id, date))
        conn.commit()
        conn.close()
        
        return render_template('success.html', name=name)

    conn = sqlite3.connect('cars.db')
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM cars WHERE available=1")
    available_cars = cur.fetchall()
    conn.close()
    return render_template('book.html', cars=available_cars)

if __name__ == '__main__':
    app.run(debug=True)
