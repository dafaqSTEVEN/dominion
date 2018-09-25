from typing import List

from telegram.ext import Updater,MessageHandler,CommandHandler,RegexHandler
import random

#cardname should be capitallized
#regexhandler for admin functions

card_market = ['village','witch','silver','gold']
counter = ['1','2','3','4','5','6','7','8','9','10','11','12','13']
card = ["copper","silver","gold"]
player1 = ['copper','copper','copper','copper','copper','copper','copper','estates','estates','estates']
player2 = ['copper','copper','copper','copper','copper','copper','copper','estates','estates','estates']
buy_hand = ['copper','copper','copper','copper','copper','copper','copper','estates','estates','estates']
buy_temp = []
show_draw = []
hand = []
gold = 0
points = 0
turn = False
buy_turn = False
buy_time = 1
action = 1


def show(bot,update):
    update.message.reply_text(x)


def draw(bot,update):
    global gold
    global points
    global player1
    global turn
    global hand
    if turn == True:
        update.message.reply_text('Your turn of drawing has ended')
    else:
        for i in range(5):
            temp = (random.choice(player1))
            hand.append(temp)
            player1.remove(temp)
            if temp == 'copper':
                gold += 1
            elif temp == 'silver':
                gold += 2
            elif temp == 'gold':
                gold += 3
            if player1 == []:
                player1 = buy_hand
        update.message.reply_text('You got ' + str(hand) + ' . Type ( /buy ) or ( /use ) to proceed')
        turn = True
        return(gold,player1)

def buy(bot,update):
    global gold
    global buy_turn
    update.message.reply_text('You have <' + str(gold) + '> dollar')
    update.message.reply_text('Cards available : ' + str(card_market))
    buy_turn = True
    if gold >= 5:
        update.message.reply_text('Buy Witch cost 5 dollars( /witch )')
    if gold >= 4:
        update.message.reply_text('You can buy some cards')
    if gold >= 3:
        update.message.reply_text('Buy Village cost 3 dollars( /village )')
        update.message.reply_text('Buy Silver cost 3 dollars( /silver )')
    if gold >= 2:
          update.message.reply_text('You can buy some cards')


def village(bot,update):
    global gold
    global buy_temp
    global buy_time
    if (buy_turn == True) and (gold - 3 >= 0):
        buy_temp.append(Village)
        gold -= 3
        buy_time -= 1
        update.message.reply_text('You have bought Village . Type ( /end ) to finish buying.')
    else:
        update.message.reply_text('You dont have enough gold or it is not your turn.')
    return gold

def use_village(bot,update):
    global buy_time
    global action
    if village not in hand :
        update.message.reply_text('You dont have this card')
    elif (buy_time >= 1) and action >=1 :
        temp = (random.choice(player1))
        update.message.reply_text('You got a <' + temp + '>')
        hand.append(temp)
        player1.remove(temp)
        action += 2
        update.message.reply_text('You still have' + str(buy_time) + 'buys ' + 'You still have' + str(action) + 'actions')

def end(bot,update):
    global gold
    global buy_hand
    global buy_temp
    global hand
    gold = 0
    buy_hand = hand + buy_temp
    hand = []
    buy_temp = []
    update.message.reply_text('done!')

def use(bot,update):
    update.message.reply_text('You have ' + str(hand))
    update.message.reply_text('Type in the name of the cards to use it')

def pass_next(bot,update):
    global turn
    turn = False
    update.message.reply_text('success')

def handshow(bot,update):
    update.message.reply_text('u have ' + str(hand))

def have(bot,update):
    update.message.reply_text(player1)
    update.message.reply_text(buy_hand + 'buy_hand')
    update.message.reply_text(buy_temp + 'buy_temp')
    update.message.reply_text(hnad + 'hand')


def money(bot,update):
    update.message.reply_text('You have <' + str(gold) + '> dollar')

def point(bot,update):
    update.message.reply_text('You have <' + str(points) + '> points')

def reset(bot,update):
    global gold
    global player1
    global turn
    global hand
    turn = False
    gold = 0
    hand = []
    player1 = ['copper', 'copper', 'copper', 'copper', 'copper', 'copper', 'copper', 'estates', 'estates', 'estates']
    update.message.reply_text('success')
    return gold


def status(bot,update):
    update.message.reply_text('normal')





def main():
    updater = Updater('599551578:AAE709inuNhedfLCwIVKF9fWXJNJ-pqv5lg')
    test = updater.dispatcher
    test.add_handler(CommandHandler('show',show))
    test.add_handler(CommandHandler('draw',draw))
    test.add_handler(CommandHandler('money',money))
    test.add_handler(CommandHandler('point',point))
    test.add_handler(CommandHandler('have',have))
    test.add_handler(CommandHandler('buy',buy))
    test.add_handler(CommandHandler('use',use))
    test.add_handler(CommandHandler('end',end))
    test.add_handler(CommandHandler('village',village))
    test.add_handler(CommandHandler('handshow',handshow))
    test.add_handler(RegexHandler('.*reset.*',reset))
    test.add_handler(CommandHandler('status',status))
    test.add_handler(RegexHandler('village',use_village))
    test.add_handler(RegexHandler('pass',pass_next))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()