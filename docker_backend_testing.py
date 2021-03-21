import requests
def rest_get(user_id):
    res = requests.get(f"http://127.0.0.1:5000/users/{user_id}")
    if res.ok:
        return {'status': 'ok', 'user_name': res.json()['user_name']}
    else:
        return {'status': 'error', 'reason': 'no such id'}
print(rest_get(863))