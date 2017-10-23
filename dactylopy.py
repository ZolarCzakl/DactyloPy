"""
Logiciel d'entrainement à la dactylographie.
Optimisé pour les romans et le respect des caractères spéciaux.

License Libre
rod.cat@free.fr
"""
import time
import pickle
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox


def affichage(text, debut='1.0'):    
    page.delete(1.0, END)
    page.insert(1.0, text)
    page.mark_set("insert", debut)   
    page.tag_add('now', INSERT, INSERT + "+1c")
    page.see("insert")
    page.focus_force()
    first_key.set(True)
    frappes.set(0)
    ligne.set(0)
    caractere.set(0)
    if pop_up.get():        
        messagebox.showinfo('Info',
                            'Sélectionnez une partie du texte\n'
                            'ou commencez à taper\n'
                            "(Esc pour terminer l'entrainement).")
        pop_up.set(False)

def pickle_access(debut):
    with open('save.pkl', 'rb') as save:
        repertoire = pickle.load(save)
    with open('save.pkl', 'wb') as save:
        repertoire[adresse.get()] = debut
        pickle.dump(repertoire, save)

def save(debut):
    """Sauvegarde ou renvoi l'emplacement du curseur dans le texte."""
    if status.get() == 'ouvrir':
        debut = '1.0'
        try:            
            with open('save.pkl', 'rb') as save:
                repertoire = pickle.load(save)                
                if adresse.get() in repertoire:
                    debut = repertoire[adresse.get()]                    
                else:                    
                    repertoire[adresse.get()] = '1.0'
                    with open('save.pkl', 'wb') as save:
                        pickle.dump(repertoire, save)
        except FileNotFoundError:
            with open('save.pkl', 'wb') as save:                
                repertoire = {adresse.get():'1.0'}
                pickle.dump(repertoire, save)
        return debut
    elif status.get() == 'selection_start':
        pickle_access(debut)        
    elif status.get() == 'selection_stop':
        pickle_access(debut)        
    else:
        pickle_access(debut)            
           
def chargement():
    debut = '1.0'
    adresse.set(filedialog.askopenfilename())    
    try:        
        with open(adresse.get()) as text_brut:
            text = text_brut.read()            
        total_car = len(text)
        status.set('ouvrir')
        debut = save(debut)        
        affichage(text,debut)
    except:
        text = "Désolé, je ne peux pas ouvrir ce fichier :("
        affichage(text, 1.0)

def sup_retour():
    """Mise en page des .txt téléchagés depuis le projet Gutenberg."""
    retour = False
    text = page.get(1.0, END)
    new_text = ''
    for char in text:
        if char == '\n':
            if retour == True:
                retour = False
            else:
                new_text += char
                retour = True
        else:                
            new_text += char
    affichage(new_text,0.1)

def now(event):
    page.tag_remove('now', 1.0, END)
    page.tag_add('now', CURRENT, CURRENT + "+1c")
    print(page.index(CURRENT))

def good(ici):
    page.tag_remove('now', 1.0, END)
    page.tag_add('now', ici, ici + "+1c")
    page.tag_add('good', INSERT, ici)    

def wrong(ici):
    page.tag_remove('now', 1.0, END)
    page.tag_add('now', ici, ici + "+1c")
    page.tag_add('wrong', INSERT, ici)

def chrono(start_stop):    
    if start_stop == 'start':
        timing.set(time.time())        
    else:
        total = time.time() - timing.get()
        if start_stop == 'stop':
            if status.get() == 'selection_start':
                sel_start = debut_sel.get().split('.')
                print('depart du txt original', sel_start)
                ligne.set(int(sel_start[0]) + ligne.get())
                print('nombre de ligne =', ligne.get())
                caractere.set(int(sel_start[1]) + caractere.get())
                print('nombre de caractère =', caractere.get())
                debut = str(ligne.get()) + '.' + str(caractere.get())  
                print('nouvel index', debut)
                status.set('selection_stop')
            else:
                debut = page.index(INSERT)
            status.set('fermer')
            save(debut)
            score = round(frappes.get() / total, 2)
            text = "Félicitations!\n\n{} caractères par seconde".format(score)
            affichage(text, 1.0)
            

