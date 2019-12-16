

#!/usr/bin/env python3
import sys
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.chrome.options import Options

# chrome_options = Options()  
# chrome_options.add_argument("--headless") 


# -*- coding: utf-8 -*-    
    
if(len(sys.argv)>1):
    item = sys.argv[1]
    
    
ratings=[]
names = []
prices = []
disPrices = []
links = []
res='y'
url=""
avail = ["earthen-cookwares","table-wares","earthen-pots","incense-sticks"]
#item = input("search item").replace(" ", "-")
item=item.replace(" ","-")
if item in avail:
    url = "https://mitticool.com/product-category/"+item
elif item in "pots":
    url = "https://mitticool.com/product-category/earthen-pots"
elif item in "cookwares":
    url = "https://mitticool.com/product-category/earthen-cookwares"
else:
    url = "https://mitticool.com/?s="+item+"&page=search&post_type=product"
r = requests.get(url)

    #headers={Cookies :                              
    #{ userLocation: {"address":"Ejipura, Bengaluru, Karnataka, India","area":"Ejipura","deliveryLocation":"Ejipura, Bengaluru","lat":12.9385333,"lng":77.6308174}}})
data = r.text
    
soup = BeautifulSoup(data,"lxml")
    
isAvailableOrNot = soup.find('p',class_="woocommerce-info")
if isAvailableOrNot!=None and isAvailableOrNot.text=="No products were found matching your selection.":
    print("No products were found matching your selection.")
    print("We can show you  some other products info you might be interested in.")
    res= input("y for yes and n for no ")
        
if res=="y":
    for listItem in soup.findAll('li', "product-warp-item"):
        
        Rating = listItem.find('div', class_='star-rating')
        if(Rating!=None):
            rating = Rating.text[6:10]+"/5.00"
            ratings.append(rating)
        else:
            ratings.append("rating not available")
    
        Name = listItem.find('div',class_="name nasa-show-one-line")
        name = Name.findChild("a" , recursive=False)
        #print(name.text+"  "+name["href"])
        names.append(name.text.strip())
        links.append(name["href"])
    
        Price = listItem.find('span', class_="price")
        if(Price!=None):
            prices.append(Price.findChildren('span', class_="woocommerce-Price-amount amount")[0].text)
            try:
                disPrices.append(Price.findChildren('span', class_="woocommerce-Price-amount amount")[1].text)
            except:
                disPrices.append("No discount")
        else:
            prices.append("Sold Out")
            disPrices.append("Sold Out")
    print("S.no.","itemName","price","disPrice","ratings", sep= '\t')
    for i in range(len(names)):
        print(str(i+1),names[i],prices[i],disPrices[i],ratings[i], sep= '\t')
        print('\n')
    resp = input("If you want to buy any of these enter 'y' else  enter 'n'.")
    if resp=='y':
        sNo = input("Enter the id of the product you wish to buy")
    else:
        print("Thankyou")
        exit()




url = links[int(sNo)-1]
driver = webdriver.Chrome(executable_path = '/home/ali_zakir/Programs/python/Codeasylum/Hackathon/chrome/chromedriver')

driver.get(url)
driver.implicitly_wait(5)
try:
    driver.find_element_by_name('add-to-cart').click()
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="nasa-cart-sidebar"]/div[3]/div[2]/div[2]/a[1]'))
    )
    element.click()


    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div/div[2]/div/div/div/div[2]/a'))
    )
    element.click()

    first_name = driver.find_element_by_id('billing_first_name')
    first_name.send_keys('Ali Asgar')

    last_name = driver.find_element_by_id('billing_last_name')
    last_name.send_keys('Zakir')

    house_no = driver.find_element_by_id('billing_address_1')
    house_no.send_keys('45')

    billing_city = driver.find_element_by_id('billing_city')
    billing_city.send_keys('Bangalore')


    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'select2-selection__arrow'))
    )
    element.click()

    state = driver.find_element_by_class_name('select2-search__field')
    state.send_keys('Karnataka')
    state.send_keys(Keys.ENTER)


    postcode = driver.find_element_by_name('billing_postcode')
    postcode.send_keys('560078')

    phone_num = driver.find_element_by_name('billing_phone')
    phone_num.send_keys('5600784580')

    email = driver.find_element_by_id('billing_email')
    email.send_keys('whatever@wherever.com')

    driver.find_element_by_id('place_order').click()
    driver.close()
    print('Thank you for ordering')


except:
    print('Out of Stock')
    driver.close()


mittikool.py

