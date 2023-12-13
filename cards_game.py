DISCARD = "discard"
PLAY_ZONE = "play_zone"


class Carte:
    def __init__(self, mana_cost, name, description):
        self.__mana_cost = mana_cost
        self.__name = name
        self.__description = description
        self.__mage = None

    def set_mage(self, mage):
        self.__mage = mage

    def get_mage(self):
        return self.__mage
    
    def get_mana_cost(self):
        return self.__mana_cost
    
    def set_mana_cost(self, mana_cost):
        self.__mana_cost = mana_cost

    def get_name(self):
        return self.__name
    
    def set_name(self, name):
        self.__name = name

    def play(self, _):
        print("Rien ne se passe")

    def display(self):
        return f"Carte {self.__name} [{self.__mana_cost} mana] ({self.__description})"
    
    def is_attackable(self):
        return False
    
    def can_retaliate(self):
        return False

class Cristal(Carte):
    def __init__(self, mana_cost, name, description, value):
        super().__init__(mana_cost, name, description)
        self.__value = value
    
    def get_value(self):
        return self.__value
    
    def set_value(self, value):
        self.__value = value

    def play(self, _):
        self.get_mage().move_card_hand_to_play_area(self)
        self.get_mage().gain_mana(self.__value)

class Creature(Carte):
    def __init__(self, mana_cost, name, description, health_points, attack_score):
        super().__init__(mana_cost, name, description)
        self.__health_points = health_points
        self.__attack_score = attack_score
    
    def get_health_points(self):
        return self.__health_points
    
    def set_health_points(self, health_points):
        self.__health_points = health_points

    def lose_health_points(self, hp):
        self.__health_points = max(0, self.__health_points - hp)
        if self.__health_points <= 0:
            self.die()
    
    def get_attack_score(self):
        return self.__attack_score
    
    def set_attack_score(self, attack_score):
        self.__attack_score = attack_score
    
    def is_attackable(self):
        return True
    
    def can_retaliate(self):
        return True
    
    def play(self, target):
        self.get_mage().move_card_hand_to_play_area(self)
        self.attack(target)
    
    def attack(self, target):
        target.lose_health_points(self.get_attack_score())
        if target.can_retaliate():
            self.lose_health_points(target.get_attack_score())

    def get_status(self):
        return f"{self.get_name()}: {self.__health_points} hp / {self.__attack_score} attaque"
    
    def die(self):
        self.get_mage().move_card_play_area_to_discard(self)

class Blast(Carte):
    def __init__(self, mana_cost, name, description, value):
        super().__init__(mana_cost, name, description)
        self.__value = value

    def play(self, target):
        target.lose_health_points(self.__value)
        self.get_mage().move_card_hand_to_discard(self)

