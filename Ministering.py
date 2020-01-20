from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import csv
import sys

def wait_for_page_load(driver, timeout=30):
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[2]/ul/div[1]/div[5]/div[1]")))

def login( driver, username, password):
    elem = driver.find_element_by_id("username")
    elem.clear()
    elem.send_keys(username)
    elem = driver.find_element_by_id("password")
    elem.clear()
    elem.send_keys(password)
    elem.send_keys(Keys.RETURN)
    return;

# Check parameters
if len(sys.argv) < 3:
    print("Not enough program arguments. Run as: python .\Ministering.py <LDS username> <LDS password>")
    exit()

# Load up ministering page
driver = webdriver.Firefox(executable_path='geckodriver-v0.26.0-win64/geckodriver.exe')
driver.get("https://lcr.churchofjesuschrist.org/ministering?lang=eng&type=EQ")

# Log in if necessary
if "https://login." in driver.current_url:
    # old_page = driver.find_element_by_tag_name('html')
    login(driver, sys.argv[1], sys.argv[2])
    wait_for_page_load(driver)

with open('ministering.csv', 'w') as csvfile:
    csv_file = csv.writer(csvfile, delimiter=',',
               quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator = '\n')
    # For each district
    div_base = 4
    district = 1
    while "District " + str(district) in driver.page_source:
        print("District " + str(district))
        district_name = "District " + str(district)
        csv_file.writerow([district_name])
        # Get the presidency member assigned to this district
        try:
            presidency_member_element = driver.find_element_by_xpath(
                "/html/body/div[3]/div[2]/ul/div[1]/div["+str(div_base+district)+"]/div[2]/span/a")
            presidency_member = presidency_member_element.get_attribute("text")
            presidency_member = presidency_member[1:]
        except:
            presidency_member = "Unassigned"
        print(presidency_member)
        csv_file.writerow(["Presidency Member:", presidency_member])

        # For each companionship
        companionship = 1
        while True:
            try:
                first_companion_elem = driver.find_element_by_xpath(
                    "/html/body/div[3]/div[2]/ul/div[1]/div["+str(div_base+district)
                    +"]/table/tbody/tr["+str(companionship)+"]/td[2]/a[1]"
                )
                first_companion = first_companion_elem.get_attribute("text")[1:]
            except: # No more companionships for this district
                break
            try:
                second_companion_elem = driver.find_element_by_xpath(
                    "/html/body/div[3]/div[2]/ul/div[1]/div["+str(div_base+district)
                    +"]/table/tbody/tr["+str(companionship)+"]/td[2]/a[2]"
                )
                second_companion = second_companion_elem.get_attribute("text")[1:]
            except: # No second companion
                second_companion = ""
            print("  " + first_companion + " and " + second_companion)
            csv_file.writerow([first_companion, second_companion])
            companionship += 1

        csv_file.writerow([""])
        district += 1

driver.close()