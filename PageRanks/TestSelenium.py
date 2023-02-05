import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver

start_url = 'https://careers.tencent.com/jobdesc.html?postId=1524645321643139072'
chrome_options = Options()
# chrome_options.add_argument("--headless")

def get_driver():
    return webdriver.Chrome(chrome_options=chrome_options)

another_url = 'https://careers.tencent.com/jobdesc.html?postId=1524644586897547264';
driver = get_driver()
driver.get(start_url)

time.sleep(1)
list_items = driver.find_elements(By.CLASS_NAME, "recruit-list-link")
main_handle = driver.window_handles
for list_item in list_items:
    list_item.click()
    time.sleep(1)
all_handles = driver.window_handles
for handle in all_handles:
    driver.switch_to.window(handle)
    print(driver.current_url)
    driver.close()
time.sleep(5)

driver.get(another_url)

time.sleep(1)
list_items = driver.find_elements(By.CLASS_NAME, "recruit-list-link")
driver.switch_to.window(main_handle[0])
driver.close()
main_handle = driver.window_handles
for list_item in list_items:
    list_item.click()
    time.sleep(1)
all_handles = driver.window_handles
for handle in all_handles:
    driver.switch_to.window(handle)
    print(driver.current_url)
    driver.close()
time.sleep(5)
driver.quit()
