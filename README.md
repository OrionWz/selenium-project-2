# selenium-project-2
Developed a Python-based web scraping and automation tool to monitor and extract flight prices from Expedia, enabling real-time tracking of cost-effective travel options.
Flight Price Scraper and Email Notifier

Overview

This Python script automates the process of scraping flight prices from Expedia for specified departure and return flights, filters for nonstop or cheapest options, and sends the results via email. It uses Selenium for web scraping, Pandas for data processing, and smtplib for email notifications. The script runs on a schedule to periodically check flight prices.

Features





Scrapes one-way flight prices from Expedia for given departure, arrival, and date inputs.



Filters for nonstop flights when available; otherwise, sorts by price.



Compiles flight details (price, departure time, arrival time, duration) into a Pandas DataFrame.



Sends an HTML-formatted email with flight details every 30 minutes.



Supports both departure and return flight searches.

Prerequisites





Python 3.7+



Chrome browser



ChromeDriver compatible with your Chrome version



Required Python packages:





selenium



pandas



schedule



smtplib (included in Python standard library)



email (included in Python standard library)

Installation





Install Python: Ensure Python 3.7 or higher is installed. Download from python.org.



Install ChromeDriver:





Download ChromeDriver from chromedriver.chromium.org matching your Chrome browser version.



Place the chromedriver executable in a known directory (e.g., /Users/maxm/chromedriver).



Update the PATH variable in the script to point to your ChromeDriver location.



Install Python Packages:

pip install selenium pandas schedule



Configure Email:





Replace email and password in the send_email function with your email address and password (or app-specific password for Gmail).



For Gmail, enable "Less secure app access" or generate an app-specific password if 2FA is enabled.

Usage





Configure Flight Inputs:





Modify the departure_flight_inputs and return_flight_inputs dictionaries with your desired flight details:

departure_flight_inputs = {'Departure': "ORD", 'Arrival': "LAX", 'Date': "May 25, 2025"}
return_flight_inputs = {'Departure': "LAX", 'Arrival': "ORD", 'Date': "Oct 28, 2025"}



Run the Script:

python flight_scraper.py

The script will:





Scrape flight data from Expedia for both departure and return flights.



Send an email with flight details every 30 minutes.



Continue running until manually stopped (Ctrl+C).



Email Output:





You will receive an email with a table containing flight details (price, departure time, arrival time, duration) for the top 5 flights per leg.

Script Details





File: flight_scraper.py



Main Functions:





find_cheapest_flights(flight_info): Scrapes Expedia for flight data based on provided inputs, filters for nonstop or cheapest flights, and returns a list of flight details.



send_email(): Calls find_cheapest_flights for both departure and return flights, compiles results into a DataFrame, and sends an HTML email.



Scheduling: Uses the schedule library to run send_email every 30 minutes.



Dependencies:





Selenium interacts with Expedia’s website.



Pandas formats flight data into a table.



smtplib and email handle email sending.

Notes





ChromeDriver Path: Ensure the PATH variable in the script points to your ChromeDriver executable.



Expedia Website: The script relies on Expedia’s HTML structure. Changes to the website may break the script.



Email Security: Use an app-specific password for Gmail to avoid security issues.



Timeout Handling: The script uses WebDriverWait to handle dynamic page loading but may require adjustments for slower connections.



Rate Limits: Be cautious of Expedia’s scraping policies to avoid IP bans.

Troubleshooting





ChromeDriver Error: Ensure ChromeDriver matches your Chrome version and the path is correct.



TimeoutException: Increase WebDriverWait timeouts or check your internet connection.



Email Not Sending: Verify email credentials and SMTP settings. Check spam/junk folders.



No Flights Found: Confirm the date format (Month Day, Year) and airport codes are valid.

License

This project is unlicensed and provided as-is for personal use. Use responsibly and respect Expedia’s terms of service.
