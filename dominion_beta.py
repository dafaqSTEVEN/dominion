import logging
from card import *
import random
import os,types
from uuid import uuid4
import itertools
from datetime import date,timedelta
import datetime
from typing import List
import csv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, MessageHandler, CommandHandler, RegexHandler, CallbackQueryHandler
import inspect
from pythonping import ping
import socket

dir_path = os.path.dirname(os.path.realpath(__file__))


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='new_log.txt',
                    level=logging.INFO)


user_list= {}
display_list = []
display_card_list = []
game_status = False
chat_id = None
current_game_card = []
game_id = None
turn = 0
result_hand = []
EndGame = False
chapel_counter = 0
vassal_status = False
merchant_status = False
TR_status = False

print(datetime.datetime.now())
print('Running on Local.')
print('==============================================')


def start(bot,update):
    update.message.reply_text('[ INFO ]\nThank you for initializing me.')

def new(bot,update):
    if update.message.chat.type == 'private':
        update.message.reply_text('[ ! ]\nCommand only available in groups.')
    elif update.message.chat.type == 'group' or 'supergroup':
        global game_status,chat_id,message_id,display_list
        chat_id = update.message.chat_id
        if game_status is False:
            game_status = None
            with open(dir_path + '/game_id/game_id.csv', 'a+')as var:
                write_data = csv.writer(var, delimiter=',')
                write_data.writerow([uuid4(), chat_id, datetime.datetime.now()])
            user_name = str(update.message.from_user.first_name) + str(update.message.from_user.last_name)
            user_tag = update.message.from_user.username
            user_id = update.message.from_user.id
            user_list['user0'] = {'user_name': user_name,'user_id':user_id,'user_tag':user_tag}
            update.message.reply_text('[ INFO ]\n'+str(user_name) + ' started a new game.\nType /join to join the game.')
            for i in range(len(user_list)):
                display_list.append(user_list['user' + str(i)]['user_name'])
            message_id = bot.sendMessage(text='[ INFO ]\nCurrent player list : \n-------------------------------------\n' + str('\n'.join(display_list)), chat_id=chat_id)
        elif game_status is True:
            update.message.reply_text('[ ! ]\nGame has already started.\nType /join to join the game.')
        elif game_status is None:
                update.message.reply_text('[ ! ]\nType /join to join existing game.')





def join(bot,update):
    if update.message.chat.type == 'private':
        update.message.reply_text('[ ! ]\nCommand only available in groups.')
    elif update.message.chat.type == 'group' or 'supergroup':
        global message_id,display_list
        if game_status is None:
            user_name = str(update.message.from_user.first_name) + str(update.message.from_user.last_name)
            user_tag = update.message.from_user.username
            user_id = update.message.from_user.id
            ignore = False
            for i in range(len(user_list)):
                if user_name in user_list['user' + str(i)]['user_name']:
                    update.message.reply_text('[ ! ]\nYou have already joined the game.')
                    ignore = True
            if ignore == False:
                    for i in range(6):
                        if 'user' + str(i) in user_list:
                            pass
                        else:
                            user_list['user' + str(i)] = {'user_name':user_name,'user_id':user_id,'user_tag':user_tag}
                            display_list.append(user_list['user' + str(i)]['user_name'])
                            break
                    update.message.reply_text('[ INFO ]\nYou have joined the game\n' +'[ '+ user_name +' ]\nType /join to join the game\nType /startgame to start the game')

                    bot.edit_message_text(text = '[ INFO ]\nCurrent player list : \n-------------------------------------\n' + str('\n'.join(display_list)),message_id = message_id.message_id,chat_id = chat_id)
        else:
            update.message.reply_text('[ ! ]\nNo game is initialized.Type /new to start a new game')



