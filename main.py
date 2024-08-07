from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException, TimeoutException,StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import os
import time

# setting up the driver
driver_path = "/home/user/chrome-linux64/chrome"
# Set the path to the ChromeDriver executable in the PATH environment variable
os.environ["PATH"] += ":/home/user/chrome-linux64/chrome"
driver = webdriver.Chrome()

# get the naivas hompepage
driver.get(url="https://naivas.online/")
all_categories = driver.find_element(by=By.XPATH, value="//a[contains(@href,'javascript')]")
try:
    all_categories.click()
except ElementNotInteractableException:
    time.sleep(2)
    all_categories.click()
# get all the submenu items
# sub_menu_names = driver.find_elements(by=By.XPATH, value="//div/div/ul/li/div/button/span/span")
# for menu in sub_menu_names:
#     print(f"menu item : {menu.text}")
#
# # get all categories under the sub menus
# sub_menu_categories = driver.find_elements(by=By.XPATH, value="//div/div/ul/li/div/div/ul/li/a")

# get the sub menu elements and treat them separately as new roots
time.sleep(5)
sub_menus = driver.find_elements(by=By.XPATH, value="//div[contains(@id,'mega')]/div/div/ul/li")
# test the submenu
# print(f"first sub menu {sub_menus[2].get_attribute('class')}")
products_dict = {}
for sub_menu in sub_menus[1:]:
    # get the categories placed under sub menus
    categories = sub_menu.find_elements(by=By.XPATH, value=".//div/div/ul/li/a")
    # get the sub menu name
    sub_menu_name = sub_menu.find_element(by=By.XPATH, value=".//div/button/span/span")
    # print(f"{sub_menu_name.text}")
    all_links = [category.get_attribute("href") for category in categories]
    dict = {sub_menu_name.text: all_links}
    products_dict.update(dict)

    # for category in categories:
    #     link = category.get_attribute('href')
    #     driver.get(link)
    #     time.sleep(2)

for key, item in products_dict.items():
    print(key)
    # key is just a category header with product pages in it ,eg food & cupboard
    # item is a list with different products pages eg food additives
    for x in item[1:2]:
        driver.get(url=x)

        # find no of products on the page
        no_of_products = driver.find_element(By.XPATH, "//div/div/div[contains(text(),'Products')]")
        no_of_products = int(no_of_products.text.split(sep=" Products")[0])
        print(f"total products= {no_of_products}")

        # find the current no of products
        # Find the element with the specific wire:snapshot attribute
        time.sleep(3.5)
        # todo img test
        image = driver.find_elements(by=By.XPATH, value="//div[contains(@class,'relative')]/div/div/a/div/img")
        for img in image:
            print(f"image : {img.get_attribute('src')}")

        # todo find the price and name of a product
        # price
        # element is the product card
        elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'product-price')]")
        element = driver.find_element(By.XPATH, "//div[contains(@class, 'product-price')]")
        price = element.find_element(by=By.XPATH, value=".//p/span").text
        # name
        price_parent = element.find_element(by=By.XPATH, value="..")
        print(f"price parent class : {price_parent.get_attribute('class')}")
        previous_sibling = price_parent.find_element(By.XPATH, "preceding-sibling::*[1]")
        product_name = previous_sibling.find_element(by=By.XPATH, value=".//a").get_attribute("title")
        print(f"name : {product_name}")
        print(f"price : {price}")


        # function to see if more products have loaded
        def has_increased(driver):
            loaded_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'product-price')]")
            return len(loaded_elements) > len(elements)


        # todo implement a while loop to keep scrolling till all products are loaded
        i = 0
        new_elements = []
        while len(new_elements) < no_of_products:
            new_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'product-price')]")
            try:
                # find the last item
                try:
                    last_item = new_elements[-6]
                except IndexError:
                    continue
                if i > 0:
                    # scroll to the last element
                    # Scroll the element into view
                    new_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'product-price')]")
                    try:
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(0.2)
                        # todo set the new_elements index for full screen to [-3]
                        driver.execute_script("arguments[0].scrollIntoView();", new_elements[-5])
                        time.sleep(2.5)
                    except StaleElementReferenceException:
                        continue

                    # Optionally, you can also adjust the view alignment
                    # Scroll to make the element appear at the top of the viewport
                    # driver.execute_script("arguments[0].scrollIntoView(true);", last_item)
                    print("yes")
                else:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    driver.execute_script("window.scrollBy(0, -200)")
            except TimeoutException:
                time.sleep(3)
                continue

            # implement a wait to wait for elements to load before scrolling again
            try:
                WebDriverWait(driver, 4).until(method=has_increased, message="either way")
            except TimeoutException:
                continue

            new_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'product-price')]")
            
            # todo implement the file write here
            i += 1

        # todo loop exited
        print(f"loop exited with products :  : {len(new_elements)}")
        elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'product-price')]")
        # new_elements is a list of product cards
        for element in new_elements:

            while True:
                try:
                    price = element.find_element(by=By.XPATH, value=".//p/span").text
                    # name
                    price_parent = element.find_element(by=By.XPATH, value="..")
                    # name is on the previous sibling of the price parent
                    previous_sibling = price_parent.find_element(By.XPATH, "preceding-sibling::*[1]")
                    product_name = previous_sibling.find_element(by=By.XPATH, value=".//a").get_attribute("title")
                    print(f"name : {product_name}")
                    print(f"price : {price}")
                    # todo fetch the product image
                    image=driver.find_elements(by=By.XPATH,value="//div/div/img")
                    for img in image:
                        print(img.get_attribute("href"))
                    # todo format the product line
                    # name,price ,discount ,image

                except NoSuchElementException:
                    continue
                time.sleep(1)
                break
        time.sleep(1)
        # determine the total no of products
        # keep fetching products until they match the number

# base_links = [link.get_attribute('href') for link in sub_menu_categories[1:]]
# print(base_links)
time.sleep(10)
