from selenium import webdriver
import time

driver = webdriver.Firefox()
driver.implicitly_wait(5)
driver.get("https://m.huobi.com/?a=home")  
  
user_mail = driver.find_element_by_id("user_mail")  
user_mail.send_keys("aaa@126.com")  

user_pass = driver.find_element_by_id("user_pass")  
user_pass.send_keys("password")  
  
user_pass.submit()

driver.get("https://m.huobi.com/trade.php")

while True:
    price_div = driver.find_element_by_class_name('tc_firebrick')
    print price_div.text
    time.sleep(5)
