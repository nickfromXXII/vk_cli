import vk_api


vk_session = vk_api.VkApi(
        login=input('Login: '),
        password=input('Password: '),
        api_version='5.53',
        app_id='5565506'
    )

try:
    vk_session.authorization()
except vk_api.AuthorizationError as error_msg:
    print(error_msg)

vk_api = vk_session.get_api()


def get_api():
    return api


def set_online(online=True):
    if online:
        vk_api.account.setOnline()
    else:
        vk_api.account.setOffline()


def get_user_info(id=None, get_fields=None):
    try:
        return vk_api.users.get(user_ids=id, fields=get_fields)
    except Exception:
        pass


def get_group_info(id=None, get_fields=None):
    return vk_api.groups.getById(group_ids=id, fields=get_fields)


def get_chat_info(id=None, get_fields=None):
    return vk_api.messages.getChat(chat_ids=id, fields=get_fields)


def get_message_info(id=0):
    return vk_api.messages.getById(message_ids=id)


def get_dialogs_receivers():
    return vk_api.execute.getReceivers()


def get_dialogs_list():
    return vk_api.messages.getDialogs(count=200, preview_length=40)


def get_dialog_history(peer=None, messages_count=20, peer_type='user'):
    if peer_type == 'group':
        peer += 2000000000
    elif peer_type == 'community':
        peer = -peer
    else:
        peer = vk_api.users.get(user_ids = peer)[0]['id']

    return vk_api.messages.getHistory(peer_id=peer, count=messages_count, rev=0)


def send_message(receiver=None, message_text='', receiver_type='user'):
    if receiver_type == 'group':
        receiver += 2000000000
    elif receiver_type == 'community':
        receiver = -receiver
    else:
        receiver = vk_api.users.get(user_ids=receiver)[0]['id']

    vk_api.messages.send(peer_id=receiver, message=message_text)

CURRENT_USER_INFO = get_user_info()
