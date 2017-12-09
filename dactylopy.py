#!/usr/bin/env python3

"""
Logiciel d’entraînement à la dactylographie.
Optimisé pour les romans et le respect des caractères spéciaux.

License Libre
rod.cat@free.fr

Logo: Simon Child https://thenounproject.com/Simon%20Child/
Creative Commons
"""

import time
import datetime
import pickle
import io
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import font
from tkinter import colorchooser


def pickle_load():
    """Charge la sauvegarde et renvoi un dictionnaire"""
    try:
        with open('.save.pkl', 'rb') as save_file:
            repertoire = pickle.load(save_file)
    except FileNotFoundError:
        try:
            with open('save.pkl', 'rb') as save_file:
                repertoire = pickle.load(save_file)
        except FileNotFoundError:
            repertoire = {pseudo.get(): {'text': {}, 'score': 0}}
            pickle_write(repertoire)
    return repertoire


def pickle_write(repertoire):
    """Mise à jour de la sauvegarde"""
    with open('.save.pkl', 'wb') as save_file:
        pickle.dump(repertoire, save_file)


def affichage(text, debut='1.0', a_score=0, b_score=0, prec=0):
    """Affiche et tag le texte sélectionné"""
    page.config(state=NORMAL)
    page.delete(1.0, END)
    page.insert(1.0, text)
    if protected.get():
        if status.get() == 'result':
            page.tag_add('now', 1.0, '1.14')
            if a_score >= b_score:
                page.tag_add('good', '4.18', '4.53')
            elif b_score - a_score <= 2:
                page.tag_add('medium', '4.18', '4.53')
            else:
                page.tag_add('wrong', '4.18', '4.54')
            page.tag_add('good', '4.55', '4.65')
            if prec >= 95:
                page.tag_add('good', '6.18', '6.51')
            elif prec >= 90:
                page.tag_add('medium', '6.18', '6.51')
            else:
                page.tag_add('wrong', '6.18', '6.51')
        elif status.get() == 'accueil':
            page.tag_add('now', '8.13', '8.22')
            page.tag_add('now', '18.0', '18.9')
            page.tag_add('good', '6.6', '6.13')
        elif status.get() == 'load':
            car = len(pseudo.get())
            page.tag_add('good', '1.8', '1.{}'.format(car + 8))
            status.set('entraînement')
        elif status.get() == 'préference':
            page.tag_add('now', '2.0', '2.12')
            page.tag_add('now', '11.55', '11.57')
            page.tag_add('good', '12.23', '12.43')
            page.tag_add('wrong', '13.23', '13.43')
            page.tag_add('medium', '14.23', '14.45')
        else: pass
        page.config(state=DISABLED)
    elif status.get() == 'edit': pass
    else:
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
                starting.set(True)
                pass
            elif starting.get():
                starting.set(False)
            messagebox.showinfo('Info',
                                'Sélectionnez une partie du texte\n'
                                'ou commencez à taper\n'
                                "(Esc pour terminer l’entraînement).")
            pop_up.set(False)


def deja_ouvert(emplacement):
    """Ouvre le fichier sélectionné"""
    try:
        adresse.set(emplacement)
        protected.set(False)
        input_mode.set(False)
        debut = ''
        with io.open(emplacement, 'r', encoding='utf8') as text_brut:
            text = text_brut.read()
        status.set('ouvrir')
        debut = save(debut)
        try:
            affichage(text, debut)
        except Exception:
            affichage(text, debut[0])
    except Exception:
        text = "Désolé, je ne peux pas ouvrir ce fichier :("
        protected.set(True)
        affichage(text)


def chargement():
    """sélection d'un texte via la barre de menu"""
    adresse.set(filedialog.askopenfilename())
    if adresse.get() == '': pass
    else:
        emplacement = adresse.get()
        deja_ouvert(emplacement)


def opened_update():
    """Mise à jour du menu 'Fichiers récents'"""
    repertoire = pickle_load()
    tup_list = []
    try:
        menu_opened.delete(0, END)
    except Exception: pass
    for texte in repertoire[pseudo.get()]['text']:
        last = repertoire[pseudo.get()]['text'][texte][1], texte
        tup_list.append(last)
    tup_list.sort()
    if len(tup_list) > 3:
        tup_list = tup_list[-3:]
    tup_list.reverse()
    for emplacement in tup_list:
        menu_opened.add_command(command=lambda emplacement=emplacement:
                                deja_ouvert(emplacement[1]),
                                label=emplacement[1])


