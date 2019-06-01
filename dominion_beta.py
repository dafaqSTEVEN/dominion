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
            total_current_game_card = card_list
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
                elif i != getturn():
                        use_me = user_list['user' + str(i)]
                        bot.sendMessage(text = "[ AWAIT ] Waiting for other player's turn",chat_id= use_me['user_id'])
            keyboard2 = [[InlineKeyboardButton('Click Me', url= 't.me/dominion_beta_bot')]]
            bot.sendMessage(chat_id=chat_id,text='[ INFO ]\nThe Game has started.Please check your PM.',reply_markup=InlineKeyboardMarkup(keyboard2))
            for i in range(player_in_game):
                print(user_list['user'+ str(i)])




def button(bot,update):
    global turn,EndGame,user_list,display_card_list,display_list,chat_id,result_hand,game_status,cellar_counter,card_market,chapel_counter
    query = update.callback_query
    filter_result = [[]]
    if query.data == 'action':
        for i in range(6):
            if i == getturn():
                det(user_list['user'+str(i)]['Hand'])
            else:
                pass
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
                use_me['Action'] -= 1
                use_me['Action'] +=1
                use_me['Hand'].remove(Cellar)
                use_me['Discard'].append(Cellar)
                for i in range(len(use_me['Hand'])):
                    keyboard.append([InlineKeyboardButton(str(use_me['Hand'][i].name),callback_data=str(use_me['Hand'][i].name)+'_d')])
                keyboard.append([InlineKeyboardButton('Done',callback_data='done_d')])
                query.edit_message_text('[ SELECT ]\nChoose any amount of card to discard, press DONE when done.',reply_markup = InlineKeyboardMarkup(keyboard))
                bot.sendMessage(chat_id = chat_id,text= '[ ACTION ]\n('+'Turn '+str(turn)+')Player '+str(use_me['user_name'])+' has played [ Cellar ].')
                bot.edit_message_text(message_id=use_me['Hand_message'].message_id, text='[ INFO ]' + ' Turn' + str(turn) + '\nThis is your Hand\n==========================\n' + str('\n'.join(map(getname, use_me["Hand"]))) + '\nkey:'+ str(uuid4()), chat_id=use_me["user_id"])
                bot.edit_message_text(chat_id=use_me['user_id'],text='[ INFO ] Status:\nAction : ' + str(use_me['Action']) + '\nBuy : ' + str(use_me['Buy']) + '\nGold : ' + str(use_me['Gold']),message_id=use_me['Message'].message_id)

    if query.data == 'Chapel':
        keyboard = [[]]
        for i in range(player_in_game):
            if i == getturn():
                use_me = user_list[str('user' + str(i))]
                use_me['Action'] -= 1
                use_me['Hand'].remove(Chapel)
                use_me['Discard'].append(Chapel)
                for i in range(len(use_me['Hand'])):
                    keyboard.append([InlineKeyboardButton(str(use_me['Hand'][i].name),callback_data=str(use_me['Hand'][i].name)+'_chapel')])
                keyboard.append([InlineKeyboardButton('Done',callback_data='done_chapel')])
                query.edit_message_text('[ SELECT ]\nChoose up to 4 cards to trash, press DONE when done.',reply_markup = InlineKeyboardMarkup(keyboard))
                bot.sendMessage(chat_id = chat_id,text= '[ ACTION ]\n('+'Turn '+str(turn)+')Player '+str(use_me['user_name'])+' has played [ CHAPEL ].')
                bot.edit_message_text(message_id=use_me['Hand_message'].message_id, text='[ INFO ]' + ' Turn' + str(turn) + '\nThis is your Hand\n==========================\n' + str('\n'.join(map(getname, use_me["Hand"]))) + '\nkey:'+ str(uuid4()), chat_id=use_me["user_id"])
                bot.edit_message_text(chat_id=use_me['user_id'],text='[ INFO ] Status:\nAction : ' + str(use_me['Action']) + '\nBuy : ' + str(use_me['Buy']) + '\nGold : ' + str(use_me['Gold']),message_id=use_me['Message'].message_id)

    if query.data == 'Moat':
        for i in range(player_in_game):
            if i == getturn():
                display_temp = []
                use_me = user_list[str('user' + str(i))]
                use_me['Action'] -= 1
                use_me['Hand'].remove(Moat)
                use_me['Discard'].append(Moat)
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
                bot.sendMessage(chat_id=chat_id, text='[ ACTION ]\n(' + 'Turn ' + str(turn) + ')Player ' + str(use_me['user_name']) + ' has played [ Moat ].')
                bot.edit_message_text(message_id=use_me['Hand_message'].message_id, text='[ INFO ]' + ' Turn' + str(turn) + '\nThis is your Hand\n==========================\n' + str('\n'.join(map(getname, use_me["Hand"]))) + '\nkey:' + str(uuid4()), chat_id=use_me["user_id"])
                bot.edit_message_text(chat_id=use_me['user_id'],
                                      text='[ INFO ] Status:\nAction : ' + str(use_me['Action']) + '\nBuy : ' + str(use_me['Buy']) + '\nGold : ' + str(use_me['Gold']),
                                      message_id=use_me['Message'].message_id)
                query.edit_message_text('You have drawn[ ' + str(' ,'.join(display_temp)) + ' ].')


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
                    bot.edit_message_text(message_id=use_me['Hand_message'].message_id, text='[ INFO ]' + ' Turn' + str(turn) + '\nThis is your Hand\n==========================\n' + str('\n'.join(map(getname, use_me["Hand"]))) + '\nkey:'+ str(uuid4()), chat_id=use_me["user_id"])
                    bot.edit_message_text(chat_id=use_me['user_id'],text='[ INFO ] Status:\nAction : ' + str(use_me['Action']) + '\nBuy : ' + str(use_me['Buy']) + '\nGold : ' + str(use_me['Gold']) + '\nkey:'+ str(uuid4()),message_id=use_me['Message'].message_id)
                    query.edit_message_text('[ SELECT ]\nChoose any amount of card to discard, press DONE when done.\nkey:' + str(uuid4()),reply_markup=InlineKeyboardMarkup(keyboard))
                    break
                if query.data == str(use_me['Hand'][i].name) + '_chapel':
                    if chapel_counter < 3:
                        chapel_counter += 1
                        print(chapel_counter)
                        keyboard = [[]]
                        temppp = use_me['Hand']
                        bot.sendMessage(chat_id=use_me['user_id'],text='[ CHAPEL ]\nYou have trashed ' + str(temppp[i].name) + '.')
                        bot.sendMessage(chat_id=chat_id,text='[ CHAPEL ]\nPlayer '+str(use_me['user_name'])+ 'have trashed ' + str(temppp[i].name) + '.')
                        use_me['Hand'].remove(temppp[i])
                        for g in range(len(use_me['Hand'])):
                            keyboard.append([InlineKeyboardButton(str(use_me['Hand'][g].name),callback_data=str(use_me['Hand'][g].name) + '_chapel')])
                        keyboard.append([InlineKeyboardButton('Done', callback_data='done_chapel')])
                        bot.edit_message_text(message_id=use_me['Hand_message'].message_id,text='[ INFO ]' + ' Turn' + str(turn) + '\nThis is your Hand\n==========================\n' + str('\n'.join(map(getname, use_me["Hand"]))) + '\nkey:' + str(uuid4()),chat_id=use_me["user_id"])
                        bot.edit_message_text(chat_id=use_me['user_id'], text='[ INFO ] Status:\nAction : ' + str(use_me['Action']) + '\nBuy : ' + str(use_me['Buy']) + '\nGold : ' + str(use_me['Gold']) + '\nkey:' + str(uuid4()), message_id=use_me['Message'].message_id)
                        query.edit_message_text('[ SELECT ]\nChoose any amount of card to discard, press DONE when done.\nkey:' + str(uuid4()), reply_markup=InlineKeyboardMarkup(keyboard))
                        break
                    elif chapel_counter >= 3:
                        chapel_counter = 0
                        query.edit_message_text('[ CHAPEL ]\nDone.')
                        temppp = use_me['Hand']
                        bot.sendMessage(chat_id=use_me['user_id'],text='[ CHAPEL ]\nYou have trashed ' + str(temppp[i].name) + '.')
                        bot.sendMessage(chat_id=chat_id,text='[ CHAPEL ]\nPlayer ' + str(use_me['user_name']) + 'have trashed ' + str(temppp[i].name) + '.')
                        use_me['Hand'].remove(temppp[i])
                        bot.edit_message_text(message_id=use_me['Hand_message'].message_id,text='[ INFO ]' + ' Turn' + str(turn) + '\nThis is your Hand\n==========================\n' + str('\n'.join(map(getname, use_me["Hand"]))) + '\nkey:' + str(uuid4()),chat_id=use_me["user_id"])
                        bot.edit_message_text(chat_id=use_me['user_id'], text='[ INFO ] Status:\nAction : ' + str(use_me['Action']) + '\nBuy : ' + str(use_me['Buy']) + '\nGold : ' + str(use_me['Gold']) + '\nkey:' + str(uuid4()), message_id=use_me['Message'].message_id)

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
                query.edit_message_text('[ CELLAR ]\nYou have drawn[ ' + str(' ,'.join(display_temp)) +' ].')
                bot.edit_message_text(message_id = use_me['Hand_message'].message_id,text='[ INFO ]'+ ' Turn' + str(turn) + '\nThis is your Hand\n==========================\n' + str('\n'.join(map(getname, use_me["Hand"]))), chat_id = use_me["user_id"])


    if query.data == 'buy':
        global buy_time,gold
        keyboard = [[]]
        for i in range(player_in_game):
            if i == getturn():
                use_me = user_list[str('user' + str(i))]
                gold = getgold(use_me)
                buy_time = use_me['Buy']
                if buy_time > 0:
                    for i in range(len(card_market)):
                        if card_market[i].usage <= 0:
                            query.message.reply_text('[ ! ]\nThere is no more ' + card_market[i].name + '  in the pile.')
                        elif card_market[i].cost <= gold :
                            keyboard.append([InlineKeyboardButton(str(card_market[i].name + '(Cost : ' +str(card_market[i].cost) + ')'),callback_data = str(card_market[i].name)+'_b')])


                    keyboard.append([InlineKeyboardButton('Cancel',callback_data='cancel')])
                    query.message.reply_text('[ SELECT ]\nPlease select a card to buy',reply_markup = InlineKeyboardMarkup(keyboard))
                else:
                    query.message.reply_text('[ ! ]\nYou dont have enough Buy.')

    if query.data == 'cancel':
        query.edit_message_text('[ OK ] Canceled.')



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
            chat_id = None
            turn = 0
            result_hand = []



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
    print(counter)

    return counter

def ty(self):
    return self[0]

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
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()