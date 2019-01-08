from typing import List
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater,MessageHandler,CommandHandler,RegexHandler,CallbackQueryHandler
import random
import logging
from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)

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
            query.edit_message_text('You have bought Silver.\nType ( /end ) to finish buying.')
    if query.data=='Witch':
        if (buy_turn == True) and (gold - 5 >= 0):
            buy_temp.append('Witch')
            gold -= 3
            buy_time -= 1
            query.edit_message_text('You have bought Witch .\nType ( /end ) to finish buying.')
        else:
            query.message.reply_text('You dont have enough gold or it is not your turn.')
        return (gold, buy_time, buy_temp)
    if query.data=="Village":
        if (buy_turn == True) and (gold - 3 >= 0):
            buy_temp.append('Village')
            gold -= 3
            buy_time -= 1
            query.edit_message_text('You have bought Village .\nType ( /end ) to finish buying.')
        else:
            query.message.reply_text('You dont have enough gold or it is not your turn.')
        return (gold, buy_time, buy_temp)
    if query.data=="Courtyard":
        if (buy_turn == True) and (gold - 2 >= 0):
            buy_temp.append('Courtyard')
            gold -= 2
            buy_time -= 1
            query.edit_message_text('You have bought Courtyard .\nType ( /end ) to finish buying.')
        else:
            query.message.reply_text('You dont have enough gold or it is not your turn.')
        return (gold, buy_time, buy_temp)
    if query.data=='usevillage':
        if action>0:
            action-=1
            action +=2
            if turn_count == 1:
                hand.remove('Village')
                temp = random.choice(deckplayer1)
                hand.append(temp)
                if temp == 'copper':
                    gold += 1
                elif temp == 'silver':
                    gold += 2
                elif temp == 'gold':
                    gold += 3
                query.edit.reply_text('You have draw ' + str(temp) + ' and you now have ' + str(action) + ' action.\nType /use to continue using cards.\nType /buy to buy cards\nType /end to end.')
            elif turn_count == 2:
                hand2.remove('Village')
                temp = random.choice(deckplayer2)
                hand.append(temp)
                if temp == 'copper':
                    gold += 1
                elif temp == 'silver':
                    gold += 2
                elif temp == 'gold':
                    gold += 3
                query.edit.reply_text('You have draw ' + str(temp) + ' and you now have ' + str(action) + ' action.\nType /use to continue using cards.\nType /buy to buy cards\nType /end to end.')
            elif turn_count == 3:
                hand3.remove('Village')
                temp = random.choice(deckplayer3)
                hand.append(temp)
                if temp == 'copper':
                    gold += 1
                elif temp == 'silver':
                    gold += 2
                elif temp == 'gold':
                    gold += 3
                query.message.reply_text('You have draw ' + str(temp) + ' and you now have ' + str(action) + ' action.\nType /use to continue using cards.\nType /buy to buy cards\nType /end to end.')
            else:
                query.message.reply_text('You dont have enough Action.')
    if query.data == 'usewitch':
        if action >0:
            action -= 1
            if turn_count == 1:
                hand.remove('Witch')
                grave2.append('Curse')
                grave3.append('Curse')
                temp = random.choice(deckplayer1)
                hand.append(temp)
                tempp =random.choice(deckplayer1)
                hand.append(tempp)
                query.edit.reply_text('You have draw ' + str(temp) + ' and' + str(tempp) + ' and you now have ' + str(action) + ' action.\nEveryone now get a Curse\nType /buy to buy cards\nType /use to continue using cards.\nType /end to end.')
            elif turn_count == 2:
                hand2.remove('Witch')
                grave1.append('Curse')
                grave3.append('Curse')
                temp = random.choice(deckplayer2)
                hand.append(temp)
                tempp = random.choice(deckplayer2)
                hand.append(tempp)
                query.message.reply_text('You have draw ' + str(temp) + ' and' + str(tempp) + ' and you now have ' + str(action) + ' action.\nEveryone now get a Curse\nType /buy to buy cards\nType /use to continue using cards.\nType /end to end.')
            elif turn_count == 3:
                hand3.remove('Witch')
                grave.append('Curse')
                grave2.append('Curse')
                temp = random.choice(deckplayer3)
                hand.append(temp)
                tempp = random.choice(deckplayer3)
                hand.append(tempp)
                query.edit.reply_text('You have draw ' + str(temp) + ' and ' + str(tempp) + ' and you now have ' + str(action) + ' action.\nEveryone now get a Curse\nType /buy to buy cards\nType /use to continue using cards.\nType /end to end.')
            else:
                query.message.reply_text('You dont have enough Action.')


