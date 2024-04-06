
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os 
import time
import re
from writexlsx import write_to_excel

tokens_urls=[]

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
        driver.maximize_window()

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
    page_source = driver.page_source

    # Create a BeautifulSoup object
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find all token elements
    tokens_list = soup.find_all('div', class_='singlecoinlink p-2 align-items-center')

    for token in tokens_list:
        # Find token body
        token_body = token.find('div', class_='media-body')
        token_name = token_body.find('p').get_text(strip=True)
        token_symbol = token_body.find('small').get_text(strip=True)
        token_full_name = f"{token_name} ${token_symbol}"
        
        # Find launch check
        launch_check = token.find('div', class_='col-2 d-none d-lg-block age-date text-center coin-redirect').get_text(strip=True)
        
        if launch_check.startswith('Launching in'):
            token_url = token.get('data-href')
            data = {'token': token_full_name, 'token_url': token_url}
            tokens_urls.append(data)
            
            print(token_url)
            
            print(f'{token_url}')
            
            


def CoinGod():
    #try:
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=chrome_options)
        
        driver.get('https://coinsgods.com/')
        driver.maximize_window()
        while True:
            try:
                """presale_button=WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, '/html/body/section/div/div[2]/div[4]/ul/li[3]/a'))
                        )
                driver.execute_script("arguments[0].scrollIntoView();", presale_button)

                presale_button.click()"""
                presale_button=WebDriverWait(driver, 10).until(
                            EC.presence_of_all_elements_located((By.CLASS_NAME, 'nav-link'))
                        )
                driver.execute_script("arguments[0].scrollIntoView();", presale_button[-1])

                presale_button[-1].click()
                break
            except Exception as e :
                print(f'e {e}')
        try:
            accept_cookies = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'js-cookie-consent-agree.cookie-consent__agree.btn.col-12'))
            )
            accept_cookies.click()
            time.sleep(4)
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
    #except Exception as e:
        print(f'Error Occured in CoinsGod {e}')
        return False
#CoinGod()