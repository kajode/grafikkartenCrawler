"""you can find most of the commonly used functions in here - it may be time to clean this file up using classes"""

import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup as bs
from mechanize import Browser
import re
from selenium_stealth import stealth
import mysql.connector
import zipfile
import random

base_path = ''

#add any unauthenticated proxies here
working_proxies = [
    '192.168.178.1:8080',
]

#add any authenticated proxies here
auth_proxies = [
    '192.168.178.1'
]

#enter further details for authenticated proxies here
PROXY_PORT = 12323 # port
PROXY_USER = 'username' # username
PROXY_PASS = 'password' # password

# add details for the MySQL Database here
mydb = mysql.connector.connect(
    host="localhost",
    user="username",
    password="password",
    database="example_database"
)

advertiser_list = {'alternate.de': 11731, 'notebooksbilliger.de': 11348}
publisher_id = 997083

def shop_get_fullname(shop):
    if shop == 'mdm' or shop == 'mediamarkt':
        return 'Media Markt'
    if shop == 'nbb':
        return 'Notebooksbilliger'
    if shop == 'alternate':
        return 'Alternate'
    if shop == 'caseking':
        return 'Caseking'
    else:
        return shop

def get_html(link):  ##opens website and returns html code
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'

    options = Options()
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('start-maximized')
    options.add_argument('--lang=de')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument(f'user-agent={user_agent}')


    browser = webdriver.Chrome(chrome_options=options)
    stealth(browser,
            languages=["de-de", "de"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    browser.get(link)

    ##wait for page to load and read it
    html = browser.page_source
    browser.delete_all_cookies()
    browser.close()


    return html

def get_html_proxy(link, proxy):  ##opens website and returns html code using proxies

    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
            },
            bypassList: ["localhost"]
            }
        };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (proxy, PROXY_PORT, PROXY_USER, PROXY_PASS)

    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    path = os.path.dirname(os.path.abspath(__file__))
    pluginfile = 'proxy_auth_plugin.zip'
    with zipfile.ZipFile(pluginfile, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)
    options = Options()
    options.add_extension(pluginfile)
    options.add_argument("--disable-dev-shm-usage")
    #options.add_argument('--headless')
    #options.add_argument('--proxy-server=%s' % proxy)
    options.add_argument('--no-sandbox')
    options.add_argument('start-maximized')
    options.add_argument('--lang=de')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument(f'user-agent={user_agent}')

    browser = webdriver.Chrome(os.path.join(path, 'chromedriver'), chrome_options=options)

    stealth(browser,
            languages=["de-de", "de"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    browser.get(link)

    ##wait for page to load and read it
    html = browser.page_source
    browser.delete_all_cookies()
    browser.close()


    return html


def get_soup(link):
    return bs(get_html(link), 'html.parser')

def get_soup_proxy(link):

    shuffel_proxies = auth_proxies
    random.shuffle(shuffel_proxies)

    for proxy in shuffel_proxies:
        print("trying proxy: %s" % str(proxy))
        try:
            html = get_html_proxy(link, proxy)
            if 'client has been blocked by bot protection' in html:
                continue
            result = bs(html, 'html.parser')
            return result
        except:
            pass


def get_html_fast(link):
    short_link = re.findall("^https://.*\..{2,3}/", link)[0]
    b = Browser()
    b.set_handle_robots(False)
    b.set_handle_referer(True)
    b.set_handle_refresh(True)
    b.addheaders = [
        ('Referer', short_link),
        ('sec-fetch-dest', 'empty'),
        ('accept-language', 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7'),
        ('sec-fetch-site', 'cross-site'),
        ('sec-fetch-mode', 'cors'),
        ('accept', '*/*'),
        ('origin', short_link),
        ('sec-ch-ua-platform','"macOS"'),
        ('user-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'),
        ('sec-ch-ua', '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"'),
    ]
    if 'notebooksbilliger.de' in link:
        b.addheaders.append(('authority', 'async-px-eu.dynamicyield.com'))
    b.open(link)

     #assert

    html = b.response().read()

    return html

def get_soup_fast(link):
    return bs(get_html_fast(link), 'html.parser')


def write_price(card_type, card_price):
    path = base_path+'price_history/'+card_type.replace(' ', '_')

    # create file if it doesnt exist
    if not os.path.exists(path):
        open(path, "x")

    file = open(path, 'a')
    content = str(card_price) + '|' + str(time.time()) + '\n'
    file.write(content)
    file.close()

def read_prices(card_type):
    path = base_path + 'price_history/' + card_type.replace(' ', '_')

    # skip file if it doesnt exist
    if not os.path.exists(path):
        return -1

    file = open(path, 'r')
    prices = file.readlines()
    file.close()

    return prices

def add_link(shop_name, type, link):

    file_name = shop_name + '_' + type.replace(' ', '_')
    path = base_path + shop_name + '/' + file_name

    if os.path.exists(path):
        file = open(path, "r+")
        for line in file:
            if line.replace('\n', '') == link:
                return 0
        file.close()

    if not os.path.exists(path):
        open(path, 'x')

    file = open(path, "a+")
    try:
        file.write(link + '\n')
    except:
        print("Error adding %s to link list" % link)
    file.close()
    return 1

def read_links(shop_name, type):

    file_name = shop_name + '_' + type.replace(' ', '_')
    path = base_path + shop_name + '/' + file_name

    # return error if file doesnt exist
    if not os.path.exists(path):
        return []

    file = open(path, "r+")
    links = file.readlines()

    return links

def read_weekly_average(card_type):
    prices = read_prices(card_type)

    #ensure file exists
    if prices == -1:
        return -1

    total_price = 0
    divider = 0
    for raw_price in prices:
        raw_price = raw_price.split('|')
        price = float(raw_price[0])
        date = float(raw_price[1])

        #make sure data is not older than a week
        if time.time() - date > 60*60*24*7:
            continue

        total_price += price
        divider += 1
    try:
        div  = total_price / divider
        return div
    except:
        return 0


def mysql_dropall():

    mycursor = mydb.cursor()

    sql = "DELETE FROM deals WHERE card_type='*'"

    mycursor.execute(sql)

    mydb.commit()

    print(mycursor.rowcount, "record(s) deleted")

def mysql_get_weekly(card_type):
    mycursor = mydb.cursor()

    sql = "SELECT * FROM grafikkarten WHERE card_type='%s'AND timestamp > CURDATE() - INTERVAL 7 DAY"  % card_type
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    if len(myresult) == 0:
        return -1

    #calculate average
    counter = 0
    for card in myresult:
        counter +=card[1]
    average = counter/len(myresult)

    return average

def mysql_in_chat(card_type):
    mycursor = mydb.cursor()
    sql = "SELECT in_chat FROM deals WHERE card_type='%s'" % card_type
    mycursor.execute(sql)
    myresult = mycursor.fetchall()


    #if not in chat change to in chat
    sql = "UPDATE deals SET in_chat=1 WHERE card_type='%s'" % card_type
    mycursor.execute(sql)
    mydb.commit()
    return myresult[0][0]

def mysql_get_deal(card_type):
    mycursor = mydb.cursor()
    sql = "SELECT * FROM deals WHERE card_type='%s'" % card_type
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult[0]


def mysql_update(card_type, card_price, link, shop, card_fullname):

    link = create_reflink(link)
    card_price = float(card_price)

    mycursor = mydb.cursor()

    sql = "SELECT * FROM deals WHERE card_type='%s'" % card_type
    mycursor.execute(sql)
    myresult = mycursor.fetchall()


    if len(myresult) == 0:
        # add row if it doesnt exist
        sql = "INSERT INTO deals (card_type, card_fullname, price, link, shop, in_chat) VALUES ('%s', '%s', '%s', '%s', '%s', 0)" % (card_type, card_fullname, card_price, link, shop_get_fullname(shop))
    else:
        #update the card if not written already
        if myresult[0][2] == card_price and myresult[0][3] == link:
            sql = "UPDATE deals SET price = '%.2f', shop = '%s', link = '%s' WHERE card_type = '%s'" % (card_price, shop_get_fullname(shop), link, card_type)
        else:
            sql = "UPDATE deals SET price = '%.2f', shop = '%s', link = '%s', in_chat = 0, card_fullname = '%s' WHERE card_type = '%s'" % (card_price, shop_get_fullname(shop), link, card_fullname, card_type)
    mycursor.execute(sql)
    mydb.commit()
    print(mycursor.rowcount,"card(s) updated or added")
 
def mysql_add(card_type, card_price, link, shop):

    card_price = float(card_price)

    mycursor = mydb.cursor()

    # add row if it doesnt exist
    sql = "INSERT INTO grafikkarten (card_type, price, link, shop) VALUES ('%s', '%s', '%s', '%s')" % (card_type, card_price, link, shop_get_fullname(shop))


    mycursor.execute(sql)
    mydb.commit()
    print(mycursor.rowcount,"card added to histroy")

def mysql_add_to_temp(card_type, card_price, link, shop, card_fullname):

    card_price = float(card_price)

    mycursor = mydb.cursor()

    # add row if it doesnt exist
    sql = "INSERT INTO temp (card_type, card_fullname, price, link, shop) VALUES ('%s', '%s', '%s', '%s', '%s')" % (card_type, card_fullname, card_price, link, shop_get_fullname(shop))


    mycursor.execute(sql)
    mydb.commit()
    print(mycursor.rowcount,"card added to temp")

def mysql_update_deals(card_type):
    """reads data for specific card_type from temp table and updates deals table with best deal"""

    #get deal with best price
    mycursor = mydb.cursor()
    sql = "select * from temp where card_type='%s' order by price ASC limit 1"  % card_type
    mycursor.execute(sql)
    result = mycursor.fetchall()

    #skip if list is empty
    if len(result) == 0:
        return 0

    result = result[0]
    card_fullname = result[1]
    price = result[2]
    shop = result[3]
    link = result[4]

    print(result)
    #change best deal
    mysql_update(card_type, price, link, shop, card_fullname)


    #drop all rows with matching card type
    sql = "delete from temp where card_type = '%s'" % card_type
    mycursor.execute(sql)
    mydb.commit()


def create_reflink(link):
    """this function may be used to create a refferal link"""
    return link
