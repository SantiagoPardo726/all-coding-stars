from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from langdetect import detect
import cv2
import urllib.request
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
import random
import time

def createDriver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    prefs = {"profile.managed_default_content_settings.images":2}
    chrome_options.headless = True


    chrome_options.add_experimental_option("prefs", prefs)
    myDriver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    return myDriver

def verifyHindi(url:str):
    try:
        time.sleep(1)
        webDriver = createDriver()

        webDriver.get(url)

        text = webDriver.find_element(By.TAG_NAME,'body').text

        language = detect(text)
        
        if language == 'hi':
            return True
        return False
    except :
        return True

def verifyImage(url):
    webDriver = createDriver()
    webDriver.get(url)
    ret = False
    images = webDriver.find_elements(By.TAG_NAME,'img')
    for image in images:
        img_link = image.get_attribute('src')
        try:
            urllib.request.urlretrieve(img_link,"image.jpg")
            img = cv2.imread("image.jpg")
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            laplacian_var = cv2.Laplacian(gray,cv2.CV_64F).var()
            print(laplacian_var)
            if laplacian_var > 5000:
                ret = True
        except :
            pass
    return ret

def verifyDropDownMenu(url):
    driver = createDriver()


    driver.get(url)

    try:
        element = driver.find_element(By.XPATH,"//button[@data-name='LARGE_UP_MAIN_NAV_TRIGGER'][contains(text(), 'पाठ्यक्रम')]")

   
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()

    
        wait = WebDriverWait(driver, 10)

        try:
            expected = driver.find_element(By.XPATH, "//nav[contains(@class,'main-nav-dropdown') and contains(@class,'js-main-nav-dropdown') and contains(@class,'is-open')]")
            return True
        except:
            return False
    except :
        return False
    
def verifyInside(url):
    webDriver = createDriver()
    webDriver.get(url)
    links = webDriver.find_elements(By.TAG_NAME,"a")
    falses = 0
    for i in random.sample(links,5):
        url = i.get_attribute("href")
        print(verifyHindi(url))
        if not verifyHindi(url):
            falses += 1
    return falses<2