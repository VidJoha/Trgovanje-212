import tkinter as tk

class AutocompleteEntry(tk.Frame):
    def __init__(self, master, sve_opcije,on_change=None *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.on_choose=on_change
        self.sve_opcije = sve_opcije
        self.master_window = master
        self._hide_job = None
        self._suppress_open = False

        # 1. Polje za unos
        self.var = tk.StringVar(master=self)
        self.entry = tk.Entry(self, textvariable=self.var, font=('Times New Roman', 12))
        self.entry.pack(fill="x", expand=True)

        self.entry.bind('<KeyRelease>', self.on_key_release)
        self.entry.bind('<FocusIn>', self.on_focus_in)
        self.entry.bind('<Button-1>', self.on_focus_in)
        self.entry.bind('<FocusOut>', self.odgodi_sakrivanje)
        self.entry.bind('<Down>', self.on_down)
        self.entry.bind('<Return>', self.on_return)
        self.entry.bind('<Escape>', lambda e: self.sakrij_listu())

        # 2. Listbox kao padajući izbornik
        self.listbox = tk.Listbox(
            master,
            font=('Times New Roman', 12),
            height=4,
            exportselection=False,
            activestyle='none'
        )
        self.listbox.bind('<ButtonRelease-1>', self.on_select)
        self.listbox.bind('<Return>', self.on_select)
        self.listbox.bind('<Escape>', lambda e: (self.sakrij_listu(), self.entry.focus_set()))

    # ---------- događaji ----------
    def on_focus_in(self, event=None):
        self.otkazi_sakrivanje()
        self.after(10, self.filtriraj)

    def on_key_release(self, event):
        if event.keysym in ('Up', 'Down', 'Return', 'Escape', 'Tab',
                            'Left', 'Right', 'Shift_L', 'Shift_R',
                            'Control_L', 'Control_R'):
            return
        self.filtriraj()
        if self.on_change:
            self.on_change(self.entry.get())

    # ---------- filtriranje i prikaz ----------

    def filtriraj(self):
        # Provjera u trenutku izvođenja, a ne pri zakazivanju
        if self._suppress_open:
            return

        typed = self.entry.get()
        if typed == '':
            self.prikazi_listu(self.sve_opcije)
            return

        filtered = [item for item in self.sve_opcije
                    if typed.lower() in str(item).lower()]
        if filtered:
            self.prikazi_listu(filtered)
        else:
            self.sakrij_listu()

    def prikazi_listu(self, opcije):
        self.otkazi_sakrivanje()
        self.listbox.delete(0, tk.END)
        for opcija in opcije:
            self.listbox.insert(tk.END, opcija)

        self.update_idletasks()
        x = self.entry.winfo_rootx() - self.master_window.winfo_rootx()
        y = (self.entry.winfo_rooty() - self.master_window.winfo_rooty()
             + self.entry.winfo_height())
        width = self.entry.winfo_width()
        self.listbox.place(x=x, y=y, width=width)
        self.listbox.lift()

    def sakrij_listu(self):
        self.listbox.place_forget()

    # ---------- sakrivanje ----------
    def otkazi_sakrivanje(self):
        if self._hide_job is not None:
            self.after_cancel(self._hide_job)
            self._hide_job = None

    def odgodi_sakrivanje(self, event=None):
        self.otkazi_sakrivanje()
        self._hide_job = self.after(150, self.provjeri_fokus)

    def provjeri_fokus(self):
        self._hide_job = None
        try:
            fokus = self.focus_get()
        except KeyError:
            fokus = None
        # Sakrij samo ako fokus nije ni na Entryju ni na listboxu
        if fokus not in (self.entry, self.listbox):
            self.sakrij_listu()

    # ---------- tipkovnica ----------
    def on_down(self, event):
        if self.listbox.winfo_ismapped() and self.listbox.size() > 0:
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(0)
            self.listbox.activate(0)
            self.listbox.focus_set()
        return "break"

    def on_return(self, event):
        if self.listbox.winfo_ismapped() and self.listbox.size() == 1:
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(0)
            self.on_select()
        return "break"

    # ---------- odabir ----------
    def on_select(self, event=None):
        if event is not None and event.type == tk.EventType.ButtonRelease:
            index = self.listbox.nearest(event.y)
            if index < 0 or index >= self.listbox.size():
                return "break"
        else:
            sel = self.listbox.curselection()
            if not sel:
                return "break"
            index = sel[0]

        selected_value = self.listbox.get(index)

        self._suppress_open = True
        self.otkazi_sakrivanje()

        # Upis izravno u Entry (neovisno o StringVar-u)
        self.entry.delete(0, tk.END)
        self.entry.insert(0, selected_value)
        self.entry.icursor(tk.END)
        if self.on_change:
            self.on_change(selected_value)
        self.sakrij_listu()
        self.entry.focus_set()

        self.after(300, self._dopusti_otvaranje)
        return "break"

    def _dopusti_otvaranje(self):
        self._suppress_open = False

    def get(self):
        return self.var.get()