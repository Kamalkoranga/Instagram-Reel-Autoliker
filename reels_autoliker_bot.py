# Packages
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import configparser

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')
username = config.get('Instagram', 'username')
password = config.get('Instagram', 'password')
crush_id = config.get('Instagram', 'crush_id')

# Microsoft Edge setup
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open Instagram
driver.get("https://www.instagram.com/")
time.sleep(3)

# Enter username, password and click on login
username_input = driver.find_element(By.XPATH, '''/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[1]/div/label/input''')
username_input.send_keys(username) # ------------- Enter your instagram username
password_input = driver.find_element(By.XPATH, '''/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[2]/div/label/input''')
password_input.send_keys(password) # -------------- Enter your instagram password
password_input.send_keys(Keys.ENTER)
time.sleep(3)
wait = WebDriverWait(driver, 10)

# Click on reel section
reel = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[4]/div/a")))
reel.click()

i = 1

while True:
    time.sleep(2)
    
    # Open likes section
    likes = wait.until(EC.visibility_of_element_located((By.XPATH, f"/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[{i}]/div/div[2]/div[1]/div")))
    driver.execute_script("arguments[0].click();", likes)
    time.sleep(2)
    
    # Searches Your crush
    # crush = driver.find_element(By.XPATH, f"// div[contains(text(), {crush_id})]") #---------------- Change Here
    crush_liked = False
    for element in driver.find_elements(By.XPATH, f"//*[contains(text(), '{crush_id}')]"):
        crush_liked = True
        break
    
    # if he/she had liked
    if crush_liked :
        print(f"{crush_id} liked this reel...")
        time.sleep(2)
        
        # Closes the likes section
        cross = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div/div[1]/div[2]/div")))
        driver.execute_script("arguments[0].click();", cross)
        time.sleep(2)
        
        # Checks if you had also liked
        like_button = driver.find_element(By.CSS_SELECTOR, '[aria-label="Like"]')
        is_liked = 'glyphsSpriteHeart__outline__24__grey_9' in like_button.get_attribute('class')

        if is_liked:
            print('The reel is liked by me also.')
        else:
            
            # If you not than it will like that reel
            like = wait.until(EC.visibility_of_element_located((By.XPATH, f"/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[{i}]/div/div[2]/div[1]/span/button")))
            driver.execute_script("arguments[0].click();", like)
        
    # If he/she had not liked then it will skip that reel
    else:
        print(f"{crush_id} didn't like this reel....")
        time.sleep(2)
        cross = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div/div[1]/div[2]/div")))
        driver.execute_script("arguments[0].click();", cross)
    
    # Scroll the window for next reel
    reels_window = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div")))
    driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', reels_window)
    i += 2
    

