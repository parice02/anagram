# -*- coding:utf-8 -*-

'''
@author: Muhammed Zeba (parice02)
'''

from pathlib import Path
import sqlite3
import tkinter
import gettext
import json
from tkinter import font, messagebox
from typing import List
from collections import Counter

from anagram import Anagram

LANG = {'en': 'English', 'fr': 'Français'}
HEIGHT, WIDTH = 500, 400
CONFIG_FILE = 'config/config.json'


class AnagramUI (object):
    """
    """

    def __init__(self):
        """
        """
        self.config = {}
        self.__letters_dict = {}
        self.__word_length = 0
        self.__y, self.__x = 17, 0

        self.__anagram = Anagram()

        self.check_config()
        self.load_language()

        self.__window = tkinter.Tk()
        # self.__window.tk.call('tk', 'windowingsystem')
        self.__window.option_add('*tearOff', tkinter.FALSE)
        self.__window.resizable(False, False)
        self.__window.title(_("Anagramme"))
        self.__window.wm_title(_("Anagramme"))
        self.__window.minsize(HEIGHT, WIDTH)
        self.__window.protocol('WM_DELETE_WINDOW', self.__window.destroy)
        self.__window.iconphoto(True, tkinter.PhotoImage(
            name="icon", file='./favicon.png'))

        self.selected_lang = tkinter.StringVar()

        self.highlightFont = font.Font(
            family='Times', name='appHighlightFont', size=15, weight='bold')

        self.textFont = font.Font(
            family='Times', name='textFont', size=12)

        self.__menubar = tkinter.Menu(self.__window)
        self.__window['menu'] = self.__menubar
        self.__menuedit = tkinter.Menu(self.__menubar)
        self.__menuquit = tkinter.Menu(self.__menubar)
        self.__menubar.add_cascade(menu=self.__menuedit, label=_('Édition'))
        self.__menubar.add_separator()
        self.__menubar.add_command(command=self.exit, label=_('Quitter'))

        self.__menulang = tkinter.Menu(self.__menuedit)
        for k, l in LANG.items():
            self.__menulang.add_radiobutton(
                label=l, variable=self.selected_lang, value=k, command=self.change_language, state=tkinter.DISABLED if self.config['language']['selected'] == k else tkinter.ACTIVE)
        self.__menuedit.add_cascade(
            label=_('Langue'), menu=self.__menulang)
        self.__menuedit.add_separator()
        self.__menuedit.add_command(
            label=_('À propos de'), command=self.__information)
        self.__menuedit.add_command(label=_('Aide'), command=None)

        self.__frame0 = tkinter.Frame(
            self.__window, width=WIDTH, height=100, bg='lightblue')
        self.__frame0.pack(side=tkinter.TOP, expand=True, fill=tkinter.BOTH)

        tkinter.Label(self.__frame0, text=_("Entrer les lettres et le nombre de lettres souhaités"),
                      bg='lightblue', font=self.highlightFont).grid(row=0, column=0, columnspan=4, pady=10)
        tkinter.Label(self.__frame0, text=_("Lettres: "),
                      bg='lightblue').grid(row=1, column=0, padx=10)
        self.__champText = tkinter.Entry(self.__frame0, width=30)
        self.__champText.focus_set()
        self.__champText.grid(row=1, column=1, padx=10)

        tkinter.Label(self.__frame0, text=_("Nombre de lettres: "),
                      bg='lightblue').grid(row=1, column=2, padx=10)
        self.__nombre = tkinter.Entry(self.__frame0, width=8)
        self.__nombre.grid(row=1, column=3, padx=10)

        self.__bouton = tkinter.Button(
            self.__frame0, text=_('OK'), command=self.search, width=5)
        self.__bouton.grid(row=1, column=4)

        self.__label = tkinter.Label(self.__frame0, fg='red', bg='lightblue')
        self.__label.grid(row=2, columnspan=5, pady=5)

        self.__frame = tkinter.Frame(self.__window, width=WIDTH, height=400,)
        self.__frame.pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=True)

        self.__caneva = tkinter.Canvas(self.__frame, width=WIDTH, height=400, bg='white',
                                       scrollregion=(0, 0, 0, 0))

        self.__scrolV = tkinter.Scrollbar(
            self.__frame, command=self.__caneva.yview, orient=tkinter.VERTICAL)
        self.__scrolV.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        self.__scrolH = tkinter.Scrollbar(
            self.__frame, command=self.__caneva.xview, orient=tkinter.HORIZONTAL)
        self.__scrolH.pack(side=tkinter.BOTTOM, fill=tkinter.X)

        self.__caneva.config(xscrollcommand=self.__scrolH.set,
                             yscrollcommand=self.__scrolV.set, state=tkinter.NORMAL)

        self.__caneva.pack(fill=tkinter.BOTH, side=tkinter.LEFT, expand=True)

        self.__champText.bind('<Tab>', self.check_input)
        self.__nombre.bind('<Return>', self.search)
        self.__bouton.bind('<Return>', self.search)
        self.__champText.bind('<Return>', self.__nombre.focus_set())
        self.__window.bind_all('<Cancel>', self.exit)

        self.__window.grid_columnconfigure(0, weight=1)
        self.__window.grid_rowconfigure(0, weight=1)

        self.__window.mainloop()

    def change_language(self):
        if self.selected_lang.get() != self.config['language']['selected']:
            self.config['language']['selected'] = self.selected_lang.get()
            with open(file=CONFIG_FILE, mode='w', encoding='utf8') as file:
                json.dump(self.config, file)
            self.restart_message()

    def check_config(self):
        config_file = Path(CONFIG_FILE)
        if config_file.exists() and config_file.is_file():
            with open(file=CONFIG_FILE, mode='r', encoding='utf8') as file:
                self.config = json.load(file)
        else:
            self.config = {"language": {"default": 'fr', "selected": ""}}
            config_file.parent.mkdir()
            config_file.touch()
            with open(file=CONFIG_FILE, mode='w', encoding='utf8') as file:
                json.dump(self.config, file)

    def load_language(self):
        """
        """
        if self.config['language']['selected']:
            lang = gettext.translation(
                'anagramUI', localedir='locales',
                languages=[self.config['language']['selected']], fallback=True)
            lang.install()
        else:
            lang = gettext.translation(
                'anagramUI', localedir='locales',
                languages=[self.config['language']['default']], fallback=True)
            lang.install()

    def exit(self, event=None):
        """
        Exit from the program
        """
        self.__anagram.close_connection()
        self.__window.quit()

    def search(self, event=None):
        """
        Checks the input and launches search in the database.
        """
        self.clear_content()
        try:
            self.__word_length = int(self.__nombre.get())
            if self.__word_length > 0:
                if self.check_input(event):
                    if (self.__word_length > len(self.__champText.get())):
                        self.__label.configure(
                            text=_("Le nombre doit être au plus égal au nombre de lettres."))
                    else:
                        self.__letters_dict = dict(Counter(
                            str(self.__champText.get()).lower()).most_common())
                        liste = self.__anagram.process(
                            self.__letters_dict, self.__word_length)
                        if type(liste[0]) == int and liste[0] == 0:
                            self.__label.configure(text=liste[1], fg='blue')
                        else:
                            self.display_content(liste)
            else:
                self.__label.configure(
                    text=_('Veuillez saisir un entier positif svp!!'))
        except Exception as e:
            self.__label.configure(text=e.__str__())
            raise e

    def clear_content(self) -> None:
        """
        Clear the canvas (the white)
        """
        self.__caneva.delete(tkinter.ALL)
        self.__label.configure(text='')
        self.__y = 17

    def check_vowel(self) -> bool:
        """
        Check if there is a vowel in the input word.
        """
        vowels = 'aeyuioéèàêëïî'
        word = str(self.__champText.get()).lower()
        for v in vowels:
            if v in word:
                return True
        return False

    def check_letter(self) -> bool:
        """
        Check if the input only contain letters (no numbers, ponctuation, ....).
        """
        symboles = """1234567890&"'(-_)=}]@^\`|[{#~²,?.;/:§!%*µ£$¨^ """
        word = str(self.__champText.get()).lower()
        for v in symboles:
            if v in word:
                print(v)
                return True
        return False

    def check_input(self, event: tkinter.Event) -> bool:
        """
        Check if the input is not empty and  call check_vowel and check_letter methods.
        """
        self.clear_content()
        if len(self.__champText.get()) == 0:
            # self.__champText.configure(command = self.__champText.focus_set)
            self.__label.configure(
                text=_("Le champs de lettres est vide."))
            return False
        else:
            if self.check_vowel() and not self.check_letter():
                return True
            else:
                self.__label.configure(
                    text=_("Absence de voyelle ou présence de caractère non alphabétique."))
                return False

    def display_content(self, liste: List):
        """
        Display the result (list of words).
        """
        i, self.__x = 0, 15
        if len(liste) <= 20:
            column_count = 1
        elif (len(liste) >= 21) and (len(liste) < 100):
            column_count = 5
        else:
            column_count = 10

        division = len(liste) // column_count

        if (len(liste)) == 1:
            text = _("1 mot a été trouvé")
        else:
            text = _(f"{len(liste)} mots ont été trouvé")

        self.__label.configure(
            text=text, justify=tkinter.CENTER, fg="black")
        self.config_scroll(ligne=division*20.5,
                           colonne=column_count*len(liste[0])*15)

        for mot in liste:
            i += 1
            self.__caneva.create_text(
                self.__x,
                self.__y, text=mot.upper(),
                justify=tkinter.LEFT,
                fill='black',
                activefill='lightblue',
                anchor=tkinter.W,
                font=self.textFont)
            self.__y += 20
            if (i == division):
                i = 0
                self.__x += len(mot) * 10 + 10
                self.__y = 17

    def __information(self):
        """
        Display about info.
        """
        about = (_("Auteur: Muhammed Zeba"),
                 _("Email: parice02@hotmail.com"), _("Licence: Compatible MIT"), _("Version: 0.0.2"))
        messagebox.showinfo(message=_('À propos'),
                            title=_('À propos'), detail="\n".join(about))

    def restart_message(self):
        """
        """
        message = _(
            "Le changement de langue ne sera effectif qu'après un redémarrage de l'application.")
        messagebox.showwarning(message=message, title=_(
            "Redémarrage"), icon='warning')
        self.exit()

    def config_scroll(self, ligne=0, colonne=0):
        """
        Configure the scrollbar
        """
        self.__caneva.config(scrollregion=(0, 0, colonne, ligne))


if __name__ == '__main__':
    a = AnagramUI()
