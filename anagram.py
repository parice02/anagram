# -*- coding:utf-8 -*-

"""
@author: Muhammed Zeba (parice02)
"""

from typing import List, Dict
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
