
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time
import re
from writexlsx import write_to_excel


def launch_verifier(pre_sale_start_date):
    date_pattern = re.compile(r'(\d{4})/(\d{2})/(\d{2})')

    match = date_pattern.match(pre_sale_start_date)
    if match:
        year, month, day = map(int, match.groups())

        launch_date = datetime(year, month, day)

        today = datetime.now()
        difference = launch_date - today

        if 0 <= difference.days <= 30:
            #write_to_excel(data)
            print("The launch date is within 1 month from today.")
            return launch_date.strftime('%d %B %Y')
        else:
            print("The launch date is not within 1 month from today.")
            return False
    else:
        print(f'date format not matched')
        return False






def GetTokeninfo(driver,token_url):
    driver.execute_script(f"window.open('{token_url}', '_blank')")

    driver.switch_to.window(driver.window_handles[-1])

    try:
        token_parent_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'flex.items-start.gap-5'))
        )
        token_name=token_parent_element.text.replace('\n',' $')
    except:
        token_name=''

    try:
        chain_element = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/div/div[1]/div[1]/div[5]/div[1]')
        chain_name = chain_element.text.strip().replace(':','')
    except:
        chain_name=''
    try:
        launch_date=driver.find_element(By.XPATH,'//*[@id="__next"]/div/main/div/div[1]/div[1]/div[4]/div[2]').text
        formatted_launch_date=launch_date.replace('-','/')
    except:
        formatted_launch_date=''
    presale_date=launch_verifier(formatted_launch_date)
    if presale_date:
        data={
            'token':token_name,
            'token_url':token_url,
            'chain_name':chain_name,
            'status':'presale',
            'upcoming_launch':presale_date
        }
        write_to_excel(data)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])


def Tokens(driver):
    #try:
        token_urls=[]
        tokensTable=WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/main/section[5]/div[2]/table'))
        )
        tokens_tbody=tokensTable.find_element(By.TAG_NAME,'tbody')
        tokens_list=tokens_tbody.find_elements(By.TAG_NAME,'tr')
        for token in tokens_list:
            token_a_tag=token.find_element(By.TAG_NAME,'a')
            token_url=token_a_tag.get_attribute('href')
            token_urls.append(token_url)
        for token_url in token_urls:
            GetTokeninfo(driver,token_url)
    #except Exception as e:
    #    print(f'Error fetching tokens from coinmooner {e}')





def Coinmooner():
    try:
        
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=chrome_options)
        driver.get('https://coinmooner.com/')
        try:
            driver.find_element(By.XPATH,'//*[@id="__next"]/div/button[1]').click()
        except:
            pass
        filter_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#__next > main > section.mb-5.w-full > div.mb-3.mt-2.grid.w-full.grid-cols-2.lg\:grid-cols-3.lg\:grid-cols-\[110px_1fr_138px\] > button'))
        )
        driver.execute_script("arguments[0].scrollIntoView();", filter_button)

        filter_button.click()   
        time.sleep(3)
        presale_button=driver.find_element(By.XPATH,'//*[@id="__next"]/main/section[5]/div[1]/div[2]/button[3]').click()
        time.sleep(5)
        while True:
            driver.execute_script("arguments[0].scrollIntoView();", filter_button)

            Tokens(driver)
            next_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/main/section[5]/div[4]/div[2]/button[2]'))
            )
            driver.execute_script("arguments[0].scrollIntoView();", next_button)

            next_button.click()
            time.sleep(5)
            is_disabled =  next_button.get_attribute('disabled') == 'true'

            if is_disabled:
                print(f"ALl done {driver.current_url}")
                break
        driver.quit()
        return True
    except Exception as e:
        print(f'Error Occured in Coinmooner :{e}')
        return False








