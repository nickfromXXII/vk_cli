#!/usr/bin/python3

import api
import os
import sys

commands = (
    '/refresh',
    '/back',
    '/exit'
)

dialogs = []


def clear_console():
    os.system('cls') if sys.platform == 'win32' else os.system('clear')


def app_exit():
    clear_console()
    sys.exit(0)


def make_dialogs_list():

    if len(dialogs):
        dialogs.clear()

    chats = []
    users = []
    communities = []

    for dialog in api.get_dialogs_list()['items']:
        message = dialog['message']
        if 'chat_id' in message:  # group chat
            chats.append(message['chat_id'])
        else:  # just dialog
            if message['user_id'] > 0:  # user
                users.append(message['user_id'])
            else:  # community
                communities.append(-message['user_id'])

    chats_info = api.get_chat_info(id=','.join([str(chat) for chat in chats]), get_fields='online')
    users_info = api.get_user_info(id=','.join([str(user) for user in users]), get_fields='online')
    communities_info = api.get_group_info(id=','.join([str(community) for community in communities]))

    counter = 1
    for dialog in api.get_dialogs_list()['items']:
        chat = dict.fromkeys(['id', 'name', 'type', 'members', 'last_message', 'unread'])
        message = dialog['message']
        receiver_info = ''
        if 'chat_id' in message:  # group chat
            for chat_info in chats_info:
                if message['chat_id'] == chat_info['id']:
                    chat['name'] = chat_info['title']
                    chat['id'] = chat_info['id']
                    chat['members'] = chat_info['users']
                    chat['type'] = 'group'
        else:  # just dialog
            if message['user_id'] > 0:  # user
                for user_info in users_info:
                    if message['user_id'] == user_info['id']:
                        chat['name'] = user_info['first_name'] + ' ' + user_info['last_name']
                        chat['id'] = user_info['id']
                        chat['members'] = user_info
                        chat['type'] = 'user'
            else:  # community
                for community_info in communities_info:
                    if message['user_id'] == -community_info['id']:
                        chat['name'] = community_info['name']
                        chat['id'] = community_info['id']
                        chat['members'] = community_info['id']
                        chat['type'] = 'community'

        chat['unread'] = ' (' + str(dialog['unread']) + ' new)' if 'unread' in dialog else ''
        chat['last_message'] = \
            message['body'] + ' (unread)' if message['out'] == 1 and message['read_state'] == 0 else message['body']
        dialogs.append(
            dict(
                id=counter,
                dialog_id=chat['id'],
                type=chat['type'],
                name=chat['name'],
                last_message=chat['last_message'],
                unread=chat['unread'],
                members=chat['members']
            )
        )

        counter += 1


def list_dialogs():
    make_dialogs_list()
    clear_console()

    for dialog in dialogs:
        print('[' + str(dialog['id']) + '] ' + dialog['name'] + " -> " + dialog['last_message'] + dialog['unread'])

    command = input("Enter number of dialog: ")

    if command not in commands:
        dialog_id = int(command)
        view_dialog(dialog_id=dialog_id)
    else:
        if command == '/refresh':
            clear_console()
            list_dialogs()
        elif command == '/exit':
            app_exit()


def view_group_chat(dialog=dict.fromkeys('dialog_id', 'members')):
    clear_console()
    dialog_history = api.get_dialog_history(peer=dialog['dialog_id'], peer_type='group')['items']
    for message in reversed(dialog_history):
        message_author='Me'
        for member in dialog['members']:
            if message['from_id'] == member['id']:
                message_author = member['first_name'] + ' ' + member['last_name']
                message_author += ' (online)' if member['online'] else ''
                break

        print_message = message['body'] if message['read_state'] else message['body'] + ' (unread)'
        print(message_author + ':' + '\n ' + print_message)

        if message['id'] == dialog_history[0]['id']:
            command = input("Answer: ")
            if command not in commands:
                if command:
                    api.send_message(receiver=dialog['dialog_id'], message_text=command, receiver_type='group')
                    view_group_chat(dialog)
                else:
                    list_dialogs()
            else:
                if command == '/refresh':
                    view_group_chat(dialog)
                elif command == '/back':
                    list_dialogs()
                elif command == '/exit':
                    app_exit()


def view_community_dialog(dialog=dict.fromkeys('dialog_id', 'members')):
    clear_console()
    pass


def view_private_dialog(dialog=dict.fromkeys('dialog_id', 'members')):
    clear_console()
    dialog_history = api.get_dialog_history(peer=dialog['dialog_id'], peer_type='user')['items']
    for message in reversed(dialog_history):
        message_author = dialog['members']['first_name'] if message['from_id'] == dialog['members']['id'] else 'Me'
        print_message = message['body'] if message['read_state'] else message['body'] + ' (unread)'
        print(message_author + ':' + '\n ' + print_message)
        if message['id'] == dialog_history[0]['id']:
            command = input("Answer: ")
            if command not in commands:
                if command:
                    api.send_message(receiver=dialog['dialog_id'], message_text=command, receiver_type='user')
                    view_private_dialog(dialog)
                else:
                    list_dialogs()
            else:
                if command == '/refresh':
                    view_private_dialog(dialog)
                elif command == '/back':
                    list_dialogs()
                elif command == '/exit':
                    app_exit()


def view_dialog(dialog_id):
    clear_console()
    for dialog in dialogs:
        if dialog['id'] == dialog_id:
            if dialog['type'] == 'group':
                view_group_chat(dialog=dialog)
            elif dialog['type'] == 'community':  # TODO dialogs with communities
                view_community_dialog(dialog=dialog)
            else:
                view_private_dialog(dialog=dialog)

            break


def main():
    list_dialogs()

if __name__ == '__main__':
    main()
