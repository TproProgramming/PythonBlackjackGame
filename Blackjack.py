"""
Author: Tyler Provencher tyler@provenchermultimedia.com
5/5/2023
This is a simple one-player command prompt Blackjack game implemented in Python. It allows you to play against a computerized dealer. 
Place bets, choose to hit or stand, and try to beat the dealer's hand without going over 21. 
The game keeps track of your balance and lets you play multiple rounds until you decide to quit or run out of money
"""

import random

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = self.get_value()

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    def get_value(self):
        if self.rank in ["J", "Q", "K"]:
            return 10
        elif self.rank == "A":
            return 11
        else:
            return int(self.rank)


class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        for suit in ["Hearts", "Diamonds", "Clubs", "Spades"]:
            for rank in range(2, 11):
                self.cards.append(Card(suit, str(rank)))
            for rank in ["J", "Q", "K", "A"]:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()


class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += card.value
        if self.value > 21 and self.has_ace():
            self.value -= 10

    def has_ace(self):
        for card in self.cards:
            if card.rank == "A":
                return True
        return False

    def __str__(self):
        return ", ".join(str(card) for card in self.cards)


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = Hand()
        self.balance = 1000

    def add_card_to_hand(self, card):
        self.hand.add_card(card)

    def clear_hand(self):
        self.hand = Hand()

    def __str__(self):
        return f"{self.name}: {self.hand} (Balance: {self.balance})"
    
    def place_bet(self):
        while True:
            try:
                bet = int(input(f"{self.name}, place your bet (current balance: {self.balance}): "))
                if bet <= self.balance:
                    self.balance -= bet
                    return bet
                else:
                    print("Invalid bet. Please enter a bet within your balance.")
            except ValueError:
                print("Invalid bet. Please enter a valid number.")


class Dealer(Player):
    def __init__(self):
        super().__init__("Dealer")

    def show_one_card(self):
        return str(self.hand.cards[0])


class Blackjack:
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.player = Player("Player")
        self.dealer = Dealer()

    def play(self):
        bet = self.player.place_bet()
        
        for i in range(2):
            self.player.add_card_to_hand(self.deck.deal_card())
            self.dealer.add_card_to_hand(self.deck.deal_card())

        print(f"Dealer's card: {self.dealer.show_one_card()}")
        print(self.player)


        while True:
            choice = input(f"{self.player.name}, do you want to hit or stand? ")
            if choice.lower() == "hit":
                self.player.add_card_to_hand(self.deck.deal_card())
                print(self.player)
                if self.player.hand.value > 21:
                    print(f"{self.player.name} busts!")
                    self.player.balance -= bet
                    print(f"{self.player.name} loses! (-{bet})")
                    print(f"{self.player.name} current balance: {self.player.balance}")
                    break
            elif choice.lower() == "stand":
                break
            else:
                print("Invalid choice. Please choose hit or stand.")

        while self.dealer.hand.value < 17:
            self.dealer.add_card_to_hand(self.deck.deal_card())
        print(f"Dealer's hand: {self.dealer.hand}")
        if self.dealer.hand.value > 21:
            print("Dealer busts!")
            self.player.balance += bet*2
            print(f"{self.player.name} wins! (+{bet})")
            print(f"{self.player.name} current balance: {self.player.balance}")
        else:
            if self.player.hand.value > 21:
                print(f"{self.player.name} loses! (-{bet})")
                print(f"{self.player.name} current balance: {self.player.balance}")
            elif self.player.hand.value > self.dealer.hand.value:
                self.player.balance += bet*2
                print(f"{self.player.name} wins! (+{bet})")
                print(f"{self.player.name} current balance: {self.player.balance}")
            elif self.player.hand.value == self.dealer.hand.value:
                self.player.balance += bet*2
                print(f"{self.player.name} and Dealer tie! (+{bet})")
                print(f"{self.player.name} current balance: {self.player.balance}")
            else:
                print(f"{self.player.name} loses! (-{bet})")
                print(f"{self.player.name} current balance: {self.player.balance}")
        self.reset()

    def reset(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.player.clear_hand()
        self.dealer.clear_hand()

    def start(self):
        while True:
            self.play()
            if self.player.balance == 0:
                print("Game Over! House Wins:(\nYou ran out of money loser:(")
                break
            choice = input("Do you want to play again? (y/n) ")
            if choice.lower() == "n":
                break

if __name__ == "__main__":
    game = Blackjack()
    game.start()
