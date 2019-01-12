from typing import List
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater,MessageHandler,CommandHandler,RegexHandler,CallbackQueryHandler
import random
import logging
from telegram.error import (TelegramError, Unauthorized, BadRequest,TimedOut, ChatMigrated, NetworkError)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='logging.txt',
                    level=logging.INFO)

logger = logging.getLogger(__name__)



card_market = ['village','witch','silver','gold']
card = ["copper","silver","gold"]
deckplayer1 = ['copper','copper','copper','copper','copper','copper','copper','estates','estates','estates']
deckplayer2 = ['copper','copper','copper','copper','copper','copper','copper','estates','estates','estates']
deckplayer3 =['copper','copper','copper','copper','copper','copper','copper','estates','estates','estates']
grave = []
grave2 = []
grave3 = []
buy_temp = []
hand = []
hand2 = []
hand3 = []
temp_deck_top=[]
temp_deck_top2 = []
temp_deck_top3 = []
gold = 0
points = 0
points2 = 0
points3 = 0
turn = False
buy_turn = False
buy_time = 1
action = 1
user1_id = 'null'
user2_id = 'null'
user3_id = 'null'
user1_name = 'null'
user2_name = 'null'
user3_name = 'null'
user1_tag = 'null'
user2_tag = 'null'
user3_tag = 'null'
current_player = 1
courtyard_temp = 0
inlinehand=[]
turn_count=0
turnnum = 0
start_game=False

def start(bot,update):
    global turn_count
    global turnnum
    global start_game
    start_game = True
    update.message.reply_text("Loby is closed\n" + str(user1_name) + ' is drawing.\nType /draw.')
    turn_count = 1
    turnnum = 1
    return(turn_count,turnnum)


