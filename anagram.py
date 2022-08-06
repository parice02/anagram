# -*- coding:utf-8 -*-

"""
@author: Muhammed Zeba (parice02)
"""

from typing import List, Dict
from collections import Counter

from utility import LoggerTimer, DBSQLite3


class Anagram(object):
    """ """

    def __init__(self):
        """ """
        self._db = DBSQLite3()

    def close_connection(self):
        """ """
        self._db.close_connection()

    @LoggerTimer("Anagram.process() process time")
    def process(self, letters: str, word_length: int) -> List:
        """ """
        letters_count = self.process_input(letters)
        _once = "".join([k for k, v in letters_count.items() if v == 1])
        once = rf"(?!.*([{_once}]).*\1)"
        more = "".join(
            [f"(?!(.*{k}){{{v + 1}}})" for k, v in letters_count.items() if v > 1]
        )
        letters = "".join([k for k in letters_count.keys()])
        params = {"expr": f"^{once}{more}[{letters}]*$", "len": word_length}

        results = self._db.execute_query(params)

        return results

    def process_input(self, letters: str):
        if not isinstance(letters, str):
            raise TypeError(f"lettre doit être de type str et non '{type(letters)}'")

        return dict(Counter(str(letters).lower()).most_common())
