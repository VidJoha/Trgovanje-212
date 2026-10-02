from tkinter import *
from tkinter import messagebox,Canvas,ttk
import sqlite3
import bcrypt
import unicodedata
from controllers.trgovanje_controller import create_diagonal_gradient,plotaj,build_canvas

connection = sqlite3.connect('dionice.db')
cursor=connection.cursor()

def focus_next(event):
    event.widget.tk_focusNext().focus_set()
    return "break"

def skip_log_in(event=None,log_in_window=None):
    log_in(event,True,log_in_window)

def log_in(event=None,skip=False,log_in_window=None,imeentry=None,prezimeentry=None,lozinkaentry=None):
    print("Idem se ulogirat")
    if(skip==True):
        ime="Vid"
        prezime="Joha"
        lozinka="ajmonakavicu"
    else:
        ime=imeentry.get().strip()
        prezime=prezimeentry.get().strip()
        lozinka=lozinkaentry.get().strip()
    cursor.execute("SELECT PASSWORD_HASH,ID_KORISNIKA FROM KORISNICI WHERE IME_KORISNIKA = ? AND PREZIME_KORISNIKA = ?",(ime,prezime))
    row = cursor.fetchone()
    photos=[]
    if row:
        hash_lozinka = row[0]
        id_korisnika=row[1]
        if bcrypt.checkpw(lozinka.encode('utf-8'), hash_lozinka):
            print("uspjeh")
            log_in_window.destroy()
            
            main_window = Tk()
            main_window.geometry("1000x750")
            main_window.title("Trgovanje212")
            main_window.configure(bg="#ffffff")

            notebook = ttk.Notebook(main_window)
            notebook.pack(pady=10,expand=False)

            dionice_tab = ttk.Frame(notebook)
            investicije_tab = ttk.Frame(notebook)
            options_tab = ttk.Frame(notebook)
            
            notebook.add(dionice_tab, text="Dionice")
            notebook.add(investicije_tab, text="Investicije")
            notebook.add(options_tab,text="Options")
            
            
            canvas1 = Canvas(dionice_tab, width=1000, height=750)
            canvas1.pack(fill="both",expand=True)

            canvas2 = Canvas(investicije_tab, width=1000, height=750)
            canvas2.pack(fill="both",expand=True)

            canvas3 = Canvas(options_tab,width=1000,height=750)
            canvas3.pack(fill="both",expand=True)
            
            build_canvas(main_window,canvas1, canvas2,canvas3,dionice_tab,investicije_tab,options_tab, hash_lozinka, id_korisnika,photos)
            main_window.mainloop()
        else:
            print("fail")
            messagebox.showinfo("Upozorenje","Krivo ime,prezime ili lozinka")
    else:
        print("veci fail")
        messagebox.showinfo("Upozorenje","Krivo ime,prezime ili lozinka")
