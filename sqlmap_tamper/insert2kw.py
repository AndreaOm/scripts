#!/usr/bin/env python

import re

from lib.core.common import randomRange
from lib.core.data import kb
from lib.core.enums import PRIORITY

__priority__ = PRIORITY.LOW # Change priority

'''
class PRIORITY:
    LOWEST = -100
    LOWER = -50
    LOW = -10
    NORMAL = 0
    HIGH = 10
    HIGHER = 50
    HIGHEST = 100
class DBMS:
    ACCESS = "Microsoft Access"
    DB2 = "IBM DB2"
    FIREBIRD = "Firebird"
    MAXDB = "SAP MaxDB"
    MSSQL = "Microsoft SQL Server"
    MYSQL = "MySQL"
    ORACLE = "Oracle"
    PGSQL = "PostgreSQL"
    SQLITE = "SQLite"
    SYBASE = "Sybase"
    HSQLDB = "HSQLDB"
'''

def tamper(payload, **kwargs):

    """

    Add any string to SQL keywords
    Change userDefine that you want to insert


    When OR in FOR or FLOOR ,will insert OR between O and R
    >>> import random
    >>> userDefine = r"/**/" 
    >>> random.seed(0)
    >>> tamper('FLOOR')
    'FLOO/**/R'


    Insert userDefine to sql keywords
    >>> import random
    >>> userDefine = r"%09" 
    >>> random.seed(0)
    >>> tamper('INSERT')
    'I%09N%09SERT'

    """

    userDefine = r"%09"  # Change userDefine that you want to insert

    kws = ["table","or"]

    retVal = payload

    if payload:
        for match in re.finditer(r"\b[A-Za-z_]+\b", payload):
            word = match.group()

            if len(word) < 2:
                continue

            if word.upper() in kb.keywords:
                _ = word[0]

                for i in xrange(1, len(word) - 1):
                    _ += "%s%s" % (userDefine if randomRange(0, 1) else "", word[i])

                _ += word[-1]

                if userDefine not in _:
                    index = randomRange(1, len(word) - 1)
                    _ = word[:index] + userDefine + word[index:]

            
                retVal = retVal.replace(word, _)

        for x in kws:
            if x in retVal:
                retVal = retVal.replace(x,x[:-1]+userDefine+x[-1:])


    return retVal
