from typing import List
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater,MessageHandler,CommandHandler,RegexHandler,CallbackQueryHandler
import random

card_market = ['village','witch','silver','gold']
card = ["copper","silver","gold"]
deckplayer1 = ['copper','copper','copper','copper','copper','copper','copper','estates','estates','estates']
deckplayer2 = ['copper','copper','copper','copper','copper','copper','copper','estates','estates','estates']
deckplayer3=['copper','copper','copper','copper','copper','copper','copper','estates','estates','estates']
grave = []
grave2 = []
grave3 = []
buy_temp = []
buy_temp2 = []
buy_temp3 = []
hand = []
hand2 = []
hand3 = []
gold = 0
gold2 = 0
gold3 = []
points = 0
points2 = []
points3 = []
turn = False
buy_turn = False
buy_time = 1
action = 1
user1_id = 'null'
user2_id = 'null'
user3_id = 'null'
current_player = 1
courtyard_temp = 0
inlinehand=[]

def button(bot,update):
    global gold
    global buy_temp
    global buy_time
    query = update.callback_query
    if query.data=="Witch":
        if (buy_turn == True) and (gold - 5 >= 0):
            buy_temp.append('Witch')
            gold -= 3
            buy_time -= 1
            query.edit_message_text('You have bought Witch . Type ( /end ) to finish buying.')
        else:
            query.message.reply_text('You dont have enough gold or it is not your turn.')
        return (gold, buy_time, buy_temp)
    if query.data=="Village":
        if (buy_turn == True) and (gold - 3 >= 0):
            buy_temp.append('Village')
            gold -= 3
            buy_time -= 1
            query.edit_message_text('You have bought Village . Type ( /end ) to finish buying.')
        else:
            query.message.reply_text('You dont have enough gold or it is not your turn.')
        return (gold, buy_time, buy_temp)
    if query.data=="Courtyard":
        if (buy_turn == True) and (gold - 2 >= 0):
            buy_temp.append('Courtyard')
            gold -= 2
            buy_time -= 1
            query.edit_message_text('You have bought Courtyard . Type ( /end ) to finish buying.')
        else:
            query.message.reply_text('You dont have enough gold or it is not your turn.')
        return (gold, buy_time, buy_temp)

def start(bot,update):
    global user1_id
    global user2_id
    global user3_id
    update.message.reply_text('Welcome ' + str(update.message.from_user.first_name) + str(update.message.from_user.last_name) + ' [ ' + str(update.message.from_user.id) + ' / ' + '@' + str(update.message.from_user.username) + ' ] ')
    if user1_id == 'null':
        user1_id = str(update.message.from_user.id)
    elif user2_id== 'null':
        user2_id = str(update.message.from_user.id)
    elif user3_id == 'null':
        user3_id = str(update.message.from_user.id)
    update.message.from_user('Current player list : ' + str(user1_id) + ' / ' + str(user2_id) + ' / ' + str(user3_id))
    return (user1_id,user2_id,user3_id)


def draw(bot,update):
    global gold
    global points
    global deckplayer1
    global turn
    global hand
    update.message.reply_text(str(update.message.from_user.first_name) + str(update.message.from_user.last_name) + ' [ ' + str(update.message.from_user.id) + ' / ' + '@' + str(update.message.from_user.username) + ' ] ' + ' is drawing.')
    if turn == True:
        update.message.reply_text('Your turn of drawing has ended')
    else:
        if str(update.message.from_user.id) == user1_id:
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
                    turn = True
            update.message.reply_text('You got ' + str(hand) + ' . Type ( /buy ) or ( /use ) to proceed')
        elif str(update.message.from_user.id) == user2_id:
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
                    turn = True
            update.message.reply_text('You got ' + str(hand2) + ' . Type ( /buy ) or ( /use ) to proceed')
        elif str(update.message.from_user.id) == user3_id:
            for i in range(5):
                    temp = (random.choice(deckplayer3))
                    hand.append(temp)
                    deckplayer3.remove(temp)
                    if temp == 'copper':
                        gold += 1
                    elif temp == 'silver':
                        gold += 2
                    elif temp == 'gold':
                        gold += 3
                    if deckplayer3 == []:
                        deckplayer1 = grave3
                    turn = True
            update.message.reply_text('You got ' + str(hand3) + ' . Type ( /buy ) or ( /use ) to proceed')
        else:
            update.message.reply_text('failed')
        return(gold,deckplayer1)

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
        keyboard.append([InlineKeyboardButton("Silver", callback_data="Silver")])
    if gold >= 2:
        update.message.reply_text('Buy Courtyard costs 2 dollar')
        keyboard.append([InlineKeyboardButton("Courtyard", callback_data="Courtyard")])
    update.message.reply_text('Cards available : ',reply_markup=InlineKeyboardMarkup(keyboard))

def end(bot,update):
    global gold
    global grave
    global buy_temp
    global hand
    if update.message.from_user == user1_id:
        gold = 0
        grave += hand
        grave += buy_temp
        hand = []
        buy_temp = []
    elif update.message.from_user == user2_id:
        gold = 0
        grave2 += hand2
        grave2 += buy_temp2
        hand2 = []
        buy_temp2 = []
    elif update.message.from_user == user3_id:
        gold = 0
        grave3 += hand3
        grave3 += buy_temp3
        hand3 = []
        buy_temp3 = []
    update.message.reply_text(str(update.message.from_user.first_name) + str(update.message.from_user.last_name) + ' [ ' + str(update.message.from_user.id) + ' / ' + '@' + str(update.message.from_user.username) + ' ] ' + 'is done!')

def money(bot,update):
    update.message.reply_text('You have <' + str(gold) + '> dollar')

def point(bot,update):
    update.message.reply_text('You have <' + str(points) + '> points')

def reset(bot,update):
    global gold
    global deckplayer1
    global turn
    global hand
    turn = False
    gold = 0
    hand = []
    deckplayer1 = ['copper', 'copper', 'copper', 'copper', 'copper', 'copper', 'copper', 'estates', 'estates', 'estates']
    update.message.reply_text('success')
    return gold

def status(bot,update):
    update.message.reply_text('normal')

def pass_next(bot,update):
    global turn
    global buy_turn
    global action
    global buy_time
    turn = False
    buy_turn = False
    buy_time = 1
    action = 1
    update.message.reply_text('success')


def main():
    updater = Updater('599551578:AAE709inuNhedfLCwIVKF9fWXJNJ-pqv5lg')
    test = updater.dispatcher
    test.add_handler(CommandHandler('draw',draw))
    test.add_handler(CommandHandler('money',money))
    test.add_handler(CommandHandler('point',point))
    test.add_handler(CommandHandler('buy',buy))
    test.add_handler(CommandHandler('end',end))
    test.add_handler(CommandHandler('start',start))
    test.add_handler(RegexHandler('.*reset.*',reset))
    test.add_handler(CommandHandler('status',status))
    test.add_handler(RegexHandler('pass',pass_next))

    test.add_handler(CallbackQueryHandler(button))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()