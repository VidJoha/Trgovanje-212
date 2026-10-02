from controllers.ulogiravanje_controller import focus_next,skip_log_in,log_in

from tkinter import *
from tkinter import messagebox,ttk

log_in_window = Tk()
log_in_window.geometry("1000x700")
log_in_window.title("Log in 212")

label = Label(log_in_window,text="Ulogiraj se 212",font=('Times New Roman',50))
label.pack(padx=50,pady=50)

labelime = Label(log_in_window,text="Ime",font=('Times New Roman',10))
labelime.pack()
imeentry=Entry(log_in_window)
imeentry.pack()
imeentry.bind('<Return>', focus_next)

labelprezime = Label(log_in_window,text="Prezime",font=('Times New Roman',10))
labelprezime.pack()
prezimeentry=Entry(log_in_window)
prezimeentry.pack()
prezimeentry.bind('<Return>', focus_next)

labellozinka = Label(log_in_window,text="Lozinka",font=('Times New Roman',10))
labellozinka.pack()
lozinkaentry=Entry(log_in_window,show="*")
lozinkaentry.pack()
lozinkaentry.bind('<Return>', lambda event: log_in(log_in_window=log_in_window,imeentry=imeentry,prezimeentry=prezimeentry,lozinkaentry=lozinkaentry))

log_in_button = Button(log_in_window, text="Ulogiraj me",font=('Times New Roman',10), command=lambda: log_in(log_in_window=log_in_window,imeentry=imeentry,prezimeentry=prezimeentry,lozinkaentry=lozinkaentry))
log_in_button.pack()

skip_button = Button(log_in_window, text="Skip",font=('Times New Roman',10), command=lambda: skip_log_in(log_in_window=log_in_window))
skip_button.pack()

log_in_window.mainloop()
