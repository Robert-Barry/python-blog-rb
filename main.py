#!/usr/bin/env python
#
# PYTHON BLOG
# A very basic blog application
#
# FILE: main.py
# This page is the blog's main page
#
# AUTHOR: Robert Barry
# DATE CREATED: July 24, 2012
# DATE CHANGED: July 24, 2012
# WEB ADDRESS: http://python-blog-rb.appspot.com/
import webapp2

from google.appengine.ext import db

# The HTML for the main page
front_page = """
<!doctype html>

<html>
    <head>
	<title>Python Blog</title>
    </head>

    <body>
	<h1>Python Blog</h1>

	<hr />

	%(entry)s

    </body>
</html>
"""

# HTML for each blog entry
blog_entries = """
		<div class="entry">
		    <div class="entry-title">%(title)s</div>
		    <div class="entry-date">%(date)s</div>
		    <pre class="entry-body">%(content)s</pre>
		</div>
	    <hr />
""" 

# This class creates the database
class Blog(db.Model):
    title = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)	

class MainHandler(webapp2.RequestHandler):
    def get(self):
	# access the datastore
        blog = db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC")
	each_entry = ""
	# loop through each blog entry and add to the HTML
	for entry in blog:
	    each_entry = each_entry + (blog_entries % {'title': entry.title, 'date': entry.created.strftime("%b %d, %Y"), 'content': entry.content })
	# display the finished page
	self.response.out.write(front_page % {'entry': each_entry})

app = webapp2.WSGIApplication([('/', MainHandler)],
                              debug=True)