def stop_chrono(event):
    answer = messagebox.askyesno('Stop?',
                                 "Stopper l'entrainement?",
                                 icon='question')
    if answer:
        chrono('stop')
        
        

def check(event):
    """Verifie et comptabilise les frappes."""    
    if first_key.get():        
        chrono('start')
        first_key.set(False)
    if event.char == '':        
        pass
    elif event.char == page.get(INSERT, INSERT + "+1c"):
        frappes.set(frappes.get() + 1)
        caractere.set(caractere.get() + 1)
        page.mark_set("ici", INSERT + "+1c")
        good('ici')
        page.mark_set("insert", INSERT + "+1c")        
        return "break"
    else:        
        page.mark_set("ici", INSERT + "+1c")
        wrong('ici')
        page.mark_set("insert", INSERT + "+1c")        
        return "break"

def correction(event):
    """Action de la touche BackSpace."""
    page.mark_set("insert", "insert -1 chars")
    page.tag_remove('wrong', INSERT, INSERT + "+1c")
    page.tag_remove('now', 1.0, END)
    page.tag_add('now', INSERT, INSERT + "+1c")
    return "break"

def retour(event):
    """Action de la touche Return"""        
    if page.get(INSERT, INSERT + "+1c") == '\n':
        frappes.set(frappes.get() + 1)
        ligne.set(ligne.get() + 1)
        caractere.set(0)
        pos = page.index(INSERT)
        line = int(pos.split('.')[0]) + 1
        if pos == page.index("end - 1 chars"):
            chrono('stop')
        else:
            page.mark_set("insert", '%d.%d' % (line,0))
            page.tag_remove('now', 1.0, END)
            page.tag_add('now', INSERT, INSERT + "+1c")
    else:
        page.mark_set("ici", INSERT + "+1c")
        wrong('ici')
        page.mark_set("insert", INSERT + "+1c")
    return "break"

def selection(event):
    try:
        page.get(SEL_FIRST, SEL_LAST)
        answer = messagebox.askyesno('selection', 
             'Utiliser cette sélection pour votre entrainement?',
             icon='question')
        if answer:
            debut = page.index(SEL_FIRST)
            debut_sel.set(debut)
            affichage(page.get(SEL_FIRST, SEL_LAST), 1.0)
            status.set('selection_start')
            save(debut)
            print('save')
    except:
        pass            

root = Tk()
root.title("DactyloPy")

root.option_add('*tearOff', FALSE)
menubar = Menu(root)
root['menu'] = menubar
menu_file = Menu(menubar)
menubar.add_cascade(menu=menu_file, label='Texte')
menu_file.add_command(command=chargement, label='Choisir un texte')
menu_file.add_command(command=sup_retour, label='Suppr double ret-char')
menu_file.add_separator()
menu_file.add_command(label="Quitter", command=root.quit)

page = Text(root, width=111, height=65, wrap=WORD, bg="#9FE2FD")
page.grid(column=0, row=0, sticky=(N,W,E,S))
sb = ttk.Scrollbar(root, orient=VERTICAL, command=page.yview)
sb.grid(column=1, row=0, sticky=(N,S))
page['yscrollcommand'] = sb.set
page.mark_set("ici", INSERT)
page.tag_config('now', background='yellow')
page.tag_config('good', background='#34FF34')
page.tag_config('wrong', background='red')

pop_up = BooleanVar()
first_key = BooleanVar()
frappes = IntVar()
timing = DoubleVar()
debut_sel = StringVar()
adresse = StringVar()
status = StringVar()
ligne = IntVar()
caractere = IntVar()
pop_up.set(True)

status_bar = ttk.Frame(root, borderwidth=1, relief=SUNKEN)
status_bar.grid(column=0, row=1, sticky=(E,W))
info = ttk.Label(status_bar, text="Nombre de frappes: ")
info.grid(column=0, row=0, sticky=(W))
nb_frappe = ttk.Label(status_bar, textvariable=frappes)
nb_frappe.grid(column=1, row=0, sticky=(W))

page.bind('<Key>', check)
page.bind('<Button-1>', now)
page.bind('<BackSpace>', correction)
page.bind('<Return>', retour)
page.bind('<ButtonRelease>', selection)
page.bind('<Escape>', stop_chrono)

root.mainloop()
