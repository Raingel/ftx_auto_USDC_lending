
# coding: utf-8

# In[1]:
import sys
import logging
import math
import urllib
import schedule
import time
from datetime import datetime, timedelta
from FTX.client import Client


# In[21]:


def now_time():
	return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
def calc_year_rate(f):
    return ((1+f)**24)**365
def lending(client, coin, rate):
    try:
        balance = client.get_private_wallet_single_balance(coin)['total']
        # client.set_private_margin_lending_offer('USD', usd_available, 2.283e-05)
        client.set_private_margin_lending_offer(coin, balance, rate)
        last_proceeds_time = (datetime.strptime(client.get_lending_history(coin)['time'],'%Y-%m-%dT%H:%M:%S+00:00')+timedelta(hours=8)).strftime('%Y-%m-%dT%H:%M:%S')    
        proceeds = client.get_lending_history(coin)['proceeds']
        last_rate = client.get_lending_history(coin)['rate']*100
        last_year_rate = (calc_year_rate(client.get_lending_history(coin)['rate'])-1)*100
        print (">>{} 現有{}總值：: {}, 設定利率: {}, 前次收利時間{}, 前次收利總額為{:f}, 前次時/年化報酬率為{:f}%/{:.2f}%".format(now_time(), coin, balance, rate, last_proceeds_time, proceeds, last_rate, last_year_rate)) 
    except:
        print ('>>{} 獲取過去資訊失敗'.format(now_time()))
        


# In[23]:



logging.basicConfig(
    handlers=[logging.StreamHandler(
        sys.stdout), logging.FileHandler('log.txt')],
    level=logging.INFO,
    format='[%(asctime)s %(levelname)-8s] %(message)s',
    datefmt='%Y%m%d %H:%M:%S',
)
INPUT_YOUR_API_KEY1 = input('請輸入API金鑰(公鑰): ')
INPUT_YOUR_API_SECRET1 = input('請輸入API金鑰(私鑰): ')
INPUT_YOUR_SUBACCOUNT_NAME1 = input('請輸入子帳戶名稱(若無可留空): ')
client = Client(INPUT_YOUR_API_KEY1, INPUT_YOUR_API_SECRET1,
                INPUT_YOUR_SUBACCOUNT_NAME1)
coin_input = input('請輸入貸出幣種(可輸入多個幣種，以半形逗號分隔，如：「USD,USDT」」。若留空，預設為USDT): ')

if not coin_input:
    #print ('使用預設幣種USDT')
    coin_list=['USDT']
else:
    coin_list=coin_input.split(',')

print ('>>貸出的幣種為：', coin_list)

rate = input('請設定利率(若留空，預設為0.000001): ')
if not rate:
    print ('>>使用預設利率0.000001')
    rate=0.000001


# In[24]:


print ('####################')
print ('>>純液男借金程式 rev 210406')
print ('>>投資一定有風險，投資有賺有賠，投資前請詳閱公開說明書。')
for coin in coin_list:
    try:
        last_proceeds_time=(datetime.strptime(client.get_lending_history(coin)['time'],'%Y-%m-%dT%H:%M:%S+00:00')+timedelta(hours=8)).strftime('%Y-%m-%dT%H:%M:%S')
        print ('======幣種:{}======'.format(coin))
        print ('>>近24小時{}幣種借金額交易量: {}'.format(coin,client.get_daily_borrowed_amounts(coin)))
        print ('>>現有{}總值：{}'.format (coin, client.get_private_wallet_single_balance(coin)['total']))
        print ('>>前次收利時間為{}'.format(last_proceeds_time))
        print ('>>前次收利總額為{0:f}'.format(client.get_lending_history(coin)['proceeds']))
        print ('>>前次時報酬率為{0:f}%'.format(client.get_lending_history(coin)['rate']*100))
        print ('>>前次年化複利報酬率為{0:.2f}%'.format((calc_year_rate(client.get_lending_history(coin)['rate'])-1)*100))
    except:
        print ('======幣種:{}======'.format(coin))
        print ('獲取過去資訊失敗')
print ('####################')


# In[25]:


print (">>開始自動全投入借金")
for coin in coin_list:
    lending(client, coin, rate)


# In[ ]:


for coin in coin_list:
    schedule.every().hour.at(":50").do(lending, client, coin, rate)
# schedule.every(0.1).minutes.do(lending, client)
while True:
    schedule.run_pending()
    time.sleep(1)

