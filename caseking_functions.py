import utility_functions as ut

shop_name = 'caseking'

def find_card(cards):
    for card in cards:
        card_type = card[0]

        #generate link
        if "RX" in card_type:
            link = "https://www.caseking.de/pc-komponenten/grafikkarten/amd/radeon-" + card_type.replace(' ', '-') + "?sTemplate=table4&sPage=1&sPerPage=48"
        else:
            link = "https://www.caseking.de/pc-komponenten/grafikkarten/nvidia/geforce-" + card_type.replace(' ', '-') + "?sTemplate=table4&sPage=1&sPerPage=48"

        try:
            print(link)
            soup = ut.get_soup(link)
        except:
            print("error parsing %s" % link)
            continue

        #find cards
        cards_list_html = soup.find('div', class_='ck_listing')

        #check if there are cards and if so carry on
        try:
            cards_html = cards_list_html.find_all('div', class_="artbox")
        except:
            print('no cards listed under %s' % link)
            continue


        for card_html in cards_html:
            try:
                card_link = card_html.find('a', class_='producttitles', href=True)['href']
            except:
                continue

            ut.add_link(shop_name, card_type, card_link)

def check_price(card):
    card_type = card[0]
    card_max_price = 0.9*ut.read_weekly_average(card_type)
    card_deals = []

    links = ut.read_links(shop_name, card_type)

    for link in links:
        try:
            print(link)
            soup = ut.get_soup(link)
        except:
            print("error parsing %s" % link)
            continue

        #check if availible
        availability = soup.find('meta', attrs={'itemprop': 'availability'})['content']
        if 'InStock' not in availability:
            print('card not available')
            continue

        card_price = float(soup.find('meta', attrs={'itemprop': 'price'})['content'])
        card_fullname = soup.find('meta', attrs={'itemprop': 'name'})['content']
        ut.write_price(card_type, card_price)
        if card_price <= card_max_price:
            card_deals.append([card_type, card_price, card_fullname, link.replace('\n', ''), shop_name])

    return card_deals