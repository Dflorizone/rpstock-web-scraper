import requests
from bs4 import BeautifulSoup
import os
import time

def rp_stock():
    gb = (1,2,4)
    ada_prod = (4295, 4292, 4296)
    ck_prod = ('', '-2gb', '-4gb')
    no_stock = 'Out of stock'

    def telebot(text):
        token = os.environ.get('python_rp_stock_bot_token')
        userID = os.environ.get('telegram_user_id')
        url = f'https://api.telegram.org/bot{token}/sendMessage'
        data = {"chat_id": userID, "text": text, "parse_mode": "markdown"}
        requests.post(url, data)

    for x in range(3):
        version = gb[x]
        prod_num = ada_prod[x]
        model = ck_prod[x]
        r_ps = requests.get(f'https://www.pishop.ca/product/raspberry-pi-4-model-b-{version}gb/') # pishop response
        r_ada = requests.get('https://www.adafruit.com/product/4295') # adafruit response
        r_ck = requests.get(f'https://www.canakit.com/raspberry-pi-4{model}.html') # canakit response
        html_ps = r_ps.text
        html_ada = r_ada.text
        html_ck = r_ck.text
        soup_ps = BeautifulSoup(html_ps, 'html.parser')
        soup_ada = BeautifulSoup(html_ada, 'html.parser')
        soup_ck = BeautifulSoup(html_ck, 'html.parser')
        tag_ps = soup_ps.find('div', class_="form-action")
        tag_ada = soup_ada.find('a', href=f'/product/{prod_num}')
        tag_ck = soup_ck.find('div', id='ProductAddToCartDiv')
        result_ps = str(tag_ps.contents[1])
        result_ada = str(tag_ada.contents)
        result_ck = str(tag_ck.contents)

        if no_stock not in result_ps:
            text = 'Raspberry pi ' + str(gb[x]) + f' are in stock at PiShop! Click this link! [URL](https://www.pishop.ca/product/raspberry-pi-4-model-b-{version}gb/)'
            telebot(text)

        if no_stock not in result_ada:
            text = 'Raspberry pi ' + str(gb[x]) + ' are in stock at Adafruit! Click this link! [URL](https://www.adafruit.com/product/4295)'
            telebot(text)


        if 'Sold Out' not in result_ck:
            text = 'Raspberry pi ' + str(gb[x]) + f' are in stock at Canakit! Click this link! [URL](https://www.canakit.com/raspberry-pi-4{model}.html)'
            telebot(text)


while True:
    rp_stock()
    time.sleep(300)
    print('5 min has passed')









