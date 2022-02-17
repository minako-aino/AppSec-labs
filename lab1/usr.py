from tkinter import *
import main as m


def user_panel_page(root, user):
    m.clear(root)

    Label(root, text="User panel", font=(None, 15, "bold"), background='red').grid(row=0, column=1, sticky=N)

    change_pass_b = Button(root, text='Change password', bg='yellow', command=lambda: change_usr_pass(root, user))
    change_pass_b.grid(row=1, column=1, sticky=EW, pady=5, padx=10)

    m.additional_buttons(root, 3)


def change_usr_pass(root, user):
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

    enter_b = Button(root, text='Submit', bg='yellow', command=lambda: m.set_pass_extended(user, pass1.get(), pass2.get(), old_pass.get()))
    enter_b.grid(row=4, column=1, sticky=EW)

    quit_b = Button(root, text='Return', bg='yellow', command=lambda: user_panel_page(root))
    quit_b.grid(row=5, column=1, sticky=EW, pady=5)

    m.additional_buttons(root, 6)