
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







def launch_verifier(pre_sale_start_date):
    date_pattern = re.compile(r'(\d{4})/(\d{2})/(\d{2}) (\d{2}):(\d{2}):(\d{2})')

    match = date_pattern.match(pre_sale_start_date)

    year, month, day, hour, minute, second = map(int, match.groups())

    launch_date = datetime(year, month, day, hour, minute, second)

    today = datetime.now()
    difference = launch_date - today

    if 0 <= difference.days <= 30:
        #write_to_excel(data)
        print("The launch date is within 1 month from today.")
        return True
    else:
        print("The launch date is not within 1 month from today.")
        return False



def GetTokeninfo(driver,data):
    token_full_name=data['token']
    token_url=data['token_url']
    driver.execute_script(f"window.open('{token_url}', '_blank')")

    driver.switch_to.window(driver.window_handles[-1])
    try:
        chain_name_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'moontok-Text-root.moontok-1qael7q'))
        )

        # Once found, extract the text
        chain_name = chain_name_element.text
    except:
        chain_name=''
    try:

        #pre_sale_outer=driver.find_element(By.CLASS_NAME,'moontok-Stack-root.moontok-14ldasb')
        pre_sale=driver.find_elements(By.CLASS_NAME,'moontok-Text-root.moontok-shgsl0')[-2].text
        formated_presale_date=pre_sale.split(' ')
        pre_sale_start_date=formated_presale_date[0]+' '+formated_presale_date[1] 
    except:
        pre_sale_start_date=''
    if pre_sale_start_date:
        if launch_verifier(pre_sale_start_date):

            data={'token':token_full_name,
                'token_url':token_url,
                'chain_name':chain_name,
                'status':'presale',
                'upcoming_launch':pre_sale_start_date}
            write_to_excel(data)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])


def GetTokenFromPage(driver):
    try:
        tokens_data=[]
        time.sleep(4)
        tokens_Table_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'moontok-1v0ymcn')))
        tokens_tbody= WebDriverWait(tokens_Table_element, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, 'tbody')))
        #tokens_Table_element.find_element(By.TAG_NAME,'tbody')
        tokens_list=WebDriverWait(tokens_tbody, 5).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, 'tr')))
        #tokens_tbody.find_elements(By.TAG_NAME,'tr')
        for token in tokens_list:
            try:
                islive=token.find_element(By.CLASS_NAME,'moontok-h9iq4m.moontok-Badge-inner').text
            except:
                 islive=''
            if not islive=='LIVE':
                token_name_symbol=token.find_element(By.CLASS_NAME,'moontok-Text-root.moontok-t4ru65').text
                token_name=token.find_element(By.CLASS_NAME,'moontok-Text-root.coin-name.moontok-68dh1v').text
                token_full_name=token_name+' '+token_name_symbol
                token_url=token.find_element(By.CLASS_NAME,'moontok-1skw8o1').get_attribute('href')
                data={
                    'token':token_full_name,'token_url':token_url
                }

                tokens_data.append(data)
        for data in tokens_data:
            GetTokeninfo(driver,data)
        return True
    except Exception as e :
        print(f'Exception occured while fetching tokens {e}')
        return False

        






def Moontok():
    try:
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=chrome_options)
        driver.get('https://www.moontok.io/listings/presales')
        while True:

            if GetTokenFromPage(driver):
                pagination = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, 'moontok-1smpnji.moontok-Pagination-item'))
                )
                next_button=pagination[-1]
                next_button.click()
                is_disabled = next_button.get_attribute('aria-disabled') == 'true' or next_button.get_attribute('disabled') == 'true'

                if is_disabled:
                    print(f"The button is disabled.{driver.current_url}")

                    break
        driver.quit()
        return True
    except Exception as e:
        print(f'Error Occured in Moontok : {e}')
        return False