def profil_update():
    """Mise à jour du menu 'Profil'"""
    repertoire = pickle_load()
    list_pseudo = sorted([key for key in repertoire])
    try:
        menu_profil.delete(0, END)
    except Exception: pass
    menu_profil.add_command(command=nouveau, label='Nouveau')
    for nom in list_pseudo:
        menu_profil.add_command(command=lambda nom=nom: profil_load(
            list_pseudo.index(nom)), label=nom)


def profil_load(profil_index):
    """Charge le profil choisi dans la barre de menu"""
    repertoire = pickle_load()
    list_pseudo = sorted([key for key in repertoire])
    pseudo.set(list_pseudo[profil_index])
    try:
        set_dic = repertoire[pseudo.get()]['pref']
        nb_line.set(set_dic['ligne'])
        nb_col.set(set_dic['col'])
        col_bg.set(set_dic['bg'])
        col_pol.set(set_dic['pol'])
        col_now.set(set_dic['now'])
        col_good.set(set_dic['good'])
        col_wrong.set(set_dic['wrong'])
        col_med.set(set_dic['med'])
        police.set(set_dic['police'])
        pol_size.set(set_dic['psize'])
        preview()
    except Exception: pass
    opened_update()
    text = ('Bonjour {}, choisissez un texte et commencez votre entraînement'
            .format(pseudo.get()))
    status.set('load')
    protected.set(True)
    starting.set(True)
    pop_up.set(False)
    affichage(text)


def nouveau():
    """Création d'un nouveau profil"""
    text = 'Bienvenue,\n\nEntrez un pseudo ci-dessous:\n'
    input_mode.set(True)
    protected.set(False)
    pop_up.set(False)
    affichage(text, '6.0')


def save(debut):
    """Sauvegarde ou renvoi l'emplacement du curseur dans le texte."""
    repertoire = pickle_load()
    date = str(datetime.datetime.now())[:16]
    if status.get() == 'ouvrir':
        if adresse.get() in repertoire[pseudo.get()]['text']:
            debut = repertoire[pseudo.get()]['text'][adresse.get()][0]
        else:
            repertoire[pseudo.get()]['text'][adresse.get()] = ('1.0', date)
            pickle_write(repertoire)
            debut = '1.0'
        status.set('entraînement')
        return debut
    else:
        repertoire[pseudo.get()]['text'][adresse.get()] = (debut, date)
        pickle_write(repertoire)
        opened_update()


