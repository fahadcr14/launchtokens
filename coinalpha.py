
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


def launch_verifier(launch_date):
    try:
        upcoming_launch_date = datetime.strptime(launch_date, '%b %d %Y')
        today = datetime.now()
            
        difference = upcoming_launch_date - today

        if -1 <= difference.days <= 30:
            print("The launch date is within 1 month from today. ")
            return True
        else:
            print(f"The launch date is not within 1 month from today. {launch_date} difference {difference.days}")
            return False
    except Exception as e:
        print(f'Launch date {launch_date}   :::{e}')
        return False

    



def GetTokeninfo(driver):
    try:
        try:
            token_fullname_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div/div/div/main/div[1]/div[5]/div[1]/div[2]/h2'))
            )
            token_fullname = token_fullname_element.text
        except: 
            token_fullname=''

        try:
            launch_date_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/main/div[1]/div[7]/div[2]/div[1]/div/ul/li[2]/a[2]/span')))
            launch_date = launch_date_element.text.strip().replace('nd', '').replace('st', '').replace('rd', '').replace('th', '')
        except:
            launch_date=''
            return False
        launch_verification_result = launch_verifier(launch_date)
        try:

            chain_name_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'chainDiv'))
            )
            chain_name = chain_name_element.text.replace('Network:', '').strip()
        except:
            chain_name=''
        if launch_verification_result and token_fullname:
            data={
                'token':token_fullname,
                'token_url':driver.current_url,
                'status':'upcoming',
                'chain_name':chain_name,
            'upcoming_launch':launch_date

            }
            write_to_excel(data)
            return True
    except Exception as e:
        print(f'Error fetching GetTokensinfo: {e}')



"""tokens_list=driver.find_elements(By.CLASS_NAME,'backgroundGray')
token_criteria=tokens_list[0].find_elements(By.CLASS_NAME,'hrefUrl.nonDisplayMB')[-1].text
token_criteria
if token_criteria.startswith('Launch'):
    tokens_list[0].click()
    driver.maximize_window()
    GetTokeninfo(driver)"""


def CoinALPHA():
    try:
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=chrome_options)
        driver.get('https://coinalpha.app/recently-add-list.html?page=1')
        try:
            close_ad=WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'btn-close.text-primary'))
            )
            close_ad.click()
        except:
            print(f'No Ad')
        driver.get('https://coinalpha.app/recently-add-list.html?page=1')
        next_button=WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/main/div/div[4]/div[2]/div/ul/li[5]/a'))
            )
        driver.execute_script("arguments[0].scrollIntoView();", next_button)

        time.sleep(4)
        next_button.click()
        total_pages_element =WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/main/div/div[4]/div[2]/div/ul/li[4]/a'))
            )
        total_pages = int(total_pages_element.text)
        # Iterate through the pages
        for page_num in range(1, total_pages + 1):
            tokens_urls=[]
            # Load the page
            url = f'https://coinalpha.app/recently-add-list.html?page={page_num}'
            driver.get(url)
            action_chain = ActionChains(driver)

            # Wait for tokens_list elements to be present
            tokens_list = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'backgroundGray'))
            )
            token_body=driver.find_element(By.CLASS_NAME,'container.coinCategory')
            a_tags=token_body.find_elements(By.TAG_NAME,'a')
            #for tag in a_tags:
            #    if '/token' in url:
            #        print(url)
            # Iterate through each token in the list
            for i,token in enumerate(tokens_list):
                # Extract token criteria

                token_criteria_element = WebDriverWait(token, 2).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, 'hrefUrl.nonDisplayMB'))
                )
                token_criteria = token_criteria_element[-1].text
                
                # Check if token criteria starts with 'Launch'
                if token_criteria.startswith('Launch'):
                    url=a_tags[i].get_attribute('href')
                    tokens_urls.append(url)
                
            for url in tokens_urls:
                driver.execute_script(f"window.open('{url}', '_blank')")

                driver.switch_to.window(driver.window_handles[-1])
                GetTokeninfo(driver)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
        driver.quit()
        return True
    except Exception as e:
        print(f'Error Occured in CoinAlpha {e}')
        return False





