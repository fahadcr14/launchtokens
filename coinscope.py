
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
from selenium.webdriver.chrome.options import Options

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
            print("Coinscope.... The launch date is within 1 month from today.")
            return upcoming_launch_date.strftime('%d %B %Y')
        else:
            print(f"Coinscope.... The launch date is not within 1 month from today. {upcoming_launch_date.strftime('%b %d %Y')} difference {difference.days}")
            return False
    except Exception as e:
        print(f'Launch date {launch_date}   :::{e}')
        return False



    



def GetTokensinfo(driver):
#    tokensTable=driver.find_elements(By.CLASS_NAME,'StyledTable__StyledTableBody-sc-1m3u5g-3.ikEKCL')[-1]
    tokens_table = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'StyledTable__StyledTableBody-sc-1m3u5g-3.ikEKCL')))[-1]
    driver.execute_script("arguments[0].scrollIntoView();", tokens_table)

    tokens_list = WebDriverWait(tokens_table, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'tr')))

    for token in tokens_list:
        driver.execute_script("arguments[0].scrollIntoView();", token)

        try:
            token_name=WebDriverWait(token, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'StyledText-sc-1sadyjn-0.fQgoZl'))).text
            #token.find_element(By.CLASS_NAME,'StyledText-sc-1sadyjn-0.fQgoZl').text
        except:
            token_name=''
        token_symbol=token.find_element(By.CLASS_NAME,'StyledText-sc-1sadyjn-0.rJhBx').text
        chain_name=token.find_element(By.CLASS_NAME,'StyledText-sc-1sadyjn-0.bQJHUq.sc-64639b5-0.dUlDoY').text
        launch_date=token.find_element(By.CLASS_NAME,'StyledText-sc-1sadyjn-0.hQCGdn').text

        formatted_data=launch_date.replace('in','').replace('today','1 day').replace('tomorrow','1 day').strip()
        launch_date=launch_verifier(formatted_data)
        if launch_date:
            token_url_element=token.find_element(By.CLASS_NAME,'sc-4c4441b8-0.VurIK')
            token_url=token_url_element.get_attribute('href')
            token_url
            
            data={
                'token':token_name+' '+token_symbol,
                'token_url':token_url,
                'chain_name':chain_name,
                'status':'upcoming',
                'upcoming_launch':launch_date
            }
            print(data)
            write_to_excel(data)


def CoinScope():
    try:
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=chrome_options)
        
        driver.get('https://www.coinscope.co/presale')
        totalpages = int(WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'StyledButtonKind-sc-1vhfpnt-0.iLkOuo.StyledPageControl__StyledPaginationButton-sc-1vlfaez-0.kPuPyK')))[-1].text)

        for pg in range(1,totalpages):
            try:
                driver.get(f'https://www.coinscope.co/presale?page={pg}')
                time.sleep(4)
                GetTokensinfo(driver)
                print(f'DOne  {pg }page --{driver.current_url}---------')
            except Exception as e:
                print(f'No page loading {e}')
        driver.quit()
        return True
    except Exception as e:
        print(f'Error Occured in Coinscope {e}')
        return False
#CoinScope()


