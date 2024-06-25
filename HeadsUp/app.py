# app.py
from flask import Flask, render_template, request, redirect, url_for
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sqlite3

app = Flask(__name__)

# Function to scrape events and store them in SQLite
def scrape_and_store(username, password):
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service)

    driver.get("https://virtualcampus.kcau.ac.ke/")

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Log in")))

    link = driver.find_element(By.PARTIAL_LINK_TEXT, "Log in")
    link.click()

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "username")))

    username_input = driver.find_element(By.ID, "username")
    username_input.clear()
    username_input.send_keys(username)

    password_input = driver.find_element(By.ID, "password")
    password_input.clear()
    password_input.send_keys(password + Keys.ENTER)

    time.sleep(5)  # Adjust sleep time if needed

    calendar_rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr[data-region='month-view-week']")

    events_data = []
    for row in calendar_rows:
        if row.find_elements(By.CSS_SELECTOR, "td[data-title]"):
            day_number = row.find_element(By.CSS_SELECTOR, "td.day").get_attribute("data-day")
            events = row.find_elements(By.CSS_SELECTOR, "li[data-region='event-item']")
            for event in events:
                event_title = event.find_element(By.CSS_SELECTOR, "span.eventname").text
                events_data.append((day_number, event_title))

    driver.quit()

    # Store events in SQLite database
    with sqlite3.connect('events.db') as conn:
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS events (day_number TEXT, event_title TEXT)')
        cursor.executemany('INSERT INTO events VALUES (?, ?)', events_data)
        conn.commit()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        scrape_and_store(username, password)
        return redirect(url_for('display_events'))
    return render_template('index.html')


@app.route('/events')
def display_events():
    with sqlite3.connect('events.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM events')
        events = cursor.fetchall()
    return render_template('events.html', events=events)


if __name__ == '__main__':
    app.run(debug=True)
