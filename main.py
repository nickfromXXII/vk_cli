#!/usr/bin/python3

import api
import time

dialogs = []
counter = 1

for dialog in api.get_dialogs_list()['items']:
    chat = dict.fromkeys(['id', 'name', 'type', 'receiver', 'last_message', 'unread'])
    message = dialog['message']
    if 'chat_id' in message: # group chat
        chat['name'] = message['title']
        receiver_info = dict(id=message['chat_id'])
        receiver_type = 'group'
    else: # just dialog
        if message['user_id'] > 0:
            receiver_info = api.get_user_info(id=message['user_id'])[0]
            chat['name'] = receiver_info['first_name'] + " " + receiver_info['last_name']
            receiver_type = 'user'
        else:
            receiver_info = api.get_group_info(id=-message['user_id'])[0]
            chat['name'] = receiver_info['name']
            receiver_type = 'community'

    chat['unread'] = ' (' + str(dialog['unread']) + ' new)' if 'unread' in dialog else ''
    chat['last_message'] = \
        message['body'] + ' (unread)' if message['out'] == 1 and message['read_state'] == 0 else message['body']
    dialogs.append(dict(id=counter, dialog_id=receiver_info['id'], type=receiver_type))

    print('[' + str(counter) + '] ' + chat['name'] + " -> " + chat['last_message'] + chat['unread'])
    #print(dialog, "\n")

    counter += 1
    time.sleep(1)

dialog_id = int(input("Enter number of dialog to view: "))

for dialog in dialogs:
    if dialog['id'] == dialog_id:
        if dialog['type'] == 'group':
            api.send_message(
                receiver=dialog['dialog_id'],
                message_text=input("Message: "),
                receiver_type='group')
        elif dialog['type'] == 'community':
            api.send_message(
                receiver=dialog['dialog_id'],
                message_text=input("Message: "),
                receiver_type='community'
            )
        else:
            api.send_message(
                receiver=dialog['dialog_id'],
                message_text=input("Message: ")
            )

        break

