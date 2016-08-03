import vk_requests

vk_login = input("VK login: ")
vk_password = input("VK password: ")


def get_api():
    return vk_requests.create_api(
        app_id = '5565506',
        login = vk_login,
        password = vk_password,
        scope = [
            'messages',
            'offline',
            'status',
            'friends',
            'wall'
        ],
        api_version = '5.53'
    )


def get_user_info(vk_api = get_api(), id = 0, get_fields = None):
    return vk_api.users.get(user_ids = id, fileds = get_fields)


def get_group_info(vk_api = get_api(), id = 0):
    return vk_api.groups.getById(group_id = id)


def get_message_info(vk_api = get_api(), id=0):
    return vk_api.messages.getById(message_ids=id)


def get_dialogs_list(vk_api = get_api()):
    return vk_api.messages.getDialogs(count=200, preview_length=40)


def send_message(vk_api = get_api(), receiver = None, message_text = "", receiver_type='user'):
    if receiver_type == 'group':
        receiver += 2000000000
    elif receiver_type == 'community':
        receiver = -receiver
    else:
        receiver = vk_api.users.get(user_ids = receiver)[0]

    if vk_api.messages.send(peer_id = receiver['id'], message = message_text):
        print('Your message has been successfully send.')


USER_INFO = get_user_info()


class User:
    id = 0
    first_name = ""
    last_name = ""
    deactivated = ""
    nickname = ""
    hidden = 0

    def __init__(self, fields):
        self.id = fields['id']
        self.first_name = fields['first_name']
        self.last_name = fields['last_name']
        self.deactivated = fields['deactivated']
        self.nickname = fields['nickname']
        self.hidden = fields['hidden']
