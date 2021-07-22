# -*- coding:utf-8 -*-

"""
@author: Muhammed Zeba (parice02)
"""

import sqlite3
from outils import regexp, listfetchall
from typing import List, Dict

from utility import LoggerTimer


class DBSQLite3(object):
    """ """

    def __init__(self, sqlite3_db: str = "ana.db") -> None:
        """ """
        self._connection = sqlite3.connect(sqlite3_db)
        self._connection.create_function("regexp", 2, regexp)
        self._cursor = self._connection.cursor()

    def close_connection(self):
        """ """
        self._connection.close()

    def close_cursor(self):
        """ """
        self._cursor.close()

    @LoggerTimer("DBSQLite.execute_query() process time")
    def execute_query(self, params) -> List:
        """ """
        query = "SELECT DISTINCT mot FROM mots WHERE LENGTH(mot) = :len AND regexp(:expr, mot)"
        try:
            self._cursor.execute(query, params)
            results = listfetchall(self._cursor)
            return (
                results
                if len(results) != 0
                else [
                    0,
                    _("Aucune correspondance trouvée"),
                ]
            )
        except Exception as e:
            return [
                0,
                e.__str__(),
            ]


class Anagram(object):
    """ """

    def __init__(self):
        """ """
        self._db = DBSQLite3()

    def close_connection(self):
        """ """
        self._db.close_connection()

    @LoggerTimer("Anagram.process() process time")
    def process(self, letters_count: Dict, word_length: int) -> List:
        """ """
        _once = "".join([k for k, v in letters_count.items() if v == 1])
        once = fr"(?!.*([{_once}]).*\1)"
        more = "".join(
            [f"(?!(.*{k}){{{v + 1}}})" for k, v in letters_count.items() if v > 1]
        )
        letters = "".join([k for k in letters_count.keys()])
        params = {"expr": f"^{once}{more}[{letters}]*$", "len": word_length}

        results = self._db.execute_query(params)
        # self._db.close_cursor()
        # print(results)
        return results
