from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import pandas as pd
import smtplib
from email.message import EmailMessage
import schedule

departure_flight_inputs = {'Departure': "ORD", 'Arrival': "LAX", 'Date': "May 25, 2025"}
return_flight_inputs = {'Departure': "LAX", 'Arrival': "ORD", 'Date': "Oct 28, 2025"}

def find_cheapest_flights(flight_info):
    PATH = r'/Users/maxm/chromedriver'  # Update this path to your ChromeDriver location
    driver = webdriver.Chrome(executable_path=PATH)

    leaving_from = flight_info['Departure']
    going_to = flight_info['Arrival']
    trip_date = flight_info['Date']

    # Go to Expedia
    driver.get("https://www.expedia.com")

    # Click on Flights tab
    flight_xpath = '//a[@aria-controls="search_form_product_selector_flights"]'
    flight_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, flight_xpath))
    )
    flight_element.click()
    time.sleep(0.5)

    # Click on One-Way
    oneway_xpath = '//button[contains(text(), "One-way")]'
    one_way_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, oneway_xpath))
    )
    one_way_element.click()
    time.sleep(0.5)

    # Fill "Leaving from" field
    leaving_from_xpath = '//button[@aria-label="Leaving from"]'
    leaving_from_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, leaving_from_xpath))
    )
    leaving_from_element.click()
    time.sleep(1)
    leaving_from_element = driver.find_element(By.XPATH, '//input[@id="origin_select"]')
    leaving_from_element.clear()
    leaving_from_element.send_keys(leaving_from)
    time.sleep(1)
    leaving_from_element.send_keys(Keys.DOWN, Keys.RETURN)

    # Fill "Going to" field
    going_to_xpath = '//button[@aria-label="Going to"]'
    going_to_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, going_to_xpath))
    )
    going_to_element.click()
    time.sleep(1)
    going_to_element = driver.find_element(By.XPATH, '//input[@id="destination_select"]')
    going_to_element.clear()
    going_to_element.send_keys(going_to)
    time.sleep(1)
    going_to_element.send_keys(Keys.DOWN, Keys.RETURN)

    # Select departure date
    departing_box_xpath = '//button[contains(@aria-label, "Departing")]'
    depart_box_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, departing_box_xpath))
    )
    depart_box_element.click()
    time.sleep(2)

    trip_date_xpath = f'//button[contains(@aria-label, "{trip_date}")]'
    departing_date_element = ""
    while not departing_date_element:
        try:
            departing_date_element = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, trip_date_xpath))
            )
            departing_date_element.click()
        except TimeoutException:
            next_month_xpath = '//button[@data-stid="date-picker-paging"][2]'
            driver.find_element(By.XPATH, next_month_xpath).click()
            time.sleep(1)

    depart_date_done_xpath = '//button[@data-stid="apply-date-picker"]'
    driver.find_element(By.XPATH, depart_date_done_xpath).click()

    # Click Search
    search_button_xpath = '//button[@data-testid="submit-button"]'
    driver.find_element(By.XPATH, search_button_xpath).click()
    time.sleep(15)  # Wait for results to load

    # Filter for nonstop flights
    nonstop_flight_xpath = '//input[@id="stops-0"]'
    if driver.find_elements(By.XPATH, nonstop_flight_xpath):
        driver.find_element(By.XPATH, nonstop_flight_xpath).click()
        time.sleep(5)

    # Get available flights
    available_flights = driver.find_elements(By.XPATH, '//span[contains(text(), "Select and show fare information")]')
    flights = []
    if available_flights:
        for item in available_flights[:5]:
            text = item.text.split(",")
            flights.append((
                text[0].split("for")[-1].title(),
                text[1].title().replace("At", ":"),
                text[2].title().replace("At", ":"),
                text[3].title().replace("At", ":")
            ))
    else:
        # Sort by price if no nonstop flights
        driver.find_element(By.XPATH, '//option[@data-opt-id="PRICE_INCREASING"]').click()
        time.sleep(5)
        available_flights = driver.find_elements(By.XPATH, '//span[contains(text(), "Select and show fare information")]')
        flights = [(item.text.split(",")[0].split("for")[-1].title(),
                    item.text.split(",")[1].title().replace("At", ":"),
                    item.text.split(",")[2].title().replace("At", ":"),
                    item.text.split(",")[3].title().replace("At", ":"))
                   for item in available_flights[:5]]

    if flights:
        print(f"Conditions satisfied for: Departure: {leaving_from}, Arrival: {going_to}, Date: {trip_date}")
    else:
        print(f"Not all conditions could be met for: Departure: {leaving_from}, Arrival: {going_to}, Date: {trip_date}")

    driver.quit()
    return flights

def send_email():
    departing_flights = find_cheapest_flights(departure_flight_inputs)
    return_flights = find_cheapest_flights(return_flight_inputs)
    df = pd.DataFrame(departing_flights + return_flights, columns=["Price", "Departure Time", "Arrival Time", "Duration"])

    if not df.empty:
        email = "wesker849@gmail.com"  # Replace with your email
        password = "Thenorth849"      # Replace with your password or app-specific password

        msg = EmailMessage()
        msg['Subject'] = f"Python Flight Info! {departure_flight_inputs['Departure']} --> {departure_flight_inputs['Arrival']}, Departing: {departure_flight_inputs['Date']}, Returning: {return_flight_inputs['Date']}"
        msg['From'] = email
        msg['To'] = email
        msg.add_alternative(f'''\
            <!DOCTYPE html>
            <html>
                <body>
                    {df.to_html()}
                </body>
            </html>''', subtype="html")

        with smtplib.SMTP_SSL('wesker849@gmail.com', 465) as smtp:
            smtp.login(email, password)
            smtp.send_message(msg)

schedule.every(30).minutes.do(send_email)

while True:
    schedule.run_pending()
    time.sleep(1)