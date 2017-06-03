# Create constants.py by duplicating this file, then change variables as needed

RELATIVE_PATH_TO_DB_FILE = '../puff_puff_db.sqlite'

MESSAGE_TEMPLATE = 'Hello, world!'

# ID of the conversation to send the message to. Conversation IDs can be found
# in the hangups debug log by searching for "conversation_id".
CONVERSATION_ID = ''

# Path where OAuth refresh token is saved, allowing hangups to remember your
# credentials.
REFRESH_TOKEN_PATH = '/home/<user>/.cache/hangups/refresh_token.txt'