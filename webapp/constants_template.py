# Create constants.py by duplicating this file, then change variables as needed

RELATIVE_PATH_TO_DB_FILE = '../puff_puff_db.sqlite'

# CherryPy configuration
CHERRYPY_CONFIG = {
	'environment': 'production',
	'log.screen': False,
	'server.socket_host': '127.0.0.1',
	'server.socket_port': 8080,
}