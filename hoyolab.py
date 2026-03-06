import requests
from utils import load_config

config = load_config()


def check_dailies_status():
    cookies = {
        'ltuid_v2': config['hoyolab']['ltuid'],
        'ltoken_v2': config['hoyolab']['ltoken'],
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Origin': 'https://act.hoyolab.com',
        'Pragma': 'no-cache',
        'Referer': 'https://act.hoyolab.com/',
        'Sec-Fetch-Mode': 'cors',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
}

    params = {
        'server': config['hoyolab']['server'],
        'role_id': config['hoyolab']['user_id'],
    }

    response = requests.get(
        'https://sg-public-api.hoyolab.com/event/game_record_zzz/api/zzz/note',
        params=params,
        cookies=cookies,
        headers=headers,
    )
    
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        return False
    
    tasks =response.json()['data']['vitality']
    if tasks['max'] == tasks['current']:
        return True
    return False