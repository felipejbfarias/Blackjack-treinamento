# In[1]:


# Embaralhar cartas
import random

playing = False
chip_pool = 100

bet = 1

restar_phrase = "Pressione 'j' para jogar novamente ou 's' para sair."


# In[2]:


suits = ('H', 'D', 'C', 'S')
ranking = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')

card_val = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':10, 'Q':10, 'K':10}


# In[4]:


class Card:
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return self.suit + self.rank
    
    def grab_suit(self):
        return self.suit
    
    def grab_rank(self):
        return self.rank
    
    def draw(self):
        print (self.suit + self.rank)
        


# In[11]:


class Hand:
    def __init__(self):
        self.card = []
        self.value = 0
        self.ace = False
        
    def __str__(self):
        hand_comp = ""
        
        for card in self.card:
            card_name = card._str_()
            hand_comp += "" + card_name
            
        return "Na mão tem {}".format(hand_comp)
    
    def card_add(self,card):
        self.card.append(card)
        
        if card.rank == 'A':
            self.ace = True
            
        self.value += card_val[card.rank]
        
    def calc_val(self):
        if (self.ace == 'True') and self.value < 12:
            return self.value + 10
        else:
            return self.value
    def draw(self,hidden):
        if (hidden == True and playing ==  True):
            starting_card = 1
        else:
            starting_card = 0
        for x in range(starting_card, len(self.card)):
            self.card[x].draw()
            


# In[ ]:


class Deck:
    
    def __init__(self):
        self.deck = []
        
        for suit in suits:
            for rank in ranking:
                self.deck.append(Card(suit, rank))
                
    def shuffle(self):
        random.shuffle(self.deck)
    
    def deal(self):
        single_card = self.deck.pop()
        return single_card
    def __str__(self):
        deck_comp = ""
        for card in self.deck:
            deck_comp += " " + card.str()
    
        return "O deck tem" + deck_comp


# In[ ]:


def make_bet():
    global bet
    bet = 0
    
    print("Quanto você gostaria de apostar? (Aposte em valores interios)")
    
    while bet == 0:
        bet_comp = input()
        bet_comp = int(bet_comp)
        
        if bet_comp >=1 and bet_comp <= chip_pool:
            bet = bet_comp
        else:
            print("Aposta inválida. Você tem apenas " + str(chip_pool) + " Bitbritas restantes")
            


# In[ ]:


def deal_cards():
    global result, playing, deck, player_hand, dealer_hand, chip_pool, bet
    
    deck = Deck()
    deck.shuffle()
    
    make_bet()
    
    player_hand = Hand()
    dealer_hand = Hand()
    
    # 2 Cartas para o jogador
    player_hand.card_add(deck.deal())
    player_hand.card_add(deck.deal())
    
    # 2 Cartas para o Dealer
    dealer_hand.card_add(deck.deal())
    dealer_hand.card_add(deck.deal())
    
    result = "Puxar outra carta ou manter? Pressione 'p' ou 'm' :"
    
    playing = True
    game_step()
    
    


# In[ ]:


def hit():
    
    global playing, chip_pool, deck, player_hand, dealer_hand, result, bet
    
    if playing:
        if player_hand.calc_val() <= 21:
            player_hand.card_add(deck.deal())
        print("A sua mão é %s" %player_hand)
        
        if player_hand.calc_val() >= 21:
                result = "O valor estourou! " + restar_phrase
                chip_pool -= bet
                playing = False
                
    else:
        result = "Desculpe, você não pode puxar outra carta!" + restar_phrase
                
    game_step()

def stand():
    global playing, chip_pool, deck, player_hand, dealer_hand, result, bet
    
    if playing == False:
        if player_hand.calc_val() > 0:
            result = "Desculpe, você não pode manter!"
    
    else:
        while dealer_hand.calc_val() < 17:
            dealer_hand.card_add(deck.deal())
        
        if dealer_hand.calc_val() > 21:
            result = "Dealer se deu mal! Você ganhou! " + restar_phrase
            chip_pool += bet
            playing = False
            
        elif dealer_hand.calc_val() < player_hand.calc_val():
            result = "Você ganhou do Dealer! Parabéns! " + restar_phrase
            chip_pool += bet
            playing = False
        
        elif dealer_hand.calc_val() == player_hand.calc_val():
            result = "Empate!" + restar_phrase
            playing = False
            
        else:
            result = "O dealer ganhou! " + restar_phrase
            chip_pool -= bet
            playing = False
    game_step()


# In[ ]:


def game_step():
    print("")
    print("A mão do jogador tem:")
    player_hand.draw(hidden=False)
    print("A mão completa do jogador tem: " + str(player_hand.calc_val()))
    
    print("")
    print("A mão do Dealer tem:")
    dealer_hand.draw(hidden=True)
    print("A mão do deller tem: " + str(dealer_hand.calc_val()))
    
    if playing == False:
        print("Chip total: "+str(chip_pool))
        
    print(result)
    
    player_input()
    
  
    
    
          


# In[ ]:


def game_exit():
    print("Obrigado por jogar!")
    exit()


# In[ ]:


def player_input():
    plin = input().lower()
    
    if plin == 'p':
        hit()
    elif plin == 'm':
        stand()
    elif plin == 'j':
        deal_cards()
    elif plin == 's':
        game_exit()
    else:
        print("Comando inválido... Pressione p, m, j, ou s: ")
        player_input()


# In[ ]:


def intro():
    statement = ''' Bem vindo ao BlackJack do Britas! Se aproxime de 21 o quanto puder!
    Você começa com 100 Bitbritas para começar!
    O Dealer destribui até ele ter 17. O 'A' conta como 1 ou 11.
    A cartas saem como uma letra seguida de um número'''
    print(statement)


# In[ ]:


deck = Deck()
deck.shuffle()

player_hand = Hand()
dealer_hand = Hand()

intro()
deal_cards()
