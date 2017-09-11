#!/usr/bin/env python

import re

from lib.core.common import randomRange
from lib.core.data import kb
from lib.core.enums import PRIORITY

__priority__ = PRIORITY.LOW



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

            if "OR" in retVal:
                retVal = retVal.replace("OR","O" + userDefine + "R")

            if "or" in retVal:
                retVal = retVal.replace("or","o" + userDefine + "r")


    return retVal
