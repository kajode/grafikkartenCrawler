import utility_functions as ut

shop_name = 'nbb'

def get_cards_html():

    links = [
        'https://www.notebooksbilliger.de/pc+hardware/grafikkarten+pc+hardware/amdati/page/1?perPage=2000',
        'https://www.notebooksbilliger.de/pc+hardware/grafikkarten/nvidia/page/1?perPage=2000'

    ]

    cards_html = []

    for link in links:
        try:
            soup = ut.get_soup_proxy(link)
        except:
            print('error parsing %s' % link)
            continue

        # get html list of cards
        cards_list = soup.find('div', class_='listing_main')
        l_cards_html = cards_list.find_all('div', class_='js-ado-product-click')

        for l_card_html in l_cards_html:
            cards_html.append(l_card_html)

    return cards_html

def find_card(card_types):

    cards_html = get_cards_html()

    for card_type in card_types:
        for card_html in cards_html:
            card_title = card_html.find('a', class_='listing_product_title').text
            link = card_html.find(class_='listing_product_title', href=True)['href']

            if card_type+' Ti' in card_title:
                ut.add_link(shop_name, card_type+' Ti', link)
            elif card_type+' XT' in card_title:
                ut.add_link(shop_name, card_type+' XT', link)
            elif card_type in card_title:
                ut.add_link(shop_name, card_type, link)

def check_price(card_type): #checks the price for all links to that card and retruns matrix with 0 = link 1 = price

    #get links from file
    links = ut.read_links(shop_name, card_type)

    #assert file exists
    if links == -1:
        return []

    #open shop website
    for link in links:
        soup = ''
        for i in range(0,2):
            #get parsed website
            try:
                print(link)
                soup = ut.get_soup_proxy(link)
                break
            except:
                print('error parsing %s' % link)
                pass

        #assert product is availible
        if len(soup.find_all('div', id='product_error')) != 0:
            continue

        #assert product is not sold out
        availibility_html = soup.find('div', class_='availability_widget')
        if 'soldOut' in str(availibility_html):
            print('Sold Out')
            continue

        quantity_wrapper = soup.find('div', id="product_detail_price")
        card_price = float(quantity_wrapper.find('span', class_='product-price__regular js-product-price').text.replace(' €','').replace('.','').replace('\n', '').replace(' ','').replace(',','.'))
        card_fullname = soup.find('h1', class_='name').text.replace('\n', '').replace('  ', '')

        #save price in history
        ut.write_price(card_type, card_price)
        ut.mysql_add_to_temp(card_type, card_price, link, shop_name, card_fullname)

    return 0