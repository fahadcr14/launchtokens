
import requests
from datetime import datetime
from writexlsx import write_to_excel



def launch_verifier(launch_date):
    try:
        try:
            upcoming_launch_date = datetime.strptime(launch_date, '%Y-%m-%d %H:%M:%S')
        except:
            upcoming_launch_date = datetime.strptime(launch_date, '%Y-%m-%d %H:%M')

        today = datetime.now()
            
        difference = upcoming_launch_date - today

        if -1 <= difference.days <= 30:
            print("The launch date is within 1 month from today. ")
            return upcoming_launch_date.strftime('%d %B %Y %H:%M')
        else:
            print(f"The launch date is not within 1 month from today. {launch_date} difference {difference.days}")
            return False
    except Exception as e:
        print(f'Launch date {launch_date}   :::{e}')
        return False





def GetAllTokens():
    while True:
        try:
            # endpoint of api
            url = "https://api.cntoken.io/api/coin/uncoming"

            # payload for the api call
            payload = {
                "type": "14days",
                "offset": 0,
                "limit": 1000,
                "search": "",
                "sort": "",
                "order": ""
            }

            # setting headers to bypass cors and user agent to unblock restrcitions
            headers = {
                "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36",
                "Referer": "https://cntoken.io/",
                "Origin": "https://cntoken.io",
                "Accept": "application/json",
                "Sec-Fetch-Site": "same-site",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Dest": "empty",
                "Sec-Ch-Ua": '"Chromium";v="123", "Not:A-Brand";v="8"',
                "Sec-Ch-Ua-Mobile": "?1",
                "Sec-Ch-Ua-Platform": '"Android"',
            }

            response = requests.get(url, params=payload, headers=headers)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Print the response content (JSON data)
                return response.json()
            else:
                # Print an error message if the request was not successful
                print(f"Error: {response.status_code}")
                return False
        except Exception as e:
            print(f'Error occured when fetching cntokens {e}')





def WriteTokens():
    try:
        response=GetAllTokens()
        tokens_list=response['data']['rows']
        for token in tokens_list:
            try:
                token_name=token['name']
            except:
                token_name=''
            try:
                token_symbol=token['symbol']
            except:
                token_symbol=''
            try:    
                token_full_name=token_name+' '+token_symbol
            except:
                token_full_name=''
            try:
                chain_name=token['chain']['name']
            except:
                chain_name=''
            try:
                presale_date=token['presale_time']
            except:
                presale_date=''
            token_url='https://cntoken.io/coin/'+str(token['id'])
            if presale_date:
                presale_launch_date=launch_verifier(presale_date)
                if presale_launch_date:
                    data={
                        'token':token_full_name,
                        'token_url':token_url,
                        'chain_name':chain_name,
                        'status':'presale',
                        'upcoming_launch':presale_launch_date
                    }
                    print(data)
                    write_to_excel(data)
    except Exception as e:
        print(f'Error Occured WriteTokens() :{e}')



def Cointoken():
    if GetAllTokens():
        WriteTokens()
        return True


