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
buy_hand = []
buy_temp = []
show_draw = []
hand = []
gold = 0
points = 0
turn = False
buy_turn = False
buy_time = 1
action = 1
user1_id = 'null'
user2_id = 'null'
user3_id = 'null'
current_player = 1
courtyard_temp = 0


def show(bot,update):
    update.message.reply_text(x)


def draw(bot,update):
    global gold
    global points
    global player1
    global turn
    global hand
    global courtyard_temp
    if turn == True:
        update.message.reply_text('Your turn of drawing has ended')
    else:
        for i in range(5):
            if courtyard_temp == 0:
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
            else:
                hand.append(courtyard_temp)
                courtyard_temp = 0
                update.message.reply_text('for admin : cleared courtyard')

        update.message.reply_text('You got ' + str(hand) + ' . Type ( /buy ) or ( /use ) to proceed')
        turn = True
        return(gold,player1,courtyard_temp)

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
          update.message.reply_text('Buy Courtyard costs 2 dollar ( /courtyard)')


def village(bot,update):
    global gold
    global buy_temp
    global buy_time
    if (buy_turn == True) and (gold - 3 >= 0):
        buy_temp.append('Village')
        gold -= 3
        buy_time -= 1
        update.message.reply_text('You have bought Village . Type ( /end ) to finish buying.')
    else:
        update.message.reply_text('You dont have enough gold or it is not your turn.')
    return (gold,buy_time,buy_temp)

def courtyard(bot,update):
    global gold
    global buy_temp
    global buy_time
    if (buy_turn == True) and (gold - 2 >= 0):
        buy_temp.append('Courtyard')
        gold -= 2
        buy_time -= 1
        update.message.reply_text('You have bought Courtyard . Type ( /end ) to finish buying.')
    else:
        update.message.reply_text('You dont have enough gold or it is not your turn.')
    return (gold, buy_time, buy_temp)

def use_courtyard(bot,update):
    global buy_time
    global action
    global player1
    global hand
    global gold
    if 'Courtyard' not in hand:
        update.message.reply_text('You dont have this card')
    elif buy_time >= 1 and action >= 1:
        action -= 1
        hand.remove('Courtyard')
        for i in range(3):
            temp = (random.choice(player1))
            update.message.reply_text('You got a <' + str(temp) + '>')
            hand.append(temp)
            player1.remove(temp)
            if temp == 'copper':
                gold += 1
            elif temp == 'silver':
                gold += 2
            elif temp == 'gold':
                gold += 3
        update.message.reply_text('Select a card to place on top of your deck')
        update.message.reply_text(str(hand))
        update.message.reply_text('type in the card name + _d , for example : Village_d')
    else:
        update.message.reply_text('error')
    return (buy_time, action, player1,hand,gold)

def estates_d(bot,update):
    global hand
    global courtyard_temp
    if 'estates' not in hand:
        update.message.reply_text('You can not place this card')
    else:
        hand.remove('estates')
        courtyard_temp.append('estates')
    update.message.reply_text('Type in the name of the next card you use or to end this turn , type /end . ')
    update.message.reply_text('You still have ' + str(buy_time) + ' buys ' + str(gold) + ' dollars, ' + '  and ' + str(action) + ' actions')

def copper_d(bot,update):
    global hand
    global courtyard_temp
    if 'copper' not in hand:
        update.message.reply_text('You can not place this card')
    else:
        hand.remove('copper')
        courtyard_temp.append('copper')
    update.message.reply_text('Type in the name of the next card you use or to end this turn , type /end . ')
    update.message.reply_text('You still have ' + str(buy_time) + ' buys ' + str(gold) + ' dollars, ' + '  and ' + str(action) + ' actions')

def silver_d(bot,update):
    global hand
    global courtyard_temp
    if 'silver' not in hand:
        update.message.reply_text('You can not place this card')
    else:
        hand.remove('silver')
        courtyard_temp.append('silver')
    update.message.reply_text('Type in the name of the next card you use or to end this turn , type /end . ')
    update.message.reply_text('You still have ' + str(buy_time) + ' buys ' + str(gold) + ' dollars, ' + '  and ' + str(action) + ' actions')

def gold_d(bot,update):
    global hand
    global courtyard_temp
    if 'gold' not in hand:
        update.message.reply_text('You can not place this card')
    else:
        hand.remove('gold')
        courtyard_temp.append('gold')
    update.message.reply_text('Type in the name of the next card you use or to end this turn , type /end . ')
    update.message.reply_text('You still have ' + str(buy_time) + ' buys ' + str(gold) + ' dollars, ' + '  and ' + str(action) + ' actions')

