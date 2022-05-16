import re
import os
import adm
import usr
import pandas as pd
import cryptolab as crypto
from tkinter import messagebox as mb
from tkinter import *
import hashlib

# v4 task
pass_policy = '^[a-zA-zа-яА-Я]*$'
faults = 0
columns = ["user", "pass", "blocked", "restrictions"]
admin_setup = ["admin", "", FALSE, TRUE]
info = "The lab was developed by Anastasiia Dorosh FB92.\n" \
       "Password policy for my task is only letters (both Latin and Cyrillic)"


def quit(df):
    crypto.encrypt(df)
    os.remove("tmp-vault.csv")
    exit()


# vault here refers to our file
def vault_setup():
    if os.path.isfile('vault.csv'):
        df = pd.read_csv('vault.csv', encoding='utf-8').drop(["Unnamed: 0"], axis=1)
        # decrypt the vault
        df = crypto.decrypt(df)
        # add data to temp file
        df.to_csv('tmp-vault.csv')
    else:
        df = pd.DataFrame([admin_setup], columns=columns)
        df.to_csv('vault.csv', index=False)
        print(df)
    return df


# changing the temp value
def change_vault(user, field, new_value):
    vault = vault_setup()
    vault.loc[vault['user'] == user, field] = new_value
    vault.to_csv('temp-vault.csv', index=False)


def clear(root):
    for widget in root.winfo_children():
        widget.destroy()


def check_credentials(root, user, passwd, vault):
    global faults
    user_data = vault.loc[vault['user'] == user]
    
    if faults < 2:
        if not user_data.empty:
            if pd.isnull(user_data["pass"]).values:
                set_pass_page(root, user, vault)
            elif user_data["blocked"].item() == 0 and user_data["pass"].item() == passwd:
                if user == "admin":
                    adm.admin_panel_page(root, vault)
                else:
                    usr.user_panel_page(root, user)
            elif user_data["pass"].item() != passwd:
                mb.showerror(title="Error", message="Wrong pass")
                faults += 1
                login_page(root, vault)
            else:
                mb.showerror(title="Error", message="Account was blocked.\nContact administrator for more info")
        else:
            mb.showerror(title="Error", message="No such user")
            clear(root)
            login_page(root, vault)
    else:
        mb.showerror(title="Error", message="Too many unsuccessful attempts.")
        faults = 0
        set_passphrase_window(root, vault)


def set_pass(user, pass1, pass2):
    vault = vault_setup()

    if re.search(pass_policy, pass1) == None and vault.loc[vault["user"] == user]["restrictions"].values[0] == 1:
        mb.showerror(title="Error", message="Please consider password policy. Check the info box")
    elif pass1 == pass2:
        change_vault(user, "pass", pass1)
        mb.showinfo(title="Info", message="The pass was set")
    else:
        mb.showerror(title="Error", message="Passwords do not match")
        return False
    return True


def set_pass_extended(user, pass1, pass2, old_pass):
    vault = vault_setup()
    if not (vault.loc[vault["user"] == user]['pass'][0] == old_pass and set_pass("admin", pass1, pass2)):
        mb.showerror(title="Error", message="Old password do not match. Please check it again")


def set_pass_init(root, user, pass1, pass2):
    if not set_pass(user, pass1, pass2):
        set_pass_page(root, user)


def set_pass_page(root, user, df):
    clear(root)

    Label(root, text="Set pass", font=(None, 15, "bold"), background= 'red').grid(row=0, column=1, sticky=N)

    Label(root, text="Pass1: ", background='red', font="bold").grid(row=1, column=0, sticky=W, pady=10, padx=10)
    pass1 = StringVar()
    user_e = Entry(root, textvariable=pass1, bg='pink')
    user_e.grid(row=1, column=1, columnspan=3, sticky=W + E, padx=10)

    Label(root, text="Pass2: ", background='red', font="bold").grid(row=2, column=0, sticky=W, pady=10, padx=10)
    pass2 = StringVar()
    pass_e=Entry(root, textvariable=pass2, bg='pink')
    pass_e.grid(row=2, column=1, columnspan=3, sticky=W + E, padx=10)

    enter_b = Button(root, text='Submit', bg='yellow', command=lambda: set_pass_init(root, user, pass1.get(), pass2.get()))
    enter_b.grid(row=3, column=1, sticky=N)

    quit_b = Button(root, text='Return', bg='yellow', command=lambda: login_page(root, df))
    quit_b.grid(row=4, column=1, sticky=N, pady=5)

    additional_buttons(root, 5, df)


