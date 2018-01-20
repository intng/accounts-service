from app.postgres import logins, users
import json, uuid

def create_token(auth_token):
    auth_token = logins.check_auth_token(auth_token)
    if auth_token:
        token = str(uuid.uuid4())
        logins.create_token(auth_token[0], token)
        logins.delete_auth_token(auth_token[1])
        token = logins.check_token_by_id(auth_token[0])
        return json.dumps({'success': True, 'token': token[1]})
    else:
        return json.dumps({'success': False, 'description': 'unauthorized'})

def check_token(token):
    if logins.check_token(token):
        return json.dumps({'success': True})
    else:
        return json.dumps({'success': False})


def create_auth_token(vk_id=None, tg_id=None):
    if vk_id != None:
        user = users.find_by_vk_id(vk_id)
    elif tg_id != None:
        user = users.find_by_tg_id(tg_id)
    else:
        return json.dumps({'success': False, 'description': 'No id requested'})
    res = logins.check_auth_token_by_id(user[0])
    if res:
        return json.dumps({'success': True, 'token': res[1]})
    token = str(uuid.uuid4())
    logins.create_auth_token(user[0], token)
    res = logins.check_auth_token_by_id(user[0])
    if res:
        return json.dumps({'success': True, 'token': res[1]})