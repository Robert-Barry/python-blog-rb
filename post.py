#!/usr/bin/env python
#
# PYTHON BLOG
# A very basic blog application
#
# FILE: post.py
# This page displays a single blog entry
#
# AUTHOR: Robert Barry
# DATE CREATED: July 24, 2012
# DATE CHANGED: July 24, 2012
# WEB ADDRESS: http://python-blog-rb.appspot.com/
import webapp2
import json

from google.appengine.ext import db

# The HTML for the indiviual post page
post = """
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
	
	%(entry)s

    </body>
</html>
"""

# HTML for the post entry
entry = """
		<div class="entry">
		    <div class="entry-title">%(title)s</div>
		    <div class="entry-date">%(date)s</div>
		    <pre class="entry-body">%(content)s</pre>
		</div>
	    <hr />
""" 

# The database
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

    def get(self, post_id):
	if self.request.url.endswith('.json'):
	    self.format = 'json'
	else:
	    self.format = 'html'

	# retrieve the individual entity using the datastore key
	key = db.Key.from_path('Blog', int(post_id))
	new_post = db.get(key)

	if not new_post:
	    self.error(404)
	    return

	if self.format == 'html':
	    # create the post for display
	    new_entry = (entry % {'title': new_post.title, 'date': new_post.created.strftime("%b %d, %Y"), 'content': new_post.content})
	    # display the page
            self.response.out.write(post % {'entry':new_entry})
	else:
	    self.render_json(new_post.as_dict())

app = webapp2.WSGIApplication([('/([0-9]+)(?:\.json)?', MainHandler)],
                              debug=True)
