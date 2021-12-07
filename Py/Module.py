import time
from http.cookiejar import Cookie
from cairosvg import svg2png
import requests as requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()
rki_dashboard = "https://digi4school.at/"
driver.get(rki_dashboard)

emailField = driver.find_element_by_id("email")
emailField.send_keys("sascha.gottsbacher@aon.at")

passwordField = driver.find_element_by_id("password")
passwordField.send_keys("BOnqRqMyP1PKWdD8OOtZ")

passwordField.send_keys(Keys.ENTER)

time.sleep(2)
cookies = driver.get_cookie("digi4s")
print(cookies)

url = 'https://a.digi4school.at/ebook/3363/21/img/6.png'
filename = url.split('/')[-1]
cookie = {'name': 'digi4s',
          'value': '\"143836%2c1632308643%2c1632308643%20{287%200%204AFEF820584A033B1653462A0B0EED569FF513C2}\"',
          'path': '/',
          'domain': '.digi4school.at',
          'secure': 'True',
          'httpOnly': 'True',
          'sameSite': 'Lax'
          }

r = requests.get(url, cookies=Cookie('name:', cookies.__getitem__("name"), 'value:', cookies.__getitem__("value")))
open(filename, 'wb').write(r.content)

#svg2png(file_obj='C:\\Users\\sasch\\Downloads\\Neuer Ordner\\21.svg', write_to='output.png')

driver.quit()