class Mage:
    def __init__(self, name, health_points, maximum_mana):
        self.__name = name
        self.__health_points = health_points
        self.__current_mana = maximum_mana
        self.__maximum_mana = maximum_mana
        self.__hand = []
        self.__discard = []
        self.__play_area = []

    def can_retaliate(self):
        return False
    
    def lose_health_points(self, hp):
        self.__health_points = max(0, self.__health_points - hp)
    
    def is_alive(self):
        return self.__health_points > 0
    
    def get_name(self):
        return self.__name
    
    def set_name(self, name):
        self.__name = name

    def get_hand(self):
        return self.__hand
    
    def set_hand(self, hand):
        self.__hand = hand

    def get_discard(self):
        return self.__discard
    
    def set_discard(self, discard):
        self.__discard = discard

    def add_cards_to_hand(self, cards):
        for card in cards:
            card.set_mage(self)
            self.__hand.append(card)
    
    def move_card_hand_to_play_area(self, card):
        card_index = self.__hand.index(card)
        card = self.__hand.pop(card_index)
        self.__play_area.append(card)

    def move_card_hand_to_discard(self, card):
        card_index = self.__hand.index(card)
        card = self.__hand.pop(card_index)
        self.__discard.append(card)

    def move_card_play_area_to_discard(self, card):
        card_index = self.__play_area.index(card)
        card = self.__play_area.pop(card_index)
        self.__discard.append(card)
    
    def get_play_area(self):
        return self.__play_area
    
    def set_play_area(self, play_area):
        self.__play_area = play_area

    def play_card(self, card, target):
        mana_cost = card.get_mana_cost()
        if self.__current_mana >= mana_cost:
            card.play(target)
            self.__current_mana -= mana_cost
        else:
            print("Pas assez de mana !")
    
    def play_card_from_index(self, card_index, target):
        # Methode pour tester principalement
        self.play_card(self.__hand[card_index], target)

    def display(self):
        return f"Mage {self.__name} ({self.__health_points} pv)"


    def get_current_mana(self):
        return self.__current_mana
    
    def set_current_mana(self, current_mana):
        self.__current_mana = current_mana

    def gain_mana(self, mana):
        self.__current_mana = min(self.__current_mana + mana, self.__maximum_mana)
    
    def regen_mana(self):
        self.__current_mana = self.__maximum_mana
    
    def play_turn(self, opponent):
        if len(self.__hand) == 0:
            print("Impossible de jouer sans carte !")
        else:
            card = self.get_input_card()
            target  = self.get_input_target(opponent)
            self.play_card(card, target)
    
    def get_input_card(self):
        user_input = None
        accepted_inputs = list(range(len(self.__hand)))
        while user_input not in accepted_inputs:
            print("Cartes disponibles :")
            for i, card in enumerate(self.__hand):
                print(f"\t{i}: {card.display()}")
            print("Quelle carte jouer ?")
            user_input = int(input())
            if user_input not in accepted_inputs:
                print("Le numéro de la carte n'est pas bon.")
        return self.__hand[user_input]
    
    def get_input_target(self, opponent: "Mage"):
        user_input = None
        opponent_cards = opponent.get_play_area()
        attackable_cards = [card for card in opponent_cards if card.is_attackable()]
        all_targets = [opponent] + attackable_cards
        accepted_inputs = list(range(len(all_targets)))
        while user_input not in accepted_inputs:
            print("Adversaires attaquables :")
            for i, target in enumerate(all_targets):
                print(f"\t{i}: {target.display()}")
            print("Quelle adversaire attaquer ?")
            user_input = int(input())
            if user_input not in accepted_inputs:
                print("Le numéro d'adversaire n'est pas bon.")
        return all_targets[user_input]
    
mage1 = Mage("Zangar", 50, 10)
mage2 = Mage("Vorph", 50, 5)
cartes_1 = [
    Cristal(0, "Cristal 2", "Octroie du mana", 2),
    Blast(1, "Blast 5", "Boule de feu", 5),
    Creature(2, "Zombie", "Mort-vivant pourri", 5, 10),
]
cartes_2 = [
    Creature(1, "Oiseau", "piaille", 10, 5),
    Creature(3, "Taureau", "déteste le rouge", 20, 15),
]
mage1.add_cards_to_hand(cartes_1)
mage2.add_cards_to_hand(cartes_2)

# # Test: le mage 1 joue toutes ses cartes en attaquant le mage 2
# print(mage2.display())
# print(mage1.get_current_mana())
# mage1.play_card_from_index(2, mage2)
# print(mage1.get_current_mana())
# print(mage2.display())
# mage1.play_card_from_index(1, mage2)
# print(mage1.get_current_mana())
# print(mage2.display())
# mage1.play_card_from_index(0, mage2)
# print(mage1.get_current_mana())
# print(mage2.display())

# # Test: le mage 2 attaque la créature du mage 1
# print("Zones de jeu")
# print(mage1.get_play_area())
# print(mage2.get_play_area())
# print("Discard")
# print(mage1.get_discard())
# print(mage2.get_discard())
# print(mage1.get_play_area()[0].get_status())
# mage2.play_card_from_index(1, mage1.get_play_area()[0])
# print(mage1.get_discard()[-1].get_status())
# print(mage2.get_play_area()[0].get_status())
# print("Zones de jeu")
# print(mage1.get_play_area())
# print(mage2.get_play_area())
# print("Discard")
# print(mage1.get_discard())
# print(mage2.get_discard())

#  Test 3: jouer un tour
# mage1.play_turn(mage2)

# Test 4 : duel
def play_round(player: Mage, opponent: Mage):
    print("Au tour de : " + player.display())
    print("Contre : " + opponent.display())
    player.play_turn(opponent)

while mage1.is_alive() and mage2.is_alive() and len(mage1.get_hand()+mage2.get_hand()) > 0:
    play_round(mage1, mage2)
    if mage2.is_alive():
        play_round(mage2, mage1)

if mage1.is_alive() and mage2.is_alive():
    print("Pas de gagnant")
elif mage1.is_alive():
    print(f"{mage1.get_name()} gagne.")
else:
    print(f"{mage2.get_name()} gagne.")