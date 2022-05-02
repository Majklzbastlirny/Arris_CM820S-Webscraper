#Arris modem scraper
#Author: @Majklzbastlirny
#Date: 2nd of May 2022
#Version: 1.0


from multiprocessing import Value
from rx import catch
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import datetime, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from ping3 import ping
import sys
from random import uniform
from time import sleep
from selenium.common.exceptions import TimeoutException



token = "GIcSmvKUhmOct6cKQ-gGOF7xYDtUPAy4-67OJxwMOcolDf9j92VjF41QDotJ37yUXU9kkAQp-x9P0aqT7XrsGA=="
org = "MajklovaBastlirna"
bucket = "Arris_Modem"

Download = 0
timeout = 6.0


client =  InfluxDBClient(url="http://192.168.0.8:8086", token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

ping_result = ping("192.168.100.1", timeout=1, unit='ms')
if ping_result == None:
    print("Cannot ping modem")
    write_api.write(bucket,org,Point("Status").field("Status", "Cannot ping modem").tag("Modem", "Arris_Modem").tag("Time", datetime.datetime.now()))
    client.close()
    sys.exit()

else:
    print("Modem is up, ping is","%.4f" % ping_result, "ms")
    write_api.write(bucket,org,Point("Status").field("Status", "Modem is up, ping is " + "%.4f" % ping_result + " ms").tag("Modem", "Arris_Modem").tag("Time", datetime.datetime.now()))



chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(options=chrome_options)
#driver = webdriver.Chrome(options=chrome_options, executable_path='/root/Arris_CM820S-Webscraper/chromedriver')
driver.set_page_load_timeout(timeout)
URL = "http://192.168.100.1/cgi-bin/status_cgi"
print("Scraping started")

try:
    driver.get(URL)   
except TimeoutException as e:
    print("TimeoutException")
    write_api.write(bucket,org,Point("Status").field("Status", "TimeoutException").tag("Modem", "Arris_Modem").tag("Time", datetime.datetime.now()))
    driver.quit()
    client.close()
    sys.exit()

time.sleep(0.1)
value1 = driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[3]/table[2]").text
time.sleep(0.1)
value2 = driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[3]/table[4]").text
time.sleep(0.1)
value3 = driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[3]/table[6]").text
time.sleep(0.1)
value4 = driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[3]").text
driver.quit()
print("Scraping finished")
print()

print("Downstream")
print()
value1 = value1.replace("----", " 0 0 ")
Downstream = value1.splitlines()
for x in range(1, len(Downstream)) :
    data = Downstream[x].split()
    Datapoint = str(data[0]) + " " + str(data[1])
    Download = Download + int(data[10])
    print(data)
    print(Datapoint)
    write_api.write(bucket,org,Point(Datapoint).field("DCID", int(data[2])).field("Frequency", float(data[3])).field("Power", float(data[5])).field("SNR", float(data[7])).field("Modulation", data[9]).field("Octets", float(data[10])).field("Correcteds", float(data[11])).field("Uncorrectables", float(data[12])))


print()
print("Downloaded: " + str(Download) + " Bytes" + " = " + str(Download/1000000) + " MB" + " = " + str(Download/1000000000) + " GB")
write_api.write(bucket,org,Point("Downloaded").field("Downloaded", Download))
print()
time.sleep(0.1)

print("Upstream")
print()
value2 = value2.replace("----", " 0 0 ")
Upstream = value2.splitlines()
for x in range(1, len(Upstream)):
    data = Upstream[x].split()
    Datapoint = str(data[0]) + " " + str(data[1])
    print(data)
    write_api.write(bucket,org,Point(Datapoint).field("UCID", int(data[2])).field("Frequency", float(data[3])).field("Power", float(data[5])).field("Channel type", (data[7] + "" + data[8])).field("Symbol rate", data[9]).field("Modulation", data[11]))

print()

time.sleep(0.1)

print("Uptime")
print()
Uptime = (((value3.split("\n")[0]).replace(" ", "")).replace("SystemUptime:", "").replace("m", "").replace("h", "").replace("d", "")).split(":")
Uptimes = (int(Uptime[0])*86400) + (int(Uptime[1])*3600) + (int(Uptime[2])*60)
print(Uptimes)
write_api.write(bucket,org,Point("Uptime").field("Uptime", Uptimes))
Uptime2 = datetime.timedelta(seconds=Uptimes)
print(Uptime2)
print()



start = value4.find("Downstream\n") + len("Downstream\n")
end = value4.find("DCID")
error = value4[start:end]
if error != "":
    print("Error:\n" + error)
    write_api.write(bucket,org,Point("Error").field("Error", error))

print()
print("Finished")

client.close()
sys.exit()

