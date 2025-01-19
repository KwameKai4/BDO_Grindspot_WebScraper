from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options  # Add this line
from bs4 import BeautifulSoup
import csv
import time

# Set up Selenium WebDriver options for Chrome (headless mode)
from webdriver_manager.chrome import ChromeDriverManager

# Configure options for headless mode
chrome_options = Options()
chrome_options.add_argument('--headless')  # Run Chrome in headless mode
chrome_options.add_argument('--disable-gpu')  # Disable GPU usage (optional, but often recommended)
chrome_options.add_argument('--no-sandbox')  # Bypass OS security model, required for some systems
chrome_options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems in containerized environments
chrome_options.add_argument('--log-level=3')  # Suppress logs
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

# Initialize WebDriver with options
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# URL for the grind spots
URL = 'REPLACE WITH YOUR OWN WEBSITE!'

# Open the URL
driver.get(URL)
time.sleep(4)  # Wait for the page to fully load

# Parse the page source with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Close the WebDriver session as we no longer need it
driver.quit()

# Find all rows in the grind spots table
rows = soup.find_all('tr', class_='cursor-pointer')

# Open (and overwrite) the CSV file
with open('grind_spots.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # Write the headers to the CSV file
    writer.writerow(['Name', 'Trash/hr', 'Silver/hour'])

    # Loop through rows and extract the required data
    for row in rows:
        try:
            # Extract the grind spot name
            name_cell = row.find('a', href=True)
            name = name_cell.text.strip() if name_cell else "N/A"

            # Extract Trash/hr
            trash_cell = row.find_all('td', class_='number')[2]  # Adjusting index for Trash/hr
            trash_per_hour = trash_cell.text.strip() if trash_cell else "N/A"

            # Extract Silver/hour
            silver_cell = row.find('td', class_='number pr-4 text-right')
            silver_per_hour = silver_cell.div.text.strip() if silver_cell and silver_cell.div else "N/A"

            # Save the extracted data to the CSV file
            writer.writerow([name, trash_per_hour, silver_per_hour])

            # Print the extracted data for validation
            print(f"Name: {name}")
            print(f"Trash/hr: {trash_per_hour}")
            print(f"Silver/hour: {silver_per_hour}")
            print("-" * 50)

        except Exception as e:
            print(f"An error occurred while processing a row: {e}")
            continue