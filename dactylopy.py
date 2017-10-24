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
    page.config(state=NORMAL)
    page.delete(1.0, END)
    page.insert(1.0, text)    
    if protected.get():
        page.config(state=DISABLED)
    page.mark_set("insert", debut)   
    page.tag_add('now', INSERT, INSERT + "+1c")
    page.see("insert")
    page.focus_force()
    first_key.set(True)
    frappes.set(0)
    erreurs.set(0)
    ligne.set(0)
    caractere.set(0)
    if pop_up.get():
        if input_mode.get():
            pass
        else:
            messagebox.showinfo('Info',
                                'Sélectionnez une partie du texte\n'
                                'ou commencez à taper\n'
                                "(Esc pour terminer l'entrainement).")
            pop_up.set(False)

def pickle_access(debut):
    with open('save.pkl', 'rb') as save_file:
        repertoire = pickle.load(save_file)
    with open('save.pkl', 'wb') as save_file:
        repertoire[pseudo.get()]['text'][adresse.get()] = debut
        pickle.dump(repertoire, save_file)

def save(debut):
    """Sauvegarde ou renvoi l'emplacement du curseur dans le texte."""    
    if status.get() == 'ouvrir':
        debut = '1.0'            
        with open('save.pkl', 'rb') as save_file:
            repertoire = pickle.load(save_file)                
            if adresse.get() in repertoire[pseudo.get()]['text']:
                debut = repertoire[pseudo.get()]['text'][adresse.get()]     
            else:                    
                repertoire[pseudo.get()]['text'][adresse.get()] = '1.0'
                with open('save.pkl', 'wb') as save_file:
                    pickle.dump(repertoire, save_file)
        return debut       
    else:
        pickle_access(debut)            
           
def chargement():
    protected.set(False)
    input_mode.set(False)
    adresse.set(filedialog.askopenfilename())    
    if adresse.get() == '':        
        pass
    else:
        try:
            debut = ''
            with open(adresse.get()) as text_brut:
                text = text_brut.read()            
            total_car = len(text)
            status.set('ouvrir')            
            debut = save(debut)        
            affichage(text)
        except:
            text = "Désolé, je ne peux pas ouvrir ce fichier :("
            protected.set(True)
            affichage(text)

# def sup_retour():
#     """Mise en page des .txt téléchagés depuis le projet Gutenberg."""
#     retour = False
#     text = page.get(1.0, END)
#     new_text = ''
#     for char in text:
#         if char == '\n':
#             if retour == True:
#                 retour = False
#             else:
#                 new_text += char
#                 retour = True
#         else:                
#             new_text += char
#     affichage(new_text,0.1)

def now(event):
    page.tag_remove('now', 1.0, END)
    page.tag_add('now', CURRENT, CURRENT + "+1c")    

def good(ici):
    page.tag_remove('now', 1.0, END)
    page.tag_add('now', ici, ici + "+1c")
    page.tag_add('good', INSERT, ici)    

def wrong(ici):
    page.tag_remove('now', 1.0, END)
    page.tag_add('now', ici, ici + "+1c")
    page.tag_add('wrong', INSERT, ici)

