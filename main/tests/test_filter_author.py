from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome('./chromedriver')
driver.get("http://deep.sas.upenn.edu/advancedsearch.php")
print(driver.title)