def button(bot,update):
    global deckplayer1,deckplayer2,deckplayer3
    global grave,grave2,grave3
    global temp_deck_top,temp_deck_top2,temp_deck_top3
    global action
    global gold
    global buy_temp
    global buy_time
    query = update.callback_query
    if query.data == 'silver':
        if (buy_turn == True) and (gold - 3 >= 0):
            buy_temp.append('silver')
            gold -= 3
            buy_time -= 1
            query.edit_message_text('You have bought Silver.\nType /buy to continue buying cards\nType /use to use cards\nType ( /end ) to finish buying.')
        else:
            query.message.reply_text('You dont have enough gold or it is not your turn.')
    if query.data=='Witch':
        if (buy_turn == True) and (gold - 5 >= 0):
            buy_temp.append('Witch')
            gold -= 3
            buy_time -= 1
            query.edit_message_text('You have bought Witch .\nType /buy to continue buying cards\nType /use to use cards\nType ( /end ) to finish buying.')
        else:
            query.message.reply_text('You dont have enough gold or it is not your turn.')
    if query.data=="Village":
        if (buy_turn == True) and (gold - 3 >= 0):
            buy_temp.append('Village')
            gold -= 3
            buy_time -= 1
            query.edit_message_text('You have bought Village .\nType /buy to continue buying cards\nType /use to use cards\nType ( /end ) to finish buying.')
        else:
            query.message.reply_text('You dont have enough gold or it is not your turn.')
    if query.data=="Courtyard":
        if (buy_turn == True) and (gold - 2 >= 0):
            buy_temp.append('Courtyard')
            gold -= 2
            buy_time -= 1
            query.edit_message_text('You have bought Courtyard .\nType /buy to continue buying cards\nType /use to use cards\nType ( /end ) to finish buying.')
        else:
            query.message.reply_text('You dont have enough gold or it is not your turn.')
    if query.data=="gold":
        if (buy_turn == True) and (gold - 6 >= 0):
            buy_temp.append('gold')
            gold -= 6
            buy_time -= 1
            query.edit_message_text('You have bought Gold .\nType /buy to continue buying cards\nType /use to use cards\nType ( /end ) to finish buying.')
        else:
            query.message.reply_text('You dont have enough gold or it is not your turn.')
    if query.data=="Harbinger":
        if (buy_turn == True) and (gold - 3 >= 0):
            buy_temp.append('Harbinger')
            gold -= 3
            buy_time -= 1
            query.edit_message_text('You have bought Harbinger .\nType /buy to continue buying cards\nType /use to use cards\nType ( /end ) to finish buying.')
        else:
            query.message.reply_text('You dont have enough gold or it is not your turn.')
    if query.data=="Laboratory":
        if (buy_turn == True) and (gold - 5 >= 0):
            buy_temp.append('Laboratory')
            gold -= 5
            buy_time -= 1
            query.edit_message_text('You have bought Laboratory .\nType /buy to continue buying cards\nType /use to use cards\nType ( /end ) to finish buying.')
        else:
            query.message.reply_text('You dont have enough gold or it is not your turn.')
    if query.data=="Workshop":
        if (buy_turn == True) and (gold - 3 >= 0):
            buy_temp.append('Workshop')
            gold -= 3
            buy_time -= 1
            query.edit_message_text('You have bought Workshop .\nType /buy to continue buying cards\nType /use to use cards\nType ( /end ) to finish buying.')
        else:
            query.message.reply_text('You dont have enough gold or it is not your turn.')
    if query.data=='usevillage':
        if action>0:
            action-=1
            action +=2
            if turn_count == 1:
                hand.remove('Village')
                grave.append('Village')
                temp = random.choice(deckplayer1)
                hand.append(temp)
                if temp == 'copper':
                    gold += 1
                elif temp == 'silver':
                    gold += 2
                elif temp == 'gold':
                    gold += 3
                query.edit_message_text('You have draw [' + str(temp) + ']  and you now have ' + str(action) + ' action.\nType /use to continue using cards.\nType /buy to buy cards\nType /end to end.')
            elif turn_count == 2:
                hand2.remove('Village')
                grave2.append('Village')
                temp = random.choice(deckplayer2)
                hand2.append(temp)
                if temp == 'copper':
                    gold += 1
                elif temp == 'silver':
                    gold += 2
                elif temp == 'gold':
                    gold += 3
                query.edit_message_text('You have draw [' + str(temp) + '] and you now have ' + str(action) + ' action.\nType /use to continue using cards.\nType /buy to buy cards\nType /end to end.')
            elif turn_count == 3:
                hand3.remove('Village')
                grave3.append('Village')
                temp = random.choice(deckplayer3)
                hand3.append(temp)
                if temp == 'copper':
                    gold += 1
                elif temp == 'silver':
                    gold += 2
                elif temp == 'gold':
                    gold += 3
                query.edit_message_text('You have draw [' + str(temp) + '] and you now have ' + str(action) + ' action.\nType /use to continue using cards.\nType /buy to buy cards\nType /end to end.')
        else:
                query.edit_message_text('You dont have enough Action.')
    if query.data == 'usewitch':
        if action >0:
            action -= 1
            if turn_count == 1:
                hand.remove('Witch')
                grave.append('Witch')
                grave2.append('Curse')
                grave3.append('Curse')
                temp = random.choice(deckplayer1)
                hand.append(temp)
                tempp =random.choice(deckplayer1)
                hand.append(tempp)
                if temp == 'copper':
                    gold += 1
                elif temp == 'silver':
                    gold += 2
                elif temp == 'gold':
                    gold += 3
                if tempp == 'copper':
                    gold += 1
                elif tempp == 'silver':
                    gold += 2
                elif tempp == 'gold':
                    gold += 3
                query.edit_message_text('You have draw [' + str(temp) + '] and [' + str(tempp) + '] and you now have ' + str(action) + ' action.\nEveryone now get a Curse\nType /buy to buy cards\nType /use to continue using cards.\nType /end to end.')
            elif turn_count == 2:
                hand2.remove('Witch')
                grave2.append('Witch')
                grave.append('Curse')
                grave3.append('Curse')
                temp = random.choice(deckplayer2)
                hand2.append(temp)
                tempp = random.choice(deckplayer2)
                hand2.append(tempp)
                if temp == 'copper':
                    gold += 1
                elif temp == 'silver':
                    gold += 2
                elif temp == 'gold':
                    gold += 3
                if tempp == 'copper':
                    gold += 1
                elif tempp == 'silver':
                    gold += 2
                elif tempp == 'gold':
                    gold += 3
                query.edit_message_text('You have draw [' + str(temp) + '] and [' + str(tempp) + '] and you now have ' + str(action) + ' action.\nEveryone now get a Curse\nType /buy to buy cards\nType /use to continue using cards.\nType /end to end.')
            elif turn_count == 3:
                hand3.remove('Witch')
                grave3.append('Witch')
                grave.append('Curse')
                grave2.append('Curse')
                temp = random.choice(deckplayer3)
                hand3.append(temp)
                tempp = random.choice(deckplayer3)
                hand3.append(tempp)
                if temp == 'copper':
                    gold += 1
                elif temp == 'silver':
                    gold += 2
                elif temp == 'gold':
                    gold += 3
                if tempp == 'copper':
                    gold += 1
                elif tempp == 'silver':
                    gold += 2
                elif tempp == 'gold':
                    gold += 3
                query.edit_message_text('You have draw [' + str(temp) + '] and [' + str(tempp) + '] and you now have ' + str(action) + ' action.\nEveryone now get a Curse\nType /buy to buy cards\nType /use to continue using cards.\nType /end to end.')
            else:
                query.edit_message_text('You dont have enough Action.')
    if query.data == 'usecourtyard':
        keyboard = [[]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        if action >0:
            action -= 1
            if turn_count == 1:
                hand.remove('Courtyard')
                grave.append('Courtyard')
                temp = random.choice(deckplayer1)
                hand.append(temp)
                if deckplayer1 == []:
                    deckplayer1 = grave
                    grave = []
                tempp =random.choice(deckplayer1)
                hand.append(tempp)
                if deckplayer1 == []:
                    deckplayer1 = grave
                    grave = []
                temppp = random.choice(deckplayer1)
                hand.append(temppp)
                if deckplayer1 == []:
                    deckplayer1 = grave
                    grave = []
                if temp == 'copper':
                    gold += 1
                elif temp == 'silver':
                    gold += 2
                elif temp == 'gold':
                    gold += 3
                if tempp == 'copper':
                    gold += 1
                elif tempp == 'silver':
                    gold += 2
                elif tempp == 'gold':
                    gold += 3
                if temppp == 'copper':
                    gold += 1
                elif temppp == 'silver':
                    gold += 2
                elif temppp == 'gold':
                    gold += 3
                for i in range(len(hand)):
                    c_temp = hand[i]
                    if c_temp == 'Village':
                        keyboard.append([InlineKeyboardButton('Village', callback_data="c_village")])
                    elif c_temp == 'Witch':
                        keyboard.append([InlineKeyboardButton("Witch", callback_data="c_witch")])
                    elif c_temp == 'Courtyard':
                        keyboard.append([InlineKeyboardButton("Courtyard", callback_data="c_courtyard")])
                    elif c_temp == 'copper':
                        keyboard.append([InlineKeyboardButton("Copper", callback_data="c_copper")])
                    elif c_temp == 'silver':
                        keyboard.append([InlineKeyboardButton("Silver", callback_data="c_silver")])
                    elif c_temp == 'gold':
                        keyboard.append([InlineKeyboardButton("gold", callback_data="c_gold")])
                    elif c_temp == 'estates':
                        keyboard.append([InlineKeyboardButton('Estates' , callback_data='c_estates')])
                query.message.reply_text('Cards available : ', reply_markup=reply_markup)
                query.edit_message_text('You have draw ' + str(temp) + ' , ' +str(temppp) + ' and ' + str(tempp) + ' and you now have ' + str(action) + ' action.\nType /buy to buy cards\nType /use to continue using cards.\nType /end to end.')
            elif turn_count == 2:
                hand2.remove('Courtyard')
                grave2.append('Courtyard')
                temp = random.choice(deckplayer2)
                hand2.append(temp)
                if deckplayer2 == []:
                    deckplayer2 = grave2
                    grave = []
                tempp = random.choice(deckplayer2)
                hand2.append(tempp)
                if deckplayer2 == []:
                    deckplayer2 = grave2
                    grave = []
                temppp = random.choice(deckplayer2)
                hand2.append(temppp)
                if deckplayer2 == []:
                    deckplayer2 = grave2
                    grave = []
                if temp == 'copper':
                    gold += 1
                elif temp == 'silver':
                    gold += 2
                elif temp == 'gold':
                    gold += 3
                if tempp == 'copper':
                    gold += 1
                elif tempp == 'silver':
                    gold += 2
                elif tempp == 'gold':
                    gold += 3
                if temppp == 'copper':
                    gold += 1
                elif temppp == 'silver':
                    gold += 2
                elif temppp == 'gold':
                    gold += 3
                for i in range(len(hand2)):
                    c_temp = hand2[i]
                    if c_temp == 'Village':
                        keyboard.append([InlineKeyboardButton('Village', callback_data="c_village")])
                    elif c_temp == 'Witch':
                        keyboard.append([InlineKeyboardButton("Witch", callback_data="c_witch")])
                    elif c_temp == 'Courtyard':
                        keyboard.append([InlineKeyboardButton("Courtyard", callback_data="c_courtyard")])
                    elif c_temp == 'copper':
                        keyboard.append([InlineKeyboardButton("Copper", callback_data="c_copper")])
                    elif c_temp == 'silver':
                        keyboard.append([InlineKeyboardButton("Silver", callback_data="c_silver")])
                    elif c_temp == 'gold':
                        keyboard.append([InlineKeyboardButton("gold", callback_data="c_gold")])
                    elif c_temp == 'estates':
                        keyboard.append([InlineKeyboardButton('Estates' , callback_data='c_estates')])
                query.message.reply_text('Cards available : ', reply_markup=reply_markup)
                query.edit_message_text('You have draw ' + str(temp) + ' , ' + str(temppp) + ' and ' + str(tempp) + ' and you now have ' + str(action) + ' action.\nType /buy to buy cards\nType /use to continue using cards.\nType /end to end.')
            elif turn_count == 3:
                hand3.remove('Courtyard')
                grave3.append('Courtyard')
                temp = random.choice(deckplayer3)
                hand3.append(temp)
                if deckplayer3 == []:
                    deckplayer3 = grave3
                    grave = []
                tempp = random.choice(deckplayer3)
                hand3.append(tempp)
                if deckplayer3 == []:
                    deckplayer3 = grave3
                    grave = []
                temppp = random.choice(deckplayer3)
                hand3.append(temppp)
                if deckplayer3 == []:
                    deckplayer3 = grave3
                    grave = []
                if temp == 'copper':
                    gold += 1
                elif temp == 'silver':
                    gold += 2
                elif temp == 'gold':
                    gold += 3
                if tempp == 'copper':
                    gold += 1
                elif tempp == 'silver':
                    gold += 2
                elif tempp == 'gold':
                    gold += 3
                if temppp == 'copper':
                    gold += 1
                elif temppp == 'silver':
                    gold += 2
                elif temppp == 'gold':
                    gold += 3
                for i in range(len(hand3)):
                    c_temp = hand3[i]
                    if c_temp == 'Village':
                        keyboard.append([InlineKeyboardButton('Village', callback_data="c_village")])
                    elif c_temp == 'Witch':
                        keyboard.append([InlineKeyboardButton("Witch", callback_data="c_witch")])
                    elif c_temp == 'Courtyard':
                        keyboard.append([InlineKeyboardButton("Courtyard", callback_data="c_courtyard")])
                    elif c_temp == 'copper':
                        keyboard.append([InlineKeyboardButton("Copper", callback_data="c_copper")])
                    elif c_temp == 'silver':
                        keyboard.append([InlineKeyboardButton("Silver", callback_data="c_silver")])
                    elif c_temp == 'gold':
                        keyboard.append([InlineKeyboardButton("gold", callback_data="c_gold")])
                    elif c_temp == 'estates':
                        keyboard.append([InlineKeyboardButton('Estates' , callback_data='c_estates')])
                query.edit_message_text('You have draw ' + str(temp) + ' , ' + str(temppp) + ' and ' + str(tempp) + ' and you now have ' + str(action) + ' action.\nType /buy to buy cards\nType /use to continue using cards.\nType /end to end.')
            query.message.reply_text('You can put one card on top of your deck\nCards availbale:',replymarkup=replymarkup)
        else:
            query.edit_message_text('You dont have enough Action.')
    if query.data == 'useharbinger':
        keyboard = [[]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        if action >0 :
            if turn_count == 1:
                query.edit_message_text('You have ' + str(grave) +' in your discarded pile')
                hand.remove('Harbinger')
                for i in range(len(grave)):
                    h_temp = grave[i]
                    if h_temp == 'Village':
                        keyboard.append([InlineKeyboardButton('Village', callback_data="h_village")])
                    elif h_temp == 'Witch':
                        keyboard.append([InlineKeyboardButton("Witch", callback_data="h_witch")])
                    elif h_temp == 'Courtyard':
                        keyboard.append([InlineKeyboardButton("Courtyard", callback_data="h_courtyard")])
                    elif h_temp == 'copper':
                        keyboard.append([InlineKeyboardButton("Copper", callback_data="h_copper")])
                    elif h_temp == 'silver':
                        keyboard.append([InlineKeyboardButton("Silver", callback_data="h_silver")])
                    elif h_temp == 'gold':
                        keyboard.append([InlineKeyboardButton("Gold", callback_data="h_gold")])
                    elif h_temp == 'estates':
                        keyboard.append([InlineKeyboardButton('Estates', callback_data='h_estates')])
                    elif h_temp == 'Harbinger':
                        keyboard.append([InlineKeyboardButton('Harbinger', callback_data='h_harbinger')])
                grave.append('Harbinger')
                query.message.reply_text('Cards available:',reply_markup=reply_markup)
            elif turn_count ==2 :
                hand2.remove('Harbinger')
                query.edit_message_text('You have ' + str(grave2) + ' in your discarded pile')
                for i in range(len(grave2)):
                    h_temp = grave[i]
                    if h_temp == 'Village':
                        keyboard.append([InlineKeyboardButton('Village', callback_data="h_village")])
                    elif h_temp == 'Witch':
                        keyboard.append([InlineKeyboardButton("Witch", callback_data="h_witch")])
                    elif h_temp == 'Courtyard':
                        keyboard.append([InlineKeyboardButton("Courtyard", callback_data="h_courtyard")])
                    elif h_temp == 'copper':
                        keyboard.append([InlineKeyboardButton("Copper", callback_data="h_copper")])
                    elif h_temp == 'silver':
                        keyboard.append([InlineKeyboardButton("Silver", callback_data="h_silver")])
                    elif h_temp == 'gold':
                        keyboard.append([InlineKeyboardButton("Gold", callback_data="h_gold")])
                    elif h_temp == 'estates':
                        keyboard.append([InlineKeyboardButton('Estates', callback_data='h_estates')])
                    elif h_temp == 'Harbinger':
                        keyboard.append([InlineKeyboardButton('Harbinger', callback_data='h_harbinger')])
                grave2.append('Harbinger')
                query.message.reply_text('Cards available:', reply_markup=reply_markup)
            elif turn_count == 3 :
                hand.remove('Harbinger')
                query.edit_message_text('You have ' + str(grave3) + ' in your discarded pile')
                for i in range(len(grave3)):
                    h_temp = grave[i]
                    if h_temp == 'Village':
                        keyboard.append([InlineKeyboardButton('Village', callback_data="h_village")])
                    elif h_temp == 'Witch':
                        keyboard.append([InlineKeyboardButton("Witch", callback_data="h_witch")])
                    elif h_temp == 'Courtyard':
                        keyboard.append([InlineKeyboardButton("Courtyard", callback_data="h_courtyard")])
                    elif h_temp == 'copper':
                        keyboard.append([InlineKeyboardButton("Copper", callback_data="h_copper")])
                    elif h_temp == 'silver':
                        keyboard.append([InlineKeyboardButton("Silver", callback_data="h_silver")])
                    elif h_temp == 'gold':
                        keyboard.append([InlineKeyboardButton("Gold", callback_data="h_gold")])
                    elif h_temp == 'estates':
                        keyboard.append([InlineKeyboardButton('Estates', callback_data='h_estates')])
                    elif h_temp == 'Harbinger':
                        keyboard.append([InlineKeyboardButton('Harbinger', callback_data='h_harbinger')])
                grave3.append('Harbinger')
                query.message.reply_text('Cards available:', reply_markup=reply_markup)
        else:
            query.message.reply_text('you dont have enough action')
    if query.data == 'uselaboratory':
        if action >0:
            action -= 1
            action +=1
            if turn_count == 1:
                hand.remove('Laboratory')
                grave.append('Laboratory')
                temp = random.choice(deckplayer1)
                hand.append(temp)
                tempp =random.choice(deckplayer1)
                hand.append(tempp)
                if temp == 'copper':
                    gold += 1
                elif temp == 'silver':
                    gold += 2
                elif temp == 'gold':
                    gold += 3
                if tempp == 'copper':
                    gold += 1
                elif tempp == 'silver':
                    gold += 2
                elif tempp == 'gold':
                    gold += 3
                query.edit_message_text('You have draw [' + str(temp) + '] and [' + str(tempp) + '] and you now have ' + str(action) + ' action.\nType /buy to buy cards\nType /use to continue using cards.\nType /end to end.')
            elif turn_count == 2:
                hand2.remove('Laboratory')
                grave2.append('Laboratory')
                temp = random.choice(deckplayer2)
                hand2.append(temp)
                tempp = random.choice(deckplayer2)
                hand2.append(tempp)
                if temp == 'copper':
                    gold += 1
                elif temp == 'silver':
                    gold += 2
                elif temp == 'gold':
                    gold += 3
                if tempp == 'copper':
                    gold += 1
                elif tempp == 'silver':
                    gold += 2
                elif tempp == 'gold':
                    gold += 3
                query.edit_message_text('You have draw [' + str(temp) + '] and [' + str(tempp) + '] and you now have ' + str(action) + ' action.\nType /buy to buy cards\nType /use to continue using cards.\nType /end to end.')
            elif turn_count == 3:
                hand3.remove('Laboratory')
                grave3.append('Laboratory')
                temp = random.choice(deckplayer3)
                hand3.append(temp)
                tempp = random.choice(deckplayer3)
                hand3.append(tempp)
                if temp == 'copper':
                    gold += 1
                elif temp == 'silver':
                    gold += 2
                elif temp == 'gold':
                    gold += 3
                if tempp == 'copper':
                    gold += 1
                elif tempp == 'silver':
                    gold += 2
                elif tempp == 'gold':
                    gold += 3
                query.edit_message_text('You have draw [' + str(temp) + '] and [' + str(tempp) + '] and you now have ' + str(action) + ' action.\nType /buy to buy cards\nType /use to continue using cards.\nType /end to end.')
            else:
                query.edit_message_text('You dont have enough Action.')
    if query.data == 'useworkshop':
        global keyboard
        keyboard=[[]]
        reply_markup=InlineKeyboardMarkup(keyboard)
        if action>0:
            action -=1
            keyboard.append([InlineKeyboardButton("Workshop", callback_data="w_workshop")])
            keyboard.append([InlineKeyboardButton("Laboratory", callback_data="w_laboratory")])
            keyboard.append([InlineKeyboardButton("Harbinger", callback_data="w_harbinger")])
            keyboard.append([InlineKeyboardButton("Village", callback_data="w_village")])
            keyboard.append([InlineKeyboardButton("Silver", callback_data="w_silver")])
            keyboard.append([InlineKeyboardButton("Courtyard", callback_data="w_courtyard")])
            keyboard.append([InlineKeyboardButton("Clickme", callback_data="clickme")])
            query.message.reply_text('Cards availbale:',reply_markup=reply_markup)
            keyboard.append([InlineKeyboardButton("Click me to end", callback_data="end")])
        else:
            query.edit_message_text('You dont have enough action')
    if query.data == 'c_witch':
        if turn_count == 1:
            temp_deck_top.append('Witch')
            hand.remove('Witch')
        elif turn_count ==2:
            temp_deck_top2.append('Witch')
            hand2.remove('Witch')
        elif turn_count==3:
            temp_deck_top3.append('Witch')
            hand3.remove('Witch')
        query.edit_message_text('Witch is placed on top of your deck.\nType /buy to buy cards\nType /use to continue using cards.\nType /end to end.')
    if query.data == 'c_village':
        if turn_count == 1:
            temp_deck_top.append('Village')
            hand.remove('Village')
        elif turn_count == 2:
            temp_deck_top2.append('Village')
            hand2.remove('Village')
        elif turn_count == 3:
            temp_deck_top3.append('Village')
            hand3.remove('Village')
        query.edit_message_text('Village is placed on top of your deck.\nType /buy to buy cards\nType /use to continue using cards.\nType /end to end.')
    if query.data == 'c_courtyard':
        if turn_count == 1:
            temp_deck_top.append('Courtyard')
            hand.remove('Courtyard')
        elif turn_count == 2:
            temp_deck_top2.append('Courtyard')
            hand2.remove('Courtyard')
        elif turn_count == 3:
            temp_deck_top3.append('Courtyard')
            hand3.remove('Courtyard')
        query.edit_message_text('Courtyard is placed on top of your deck.\nType /buy to buy cards\nType /use to continue using cards.\nType /end to end.')
    if query.data == 'c_copper':
        if turn_count == 1:
            temp_deck_top.append('copper')
            hand.remove('copper')
        elif turn_count == 2:
            temp_deck_top2.append('copper')
            hand2.remove('copper')
        elif turn_count == 3:
            temp_deck_top3.append('copper')
            hand3.remove('copper')
        query.edit_message_text('Copper is placed on top of your deck.\nType /buy to buy cards\nType /use to continue using cards.\nType /end to end.')
    if query.data == 'c_silver':
        if turn_count == 1:
            temp_deck_top.append('silver')
            hand.remove('silver')
        elif turn_count == 2:
            temp_deck_top2.append('silver')
            hand2.remove('silver')
        elif turn_count == 3:
            temp_deck_top3.append('silver')
            hand3.remove('silver')
        query.edit_message_text('Silver is placed on top of your deck.\nType /buy to buy cards\nType /use to continue using cards.\nType /end to end.')
    if query.data == 'c_gold':
        if turn_count == 1:
            temp_deck_top.append('gold')
            hand.remove('gold')
        elif turn_count == 2:
            temp_deck_top2.append('gold')
            hand2.remove('gold')
        elif turn_count == 3:
            temp_deck_top3.append('gold')
            hand3.remove('gold')
        query.edit_message_text('Gold is placed on top of your deck.\nType /buy to buy cards\nType /use to continue using cards.\nType /end to end.')
    if query.data == 'c_estates':
        if turn_count == 1:
            temp_deck_top.append('estates')
            hand.remove('estates')
        elif turn_count == 2:
            temp_deck_top2.append('estates')
            hand2.remove('estates')
        elif turn_count == 3:
            temp_deck_top3.append('estates')
            hand3.remove('estates')
        query.edit_message_text('Estates is placed on top of your deck.\nType /buy to buy cards\nType /use to continue using cards.\nType /end to end.')
    if query.data == 'h_witch':
        if turn_count == 1:
            temp_deck_top.append('Witch')
            grave.remove('Witch')
        elif turn_count ==2:
            temp_deck_top2.append('Witch')
            grave2.remove('Witch')
        elif turn_count==3:
            temp_deck_top3.append('Witch')
            grave3.remove('Witch')
        query.edit_message_text('Witch is placed on top of your deck.\nType /buy to buy cards\nType /use to continue using cards.\nType /end to end.')
    if query.data == 'h_village':
        if turn_count == 1:
            temp_deck_top.append('Village')
            grave.remove('Village')
        elif turn_count == 2:
            temp_deck_top2.append('Village')
            grave2.remove('Village')
        elif turn_count == 3:
            temp_deck_top3.append('Village')
            grave3.remove('Village')
        query.edit_message_text('Village is placed on top of your deck.\nType /buy to buy cards\nType /use to continue using cards.\nType /end to end.')
    if query.data == 'h_courtyard':
        if turn_count == 1:
            temp_deck_top.append('Courtyard')
            grave.remove('Courtyard')
        elif turn_count == 2:
            temp_deck_top2.append('Courtyard')
            grave2.remove('Courtyard')
        elif turn_count == 3:
            temp_deck_top3.append('Courtyard')
            grave3.remove('Courtyard')
        query.edit_message_text('Courtyard is placed on top of your deck.\nType /buy to buy cards\nType /use to continue using cards.\nType /end to end.')
    if query.data == 'h_copper':
        if turn_count == 1:
            temp_deck_top.append('copper')
            grave.remove('copper')
        elif turn_count == 2:
            temp_deck_top2.append('copper')
            grave2.remove('copper')
        elif turn_count == 3:
            temp_deck_top3.append('copper')
            grave3.remove('copper')
        query.edit_message_text('Copper is placed on top of your deck.\nType /buy to buy cards\nType /use to continue using cards.\nType /end to end.')
    if query.data == 'h_silver':
        if turn_count == 1:
            temp_deck_top.append('silver')
            grave.remove('silver')
        elif turn_count == 2:
            temp_deck_top2.append('silver')
            grave2.remove('silver')
        elif turn_count == 3:
            temp_deck_top3.append('silver')
            grave3.remove('silver')
        query.edit_message_text('Silver is placed on top of your deck.\nType /buy to buy cards\nType /use to continue using cards.\nType /end to end.')
    if query.data == 'h_gold':
        if turn_count == 1:
            temp_deck_top.append('gold')
            grave.remove('gold')
        elif turn_count == 2:
            temp_deck_top2.append('gold')
            grave2.remove('gold')
        elif turn_count == 3:
            temp_deck_top3.append('gold')
            grave3.remove('gold')
        query.edit_message_text('Gold is placed on top of your deck.\nType /buy to buy cards\nType /use to continue using cards.\nType /end to end.')
    if query.data == 'h_estates':
        if turn_count == 1:
            temp_deck_top.append('estates')
            grave.remove('estates')
        elif turn_count == 2:
            temp_deck_top2.append('estates')
            grave2.remove('estates')
        elif turn_count == 3:
            temp_deck_top3.append('estates')
            grave3.remove('estates')
        query.edit_message_text('Estates is placed on top of your deck.\nType /buy to buy cards\nType /use to continue using cards.\nType /end to end.')
    if query.data == 'h_harbinger':
        if turn_count == 1:
            temp_deck_top.append('Harbinger')
            grave.remove('Harbinger')
        elif turn_count == 2:
            temp_deck_top2.append('Harbinger')
            grave2.remove('Harbinger')
        elif turn_count == 3:
            temp_deck_top3.append('Harbinger')
            grave3.remove('Harbinger')
        query.edit_message_text('Harbinger is placed on top of your deck.\nType /buy to buy cards\nType /use to continue using cards.\nType /end to end.')
    if query.data == 'w_village':
        if turn_count == 1:
            grave.append('Village')
        elif turn_count == 2:
            grave2.append('Village')
        elif turn_count == 3:
            grave3.append('Village')
        query.edit_message_text('Village is gained into your discarded pile.\nType /buy to buy cards\nType /use to continue using cards.\nType /end to end.')
    if query.data == 'w_courtyard':
        if turn_count == 1:
            grave.append('Courtyard')
        elif turn_count == 2:
            grave2.append('Courtyard')
        elif turn_count == 3:
            grave3.append('Courtyard')
        query.edit_message_text('Courtyard is gained into your discarded pile.\nType /buy to buy cards\nType /use to continue using cards.\nType /end to end.')
    if query.data == 'w_copper':
        if turn_count == 1:
            grave.append('copper')
        elif turn_count == 2:
            grave2.append('copper')
        elif turn_count == 3:
            grave3.append('copper')
        query.edit_message_text('Copper is gained into your discarded pile.\nType /buy to buy cards\nType /use to continue using cards.\nType /end to end.')
    if query.data == 'w_silver':
        if turn_count == 1:
            grave.append('silver')
        elif turn_count == 2:
            grave2.append('silver')
        elif turn_count == 3:
            grave3.append('silver')
        query.edit_message_text('Silver is gained into your discarded pile.\nType /buy to buy cards\nType /use to continue using cards.\nType /end to end.')
    if query.data == 'w_workshop':
        if turn_count == 1:
            grave.append('Workshop')
        elif turn_count == 2:
            grave2.append('Workshop')
        elif turn_count == 3:
            grave3.append('Workshop')
        query.edit_message_text('Workshop is gained into your discarded pile.\nType /buy to buy cards\nType /use to continue using cards.\nType /end to end.')
    if query.data == 'clickme':
        query.edit_message_text('END')
    if query.data == 'end':
        reply_markup=InlineKeyboardMarkup(keyboard)
        query.message.reply_text('end',reply_markup=reply_markup)

def join(bot,update):
    global user1_id
    global user2_id
    global user3_id
    global user1_name
    global user2_name
    global user3_name
    global user1_tag,user2_tag,user3_tag
    if start_game == True:
       update.message.reply_text('The Loby is closed')
    else:
        if str(update.message.from_user.id) == user1_id or str(update.message.from_user.id) == user2_id or str(update.message.from_user.id) == user3_id:
            update.message.reply_text('You have already joined the game.')
        else:
            update.message.reply_text('Welcome ' + str(update.message.from_user.first_name) + str(update.message.from_user.last_name) + ' [ ' + str(update.message.from_user.id) + ' / ' + '@' + str(update.message.from_user.username) + ' ] ')
            if user1_id == 'null':
                user1_id = str(update.message.from_user.id)
                user1_name = str(update.message.from_user.first_name) + str(update.message.from_user.last_name)
                user1_tag = str(update.message.from_user.username)
            elif user2_id== 'null':
                user2_id = str(update.message.from_user.id)
                user2_name = str(update.message.from_user.first_name) + str(update.message.from_user.last_name)
                user2_tag = str(update.message.from_user.username)
            elif user3_id == 'null':
                user3_id = str(update.message.from_user.id)
                user3_name = str(update.message.from_user.first_name) + str(update.message.from_user.last_name)
                user3_tag = str(update.message.from_user.username)
            update.message.reply_text('Current player list :\n [' + str(user1_name) + ' / ' + str(user2_name) + ' / ' + str(user3_name) + ']\nType /join to join the game.\nType /start to start the game.')

def draw(bot,update):
    global temp_deck_top,temp_deck_top2,temp_deck_top3
    global gold
    global points
    global deckplayer1
    global deckplayer2
    global deckplayer3
    global grave
    global grave2
    global grave3
    global turn
    global hand
    global turnnum
    if turn_count == 0:
        update.message.reply_text('Type /join to join the game\nType /start to start the game.')
    else:
        if turn == True:
            update.message.reply_text('Your turn of drawing has ended')
        else:
            update.message.reply_text('Turn ' + str(turnnum))
            if str(update.message.from_user.id) == user1_id and turn_count == 1:
                if temp_deck_top != []:
                    c = temp_deck_top[0]
                    hand.append(c)
                    temp_deck_top = []
                    for i in range(4):
                            temp = (random.choice(deckplayer1))
                            hand.append(temp)
                            deckplayer1.remove(temp)
                            if temp == 'copper':
                                gold += 1
                            elif temp == 'silver':
                                gold += 2
                            elif temp == 'gold':
                                gold += 3
                            if deckplayer1 == []:
                                deckplayer1 = grave
                                grave = []
                            turn = True
                else:
                    for i in range(5):
                            temp = (random.choice(deckplayer1))
                            hand.append(temp)
                            deckplayer1.remove(temp)
                            if temp == 'copper':
                                gold += 1
                            elif temp == 'silver':
                                gold += 2
                            elif temp == 'gold':
                                gold += 3
                            if deckplayer1 == []:
                                deckplayer1 = grave
                                grave = []
                            turn = True
                update.message.reply_text('You got ' + str(hand) + ' .\nType ( /buy ) or ( /use ) to proceed')
            elif str(update.message.from_user.id) == user2_id and turn_count == 2:
                if temp_deck_top2 != []:
                    c = temp_deck_top2[0]
                    hand2.append(c)
                    temp_deck_top2 = []
                    for i in range(4):
                        temp = (random.choice(deckplayer2))
                        hand2.append(temp)
                        deckplayer2.remove(temp)
                        if temp == 'copper':
                            gold += 1
                        elif temp == 'silver':
                            gold += 2
                        elif temp == 'gold':
                            gold += 3
                        if deckplayer1 == []:
                            deckplayer2 = grave2
                            grave2 = []
                        turn = True
                else:
                    for i in range(5):
                            temp = (random.choice(deckplayer2))
                            hand2.append(temp)
                            deckplayer2.remove(temp)
                            if temp == 'copper':
                                gold += 1
                            elif temp == 'silver':
                                gold += 2
                            elif temp == 'gold':
                                gold += 3
                            if deckplayer2 == []:
                                deckplayer2 = grave2
                                grave2 = []
                            turn = True
                update.message.reply_text('You got ' + str(hand2) + ' .\nType ( /buy ) or ( /use ) to proceed')
            elif str(update.message.from_user.id) == user3_id and turn_count == 3:
                if temp_deck_top != []:
                    c = temp_deck_top3[0]
                    hand3.append(c)
                    temp_deck_top3 = []
                    for i in range(4):
                        temp = (random.choice(deckplayer3))
                        hand3.append(temp)
                        deckplayer3.remove(temp)
                        if temp == 'copper':
                            gold += 1
                        elif temp == 'silver':
                            gold += 2
                        elif temp == 'gold':
                            gold += 3
                        if deckplayer3 == []:
                            deckplayer3 = grave3
                            grave3 = []
                        turn = True
                else:
                    for i in range(5):
                            temp = (random.choice(deckplayer3))
                            hand3.append(temp)
                            deckplayer3.remove(temp)
                            if temp == 'copper':
                                gold += 1
                            elif temp == 'silver':
                                gold += 2
                            elif temp == 'gold':
                                gold += 3
                            if deckplayer3 == []:
                                deckplayer3 = grave3
                                grave3 = []
                            turn = True
                update.message.reply_text('You got ' + str(hand3) + ' .\nType ( /buy ) or ( /use ) to proceed')
            else:
                update.message.reply_text('Its not your turn or you havent joined the game yet.')

def use(bot,update):
    keyboard = [[]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if turn_count == 1:
        update.message.reply_text(str(user1_name) + ', you have : ' + str(hand))
        for i in range(len(hand)):
            tempp = hand[i]
            if tempp == 'Village':
                keyboard.append([InlineKeyboardButton('Village', callback_data="usevillage")])
            elif tempp == 'Witch':
                keyboard.append([InlineKeyboardButton("Witch", callback_data="usewitch")])
            elif tempp == 'Courtyard':
                keyboard.append([InlineKeyboardButton("Courtyard", callback_data="usecourtyard")])
            elif tempp == 'Harbinger':
                keyboard.append([InlineKeyboardButton("Harbinger", callback_data="useharbinger")])
            elif tempp == 'Laboratory':
                keyboard.append([InlineKeyboardButton("Laboratory", callback_data="uselaboratory")])
            elif tempp == 'Workshop':
                keyboard.append([InlineKeyboardButton("Workshop", callback_data="useworkshop")])
        update.message.reply_text('Cards available : ', reply_markup=reply_markup)
    elif turn_count == 2:
        update.message.reply_text(str(user2_name) + ', you have : ' + str(hand2))
        for i in range(len(hand2)):
            tempp = hand2[i]
            if tempp == 'Village':
                keyboard.append([InlineKeyboardButton('Village', callback_data="usevillage")])
            elif tempp == 'Witch':
                keyboard.append([InlineKeyboardButton("Witch", callback_data="usewitch")])
            elif tempp == 'Courtyard':
                keyboard.append([InlineKeyboardButton("Courtyard", callback_data="usecourtyard")])
            elif tempp == 'Harbinger':
                keyboard.append([InlineKeyboardButton("Harbinger", callback_data="useharbinger")])
            elif tempp == 'Laboratory':
                keyboard.append([InlineKeyboardButton("Laboratory", callback_data="uselaboratory")])
            elif tempp == 'Workshop':
                keyboard.append([InlineKeyboardButton("Workshop", callback_data="useworkshop")])
        update.message.reply_text('Cards available : ', reply_markup=reply_markup)
    elif turn_count == 3:
        update.message.reply_text(str(user3_name) + ', you have : ' + str(hand))
        for i in range(len(hand3)):
            tempp = hand3[i]
            if tempp == 'Village':
                keyboard.append([InlineKeyboardButton('Village', callback_data="usevillage")])
            elif tempp == 'Witch':
                keyboard.append([InlineKeyboardButton("Witch", callback_data="usewitch")])
            elif tempp == 'Courtyard':
                keyboard.append([InlineKeyboardButton("Courtyard", callback_data="usecourtyard")])
            elif tempp == 'Harbinger':
                keyboard.append([InlineKeyboardButton("Harbinger", callback_data="useharbinger")])
            elif tempp == 'Laboratory':
                keyboard.append([InlineKeyboardButton("Laboratory", callback_data="uselaboratory")])
            elif tempp == 'workshop':
                keyboard.append([InlineKeyboardButton("Workshop", callback_data="useworkshop")])
        update.message.reply_text('Cards available : ', reply_markup=reply_markup)



def buy(bot,update):
    global gold
    global buy_turn
    update.message.reply_text('You have <' + str(gold) + '> dollar')
    buy_turn = True
    keyboard = [[]]
    if gold >=6 :
        keyboard.append([InlineKeyboardButton("Gold", callback_data="gold")])
        keyboard.append([InlineKeyboardButton("Laboratory", callback_data="Laboratory")])
        keyboard.append([InlineKeyboardButton("Witch", callback_data="Witch")])
        keyboard.append([InlineKeyboardButton("Harbinger", callback_data="Harbinger")])
        keyboard.append([InlineKeyboardButton("Village", callback_data="Village")])
        keyboard.append([InlineKeyboardButton("Silver", callback_data="silver")])
        keyboard.append([InlineKeyboardButton("Courtyard", callback_data="Courtyard")])
        update.message.reply_text('Buy Gold costs 6 dollars\nBuy Laboratory costs 5 dollars\nBuy Witch costs 5 dollars\nBuy Harbinger costs 3 dollars\nBuy Village costs 3 dollars\nBuy Silver costs 3 dollars\nBuy Courtyard costs 2 dollar')
    elif gold == 5:
        keyboard.append([InlineKeyboardButton("Laboratory", callback_data="Laboratory")])
        keyboard.append([InlineKeyboardButton("Witch", callback_data="Witch")])
        keyboard.append([InlineKeyboardButton("Harbinger", callback_data="Harbinger")])
        keyboard.append([InlineKeyboardButton("Village", callback_data="Village")])
        keyboard.append([InlineKeyboardButton("Silver", callback_data="silver")])
        keyboard.append([InlineKeyboardButton("Courtyard", callback_data="Courtyard")])
        update.message.reply_text('Buy Witch costs 5 dollars\nBuy Laboratory costs 5 dollar\nBuy Harbinger costs 3 dollars\nBuy Village costs 3 dollars\nBuy Silver costs 3 dollars\nBuy Courtyard costs 2 dollar')
    elif gold == 4:
        update.message.reply_text('Buy Harbinger costs 3 dollars\nBuy Workshop costs 3 dollar\nBuy Village costs 3 dollars\nBuy Silver costs 3 dollars\nBuy Courtyard costs 2 dollar')
        keyboard.append([InlineKeyboardButton("Workshop", callback_data="Workshop")])
        keyboard.append([InlineKeyboardButton("Harbinger", callback_data="Harbinger")])
        keyboard.append([InlineKeyboardButton("Village", callback_data="Village")])
        keyboard.append([InlineKeyboardButton("Silver", callback_data="silver")])
        keyboard.append([InlineKeyboardButton("Courtyard", callback_data="Courtyard")])
    elif gold == 3 :
        update.message.reply_text('Buy Harbinger costs 3 dollars\nBuy Workshop costs 3 dollar\nBuy Village costs 3 dollars\nBuy Silver costs 3 dollars\nBuy Courtyard costs 2 dollar')
        keyboard.append([InlineKeyboardButton("Workshop", callback_data="Workshop")])
        keyboard.append([InlineKeyboardButton("Harbinger", callback_data="Harbinger")])
        keyboard.append([InlineKeyboardButton("Village", callback_data="Village")])
        keyboard.append([InlineKeyboardButton("Silver", callback_data="silver")])
        keyboard.append([InlineKeyboardButton("Courtyard", callback_data="Courtyard")])
    elif gold == 2:
        update.message.reply_text('Buy Courtyard costs 2 dollar')
        keyboard.append([InlineKeyboardButton("Courtyard", callback_data="Courtyard")])
    update.message.reply_text('Cards available : ',reply_markup=InlineKeyboardMarkup(keyboard))

def end(bot,update):
    global turn
    global gold
    global grave
    global grave2
    global grave3
    global buy_temp
    global hand
    global hand2
    global hand3
    global turn_count
    global turnnum
    global action
    turn = False
    turnnum += 1
    turn=False
    action = 1
    gold = 0
    if  turn_count == 1 :
        grave += hand
        grave += buy_temp
        hand = []
        buy_temp = []
        update.message.reply_text(str(user1_name) + ' is done!')
    elif turn_count == 2 :
        grave2 += hand2
        grave2 += buy_temp
        hand2 = []
        buy_temp = []
        update.message.reply_text(str(user2_name) + ' is done!')
    elif turn_count == 3 :
        grave3 += hand3
        grave3 += buy_temp
        hand3 = []
        buy_temp = []
        update.message.reply_text(str(user3_name) + ' is done!')
    else:
        update.message.reply_text('Its not your turn.')
    turn_count += 1
    if user3_name == 'null' and turn_count == 3:
        turn_count = 1
    elif turn_count == 4:
        turn_count = 1
    if turn_count==1:
        update.message.reply_text("Its now your turn , " + str(user1_name) + ' @' + user1_tag + '\nType /draw')
    elif turn_count==2:
        update.message.reply_text("Its now your turn , " + str(user2_name) + ' @' + user2_tag +'\nType /draw')
    elif turn_count==3:
        update.message.reply_text("Its now your turn , " + str(user3_name) + ' @' + user3_tag +'\nType /draw')

def playerlist(bot,update):
    update.message.reply_text('Current player list :\n [' + str(user1_name) + ' / ' + str(user2_name) + ' / ' + str(user3_name) + ']\nSupport Max to 3 player')

def money(bot,update):
    update.message.reply_text('You have <' + str(gold) + '> dollar')

def point(bot,update):
    update.message.reply_text('You have <' + str(points) + '> points')

def reset(bot,update):
    global gold
    global deckplayer1
    global deckplayer2
    global deckplayer3
    global grave
    global grave2
    global grave3
    global buy_temp
    global hand
    global hand2
    global hand3
    global gold2,gold3,points,points2,points3,buy_turn,buy_time,action,user1_id,user1_name,user2_id,user2_name,user3_id,user3_name,current_player,inlinehand,courtyard_temp,turn_count,turnnum,start_game
    global turn
    global hand
    deckplayer1 = ['copper', 'copper', 'copper', 'copper', 'copper', 'copper', 'copper', 'estates', 'estates','estates']
    deckplayer2 = ['copper', 'copper', 'copper', 'copper', 'copper', 'copper', 'copper', 'estates', 'estates','estates']
    deckplayer3 = ['copper', 'copper', 'copper', 'copper', 'copper', 'copper', 'copper', 'estates', 'estates','estates']
    grave = []
    grave2 = []
    grave3 = []
    buy_temp = []
    hand = []
    hand2 = []
    hand3 = []
    gold = 0
    gold2 = 0
    gold3 = 0
    points = 0
    points2 = 0
    points3 = 0
    turn = False
    buy_turn = False
    buy_time = 1
    action = 1
    user1_id = 'null'
    user2_id = 'null'
    user3_id = 'null'
    user1_name = 'null'
    user2_name = 'null'
    user3_name = 'null'
    current_player = 1
    courtyard_temp = 0
    inlinehand = []
    turn_count = 0
    turnnum = 0
    start_game = False
    update.message.reply_text('Success')

def status(bot,update):
    update.message.reply_text('normal\nv 1.2.3.3 (beta)')


def show (bot,update):
    update.message.reply_text('Action:'+str(action)+'\nTurn count is '+str(turn_count)+'\n'+str(hand)+'\n'+str(hand2)+'\n'+str(hand3))
    update.message.reply_text(user1_id+ '\n' +str(update.message.from_user.id))
    update.message.reply_text('Grave\n'+str(grave)+'\n'+str(grave2)+'\n'+str(grave3))
    update.message.reply_text('Deck\n'+str(deckplayer1)+'\n'+str(deckplayer2)+'\n'+str(deckplayer3))

def admin(bot,update):
    update.message.reply_text('/join\n/start\n/draw')

def error(bot,update,error):
    logger.warning('Update "%s" caused error "%s"', update, error)

def log(bot,update):
    fp = open('logging.txt', "r")
    lines = fp.readlines()
    fp.close()
    n = len(lines) - 10
    for i in range(10):
        temp = (str(lines[n]))
        n += 1
        update.message.reply_text(str(temp))

def lg(bot,update):
    fp = open('logging.txt', "r")
    lines = fp.readlines()
    fp.close()
    n = len(lines) - 3
    for i in range(3):
        temp = (str(lines[n]))
        n += 1
        update.message.reply_text(str(temp))


def main():
    updater = Updater('599551578:AAE709inuNhedfLCwIVKF9fWXJNJ-pqv5lg')
    test = updater.dispatcher
    test.add_handler(CommandHandler('draw',draw))
    test.add_handler(CommandHandler('money',money))
    test.add_handler(CommandHandler('point',point))
    test.add_handler(CommandHandler('buy',buy))
    test.add_handler(CommandHandler('end',end))
    test.add_handler(CommandHandler('join',join))
    test.add_handler(CommandHandler('start',start))
    test.add_handler(CommandHandler('use',use))
    test.add_handler(CommandHandler('playerlist',playerlist))
    test.add_handler(RegexHandler('.*status.*',status))
    test.add_handler(RegexHandler('.*reset.*', reset))
    test.add_handler(RegexHandler('admin',admin))
    test.add_handler(RegexHandler('.*show.*',show))
    test.add_handler(RegexHandler('.*log.*',log))
    test.add_handler(RegexHandler('.*lg.*', lg))
    test.add_error_handler(error)
    test.add_handler(CallbackQueryHandler(button))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()