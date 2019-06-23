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
    def __init__(self, name,cost, usage, points):
        self.name = name
        self.cost = cost
        self.usage = usage
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
Cellar = action('Cellar',2,10,0)

Chapel = action('Chapel',2,10,0)

Moat = action_reaction('Moat',2,10,0)

# Action cards costing 3 dollars-----------------------------------------
Harbinger = action('Harbinger',3,10,0)

Merchant = action('Merchant',3,10,0)

Vassal = action('Vassal',3,10,0)

Village = action('Village',3,10,0)

Workshop = action('Workshop',3,10,0)

# Action cards costing 4 dollars-----------------------------------------
Bureaucrat = action('Bureaucrat',4,10,0)

Militia = action_attack('Militia',4,10,0)

Moneylender = action('Moneylender',4,10,0)

Poacher = action('Poacher',4,10,0)

Remodel = action('Remodel',4,10,0)

Smithy = action('Smith',4,10,0)

Throne_Room = action('Throne Room',4,10,0)

# Action cards costing 5 dollars-----------------------------------------
Bandit = action_attack('Bandit',5,10,0)

Council_Room = action('Council room',5,10,0)

Festival = action('Festival',5,10,0)

Laboratory = action('Laboratory',5,10,0)

Library = action('Library',5,10,0)

Market = action('Market',5,10,0)

Mine = action('Mine',5,10,0)

Sentry = action('Sentry',5,10,0)

Witch = action_attack('Witch',5,10,0)

# Action cards costing 6 dollars-----------------------------------------
Artisan = action('Artisan',6,10,0)



