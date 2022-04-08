from tkinter import *
import pandas as pd
import main as m
from tkinter import messagebox as mb


def admin_panel_page(root):
    m.clear(root)

    Label(root, text="Admin panel", font=(None, 15, "bold"), background='red').grid(row=0, column=1, sticky=N)

    change_pass_b = Button(root, text='Change password', bg='yellow', command=lambda: change_adm_pass(root))
    change_pass_b.grid(row=1, column=1, sticky=EW, pady=5, padx=10)

    user_mgmt_b = Button(root, text='Show users', bg='yellow', command=lambda: user_table_page(root))
    user_mgmt_b.grid(row=2, column=1, sticky=EW, pady=5, padx=10)

    add_user_b = Button(root, text='Add user', bg='yellow', command=lambda: add_user_page(root))
    add_user_b.grid(row=3, column=1, sticky=EW, pady=5, padx=10)

    block_user_b = Button(root, text='Block user', bg='yellow', command=lambda: block_user_page(root))
    block_user_b.grid(row=4, column=1, sticky=EW, pady=5, padx=10)

    restrictions_b = Button(root, text='Apply restrictions', bg='yellow', command=lambda: restrictions_page(root))
    restrictions_b.grid(row=5, column=1, sticky=EW, pady=5, padx=10)

    m.additional_buttons(root, 8)


def change_adm_pass(root):
    m.clear(root)

    Label(root, text="Change pass", font=(None, 15, "bold"), background='red').grid(row=0, column=1, sticky=N)

    Label(root, text="Old pass: ", background='red', font="bold").grid(row=1, column=0, sticky=W, pady=10, padx=10)
    old_pass = StringVar()
    old_pass_e = Entry(root, textvariable=old_pass, bg='pink')
    old_pass_e.grid(row=1, column=1, columnspan=3, sticky=W + E, padx=10)

    Label(root, text="New pass: ", background='red', font="bold").grid(row=2, column=0, sticky=W, pady=10, padx=10)
    pass1 = StringVar()
    pass1_e = Entry(root, textvariable=pass1, bg='pink')
    pass1_e.grid(row=2, column=1, columnspan=3, sticky=W + E, padx=10)

    Label(root, text="Repeat your pass: ", background='red', font="bold").grid(row=3, column=0, sticky=W, pady=10, padx=10)
    pass2 = StringVar()
    pass2_e = Entry(root, textvariable=pass2, bg='pink')
    pass2_e.grid(row=3, column=1, columnspan=3, sticky=W + E, padx=10)

    enter_b = Button(root, text='Submit', bg='yellow', command=lambda: m.set_pass_extended("admin", pass1.get(), pass2.get(), old_pass.get()))
    enter_b.grid(row=4, column=1, sticky=EW)

    quit_b = Button(root, text='Return', bg='yellow', command=lambda: admin_panel_page(root))
    quit_b.grid(row=5, column=1, sticky=EW, pady=5)

    m.additional_buttons(root, 6)


def user_table_page(root):
    global df
    m.clear(root)

    df = m.vault_setup()

    Label(root, text="Users status", font=(None, 15, "bold"), background='red').grid(row=0, column=1, sticky=N, pady=5)
    text = Text(root, bg="red", insertborderwidth = 50, insertwidth=2)
    text.insert(END, str(df))
    text.grid(row=1, column=1, sticky=N, pady=5)

    quit_b = Button(root, text='Return', bg='yellow', command=lambda: admin_panel_page(root))
    quit_b.grid(row=2, column=1, sticky=N, pady=5)

    m.additional_buttons(root, 3)


def add_user(user):
    vault = m.vault_setup()
    if vault.loc[vault['user'] == user].values.all():
        usr_zero_point = {"user": user, "pass": "", "blocked": FALSE, "restrictions": TRUE}
        vault_mod = vault.append(usr_zero_point, ignore_index=True)
        vault_mod.to_csv('vault.csv', index=False)
        mb.showinfo(title="Info", message="The user with empty pass was added")
    else:
        mb.showerror(title="Error", message="Such user already exists.")


def add_user_page(root):
    m.clear(root)
    Label(root, text="Add user", font=(None, 15, "bold"), background='red').grid(row=0, column=1, sticky=N, pady=5)

    Label(root, text="Username: ", background='red', font="bold").grid(row=1, column=0, sticky=W, pady=10, padx=10)
    user = StringVar()
    user_e = Entry(root, textvariable=user, bg='pink')
    user_e.grid(row=1, column=1, columnspan=3, sticky=W + E, padx=10)

    enter_b = Button(root, text='Submit', bg='yellow', command=lambda: add_user(user.get()))
    enter_b.grid(row=2, column=1, sticky=N)

    quit_b = Button(root, text='Return', bg='yellow', command=lambda: admin_panel_page(root))
    quit_b.grid(row=3, column=1, sticky=N, pady=5)

    m.additional_buttons(root, 4)


def block_user_page(root):
    m.clear(root)
    Label(root, text="Block user", font=(None, 15, "bold"), background='red').grid(row=0, column=1, sticky=N, pady=5)

    Label(root, text="Username: ", background='red', font="bold").grid(row=1, column=0, sticky=W, pady=10, padx=10)
    user = StringVar()
    user_e = Entry(root, textvariable=user, bg='pink')
    user_e.grid(row=1, column=1, columnspan=3, sticky=W + E, padx=10)

    block_b = Button(root, text='Block', bg='yellow', command=lambda: block(user.get(), True))
    block_b.grid(row=2, column=1, sticky=N, pady=5)

    unblock_b = Button(root, text='Unblock', bg='yellow', command=lambda: block(user.get(), False))
    unblock_b.grid(row=3, column=1, sticky=N, pady=5)

    quit_b = Button(root, text='Return', bg='yellow', command=lambda: admin_panel_page(root))
    quit_b.grid(row=4, column=1, sticky=N, pady=5)

    m.additional_buttons(root, 5)


def block(user, blocked: bool):
    if blocked:
        m.change_vault(user, "blocked", 1)
        mb.showinfo(title="Info", message="The user is blocked")
    else:
        m.change_vault(user, "blocked", 0)
        mb.showinfo(title="Info", message="The user is unblocked")


def restrictions_page(root):
    m.clear(root)
    Label(root, text="Change pass restrictions", font=(None, 15, "bold"), background='red').grid(row=0, column=1, sticky=N, pady=5)

    Label(root, text="Username: ", background='red', font="bold").grid(row=1, column=0, sticky=W, pady=10, padx=10)
    user = StringVar()
    user_e = Entry(root, textvariable=user, bg='pink')
    user_e.grid(row=1, column=1, columnspan=3, sticky=W + E, padx=10)

    block_b = Button(root, text='Restrict', bg='yellow', command=lambda: restrict(user.get(), True))
    block_b.grid(row=2, column=1, sticky=N, pady=5)

    unblock_b = Button(root, text='Allow', bg='yellow', command=lambda: restrict(user.get(), False))
    unblock_b.grid(row=3, column=1, sticky=N, pady=5)

    quit_b = Button(root, text='Return', bg='yellow', command=lambda: admin_panel_page(root))
    quit_b.grid(row=4, column=1, sticky=N, pady=5)

    m.additional_buttons(root, 5)


def restrict(user, restricted: bool):
    if restricted:
        m.change_vault(user, "restrictions", 1)
        mb.showinfo(title="Info", message=f"The restrictions to the {user} was applied")
    else:
        m.change_vault(user, "restrictions", 0)
        mb.showinfo(title="Info", message=f"The restrictions to the {user} was disabled")
