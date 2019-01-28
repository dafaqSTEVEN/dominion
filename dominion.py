import logging
import random
from typing import List

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, MessageHandler, CommandHandler, RegexHandler, CallbackQueryHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='logging.txt',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


deckplayer1 = ['Copper','Copper','Copper','Copper','Copper','Copper','Copper','Estates','Estates','Estates']
deckplayer2 = ['Copper','Copper','Copper','Copper','Copper','Copper','Copper','Estates','Estates','Estates']
deckplayer3 =['Copper','Copper','Copper','Copper','Copper','Copper','Copper','Estates','Estates','Estates']
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
gold1 =0
gold2=0
gold3=0
points = 0
points2 = 0
points3 = 0
turn = False
buy_turn = False
buy_time = 1
action = 1
chat_id = 'null'
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
Provincecard=10
Duchycard=10
Estatescard=10
Villagecard=10
Harbingercard=10
Laboratorycard=10
Witchcard=10
Workshopcard=10
Courtyardcard=10
Moneylendercard=10
Endgame=False




def startgame(bot,update):
    global turn_count
    global turnnum
    global start_game
    start_game = True
    update.message.reply_text("Loby is closed\n" + str(user1_name) + 's turn..')
    global temp_deck_top, temp_deck_top2, temp_deck_top3
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
    global gold1,gold2,gold3
    global chat_id
    turn_count = 1
    turnnum = 1
    chat_id = str(update.message.chat.id)
    if turn_count > 1:
        update.message.reply_text('The game is started.')
    else:
        for i in range(5):
                temp = (random.choice(deckplayer1))
                hand.append(temp)
                deckplayer1.remove(temp)
                if temp == 'Copper':
                    gold1 += 1
                elif temp == 'Silver':
                    gold1 += 2
                elif temp == 'Gold':
                    gold1 += 3
                turn = True
        bot.sendMessage(chat_id = str(user1_id),text = 'You got ' + str(hand) + ' .')
        for i in range(5):
            temp = (random.choice(deckplayer2))
            hand2.append(temp)
            deckplayer2.remove(temp)
            if temp == 'Copper':
                gold2 += 1
            elif temp == 'Silver':
                gold2 += 2
            elif temp == 'Gold':
                gold2 += 3
            turn = True
        bot.sendMessage(chat_id = str(user2_id),text = 'You got ' + str(hand2) + ' .')
        if user3_id !='null':
            for i in range(5):
                temp = (random.choice(deckplayer3))
                hand3.append(temp)
                deckplayer3.remove(temp)
                if temp == 'Copper':
                    gold3 += 1
                elif temp == 'Silver':
                    gold3 += 2
                elif temp == 'Gold':
                    gold3 += 3
                turn = True
            bot.sendMessage(chat_id = str(user3_id),text = 'You got ' + str(hand3) + ' .')
        gold = gold1

