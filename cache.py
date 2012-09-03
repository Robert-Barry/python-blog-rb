import logging
from datetime import datetime, timedelta

from google.appengine.ext import db


CACHE = {}
def top_posts(update = False):
    key = 'top'
    time_key = 'saved_time'
    time_now = datetime.utcnow()

    if not update and key in CACHE:
	posts = CACHE[key]
    else:
	logging.error("DB QUERY")
	# access the datastore
        blog = db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC")
	CACHE[time_key] = time_now

	# Prevent the running of mutiple queries
	posts = list(blog)
	CACHE[key] = posts

    return posts, int((time_now - CACHE[time_key]).total_seconds())