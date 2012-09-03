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
import json
import webapp2
import logging
from cache import *
from datetime import datetime, timedelta

from google.appengine.ext import db

# The HTML for the main page
front_page = """
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

	<hr />

	%(entry)s

	<p>Queried %(age)s</p>

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

    def as_dict(self):
        time_fmt = '%c'
        d = {'subject': self.title,
	     'content': self.content,
	     'created': self.created.strftime(time_fmt),
	     'last_modified': self.last_modified.strftime(time_fmt)}
        return d
		

class MainHandler(webapp2.RequestHandler):
    def render_json(self, d):
        json_txt = json.dumps(d)
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
        self.response.out.write(json_txt)

    def get(self):	
	if self.request.url.endswith('.json'):
	    self.format = 'json'
	else:
	    self.format = 'html'

	blog, age = top_posts()
	if age == 1:
	    age = str(age) + " second ago"
	else:
	    age = str(age) + " seconds ago"
	
	if self.format == 'html':
	    each_entry = ""
	    # loop through each blog entry and add to the HTML
	    for entry in blog:
	        each_entry = each_entry + (blog_entries % {'title': entry.title, 'date': entry.created.strftime("%b %d, %Y"), 'content': entry.content})

	    # display the finished page
	    self.response.out.write(front_page % {'entry': each_entry, 'age': age})
	else:
	    return self.render_json([p.as_dict() for p in blog])

app = webapp2.WSGIApplication([('/(?:\.json)?', MainHandler)],
                              debug=True)
