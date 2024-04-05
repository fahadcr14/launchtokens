
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
        upcominglaunch_date = datetime.strptime(launch_date, '%B %d, %Y')

        today = datetime.now()
            
        today = datetime.now()
        difference = upcominglaunch_date - today

        if 0 <= difference.days <= 30:
            #write_to_excel(data)
            print("The launch date is within 1 month from today.")
            return True
        else:
            print("The launch date is not within 1 month from today.")
            return False
    except Exception as e:
        print(e)
        return False
    



def GetTokenInfo(driver,data):
    try:
        token_url=data['token_url']
        driver.get(token_url)
        time.sleep(2)
        chain_name=WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'mr-3'))
                ).text
        chain_name
        launch_date_element=driver.find_element(By.CLASS_NAME,'text-muted.mb-3').text
        launch_date=launch_date_element.replace('Launch Date','').strip()
        if launch_verifier(launch_date):
            data['chain_name']=chain_name
            data['status']='presale'
            data['upcoming_launch']=launch_date
            write_to_excel(data)
            return True
    except Exception as e:
        print(f'Error while fetching token info :{e}')
        return False


def GetAllTokens(driver):
    global tokens_urls
    tokenTable=driver.find_element(By.ID,'presale-content')
    tokens_list=driver.find_elements(By.CLASS_NAME,'singlecoinlink.p-2.align-items-center')

    token_body=tokens_list[0].find_element(By.CLASS_NAME,'media-body')
    token_name=token_body.find_element(By.TAG_NAME,'p').text
    token_symbol=token_body.find_element(By.TAG_NAME,'small').text
    token_full_name=token_name+' $'+token_symbol
    for token in tokens_list:
        launch_check=token.find_element(By.CLASS_NAME,'col-2.d-none.d-lg-block.age-date.text-center.coin-redirect').text
        if launch_check.startswith('Launching in'):
            token_url=token.get_attribute('data-href')
            data={
                'token':token_full_name,'token_url':token_url
            }
            tokens_urls.append(data)
            
            print(f'{token_url}')
            


def CoinGod():
    try:
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=chrome_options)
        tokens_urls=[]
        driver.get('https://coinsgods.com/')
        while True:
            try:
                presale_button=WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, '/html/body/section/div/div[2]/div[4]/ul/li[3]/a'))
                        )
                driver.execute_script("arguments[0].scrollIntoView();", presale_button)

                presale_button.click()
                break
            except:
                pass
        while True:
            try:
                show_all_button=WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, 'presale-more'))
                    )
                show_all_button.click()
            except:
                show_all_button=''
            time.sleep(2)
            if not show_all_button:
                break
        GetAllTokens(driver)
        for data in tokens_urls:
            GetTokenInfo(driver,data)
        driver.quit()
        return True
    except Exception as e:
        print(f'Error Occured in CoinsGod {e}')
        return False
