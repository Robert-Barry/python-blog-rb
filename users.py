# LOGIN SYSTEM
# This is a basic login system that does nothing more
# than register a user to a database and allows that
# user to log in. It verifies the user identity and
# welcomes them on the next page. It is also an exmaple
# of simple hashing and salting of passwords.
#
# USERS.PY
# Creates the datastore for a simple login system
# 
# AUTHOR: Robert Barry
# DATE CREATED: August 5, 2012
# DATE CHANGED: August 5, 2012
# WEB ADDRESS: http://rb-login-rb.appspot.com/signup
#

from google.appengine.ext import db

# the database
class Users(db.Model):
    user_name = db.StringProperty(required = True)
    password = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    email = db.StringProperty()