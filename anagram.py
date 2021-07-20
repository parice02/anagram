# -*- coding:utf-8 -*-

"""
@author: Muhammed Zeba (parice02)
"""

import sqlite3
from outils import regexp, listfetchall
from typing import List, Dict
from datetime import time
import logging

from utility import LoggerTimer

logger = logging.getLogger("loggertimer.test")


class Anagram(object):
    """ """

    def __init__(self):
        """ """
        self.connection = sqlite3.connect("ana.db")
        self.connection.create_function("regexp", 2, regexp)

    def close_connection(self):
        """ """
        self.connection.close()

    @LoggerTimer("Anagram.process() process time: ")
    def process(self, letters_count: Dict, word_length: int) -> List:
        """ """
        try:
            query = "SELECT DISTINCT mot FROM mots WHERE LENGTH(mot) = :len AND regexp(:expr, mot)"
            _once = "".join([k for k, v in letters_count.items() if v == 1])
            once = fr"(?!.*([{_once}]).*\1)"
            more = "".join(
                [f"(?!(.*{k}){{{v + 1}}})" for k, v in letters_count.items() if v > 1]
            )
            letters = "".join([k for k in letters_count.keys()])
            params = {"expr": f"^{once}{more}[{letters}]*$", "len": word_length}

            curseur = self.connection.cursor()
            curseur.execute(query, params)
            results = listfetchall(curseur)
            curseur.close()
            # print(results)
            # print(params['expr'])
            return (
                results
                if len(results) != 0
                else [
                    0,
                    _("Aucune correspondance trouvée"),
                ]
            )
        except Exception as e:
            raise e
            return [
                0,
                e.__str__(),
            ]
