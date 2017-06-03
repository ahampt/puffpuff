import constants
import asyncio
import hangups
import sqlite3
import os
dir = os.path.dirname(__file__)

DB_FILE_PATH = os.path.join(dir, constants.RELATIVE_PATH_TO_DB_FILE)

@asyncio.coroutine
def send_message(client):
    request = hangups.hangouts_pb2.SendChatMessageRequest(
        request_header=client.get_request_header(),
        event_request_header=hangups.hangouts_pb2.EventRequestHeader(
            conversation_id=hangups.hangouts_pb2.ConversationId(
                id=constants.CONVERSATION_ID
            ),
            client_generated_id=client.get_client_generated_id(),
        ),
        message_content=hangups.hangouts_pb2.MessageContent(
            segment=[hangups.ChatMessageSegment(MESSAGE).serialize()],
        ),
    )
    yield from client.send_chat_message(request)
    yield from client.disconnect()


def main():
    cookies = hangups.auth.get_auth_stdin(constants.REFRESH_TOKEN_PATH)
    client = hangups.Client(cookies)
    client.on_connect.add_observer(lambda: asyncio.async(send_message(client)))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(client.connect())


if __name__ == '__main__':
	conn = sqlite3.connect(DB_FILE_PATH)
	c = conn.cursor()

	(name,) = c.execute('SELECT Name FROM Users Where IsCurrentlyPuffing = 1').fetchone()

	# Committing changes and closing the connection to the database file
	conn.commit()
	conn.close()

	global MESSAGE
	MESSAGE = constants.MESSAGE_TEMPLATE.format(name)
	main()