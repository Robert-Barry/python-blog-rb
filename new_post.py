#!/usr/bin/env python
#
# PYTHON BLOG
# A very basic blog application
#
# FILE: new_post.py
# This page allows the user to enter a new blog post
#
# AUTHOR: Robert Barry
# DATE CREATED: July 24, 2012
# DATE CHANGED: July 24, 2012
# WEB ADDRESS: http://python-blog-rb.appspot.com/

import webapp2

from google.appengine.ext import db

# The HTML for the blog entry form
new_post = """
<!doctype html>

<html>
    <head>
	<title>Python Blog</title>
	<style>
	body {
    	    font-family: sans-serif; 
	    width: 800px; 
	    margin: 0 auto; 
	    padding: 10px;
	}
	error {
    	    color: red;
	}
	label {
    	    display: block; 
	    font-size: 20px;
	}
	input[type=text] {
    	    width: 400px; 
	    font-size: 20px; 
	    padding: 2px;
	}
	textarea {
    	    width: 400px; 
	    height: 200px; 
	    font-size: 17px; 
	    font-family: monospace;
	}
	input[type=submit] {
     	    font-size: 24px;
	}
	hr {
    	    margin: 20px auto;
	}
	.art + .art {
    	    margin-top: 20px;
	}
	.art-title {
    	    font-weight: bold; 
	    font-size: 20px;
	}
	.art-body {
    	    margin: 0;
	    font-size: 17px;
	}
	</style>
    </head>

    <body>
	<h1>Python Blog</h1>
	<h2>New Post</h2>

	<form method="post">
	    <label>
		<div>post title</div>
	    	    <input type="text" name="title" />
	    </label>

	    <div>blog post</div>
	    <textarea name="content"></textarea>

	    <div><input type="submit" name="submit" /></div>
	</form>

    </body>
</html>
"""

# the database
class Blog(db.Model):
    title = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
	# display the HTML
        self.response.out.write(new_post)

    def post(self):
	# Get the variables
	title = self.request.get("title")
	content = self.request.get("content")
	
	# test that the submission contains content
	if title and content:
	    # create the datastore entity
	    entry = Blog(title = title, content = content)
	    # store the post in the datastore
	    entry.put()
	    # find the entry's id and redirect to a page
	    # with the id as the path
	    x = str(entry.key().id())
	    self.redirect('/%s' % x)
	else:
	    error = "You need both a subject and content!";

	

app = webapp2.WSGIApplication([('/new_post', MainHandler)],
                              debug=True)