def additional_buttons(root, row, df):
    info_ba = Button(root, text='Info', bg='yellow', command=lambda: mb.showinfo(title="Info", message=info))
    info_ba.grid(row=row, column=1, sticky=EW, pady=5, padx=10)
    
    quit_b = Button(root, text='Quit', bg='yellow', command=lambda: set_passphrase_window(root, df))
    quit_b.grid(row=row+1, column=1, sticky=EW, pady=5, padx=10)


def login_page(root, df):
    clear(root)
    root['bg'] = 'red'
    root.title('lab1')
    # root.geometry('250x200')
    Label(root, text="Login", font=(None, 15, "bold"), background= 'red').grid(row=0, column=1, sticky=N)

    Label(root, text="User: ", background='red', font="bold").grid(row=1, column=0, sticky=W, pady=10, padx=10)
    user = StringVar()
    user_e = Entry(root, textvariable=user, bg='pink')
    user_e.grid(row=1, column=1, columnspan=3, sticky=W + E, padx=10)

    Label(root, text="Pass: ", background='red', font="bold").grid(row=2, column=0, sticky=W, pady=10, padx=10)
    passwd = StringVar()
    pass_e=Entry(root, textvariable=passwd, bg='pink')
    pass_e.grid(row=2, column=1, columnspan=3, sticky=W + E, padx=10)

    enter_b = Button(root, text='Submit', bg='yellow', command=lambda: check_credentials(root, user.get(), passwd.get(), df))
    enter_b.grid(row=3, column=1, sticky=N)

    additional_buttons(root, 4, df)


# check the pass
def check_phrase_window(root, df):
    clear(root)

    Label(root, text="Passphrase: ", background='red', font="bold").grid(row=1, column=0, sticky=W, pady=10, padx=10)
    phrase = StringVar()
    phrase_e = Entry(root, textvariable=phrase, bg='pink')
    phrase_e.grid(row=1, column=1, columnspan=3, sticky=W + E, padx=10)

    enter_b = Button(root, text='Submit', bg='yellow', command=lambda: check_phrase(root, phrase, df))
    enter_b.grid(row=3, column=1, sticky=N)

    additional_buttons(root, 4, df)


def check_phrase(root, phrase, df):
    f = open("master.key", "r")
    phrase = str(phrase)
    phrase_hash = hashlib.md5(phrase.encode()).hexdigest()
    print(phrase_hash)

    if phrase_hash == f.read():
        login_page(root, df)
    else:
        mb.showerror("Error", "The passphrase is wrong")

    f.close()


def set_passphrase_window(root, df):
    clear(root)

    Label(root, text="Passphrase: ", background='red', font="bold").grid(row=1, column=0, sticky=W, pady=10, padx=10)
    phrase = StringVar()
    phrase_e = Entry(root, textvariable=phrase, bg='pink')
    phrase_e.grid(row=1, column=1, columnspan=3, sticky=W + E, padx=10)

    enter_b = Button(root, text='Submit', bg='yellow', command=lambda: set_passphrase(phrase, df))
    enter_b.grid(row=3, column=1, sticky=N)

    additional_buttons(root, 4, df)


def set_passphrase(phrase, df):
    f = open("master.key", "w")
    phrase = str(phrase)
    phrase_hash = hashlib.md5(phrase.encode()).hexdigest()
    f.write(phrase_hash)
    f.close()

    mb.showinfo("Info", "The passphrase was set")
    quit(df)


if __name__ == '__main__':
    root = Tk()
    df = vault_setup()
    check_phrase_window(root, df)
    root.mainloop()
