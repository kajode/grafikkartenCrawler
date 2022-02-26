import requests
from mechanize import Browser
from bs4 import BeautifulSoup as bs
import utility_functions as ut

shop_name = "alternate"

def find_card(card_types):

    headers = requests.utils.default_headers()
    headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    })

    for card_type in card_types:
        link = 'https://www.alternate.de/Grafikkarten/'+card_type.replace(' ', '-').replace('Ti', 'TI')
        try:
            print(link)
            soup = ut.get_soup_fast(link)
        except:
            print('error parsing %s' % link)
            continue

        # get html list of cards
        cards_list = soup.find('div', class_='grid-container listing')
        cards_html = cards_list.find_all('a', class_='card')

        # select card from list and find link
        for card_html in cards_html:
            link = card_html.get('href')
            ut.add_link(shop_name, card_type, link)

def check_price(card_type):

    b = Browser()
    b.set_handle_robots(False)
    b.set_handle_referer(True)
    b.set_handle_refresh(True)
    b.addheaders = [
        ('Referer', 'https://www.alternate.de/'),
        ('sec-fetch-dest', 'empty'),
        ('accept-language', 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7'),
        ('sec-fetch-site', 'cross-site'),
        ('sec-fetch-mode', 'cors'),
        ('accept', '*/*'),
        ('sec-ch-ua-platform','"macOS"'),
        ('origin', 'https://www.alternate.de'),
        ('user-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'),
        ('sec-ch-ua', '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"'),
    ]

    shop_name = "alternate"

    links = ut.read_links(shop_name, card_type)

    #assert file exists
    if links == -1:
        return []

    for link in links:
        b.open(link)

        print(link)

        #assert page loads
        response_code = b.response().code
        if response_code != 200:
            print("-- page failed to load -- Code: %s\n" % response_code)
            continue

        # Parsing the HTML
        soup = bs(b.response().read(), 'html.parser')

        header = soup.find('h1').text

        if header == 'Der Artikel ist zur Zeit leider nicht verfügbar.':
            continue
        else:
            card_fullname = header

        card_price = float(soup.find('div', class_='price').find('span').text.replace('€', '').replace(' ', '').replace('.', '').replace(',','.'))


        link = ut.create_reflink(link.replace('\n', ''))

        # save price in history
        ut.mysql_add(card_type, card_price, link, shop_name)
        #save price to temp table for later adding it to deals
        ut.mysql_add_to_temp(card_type, card_price, link, shop_name, card_fullname)

    return 0

