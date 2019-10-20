import sys

from assistant import Assistant

assistant = Assistant()

while True:
    print('Press ENTER to start a conversation, Ctrl+C to terminate')

    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        print('\nExiting the assistant')
        break

    interactions = assistant.start_conversation()
    print(interactions)
    assistant.stop_conversation()
