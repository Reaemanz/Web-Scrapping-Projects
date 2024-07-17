from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import csv

# INPUTS START
linkedin_email_id = "enter_linkedin_email_id_here"
linkedin_password = "enter_linkedin_password_here"
search_url = "https://www.linkedin.com/search/results/people/?currentCompany=%5B%221441%22%2C%2216140%22%2C%2217876832%22%2C%2210440912%22%2C%22791962%22%5D&origin=COMPANY_PAGE_CANNED_SEARCH&page=6&sid=2Uo"
excel_file_name = "google.csv"
company_domain_for_email = "@google.com"
number_of_pages = 5
# INPUTS END

# Login 
driver = webdriver.Chrome(webdriver.ChromeOptions())
driver.get("https://linkedin.com/uas/login")
time.sleep(5)
username = driver.find_element(By.ID, "username")
username.send_keys(linkedin_email_id) 
pword = driver.find_element(By.ID, "password")
pword.send_keys(linkedin_password)    
driver.find_element(By.XPATH, "//button[@type='submit']").click()

# Extract names and positions
time.sleep(5)
page_count = 1
csv_rows = []
while page_count <= number_of_pages:
    current_url = search_url + "&page=" + str(page_count)
    driver.get(current_url)  
    time.sleep(10)
    src = driver.page_source
    soup = BeautifulSoup(src, 'html.parser')
    name_divs = soup.findAll('span', attrs={'dir': 'ltr'})
    position_divs = soup.findAll('div', attrs={'class': 'entity-result__primary-subtitle t-14 t-black t-normal'})
    for i in range(len(position_divs)):
        name = name_divs[i].find('span').getText().strip().split()
        first_name = name[0]
        last_name = ""
        for j in range(1, len(name)):
            last_name += name[j]
        email = first_name + "." + last_name + company_domain_for_email
        position = position_divs[i].getText().strip()
        csv_rows.append([first_name, last_name, email, position])
    page_count += 1
   
# Writing to a csv file (openable in Excel)
with open(excel_file_name + '.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        header_row = ["first_name", "last_name", "email", "position"]
        writer.writerow(header_row)
        for data_row in csv_rows:
            writer.writerow(data_row)