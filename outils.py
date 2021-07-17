# -*- coding:utf-8 -*-
'''
Created on 2 avr. 2018

@author: parice02
'''

from typing import List
from re import compile, I
from sqlite3 import Cursor


def regexp(motif: str, item: str) -> bool:
    """retourne True si le motif regex a été satisfait dans l'item 
       False sinon 
    """
    pattern = compile(motif, I)
    return pattern.search(item) is not None


def listfetchall(cursor: Cursor) -> List:
    "Return all rows from a cursor as a list"
    return [row[0] for row in cursor.fetchall()]
