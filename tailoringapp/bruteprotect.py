#brute force protection implementation
#using helper function
#define a custom path for a custom timer database location

import time, sqlite3 as sql, os, sys

import threading

TIMER_DATABASE_PATH = "C:/Users/G-corp/tailorsorg/timer.db"

def protect():
    
    data = sql.connect(TIMER_DATABASE_PATH, isolation_level = "exclusive" )

    cursor = data.cursor()

    cursor.execute("update timer set counter = 0")

    data.commit()

    data.close()

def initialize():

    database = sql.connect(TIMER_DATABASE_PATH, isolation_level = "exclusive")

    cursor = database.cursor()

    STATUS = False


    try:

        data = list(cursor.execute("select * from timer"))

        if data:
            

            if data[0][0] > 9:

                STATUS = True

                timer = threading.Timer(60 * 5, protect)
                
                timer.start()

                database.close()

                return STATUS

                

            else:

                data = data[0][0] + 1

                cursor.execute("update timer set counter = %d" % data)

                database.commit()

                database.close()

        else:

            cursor.execute("insert into timer values(1)")

            database.commit()

            database.close()

    except sql.OperationalError:

        cursor.execute("create table timer (counter int)")

        cursor.execute("insert into timer values(0)")

        database.commit()

        database.close()