def village_d(bot,update):
    global hand
    global courtyard_temp
    if 'Village' not in hand:
        update.message.reply_text('You can not place this card')
    else:
        hand.remove('Village')
        courtyard_temp.append('Village')
    update.message.reply_text('Type in the name of the next card you use or to end this turn , type /end . ')
    update.message.reply_text('You still have ' + str(buy_time) + ' buys ' + str(gold) + ' dollars, ' + '  and ' + str(action) + ' actions')

def courtyard_d(bot,update):
    global hand
    global courtyard_temp
    if 'Courtyard' not in hand:
        update.message.reply_text('You can not place this card')
    else:
        hand.remove('Courtyard')
        courtyard_temp.append('Courtyard')
    update.message.reply_text('Type in the name of the next card you use or to end this turn , type /end . ')
    update.message.reply_text('You still have ' + str(buy_time) + ' buys ' + str(gold) + ' dollars, ' + '  and ' + str(action) + ' actions')

def use_village(bot,update):
    global buy_time
    global action
    global player1
    global hand
    global hand
    global gold
    if 'Village' not in hand :
        update.message.reply_text('You dont have this card')
    elif buy_time >= 1 and action >= 1 :
        action -= 1
        hand.remove('Village')
        temp = (random.choice(player1))
        update.message.reply_text('You got a <' + str(temp) + '>')
        hand.append(temp)
        player1.remove(temp)
        if temp == 'copper':
            gold += 1
        elif temp == 'silver':
            gold += 2
        elif temp == 'gold':
            gold += 3
        action += 2
        update.message.reply_text('You still have ' + str(buy_time) + ' buys ' + str(gold) +' dollars, ' + ' and ' + str(action) + ' actions')
    else:
        update.message.reply_text('error')
    return (buy_time,action,player1,hand)

def end(bot,update):
    global gold
    global buy_hand
    global buy_temp
    global hand
    gold = 0
    buy_hand += hand
    buy_hand += buy_temp
    hand = []
    buy_temp = []
    update.message.reply_text('done!')

def use(bot,update):
    update.message.reply_text('You have ' + str(hand))
    update.message.reply_text('Type in the name of the cards to use it')

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

def handshow(bot,update):
    update.message.reply_text('u have ' + str(hand))

def have(bot,update):
    update.message.reply_text(buy_hand)
    update.message.reply_text(buy_temp)
    update.message.reply_text(hand)
    update.message.reply_text(player1)
    update.message.reply_text(courtyard_temp)


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

def command_list(bot,update):
    update.message.reply_text('/draw to draw - /buy to buy -  /end to end - pass to reset to next player - ')

def start(bot,update):
    global user1_id
    global user2_id
    global user3_id
    update.message.reply_text('Welcome ' + str(update.message.from_user.first_name) + str(update.message.from_user.last_name) + ' [ ' + str(update.message.from_user.id) + ' / ' + '@' + str(update.message.from_user.username) + ' ] ')
    if user1_id == 'null':
        user1_id = update.message.from_user.id
    elif user2_id== 'null':
        user2_id = update.message.from_user.id
    elif user3_id == 'null':
        user3_id = update.message.from_user.id
    update.message.reply_text('Current player list : ' + str(user1_id) + ' / ' + str(user2_id) + ' / ' + str(user3_id))
    return (user1_id,user2_id,user3_id)

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
    test.add_handler(CommandHandler('courtyard',courtyard))
    test.add_handler(CommandHandler('handshow',handshow))
    test.add_handler(CommandHandler('command',command_list))
    test.add_handler(CommandHandler('start',start))
    test.add_handler(RegexHandler('.*reset.*',reset))
    test.add_handler(CommandHandler('status',status))
    test.add_handler(RegexHandler('village',use_village))
    test.add_handler(RegexHandler('courtyard',use_courtyard))
    test.add_handler(RegexHandler('pass',pass_next))
    test.add_handler(CommandHandler('estates_d',estates_d))
    test.add_handler(CommandHandler('copper_d',copper_d))
    test.add_handler(CommandHandler('silver_d',silver_d))
    test.add_handler(CommandHandler('gold_d',gold_d))
    test.add_handler(CommandHandler('village_d',village_d))
    test.add_handler(CommandHandler('courtyard_d',courtyard_d))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()