import random
import string
import constants

import cherrypy

import sqlite3

import os
dir = os.path.dirname(__file__)

from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader(os.path.join(dir, 'templates')))

DB_FILE_PATH = os.path.join(dir, constants.RELATIVE_PATH_TO_DB_FILE)

class Root(object):
	@cherrypy.expose
	def index(self):
		conn = sqlite3.connect(DB_FILE_PATH)
		c = conn.cursor()

		(name,) = c.execute('SELECT Name FROM Users Where IsCurrentlyPuffing = 1').fetchone()
		users = (element for tupl in c.execute('SELECT Name FROM Users').fetchall() for element in tupl)	#Flatten the tuples using science

		# Committing changes and closing the connection to the database file
		conn.commit()
		conn.close()
		return env.get_template('index.html').render(name=name, users=users)

	@cherrypy.expose
	def next(self):
		get_next_person_for_last_person()
		raise cherrypy.HTTPRedirect("/")
		return

	@cherrypy.expose
	def credit(self, user):
		conn = sqlite3.connect(DB_FILE_PATH)
		c = conn.cursor()
		c.execute('UPDATE Users SET CountPaidEarly = CountPaidEarly + 1 WHERE Name = ?', (user,))
		# Committing changes and closing the connection to the database file
		conn.commit()
		conn.close()
		raise cherrypy.HTTPRedirect("/")
		return

def get_next_person_for_last_person():
	conn = sqlite3.connect(DB_FILE_PATH)
	c = conn.cursor()

	(count,) = c.execute('SELECT COUNT(*) FROM Users').fetchone()

	(last_user_id,last_sort_index) = c.execute('SELECT id,SortIndex FROM Users Where IsCurrentlyPuffing = 1').fetchone()
	
	found = False
	next_sort_index = last_sort_index
	while(not found):
		next_sort_index = get_next_sort_index(next_sort_index, count)
		(next_user_id,next_count_paid_early) = c.execute('SELECT id,CountPaidEarly FROM Users Where SortIndex = ?', (next_sort_index,)).fetchone()
		if(next_count_paid_early == 0):
			found = True
		else:
			c.execute('UPDATE Users SET CountPaidEarly = ? WHERE id = ?', (next_count_paid_early - 1, next_user_id))

	c.execute('UPDATE Users SET IsCurrentlyPuffing = 0 WHERE id = ?', (last_user_id,))
	c.execute('UPDATE Users SET IsCurrentlyPuffing = 1 WHERE id = ?', (next_user_id,))

	# Committing changes and closing the connection to the database file
	conn.commit()
	conn.close()
	return

def get_next_sort_index(sort_index, count):
	sort_index = sort_index + 1
	if (sort_index > count):
		sort_index = 1
	return sort_index

if __name__ == '__main__':
	cherrypy.config.update(constants.CHERRYPY_CONFIG)
	cherrypy.quickstart(Root())