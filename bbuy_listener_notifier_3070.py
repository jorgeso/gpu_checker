import winsound
import time
from bs4 import BeautifulSoup
import requests
from twilio.rest import Client
import webbrowser
import os

def signal():
    for _ in range(2000):
        for i in range(1, 10):
            winsound.Beep(i * 100, 200)
        time.sleep(.05)
    print('done')

def send_text(url):
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    client = Client(account_sid, auth_token)
    client.messages \
        .create(
            body=f'3070 {url}',
            from_=os.getenv('TWILIO_PHONE'),
            to='+18888888'
        )
    print('text message sent!')

def send_no_button_text(url):
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
            body=f'3070 no button {url}',
            from_=os.getenv('TWILIO_PHONE'),
            to='+18888888'
        )

def check(url):
    print('still checking for you master.')
    try:
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
        }

        cookies = {
            'locDestZip': '20874'
        }

        response = requests.get(url, headers=headers, cookies=cookies)

        soup = BeautifulSoup(response.text, 'html.parser')

        sku = "6429442"

        button = soup.find('button', attrs={"data-sku-id":sku})
        
        if button is None:
            print('no button found')
            send_no_button_text(url)
            return True
        else:
            print(button.getText())

        if 'disabled' not in button.attrs.keys():
            send_text(url)
            webbrowser.open(url)
            print(url)
            signal()
            print('GPU available. Process over.')
            return False
        
        return True
        
    except requests.exceptions.ConnectionError as e:
        print('there was an error')
        time.sleep(15)
        return True

def start_process():
    url = 'https://www.bestbuy.com/site/nvidia-geforce-rtx-3070-8gb-gddr6-pci-express-4-0-graphics-card-dark-platinum-and-black/6429442.p?skuId=6429442'

    keep_checking = True
    instance = 1
    while keep_checking:
        print(instance)
        keep_checking = check(url)
        instance += 1
        time.sleep(1)

if __name__ == '__main__':
    start_process()