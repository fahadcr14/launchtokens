
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

import time
from writexlsx import write_to_excel


def launch_verifier(launch_date):
    try:
        upcoming_launch_date = datetime.strptime(launch_date, '%d %B, %Y')

        today = datetime.now()
            
        today = datetime.now()
        difference = upcoming_launch_date - today

        if 0 <= difference.days <= 30:
            print("The launch date is within 1 month from today.")
            return upcoming_launch_date.strftime('%d %B %Y')
        else:
            print("The launch date is not within 1 month from today.")
            return False
    except :
        return False
    



    
def GetAllCoins(driver):
    global tokens_urls,offset
    total_coins=0
    while True:
        if offset>16810:
            break
        try:
            coins_cards=WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'singlecoinlink.views_pages_all-time-best-ajax'))
        )
            #driver.find_elements(By.CLASS_NAME,'singlecoinlink.views_pages_all-time-best-ajax')
            for coin in coins_cards[offset:]:
                driver.execute_script("arguments[0].scrollIntoView();", coin)

                days=coin.find_element(By.CLASS_NAME,'days').text
                #print(days)
                if days.startswith('Launch'):
                    token_url=coin.get_attribute('data-href')
                    tokens_urls.append(token_url)
                total_coins+=1
            offset=len(coins_cards)
            print(f'Total coins {total_coins} Urls added:{len(tokens_urls)}')

            load_more=load_more = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'auto-load_.text-center'))
            )
            if load_more.text.startswith("We don't have more data to display"):
                break
            if load_more:
                driver.execute_script("arguments[0].scrollIntoView();", load_more)
                load_more.click()
            else:
                break
        except:
            pass
        



def GetTokeninfo(driver,token_url):
    driver.get(token_url)
    try:
        token_name=WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'mb-0'))
        )
        token_symbol=driver.find_element(By.CLASS_NAME,'h4.text-muted.mb-4')
        token_full_name=token_name.text+' $'+token_symbol.text

    except:
        token_full_name=''
    try:
        chain_name=driver.find_element(By.CLASS_NAME,'col-4.mb-2').text
    except:
        chain_name=''
    try:
        launch_date=WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/section/div[2]/div[2]/div[3]/div[1]/div[3]/p[2]'))
        ).text
    except:
        launch_date=''
    if launch_date:
        upcoming_launch_date=launch_verifier(launch_date)
        if upcoming_launch_date:
            data={
                'token':token_full_name,
                'token_url':token_url,
                'chain_name':chain_name,
                'status':'upcoming',
                'upcoming_launch':upcoming_launch_date
            }
            #print(data)
            write_to_excel(data)
            return True

tokens_urls=[]
offset=0
def Gemfind():
    try:
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=chrome_options)
        driver.get('https://gemfinder.cc/')
        
        
        time.sleep(5)
        alltimebutton=driver.find_element(By.XPATH,'/html/body/section/div[3]/ul/li[1]/a')
        if alltimebutton:
            driver.execute_script("arguments[0].scrollIntoView();", alltimebutton)
            alltimebutton.click()
        time.sleep(5)
        GetAllCoins(driver)
        for url in tokens_urls:
            GetTokeninfo(driver,url)
        driver.quit()
        return True
    except Exception as e:
        print(f'Error Occured in Gemfind :{e}')
        return False


Gemfind()