#
#
# LOGIN SYSTEM
# This is a basic login system that does nothing more
# than register a user to a database and allows that
# user to log in. It verifies the user identity and
# welcomes them on the next page. It is also an exmaple
# of simple hashing and salting of passwords.
#
# HASHING.PY
# These functions are for securing data using a sha256 hash
# 
#
# AUTHOR: Robert Barry
# DATE CREATED: August 5, 2012
# DATE CHANGED: August 5, 2012
# WEB ADDRESS: http://rb-login-rb.appspot.com/signup
#
import hashlib
import random
import string

# Create a random salt for hashing data
def make_salt():
    return "".join(random.choice(string.letters) for x in xrange(5))

# Makes a hash using sha256 with an optional second input
# and an optional salt. 
def make_hash(toHash1, toHash2 = "", salt = None):
    if salt == None:    
	salt = make_salt()
    # Create the actual hashed data
    h = hashlib.sha256(toHash1 + toHash2 + salt).hexdigest()
    # Return a name value pair using the hash and the salt
    return "%s|%s" % (h, salt)

def make_3hash(toHash1, salt = None):
    if salt == None:    
	salt = make_salt()
    # Create the actual hashed data
    h = hashlib.sha256(toHash1 + salt).hexdigest()
    # Return a name value pair using the hash and the salt
    return "%s|%s|%s" % (toHash1, h, salt)

# Validates the hashed inputs by accepting the 2 inputs and
# the hash and making a new hash and testing against the original
def valid_hash(testHash1, testHash2 = "", h = ""):
    salt = h.split('|')[1]
    return h == make_hash(testHash1, testHash2, salt)

def valid_3hash(testHash1, h = ""):
    salt = h.split('|')[2]
    return h == make_3hash(testHash1, salt)
