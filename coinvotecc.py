
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime,timedelta
import csv 
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

import os 
import time
import re
import pandas as pd




def write_to_excel(data):
    filename = f'cryptotokens.xlsx' 
    new_row = pd.DataFrame([data])

    if os.path.isfile(filename):
        df = pd.read_excel(filename)
        if 'token' in df.columns:
            # Check for duplicates based on job_title
            if data['token'] in df['token'].values:
                duplicate_index = df.index[df['token'] == data['token']].tolist()
                df.loc[duplicate_index[0]] = new_row.iloc[0]
                df.to_excel(filename, index=False)  # Save updated DataFrame to Excel
                return
        updated_df = pd.concat([df, new_row], ignore_index=True)
        updated_df.to_excel(filename, index=False)

    else:
        # Write DataFrame to Excel
        new_row.to_excel(filename, index=False)





def cloudflarehelper(driver):
    try:
        time.sleep(5)
        driver.switch_to.window(driver.window_handles[0])
        driver.close()
        driver.switch_to.window(driver.window_handles[-1])
        return True
    except:
        return False
def cloudflarebypass(driver):
    driver.get('https://coinvote.cc/')

    driver.execute_script("window.open('https://coinvote.cc/', '_blank')")
    time.sleep(2)
    maxtries=0
    while True:
        driver.switch_to.window(driver.window_handles[-1])

        if not driver.title.startswith('Just'):
            break
        elif maxtries>5:
            driver.execute_script("window.open('https://coinvote.cc/', '_blank')")

            time.sleep(2)
            cloudflarehelper(driver)
        maxtries+=1
    cloudflarehelper(driver)






def TokenDateTime(driver,token_url,data):
    try:
        driver.get(token_url)
        upcoming_launch_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'fw-light.fs-5.text-white.text-opacity-75')))
        try:
            for launch_ele in upcoming_launch_elements:
                if launch_ele.text=='Launch Date':
                    sibling_element = launch_ele.find_element(By.XPATH, 'following-sibling::*')
                    upcoming_launch_date = sibling_element.text
                    break
        except:
            upcoming_launch_date=''
        if upcoming_launch_date:
            data['upcoming_launch']=upcoming_launch_date
            date_pattern = re.compile(r'\b(\d+)(st|nd|rd|th)\b')

            date_string_cleaned = re.sub(date_pattern, r'\1', upcoming_launch_date)

            launch_date = datetime.strptime(date_string_cleaned, '%B %d %Y, %H:%M')

            # Calculate today's date
            today = datetime.now()

            difference = launch_date - today
            if difference <= timedelta(days=30) and difference>=timedelta(days=0):
                write_to_excel(data)
                print("The launch date is within 1 month from today.")
            else:
                print("The launch date is not within 1 month from today.")
    except Exception as e:
        print(f'Error in date {e}')
        return False


def Gettokensinfo(driver):
    tokens_urls=[]
    try:
        coinTables=driver.find_elements(By.CLASS_NAME,'table.table-sm.table-hover.table-sort.align-middle')

        coins=coinTables[-1].find_elements(By.TAG_NAME,'tr')
        for coin in coins[1:]:
            try:
                token=coin.find_element(By.CLASS_NAME,'link-white.d-inline-flex.fw-semibold.mb-0')
                token_symbl=token.find_element(By.XPATH, 'following-sibling::*').get_attribute('innerHTML')
                token_name=token.text+' '+token_symbl
            except:
                token_name=''
            try:
                token_url=token.get_attribute('href')
            except:
                token_url=''
            try:
                token_chain_element=coin.find_element(By.CLASS_NAME,'async-tooltip')
                chain_name=token_chain_element.get_attribute('data-bs-title')
            except:
                chain_name=''
            data={
                'token':token_name,
                'token_url':token_url,
                'chain_name':chain_name,
                'status':'upcoming'
            }
            tokens_urls.append(data)
        return tokens_urls
    except Exception as e :
        print(f'Erro occured :{e}')
        return False

def Coinvote():
    try:
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=chrome_options)
        cloudflarebypass(driver)
        driver.switch_to.window(driver.window_handles[0])

        pg=1

        explored_urls=[]
        while True:
            upcoming_launch=f'https://coinvote.cc/en/soon?page={pg}'
            driver.get(upcoming_launch)
            tokens_urls=Gettokensinfo(driver)

            """if not tokens_urls:
                break"""
            for data in tokens_urls:
                token_url=data['token_url']
                TokenDateTime(driver,token_url,data)
            upcoming_launch=f'https://coinvote.cc/en/soon?page={pg}'
            driver.get(upcoming_launch)
            
            try:
                # Wait for the Next>> page button to be present
                next_buttons = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, 'page-link.scroll-to-id'))
                )

                # Scroll to the last page button
                driver.execute_script("arguments[0].scrollIntoView(true);", next_buttons[-1])
                time.sleep(5)
                # Click on the last page button
                next_buttons[-1].click()
                time.sleep(3)
                current_url=driver.current_url
                
                if  current_url in explored_urls:
                    print(f'stopped {pg}')
                    break
                explored_urls.append(current_url)

                pg+=1
            except Exception as e:
                print(f'Error clicking not found {e}')
                break
        driver.quit()
        return True
    except Exception as e:
        print(f'Error Occured in Coinvote {e}')
        return False




