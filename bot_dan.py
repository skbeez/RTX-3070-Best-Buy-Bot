from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from include.credentials import *
from include.config import *
import smtplib, ssl
import shutil

PROFILE_PATH = "/Users/kiran/Downloads/ChromeProfile/Profile2"

try:
    shutil.rmtree(PROFILE_PATH)
except OSError as e:
    print("Error: %s : %s" % (PROFILE_PATH, e.strerror))

# Email context
context = ssl.create_default_context()

# make sure this path is correct
PATH = "/Users/kiran/Github/RTX-3070-Best-Buy-Bot/chromedriver"

chrome_options = Options()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument(f'--user-data-dir={PROFILE_PATH}')
driver = webdriver.Chrome(PATH, options=chrome_options)

RTX3070LINK1 = "https://www.bestbuy.com/site/nvidia-geforce-rtx-3070-8gb-gddr6-pci-express-4-0-graphics-card-dark-platinum-and-black/6429442.p?skuId=6429442"
RTX3070LINK2 = "https://www.bestbuy.com/site/gigabyte-geforce-rtx-3070-8g-gddr6-pci-express-4-0-graphics-card-black/6437912.p?skuId=6437912"
XBOXONETEST = "https://www.bestbuy.com/site/microsoft-xbox-one-s-1tb-console-bundle-white/6415222.p?skuId=6415222"
TEST = "https://www.bestbuy.com/site/logitech-z150-2-0-multimedia-speakers-2-piece-black/5326434.p?skuId=5326434"
RTX3060TILINK = "https://www.bestbuy.com/site/nvidia-geforce-rtx-3060-ti-8gb-gddr6-pci-express-4-0-graphics-card-steel-and-black/6439402.p?skuId=6439402"

link_to_buy = RTX3060TILINK
email = dan_email
password = dan_password
cvv = dan_cvv

driver.get(link_to_buy)

isComplete = False

print(f"Running with email:{email}")
while not isComplete:
    try:
        # find add to cart button
        try:
            atcBtn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".add-to-cart-button"))
            )
        except:
            driver.refresh()
            continue

        print("Add to cart button found")

        try:
            # add to cart
            atcBtn.click()

            # go to cart and begin checkout as guest
            driver.get("https://www.bestbuy.com/cart")

            checkoutBtn = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/main/div/div[2]/div[1]/div/div[1]/div[1]/section[2]/div/div/div[3]/div/div[1]/button"))
            )
            checkoutBtn.click()
            print("Successfully added to cart - beginning check out")

            # fill in email and password
            emailField = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "fld-e"))
            )
            emailField.send_keys(email)

            pwField = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "fld-p1"))
            )
            pwField.send_keys(password)

            # click sign in button
            signInBtn = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/section/main/div[2]/div[1]/div/div/div/div/form/div[3]/button"))
            )
            signInBtn.click()
            print("Signing in")

            # fill in card cvv
            cvvField = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "credit-card-cvv"))
            )
            cvvField.send_keys(cvv)
            print("Attempting to place order")

            # place order
            placeOrderBtn = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".button__fast-track"))
            )
            placeOrderBtn.click()

            isComplete = True
        except:
            # make sure this link is the same as the link passed to driver.get() before looping
            driver.get(link_to_buy)
            print("Error - restarting bot")
            continue
    except KeyboardInterrupt:
        print("Caught stop signal...")
        driver.close()
        exit()

print("Order successfully placed")

with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT, context=context) as server:
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    email_message = f"Subject: Best Buy Bot\n\n"
    email_message += "Order has been placed successfully! -Kiran"

    server.sendmail(EMAIL_ADDRESS, email, email_message)
    server.sendmail(EMAIL_ADDRESS, EMAIL_SMS_DAN, email_message)

