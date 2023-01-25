from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    password_entry.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for letter in range(randint(8, 10))]
    password_symbols = [choice(symbols) for symbol in range(randint(2, 4))]
    password_numbers = [choice(numbers) for number in range(randint(2, 4))]
    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    pyperclip.copy(password)
    password_entry.insert(0, password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {website.upper(): {"email": email, "password": password}}

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Error", message="Fields can't be empty!")
    else:
        is_ok = messagebox.askokcancel(title=website,
                                       message=f"These are the details entered: \nEmail:{email} \nPassword: {password} \nSave?")
        if is_ok:
            try:
                with open("data.json", "r") as data_file:
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                data.update(new_data)
                with open("data.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)

            website_entry.delete(0, END)
            password_entry.delete(0, END)
            website_entry.focus()


# ---------------------------- SEARCH DATA ------------------------------- #
def search():
    search_website = website_entry.get().upper()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
        searched_password = data[search_website]["password"]
        searched_email = data[search_website]["email"]
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Stored!")
    except KeyError:
        messagebox.showinfo(title="Error", message="Website Entered Not Found!")
    else:
        password_entry.delete(0, END)
        password_entry.insert(0, searched_password)
        email_entry.delete(0, END)
        email_entry.insert(0, searched_email)
        #messagebox.showinfo(title="Search", message=f"Website: {search_website.title()}\n Password: {searched_password}")


# ---------------------------- UI SETUP ------------------------------- #
root = Tk()
root.title("Password Manager")
root.config(padx=20, pady=20)

logo = PhotoImage(file="logo.png")
canvas = Canvas(width=200, height=200)
canvas.create_image(100, 100, image=logo)

website_label = Label(root, text="Website:")
email_label = Label(root, text="Email/Username:")
password_label = Label(root, text="Password:")
website_entry = Entry(root, width=33)
email_entry = Entry(root, width=51)
password_entry = Entry(root, width=33)
search_button = Button(root, text="Search", width=14, command=search)
generate_button = Button(root, text="Generate Password", command=generate_password)
add_button = Button(root, text="Add", width=43, command=save)

canvas.grid(row=0, column=1)
website_label.grid(row=1, column=0)
email_label.grid(row=2, column=0)
password_label.grid(row=3, column=0)
website_entry.grid(row=1, column=1)
website_entry.focus()
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "example@email.com")
password_entry.grid(row=3, column=1)
search_button.grid(row=1, column=2)
generate_button.grid(row=3, column=2)
add_button.grid(row=4, column=1, columnspan=2)


root.mainloop()