def button(bot,update):
    global Endgame
    global deckplayer1,deckplayer2,deckplayer3
    global grave,grave2,grave3
    global temp_deck_top,temp_deck_top2,temp_deck_top3
    global action
    global gold
    global buy_temp
    global buy_time
    global Provincecard,Duchycard,Estatescard,Villagecard,Laboratorycard,Workshopcard,Harbingercard,Courtyardcard,Witchcard,Moneylendercard
    query = update.callback_query
    #buy section
	if query.data == 'Moneylender':
		if (buy_turn == true) and (gold - 4 >= 0):
			buy_temp.append('Moneylender')
			gold-=4
			buy_time-=1
			Moneylendercard-=1
			query.edit_message_text('You have bought Moneylender.\nype /buy to continue buying cards\nType /action to use cards\nType ( /end ) to finish buying.')
		else:
			query.message.reply_text('You dont have enough gold or there is no more card in the pile.')
    if query.data == 'Province':
        if (buy_turn == True) and (gold - 8 >= 0) and (Provincecard == 1):
            buy_temp.append('Province')
            gold -= 8
            buy_time -= 1
            Provincecard -= 1
            query.edit_message_text('You have bought Province.\nType /buy to continue buying cards\nType /action to use cards\nType ( /end ) to finish buying.')
            query.message.reply_text('Game will be ended after this bought')
            Endgame=True
        elif (buy_turn == True) and (gold - 8 >= 0) and (Provincecard>0):
                buy_temp.append('Province')
                gold -= 8
                buy_time -= 1
                Provincecard -= 1
                query.edit_message_text('You have bought Province.\nType /buy to continue buying cards\nType /action to use cards\nType ( /end ) to finish buying.')
        else:
                query.message.reply_text('You dont have enough gold or there is no more card in the pile.')
    if query.data == 'Duchy':
        if (buy_turn == True) and (gold - 5 >= 0) and (Duchycard>0):
            buy_temp.append('Duchy')
            gold -= 5
            buy_time -= 1
            Duchycard -=1
            query.edit_message_text('You have bought Duchy.\nType /buy to continue buying cards\nType /action to use cards\nType ( /end ) to finish buying.')
        else:
            query.message.reply_text('You dont have enough gold or there is no more card in the pile.')
    if query.data == 'Estates':
        if (buy_turn == True) and (gold - 2 >= 0) and (Estatescard>0):
            buy_temp.append('Estates')
            gold -= 2
            buy_time -= 1
            Estatescard-=1
            query.edit_message_text('You have bought Estates.\nType /buy to continue buying cards\nType /action to use cards\nType ( /end ) to finish buying.')
        else:
            query.message.reply_text('You dont have enough gold or there is no more card in the pile.')
    if query.data == 'Copper':
        if (buy_turn == True) and (gold - 0 >= 0):
            buy_temp.append('Copper')
            gold -= 0
            buy_time -= 1
            query.edit_message_text('You have bought Copper.\nType /buy to continue buying cards\nType /action to use cards\nType ( /end ) to finish buying.')
        else:
            query.message.reply_text('You dont have enough gold or it is not your turn.')
    if query.data == 'Silver':
        if (buy_turn == True) and (gold - 3 >= 0):
            buy_temp.append('Silver')
            gold -= 3
            buy_time -= 1
            query.edit_message_text('You have bought Silver.\nType /buy to continue buying cards\nType /action to use cards\nType ( /end ) to finish buying.')
        else:
            query.message.reply_text('You dont have enough gold or it is not your turn.')
    if query.data=='Witch':
        if (buy_turn == True) and (gold - 5 >= 0) and (Witchcard>0):
            buy_temp.append('Witch')
            gold -= 3
            buy_time -= 1
            Witchcard-=1
            query.edit_message_text('You have bought Witch .\nType /buy to continue buying cards\nType /action to use cards\nType ( /end ) to finish buying.')
        else:
            query.message.reply_text('You dont have enough gold or there is no more card in the pile.')
    if query.data=="Village":
        if (buy_turn == True) and (gold - 3 >= 0) and (Villagecard>0):
            buy_temp.append('Village')
            gold -= 3
            buy_time -= 1
            Villagecard-=1
            query.edit_message_text('You have bought Village .\nType /buy to continue buying cards\nType /action to use cards\nType ( /end ) to finish buying.')
        else:
            query.message.reply_text('You dont have enough gold or there is no more card in the pile.')
    if query.data=="Courtyard":
        if (buy_turn == True) and (gold - 2 >= 0) and (Courtyardcard>0):
            buy_temp.append('Courtyard')
            gold -= 2
            buy_time -= 1
            Courtyardcard-=1
            query.edit_message_text('You have bought Courtyard .\nType /buy to continue buying cards\nType /action to use cards\nType ( /end ) to finish buying.')
        else:
            query.message.reply_text('You dont have enough gold or there is no more card in the pile.')
    if query.data=='Gold':
        if (buy_turn == True) and (gold - 6 >= 0):
            buy_temp.append('Gold')
            gold -= 6
            buy_time -= 1
            query.edit_message_text('You have bought Gold .\nType /buy to continue buying cards\nType /action to use cards\nType ( /end ) to finish buying.')
        else:
            query.message.reply_text('You dont have enough gold or it is not your turn.')
    if query.data=="Harbinger":
        if (buy_turn == True) and (gold - 3 >= 0) and(Harbingercard>0):
            buy_temp.append('Harbinger')
            gold -= 3
            buy_time -= 1
            Harbingercard-=1
            query.edit_message_text('You have bought Harbinger .\nType /buy to continue buying cards\nType /action to use cards\nType ( /end ) to finish buying.')
        else:
            query.message.reply_text('You dont have enough gold or it is not your turn.')
    if query.data=="Laboratory":
        if (buy_turn == True) and (gold - 5 >= 0) and(Laboratorycard>0):
            buy_temp.append('Laboratory')
            gold -= 5
            buy_time -= 1
            Laboratorycard-=1
            query.edit_message_text('You have bought Laboratory .\nType /buy to continue buying cards\nType /action to use cards\nType ( /end ) to finish buying.')
        else:
            query.message.reply_text('You dont have enough gold or there is no more card in the pile.')
    if query.data=="Workshop":
        if (buy_turn == True) and (gold - 3 >= 0) and(Workshopcard>0):
            buy_temp.append('Workshop')
            gold -= 3
            buy_time -= 1
            Workshopcard-=1
            query.edit_message_text('You have bought Workshop .\nType /buy to continue buying cards\nType /action to use cards\nType ( /end ) to finish buying.')
        else:
            query.message.reply_text('You dont have enough gold or there is no more card in the pile.')
    #end of buy section
    if query.data=='usevillage':
        if action>0:
            action-=1
            action +=2
            if turn_count == 1:
                hand.remove('Village')
                grave.append('Village')
                temp = random.choice(deckplayer1)
                hand.append(temp)
                if temp == 'Copper':
                    gold += 1
                elif temp == 'Silver':
                    gold += 2
                elif temp == 'Gold':
                    gold += 3
                query.edit_message_text('You have draw [' + str(temp) + ']  and you now have ' + str(action) + ' action.\nType /action to continue using cards.\nType /buy to buy cards\nType /end to end.')
            elif turn_count == 2:
                hand2.remove('Village')
                grave2.append('Village')
                temp = random.choice(deckplayer2)
                hand2.append(temp)
                if temp == 'Copper':
                    gold += 1
                elif temp == 'Silver':
                    gold += 2
                elif temp == 'Gold':
                    gold += 3
                query.edit_message_text('You have draw [' + str(temp) + '] and you now have ' + str(action) + ' action.\nType /action to continue using cards.\nType /buy to buy cards\nType /end to end.')
            elif turn_count == 3:
                hand3.remove('Village')
                grave3.append('Village')
                temp = random.choice(deckplayer3)
                hand3.append(temp)
                if temp == 'Copper':
                    gold += 1
                elif temp == 'Silver':
                    gold += 2
                elif temp == 'Gold':
                    gold += 3
                query.edit_message_text('You have draw [' + str(temp) + '] and you now have ' + str(action) + ' action.\nType /action to continue using cards.\nType /buy to buy cards\nType /end to end.')
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
                if temp == 'Copper':
                    gold += 1
                elif temp == 'Silver':
                    gold += 2
                elif temp == 'Gold':
                    gold += 3
                if tempp == 'Copper':
                    gold += 1
                elif tempp == 'Silver':
                    gold += 2
                elif tempp == 'Gold':
                    gold += 3
                query.edit_message_text('You have draw [' + str(temp) + '] and [' + str(tempp) + '] and you now have ' + str(action) + ' action.\nEveryone now get a Curse\nType /buy to buy cards\nType /action to continue using cards.\nType /end to end.')
            elif turn_count == 2:
                hand2.remove('Witch')
                grave2.append('Witch')
                grave.append('Curse')
                grave3.append('Curse')
                temp = random.choice(deckplayer2)
                hand2.append(temp)
                tempp = random.choice(deckplayer2)
                hand2.append(tempp)
                if temp == 'Copper':
                    gold += 1
                elif temp == 'Silver':
                    gold += 2
                elif temp == 'Gold':
                    gold += 3
                if tempp == 'Copper':
                    gold += 1
                elif tempp == 'Silver':
                    gold += 2
                elif tempp == 'Gold':
                    gold += 3
                query.edit_message_text('You have draw [' + str(temp) + '] and [' + str(tempp) + '] and you now have ' + str(action) + ' action.\nEveryone now get a Curse\nType /buy to buy cards\nType /action to continue using cards.\nType /end to end.')
            elif turn_count == 3:
                hand3.remove('Witch')
                grave3.append('Witch')
                grave.append('Curse')
                grave2.append('Curse')
                temp = random.choice(deckplayer3)
                hand3.append(temp)
                tempp = random.choice(deckplayer3)
                hand3.append(tempp)
                if temp == 'Copper':
                    gold += 1
                elif temp == 'Silver':
                    gold += 2
                elif temp == 'Gold':
                    gold += 3
                if tempp == 'Copper':
                    gold += 1
                elif tempp == 'Silver':
                    gold += 2
                elif tempp == 'Gold':
                    gold += 3
                query.edit_message_text('You have draw [' + str(temp) + '] and [' + str(tempp) + '] and you now have ' + str(action) + ' action.\nEveryone now get a Curse\nType /buy to buy cards\nType /action to continue using cards.\nType /end to end.')
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
                if temp == 'Copper':
                    gold += 1
                elif temp == 'Silver':
                    gold += 2
                elif temp == 'Gold':
                    gold += 3
                if tempp == 'Copper':
                    gold += 1
                elif tempp == 'Silver':
                    gold += 2
                elif tempp == 'Gold':
                    gold += 3
                if temppp == 'Copper':
                    gold += 1
                elif temppp == 'Silver':
                    gold += 2
                elif temppp == 'Gold':
                    gold += 3
                for i in range(len(hand)):
                    c_temp = hand[i]
                    if c_temp == 'Village':
                        keyboard.append([InlineKeyboardButton('Village', callback_data="c_village")])
                    elif c_temp == 'Witch':
                        keyboard.append([InlineKeyboardButton("Witch", callback_data="c_witch")])
                    elif c_temp == 'Courtyard':
                        keyboard.append([InlineKeyboardButton("Courtyard", callback_data="c_courtyard")])
                    elif c_temp == 'Copper':
                        keyboard.append([InlineKeyboardButton("Copper", callback_data="c_copper")])
                    elif c_temp == 'Silver':
                        keyboard.append([InlineKeyboardButton("Silver", callback_data="c_silver")])
                    elif c_temp == 'Gold':
                        keyboard.append([InlineKeyboardButton('Gold', callback_data="c_gold")])
                    elif c_temp == 'Estates':
                        keyboard.append([InlineKeyboardButton('Estates' , callback_data='c_estates')])
                query.message.reply_text('Cards available : ', reply_markup=reply_markup)
                query.edit_message_text('You have draw ' + str(temp) + ' , ' +str(temppp) + ' and ' + str(tempp) + ' and you now have ' + str(action) + ' action.\nType /buy to buy cards\nType /action to continue using cards.\nType /end to end.')
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
                if temp == 'Copper':
                    gold += 1
                elif temp == 'Silver':
                    gold += 2
                elif temp == 'Gold':
                    gold += 3
                if tempp == 'Copper':
                    gold += 1
                elif tempp == 'Silver':
                    gold += 2
                elif tempp == 'Gold':
                    gold += 3
                if temppp == 'Copper':
                    gold += 1
                elif temppp == 'Silver':
                    gold += 2
                elif temppp == 'Gold':
                    gold += 3
                for i in range(len(hand2)):
                    c_temp = hand2[i]
                    if c_temp == 'Village':
                        keyboard.append([InlineKeyboardButton('Village', callback_data="c_village")])
                    elif c_temp == 'Witch':
                        keyboard.append([InlineKeyboardButton("Witch", callback_data="c_witch")])
                    elif c_temp == 'Courtyard':
                        keyboard.append([InlineKeyboardButton("Courtyard", callback_data="c_courtyard")])
                    elif c_temp == 'Copper':
                        keyboard.append([InlineKeyboardButton("Copper", callback_data="c_copper")])
                    elif c_temp == 'Silver':
                        keyboard.append([InlineKeyboardButton("Silver", callback_data="c_silver")])
                    elif c_temp == 'Gold':
                        keyboard.append([InlineKeyboardButton('Gold', callback_data="c_gold")])
                    elif c_temp == 'Estates':
                        keyboard.append([InlineKeyboardButton('Estates' , callback_data='c_estates')])
                query.message.reply_text('Cards available : ', reply_markup=reply_markup)
                query.edit_message_text('You have draw ' + str(temp) + ' , ' + str(temppp) + ' and ' + str(tempp) + ' and you now have ' + str(action) + ' action.\nType /buy to buy cards\nType /action to continue using cards.\nType /end to end.')
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
                if temp == 'Copper':
                    gold += 1
                elif temp == 'Silver':
                    gold += 2
                elif temp == 'Gold':
                    gold += 3
                if tempp == 'Copper':
                    gold += 1
                elif tempp == 'Silver':
                    gold += 2
                elif tempp == 'Gold':
                    gold += 3
                if temppp == 'Copper':
                    gold += 1
                elif temppp == 'Silver':
                    gold += 2
                elif temppp == 'Gold':
                    gold += 3
                for i in range(len(hand3)):
                    c_temp = hand3[i]
                    if c_temp == 'Village':
                        keyboard.append([InlineKeyboardButton('Village', callback_data="c_village")])
                    elif c_temp == 'Witch':
                        keyboard.append([InlineKeyboardButton("Witch", callback_data="c_witch")])
                    elif c_temp == 'Courtyard':
                        keyboard.append([InlineKeyboardButton("Courtyard", callback_data="c_courtyard")])
                    elif c_temp == 'Copper':
                        keyboard.append([InlineKeyboardButton("Copper", callback_data="c_copper")])
                    elif c_temp == 'Silver':
                        keyboard.append([InlineKeyboardButton("Silver", callback_data="c_silver")])
                    elif c_temp == 'Gold':
                        keyboard.append([InlineKeyboardButton('Gold', callback_data="c_gold")])
                    elif c_temp == 'Estates':
                        keyboard.append([InlineKeyboardButton('Estates' , callback_data='c_estates')])
                query.edit_message_text('You have draw ' + str(temp) + ' , ' + str(temppp) + ' and ' + str(tempp) + ' and you now have ' + str(action) + ' action.\nType /buy to buy cards\nType /action to continue using cards.\nType /end to end.')
            query.message.reply_text('You can put :one: card on top of your deck\nCards availbale:',replymarkup=replymarkup)
        else:
            query.edit_message_text('You dont have enough Action.')
    if query.data == 'useharbinger':
        keyboard = [[]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        if action >0 :
            if turn_count == 1:
                for i in range(len(grave)):
                    h_temp = grave[i]
                    if h_temp == 'Village':
                        keyboard.append([InlineKeyboardButton('Village', callback_data="h_village")])
                    elif h_temp == 'Witch':
                        keyboard.append([InlineKeyboardButton("Witch", callback_data="h_witch")])
                    elif h_temp == 'Courtyard':
                        keyboard.append([InlineKeyboardButton("Courtyard", callback_data="h_courtyard")])
                    elif h_temp == 'Copper':
                        keyboard.append([InlineKeyboardButton("Copper", callback_data="h_copper")])
                    elif h_temp == 'Silver':
                        keyboard.append([InlineKeyboardButton("Silver", callback_data="h_silver")])
                    elif h_temp == 'Gold':
                        keyboard.append([InlineKeyboardButton('Gold', callback_data="h_gold")])
                    elif h_temp == 'Estates':
                        keyboard.append([InlineKeyboardButton('Estates', callback_data='h_estates')])
                    elif h_temp == 'Harbinger':
                        keyboard.append([InlineKeyboardButton('Harbinger', callback_data='h_harbinger')])
                query.edit_message_text('You have ' + str(grave) + ' in your discarded pile,Cards available:',reply_markup=reply_markup)
                hand.remove('Harbinger')
                grave.append('Harbinger')
            elif turn_count ==2 :
                for i in range(len(grave2)):
                    h_temp = grave2[i]
                    if h_temp == 'Village':
                        keyboard.append([InlineKeyboardButton('Village', callback_data="h_village")])
                    elif h_temp == 'Witch':
                        keyboard.append([InlineKeyboardButton("Witch", callback_data="h_witch")])
                    elif h_temp == 'Courtyard':
                        keyboard.append([InlineKeyboardButton("Courtyard", callback_data="h_courtyard")])
                    elif h_temp == 'Copper':
                        keyboard.append([InlineKeyboardButton("Copper", callback_data="h_copper")])
                    elif h_temp == 'Silver':
                        keyboard.append([InlineKeyboardButton("Silver", callback_data="h_silver")])
                    elif h_temp == 'Gold':
                        keyboard.append([InlineKeyboardButton('Gold', callback_data="h_gold")])
                    elif h_temp == 'Estates':
                        keyboard.append([InlineKeyboardButton('Estates', callback_data='h_estates')])
                    elif h_temp == 'Harbinger':
                        keyboard.append([InlineKeyboardButton('Harbinger', callback_data='h_harbinger')])
                grave2.append('Harbinger')
                hand2.remove('Harbinger')
                query.edit_message_text('You have ' + str(grave2) + ' in your discarded pile,Cards availble:',reply_markup=reply_markup)
            elif turn_count == 3 :
                for i in range(len(grave3)):
                    h_temp = grave3[i]
                    if h_temp == 'Village':
                        keyboard.append([InlineKeyboardButton('Village', callback_data="h_village")])
                    elif h_temp == 'Witch':
                        keyboard.append([InlineKeyboardButton("Witch", callback_data="h_witch")])
                    elif h_temp == 'Courtyard':
                        keyboard.append([InlineKeyboardButton("Courtyard", callback_data="h_courtyard")])
                    elif h_temp == 'Copper':
                        keyboard.append([InlineKeyboardButton("Copper", callback_data="h_copper")])
                    elif h_temp == 'Silver':
                        keyboard.append([InlineKeyboardButton("Silver", callback_data="h_silver")])
                    elif h_temp == 'Gold':
                        keyboard.append([InlineKeyboardButton('Gold', callback_data="h_gold")])
                    elif h_temp == 'Estates':
                        keyboard.append([InlineKeyboardButton('Estates', callback_data='h_estates')])
                    elif h_temp == 'Harbinger':
                        keyboard.append([InlineKeyboardButton('Harbinger', callback_data='h_harbinger')])
                grave3.append('Harbinger')
                hand.remove('Harbinger')
                query.edit_message_text('You have ' + str(grave3) + ' in your discarded pile,Cards available',reply_markup=reply_markup)
        else:
            query.message.reply_text('You dont have enough action')
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
                if temp == 'Copper':
                    gold += 1
                elif temp == 'Silver':
                    gold += 2
                elif temp == 'Gold':
                    gold += 3
                if tempp == 'Copper':
                    gold += 1
                elif tempp == 'Silver':
                    gold += 2
                elif tempp == 'Gold':
                    gold += 3
                query.edit_message_text('You have draw [' + str(temp) + '] and [' + str(tempp) + '] and you now have ' + str(action) + ' action.\nType /buy to buy cards\nType /action to continue using cards.\nType /end to end.')
            elif turn_count == 2:
                hand2.remove('Laboratory')
                grave2.append('Laboratory')
                temp = random.choice(deckplayer2)
                hand2.append(temp)
                tempp = random.choice(deckplayer2)
                hand2.append(tempp)
                if temp == 'Copper':
                    gold += 1
                elif temp == 'Silver':
                    gold += 2
                elif temp == 'Gold':
                    gold += 3
                if tempp == 'Copper':
                    gold += 1
                elif tempp == 'Silver':
                    gold += 2
                elif tempp == 'Gold':
                    gold += 3
                query.edit_message_text('You have draw [' + str(temp) + '] and [' + str(tempp) + '] and you now have ' + str(action) + ' action.\nType /buy to buy cards\nType /action to continue using cards.\nType /end to end.')
            elif turn_count == 3:
                hand3.remove('Laboratory')
                grave3.append('Laboratory')
                temp = random.choice(deckplayer3)
                hand3.append(temp)
                tempp = random.choice(deckplayer3)
                hand3.append(tempp)
                if temp == 'Copper':
                    gold += 1
                elif temp == 'Silver':
                    gold += 2
                elif temp == 'Gold':
                    gold += 3
                if tempp == 'Copper':
                    gold += 1
                elif tempp == 'Silver':
                    gold += 2
                elif tempp == 'Gold':
                    gold += 3
                query.edit_message_text('You have draw [' + str(temp) + '] and [' + str(tempp) + '] and you now have ' + str(action) + ' action.\nType /buy to buy cards\nType /action to continue using cards.\nType /end to end.')
            else:
                query.edit_message_text('You dont have enough Action.')
    if query.data == 'useworkshop':
        keyboard=[[]]
        reply_markup=InlineKeyboardMarkup(keyboard)
        if action>0:
            action -=1
            if turn_count == 1:
                hand.remove('Workshop')
                grave.append('Workshop')
            elif turn_count == 2:
                hand2.remove('Workshop')
                grave2.append('Workshop')
            elif turn_count == 3:
                hand3.remove('Workshop')
                grave3.append('Workshop')

            keyboard.append([InlineKeyboardButton("Workshop", callback_data="w_workshop")])
            keyboard.append([InlineKeyboardButton("Laboratory", callback_data="w_laboratory")])
            keyboard.append([InlineKeyboardButton("Harbinger", callback_data="w_harbinger")])
            keyboard.append([InlineKeyboardButton("Village", callback_data="w_village")])
            keyboard.append([InlineKeyboardButton("Silver", callback_data="w_silver")])
            keyboard.append([InlineKeyboardButton("Courtyard", callback_data="w_courtyard")])
            query.edit_message_text('Cards availble',reply_markup=reply_markup)
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
        query.edit_message_text('Witch is placed on top of your deck.\nType /buy to buy cards\nType /action to continue using cards.\nType /end to end.')
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
        query.edit_message_text('Village is placed on top of your deck.\nType /buy to buy cards\nType /action to continue using cards.\nType /end to end.')
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
        query.edit_message_text('Courtyard is placed on top of your deck.\nType /buy to buy cards\nType /action to continue using cards.\nType /end to end.')
    if query.data == 'c_copper':
        if turn_count == 1:
            temp_deck_top.append('Copper')
            hand.remove('Copper')
        elif turn_count == 2:
            temp_deck_top2.append('Copper')
            hand2.remove('Copper')
        elif turn_count == 3:
            temp_deck_top3.append('Copper')
            hand3.remove('Copper')
        query.edit_message_text('Copper is placed on top of your deck.\nType /buy to buy cards\nType /action to continue using cards.\nType /end to end.')
    if query.data == 'c_silver':
        if turn_count == 1:
            temp_deck_top.append('Silver')
            hand.remove('Silver')
        elif turn_count == 2:
            temp_deck_top2.append('Silver')
            hand2.remove('Silver')
        elif turn_count == 3:
            temp_deck_top3.append('Silver')
            hand3.remove('Silver')
        query.edit_message_text('Silver is placed on top of your deck.\nType /buy to buy cards\nType /action to continue using cards.\nType /end to end.')
    if query.data == 'c_gold':
        if turn_count == 1:
            temp_deck_top.append('Gold')
            hand.remove('Gold')
        elif turn_count == 2:
            temp_deck_top2.append('Gold')
            hand2.remove('Gold')
        elif turn_count == 3:
            temp_deck_top3.append('Gold')
            hand3.remove('Gold')
        query.edit_message_text('Gold is placed on top of your deck.\nType /buy to buy cards\nType /action to continue using cards.\nType /end to end.')
    if query.data == 'c_estates':
        if turn_count == 1:
            temp_deck_top.append('Estates')
            hand.remove('Estates')
        elif turn_count == 2:
            temp_deck_top2.append('Estates')
            hand2.remove('Estates')
        elif turn_count == 3:
            temp_deck_top3.append('Estates')
            hand3.remove('Estates')
        query.edit_message_text('Estates is placed on top of your deck.\nType /buy to buy cards\nType /action to continue using cards.\nType /end to end.')
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
        query.edit_message_text('Witch is placed on top of your deck.\nType /buy to buy cards\nType /action to continue using cards.\nType /end to end.')
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
        query.edit_message_text('Village is placed on top of your deck.\nType /buy to buy cards\nType /action to continue using cards.\nType /end to end.')
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
        query.edit_message_text('Courtyard is placed on top of your deck.\nType /buy to buy cards\nType /action to continue using cards.\nType /end to end.')
    if query.data == 'h_copper':
        if turn_count == 1:
            temp_deck_top.append('Copper')
            grave.remove('Copper')
        elif turn_count == 2:
            temp_deck_top2.append('Copper')
            grave2.remove('Copper')
        elif turn_count == 3:
            temp_deck_top3.append('Copper')
            grave3.remove('Copper')
        query.edit_message_text('Copper is placed on top of your deck.\nType /buy to buy cards\nType /action to continue using cards.\nType /end to end.')
    if query.data == 'h_silver':
        if turn_count == 1:
            temp_deck_top.append('Silver')
            grave.remove('Silver')
        elif turn_count == 2:
            temp_deck_top2.append('Silver')
            grave2.remove('Silver')
        elif turn_count == 3:
            temp_deck_top3.append('Silver')
            grave3.remove('Silver')
        query.edit_message_text('Silver is placed on top of your deck.\nType /buy to buy cards\nType /action to continue using cards.\nType /end to end.')
    if query.data == 'h_gold':
        if turn_count == 1:
            temp_deck_top.append('Gold')
            grave.remove('Gold')
        elif turn_count == 2:
            temp_deck_top2.append('Gold')
            grave2.remove('Gold')
        elif turn_count == 3:
            temp_deck_top3.append('Gold')
            grave3.remove('Gold')
        query.edit_message_text('Gold is placed on top of your deck.\nType /buy to buy cards\nType /action to continue using cards.\nType /end to end.')
    if query.data == 'h_estates':
        if turn_count == 1:
            temp_deck_top.append('Estates')
            grave.remove('Estates')
        elif turn_count == 2:
            temp_deck_top2.append('Estates')
            grave2.remove('Estates')
        elif turn_count == 3:
            temp_deck_top3.append('Estates')
            grave3.remove('Estates')
        query.edit_message_text('Estates is placed on top of your deck.\nType /buy to buy cards\nType /action to continue using cards.\nType /end to end.')
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
        query.edit_message_text('Harbinger is placed on top of your deck.\nType /buy to buy cards\nType /action to continue using cards.\nType /end to end.')
    if query.data == 'w_village':
        if turn_count == 1:
            grave.append('Village')
        elif turn_count == 2:
            grave2.append('Village')
        elif turn_count == 3:
            grave3.append('Village')
        query.edit_message_text('Village is gained into your discarded pile.\nType /buy to buy cards\nType /action to continue using cards.\nType /end to end.')
    if query.data == 'w_courtyard':
        if turn_count == 1:
            grave.append('Courtyard')
        elif turn_count == 2:
            grave2.append('Courtyard')
        elif turn_count == 3:
            grave3.append('Courtyard')
        query.edit_message_text('Courtyard is gained into your discarded pile.\nType /buy to buy cards\nType /action to continue using cards.\nType /end to end.')
    if query.data == 'w_copper':
        if turn_count == 1:
            grave.append('Copper')
        elif turn_count == 2:
            grave2.append('Copper')
        elif turn_count == 3:
            grave3.append('Copper')
        query.edit_message_text('Copper is gained into your discarded pile.\nType /buy to buy cards\nType /action to continue using cards.\nType /end to end.')
    if query.data == 'w_silver':
        if turn_count == 1:
            grave.append('Silver')
        elif turn_count == 2:
            grave2.append('Silver')
        elif turn_count == 3:
            grave3.append('Silver')
        query.edit_message_text('Silver is gained into your discarded pile.\nType /buy to buy cards\nType /action to continue using cards.\nType /end to end.')
    if query.data == 'w_workshop':
        if turn_count == 1:
            grave.append('Workshop')
        elif turn_count == 2:
            grave2.append('Workshop')
        elif turn_count == 3:
            grave3.append('Workshop')
        query.edit_message_text('Workshop is gained into your discarded pile.\nType /buy to buy cards\nType /action to continue using cards.\nType /end to end.')
    if query.data == 'w_harbinger':
        if turn_count == 1:
            grave.append('Harbinger')
        elif turn_count == 2:
            grave2.append('Harbinger')
        elif turn_count == 3:
            grave3.append('Harbinger')
        query.edit_message_text('Harbinger is gained into your discarded pile.\nType /buy to buy cards\nType /action to continue using cards.\nType /end to end.')
    if query.data == 'w_laboratory':
        if turn_count == 1:
            grave.append('Laboratory')
        elif turn_count == 2:
            grave2.append('Laboratory')
        elif turn_count == 3:
            grave3.append('Laboratory')
        query.edit_message_text('Laboratory is gained into your discarded pile.\nType /buy to buy cards\nType /action to continue using cards.\nType /end to end.')
	if query.data == 'usemoneylender':
		if turn_count == 1:
			if 'Copper' in hand:
				hand.remove('Copper')
				gold+=3
			elif 'Copper' in hand2:
				hand2.remove('Copper')
				gold+=3
			elif 'Copper' in hand3:
				hand3.remove('Copper')
				gold+=3

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
            update.message.reply_text('Current player list :\n [' + str(user1_name) + ' / ' + str(user2_name) + ' / ' + str(user3_name) + ']\nType /join to join the game.\nType /startgame to start the game.')



def actionphase(bot,update):
    keyboard = [[]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if turn_count == 1:
        bot.sendMessage(chat_id=user1_id,text=str(user1_name) + ', you have : ' + str(hand))
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
        bot.sendMessage(chat_id=user2_id,text=str(user2_name) + ', you have : ' + str(hand2))
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
        bot.sendMessage(chat_id=user3_id,text=str(user3_name) + ', you have : ' + str(hand))
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
    if turn_count == 1:
        bot.sendMessage(chat_id=user1_id,text='You have <' + str(gold) + '> dollar')
    elif turn_count == 2:
        bot.sendMessage(chat_id=user2_id,text='You have <' + str(gold) + '> dollar')
    else:
        bot.sendMessage(chat_id=user3_id,text='You have <' + str(gold) + '> dollar')
    buy_turn = True
    keyboard = [[]]
    if gold >=8:
        keyboard.append([InlineKeyboardButton('Province', callback_data='Province')])
        keyboard.append([InlineKeyboardButton('Gold', callback_data='Gold')])
        keyboard.append([InlineKeyboardButton("Duchy", callback_data="Duchy")])
        keyboard.append([InlineKeyboardButton("Laboratory", callback_data="Laboratory")])
        keyboard.append([InlineKeyboardButton("Witch", callback_data="Witch")])
        keyboard.append([InlineKeyboardButton("Workshop", callback_data="Workshop")])
		keyboard.append([InlineKeyboardButton("Moneylender", callback_data="Moneylender")])
        keyboard.append([InlineKeyboardButton("Harbinger", callback_data="Harbinger")])
        keyboard.append([InlineKeyboardButton("Village", callback_data="Village")])
        keyboard.append([InlineKeyboardButton("Silver", callback_data="Silver")])
        keyboard.append([InlineKeyboardButton("Courtyard", callback_data="Courtyard")])
        keyboard.append([InlineKeyboardButton("Copper", callback_data="Copper")])
        update.message.reply_text('Buy Province for 8 dollar\nBuy Gold costs 6 dollars\nBuy Duchy For 5 dollar\nBuy Laboratory costs 5 dollars\nBuy Witch costs 5 dollars\nBuy Moneylender costs 4 dollar\nBuy Workshop costs 4 dollar\nBuy Harbinger costs 3 dollars\nBuy Village costs 3 dollars\nBuy Silver costs 3 dollars\nBuy Courtyard costs 2 dollar\nBuy Copper for 0 dollar')
    elif gold == 7 or gold == 6 :
        keyboard.append([InlineKeyboardButton('Gold', callback_data='Gold')])
        keyboard.append([InlineKeyboardButton("Duchy", callback_data="Duchy")])
        keyboard.append([InlineKeyboardButton("Laboratory", callback_data="Laboratory")])
        keyboard.append([InlineKeyboardButton("Witch", callback_data="Witch")])
        keyboard.append([InlineKeyboardButton("Workshop", callback_data="Workshop")])
		keyboard.append([InlineKeyboardButton("Moneylender", callback_data="Moneylender")])
        keyboard.append([InlineKeyboardButton("Harbinger", callback_data="Harbinger")])
        keyboard.append([InlineKeyboardButton("Village", callback_data="Village")])
        keyboard.append([InlineKeyboardButton("Silver", callback_data="Silver")])
        keyboard.append([InlineKeyboardButton("Courtyard", callback_data="Courtyard")])
        keyboard.append([InlineKeyboardButton("Copper", callback_data="Copper")])
        update.message.reply_text('Buy Gold costs 6 dollars\nBuy Duchy For 5 dollar\nBuy Laboratory costs 5 dollars\nBuy Witch costs 5 dollars\nBuy Moneylender costs 4 dollar\nBuy Workshop costs 4 dollar\nBuy Harbinger costs 3 dollars\nBuy Village costs 3 dollars\nBuy Silver costs 3 dollars\nBuy Courtyard costs 2 dollar\nBuy Copper for 0 dollar')
    elif gold == 5:
        keyboard.append([InlineKeyboardButton("Duchy", callback_data="Duchy")])
        keyboard.append([InlineKeyboardButton("Laboratory", callback_data="Laboratory")])
        keyboard.append([InlineKeyboardButton("Witch", callback_data="Witch")])
        keyboard.append([InlineKeyboardButton("Workshop", callback_data="Workshop")])
		keyboard.append([InlineKeyboardButton("Moneylender", callback_data="Moneylender")])
        keyboard.append([InlineKeyboardButton("Harbinger", callback_data="Harbinger")])
        keyboard.append([InlineKeyboardButton("Village", callback_data="Village")])
        keyboard.append([InlineKeyboardButton("Silver", callback_data="Silver")])
        keyboard.append([InlineKeyboardButton("Courtyard", callback_data="Courtyard")])
        keyboard.append([InlineKeyboardButton("Copper", callback_data="Copper")])
        update.message.reply_text('Buy Duchy For 5 dollar\nBuy Witch costs 5 dollars\nBuy Laboratory costs 5 dollar\nBuy Workshop costs 3 dollar\nBuy Harbinger costs 3 dollars\nBuy Village costs 3 dollars\nBuy Silver costs 3 dollars\nBuy Courtyard costs 2 dollar\nBuy Copper for 0 dollar')
    elif gold == 4:
        update.message.reply_text('Buy Moneylender costs 4 dollar\nBuy Workshop costs 3 dollar\nBuy Harbinger costs 3 dollars\nBuy Village costs 3 dollars\nBuy Silver costs 3 dollars\nBuy Courtyard costs 2 dollar\nBuy Copper for 0 dollar')
		keyboard.append([InlineKeyboardButton("Moneylender", callback_data="Moneylender")])
		keyboard.append([InlineKeyboardButton("Workshop", callback_data="Workshop")])
        keyboard.append([InlineKeyboardButton("Harbinger", callback_data="Harbinger")])
        keyboard.append([InlineKeyboardButton("Village", callback_data="Village")])
        keyboard.append([InlineKeyboardButton("Silver", callback_data="Silver")])
        keyboard.append([InlineKeyboardButton("Courtyard", callback_data="Courtyard")])
        keyboard.append([InlineKeyboardButton("Copper", callback_data="Copper")])
    elif gold == 3 :
        update.message.reply_text('Buy Harbinger costs 3 dollars\nBuy Workshop costs 3 dollar\nBuy Village costs 3 dollars\nBuy Silver costs 3 dollars\nBuy Courtyard costs 2 dollar\nBuy Copper for 0 dollar')
        keyboard.append([InlineKeyboardButton("Workshop", callback_data="Workshop")])
        keyboard.append([InlineKeyboardButton("Harbinger", callback_data="Harbinger")])
        keyboard.append([InlineKeyboardButton("Village", callback_data="Village")])
        keyboard.append([InlineKeyboardButton("Silver", callback_data="Silver")])
        keyboard.append([InlineKeyboardButton("Courtyard", callback_data="Courtyard")])
        keyboard.append([InlineKeyboardButton("Copper", callback_data="Copper")])
    elif gold == 2:
        update.message.reply_text('Buy Courtyard costs 2 dollar\nBuy Copper for 0 dollar')
        keyboard.append([InlineKeyboardButton("Courtyard", callback_data="Courtyard")])
        keyboard.append([InlineKeyboardButton("Estates", callback_data="Estates")])
        keyboard.append([InlineKeyboardButton("Copper", callback_data="Copper")])
    elif gold == 0:
        update.message.reply_text('Buy Copper for 0 dollar')
        keyboard.append([InlineKeyboardButton("Copper", callback_data="Copper")])
    update.message.reply_text('Cards available : ',reply_markup=InlineKeyboardMarkup(keyboard))



def end(bot,update):
    global chat_id
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
    global gold1, gold2, gold3, points, points2, points3, buy_turn, buy_time, action, user1_id, user1_name, user2_id, user2_name, user3_id, user3_name, current_player, inlinehand, courtyard_temp, turn_count, turnnum, start_game
    global turn
    global hand
    global user1_tag, user2_tag, user3_tag
    global Provincecard, Duchycard, Estatescard, Villagecard, Laboratorycard, Workshopcard, Harbingercard, Courtyardcard, Witchcard
    global temp_deck_top, temp_deck_top2, temp_deck_top3
    global Endgame
    turn = False
    turnnum += 1
    turn=False
    action = 1
    gold = 0
    if Endgame == True:
        if turn_count == 1:
            grave += buy_temp
        elif turn_count == 2:
            grave2 += buy_temp
        elif turn_count == 3:
            grave3 += buy_temp
        update.message.reply_text('Game has ended.')
        grave += hand
        grave += deckplayer1
        grave += temp_deck_top
        for i in range(len(grave)):
            temp = grave[i]
            if temp == 'Estates':
                points += 1
            elif temp == 'Duchy':
                points += 3
            elif temp == 'Province':
                points += 5
        grave2 += hand
        grave2 += deckplayer1
        grave2 += temp_deck_top
        for i in range(len(grave2)):
            temp = grave2[i]
            if temp == 'Estates':
                points2 += 1
            elif temp == 'Duchy':
                points2 += 3
            elif temp == 'Province':
                points2 += 5
        grave3 += hand
        grave3 += deckplayer1
        grave3 += temp_deck_top
        for i in range(len(grave3)):
            temp = grave3[i]
            if temp == 'Estates':
                points3 += 1
            elif temp == 'Duchy':
                points3 += 3
            elif temp == 'Province':
                points3 += 5
        if user3_name == 'null':
            update.message.reply_text(user1_name+' have ' + str(points)+' points\n'+user2_name+' have'+ str(points2)+' points')
        else:
            update.message.reply_text(user1_name + ' have ' + str(points) + ' points\n' + user2_name + ' have' + str(points2) + ' points\n'+user3_name+'have'+ str(points3)+'points')
        if points >(points2 and points3):
            update.message.reply_text('The winner is '+ user1_name +'!')
        elif points2>(points and points3):
            update.message.reply_text('The winner is ' + user2_name + '!')
        elif points3>(points and points2):
            update.message.reply_text('The winner is ' + user3_name + '!')
        update.message.reply_text('Game has ended, Type /join to join a new game.')
        deckplayer1 = ['Copper', 'Copper', 'Copper', 'Copper', 'Copper', 'Copper', 'Copper', 'Estates', 'Estates',
                       'Estates']
        deckplayer2 = ['Copper', 'Copper', 'Copper', 'Copper', 'Copper', 'Copper', 'Copper', 'Estates', 'Estates',
                       'Estates']
        deckplayer3 = ['Copper', 'Copper', 'Copper', 'Copper', 'Copper', 'Copper', 'Copper', 'Estates', 'Estates',
                       'Estates']
        grave = []
        grave2 = []
        grave3 = []
        buy_temp = []
        hand = []
        hand2 = []
        hand3 = []
        temp_deck_top = []
        temp_deck_top2 = []
        temp_deck_top3 = []
        gold = 0
        gold1 = 0
        gold2 = 0
        gold3 = 0
        points = 0
        points2 = 0
        points3 = 0
        turn = False
        buy_turn = False
        buy_time = 1
        action = 1
        chat_id = 'null'
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
        inlinehand = []
        turn_count = 0
        turnnum = 0
        start_game = False
        Provincecard = 10
        Duchycard = 10
        Estatescard = 10
        Villagecard = 10
        Harbingercard = 10
        Laboratorycard = 10
        Witchcard = 10
        Workshopcard = 10
        Courtyardcard = 10
        Endgame = False
    elif  turn_count == 1 :
        if str(update.message.from_user.id) != user1_id:
            update.message.reply_text('It is not your turn.')
        else:
            grave += hand
            grave += buy_temp
            hand = []
            buy_temp = []
            if str(update.message.from_user.id) == user1_id and turn_count == 1:
                gold1 = 0
                if temp_deck_top != []:
                    c = temp_deck_top[0]
                    hand.append(c)
                    temp_deck_top = []
                    for i in range(4):
                        temp = (random.choice(deckplayer1))
                        hand.append(temp)
                        deckplayer1.remove(temp)
                        if temp == 'Copper':
                            gold1 += 1
                        elif temp == 'Silver':
                            gold1 += 2
                        elif temp == 'Gold':
                            gold1 += 3
                        if deckplayer1 == []:
                            deckplayer1 = grave
                            grave = []
                        turn = True
                else:
                    for i in range(5):
                        temp = (random.choice(deckplayer1))
                        hand.append(temp)
                        deckplayer1.remove(temp)
                        if temp == 'Copper':
                            gold1 += 1
                        elif temp == 'Silver':
                            gold1 += 2
                        elif temp == 'Gold':
                            gold1 += 3
                        if deckplayer1 == []:
                            deckplayer1 = grave
                            grave = []
                        turn = True
            bot.sendMessage(chat_id=str(user1_id), text='Turn '+ str(turnnum) + '\nYou got ' + str(hand) + 'after shufle.' )
            gold = gold2
            update.message.reply_text(str(user1_name) + ' is done!\nIts now your turn , ' + str(user2_name) + ' @' + user2_tag +'\nType ( /action ) or ( /buy ) to proceed')
            turn_count += 1
    elif turn_count == 2 :
        if str(update.message.from_user.id) != user2_id:
            update.message.reply_text('It is not your turn.')
        else:
            gold2 = 0
            grave2 += hand2
            grave2 += buy_temp
            hand2 = []
            buy_temp = []
            if temp_deck_top2 != []:
                c = temp_deck_top2[0]
                hand2.append(c)
                temp_deck_top2 = []
                for i in range(4):
                    temp = (random.choice(deckplayer2))
                    hand2.append(temp)
                    deckplayer2.remove(temp)
                    if temp == 'Copper':
                        gold2 += 1
                    elif temp == 'Silver':
                        gold2 += 2
                    elif temp == 'Gold':
                        gold2 += 3
                    if deckplayer1 == []:
                        deckplayer2 = grave2
                        grave2 = []
                    turn = True
            else:
                for i in range(5):
                    temp = (random.choice(deckplayer2))
                    hand2.append(temp)
                    deckplayer2.remove(temp)
                    if temp == 'Copper':
                        gold2 += 1
                    elif temp == 'Silver':
                        gold2 += 2
                    elif temp == 'Gold':
                        gold2 += 3
                    if deckplayer2 == []:
                        deckplayer2 = grave2
                        grave2 = []
                    turn = True
            turn_count += 1
            bot.sendMessage(chat_id=str(user2_id), text='Turn '+ str(turnnum) + '\nYou got ' + str(hand2) + 'after shufle.')
            if user3_name == 'null' and turn_count == 3:
                turn_count = 1
            if turn_count == 1:
                gold = gold1
                update.message.reply_text(str(user2_name) + ' is done!\nIts now your turn , ' + str( user1_name) + ' @' + user1_tag + '\nType ( /action ) or ( /buy ) to proceed')
            elif turn_count == 3:
                gold=gold3
                update.message.reply_text(str(user2_name) + ' is done!\nIts now your turn , ' + str(user3_name) + ' @' + user3_tag + '\nType ( /action ) or ( /buy ) to proceed')
    elif turn_count == 3 :
        if str(update.message.from_user.id) != user3_id:
            update.message.reply_text('It is not your turn.')
        else:
            gold3 = 0
            grave3 += hand3
            grave3 += buy_temp
            hand3 = []
            buy_temp = []
            if temp_deck_top != []:
                c = temp_deck_top3[0]
                hand3.append(c)
                temp_deck_top3 = []
                for i in range(4):
                    temp = (random.choice(deckplayer3))
                    hand3.append(temp)
                    deckplayer3.remove(temp)
                    if temp == 'Copper':
                        gold3 += 1
                    elif temp == 'Silver':
                        gold3 += 2
                    elif temp == 'Gold':
                        gold3 += 3
                    if deckplayer3 == []:
                        deckplayer3 = grave3
                        grave3 = []
                    turn = True
            else:
                for i in range(5):
                    temp = (random.choice(deckplayer3))
                    hand3.append(temp)
                    deckplayer3.remove(temp)
                    if temp == 'Copper':
                        gold3 += 1
                    elif temp == 'Silver':
                        gold3 += 2
                    elif temp == 'Gold':
                        gold3 += 3
                    if deckplayer3 == []:
                        deckplayer3 = grave3
                        grave3 = []
                    turn = True
            bot.sendMessage(chat_id=str(user3_id), text='Turn '+ str(turnnum) + '\nYou got ' + str(hand3) + 'after shufle.')
            update.message.reply_text(str(user3_name) + ' is done!\nIts now your turn , ' + str(user1_name) + ' @' + user1_tag + '\nType ( /action ) or ( /buy ) to proceed')
            gold3 = 0
            gold=gold1
            turn_count += 1
            if turn_count == 4:
                turn_count = 1
    else:
        update.message.reply_text('You havent join the game yet.')


def playerlist(bot,update):
    update.message.reply_text('Current player list :\n [' + str(user1_name) + ' / ' + str(user2_name) + ' / ' + str(user3_name) + ']\nSupport Max to 3 player')

def money(bot,update):
    update.message.reply_text('You have <' + str(gold) + '> dollar')

def point(bot,update):
    update.message.reply_text('You have <' + str(points) + '> points')

def reset(bot,update):
    global chat_id
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
    global gold1,gold2,gold3,points,points2,points3,buy_turn,buy_time,action,user1_id,user1_name,user2_id,user2_name,user3_id,user3_name,current_player,inlinehand,courtyard_temp,turn_count,turnnum,start_game
    global turn
    global hand
    global user1_tag,user2_tag,user3_tag
    global Provincecard, Duchycard, Estatescard, Villagecard, Laboratorycard, Workshopcard, Harbingercard, Courtyardcard,Witchcard
    global temp_deck_top,temp_deck_top2,temp_deck_top3
    global Endgame
    deckplayer1 = ['Copper', 'Copper', 'Copper', 'Copper', 'Copper', 'Copper', 'Copper', 'Estates', 'Estates',
                   'Estates']
    deckplayer2 = ['Copper', 'Copper', 'Copper', 'Copper', 'Copper', 'Copper', 'Copper', 'Estates', 'Estates',
                   'Estates']
    deckplayer3 = ['Copper', 'Copper', 'Copper', 'Copper', 'Copper', 'Copper', 'Copper', 'Estates', 'Estates',
                   'Estates']
    grave = []
    grave2 = []
    grave3 = []
    buy_temp = []
    hand = []
    hand2 = []
    hand3 = []
    temp_deck_top = []
    temp_deck_top2 = []
    temp_deck_top3 = []
    gold = 0
    gold1 = 0
    gold2 = 0
    gold3 = 0
    points = 0
    points2 = 0
    points3 = 0
    turn = False
    buy_turn = False
    buy_time = 1
    action = 1
    chat_id = 'null'
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
    inlinehand = []
    turn_count = 0
    turnnum = 0
    start_game = False
    Provincecard = 10
    Duchycard = 10
    Estatescard = 10
    Villagecard = 10
    Harbingercard = 10
    Laboratorycard = 10
    Witchcard = 10
    Workshopcard = 10
    Courtyardcard = 10
    Endgame = False
    update.message.reply_text('Success')

def status(bot,update):
    update.message.reply_text('Normal\nv 2.0.1 (Close Beta Development)')


def show (bot,update):
    update.message.reply_text('Action:'+str(action)+'\nTurn count is '+str(turn_count)+'\n'+str(hand)+'\n'+str(hand2)+'\n'+str(hand3))
    update.message.reply_text(user1_id+ '\n' +str(update.message.from_user.id))
    update.message.reply_text('Grave\n'+str(grave)+'\n'+str(grave2)+'\n'+str(grave3))
    update.message.reply_text('Deck\n'+str(deckplayer1)+'\n'+str(deckplayer2)+'\n'+str(deckplayer3))

def admin(bot,update):
    update.message.reply_text(chat_id)

def error(bot,update,error):
    logger.warning('Update "%s" caused error "%s"', update, error)

def log(bot,update):
    fp = open('logging.txt', "r")
    lines = fp.readlines()
    fp.close()
    n = len(lines) -20
    for i in range(20):
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

def allcommand(bot,update):
    update.message.reply_text('Command List:\nquick\n/buy\n/end\n/join\n/point\n/money\n/startgame\n/action\n/playerlist\nstatus\nreset\nshow\nlog\nlg')

def start(bot,update):
    update.message.reply_text('Welcome to Dominion Bot!')

def quick(bot,update):
    global Provincecard
    global gold1,gold2,gold3
    Provincecard = 1
    gold1 = 8
    gold2 = 8
    gold3 = 8
    update.message.reply_text('Success')



def main():
    updater = Updater('599551578:AAE709inuNhedfLCwIVKF9fWXJNJ-pqv5lg')
    test = updater.dispatcher
    test.add_handler(CommandHandler('money',money))
    test.add_handler(CommandHandler('point',point))
    test.add_handler(CommandHandler('buy',buy))
    test.add_handler(CommandHandler('end',end))
    test.add_handler(CommandHandler('join',join))
    test.add_handler(CommandHandler('startgame',startgame))
    test.add_handler(CommandHandler('action',actionphase))
    test.add_handler(CommandHandler('playerlist',playerlist))
    test.add_handler(CommandHandler('all',allcommand))
    test.add_handler(RegexHandler('.*status.*',status))
    test.add_handler(RegexHandler('.*reset.*', reset))
    test.add_handler(RegexHandler('admin',admin))
    test.add_handler(RegexHandler('.*show.*',show))
    test.add_handler(RegexHandler('.*log.*',log))
    test.add_handler(RegexHandler('.*lg.*', lg))
    test.add_handler(RegexHandler('.*quick.*',quick))
    test.add_error_handler(error)
    test.add_handler(CallbackQueryHandler(button))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()