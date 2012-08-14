#!/usr/bin/env python
#
#
# PYTHON BLOG
# A very basic blog application
# 
# SIGNUP.PY
# This file creates a basic registration page that stores
# the user's username, hashed password, and optional email
# in a datastore.
#
# AUTHOR: Robert Barry
# DATE CREATED: August 5, 2012
# DATE CHANGED: August 13, 2012
# WEB ADDRESS: http://python-blog-rb.appspot.com/signup
#
import webapp2
import re
from users import *
from hashing import *

from google.appengine.ext import db

# Create the regular expressions for form validation
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

# Create the form itself
form = """
<!DOCTYPE html>

<html>
  <head>
    <title>Sign Up</title>
    <style type="text/css">
      .label {text-align: right}
      .error {color: red}
    </style>

  </head>

  <body>
    <h2>Signup</h2>
    <form method="post">
      <table>
        <tr>
          <td class="label">
            Username
          </td>
          <td>
            <input type="text" name="username" value="%(v_name)s">
          </td>
          <td class="error">
          	%(name)s  
          </td>
        </tr>

        <tr>
          <td class="label">
            Password
          </td>
          <td>
            <input type="password" name="password" value="%(v_password)s">
          </td>
          <td class="error">
          	%(password)s  
          </td>
        </tr>

        <tr>
          <td class="label">
            Verify Password
          </td>
          <td>
            <input type="password" name="verify" value="%(v_verify)s">
          </td>
          <td class="error">
       	      %(verify)s  
          </td>
        </tr>

        <tr>
          <td class="label">
            Email (optional)
          </td>
          <td>
            <input type="text" name="email" value="%(v_email)s">
          </td>
          <td class="error">
              %(email)s  
          </td>
        </tr>
      </table>

      <input type="submit">
    </form>
  </body>

</html>
"""

# Dictionary used for updating the form with valid or invalid entries
validate = {'name': "", 'password': "", 'verify': "", 'email': "", 'v_name': "", 'v_password': "", 'v_verify': "", 'v_email': ""}

# Validify the name
def valid_name(name):
    return USER_RE.match(name)

# Validify the password
def valid_password(password):
    return PASSWORD_RE.match(password)

# Verify that the password matches
def verify_password(password, verify):
    if password == verify:
	return True
    return False

# Validify the email address
def verify_email(email):
    if len(email) < 1:
	return True
    return EMAIL_RE.match(email)

# Handler for the main signup page
class MainHandler(webapp2.RequestHandler):
    def get(self):
	# Set the form variables to empty strings
	validate['v_name'] = ""
	validate['v_password'] = ""
	validate['v_verify'] = ""
	validate['v_email'] = ""
	validate['name'] = ""
	# Render the form
        self.response.out.write(form % validate)

    def post(self):
	# Get the form variables that were entered
	name = self.request.get('username')
	password = self.request.get('password')
	verify = self.request.get('verify')
	email = self.request.get('email')

	# Call the validify functions to test
	# user input
	v_name = valid_name(name)
	v_password = valid_password(password)
	v_verify = verify_password(password, verify)
	v_email = verify_email(email)	

	# The following code updates the error information
	# in the form to inform the user of errors.
	if not v_name:
	    validate['name'] = "That's not a valid username"
	    validate['v_name'] = name
	else:
	    validate['name'] = ""
	    validate['v_name'] = name

	if not v_password:
	    validate['password'] = "That wasn't a valid password"
	else:
	    if not v_verify:
		validate['verify'] = "Your passwords didn't match"
		validate['password'] = ""
	    else:
		validate['verify'] = ""
		validate['v_password'] = password
		validate['v_verify'] = password
	
	if not v_email:
	    validate['email'] = "That's not a valid email."
	    validate['v_email'] = email
	else:
	    validate['email'] = ""
	    validate['v_email'] = email
	
	# Test if the username already exists
	users = db.GqlQuery("SELECT * FROM Users WHERE user_name=:1", name).get()
	
	# If the user name already exists, re-render the form with empty values
	if users:
	    validate['name'] = "That user already exists"
	    v_name = False	
	    validate['v_name'] = ""
	    validate['v_password'] = ""
	    validate['v_verify'] = ""
	    validate['v_email'] = ""

	# If all the data is valid, store the data in the database and create
	# cookies for verification in other pages
	if v_name and v_password and v_verify and v_email:
	    # Hash and salt the password to store in the database
	    x = make_hash(name, password)

	    # Create the datastore entity
	    registration = Users(user_name = name, password = x, email = email)
	    # Store the entity in the datastore
	    registration.put()

	    # Get the unique id of the user
	    user_id = registration.key().id()
	    # Hash and salt the id
	    id_hash = make_3hash(str(user_id))

	    # Create a cookie with the id, the hashed id, and the salt for the user
	    # for later user verification
	    self.response.headers.add_header('Set-Cookie', 'user-id=%s; Path=/' % id_hash)
	    self.redirect("/welcome")
	else:
	    # If the data was not valid, re-render the form with the values filled in
	    self.response.out.write(form % validate)

app = webapp2.WSGIApplication([('/signup', MainHandler)],
                              debug=True)
