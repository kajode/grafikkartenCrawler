import alternate_functions as alternate
import mediamarkt_functions
import nbb_functions as nbb
import chat_functions as chat


#vars
import utility_functions

type = 0
price = 1
fullname = 2
link = 3

#card that should be recorded
cards = [
    "GTX 1650",
    "GTX 1660",
    "RTX 2060",
    "RTX 2070",
    "RTX 2080",
    "RTX 3060",
    "RTX 3060 Ti",
    "RTX 3070",
    "RTX 3070 Ti",
    "RTX 3080",
    "RTX 3080 Ti",
    "RTX 3090",
    "RX 6600",
    "RX 6600 XT",
    "RX 6700",
    "RX 6700 XT",
    "RX 6800",
    "RX 6800 XT",
    "RX 6900",
    "RX 6900 XT"
]
'''
alternate.find_card(cards)
ck.find_card(cards)
mdm.find_card(cards)
'''


#fill up links
nbb.find_card(cards)
alternate.find_card(cards)

## experimental feature
try:
    mediamarkt_functions.find_card(cards)
except:
    pass

#update deals
for card_type in cards:
    print(card_type)
    nbb.check_price(card_type)
    alternate.check_price(card_type)

    ## experimental feature
    try:
        mediamarkt_functions.check_price(card_type)
    except:
        pass

    ## experimental feature
    try:
        mediamarkt_functions.check_price(card_type)
    except:
        pass

    #finshing touches
    utility_functions.mysql_update_deals(card_type)
    chat.check_and_send_deal(card_type)