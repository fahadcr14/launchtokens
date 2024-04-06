
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

import os 
import time
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
            print(f"The launch date is not within 1 month from today. {upcoming_launch_date.strftime('%b %d %Y')} difference {difference.days}")
            return False
    except Exception as e:
        print(f'Launch date {launch_date}   :::{e}')
        return False



    



def GetTokeninfo(driver):
    time.sleep(5)
    try:
        tokensTable=driver.find_elements(By.CLASS_NAME,'chakra-table.css-6w6wki')[-1]
        tokens_list=tokensTable.find_elements(By.TAG_NAME,'tr')

        url_prefix='https://www.freshcoins.io/coins/'
        for token in tokens_list:
            try:
                token_element=token.find_element(By.CLASS_NAME,'chakra-text.css-1bsgmhw').text
            except:
                token_element=''
            try:
                token_name=token_element.split('\n')[0]
            except:
                token_name=''
            try:
                token_symbol=token.find_element(By.CLASS_NAME,'chakra-stack.css-84zodg').text
            except:
                token_symbol=''
            try:
                chain_name=token_element.split('\n')[1]
            except:
                chain_name=''
            try:
                launch_date=token.find_elements(By.CLASS_NAME,'css-61tknw')[-2].text
            except:
                launch_date=''
            if launch_date:
                formated_date=launch_date.replace('in','').strip()
                upcoming_launch_date=launch_verifier(formated_date)
                if upcoming_launch_date:
                    
                    token_url_suffix=token_name.replace(' ','-').replace('$','').strip().lower()
                    token_url=url_prefix+token_url_suffix
                    
                    data={
                        'token':token_name+' '+token_symbol,
                        'token_url':token_url,
                        'chain_name':chain_name,
                        'status':'upcoming',
                        'upcoming_launch':upcoming_launch_date
                    }
                    print(data)
                    write_to_excel(data)
        return True
    except Exception as e :
        print(f'Error fetching tokens: {e}')

        return False


def Freshcoins():
    #try:
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=chrome_options)

        # Load the webpage
        driver.get('https://www.freshcoins.io/')
        recently_added_tab = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'tabs-57--tab-3')))
        recently_added_tab.click()

        # Find the next button
        while True:
            if GetTokeninfo(driver):
                next_button = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'chakra-button.css-19i45qx')))[-1]
                driver.execute_script("arguments[0].scrollIntoView();", next_button)
                time.sleep(5)
                # Click the next button
                next_button.click()

                # Check if the button is disabled
                if next_button.get_attribute('disabled'):
                    print('Yes, the button is disabled')
                    break
            else:
                print(f'Fetching token again')
        driver.quit()
        return True
    #except Exception as e:
        print(f'Error Occured in Freshcoins {e}')
        return False

Freshcoins()
