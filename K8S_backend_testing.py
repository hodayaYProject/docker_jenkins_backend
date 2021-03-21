import requests

f = open("k8s_url.txt", "r")
url = f.read()
def rest_get(user_id):
    res = requests.get(f"{url}/{user_id}")
    if res.ok:
        return {'status': 'ok', 'user_name': res.json()['user_name']}
    else:
        return {'status': 'error', 'reason': 'no such id'}

print(rest_get(863))
