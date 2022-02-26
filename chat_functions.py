""" this file contains all the functions related to the telegram bot. If you like to make any changes to
when the bots sends a message look at check_and_send_deal"""

import logging
import telegram
import utility_functions as ut

#enter your telegram bot token and the chat id here:
token = 'sampleToken'
chatID = 1234567

def send(message):
    # Enable logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )

    bot = telegram.Bot(token=token)
    bot.send_message(text=message, chat_id=chatID, parse_mode = telegram.ParseMode.MARKDOWN_V2)

def send_deal(card_type, price, card_fullname, link, shop_name, value):

    if value == 0:
        emote = '\U0001F680'
    elif value == 1:
        emote = '\U0001F680\U0001F680'
    elif value ==2:
        emote = '\U0001F680\U0001F48E\U0001F680'


    link = ut.create_reflink(link)
    text="""
------ *%s* ------ %s
%s
Bei: %s                  
                    
für *%.2f€*         
%s

je mehr \U0001F680's desto besser der
Deal   
----------------------------------
"""% (card_type, emote, card_fullname, shop_name, price, link)

    ## fix reserved character issue with markdown
    text = text.replace('.', '\.').replace('-', '\-').replace('+', '\+').replace('=', '\=').replace('<', '\<').replace('>', '\>').replace('(', '\(').replace(')','\)').replace('_','\c')

    print(text)

    send(text)

def check_and_send_deal(card_type):
    """checks if the deal is good by taking a look into the MySQL database"""

    weekly_average = ut.mysql_get_weekly(card_type)
    if weekly_average == -1:
        return 0

    value0_price = 0.82*weekly_average
    value1_price = 0.78*weekly_average
    value2_price = 0.75*weekly_average

    card_data = ut.mysql_get_deal(card_type)

    current_price = card_data[2]

    card_fullname = card_data[1]

    in_chat = ut.mysql_in_chat(card_type)

    #value 2
    if current_price <= value2_price and in_chat != 1:
        send_deal(card_type, current_price, card_fullname, card_data[3], card_data[4], 2)
    #value 1
    elif current_price <= value1_price and in_chat != 1:
        send_deal(card_type, current_price, card_fullname, card_data[3], card_data[4], 1)
    #value 0
    elif current_price <= value0_price and in_chat != 1:
        send_deal(card_type, current_price, card_fullname, card_data[3], card_data[4], 0)

    return 0