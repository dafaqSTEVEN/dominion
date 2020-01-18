card_list = []

class treasure():
    def __init__(self,name,cost,usage,points,value):
        self.name = name
        self.cost = cost
        self.usage = usage
        self.points = points
        self.value = value

    def __repr__(self):
        return '{}:{}'.format(self.__class__.__name__,self.name)




class victory():
    def __init__(self, name, cost, usage, points):
        self.name = name
        self.cost = cost
        self.usage = usage
        self.points = points
    def __repr__(self):
        return '{}:{}'.format(self.__class__.__name__,self.name)



class action():
    def __init__(self, name,cost, usage,description,points):
        self.name = name
        self.cost = cost
        self.usage = usage
        self.description = description
        self.points = points
        card_list.append(self)
    def __repr__(self):
        return '{}:{}'.format(self.__class__.__name__,self.name)





class action_attack(action):
    def __repr__(self):
        return '{}:{}'.format(self.__class__.__name__,self.name)


class action_reaction(action):
    def __repr__(self):
        return '{}:{}'.format(self.__class__.__name__,self.name)


# Treasure cards-----------------------------------------
Copper = treasure('Copper',0,60,0,1)

Silver = treasure('Silver',3,40,0,2)

Gold = treasure('Gold',6,30,0,3)

# Victory Cards-----------------------------------------
Curse = victory('Curse',0,40,-1)

Estates = victory('Estates',2,12,1)

Duchy = victory('Duchy',5,12,3)

Province = victory('Province',8,12,6)

# Action cards costing 2 dollars-----------------------------------------
Cellar = action('Cellar',2,10,'<+1 Action>,Discard any number of cards, then draw that many.',0)

Chapel = action('Chapel',2,10,'Trash up to 4 cards from your hand.',0)

Moat = action_reaction('Moat',2,10,'<+2 Cards>,When another player plays an Attack card, you may first reveal this from your hand, to be unaffected by it.',0)

# Action cards costing 3 dollars-----------------------------------------
Harbinger = action('Harbinger',3,10,'<+1 Card>,<+1 Action>,Look through your discard pile. You may put a card from it onto your deck.',0)

Merchant = action('Merchant',3,10,'<+1 Card>,<+1 Action>,The first time you play a Silver this turn, +$1',0)

Vassal = action('Vassal',3,10,'<+$2>,Discard the top card of your deck. If it is an Action card, you may play it.',0)

Village = action('Village',3,10,'<+1 Card>,<+2 Actions>',0)

Workshop = action('Workshop',3,10,'Gain a card costing up to $4.',0)

# Action cards costing 4 dollars-----------------------------------------
Bureaucrat = action('Bureaucrat',4,10,'Gain a Silver onto your deck. Each other player reveals a Victory card from their hand and puts it onto their deck (or reveals a hand with no Victory cards).',0)

Militia = action_attack('Militia',4,10,'<+$2>,Each other player discards down to 3 cards in hand.',0)

Moneylender = action('Moneylender',4,10,'You may trash a Copper from your hand for +$3.',0)

Poacher = action('Poacher',4,10,'<+1 Card>,<+1 Action>,<+$1>,Discard a card per empty supply pile.',0)

Remodel = action('Remodel',4,10,'Trash a card from your hand.,Gain a card costing up to $2 more than it.',0)

Smithy = action('Smith',4,10,'<+3 Cards>',0)

Throne_Room = action('Throne Room',4,10,'You may play an Action card from your hand twice.',0)

# Action cards costing 5 dollars-----------------------------------------
Bandit = action_attack('Bandit',5,10,'Gain a Gold. Each other player reveals the top 2 cards of their deck, trashes a revealed Treasure other than Copper, and discards the rest.',0)

Council_Room = action('Council Room',5,10,'<+4 Cards>,<+1 Buy>,Each other player draws a card.',0)

Festival = action('Festival',5,10,'<+2>,<Actions+1>,<Buy+$2>',0)

Laboratory = action('Laboratory',5,10,'<+2 Cards>,<+1 Action>',0)

Library = action('Library',5,10,'Draw until you have 7 cards in hand, skipping any Action cards you choose to; set those aside, discarding them afterwards.',0)

Market = action('Market',5,10,'<Card+1>,<Action+1>,<Buy+$1>,<+$1>',0)

Mine = action('Mine',5,10,'You may trash a Treasure from your hand. Gain a Treasure to your hand costing up to $3 more than it.',0)

Sentry = action('Sentry',5,10,'<+1 Card>,<+1 Action>,Look at the top 2 cards of your deck. Trash and/or discard any number of them. Put the rest back on top in any order.',0)

Witch = action_attack('Witch',5,10,'<+2 Cards>,Each other player gains a Curse.',0)

# Action cards costing 6 dollars-----------------------------------------
Artisan = action('Artisan',6,10,'Gain a card to your hand costing up to $5.Put a card from your hand onto your deck.',0)