def chrono(start_stop):
    if input_mode.get():
        pass
    elif start_stop == 'start':
        timing.set(time.time())        
    else:
        total = time.time() - timing.get()
        print(total)
        print(total/60)
        if start_stop == 'stop':
            if status.get() == 'selection_start':
                sel_start = debut_sel.get().split('.')                
                ligne.set(int(sel_start[0]) + ligne.get())                
                caractere.set(int(sel_start[1]) + caractere.get())              
                debut = str(ligne.get()) + '.' + str(caractere.get())           
                status.set('selection_stop')
            else:
                debut = page.index(INSERT)
            status.set('fermer')
            save(debut)
            score = round(frappes.get() / total, 2)
            temps_total = [int(total // 60), int(total % 60)]
            text = ("""Félicitations!


                      {} caractères par seconde
                      {} erreurs
                      temps total = {}:{}mn"""
            ).format(score, erreurs.get(), temps_total[0], temps_total[1])
            protected.set(True)
            affichage(text)            

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
    if input_mode.get():
        pass
    elif event.char == '':        
        pass
    elif event.char == page.get(INSERT, INSERT + "+1c"):
        frappes.set(frappes.get() + 1)
        caractere.set(caractere.get() + 1)
        page.mark_set("ici", INSERT + "+1c")
        good('ici')
        page.mark_set("insert", INSERT + "+1c")        
        return "break"
    else:
        erreurs.set(erreurs.get() + 1)
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
    if input_mode.get():
        nom = page.get('4.0', END)
        answer = messagebox.askyesno('Pseudo?',
                                     'Voulez-vous:\n{}\ncomme pseudo'.format(
                                         nom),
                                     icon='question')
        if answer:
            pseudo.set(nom[:-1])
            with open('save.pkl', 'rb') as save_file:
                repertoire = pickle.load(save_file)
            with open('save.pkl', 'wb') as save_file:                
                repertoire[pseudo.get()] = {'text':{}}
                pickle.dump(repertoire, save_file)
        else:
            nouveau()        
                                     
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
            affichage(page.get(SEL_FIRST, SEL_LAST))
            status.set('selection_start')
            save(debut)            
    except:
        pass

def nouveau():
    text = 'Bienvenu,\n\nEntrez un pseudo ci-dessous:\n'
    input_mode.set(True)
    affichage(text, '6.0')

def profil_load(profil_index):    
    pseudo.set(list_pseudo[profil_index])    

preferenece = {}

root = Tk()
root.title("DactyloPy")

pop_up = BooleanVar()
protected = BooleanVar()
first_key = BooleanVar()
input_mode = BooleanVar()
frappes = IntVar()
erreurs = IntVar()
timing = DoubleVar()
debut_sel = StringVar()
adresse = StringVar()
status = StringVar()
ligne = IntVar()
caractere = IntVar()
pseudo = StringVar()
pop_up.set(True)
protected.set(False)
input_mode.set(False)
pseudo.set('Anonyme')

root.option_add('*tearOff', FALSE)
menubar = Menu(root)
root['menu'] = menubar
menu_file = Menu(menubar)
menubar.add_cascade(menu=menu_file, label='Texte')
menu_file.add_command(command=chargement, label='Choisir un texte')
#menu_file.add_command(command=sup_retour, label='Suppr double ret-char')
menu_file.add_separator()
menu_file.add_command(label="Quitter", command=root.quit)
menu_profil = Menu(menubar)
menubar.add_cascade(menu=menu_profil, label='Profil')
menu_profil.add_command(command=nouveau, label='Nouveau')
try:
    with open('save.pkl', 'rb') as save_file:
        names = pickle.load(save_file)        
except FileNotFoundError:
    with open('save.pkl', 'wb') as save_file:                
        repertoire = {pseudo.get():{'text':{}}}
        pickle.dump(repertoire, save_file)
        names = repertoire
profil_index = 0
list_pseudo = []
for key in names:
    print(key, profil_index)
    menu_profil.add_command(command=lambda: profil_load(
        profil_index - 1), label=key)
    list_pseudo.append(key)
    profil_index += 1
print(list_pseudo)
    

page = Text(root, width=85, height=50, wrap=WORD, bg="#9FE2FD",
            font=('Arial', 12))
page.grid(column=0, row=0, sticky=(N,W,E,S))
sb = ttk.Scrollbar(root, orient=VERTICAL, command=page.yview)
sb.grid(column=1, row=0, sticky=(N,S))
page['yscrollcommand'] = sb.set
page.mark_set("ici", INSERT)
page.tag_config('now', background='yellow')
page.tag_config('good', background='#34FF34')
page.tag_config('wrong', background='red')

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

text = """Bienvenu dans DactyloPy

Créez ou charger un profil ou selectionnez un texte et commencez à taper."""
affichage(text)

root.mainloop()
