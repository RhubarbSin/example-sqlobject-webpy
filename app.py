#!/usr/bin/env python

import string
import random

import web

from models import *

urls = (
    "/", "add",
    "/view", "view"
)

def load_sqlo(handler):
    con = connectionForURI('sqlite:mydatabase.db')
    if not web.ctx.has_key('env'):  # not using web.py
        sqlhub.processConnection = con
        return
    trans = con.transaction()
    sqlhub.threadConnection = trans
    try:
        return handler()
    except web.HTTPError:
        trans.commit(close=True)
        raise
    except:
        trans.rollback()
        trans.begin()
        raise
    finally:
        trans.commit(close=True)

app = web.application(urls, locals())
app.add_processor(load_sqlo)


class add:
    def GET(self):
        web.header('Content-type', 'text/html')
        fname = "".join(random.choice(string.letters) for i in range(4))
        lname = "".join(random.choice(string.letters) for i in range(7))
        u = User(name=fname
                ,fullname=fname + ' ' + lname
                ,password='542')
        return "added:" + web.websafe(str(u)) \
                            + "<br/>" \
                            + '<a href="/view">view all</a>'

class view:
    def GET(self):
        web.header('Content-type', 'text/plain')
        return "\n".join(map(str, User.select()))


if __name__ == "__main__":
    app.run()
