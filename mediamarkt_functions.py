import utility_functions as ut

shop_name = 'mediamarkt'

def get_cards_html():
    cards_html = []

    #repeat for all pages
    for i in range(1,10):

        # parse website and extract all cards
        soup = ut.get_soup_proxy("https://www.mediamarkt.de/de/category/grafikkarten-4560.html?page="+str(i))
        cards_list = soup.find('div', attrs={"data-test": "mms-search-srp-productlist"})
        l_cards_html = cards_list.find_all('div',attrs={"data-test": "mms-search-srp-productlist-item"})

        for l_card_html in l_cards_html:
            cards_html.append(l_card_html)

    return cards_html


def find_card(card_types):

    cards_html = get_cards_html()

    for card_html in cards_html:
        card_fullname = card_html.find('h2', attrs={"data-test": "product-title"}).text
        card_link = 'https://www.mediamarkt.de' + card_html.find('a', attrs={"data-test": "mms-router-link"})['href']

        #remove ® and ™ from card name
        card_fullname = card_fullname.replace('™','').replace('®','')

        print(card_fullname)

        #check if the card is looked for and add it to list
        for card_type in card_types:
            if card_type+' Ti' in card_fullname:
                ut.add_link(shop_name, card_type+' Ti', card_link)
            elif card_type+' XT' in card_fullname:
                print('adding to list')
                ut.add_link(shop_name, card_type+' XT', card_link)
            elif card_type in card_fullname:
                print('adding to list')
                ut.add_link(shop_name, card_type, card_link)

def check_price(card_type):

    links = ut.read_links(shop_name, card_type)
    deals = []
    minprice  = ''

    print(links)
    for link in links:

        #load website
        soup = ut.get_soup_proxy(link)

        #check if availible
        status = soup.find('span', class_='StyledAvailabilityTypo-sc-901vi5-7')
        if 'Leider keine Lieferung möglich' in status:
            print('not in stock\n')
            continue

        card_price = float(soup.find('span', class_='ScreenreaderTextSpan-sc-11hj9ix-0').text.replace('undefined ',''))
        try:
            card_fullname = soup.find('h1', class_='StyledInfoTypo-sc-1jga2g7-0').text.replace('"','')
        except:
            card_fullname = soup.find('h1', class_='StyledInfoTypo-sc-1jga2g7-1').text.replace('"','')

        #save price in history
        ut.write_price(card_type, card_price)
        ut.mysql_add_to_temp(card_type, card_price, link, shop_name, card_fullname)

    return deals



