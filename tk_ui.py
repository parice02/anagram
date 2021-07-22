# -*- coding:utf-8 -*-

"""
@author: Muhammed Zeba (parice02)
"""

from pathlib import Path
import tkinter
import gettext
import json
from tkinter import font, messagebox
from typing import List
from collections import Counter

from anagram import Anagram
from utility import LoggerTimer

LANG = {"en": "English", "fr": "Français"}
HEIGHT, WIDTH = 500, 400
CONFIG_FILE = "config/config.json"


class AnagramUI(object):
    """ """

    def __init__(self):
        """ """
        self.config = {}
        self._letters_dict = {}
        self._word_length = 0
        self._y, self._x = 17, 0

        self._anagram = Anagram()

        self.check_config()
        self.load_language()

        self._window = tkinter.Tk()
        self._window.option_add("*tearOff", tkinter.FALSE)
        self._window.resizable(False, False)
        self._window.title(_("Anagramme"))
        self._window.wm_title(_("Anagramme"))
        self._window.minsize(HEIGHT, WIDTH)
        self._window.protocol("WM_DELETE_WINDOW", self._window.destroy)
        self._window.iconphoto(
            True, tkinter.PhotoImage(name="icon", file="./favicon.png")
        )

        self.selected_lang = tkinter.StringVar()
        self.highlightFont = font.Font(
            family="Times", name="appHighlightFont", size=15, weight="bold"
        )
        self.textFont = font.Font(family="Times", name="textFont", size=10)

        self._menubar = tkinter.Menu(self._window)
        self._window["menu"] = self._menubar
        self._menuedit = tkinter.Menu(self._menubar)
        self._menuquit = tkinter.Menu(self._menubar)
        self._menubar.add_cascade(menu=self._menuedit, label=_("Édition"))
        self._menubar.add_separator()
        self._menubar.add_command(command=self.exit, label=_("Quitter"))

        self._menulang = tkinter.Menu(self._menuedit)
        for k, l in LANG.items():
            self._menulang.add_radiobutton(
                label=l,
                variable=self.selected_lang,
                value=k,
                command=self.change_language,
                state=tkinter.DISABLED
                if self.config["language"]["selected"] == k
                else tkinter.ACTIVE,
            )
        self._menuedit.add_cascade(label=_("Langue"), menu=self._menulang)
        self._menuedit.add_separator()
        self._menuedit.add_command(label=_("À propos de"), command=self._information)
        self._menuedit.add_command(label=_("Aide"), command=None)

        self._frame0 = tkinter.Frame(
            self._window, width=WIDTH, height=100, bg="lightblue"
        )
        self._frame0.pack(side=tkinter.TOP, expand=True, fill=tkinter.BOTH)

        tkinter.Label(
            self._frame0,
            text=_("Entrer les lettres et le nombre de lettres souhaités"),
            bg="lightblue",
            font=self.highlightFont,
        ).grid(row=0, column=0, columnspan=4, pady=10)
        tkinter.Label(self._frame0, text=_("Lettres: "), bg="lightblue").grid(
            row=1, column=0, padx=10
        )
        self._champText = tkinter.Entry(self._frame0, width=30)
        self._champText.focus_set()
        self._champText.grid(row=1, column=1, padx=10)

        tkinter.Label(
            self._frame0, text=_("Nombre de lettres: "), bg="lightblue"
        ).grid(row=1, column=2, padx=10)
        self._nombre = tkinter.Entry(self._frame0, width=8)
        self._nombre.grid(row=1, column=3, padx=10)

        self._bouton = tkinter.Button(
            self._frame0, text=_("OK"), command=self.search, width=5
        )
        self._bouton.grid(row=1, column=4)

        self._label = tkinter.Label(self._frame0, fg="red", bg="lightblue")
        self._label.grid(row=2, columnspan=5, pady=5)

        self._frame = tkinter.Frame(
            self._window,
            width=WIDTH,
            height=400,
        )
        self._frame.pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=True)

        self._caneva = tkinter.Canvas(
            self._frame, width=WIDTH, height=400, bg="white", scrollregion=(0, 0, 0, 0)
        )

        self._scrollV = tkinter.Scrollbar(
            self._frame, command=self._caneva.yview, orient=tkinter.VERTICAL
        )
        self._scrollV.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        self._scrollH = tkinter.Scrollbar(
            self._frame, command=self._caneva.xview, orient=tkinter.HORIZONTAL
        )
        self._scrollH.pack(side=tkinter.BOTTOM, fill=tkinter.X)

        self._caneva.config(
            xscrollcommand=self._scrollH.set,
            yscrollcommand=self._scrollV.set,
            state=tkinter.NORMAL,
        )

        self._scrollH["command"] = self._caneva.xview
        self._scrollV["command"] = self._caneva.yview

        self._caneva.pack(fill=tkinter.BOTH, side=tkinter.LEFT, expand=True)

        self._champText.bind("<Tab>", self.check_input)
        self._nombre.bind("<Return>", self.search)
        self._bouton.bind("<Return>", self.search)
        self._champText.bind("<Return>", self._nombre.focus_set())
        self._window.bind_all("<Cancel>", self.exit)

        self._window.grid_columnconfigure(0, weight=1)
        self._window.grid_rowconfigure(0, weight=1)

        self._window.mainloop()

    def change_language(self):
        if self.selected_lang.get() != self.config["language"]["selected"]:
            self.config["language"]["selected"] = self.selected_lang.get()
            with open(file=CONFIG_FILE, mode="w", encoding="utf8") as file:
                json.dump(self.config, file)
            self.restart_message()

    def check_config(self):
        config_file = Path(CONFIG_FILE)
        if config_file.exists() and config_file.is_file():
            with open(file=CONFIG_FILE, mode="r", encoding="utf8") as file:
                self.config = json.load(file)
        else:
            self.config = {"language": {"default": "fr", "selected": ""}}
            config_file.parent.mkdir()
            config_file.touch()
            with open(file=CONFIG_FILE, mode="w", encoding="utf8") as file:
                json.dump(self.config, file)

    def load_language(self):
        """ """
        lang = gettext.translation(
            "anagramUI",
            localedir="locales",
            languages=[
                self.config["language"]["selected"]
                or self.config["language"]["default"]
            ],
        )
        lang.install()

    def exit(self, event=None):
        """
        Exit from the program
        """
        self._anagram.close_connection()
        self._window.quit()

    @LoggerTimer("AnagramUI.search() process time")
    def search(self, event=None):
        """
        Checks the input and launches search in the database.
        """
        self.clear_content()
        try:
            self._word_length = int(self._nombre.get())
            if self._word_length > 0:
                if self.check_input(event):
                    if self._word_length > len(self._champText.get()):
                        self._label.configure(
                            text=_(
                                "Le nombre doit être au plus égal au nombre de lettres."
                            )
                        )
                    else:
                        self._letters_dict = dict(
                            Counter(str(self._champText.get()).lower()).most_common()
                        )
                        liste = self._anagram.process(
                            self._letters_dict, self._word_length
                        )
                        if type(liste[0]) == int and liste[0] == 0:
                            self._label.configure(text=liste[1], fg="blue")
                        else:
                            self.display_content(liste)
            else:
                self._label.configure(
                    text=_("Veuillez saisir un entier positif svp!!")
                )
        except Exception as e:
            self._label.configure(text=e.__str__())
            # raise e

    def clear_content(self) -> None:
        """
        Clear the canvas (the white)
        """
        self._caneva.delete(tkinter.ALL)
        self._label.configure(text="")
        self._y = 17

    def check_vowel(self) -> bool:
        """
        Check if there is a vowel in the input word.
        """
        vowels = "aeyuioéèàêëïî"
        word = str(self._champText.get()).lower()
        for v in vowels:
            if v in word:
                return True
        return False

    def check_letter(self) -> bool:
        """
        Check if the input only contain letters (no numbers, ponctuation, ....).
        """
        symboles = """1234567890&"'(-_)=}]@^\`|[{#~²,?.;/:§!%*µ£$¨^ """
        word = str(self._champText.get()).lower()
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
        if len(self._champText.get()) == 0:
            # self._champText.configure(command = self._champText.focus_set)
            self._label.configure(text=_("Le champs de lettres est vide."))
            return False
        else:
            if self.check_vowel() and not self.check_letter():
                return True
            else:
                self._label.configure(
                    text=_(
                        "Absence de voyelle ou présence de caractère non alphabétique."
                    )
                )
                return False

    def compute_column_count(self, word_count: int):
        """ """
        if word_count <= 20:
            return 1
        elif (word_count >= 21) and (word_count < 100):
            return 5
        else:
            return 10

    def display_content(self, liste: List):
        """
        Display the result (list of words).
        """
        i, self._x = 0, 15
        word_length, word_count = int(self._nombre.get()), len(liste)
        column_count = self.compute_column_count(word_count)
        space_between_words = 100

        division = (
            word_count // column_count
            if word_count % column_count == 0
            else word_count // column_count + 1
        )
        text = _(f"{word_count} mot(s) ont été trouvé.")

        self._label.configure(text=text, justify=tkinter.CENTER, fg="black")
        self.config_scroll(
            ligne=division * 20.5, colonne=column_count * word_length * 15
        )

        # self.config_scroll(
        #     ligne=(word_length + space_between_words) * column_count,
        #     colonne=20 * division,
        # )

        for mot in liste:
            i += 1
            self._caneva.create_text(
                self._x,
                self._y,
                text=mot.upper(),
                justify=tkinter.LEFT,
                fill="black",
                activefill="lightblue",
                anchor=tkinter.W,
                font=self.textFont,
            )
            self._y += 20
            if i == division:
                i = 0
                self._x += space_between_words
                self._y = 17

    def _information(self):
        """
        Display about info.
        """
        about = (
            _("Auteur: Muhammed Zeba"),
            _("Email: parice02@hotmail.com"),
            _("Licence: MIT"),
            _("Version: 0.0.2"),
        )
        messagebox.showinfo(
            message=_("À propos"), title=_("À propos"), detail="\n".join(about)
        )

    def restart_message(self):
        """ """
        message = _(
            "Le changement de langue ne sera effectif qu'après un redémarrage de l'application."
        )
        messagebox.showwarning(message=message, title=_("Redémarrage"), icon="warning")
        self.exit()

    def config_scroll(self, ligne=0, colonne=0):
        """
        Configure the scrollbar
        """
        self._caneva.config(scrollregion=(0, 0, colonne, ligne))


if __name__ == "__main__":
    a = AnagramUI()
