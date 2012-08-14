#!/usr/bin/env python
#
#
# LOGIN SYSTEM
# This is a basic login system that does nothing more
# than register a user to a database and allows that
# user to log in. It verifies the user identity and
# welcomes them on the next page. It is also an exmaple
# of simple hashing and salting of passwords.
# 
# LOGOUT.PY
# This file creates logs a user out and redirects them to
# the signup page.
#
# AUTHOR: Robert Barry
# DATE CREATED: August 6, 2012
# DATE CHANGED: August 6, 2012
# WEB ADDRESS: http://rb-login-rb.appspot.com/login
#
import webapp2

# Handler for the main signup page
class LogoutHandler(webapp2.RequestHandler):
    def get(self):
	# Delete the cookie for the user
	self.response.headers.add_header('Set-Cookie', 'user-id=; Path=/')
	# Redirect to the signup page
	self.redirect("/signup")
	    
    
app = webapp2.WSGIApplication([('/logout', LogoutHandler)],
                              debug=True)
