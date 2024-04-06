
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options

#from selenium.webdriver.chrome.options import Options

import os 
import time
from bs4 import BeautifulSoup

import re
from writexlsx import write_to_excel


from datetime import datetime, timedelta

def parse_time_delta(delta_str):
    # expected may be 2 or 3 so using except
    try:
        amount, unit, direction = delta_str.split()
    except:
        amount, unit = delta_str.split()
        direction=''
    amount = int(amount)

    # On basis of unit and create a timedelta so we can get diff time
    if unit.startswith("day"):
        delta = timedelta(days=amount)
    elif unit.startswith("hour"):
        delta = timedelta(hours=amount)
    
    elif unit.startswith("month"):
        delta = timedelta(days=amount * 30)
    elif unit.startswith("year"):
        delta = timedelta(days=amount * 365)
    else:
        raise ValueError("Unsupported unit")
    
    # Adjust the timedelta based on direction
    if direction == "ago":
        return -delta
    else:
        return delta

def launch_verifier(launch_date):
    try:
        # Parse the input to get the time delta
        delta = parse_time_delta(launch_date)

        # Calculate the upcoming launch date
        upcoming_launch_date = datetime.now() + delta
        
        today = datetime.now()
        difference = upcoming_launch_date - today

        if -1 <= difference.days <= 30:
            print("The launch date is within 1 month from today.")
            return upcoming_launch_date.strftime('%d %B %Y')
        else:
            print(f"The launch date is not within 1 month from today.") #{upcoming_launch_date.strftime('%b %d %Y')} difference {difference.days}")
            return False
    except Exception as e:
        print(f'Launch date {launch_date}   :::{e}')
        return False



    



import time

def cloudflarehelper(driver):
    try:
        time.sleep(5)
        # Switch to the first window handle
        driver.switch_to.window(driver.window_handles[0])
        
        # Iterate through all window handles except the last one
        for window_handle in driver.window_handles[:-1]:
            # Switch to the window handle
            driver.switch_to.window(window_handle)
            # Close the window
            driver.close()
        
        # Switch back to the last window handle
        driver.switch_to.window(driver.window_handles[-1])
        
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

    except:
        return False
def cloudflarebypass(driver,pg=1):
    """if not driver.title.startswith('Just'):
        return"""
    
    driver.get(f'https://coinsniper.net/presales?page={pg}')

    driver.execute_script(f"window.open('https://coinsniper.net/presales?page={pg}', '_blank')")
    time.sleep(6)
    driver.switch_to.default_content()
    verify_iframe = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'iframe'))
    )
    #driver.find_element(By.TAG_NAME, 'iframe')
    driver.switch_to.frame(verify_iframe)

    # Finding the verify button
    verify_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'ctp-checkbox-label'))
    )

    # Clicking the verify button
    verify_button.click()

    # Switching back to the default content
    driver.switch_to.default_content()
    time.sleep(5)
    maxtries=0
    while True:
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(5)
        if not driver.title.startswith('Just'):
            break
        elif not driver.title.startswith('Attention'):
            break
        elif maxtries>5:
            driver.execute_script(f"window.open('https://coinsniper.net/presales?page={pg}', '_blank')")

            #time.sleep(2)
            cloudflarehelper(driver)
        maxtries+=1
    cloudflarehelper(driver)






def Getalltokens(driver):
    # wait for table to load
    try:
        token_table = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'table.is-fullwidth'))
        )[-1]
        token_tbody=token_table.find_element(By.TAG_NAME,'tbody')
        driver.execute_script("arguments[0].scrollIntoView();", token_tbody)

        # findlist of all tokens
        tokens_list = token_tbody.find_elements(By.TAG_NAME, 'tr')
        print(f'Length {len(tokens_list)} ')
        for token in tokens_list:
            driver.execute_script("arguments[0].scrollIntoView();", token)

            # Find token name, symbol, and chain name
            #try:
            token_html=token.get_attribute('outerHTML')
            token_soup = BeautifulSoup(token_html, 'html.parser')

            # Find the element with class 'listing-name' inside the `token` element
            token_name_element = token_soup.find(class_='listing-name')

            # Get the text of the element
            token_name = token_name_element.get_text().replace('\n','').strip()
            token_symbol_element = token_soup.find(class_='listing-symbol')
            token_symbol=token_symbol_element.get_text().replace('\n','').strip()
            #token.find_element(By.CLASS_NAME, 'listing-name').text
            token_full_name=token_name+' $'+token_symbol
            #except:
            #    token_full_name=''
            try:
                chain_name = token.find_element(By.CLASS_NAME, 'network').text
            except:
                chain_name=''
            # Find launch date upcoming date
            #try:                                                /html/body/section[5]/div[8]/div/div[1]/table/tbody/tr[1]/td[12]
            launch_date_element = token.find_element(By.XPATH, f'./td[9]')
            launch_date_text = launch_date_element.text.lower()

            #except:
            #    launch_date_text=''
            formatted_date = launch_date_text.replace('in', '').replace('tba', '').strip()

            print('formatted date:',formatted_date)
            # Check if date is not empty 
            if formatted_date:
                upcoming_launch = launch_verifier(formatted_date)
                if upcoming_launch:
                    # Get url
                    token_url_element = token.get_attribute('data-listingid')
                    token_url = f'https://coinsniper.net/coin/{token_url_element}'
                    
                    # writing data to xlsx
                    data = {
                        'token': token_full_name,
                        'token_url': token_url,
                        'chain_name': chain_name,
                        'status':'upcoming',
                        'upcoming_launch':upcoming_launch
                    }
                    print(data) 
                    write_to_excel(data)
        return True
    except Exception as e:
        print(f'Error occured Coinsniper func(GetAllTokens) : {e}')
        return False


def verifier(driver,pg=1):
     if  driver.title.startswith('Attention') or  driver.title.startswith('Just'):
        driver.delete_all_cookies()
        
        cloudflarebypass(driver,pg)
        try:
            time.sleep(4)
            understand_button=driver.find_element(By.CLASS_NAME,'button.is-primary.close.full-width')
            understand_button.click()
            time.sleep(0.5)

        except:
            pass


def Coinsniper():
    # Set up Chrome options
    try:
        chrome_options = Options()
        chrome_options.add_argument(f'--incognito')
        #chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        #chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--no-sandbox")
        #chrome_options.add_argument("--headless=new")
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Firefox(options=chrome_options)


        # Open a webpage that requires cookies
        driver.get("https://www.coinsniper.net")
        driver.delete_all_cookies()
        verifier(driver)
        try:
            totalpages= int(WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, 'pagination-link'))
                )[-1].text)
        except:
            totalpages=9
        for pg in range(1,totalpages+1):
            driver.get(f'https://coinsniper.net/presales?page={pg}')
            #time.sleep(4)
            verifier(driver,pg)
            #while True:
            Getalltokens(driver)
        driver.quit()
        return True
    except Exception as e:
        print(f'Error Occured in Coinsniper {e}')
        return False        
    

Coinsniper()
"""chrome_options = Options()
chrome_options.add_argument(f'--incognito')
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
chrome_options.add_experimental_option('useAutomationExtension', False)
driver=webdriver.Chrome(options=chrome_options)


# Open a webpage that requires cookies
driver.get("https://coinsniper.net/presales")


driver.switch_to.window(driver.window_handles[0])



driver.switch_to.default_content()
verify_iframe=driver.find_element(By.TAG_NAME,'iframe')
driver.switch_to.frame(verify_iframe)
verify_button=driver.find_element(By.CLASS_NAME,'ctp-checkbox-label').click()
driver.switch_to.default_content()
"""





