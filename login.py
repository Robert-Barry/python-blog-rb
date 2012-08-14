#!/usr/bin/env python
#
#
# PYTHON BLOG
# A very basic blog application

# LOGIN.PY
# This file creates a basic login page where a user
# enters a username and email and is redirected to 
# a welcome page upon successful login.
#
# AUTHOR: Robert Barry
# DATE CREATED: August 6, 2012
# DATE CHANGED: August 13, 2012
# WEB ADDRESS: http://python-blog-rb.appspot.com/login
#
import webapp2

from users import *
from hashing import *

from google.appengine.ext import db


# Create the form itself
form = """
<!DOCTYPE html>

<html>
  <head>
    <title>Login</title>
    <style type="text/css">
      .label {text-align: right}
      .error {color: red; width = 10px;}
    </style>

  </head>

  <body>
    <h2>Login</h2>
    <form method="post">
      <table>
        <tr>
          <td class="label">
            Username
          </td>
          <td>
            <input type="text" name="username" value="">
          </td>
        </tr>

        <tr>
          <td class="label">
            Password
          </td>
          <td>
            <input type="password" name="password">
          </td>
        </tr>
        <tr>
          <td class="error" colspan="2">
              %(error)s  
          </td>
        </tr>
      </table>

      <input type="submit">
    </form>
  </body>

</html>
"""

error = {'error': ""}

# Handler for the main signup page
class LoginHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(form % error)

    def post(self):
	# Get the form variables that were entered
	name = self.request.get('username')
	password = self.request.get('password')
	
	# Test if the username already exists
	users = db.GqlQuery("SELECT * FROM Users WHERE user_name=:1", name).get()

	if not users or not valid_hash(name, password, users.password):
	    error['error'] = "The username and/or password is not valid."
	    self.response.out.write(form % error) 
	else:
	    # Get the unique id of the user
	    user_id = users.key().id()
	    # Hash and salt the id
	    id_hash = make_3hash(str(user_id))

	    # Create a cookie with the username and a cookie for the hashed id
	    # for later user verification
	    self.response.headers.add_header('Set-Cookie', 'user-id=%s' % id_hash)
	    self.redirect("/welcome")
	    
    
app = webapp2.WSGIApplication([('/login', LoginHandler)],
                              debug=True)
