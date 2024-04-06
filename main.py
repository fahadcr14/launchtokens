from coinvotecc import Coinvote
from cntokens import Cointoken
from coinmooner import Coinmooner
from coinscope import CoinScope
from coinsgod import CoinGod
from coinsniper import Coinsniper
from freshcoins import Freshcoins
from gemfind import Gemfind
from moontok import Moontok
from coinalpha import CoinALPHA

if __name__=="__main__":
    while True:
        if Coinvote():
            print(f'Coinvote is Finished')
            
        if Cointoken():
            print(f'Cointoken is Finished')
        if Coinmooner():
            print(f'Coinmooner is Finished')
        if CoinScope():
            print(f'CoinScope is Finished')
        if CoinGod():
            print(f'CoinGod is Finished')
        if Coinsniper():
            print(f'Coinsniper is Finished')
        if Freshcoins():
            print(f'Freshcoins is Finished')
        if Gemfind():
            print(f'Gemfind is Finished')
        if Moontok():
            print(f'Moontok is Finished')
        if CoinALPHA():
            print(f'CoinALPHA is Finished')
