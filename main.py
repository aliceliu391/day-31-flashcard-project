from tkinter import *
from tkinter import messagebox
import pandas
import random
new_entry = {}

BACKGROUND_COLOR = "#B1DDC6"

# Data
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/chinese_words.csv")
    data_dict = original_data.to_dict(orient="records")
else:
    data_dict = data.to_dict(orient="records")


def flip_card(entry):

    canvas.itemconfig(flashcard_img, image=card_back)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=entry["English"], fill="white")


def next_card():
    global new_entry, flip_timer
    window.after_cancel(flip_timer)

    try:
        new_entry = random.choice(data_dict)
    except IndexError:
        messagebox.showinfo("Congrats!", "You completed all the cards :)")
        window.destroy()
    else:
        canvas.itemconfig(flashcard_img, image=card_front)
        canvas.itemconfig(card_title, text="Chinese", fill="black")
        canvas.itemconfig(card_word, text=new_entry["Chinese"], fill="black")
        flip_timer = window.after(3000, flip_card, new_entry)


def remove_card():

    global new_entry, data_dict
    data_dict.remove(new_entry)
    new_data = pandas.DataFrame(data_dict)
    new_data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


# Window
window = Tk()
window.title("Stelle Flashcards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, flip_card, new_entry)

# Flashcard
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
flashcard_img = canvas.create_image(400, 263, image=card_front)
card_title = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

# Buttons
right_img = PhotoImage(file="images/right.png")
right_button = Button(image=right_img, highlightthickness=0, bg=BACKGROUND_COLOR, command=remove_card, bd=0)
right_button.grid(column=0, row=1)
wrong_img = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_img, highlightthickness=0, bg=BACKGROUND_COLOR, command=next_card, bd=0)
wrong_button.grid(column=1, row=1)

new_entry = random.choice(data_dict)
next_card()

window.mainloop()
