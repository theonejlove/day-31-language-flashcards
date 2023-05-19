from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    flashcard_data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = flashcard_data.to_dict(orient="records")


# UNKNOWN CARD FUNCTION
def new_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(vocabulary, text=f"{current_card['French']}", fill="black")
    canvas.itemconfig(title, text="French", fill="black")
    canvas.itemconfig(card_image, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)


# KNOWN CARD FUNCTION
def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    new_card()

# TRANSLATED CARD FUNCTION
def flip_card():
    canvas.itemconfig(card_image, image=card_back_img)
    canvas.itemconfig(title, text="English", fill="#ffffff")
    canvas.itemconfig(vocabulary, text=f"{current_card['English']}", fill="#ffffff")

window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)


flip_timer = window.after(3000, func=flip_card)

# THE CANVAS
canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")

card_image = canvas.create_image(400, 263, image=card_front_img)
title = canvas.create_text(400, 150, text="Title", font=("Arial", 40, "italic"))
vocabulary = canvas.create_text(400, 263, text="Word", font=("Arial", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

# YES/NO BUTTONS
correct_image = PhotoImage(file="images/right.png")
correct_button = Button(image=correct_image, highlightthickness=0, command=is_known)
correct_button.grid(row=1, column=1)
wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=new_card)
wrong_button.grid(row=1, column=0)

new_card()

window.mainloop()
