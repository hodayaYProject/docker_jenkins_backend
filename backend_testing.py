import requests

def rest_post(user_id,user_name):
    res = requests.post(f'http://localhost:5000/users/{user_id}', json={"user_name" : user_name})
    if res.ok:
        return {'status': 'ok', 'user_add': user_name}
    else:
        return {'status': 'error', 'reason': 'id already exits' }


def rest_get(user_id):
    res = requests.get(f"http://127.0.0.1:5000/users/{user_id}")
    if res.ok:
        return {'status': 'ok', 'user_name': res.json()['user_name']}
    else:
        return {'status': 'error', 'reason': 'no such id'}

def rest_put(user_id,user_name):
    res = requests.put(f"http://127.0.0.1:5000/users/{user_id}",json={"user_name" : user_name})
    if res.ok:
        return {'status': 'ok', 'user_updated': res.json()['user_update']}
    else:
        return {'status': 'error', 'reason': 'no such id'}


def rest_delete(user_id):
    res = requests.delete(f"http://127.0.0.1:5000/users/{user_id}")
    if res.ok:
        return {'status': 'ok', 'user_deleted': res}
    else:
        return {'status': 'error', 'reason': 'no such id'}



print(rest_post(2,'YOAV'))
print(rest_get(863))
# print(rest_delete(552))
print(rest_put(863,'Hodaya'))
