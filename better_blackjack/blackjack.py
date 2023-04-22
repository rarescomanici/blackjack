import random

try:
    import tkinter
except ImportError:     # python 2
    import Tkinter as tkinter


def load_images(card_images):
    suits = ["heart", "club", "diamond", "spade"]
    face_cards = ["jack", "queen", "king"]

    if tkinter.TkVersion >= 8.6:
        extension = "png"
    else:
        extension = "ppm"

    # for each suite retrieve the image for the cards
    for suit in suits:
        # first the numbers 1 to 10
        for card in range(1, 11):
            name = "cards/{}_{}.{}".format(str(card), suit, extension)
            image = tkinter.PhotoImage(file=name)
            card_images.append((card, image, ))

        # next, the face cards
        for card in face_cards:
            name = "cards/{}_{}.{}".format(str(card), suit, extension)
            image = tkinter.PhotoImage(file=name)
            card_images.append((10, image, ))


def deal_card(frame):
    # pop the next card off the top of the deck
    next_card = deck.pop(0)

    # and add it to the back of the pack
    deck.append(next_card)

    # add the image to a label and display the label
    tkinter.Label(frame, image=next_card[1], relief="raised").pack(side="left")

    # now return the card's face value
    return next_card


def score_hand(hand):
    # Calculate the total score of all cards passed to it
    # Only one ace can have the value 11, reduce to 1 if the hand will bust
    score = 0
    ace = False
    for next_card in hand:
        card_value = next_card[0]
        if card_value == 1 and not ace:
            ace = True
            card_value = 11
        score += card_value
        # if we would bust, check if there's an ace and subtract 10
        if score > 1 and ace:
            score -= 10
            ace = False
    return score


def hold():
    global game_finished, times_won, times_lost
    if not game_finished:
        dealer_hand.append(deal_card(dealer_card_frame))
        dealer_score = score_hand(dealer_hand)
        player_score = score_hand(player_hand)
        while dealer_score < player_score or dealer_score < 17:
            dealer_hand.append(deal_card(dealer_card_frame))
            dealer_score = score_hand(dealer_hand)
        dealer_score_label.set(dealer_score)
        game_finished = True

        if player_score > 21:
            result_text.set("Dealer wins!")
            times_lost += 1
        elif dealer_score > 21 or dealer_score < player_score:
            result_text.set("You win!")
            times_won += 1
        elif dealer_score > player_score:
            result_text.set("Dealer wins!")
            times_lost += 1
        else:
            result_text.set("Draw!")


def deal():
    global game_finished, times_lost
    if not game_finished:
        player_hand.append(deal_card(player_card_frame))
        player_score = score_hand(player_hand)
        player_score_label.set(player_score)
        if player_score > 21:
            result_text.set("Bust!")
            game_finished = True
            times_lost += 1


def new_game():
    global dealer_card_frame, player_card_frame
    global dealer_hand, player_hand
    global game_finished
    result_text.set("Deal!")

    # parameter to check if the game is finished
    game_finished = False

    # embedded frame to hold the card images
    dealer_card_frame.destroy()
    dealer_card_frame = tkinter.Frame(card_frame, background="green")
    dealer_card_frame.grid(row=0, column=1, sticky="ew", rowspan=2)
    player_card_frame.destroy()
    player_card_frame = tkinter.Frame(card_frame, background="green")
    player_card_frame.grid(row=2, column=1, sticky="ew", rowspan=2)

    # updating the win/loss entries
    win_text.set("Won {} times!".format(times_won))
    loss_text.set("Lost {} times!".format(times_lost))

    # create the lists to store the dealer's and player's hands
    dealer_hand = []
    player_hand = []

    dealer_hand.append(deal_card(dealer_card_frame))
    dealer_score_label.set(score_hand(dealer_hand))
    player_hand.append(deal_card(player_card_frame))
    player_hand.append(deal_card(player_card_frame))
    player_score_label.set(score_hand(player_hand))


def shuffle():
    random.shuffle(deck)


# tally the times won/lost
times_won = 0
times_lost = 0

mainWindow = tkinter.Tk()
mainWindow.title("Blackjack")
mainWindow.geometry("640x480")
mainWindow.resizable(False, False)
mainWindow.configure(background="green")

# Set up the screen in frames for the dealer and player
result_text = tkinter.StringVar()
result = tkinter.Label(mainWindow, textvariable=result_text)
result_text.set("Deal!")
result.grid(row=0, column=0, columnspan=3)

card_frame = tkinter.Frame(mainWindow, relief="sunken", borderwidth=1, background="green")
card_frame.grid(row=1, column=0, sticky="ew", columnspan=3, rowspan=2)

dealer_score_label = tkinter.IntVar()
tkinter.Label(card_frame, text="Dealer", background="green", fg="white") \
    .grid(row=0, column=0)
tkinter.Label(card_frame, textvariable=dealer_score_label, background="green", fg="white") \
    .grid(row=1, column=0)

# embedded frame to hold the card images
dealer_card_frame = tkinter.Frame(card_frame, background="green")
dealer_card_frame.grid(row=0, column=1, sticky="ew", rowspan=2)

player_score_label = tkinter.IntVar()
tkinter.Label(card_frame, text="Player", background="green", fg="white") \
    .grid(row=2, column=0)
tkinter.Label(card_frame, textvariable=player_score_label, background="green", fg="white") \
    .grid(row=3, column=0)

# embedded frame to hold the card images
player_card_frame = tkinter.Frame(card_frame, background="green")
player_card_frame.grid(row=2, column=1, sticky="ew", rowspan=2)

button_frame = tkinter.Frame(mainWindow)
button_frame.grid(row=3, column=0, columnspan=3, sticky="w")

deal_button = tkinter.Button(button_frame, text="Deal", command=deal)
deal_button.grid(row=0, column=0)

hold_button = tkinter.Button(button_frame, text="Hold", command=hold)
hold_button.grid(row=0, column=2)

game_button = tkinter.Button(button_frame, text="New Game", command=new_game)
game_button.grid(row=0, column=4)

shuffle_button = tkinter.Button(button_frame, text="Shuffle", command=shuffle)
shuffle_button.grid(row=0, column=6)

# frame to display number of times won/lost
win_frame = tkinter.LabelFrame(mainWindow, text="Times won:")
win_frame.grid(row=4, column=0, columnspan=3, sticky="w")
win_text = tkinter.StringVar()
win = tkinter.Label(win_frame, textvariable=win_text)
win_text.set("Won {} times!".format(times_won))
win.grid(row=0, column=0, columnspan=3)

loss_frame = tkinter.LabelFrame(mainWindow, text="Times lost:")
loss_frame.grid(row=5, column=0, columnspan=3, sticky="w")
loss_text = tkinter.StringVar()
loss = tkinter.Label(loss_frame, textvariable=loss_text)
loss_text.set("Lost {} times!".format(times_lost))
loss.grid(row=0, column=0, columnspan=3)

# load cards
cards = []
load_images(cards)

# create a new deck of cards and shuffle them
deck = list(cards)
shuffle()

# create the lists to store the dealer's and player's hands
dealer_hand = []
player_hand = []

# parameter to check if the game is finished
game_finished = False

new_game()

mainWindow.mainloop()
