import time
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select



from flask import Flask
app = Flask(__name__)


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@app.route('/')
def fill_cgat_form(case_type, case_number, case_year):
    # Replace 'path/to/chromedriver' with the actual path to your ChromeDriver executable
    driver = webdriver.Chrome()

    # Open the website
    driver.get('https://cgat.gov.in/#/lucknow/case-status')

    try:
        # Wait for the form elements to load
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, 'caseTypeId')))
        wait.until(EC.presence_of_element_located((By.ID, 'caseNo')))
        wait.until(EC.presence_of_element_located((By.ID, 'caseYear')))
        
        # Fill the form fields
        type_input = driver.find_element(By.ID, 'caseTypeId')
        type_input.send_keys('Original Application')
        time.sleep(2)

        case_no_input = driver.find_element(By.ID, 'caseNo')
        case_no_input.send_keys('100')
        time.sleep(2)

        year_input = driver.find_element(By.ID, 'caseYear')
        year_input.send_keys('2019')
        
        time.sleep(2)
        # Submit the form (assuming there's a submit button, replace with the correct selector if needed)
        submit_button = driver.find_element(By.CLASS_NAME, 'search')
        submit_button.click()

        
        time.sleep(2)
        # Wait for the modal to appear (modify the locator based on the actual modal element)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'modal-body')))
        time.sleep(2)
        # Find the modal table and extract the data
        modal_table = driver.find_element(By.CLASS_NAME, 'table')
        rows = modal_table.find_elements(By.TAG_NAME, 'tr')

        modal_data = {}
        for row in rows:
            # Extract data from each row
            columns = row.find_elements(By.TAG_NAME, 'td')
            if len(columns) == 7:
                applicant_vs_respondent = columns[0].text
                dairy_no = columns[1].text
                location = columns[2].text
                case_type = columns[3].text
                case_no = columns[4].text
                date_of_filing = columns[5].text
                other_details_link = columns[6].find_element(By.TAG_NAME, 'a').get_attribute('href')

                modal_data = {
                    "Title": applicant_vs_respondent,
                    "Dairy No.": dairy_no,
                    "Location": location,
                    "Case Type": case_type,
                    "Case No.": case_no,
                    "Date of Filing": date_of_filing,
                    "Other Details Link": other_details_link
                }
        if modal_data is not None:
            with open('cgat_data.json', 'w') as json_file:
                json.dump(modal_data, json_file)

        print(modal_data)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()


case_type = "Original Application"
case_number = "100"
case_year = "2019"

data = fill_cgat_form(case_type, case_number, case_year)


if __name__ == '__main__':
    app.run(debug=True)