from selenium import webdriver
from selenium.webdriver.common.by import By
import time

chrome_driver_path = "C:\Development/chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver_path)

cookie_clicker_url = "http://orteil.dashnet.org/experiments/cookie/"
driver.get(url=cookie_clicker_url)

cookie = driver.find_element(by=By.ID, value="cookie")

# returns items in the store
store = driver.find_elements(by=By.CSS_SELECTOR, value="#store div")
store_items = [items.get_attribute("id") for items in store if items != ""]
print(store_items)

timeout = time.time() + 5
end_game = time.time() + 60 * 5

while True:
    cookie.click()

    if time.time() > timeout:

        # returns value of items in the store
        value = driver.find_elements(by=By.CSS_SELECTOR, value="#store b")
        item_cost = []

        for item in value:
            element_text = item.text
            if element_text != "":
                cost = int(element_text.split("-")[1].strip().replace(",", ""))
                item_cost.append(cost)

        # return amount of money available
        cookie_avalible = driver.find_element(by=By.ID, value="money")
        money = int(cookie_avalible.text.replace(",", ""))

        # find and purchase the highest item with cookies available by returning the index of money
        x = min(item_cost, key=lambda x: abs(x - money))
        if x > money:
            item_index = item_cost.index(x) - 1
        else:
            item_index = item_cost.index(x)

        purchase_item = driver.find_element(by=By.ID, value=f"{store_items[item_index]}")
        purchase_item.click()

        timeout = time.time() + 5
        # End Game after 5 min.
        if time.time() > end_game:
            cps = driver.find_element(by=By.ID, value="cps")
            print(cps.text)
            break

driver.quit()