def join(bot,update):
    global user1_id
    global user2_id
    global user3_id
    global user1_name
    global user2_name
    global user3_name
    if start_game == True:
       update.message.reply_text('The Loby is closed')
    else:
        update.message.reply_text('Welcome ' + str(update.message.from_user.first_name) + str(update.message.from_user.last_name) + ' [ ' + str(update.message.from_user.id) + ' / ' + '@' + str(update.message.from_user.username) + ' ] ')
        if user1_id == 'null':
            user1_id = str(update.message.from_user.id)
            user1_name = str(update.message.from_user.first_name) + str(update.message.from_user.last_name)
        elif user2_id== 'null':
            user2_id = str(update.message.from_user.id)
            user2_name = str(update.message.from_user.first_name) + str(update.message.from_user.last_name)
        elif user3_id == 'null':
            user3_id = str(update.message.from_user.id)
            user3_name = str(update.message.from_user.first_name) + str(update.message.from_user.last_name)
        update.message.reply_text('Current player list :\n [' + str(user1_name) + ' / ' + str(user2_name) + ' / ' + str(user3_name) + ']\nType /join to join the game.\nType /start to start the game.')
    return (user1_id,user2_id,user3_id,user1_name,user2_name,user3_name)

def draw(bot,update):
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
        return(gold,deckplayer1)

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
        update.message.reply_text('Cards available : ', reply_markup=reply_markup)



def buy(bot,update):
    global gold
    global buy_turn
    update.message.reply_text('You have <' + str(gold) + '> dollar')
    buy_turn = True
    keyboard = [[]]
    if gold >= 5:
        update.message.reply_text('Buy Witch cost 5 dollars')
        keyboard.append([InlineKeyboardButton("Witch", callback_data="Witch")])
    if gold >= 4:
        update.message.reply_text('You can buy some cards')
        keyboard.append([InlineKeyboardButton("Some", callback_data="Some")])
    if gold >= 3:
        update.message.reply_text('Buy Village cost 3 dollars')
        keyboard.append([InlineKeyboardButton("Village", callback_data="Village")])
        update.message.reply_text('Buy Silver cost 3 dollars')
        keyboard.append([InlineKeyboardButton("Silver", callback_data="silver")])
    if gold >= 2:
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
    turn = False
    turnnum += 1
    turn=False
    if  turn_count == 1:
        gold = 0
        grave += hand
        grave += buy_temp
        hand = []
        buy_temp = []
    elif turn_count == 2:
        gold2 = 0
        grave2 += hand2
        grave2 += buy_temp
        hand2 = []
        buy_temp = []
    elif turn_count == 3:
        gold3 = 0
        grave3 += hand3
        grave3 += buy_temp
        hand3 = []
        buy_temp = []
    turn_count += 1
    if user3_name == 'null' and turn_count == 3:
        turn_count = 1
    elif turn_count == 4:
        turn_count = 1
    update.message.reply_text(str(update.message.from_user.first_name) + str(update.message.from_user.last_name) + ' [ ' + str(update.message.from_user.id) + ' / ' + '@' + str(update.message.from_user.username) + ' ] ' + 'is done!')
    if turn_count==1:
        update.message.reply_text("Its now your turn , " + str(user1_name) + '\nType /draw')
    elif turn_count==2:
        update.message.reply_text("Its now your turn , " + str(user2_name) + '\nType /draw')
    elif turn_count==3:
        update.message.reply_text("Its now your turn , " + str(user3_name) + '\nType /draw')



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
    return gold

def status(bot,update):
    update.message.reply_text('normal')

def pass_next(bot,update):
    global turn
    global buy_turn
    global action
    global buy_time
    global turn_count
    turn = False
    turn_count += 1
    buy_turn = False
    buy_time = 1
    action = 1
    update.message.reply_text('success')


def admin(bot,update):
    update.message.reply_text('/join\n/start\n/draw')

def error(bot,update,error):
    logger.warning('Update "%s" caused error "%s"', update, error)

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
    test.add_handler(RegexHandler('.*status.*',status))
    test.add_handler(RegexHandler('.*reset.*', reset))
    test.add_handler(RegexHandler('pass',pass_next))
    test.add_handler(RegexHandler('admin',admin))
    test.add_error_handler(error)

    test.add_handler(CallbackQueryHandler(button))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()