import random


class Card:

  def __init__(self, suit, rank, value):
    self.suit = suit
    self.rank = rank
    self.value = value

  def __str__(self):
    return f"{self.rank} of {self.suit}"


class Deck:

  def __init__(self):
    self.cards = []
    suits = ["♠️", "♣️", "♥️", "♦️"]
    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    values = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

    for suit in suits:
      for i in range(0, 12):
        self.cards.append(Card(suit, ranks[i], values[i]))

  def shuffle(self):
    if len(self.cards) > 1:
      random.shuffle(self.cards)

  def deal(self, amount):
    cards_dealt = []
    if len(self.cards) > 0:
      for i in range(amount):
        card = self.cards.pop()
        cards_dealt.append(card)
    return cards_dealt


class Hand:

  def __init__(self, dealer=False):
    self.cards = []
    self.value = 0
    self.dealer = dealer

  def add_card(self, card_list):
    self.cards.extend(card_list)

  def calculate_value(self):
    self.value = 0
    has_ace = False

    for card in self.cards:
      self.value += int(card.value)
      if card.rank == "A":
        has_ace = True

    if has_ace and self.value > 21:
      self.value -= 10

  def get_value(self):
    self.calculate_value()
    return self.value

  def is_blackjack(self):
    return self.get_value() == 21

  def display(self, show_all_dealer_cards=False):
    print(f'''{"Dealers's" if self.dealer else "Your"} hand:''')
    for index, card in enumerate(self.cards):
      if index == 0 and self.dealer \
      and not show_all_dealer_cards \
      and not self.is_blackjack():
        print("Hidden")
      else:
        print(card)

    if not self.dealer:
      print("Value:", self.get_value())
    print()


class Game():

  def __innit__(self):
    pass

  def play(self):
    game_number = 0
    games_to_play = 0

    while games_to_play <= 0:
      try:
        games_to_play = int(input("How many games do you want to play? "))
      except:
        print("You must enter a number.")

    while game_number < games_to_play:
      game_number += 1

      deck = Deck()
      deck.shuffle()

      player_hand = Hand()
      dealer_hand = Hand(dealer=True)

      for i in range(2):
        player_hand.add_card(deck.deal(1))
        dealer_hand.add_card(deck.deal(1))

      print()
      print("*" * 30)
      print(f"{(game_number-1)*'🟩'}{(games_to_play-(game_number-1))*'⬜️'}")
      print("*" * 30)

      player_hand.display()
      dealer_hand.display()

      if self.check_win(player_hand, dealer_hand):
        continue

      choice = ""

      while player_hand.get_value() < 21 and choice not in [
          "s", "stand"
      ] and dealer_hand.get_value() != 21:
        choice = input("Please choose 'Hit' or 'Stand': ").lower()
        while choice not in ["s", "h", "hit", "stand"]:
          choice = input("Enter either 'Hit' or 'Stand' (or H/S): ").lower()
        print()
        if choice in ["h", "hit"]:
          player_hand.add_card(deck.deal(1))
          player_hand.display()

      if self.check_win(player_hand, dealer_hand):
        continue

      player_hand_value = player_hand.get_value()
      dealer_hand_value = dealer_hand.get_value()

      while dealer_hand_value < 17:
        print("\nDealer draws...\n")
        dealer_hand.add_card(deck.deal(1))
        dealer_hand_value = dealer_hand.get_value()

      dealer_hand.display(show_all_dealer_cards=True)

      if self.check_win(player_hand, dealer_hand):
        continue

      print("\nFinal Results")
      print("Your hand:", player_hand_value)
      print("Dealer's hand:", dealer_hand_value)

      self.check_win(player_hand, dealer_hand, True)

    print("\nThanks for playing!")

  def check_win(self, player_hand, dealer_hand, game_over=False):
    if not game_over:
      if player_hand.get_value() > 21:
        print("You busted! Dealer wins.")
        return True
      elif dealer_hand.get_value() > 21:
        print("Dealer busted! You win.")
        return True
      elif dealer_hand.is_blackjack() and player_hand.is_blackjack():
        print("Both players have blackjack! Tie!")
        return True
      elif player_hand.is_blackjack():
        print("You have a blackjack! You win!")
        return True
      elif dealer_hand.is_blackjack():
        print("The Dealer has a blackjack! Dealer wins!")
        return True
    else:
      if player_hand.get_value() > dealer_hand.get_value():
        print("You win!")
      elif player_hand.get_value() == dealer_hand.get_value():
        print("It's a Tie!")
      else:
        print("Dealer wins.")
      return True
    return False


g = Game()
g.play()