def selection(event):
    """Sélectionne une partie du texte pour l'entraînement"""
    if protected.get() or status.get() == 'edit': pass
    else:
        try:
            nb_char = len(page.get(SEL_FIRST, SEL_LAST))
            repertoire = pickle_load()
            score = repertoire[pseudo.get()]['score']
            if not score:
                score = 3
            estimation = nb_char // score
            if estimation > 90:
                estimation = int(estimation // 60)
            else:
                estimation = 1
            text = 'Utiliser cette sélection pour votre entraînement?\n'
            text += 'Nombre de caractères de la sélection = {}'.format(nb_char)
            text += '\nEnviron {} min'.format(estimation)
            answer = messagebox.askyesno('selection', text, icon='question')
            if answer:
                debut = page.index(SEL_FIRST)
                debut_sel.set(debut)
                text = page.get(SEL_FIRST, SEL_LAST)
                while True:
                    if text[-2] == '\n':
                        text = text[:-1]
                    else:
                        break
                affichage(text)
                status.set('selection_start')
                save(debut)
        except Exception: pass


def chrono(start_stop):
    """Déclenche et stoppe le chronomètre, calcul le score final"""
    if input_mode.get(): pass
    elif start_stop == 'start':
        timing.set(time.time())
    else:
        total = time.time() - timing.get()
        repertoire = pickle_load()
        best_score = repertoire[pseudo.get()]['score']
        if start_stop == 'stop':
            if status.get() == 'selection_start':
                sel_start = debut_sel.get().split('.')
                ligne.set(int(sel_start[0]) + ligne.get())
                caractere.set(int(sel_start[1]) + caractere.get())
                debut = str(ligne.get()) + '.' + str(caractere.get())
            else:
                debut = page.index(INSERT)
            status.set('fermer')
            save(debut)
            score = round(frappes.get() / total, 2)
            temps_total = [int(total // 60), int(total % 60)]
            mn, sec = temps_total[0], temps_total[1]
            precision = round(100 - (erreurs.get()/frappes.get()) * 100, 2)
            text = ("""Félicitations!


                      {} caractères par seconde        ({})
                      {} erreurs
                      précision = {}%
                      temps total = {}:{:02d}mn
                      """
                    ).format(score, best_score, erreurs.get(),
                             precision, mn, sec)
            if score > best_score:
                repertoire[pseudo.get()]['score'] = score
                pickle_write(repertoire)
            if erreurs.get() == 0:
                text += "Parfait, aucune erreur"
            else:
                text += ("Erreurs fréquentes:\n")
                sorted_collec = sorted([key for key in error_collec])
                for i in sorted_collec:
                    if len(error_collec[i]) < 2: pass
                    else:
                        car = i
                        if i == ' ':
                            car = '[esp]'
                        text += ("à la place de [{}], vous avez tapé {}\n"
                                 ).format(car, str(error_collec[i]))
                    del error_collec[i]
            status.set('result')
            protected.set(True)
            affichage(text, a_score=score, b_score=best_score, prec=precision)


def stop_chrono(event):
    """Stopper l'entraînement avec la touche échappe"""
    answer = messagebox.askyesno('Stop?',
                                 "Stopper l’entraînement?",
                                 icon='question')
    if answer:
        chrono('stop')


def now(event):
    """Tag de la position courante du curseur"""
    if protected.get(): pass
    else:
        page.tag_remove('now', 1.0, END)
        page.tag_add('now', CURRENT, CURRENT + "+1c")


def good(ici):
    """Tag des lettres correctes déjà tapées"""
    page.tag_remove('now', 1.0, END)
    page.tag_add('now', ici, ici + "+1c")
    page.tag_add('good', INSERT, ici)


def wrong(ici):
    """Tag des erreurs"""
    page.tag_remove('now', 1.0, END)
    page.tag_add('now', ici, ici + "+1c")
    page.tag_add('wrong', INSERT, ici)


def check(event):
    """Vérifie et comptabilise les frappes."""
    if first_key.get():
        chrono('start')
        first_key.set(False)
    if input_mode.get(): pass
    elif status.get() == 'edit': pass
    elif event.char == '': pass
    elif event.char == page.get(INSERT, INSERT + "+1c"):
        frappes.set(frappes.get() + 1)
        caractere.set(caractere.get() + 1)
        page.mark_set("ici", INSERT + "+1c")
        good('ici')
        page.mark_set("insert", INSERT + "+1c")
        return "break"
    else:
        erreurs.set(erreurs.get() + 1)
        missed = page.get(INSERT, INSERT + "+1c")
        page.mark_set("ici", INSERT + "+1c")
        wrong('ici')
        page.mark_set("insert", INSERT + "+1c")
        if missed in error_collec:
            error_collec[missed].append(event.char)
        else:
            error_collec[missed] = [event.char]
        return "break"


def retour(event):
    """Action de la touche Return"""
    if input_mode.get():
        nom = page.get('4.0', END)
        nom = nom[:-1]
        answer = messagebox.askyesno('Pseudo?',
                                     'Voulez-vous:\n{}\ncomme pseudo'.format(
                                         nom), icon='question')
        if answer:
            pseudo.set(nom)
            repertoire = pickle_load()
            text = '{} est déjà enregistré\n'.format(nom)
            text += 'Voulez-vous le réinitialiser?'
            if nom in repertoire:
                answer = messagebox.askyesno('Hum...', text, icon='question')
                if answer:
                    repertoire[nom] = {'text': {}, 'score': 0}
                    pickle_write(repertoire)
                    text = ('Bonjour {},\n'.format(pseudo.get()) +
                            'choisissez un texte et commencez'
                            'votre entraînement')
                    protected.set(True)
                    starting.set(True)
                    pop_up.set(True)
                    status.set('entraînement')
                    profil_update()
                    opened_update()
                    affichage(text)
                else:
                    nouveau()
            else:
                repertoire[nom] = {'text': {}, 'score': 0}
                pickle_write(repertoire)
                text = ('Bonjour {},\n'.format(pseudo.get()) +
                        'choisissez un texte et commencez'
                        'votre entraînement')
                protected.set(True)
                starting.set(True)
                pop_up.set(True)
                status.set('entraînement')
                profil_update()
                affichage(text)
        else:
            nouveau()
        return "break"
    elif status.get() == 'edit': pass
    elif page.get(INSERT, INSERT + "+1c") == '\n':
        frappes.set(frappes.get() + 1)
        ligne.set(ligne.get() + 1)
        caractere.set(0)
        pos = page.index(INSERT)
        line = int(pos.split('.')[0]) + 1
        if pos == page.index("end - 1 chars"):
            chrono('stop')
        else:
            page.mark_set("insert", '%d.%d' % (line, 0))
            page.tag_remove('now', 1.0, END)
            page.tag_add('now', INSERT, INSERT + "+1c")
            page.see("insert +5 lines")
        return "break"
    else:
        erreurs.set(erreurs.get() + 1)
        page.mark_set("ici", INSERT + "+1c")
        wrong('ici')
        page.mark_set("insert", INSERT + "+1c")
        missed = '[ret]'
        if missed in error_collec:
            error_collec[missed].append(event.char)
        else:
            error_collec[missed] = [event.char]
        return "break"


def correction(event):
    """Action de la touche BackSpace."""
    if input_mode.get(): pass
    elif status.get() == 'edit': pass
    else:
        page.mark_set("insert", "insert -1 chars")
        page.tag_remove('wrong', INSERT, INSERT + "+1c")
        page.tag_remove('now', 1.0, END)
        page.tag_add('now', INSERT, INSERT + "+1c")
        return "break"


def edit_mode():
    """Permet l'édition du texte affiché"""
    status.set('edit')
    protected.set(False)


def sup_retour():
    """Mise en page des .txt téléchargés depuis le projet Gutenberg."""
    if status.get() == 'edit':
        text = page.get(1.0, END)
        with io.open('edit_save.txt', 'w', encoding='utf8') as save_text:
            save_text.write(text)
        text = ''
        with io.open('edit_save.txt', 'r', encoding='utf8') as save_text:
            ponct = ['.', '?', '!', ':']
            for line in save_text:
                if line[0] == '\n' or line[-2] in ponct or line.isupper():
                    text += line
                else:
                    text += line[:-1] + ' '
        with io.open('edit_save.txt', 'w', encoding='utf8') as save_text:
            save_text.write(text)
        affichage(text)
    else:
        messagebox.showinfo('Info',
                            "Seulement en mode'Édition'")


def record():
    """Enregistre le texte affiché après édition"""
    text = page.get(1.0, END)
    fichier = filedialog.asksaveasfilename()
    with io.open(fichier, 'w', encoding='utf8') as save_text:
        save_text.write(text)
    status.set('entraînement')
    save(1.0)
    affichage(text)


def font_choice():
    """Choix de la police de caractères"""
    police.set(police_list.get(ACTIVE))


def coul_choice():
    """Ouvre l'interface de choix de couleurs et renvoi la sélection"""
    couleur = colorchooser.askcolor()
    return couleur[1]


def bg_coul():
    """Couleur du fond"""
    coul = coul_choice()
    if coul:
        col_bg.set(coul)


def pol_coul():
    """Couleur des caractères"""
    coul = coul_choice()
    if coul:
        col_pol.set(coul)


def now_coul():
    """couleur du tag 'now'"""
    coul = coul_choice()
    if coul:
        col_now.set(coul)


def good_coul():
    """couleur du tag 'good'"""
    coul = coul_choice()
    if coul:
        col_good.set(coul)


def wrong_coul():
    """couleur du tag 'wrong'"""
    coul = coul_choice()
    if coul:
        col_wrong.set(coul)


def med_coul():
    """couleur du tag 'medium'"""
    coul = coul_choice()
    if coul:
        col_med.set(coul)


def preview():
    """Affiche les modifications des préférences"""
    root.resizable(width=True, height=True)
    page.configure(width=nb_line.get(), height=nb_col.get(), bg=col_bg.get(),
                   font=(police.get(), pol_size.get()), fg=col_pol.get())
    page.tag_config('now', background=col_now.get())
    page.tag_config('good', background=col_good.get())
    page.tag_config('wrong', background=col_wrong.get())
    page.tag_config('medium', background=col_med.get())
    root.resizable(width=False, height=False)


def classic_preset():
    """preset de préférences 1"""
    col_bg.set("#9FE2FD")
    col_pol.set('black')
    col_now.set('yellow')
    col_good.set('#34FF34')
    col_wrong.set('red')
    col_med.set('#FF9903')
    police.set('Arial')
    pol_size.set(12)
    nb_line.set(85)
    nb_col.set(50)


def dark_preset():
    """preset de préférences 2"""
    col_bg.set('black')
    col_pol.set('#feab16')
    col_now.set('#2636ac')
    col_good.set('#61a900')
    col_wrong.set('red')
    col_med.set('#e059ff')
    police.set('Arial')
    pol_size.set(12)
    nb_line.set(85)
    nb_col.set(50)


def page_reload():
    """Redémarrage de l'application pour fermer le frame préférences"""
    boutons.grid_forget()
    preview()


def save_pref():
    """Sauvegarde les préférences dans le profil actif"""
    repertoire = pickle_load()
    repertoire[pseudo.get()]['pref'] = {'ligne': nb_line.get(),
                                        'col': nb_col.get(),
                                        'bg': col_bg.get(),
                                        'pol': col_pol.get(),
                                        'now': col_now.get(),
                                        'good': col_good.get(),
                                        'wrong': col_wrong.get(),
                                        'med': col_med.get(),
                                        'police': police.get(),
                                        'psize': pol_size.get()}
    print(repertoire)
    pickle_write(repertoire)


def pref():
    """Affiche le frame des préférences"""
    status.set('préference')
    with io.open('preference.txt', 'r', encoding='utf8') as text:
        text = text.read()
    page['width'] = 70
    boutons.grid(column=2, row=0, sticky=(N, E))
    ttk.Label(boutons, text='\nPolices de caractères\n',
              background='#C3C4C9').grid(column=0, row=0, sticky=(E, W))
    police_list = Listbox(boutons, height=10)
    police_list.grid(column=0, row=1)
    ind = 0
    for fonte in fonts:
        police_list.insert(ind, fonte)
        ind += 1
    ttk.Button(boutons, text='Choisir cette police', command=lambda:
               police.set(police_list.get(ACTIVE))).grid(
                   column=0, row=2, sticky=(E, W))
    ttk.Label(boutons, text='\nTaille de caractères\n',
              background='#C3C4C9').grid(column=0, row=3, sticky=(E, W))
    p_size = Spinbox(boutons, from_=4, to=40, state='readonly',
                     textvariable=pol_size)
    p_size.grid(column=0, row=4)
    ttk.Label(boutons, text='\nNombre de lignes\n',
              background='#C3C4C9').grid(column=0, row=5, sticky=(E, W))
    nbL = Spinbox(boutons, from_=10, to=400, state='readonly',
                  textvariable=nb_line)
    nbL.grid(column=0, row=6)
    ttk.Label(boutons, text='\nNombre de colonnes\n',
              background='#C3C4C9').grid(column=0, row=7, sticky=(E, W))
    nbC = Spinbox(boutons, from_=10, to=600, state='readonly',
                  textvariable=nb_col)
    nbC.grid(column=0, row=8)
    ttk.Label(boutons, text='\nChoix de couleurs\n',
              background='#C3C4C9').grid(column=0, row=9, sticky=(E, W))
    ttk.Button(boutons, text='Couleur de fond', command=bg_coul).grid(
               column=0, row=10, sticky=(E, W))
    ttk.Button(boutons, text='Couleur des caractères', command=pol_coul).grid(
               column=0, row=11, sticky=(E, W))
    ttk.Button(boutons, text='Couleur du curseur', command=now_coul).grid(
               column=0, row=12, sticky=(E, W))
    ttk.Button(boutons, text='Frappes correctes', command=good_coul
               ).grid(column=0, row=13, sticky=(E, W))
    ttk.Button(boutons, text='Frappes érronées', command=wrong_coul).grid(
               column=0, row=14, sticky=(E, W))
    ttk.Button(boutons, text='Résultat moyen', command=med_coul).grid(
               column=0, row=15, sticky=(E, W))
    ttk.Label(boutons, text='\nPrévisualisation\n',
              background='#C3C4C9').grid(column=0, row=16, sticky=(E, W))
    ttk.Button(boutons, text='Voyons voir', command=preview).grid(
               column=0, row=17, sticky=(E, W))
    ttk.Label(boutons, text='\nSauvegarde préferences\n',
              background='#C3C4C9').grid(column=0, row=18, sticky=(E, W))
    ttk.Button(boutons, text='Enregistrer', command=save_pref).grid(
               column=0, row=19, sticky=(E, W))
    ttk.Button(boutons, text='Quitter préference', command=page_reload).grid(
               column=0, row=20, sticky=(E, W))
    protected.set(True)
    affichage(text)


root = Tk()
root.title("DactyloPy")
try:
    root.iconbitmap('TW.ico')
except Exception:
    root.iconbitmap('@TW.xbm')
else: pass
root.option_add('*tearOff', FALSE)

fonts = list(font.families())
fonts.sort()
#preferenece = {}
error_collec = {}
starting = BooleanVar()
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
col_bg = StringVar()
col_pol = StringVar()
col_now = StringVar()
col_good = StringVar()
col_wrong = StringVar()
col_med = StringVar()
police = StringVar()
pol_size = IntVar()
nb_line = IntVar()
nb_col = IntVar()
starting.set(True)
pop_up.set(True)
protected.set(True)
input_mode.set(False)
pseudo.set('Anonyme')
dark_preset()


menubar = Menu(root)
menu_file = Menu(menubar)
menu_edit = Menu(menu_file)
menu_opened = Menu(menu_file)
menu_profil = Menu(menubar)
menu_pref = Menu(menubar)
menubar.add_cascade(menu=menu_file, label='Textes')
menu_file.add_command(command=chargement, label='Choisir un texte')
menu_file.add_cascade(menu=menu_opened, label='Récemment ouverts')
menu_file.add_cascade(menu=menu_edit, label='Édition')
menu_edit.add_command(command=edit_mode, label='Mode Édition')
menu_edit.add_command(command=sup_retour, label='Supprime les retours en trop')
menu_edit.add_command(command=record, label='Enregistrer')
menu_file.add_separator()
menu_file.add_command(label='Quitter', command=root.quit)
menubar.add_cascade(menu=menu_profil, label='Profil')
profil_update()
menubar.add_cascade(menu=menu_pref, label='Apparence')
menu_pref.add_command(command=pref, label='Préferences')
menu_pref.add_command(command=classic_preset, label='Thème classique')
menu_pref.add_command(command=dark_preset, label='Thème sombre')
root['menu'] = menubar

page = Text(root, wrap=WORD)
page.grid(column=0, row=0, sticky=(N, W, E, S))
preview()
sb = ttk.Scrollbar(root, orient=VERTICAL, command=page.yview)
sb.grid(column=1, row=0, sticky=(N, S))
page['yscrollcommand'] = sb.set
page.mark_set("ici", INSERT)
page.tag_config('now', background=col_now.get())
page.tag_config('good', background=col_good.get())
page.tag_config('wrong', background=col_wrong.get())
page.tag_config('medium', background=col_med.get())

root.resizable(width=False, height=False)

page.bind('<Key>', check)
page.bind('<Button-1>', now)
page.bind('<BackSpace>', correction)
page.bind('<Return>', retour)
page.bind('<ButtonRelease>', selection)
page.bind('<Escape>', stop_chrono)

status_bar = ttk.Frame(root, borderwidth=1, relief=SUNKEN)
status_bar.grid(column=0, row=1, sticky=(E, W), columnspan=3)
info1 = ttk.Label(status_bar, text="Nombre de frappes: ")
info1.grid(column=0, row=0, sticky=(W))
nb_frappe = ttk.Label(status_bar, textvariable=frappes)
nb_frappe.grid(column=1, row=0, sticky=(W))
info2 = ttk.Label(status_bar, text="    Profil actuel: ")
info2.grid(column=2, row=0, sticky=(W))
pseudo_actuel = ttk.Label(status_bar, textvariable=pseudo)
pseudo_actuel.grid(column=3, row=0, sticky=(W))
info3 = ttk.Label(status_bar, text="    Statut: ")
info3.grid(column=4, row=0, sticky=(W))
statut_actuel = ttk.Label(status_bar, textvariable=status)
statut_actuel.grid(column=5, row=0, sticky=(W))
info4 = ttk.Label(status_bar, text="  Police de caractères: ")
info4.grid(column=6, row=0)
police_actuelle = ttk.Label(status_bar, textvariable=police)
police_actuelle.grid(column=7, row=0)

boutons = ttk.Frame(root)

try:
    with io.open('accueil.txt', 'r', encoding='utf8') as text:
        text = text.read()
    status.set('accueil')
except Exception:
    text = """Bienvenue dans DactyloPy

    Créez, charger un profil ou sélectionnez un texte et commencez à taper."""
affichage(text)

root.mainloop()
