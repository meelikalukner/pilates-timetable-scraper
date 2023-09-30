from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Define the URL of the page to scrape
url = "https://www.maripilates.ee/broneerimine"
driver = webdriver.Chrome()  # Only use this if defined in PATH
driver.get(url)

# Define a set to store previously found appointments
previous_appointments = set()

def get_appointments():
    # Parse the page data directly from the Selenium driver
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Find the appointments on the page
    appointments = soup.find_all("div", class_="babel-ignore")
    
    return set(appointments)

def click_more_times_and_get_appointments():
    all_appointments = set()
    
    while True:
        try:
            # Wait for the "more times" span to be clickable
            more_times_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'class-list-next'))
            )
            more_times_btn.click()

            # Wait for the page to load new data after clicking (adjust if needed)
            time.sleep(5)

            # Parse the additional data
            more_appointments = get_appointments()
            
            # Combine with previously fetched appointments
            all_appointments = all_appointments.union(more_appointments)
        except:
            # If "more times" span is not found, exit the loop
            break

    return all_appointments

def check_for_new_appointments():
    global previous_appointments
    
    # Get the current appointments from the first page
    current_appointments = get_appointments()

    # Click "more times" button and get more appointments (if any)
    more_appointments = click_more_times_and_get_appointments()

    # Combine both sets of appointments
    combined_appointments = current_appointments.union(more_appointments)
    
    # Check if there are any new appointments
    new_appointments = combined_appointments - previous_appointments

    # If there are new appointments, notify the user
    if new_appointments:
        print("New appointments available:", new_appointments)

    # Update the set of previous appointments
    previous_appointments = combined_appointments

    return new_appointments

# Check for new appointments at regular intervals (e.g., every 30 seconds)
new_appointments = set()
while True:
    check_for_new_appointments()
    print(new_appointments)
    time.sleep(60)




