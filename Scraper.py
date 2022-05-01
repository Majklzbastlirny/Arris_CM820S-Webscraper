from multiprocessing import Value
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import datetime, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
URL = "http://192.168.100.1/cgi-bin/status_cgi"
driver.get(URL)

token = "GIcSmvKUhmOct6cKQ-gGOF7xYDtUPAy4-67OJxwMOcolDf9j92VjF41QDotJ37yUXU9kkAQp-x9P0aqT7XrsGA=="
org = "MajklovaBastlirna"
bucket = "Arris_Modem"

#with InfluxDBClient(url="http://192.168.0.8:8086", token=token, org=org) as client:




print("Downstream")
print()
value1 = driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[3]/table[2]").text
Downstream = value1.splitlines()
for x in range(1, len(Downstream)) :
    print(Downstream[x])
print()


print("Upstream")
print()
value2 = driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[3]/table[4]").text
Upstream = value2.splitlines()
for x in range(1, len(Upstream)):
    print(Upstream[x])
   
print()

print("Uptime")
print()
value3 = driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[3]/table[6]").text
Uptime = (((value3.split("\n")[0]).replace(" ", "")).replace("SystemUptime:", "").replace("m", "").replace("h", "").replace("d", "")).split(":")
Uptimes = (int(Uptime[0])*86400) + (int(Uptime[1])*3600) + (int(Uptime[2])*60)
print(Uptimes)
Uptime2 = datetime.timedelta(seconds=Uptimes)
print(Uptime2)
print()


print("Error")
print()
#///html/body/div[1]/div[3]/text()
value4 = driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[3]").text
start = value4.find("Downstream\n") + len("Downstream\n")
end = value4.find("DCID")
error = value4[start:end]
print(error)

print()

driver.quit()