def startgame(bot,update):
    global gold,EndGame,total_current_game_card
    if update.message.chat.type == 'private':
        update.message.reply_text('[ ! ]\nCommand only available in groups.')
    else:
        global display_list,player_in_game,turn,game_status,card_market
        if game_status is False:
            update.message.reply_text('[ ! ]\nNo game is initialized.Type /new to start a new game')
        elif game_status is True:
            update.message.reply_text('[ ! ]\nGame has already started.')
        else:
            game_status = True
            EndGame = False
            player_in_game = len(user_list)
            for i in range(player_in_game):
                use_me = user_list['user' + str(i)]
                use_me['Deck'] = list(itertools.repeat(Copper,7)) + list(itertools.repeat(Estates,3))
                random.shuffle(use_me['Deck'])
                use_me['Hand'] = [use_me['Deck'].pop(0) for i in range(5)]
                use_me['Use'] = []
                use_me['Buy_temp'] = []
                use_me['Discard'] = []
                getgold(use_me)
                use_me['Buy'] = 1
                use_me['Action'] = 1
            update.message.reply_text('[ INFO ]\nAmount of Players : ' + str(player_in_game))
            current_game_card.clear()
            total_current_game_card = []
            for i in range(len(card_list)):
                total_current_game_card.append(card_list[i])
            for i in range(10):
                select = random.choice(total_current_game_card)
                select.usage = 10
                current_game_card.append(select)
                total_current_game_card.remove(select)
            current_game_card.sort(key=getcost)
            for i in range(len(current_game_card)):
                display_card_list.append(str(current_game_card[i].name) + '(' + str(current_game_card[i].cost) + ')')
            display = '\n'.join(map(str,display_card_list))
            update.message.reply_text('[ INFO ]\n10 action cards are chosen for the game :\n' + str(display))
            Copper.usage = 60
            Silver.usage = 40
            Gold.usage = 30
            Curse.usage = 40
            Estates.usage = 12
            Duchy.usage = 12
            Province.usage = 12
            card_market = current_game_card + [Copper,Silver,Gold,Estates,Duchy,Province]
            card_market.sort(key = getcost)
            turn = 1
            for i in range(player_in_game):
                use_me = user_list['user' + str(i)]
                bot.sendMessage(text='[ INFO ]'+ ' Turn' + str(turn) + '\nThis is your Hand\n==========================\n' + str('\n'.join(map(getname,use_me["Hand"]))), chat_id=use_me["user_id"])
            keyboard = [[InlineKeyboardButton('Action', callback_data="action"),InlineKeyboardButton('Buy', callback_data="buy"),InlineKeyboardButton('Clean Up', callback_data="cleanup")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            for i in range(player_in_game):
                if i == getturn():
                    use_me = user_list['user' + str(i)]
                    user_list['user' + str(i)]['Message'] = bot.sendMessage(
                        text='[ INFO ] Status:\nAction : ' + str(use_me['Action']) + '\nBuy : ' + str(
                            use_me['Buy']) + '\nGold : ' + str(use_me['Gold']), chat_id=use_me['user_id'])
                    use_me['Menu'] = bot.sendMessage(chat_id=use_me['user_id'],text = '[ SELECT ]\nPlease Select :',reply_markup = reply_markup)
                    getgold(use_me)
                elif i != getturn():
                    use_me = user_list['user' + str(i)]
                    bot.sendMessage(text = "[ AWAIT ] Waiting for other player's turn",chat_id= use_me['user_id'])
                    getgold(use_me)
            keyboard2 = [[InlineKeyboardButton('Click Me', url= 't.me/dominion_beta_bot')]]
            bot.sendMessage(chat_id=chat_id,text='[ INFO ]\nThe Game has started.Please check your PM.',reply_markup=InlineKeyboardMarkup(keyboard2))
            for i in range(player_in_game):
                print(user_list['user'+ str(i)])





def button(bot,update):
    global turn,EndGame,user_list,display_card_list,display_list,chat_id,result_hand,game_status,cellar_counter,card_market,chapel_counter,vassal_status,merchant_status,bu_counter,militia_counter,emp_count,TR_status,TR_temp
    query = update.callback_query
    filter_result = [[]]
    if query.data == 'cancel':
        query.edit_message_text('[ OK ] Canceled.')



    if query.data == 'action':
        for i in range(6):
            if i == getturn():
                use_me = user_list['user' + str(i)]
                if use_me['Action'] <= 0:
                    query.message.reply_text('[ ! ]\nYou dont have enough Action')
                else:
                    det(user_list['user'+str(i)]['Hand'])
                    if result_hand == []:
                        query.answer(text = "[ ! ]\nYou don't have any action card",show_alert = True)
                    else:
                        for i in range(len(result_hand)):
                            filter_result.append([InlineKeyboardButton(str(result_hand[i].name),callback_data=str(result_hand[i].name))])
                        filter_result.append([InlineKeyboardButton('Cancel',callback_data='cancel')])
                        query.message.reply_text(text = '[ SELECT ]\nPlease select a Action card to play.',reply_markup = InlineKeyboardMarkup(filter_result))

    for i in range(len(card_market)):
        if str(query.data) == str(card_market[i].name + '_b'):
            temp = card_market[i]
            for i in range(player_in_game):
                use_me = user_list['user' + str(i)]
                if i == getturn():
                    use_me['Buy_temp'].append(temp)
                    use_me['Gold'] -= temp.cost
                    use_me['Buy'] -= 1
                    temp.usage -= 1
                    query.edit_message_text('[ INFO ]\nYou have bought '+ str(temp.name) +'.')
                    query.answer(text = '[ INFO ]\nYou have bought '+ str(temp.name) +'.',show_alert = True)
                    bot.edit_message_text(chat_id = use_me['user_id'],text = '[ INFO ] Status:\nAction : ' + str(use_me['Action']) + '\nBuy : ' + str(use_me['Buy'])+'\nGold : '+str(use_me['Gold']),message_id = use_me['Message'].message_id)
                    bot.sendMessage(chat_id = chat_id,text = '[ Buy ]\n('+'Turn '+str(turn)+')Player '+str(use_me['user_name'])+' has bought [ '+ str(temp.name) +' ].')
            empty = 0
            for i in range(len(card_market)):
                if card_market[i].name == 'Province':
                    if card_market[i].usage == 0:
                        EndGame = True
                elif card_market[i].usage == 0:
                    empty +=1
            if empty >= 3 :
                EndGame = True

    if query.data == 'Cellar':
        cellar_counter = 0
        keyboard = [[]]
        for i in range(player_in_game):
            if i == getturn():
                use_me = user_list[str('user' + str(i))]
                usecard(use_me,Cellar)
                use_me['Action'] += 1
                for i in range(len(use_me['Hand'])):
                    keyboard.append([InlineKeyboardButton(str(use_me['Hand'][i].name),callback_data=str(use_me['Hand'][i].name)+'_d')])
                keyboard.append([InlineKeyboardButton('Cancel', callback_data='cancel')])
                keyboard.append([InlineKeyboardButton('Done',callback_data='done_d')])
                query.edit_message_text('[ SELECT ]\nChoose any amount of card to discard, press DONE when done.',reply_markup = InlineKeyboardMarkup(keyboard))
                bot.sendMessage(chat_id = chat_id,text= GroupInfo(use_me,Cellar.name,'ACTION'))
                bot.edit_message_text(chat_id = getChat_id_private(use_me),text = getUpdateHand_text(use_me),message_id = getHand_Message_id(use_me))
                bot.edit_message_text(chat_id=getChat_id_private(use_me),text= getUpdateStatus_text(use_me),message_id=getStatus_Message_id(use_me))

    if query.data == 'Chapel':
        keyboard = [[]]
        for i in range(player_in_game):
            if i == getturn():
                use_me = user_list[str('user' + str(i))]
                usecard(use_me,Chapel)
                for i in range(len(use_me['Hand'])):
                    keyboard.append([InlineKeyboardButton(str(use_me['Hand'][i].name),callback_data=str(use_me['Hand'][i].name)+'_chapel')])
                keyboard.append([InlineKeyboardButton('Cancel', callback_data='cancel')])
                keyboard.append([InlineKeyboardButton('Done',callback_data='done_chapel')])
                query.edit_message_text('[ SELECT ]\nChoose up to 4 cards to trash, press DONE when done.',reply_markup = InlineKeyboardMarkup(keyboard))
                bot.sendMessage(chat_id = chat_id,text= GroupInfo(use_me,Chapel.name,'ACTION'))
                bot.edit_message_text(message_id=getStatus_Message_id(use_me), text= getUpdateStatus_text(use_me), chat_id=getChat_id_private(use_me))
                bot.edit_message_text(chat_id=getChat_id_private(use_me),text= getUpdateHand_text(use_me),message_id=getHand_Message_id(use_me))

    if query.data == 'Moat':
        for i in range(player_in_game):
            if i == getturn():
                display_temp = []
                use_me = user_list[str('user' + str(i))]
                usecard(use_me,Moat)
                for i in range(2):
                    if len(use_me['Deck']) == 0:
                        use_me['Deck'] += use_me['Discard']
                        random.shuffle(use_me['Deck'])
                        tempp = use_me['Deck'].pop(0)
                        display_temp.append(str(tempp.name))
                        use_me['Hand'].append(tempp)
                        use_me['Discard'].clear()
                    else:
                        tempp = use_me['Deck'].pop(0)
                        display_temp.append(str(tempp.name))
                        use_me['Hand'].append(tempp)
                    gold_b(tempp,use_me)
                bot.sendMessage(chat_id=chat_id, text=GroupInfo(use_me, Moat.name, 'ACTION'))
                bot.edit_message_text(message_id=getStatus_Message_id(use_me), text=getUpdateStatus_text(use_me),chat_id=getChat_id_private(use_me))
                bot.edit_message_text(chat_id=getChat_id_private(use_me), text=getUpdateHand_text(use_me),message_id=getHand_Message_id(use_me))
                query.edit_message_text('[ MOAT ]\nYou have drawn[ ' + str(' ,'.join(display_temp)) + ' ].')

    if query.data == 'Harbinger':
        for i in range(player_in_game):
            if i == getturn():
                keyboard = [[]]
                use_me = user_list[str('user' + str(i))]
                usecard(use_me,Harbinger)
                use_me['Action'] += 1
                if len(use_me['Deck']) == 0:
                    use_me['Deck'] += use_me['Discard']
                    random.shuffle(use_me['Deck'])
                    tempp = use_me['Deck'].pop(0)
                    use_me['Hand'].append(tempp)
                    use_me['Discard'].clear()
                else:
                    tempp = use_me['Deck'].pop(0)
                    use_me['Hand'].append(tempp)
                gold_b(tempp,use_me)
                bot.sendMessage(chat_id=chat_id, text=GroupInfo(use_me, Harbinger.name, 'ACTION'))
                bot.edit_message_text(message_id=getStatus_Message_id(use_me), text=getUpdateStatus_text(use_me),chat_id=getChat_id_private(use_me))
                bot.edit_message_text(chat_id=getChat_id_private(use_me), text=getUpdateHand_text(use_me),message_id=getHand_Message_id(use_me))
                query.edit_message_text('[ HARBINGER ]\nYou have drawn[ ' + str(tempp.name) + ' ].')
                if len(use_me['Discard']) == 0:
                    query.message.reply_text('[ ! ]\nYou have no cards in your discarded pile.')
                else:
                    for g in range(len(use_me['Discard'])):
                        keyboard.append([InlineKeyboardButton(str(use_me['Discard'][g].name),callback_data=str(use_me['Discard'][g].name) + '_har')])
                    keyboard.append([InlineKeyboardButton('Cancel',callback_data='cancel')])
                    query.message.reply_text('[ SELECT ]\nPlease select a card to place on top of your deck from the discarded pile.',reply_markup = InlineKeyboardMarkup(keyboard))

    if query.data == 'Merchant':
        for i in range(player_in_game):
            if i == getturn():
                use_me = user_list[str('user' + str(i))]
                usecard(use_me,Merchant)
                use_me['Action'] += 1
                query.edit_message_text("[ NOTE ]\nAs Dominion Bot auto-plays treasures for you, Merchant's Original effect(The first time you play a Silver this turn, +$1) is changed to\n[ When you own a Silver in your hand(single or multiple), you gain $1 this round. Playing this card multiple times in the same round will only be effective once.]\nThe effect remains mostly unchanged.")
                if len(use_me['Deck']) == 0:
                    use_me['Deck'] += use_me['Discard']
                    random.shuffle(use_me['Deck'])
                    tempp = use_me['Deck'].pop(0)
                    use_me['Hand'].append(tempp)
                    use_me['Discard'].clear()
                else:
                    tempp = use_me['Deck'].pop(0)
                    use_me['Hand'].append(tempp)
                gold_b(tempp, use_me)
                if Silver in use_me['Hand'] and merchant_status is False:
                    use_me['Gold'] += 1
                    merchant_status = True
                query.message.reply_text('[ MERCHANT ]\nYou have drawn [ '+ str(tempp.name) + ' ].')
                bot.sendMessage(chat_id=chat_id, text=GroupInfo(use_me, Merchant.name, 'ACTION'))
                bot.edit_message_text(message_id=getStatus_Message_id(use_me), text=getUpdateStatus_text(use_me),chat_id=getChat_id_private(use_me))
                bot.edit_message_text(chat_id=getChat_id_private(use_me), text=getUpdateHand_text(use_me),message_id=getHand_Message_id(use_me))

    if query.data == 'Vassal':
        for i in range(player_in_game):
            if i == getturn():
                use_me = user_list[str('user' + str(i))]
                usecard(use_me,Vassal)
                tempppp = use_me['Deck'].pop(0)
                use_me['Gold'] += 2
                use_me['Discard'].append(tempppp)
                if isinstance(tempppp,action):
                    keyboard = [[InlineKeyboardButton('Yes',callback_data= str(tempppp.name))],[InlineKeyboardButton('No',callback_data='No')]]
                    vassal_status = True
                    query.edit_message_text('[ VASSAL ]\n' + str(tempppp.name) + ' is revealed. Do you want to play it?',reply_markup = InlineKeyboardMarkup(keyboard))
                    bot.sendMessage(chat_id=chat_id, text=GroupInfo(use_me, Vassal.name, 'ACTION'))
                    bot.edit_message_text(message_id=getStatus_Message_id(use_me), text=getUpdateStatus_text(use_me),chat_id=getChat_id_private(use_me))
                    bot.edit_message_text(chat_id=getChat_id_private(use_me), text=getUpdateHand_text(use_me),message_id=getHand_Message_id(use_me))
                else:
                    query.edit_message_text('[ VASSAL ]\n' + str(tempppp.name) + ' is revealed and is not an action card, therefore discarded.')
                    bot.sendMessage(chat_id=chat_id, text=GroupInfo(use_me, Vassal.name, 'ACTION'))
                    bot.edit_message_text(message_id=getStatus_Message_id(use_me), text=getUpdateStatus_text(use_me),chat_id=getChat_id_private(use_me))
                    bot.edit_message_text(chat_id=getChat_id_private(use_me), text=getUpdateHand_text(use_me),message_id=getHand_Message_id(use_me))


    if query.data == 'Village':
        for i in range(player_in_game):
            if i == getturn():
                use_me = user_list[str('user' + str(i))]
                usecard(use_me,Village)
                use_me['Action'] += 2
                if len(use_me['Deck']) == 0:
                    use_me['Deck'] += use_me['Discard']
                    random.shuffle(use_me['Deck'])
                    tempp = use_me['Deck'].pop(0)
                    use_me['Hand'].append(tempp)
                    use_me['Discard'].clear()
                else:
                    tempp = use_me['Deck'].pop(0)
                    use_me['Hand'].append(tempp)
                gold_b(tempp, use_me)
                query.edit_message_text('[ VILLAGE ]\nYou have drawn[ ' + str(tempp.name) + ' ].')
                bot.sendMessage(chat_id=chat_id, text=GroupInfo(use_me, Village.name, 'ACTION'))
                bot.edit_message_text(message_id=getStatus_Message_id(use_me), text=getUpdateStatus_text(use_me),chat_id=getChat_id_private(use_me))
                bot.edit_message_text(chat_id=getChat_id_private(use_me), text=getUpdateHand_text(use_me),message_id=getHand_Message_id(use_me))

    if query.data == 'Workshop':
        for i in range(player_in_game):
            if i == getturn():
                keyboard = [[]]
                use_me = user_list[str('user' + str(i))]
                usecard(use_me,Workshop)
                bot.sendMessage(chat_id=chat_id, text=GroupInfo(use_me, Workshop.name, 'ACTION'))
                bot.edit_message_text(message_id=getStatus_Message_id(use_me), text=getUpdateStatus_text(use_me),chat_id=getChat_id_private(use_me))
                bot.edit_message_text(chat_id=getChat_id_private(use_me), text=getUpdateHand_text(use_me),message_id=getHand_Message_id(use_me))
                for i in range(len(card_market)):
                        if card_market[i].cost <= 4:
                            keyboard.append([InlineKeyboardButton(str(card_market[i].name + '(Cost : ' +str(card_market[i].cost) + ')'),callback_data=str(card_market[i].name)+'_ws')])
                query.edit_message_text('[ SELECT ]\nGain a Card costing up to $4',reply_markup = InlineKeyboardMarkup(keyboard))

    if query.data == 'Bureaucrat':
        for i in range(player_in_game):
            if i == getturn():
                use_me = user_list[str('user' + str(i))]
                usecard(use_me,Bureaucrat)
                use_me['Deck'].insert(0,Silver)
                bot.sendMessage(chat_id=chat_id, text=GroupInfo(use_me, Bureaucrat.name, 'ACTION'))
                bot.edit_message_text(message_id=getStatus_Message_id(use_me), text=getUpdateStatus_text(use_me),chat_id=getChat_id_private(use_me))
                bot.edit_message_text(chat_id=getChat_id_private(use_me), text=getUpdateHand_text(use_me),message_id=getHand_Message_id(use_me))
                bot.sendMessage(chat_id=chat_id, text='[ ACTION ]\n(' + 'Turn ' + str(turn) + ')Player ' + str(use_me['user_name']) + ' has played [ BUREAUCRAT ].')
                query.edit_message_text('[ BUREAUCRAT ]\nYou have gained a silver on to your Deck.')
                bu_counter = [str(1),str(len(user_list))]
                query.message.reply_text('[ AWAIT ]\nWaiting for other players to select their card.  ' + str(' / '.join(bu_counter)))
                bot.edit_message_text(text = '[ AWAIT ]\nWaiting for user to complete',chat_id = use_me['user_id'],message_id = use_me['Menu'].message_id)
            else:
                use_me = user_list[str('user' + str(i))]
                if Moat in use_me['Hand']:
                    bot.sendMessage(text = '[ MOAT ]\nPlayer' + str(user_list[str('user' + str(getturn()))]['user_name']) + ' wants to play Bureaucrat\n[ Effect : Each other player reveals a Victory card from his hand and puts it on his deck (or reveals a hand with no Victory cards).  ]\nBut Moat protects you and you have not been affected.' ,chat_id=use_me['user_id'])
                    bot.sendMessage(chat_id=chat_id,text = ('[ MOAT ]\n(' + 'Turn ' + str(turn) + ')Player ' + str(use_me['user_name']) + ' has revealed [ MOAT ] to be immune from [ BUREAUCRAT ].'))
                    bu_counter[0] = str(int(bu_counter[0]) + 1)
                    if str(bu_counter[0]) == str(bu_counter[1]):
                        keyboard = [[InlineKeyboardButton('Action', callback_data="action"),
                                     InlineKeyboardButton('Buy', callback_data="buy"),
                                     InlineKeyboardButton('Clean Up', callback_data="cleanup")]]
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        bot.edit_message_text(text='[ SELECT ]\nPlease Select :', reply_markup=reply_markup,
                                              chat_id=user_list[str('user' + str(getturn()))]['user_id'],
                                              message_id=user_list[str('user' + str(getturn()))]['Menu'].message_id)
                    bot.sendMessage(chat_id=user_list[str('user' + str(getturn()))]['user_id'],
                                    text='Player Done.  ' + str(' / '.join(bu_counter)))
                else:
                    keyboard = [[]]
                    display_temp = []
                    for g in range(len(use_me['Hand'])):
                        display_temp.append(use_me['Hand'][g].name)
                        if isinstance(use_me['Hand'][g],victory):
                            keyboard.append([InlineKeyboardButton(str(use_me['Hand'][g].name),callback_data=str(use_me['Hand'][g].name +str(i) +'_select_v'))])
                    if keyboard == [[]]:
                        bot.sendMessage(chat_id=chat_id,text = '[ BUREAUCRAT ]\nPlayer' + str(use_me['user_name'] + ' has no victory in hand, therefore hand is revealed.\n' + str('\n'.join(display_temp))))
                        bu_counter[0] = str(int(bu_counter[0]) + 1)
                        if str(bu_counter[0]) == str(bu_counter[1]):
                            keyboard = [[InlineKeyboardButton('Action', callback_data="action"),
                                         InlineKeyboardButton('Buy', callback_data="buy"),
                                         InlineKeyboardButton('Clean Up', callback_data="cleanup")]]
                            reply_markup = InlineKeyboardMarkup(keyboard)
                            bot.edit_message_text(text='[ SELECT ]\nPlease Select :', reply_markup=reply_markup,
                                                  chat_id=user_list[str('user' + str(getturn()))]['user_id'],
                                                  message_id=user_list[str('user' + str(getturn()))]['Menu'].message_id)
                        bot.sendMessage(chat_id=user_list[str('user' + str(getturn()))]['user_id'],
                                        text='Player Done.  ' + str(' / '.join(bu_counter)))
                        for k in range(player_in_game):
                            use_me = user_list[str('user' + str(k))]
                            bot.sendMessage(chat_id=use_me['user_id'],text='[ LOG ]\nHand revealed in Group.')
                    else:
                        bot.sendMessage(chat_id = use_me['user_id'],text = '[ SELECT ]\nChoose a victory to place on top of your Deck.',reply_markup=InlineKeyboardMarkup(keyboard))

    if query.data == 'Militia':
        for i in range(player_in_game):
            if i == getturn():
                use_me = user_list[str('user' + str(i))]
                usecard(use_me,Militia)
                use_me['Gold'] += 2
                bot.sendMessage(chat_id=chat_id, text=GroupInfo(use_me, Militia.name, 'ACTION'))
                bot.edit_message_text(message_id=getStatus_Message_id(use_me), text=getUpdateStatus_text(use_me),chat_id=getChat_id_private(use_me))
                bot.edit_message_text(chat_id=getChat_id_private(use_me), text=getUpdateHand_text(use_me),message_id=getHand_Message_id(use_me))
                query.edit_message_text('[ MILITIA ]\nYou have gained $2 .')
                militia_counter = [str(1),str(len(user_list))]
                query.message.reply_text('[ AWAIT ]\nWaiting for other players to select their card.  ' + str(' / '.join(militia_counter)))
                bot.edit_message_text(text = '[ AWAIT ]\nWaiting for user to complete',chat_id = use_me['user_id'],message_id = use_me['Menu'].message_id)
            else:
                use_me = user_list[str('user' + str(i))]
                if Moat in use_me['Hand']:
                    bot.sendMessage(text = '[ MOAT ]\nPlayer' + str(user_list[str('user' + str(getturn()))]['user_name']) + ' wants to play Militia\n[ Effect : Each other player discards down to 3 cards in his hand. ]\nBut Moat protects you and you have not been affected.' ,chat_id=use_me['user_id'])
                    bot.sendMessage(chat_id=chat_id,text = ('[ MOAT ]\n(' + 'Turn ' + str(turn) + ')Player ' + str(use_me['user_name']) + ' has revealed [ MOAT ] to be immune from [ MILITIA ].'))
                    militia_counter[0] = str(int(militia_counter[0]) + 1)
                    if str(militia_counter[0]) == str(militia_counter[1]):
                        keyboard = [[InlineKeyboardButton('Action', callback_data="action"),
                                     InlineKeyboardButton('Buy', callback_data="buy"),
                                     InlineKeyboardButton('Clean Up', callback_data="cleanup")]]
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        bot.edit_message_text(text='[ SELECT ]\nPlease Select :', reply_markup=reply_markup,
                                              chat_id=user_list[str('user' + str(getturn()))]['user_id'],
                                              message_id=user_list[str('user' + str(getturn()))]['Menu'].message_id)
                    bot.sendMessage(chat_id=user_list[str('user' + str(getturn()))]['user_id'],
                                    text='Player Done.  ' + str(' / '.join(militia_counter)))
                elif len(use_me['Hand']) <= 3:
                    militia_counter[0] = str(int(militia_counter[0]) + 1)
                    bot.sendMessage(chat_id=use_me['user_id'],text = '[ MILITIA ]\nCards in hand equal or less then 3 therefore ignored.')
                    if str(militia_counter[0]) == str(militia_counter[1]):
                        keyboard = [[InlineKeyboardButton('Action', callback_data="action"),
                                     InlineKeyboardButton('Buy', callback_data="buy"),
                                     InlineKeyboardButton('Clean Up', callback_data="cleanup")]]
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        bot.edit_message_text(text='[ SELECT ]\nPlease Select :', reply_markup=reply_markup,
                                              chat_id=user_list[str('user' + str(getturn()))]['user_id'],
                                              message_id=user_list[str('user' + str(getturn()))]['Menu'].message_id)
                    bot.sendMessage(chat_id=user_list[str('user' + str(getturn()))]['user_id'],
                                    text='Player Done.  ' + str(' / '.join(militia_counter)))
                else:
                    keyboard = [[]]
                    for g in range(len(use_me['Hand'])):
                        keyboard.append([InlineKeyboardButton(str(use_me['Hand'][g].name),callback_data=str(use_me['Hand'][g].name +str(i) +'_select_mil'))])
                    bot.sendMessage(chat_id = use_me['user_id'],text = '[ SELECT ]\nDiscard down to 3 cards in hand.',reply_markup=InlineKeyboardMarkup(keyboard))

    if query.data == 'Moneylender':
        for i in range(player_in_game):
            if i == getturn():
                use_me = user_list[str('user' + str(i))]
                usecard(use_me,Moneylender)
                if Copper in use_me['Hand']:
                    use_me['Hand'].remove(Copper)
                    use_me['Gold'] += 2
                    query.edit_message_text('[ MONEYLENDER ]\nA copper is trashed from your hand and you have gained $3 this turn.')
                else:
                    query.edit_message_text('[ ! ]\nYou dont have any Copper in your hand.')
                bot.sendMessage(chat_id=chat_id, text=GroupInfo(use_me, Moneylender.name, 'ACTION'))
                bot.edit_message_text(message_id=getStatus_Message_id(use_me), text=getUpdateStatus_text(use_me),chat_id=getChat_id_private(use_me))
                bot.edit_message_text(chat_id=getChat_id_private(use_me), text=getUpdateHand_text(use_me),message_id=getHand_Message_id(use_me))

    if query.data == 'Poacher':
        for i in range(player_in_game):
            if i == getturn():
                use_me = user_list[str('user' + str(i))]
                usecard(use_me,Poacher)
                use_me['Action'] += 1
                use_me['Gold'] +=1
                if len(use_me['Deck']) == 0:
                    use_me['Deck'] += use_me['Discard']
                    random.shuffle(use_me['Deck'])
                    tempp = use_me['Deck'].pop(0)
                    use_me['Hand'].append(tempp)
                    use_me['Discard'].clear()
                else:
                    tempp = use_me['Deck'].pop(0)
                    use_me['Hand'].append(tempp)
                gold_b(tempp, use_me)
                emp_count = 0
                for i in range(len(card_market)):
                    if card_market[i].usage  == 0:
                        emp_count +=1
                if emp_count == 0:
                    bot.sendMessage(chat_id=chat_id, text=GroupInfo(use_me, Poacher.name, 'ACTION'))
                    bot.edit_message_text(message_id=getStatus_Message_id(use_me), text=getUpdateStatus_text(use_me),chat_id=getChat_id_private(use_me))
                    bot.edit_message_text(chat_id=getChat_id_private(use_me), text=getUpdateHand_text(use_me),message_id=getHand_Message_id(use_me))
                    query.edit_message_text('[ POACHER ]\nYou have drawn ' + str(tempp.name) + '.')
                else:
                    keyboard = [[]]
                    for i in range(len(use_me['Hand'])):
                        keyboard.append([InlineKeyboardButton(str(use_me['Hand'][i].name),callback_data=str(use_me['Hand'][i].name+'_poa'))])
                    query.edit_message_text('[ SELECT ]\nSelect ' + str(emp_count) + 'cards to discard.',reply_markup = InlineKeyboardMarkup(keyboard))

    if query.data == 'Remodel':
        for i in range(player_in_game):
            if i == getturn():
                use_me = user_list[str('user' + str(i))]
                usecard(use_me,Remodel)
                keyboard = [[]]
                for i in range(len(use_me['Hand'])):
                    keyboard.append([InlineKeyboardButton(str(use_me['Hand'][i].name  + '(Cost : ' +str(use_me['Hand'][i].cost) + ')'),callback_data=str(use_me['Hand'][i].name + '_remodel'))])
                query.edit_message_text('[ REMODEL ]\nSelect a card to trash.',reply_markup = InlineKeyboardMarkup(keyboard))
                bot.sendMessage(chat_id=chat_id, text=GroupInfo(use_me, Remodel.name, 'ACTION'))
                bot.edit_message_text(message_id=getStatus_Message_id(use_me), text=getUpdateStatus_text(use_me),chat_id=getChat_id_private(use_me))
                bot.edit_message_text(chat_id=getChat_id_private(use_me), text=getUpdateHand_text(use_me),message_id=getHand_Message_id(use_me))

    if query.data == 'Smithy':
        for i in range(player_in_game):
            if i == getturn():
                use_me = user_list[str('user' + str(i))]
                display_temp = []
                usecard(use_me,Smithy)
                for i in range(3):
                    if len(use_me['Deck']) == 0:
                        use_me['Deck'] += use_me['Discard']
                        random.shuffle(use_me['Deck'])
                        tempp = use_me['Deck'].pop(0)
                        display_temp.append(str(tempp.name))
                        use_me['Hand'].append(tempp)
                        use_me['Discard'].clear()
                    else:
                        tempp = use_me['Deck'].pop(0)
                        display_temp.append(str(tempp.name))
                        use_me['Hand'].append(tempp)
                    gold_b(tempp, use_me)
                bot.sendMessage(chat_id=chat_id, text=GroupInfo(use_me, Smithy.name, 'ACTION'))
                bot.edit_message_text(message_id=getStatus_Message_id(use_me), text=getUpdateStatus_text(use_me),chat_id=getChat_id_private(use_me))
                bot.edit_message_text(chat_id=getChat_id_private(use_me), text=getUpdateHand_text(use_me),message_id=getHand_Message_id(use_me))

    if query.data == 'Throne Room':
        for i in range(player_in_game):
            if i == getturn():
                use_me = user_list[str('user' + str(i))]
                usecard(use_me,Throne_Room)
                keyboard = [[]]
                bot.sendMessage(chat_id=chat_id, text=GroupInfo(use_me, Throne_Room.name, 'ACTION'))
                bot.edit_message_text(message_id=getStatus_Message_id(use_me), text=getUpdateStatus_text(use_me),chat_id=getChat_id_private(use_me))
                bot.edit_message_text(chat_id=getChat_id_private(use_me), text=getUpdateHand_text(use_me),message_id=getHand_Message_id(use_me))
                for i in range(len(use_me['Hand'])):
                    if isinstance(use_me['Hand'][i],action):
                        keyboard.append([InlineKeyboardButton(str(use_me['Hand'][i].name),callback_data=str(use_me['Hand'][i].name))])
                if keyboard != [[]]:
                    TR_status = True
                    query.edit_message_text('[ THRONE ROOM ]\nSelect a card to play twice.\nNote : You cannot play any other card in between.',reply_markup = InlineKeyboardMarkup(keyboard))
                else:
                    query.edit_message_text('[ ! ]\nYou dont have any Action cards.')

    if query.data == 'Bandit':
        for i in range(player_in_game):
            if i == getturn():
                use_me = user_list[str('user' + str(i))]
                usecard(use_me,Bandit)
                use_me['Discard'].append(Gold)
                query.edit_message_text('[ BANDIT ]\nYou have gained a Gold into your discarded pile.')
                bandit_counter = [str(1),str(len(user_list))]
                bot.sendMessage(chat_id=chat_id, text=GroupInfo(use_me,Bandit.name, 'ACTION'))
                bot.edit_message_text(message_id=getStatus_Message_id(use_me), text=getUpdateStatus_text(use_me),chat_id=getChat_id_private(use_me))
                bot.edit_message_text(chat_id=getChat_id_private(use_me), text=getUpdateHand_text(use_me),message_id=getHand_Message_id(use_me))
                query.message.reply_text('[ AWAIT ]\nWaiting for other players to select their card.  ' + str(' / '.join(bu_counter)))
                bot.edit_message_text(text = '[ AWAIT ]\nWaiting for user to complete',chat_id = use_me['user_id'],message_id = use_me['Menu'].message_id)
            else:
                use_me = user_list[str('user' + str(i))]
                if Moat in use_me['Hand']:
                    bot.sendMessage(text = '[ MOAT ]\nPlayer' + str(user_list[str('user' + str(getturn()))]['user_name']) + ' wants to play Bandit\n[ Effect : Each other player reveals the top 2 cards of their deck, trashes a revealed Treasure other than Copper, and discards the rest.  ]\nBut Moat protects you and you have not been affected.' ,chat_id=use_me['user_id'])
                    bot.sendMessage(chat_id=chat_id,text = ('[ MOAT ]\n(' + 'Turn ' + str(turn) + ')Player ' + str(use_me['user_name']) + ' has revealed [ MOAT ] to be immune from [ BANDIT ].'))
                    bandit_counter[0] = str(int(bandit_counter[0]) + 1)
                    if str(bandit_counter[0]) == str(bandit_counter[1]):
                        keyboard = [[InlineKeyboardButton('Action', callback_data="action"),
                                     InlineKeyboardButton('Buy', callback_data="buy"),
                                     InlineKeyboardButton('Clean Up', callback_data="cleanup")]]
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        bot.edit_message_text(text='[ SELECT ]\nPlease Select :', reply_markup=reply_markup,
                                              chat_id=user_list[str('user' + str(getturn()))]['user_id'],
                                              message_id=user_list[str('user' + str(getturn()))]['Menu'].message_id)
                    bot.sendMessage(chat_id=user_list[str('user' + str(getturn()))]['user_id'],
                                    text='Player Done.  ' + str(' / '.join(bandit_counter)))
                else:
                    temp = []
                    bandit_use_me = []
                    for i in range(2):
                        here = use_me['Deck'].pop(0)
                        temp.append(here)
                    for i in range(len(temp)):
                        if temp[i].name != 'Copper' and isinstance(temp[i],treasure):
                            bandit_use_me.append(temp[i])
                        else:
                            use_me['Discard'].append(temp[i])
                            query.message.reply_text('[ BANDIT ]\n' + str(temp[i].name) + ' is discarded.')
                    if len(bandit_use_me) > 1:
                        if Silver in bandit_use_me:
                            query.message.reply_text('[ BANDIT ]\nSilver is trashed. ')
                            bandit_use_me.remove(Silver)
                            use_me['Discard'].append(bandit_use_me[0])
                        else:
                            query.message.reply_text('[ BANDIT ]\nGold is trashed. ')
                            bandit_use_me.remove(Gold)
                            use_me['Discard'].append(bandit_use_me[0])
                        banndit_counter[0] = str(int(bandit_counter[0]) + 1)
                        if str(bandit_counter[0]) == str(bandit_counter[1]):
                            keyboard = [[InlineKeyboardButton('Action', callback_data="action"),
                                             InlineKeyboardButton('Buy', callback_data="buy"),
                                             InlineKeyboardButton('Clean Up', callback_data="cleanup")]]
                            reply_markup = InlineKeyboardMarkup(keyboard)
                            bot.edit_message_text(text='[ SELECT ]\nPlease Select :',reply_markup=reply_markup, chat_id=user_list[str('user' + str(getturn()))]['user_id'],message_id=user_list[str('user' + str(getturn()))]['Menu'].message_id)
                        bot.sendMessage(chat_id = user_list[str('user' + str(getturn()))]['user_id'],text = 'Player Done.  ' + str(' / '.join(bandit_counter)))
                    elif len(bandit_use_me) == 1 :
                        query.message.reply_text('[ BANDIT ]\n' + str(bandit_use_me[0].name) + ' is trashed.')
                        banndit_counter[0] = str(int(bandit_counter[0]) + 1)
                        if str(bandit_counter[0]) == str(bandit_counter[1]):
                            keyboard = [[InlineKeyboardButton('Action', callback_data="action"),
                                             InlineKeyboardButton('Buy', callback_data="buy"),
                                             InlineKeyboardButton('Clean Up', callback_data="cleanup")]]
                            reply_markup = InlineKeyboardMarkup(keyboard)
                            bot.edit_message_text(text='[ SELECT ]\nPlease Select :',reply_markup=reply_markup, chat_id=user_list[str('user' + str(getturn()))]['user_id'],message_id=user_list[str('user' + str(getturn()))]['Menu'].message_id)
                        bot.sendMessage(chat_id = user_list[str('user' + str(getturn()))]['user_id'],text = 'Player Done.  ' + str(' / '.join(bandit_counter)))
                    elif len(bandit_use_me) == 0:
                        query.message.reply_text('[ BANDIT ]\nNo card is trashed.')
                        banndit_counter[0] = str(int(bandit_counter[0]) + 1)
                        if str(bandit_counter[0]) == str(bandit_counter[1]):
                            keyboard = [[InlineKeyboardButton('Action', callback_data="action"),
                                             InlineKeyboardButton('Buy', callback_data="buy"),
                                             InlineKeyboardButton('Clean Up', callback_data="cleanup")]]
                            reply_markup = InlineKeyboardMarkup(keyboard)
                            bot.edit_message_text(text='[ SELECT ]\nPlease Select :',reply_markup=reply_markup, chat_id=user_list[str('user' + str(getturn()))]['user_id'],message_id=user_list[str('user' + str(getturn()))]['Menu'].message_id)
                        bot.sendMessage(chat_id = user_list[str('user' + str(getturn()))]['user_id'],text = 'Player Done.  ' + str(' / '.join(bandit_counter)))
                          

    for i in range(player_in_game):
        use_me = user_list[str('user' + str(i))]
        for g in range(len(use_me['Hand'])):
            if query.data == str(use_me['Hand'][g].name +str(i) +'_select_v'):
                query.edit_message_text('[ BUREAUCRAT ]\n' + str(use_me['Hand'][g].name) + ' is placed on top of your Deck.')
                temp = use_me['Hand']
                use_me['Deck'].insert(0, temp[g])
                use_me['Hand'].remove(temp[g])
                bot.edit_message_text(message_id= getHand_preview_message_id(use_me), text= getUpdateHand_preview(use_me))
                bu_counter[0] = str(int(bu_counter[0]) + 1)
                if str(bu_counter[0]) == str(bu_counter[1]):
                    keyboard = [[InlineKeyboardButton('Action', callback_data="action"),
                                 InlineKeyboardButton('Buy', callback_data="buy"),
                                 InlineKeyboardButton('Clean Up', callback_data="cleanup")]]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    bot.edit_message_text(text='[ SELECT ]\nPlease Select :',reply_markup=reply_markup, chat_id=user_list[str('user' + str(getturn()))]['user_id'],message_id=user_list[str('user' + str(getturn()))]['Menu'].message_id)
                bot.sendMessage(chat_id = user_list[str('user' + str(getturn()))]['user_id'],text = 'Player Done.  ' + str(' / '.join(bu_counter)))
                break
            if query.data == str(use_me['Hand'][g].name +str(i) +'_select_mil'):
                query.edit_message_text('[ MILITIA ]\n' + str(use_me['Hand'][g].name) + ' is discarded.')
                temp = use_me['Hand']
                use_me['Discard'].append(temp[g])
                use_me['Hand'].remove(temp[g])
                bot.edit_message_text(message_id=getHand_preview_message_id(use_me), text=getUpdateHand_preview(use_me))
                if len(use_me['Hand']) <= 3:
                    militia_counter[0] = str(int(militia_counter[0]) + 1)
                    if str(militia_counter[0]) == str(militia_counter[1]):
                        keyboard = [[InlineKeyboardButton('Action', callback_data="action"),
                                     InlineKeyboardButton('Buy', callback_data="buy"),
                                     InlineKeyboardButton('Clean Up', callback_data="cleanup")]]
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        bot.edit_message_text(text='[ SELECT ]\nPlease Select :',reply_markup=reply_markup, chat_id=user_list[str('user' + str(getturn()))]['user_id'],message_id=user_list[str('user' + str(getturn()))]['Menu'].message_id)
                    bot.sendMessage(chat_id = user_list[str('user' + str(getturn()))]['user_id'],text = 'Player Done.  ' + str(' / '.join(militia_counter)))
                else:
                    keyboard = [[]]
                    for g in range(len(use_me['Hand'])):
                        keyboard.append([InlineKeyboardButton(str(use_me['Hand'][g].name), callback_data=str(
                            use_me['Hand'][g].name + str(i) + '_select_mil'))])
                    bot.sendMessage(chat_id=use_me['user_id'], text='[ SELECT ]\nDiscard down to 3 cards in hand.',
                                    reply_markup=InlineKeyboardMarkup(keyboard))
                break
            if query.data == str(use_me['Hand'][g].name +'_poa'):
                temp = use_me['Hand']
                use_me['Hand'].remove(temp[g])
                use_me['Discard'].append(temp[g])
                query.message.reply_text('[ POACHER ]\nYou have discarded ' + str(temp[g].name))
                bot.edit_message_text(message_id=getHand_Message_id(use_me), text=getUpdateHand_text(use_me), chat_id=getChat_id_private(use_me))
                bot.edit_message_text(chat_id=getChat_id_private(use_me),text=getUpdateStatus_text(use_me),message_id=getStatus_Message_id(use_me))
                if emp_count >0:
                    emp_count -= 1
                    keyboard = [[]]
                    for i in range(len(use_me['Hand'])):
                        keyboard.append([InlineKeyboardButton(str(use_me['Hand'][i].name),callback_data=str(use_me['Hand'][i].name + '_poa'))])
                    query.edit_message_text('[ SELECT ]\nSelect ' + str(emp_count) + 'cards to discard.',
                                            reply_markup=InlineKeyboardMarkup(keyboard))
                else:
                    query.edit_message_text('[ POACHER ]\nDone.')
            if query.data == str(use_me['Hand'][g].name + '_remodel'):
                temp = use_me['Hand'][g]
                use_me['Hand'].remove(temp)
                keyboard = [[]]
                for i in range(len(card_market)):
                    if card_market[i].cost <= (temp.cost + 2):
                        keyboard.append([InlineKeyboardButton(str(card_market[i].name + '(Cost : ' +str(card_market[i].cost) + ')'),callback_data= str(card_market[i].name)+ '_g_rem')])
                query.edit_message_text('[ REMODEL ]\nSelect a card to gain.',reply_markup = InlineKeyboardMarkup(keyboard))



    for i in range(player_in_game):
        if i == getturn():
            use_me = user_list[str('user' + str(i))]
            for i in range(len(use_me['Discard'])):
                if query.data == str(use_me['Discard'][i].name) + '_har':
                    use_me['Deck'].insert(0,use_me['Discard'][i])
                    query.edit_message_text('[ HARBINGER ]\nYou have placed [ ' + str(use_me['Discard'][i].name) + ' ] on top of your Deck.')
                    break

    for i in range(player_in_game):
        if i == getturn():
            use_me = user_list[str('user'+str(i))]
            for i in range(len(card_market)):
                if query.data == str(card_market[i].name)+'_ws':
                    use_me['Buy_temp'].append(card_market[i])
                    query.edit_message_text('[ WORKSHOP ]\nYou have gained [ ' + str(card_market[i].name) + ' ] .')
                    break
                if query.data == str(card_market[i].name) + '_g_rem':
                    use_me['Buy_temp'].append(card_market[i])
                    query.edit_message_text('[ REMODEL ]\nYou have gained [ ' + str(card_market[i].name) + ' ] .')


    for i in range(player_in_game):
        if i == getturn():
            use_me = user_list[str('user' + str(i))]
            for i in range(len(use_me['Hand'])):
                if query.data == str(use_me['Hand'][i].name) + '_d':
                    cellar_counter += 1
                    keyboard = [[]]
                    temppp = use_me['Hand']
                    bot.sendMessage(chat_id=use_me['user_id'],text='[ CELLAR ]\nYou have discarded ' + str(temppp[i].name) + '.')
                    use_me['Use'].append(temppp[i])
                    use_me['Hand'].remove(temppp[i])
                    for g in range(len(use_me['Hand'])):
                        keyboard.append([InlineKeyboardButton(str(use_me['Hand'][g].name),callback_data=str(use_me['Hand'][g].name)+'_d')])
                    keyboard.append([InlineKeyboardButton('Done', callback_data='done_d')])
                    bot.edit_message_text(chat_id=getChat_id_private(use_me), text=getUpdateHand_text(use_me),message_id=getHand_Message_id(use_me))
                    bot.edit_message_text(chat_id=getChat_id_private(use_me), text=getUpdateStatus_text(use_me),message_id=getStatus_Message_id(use_me))
                    query.edit_message_text('[ SELECT ]\nChoose any amount of card to discard, press DONE when done.\nkey:' + str(uuid4()),reply_markup=InlineKeyboardMarkup(keyboard))
                    break
                if query.data == str(use_me['Hand'][i].name) + '_chapel':
                    if chapel_counter < 3:
                        chapel_counter += 1
                        keyboard = [[]]
                        temppp = use_me['Hand']
                        bot.sendMessage(chat_id=use_me['user_id'],text='[ CHAPEL ]\nYou have trashed ' + str(temppp[i].name) + '.')
                        bot.sendMessage(chat_id=chat_id,text='[ CHAPEL ]\nPlayer '+str(use_me['user_name'])+ 'have trashed ' + str(temppp[i].name) + '.')
                        use_me['Hand'].remove(temppp[i])
                        for g in range(len(use_me['Hand'])):
                            keyboard.append([InlineKeyboardButton(str(use_me['Hand'][g].name),callback_data=str(use_me['Hand'][g].name) + '_chapel')])
                        keyboard.append([InlineKeyboardButton('Done', callback_data='done_chapel')])
                        bot.edit_message_text(chat_id=getChat_id_private(use_me), text=getUpdateHand_text(use_me),message_id=getHand_Message_id(use_me))
                        bot.edit_message_text(chat_id=getChat_id_private(use_me), text=getUpdateStatus_text(use_me),message_id=getStatus_Message_id(use_me))
                        query.edit_message_text('[ SELECT ]\nChoose any amount of card to discard, press DONE when done.\nkey:' + str(uuid4()), reply_markup=InlineKeyboardMarkup(keyboard))
                        break
                    elif chapel_counter >= 3:
                        chapel_counter = 0
                        query.edit_message_text('[ CHAPEL ]\nDone.')
                        temppp = use_me['Hand']
                        bot.sendMessage(chat_id=use_me['user_id'],text='[ CHAPEL ]\nYou have trashed ' + str(temppp[i].name) + '.')
                        bot.sendMessage(chat_id=chat_id,text='[ CHAPEL ]\nPlayer ' + str(use_me['user_name']) + 'have trashed ' + str(temppp[i].name) + '.')
                        use_me['Hand'].remove(temppp[i])
                        bot.edit_message_text(chat_id=getChat_id_private(use_me), text=getUpdateHand_text(use_me),message_id=getHand_Message_id(use_me))
                        bot.edit_message_text(chat_id=getChat_id_private(use_me), text=getUpdateStatus_text(use_me),message_id=getStatus_Message_id(use_me))

    if query.data == 'done_chapel':
        query.edit_message_text('[ CHAPEL ]\nDone.')

    if query.data == 'done_d':
        for i in range(player_in_game):
            if i == getturn():
                use_me = user_list[str('user' + str(i))]
                display_temp = []
                for i in range(cellar_counter):
                    if len(use_me['Deck']) == 0:
                        use_me['Deck'] += use_me['Discard']
                        random.shuffle(use_me['Deck'])
                        tempp = use_me['Deck'].pop(0)
                        display_temp.append(str(tempp.name))
                        use_me['Hand'].append(tempp)
                        use_me['Discard'].clear()
                    else:
                        tempp = use_me['Deck'].pop(0)
                        display_temp.append(str(tempp.name))
                        use_me['Hand'].append(tempp)
                    gold_b(tempp,use_me)
                query.edit_message_text('[ CELLAR ]\nYou have drawn[ ' + str(' ,'.join(display_temp)) +' ].')
                bot.edit_message_text(chat_id=getChat_id_private(use_me), text=getUpdateHand_text(use_me),message_id=getHand_Message_id(use_me))
                bot.edit_message_text(chat_id=getChat_id_private(use_me), text=getUpdateStatus_text(use_me),message_id=getStatus_Message_id(use_me))

    if query.data == 'buy':
        keyboard = [[]]
        for i in range(player_in_game):
            if i == getturn():
                use_me = user_list[str('user' + str(i))]
                buy_time = use_me['Buy']
                if buy_time > 0:
                    for i in range(len(card_market)):
                        if card_market[i].usage <= 0:
                            query.message.reply_text('[ ! ]\nThere is no more ' + card_market[i].name + '  in the pile.')
                        elif card_market[i].cost <= use_me['Gold'] :
                            keyboard.append([InlineKeyboardButton(str(card_market[i].name + '(Cost : ' +str(card_market[i].cost) + ')'),callback_data = str(card_market[i].name)+'_b')])

                    keyboard.append([InlineKeyboardButton('Cancel',callback_data='cancel')])
                    query.message.reply_text('[ SELECT ]\nPlease select a card to buy',reply_markup = InlineKeyboardMarkup(keyboard))
                else:
                    query.message.reply_text('[ ! ]\nYou dont have enough Buy.')





    if query.data == 'cleanup':
        query.edit_message_text('[ IN PROGRESS ]')
        for i in range(player_in_game):
            if i == getturn():
                use_me = user_list['user' + str(i)]
                bot.edit_message_text(chat_id=use_me['user_id'], text='[ ! ]\nNo longer Available.',message_id=use_me['Menu'].message_id)
                use_me['Discard'] += use_me['Buy_temp']
                use_me['Discard'] += use_me['Use']
                use_me['Discard'] += use_me['Hand']
                use_me['Buy_temp'].clear()
                use_me['Use'].clear()
                use_me['Hand'].clear()
                for g in range(5):
                    if len(use_me['Deck']) == 0:
                        use_me['Deck'] += use_me['Discard']
                        random.shuffle(use_me['Deck'])
                        use_me['Hand'].append(use_me['Deck'].pop(0))
                        use_me['Discard'].clear()
                    else:
                        use_me['Hand'].append(use_me['Deck'].pop(0))
                use_me['Buy'] = 1
                use_me['Action'] = 1
                query.answer(text='[ INFO ]\nYou turn has ended.' ,show_alert = True)
                use_me['Hand_preview'] = bot.sendMessage(text='[ LOG ]' + ' Turn' + str(turn) + '\nThis is your Hand for next turn \n----------------\n' + str('\n'.join(map(getname, use_me["Hand"]))), chat_id=use_me["user_id"])
                bot.sendMessage(text='[ Clean Up ]\n(Turn '+ str(turn) + ')Player'+str(use_me['user_name']) + ' has ended.',chat_id= chat_id)
        if EndGame == False:
            turn += 1
            for i in range(player_in_game):
                if i == getturn():
                    use_me = user_list['user' + str(i)]
                    getgold(use_me)
                    use_me = user_list['user' + str(i)]
                    bot.sendMessage(chat_id = chat_id,text = '[ INFO ]'+' Turn '+str(turn)+'\nIt is now Player ' + str(user_list['user' + str(i)]['user_name'])+"'s turn.")
                    use_me['Hand_message'] = bot.sendMessage(text='[ INFO ]'+ ' Turn' + str(turn) + '\nThis is your Hand\n==========================\n' + str('\n'.join(map(getname, use_me["Hand"]))), chat_id=use_me["user_id"])
                    use_me['Message'] = bot.sendMessage(text='[ INFO ] Status:\nAction : ' + str(use_me['Action']) + '\nBuy : ' + str(use_me['Buy']) + '\nGold : ' + str(use_me['Gold']), chat_id=use_me['user_id'])
                    keyboard = [[InlineKeyboardButton('Action', callback_data="action"),InlineKeyboardButton('Buy', callback_data="buy"),InlineKeyboardButton('Clean Up', callback_data="cleanup")]]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    use_me['Menu'] = bot.sendMessage(chat_id=use_me['user_id'],text = '[ SELECT ]\nPlease Select :',reply_markup = reply_markup)
                    getgold(use_me)
                    vassal_status = False
                    merchant_status = False
                elif i != getturn():
                    use_me = user_list['user' + str(i)]
                    bot.sendMessage(text = "[ AWAIT ] Waiting for other player's turn",chat_id= use_me['user_id'])
        elif EndGame == True:
            rank = []
            for i in range(player_in_game):
                use_me = user_list['user'+str(i)]
                query.message.reply_text('[ INFO ]\n Game will be ended\nFinal adjustment in progress.')
                use_me['Discard'] += use_me['Hand']
                use_me['Discard'] += use_me['Deck']
                use_me['Hand'].clear()
                use_me['Deck'].clear()
                getpoint(use_me['Discard'])
                rank.append([counter,str(use_me['user_name'])])
            rank.sort(reverse = True,key = ty)
            bot.sendMessage(chat_id=chat_id, text='Game has ended')
            for i in range(len(rank)):
                bot.sendMessage(chat_id = chat_id,text = 'Rank '+str(i+1)+'\n' + str(rank[i][1] + ' has scored : ' + str(rank[i][0])))
            user_list = {}
            display_list = []
            display_card_list = []
            game_status = False
            EndGame = False
            chat_id = None
            turn = 0
            result_hand = []

    TR_temp = update.callback_query.data
    for i in range(len(card_market)):
        if card_market[i].name == TR_temp:
            use_TR = card_market[i]
    if TR_status is True:
        keyboard = [[InlineKeyboardButton(str(use_TR.name),callback_data=str(use_TR.name))]]
        query.message.reply_text('[ THRONE_ROOM ]\nPlay the card again',InlineKeyboardMarkup(keyboard))
        TR_status = False




def force(bot,update):
    Province.usage = 1
    user_list['user0']['Gold'] = 100
    print('OK')

def summon(bot,update):
    for i in range(player_in_game):
        if i == getturn():
            use_me = user_list['user' + str(i)]
            bot.sendMessage(text='[ INFO ]'+ ' Turn' + str(turn) + 'This is your Hand\n==========================\n' + str('\n'.join(map(getname, use_me["Hand"]))), chat_id=use_me["user_id"])
    keyboard = [[InlineKeyboardButton('Action', callback_data="action"), InlineKeyboardButton('Buy', callback_data="buy"),InlineKeyboardButton('Clean Up', callback_data="cleanup")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    for i in range(player_in_game):
        if i == getturn():
            use_me = user_list['user' + str(i)]
            user_list['user' + str(i)]['Message'] = bot.sendMessage(
                text='[ INFO ]Status:\nAction : ' + str(use_me['Action']) + '\nBuy : ' + str(
                    use_me['Buy']) + '\nGold : ' + str(use_me['Gold']), chat_id=use_me['user_id'])
            use_me['Menu'] = bot.sendMessage(chat_id=use_me['user_id'], text='[ SELECT ]\nPlease Select :',reply_markup=reply_markup)


def say(bot,update,user_data):
    global sender
    content = update.message.text.partition(' ')[2]
    for i in range(player_in_game):
        if user_list['user' + str(i)]['user_id'] == update.message.from_user.id:
            sender = user_list['user' + str(i)]
            update.message.reply_text('[ LOG ]\nSent.')

    for i in range(player_in_game):
        if sender == user_list['user' + str(i)]:
            pass
        else:
            use_me = user_list['user' + str(i)]
            bot.sendMessage(text = '[ CONV ] Sent from '+ str(sender['user_name']) +'\nMessage : ' + str(content),chat_id= use_me['user_id'])
    bot.sendMessage(text='[ CONV ] Sent from' + str(sender['user_name']) + '\nMessage : ' + str(content),chat_id=chat_id)


def getHand_Message_id(self):
    message_id = self['Hand_message'].message_id
    return message_id

def getStatus_Message_id(self):
    message_id = self['Hand_message'].message_id
    return message_id

def getChat_id_private(self):
    chat_id_private = self["user_id"]
    return chat_id_private

def getUpdateHand_text(self):
    text = '[ INFO ]' + ' Turn' + str(turn) + '\nThis is your Hand\n==========================\n' + str(
        '\n'.join(map(getname, self["Hand"]))) + '\n\nkey:' + str(uuid4())
    return text

def getUpdateStatus_text(self):
    text = '[ INFO ] Status:\nAction : ' + str(self['Action']) + '\nBuy : ' + str(self['Buy']) + '\nGold : ' + str(self['Gold']) + '\n\nkey:' +str(uuid4())
    return text

def GroupInfo(self,card_name,type):
    text = '[ ' + type + ' ]\n('+'Turn '+str(turn)+')Player '+str(self['user_name'])+' has played [ '+ card_name + ' ].'
    return text

def getUpdateHand_preview(self):
    text = '[ INFO ]' + ' Turn' + str(turn) + '\nThis is your Hand\n==========================\n' + str('\n'.join(map(getname, self["Hand"]))) +'\n\nkey:' + str(uuid4())
    return text
def getHand_preview_message_id(self):
    text = self['Hand_preview'].message_id
    return text

# Detect action card for Action Button=======================
def detaction(self):
    if isinstance(self,action) or isinstance(self,action_attack) or isinstance(self,action_reaction):
        return self
    else:
        return 'ignore'

def det(self):
    global result_hand
    temp = list(map(detaction, self))
    result_hand = list(filter(lambda a: a != 'ignore', temp))
    return result_hand

# Ends here=====================================================
def getcost(self):
    return self.cost

def getname(self):
    return self.name

def gold_b(self,user):
    if self == Copper:
        user['Gold'] += 1
    if self == Silver:
        user['Gold'] += 2
    if self == Gold:
        user['Gold'] += 3


def getgold(self):
    temp_copper = self['Hand'].count(Copper)
    temp_silver = self['Hand'].count(Silver)
    temp_gold = self['Hand'].count(Gold)
    self["Gold"] = temp_copper + (temp_silver *2) + (temp_gold *3)
    return self['Gold']

def getturn():
    result = (turn % player_in_game) -1
    if result == -1:
        result = (player_in_game -1)
    return result

def getpoint(self):
    global counter
    counter = 0
    for i in range(len(self)):
        counter += self[i].points

    return counter

def usecard(self,card_name):
    if vassal_status and TR_status is False:
        self['Action'] -= 1
        self['Hand'].remove(card_name)
        self['Use'].append(card_name)

def ty(self):
    return self[0]

def pingme(bot,update):
    update.message.reply_text(str(ping(str('149.154.167.220'))))

def restart(bot,update):
    global user_list,display_list,display_card_list,EndGame,chat_id,turn,result_hand,game_status
    user_list = {}
    display_list = []
    display_card_list = []
    EndGame = False
    chat_id = None
    turn = 0
    result_hand = []
    game_status = False
    update.message.reply_text('OK')

logger = logging.getLogger(__name__)

def main():
    updater = Updater('851835971:AAGVgxB8TGLM9hF9AhL6IGwOGXwcBjszHN8')
    test = updater.dispatcher
    test.add_handler(CommandHandler('start',start))
    test.add_handler(CommandHandler('join',join))
    test.add_handler(CommandHandler('startgame',startgame))
    test.add_handler(CommandHandler('new',new))
    test.add_handler(CommandHandler('force',force))
    test.add_handler(CommandHandler('summon',summon))
    test.add_handler(CallbackQueryHandler(button))
    test.add_handler(CommandHandler('say',say,pass_user_data= True))
    test.add_handler(CommandHandler('restart',restart))
    test.add_handler(CommandHandler('ping',pingme))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
