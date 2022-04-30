from multiprocessing import Value
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

chrome_options = Options()

chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
start_url = "http://192.168.100.1/cgi-bin/status_cgi"
driver.get(start_url)

print("Downstream")
print()
value1 = driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[3]/table[2]").text
print(value1)
print()

print("Upstream")
print()
value2 = driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[3]/table[4]").text
print(value2)
print()

print("Uptime")
print()
value3 = driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[3]/table[6]").text
print((value3.split("\n")[0]).replace(" ", ""))
print()
print()

driver.quit()
