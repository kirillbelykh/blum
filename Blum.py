import requests as req
import json
import time
import random
import os


def get_jwt():
    check_and_create_file(file_path)
    with open(file_path, 'r') as f:
        quary = f.read()
    data = {"query": quary}
    try:
        js = req.post(url='https://user-domain.blum.codes/api/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP', headers={
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
        }, data=data)
        jwt = json.loads(js.text)['token']['access']
        main(jwt)
    except KeyError:
        print('Неправильно указан quary, проверьте.')
        exit()

def check_and_create_file(file_path):
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            pass
        print(f"Файл '{file_path}' не найден. Создан новый файл. Пожалуйста, заполните его.")
    else:
        pass


def main(jwt):
    url_play = "https://game-domain.blum.codes/api/v1/game/play"
    url_claim = "https://game-domain.blum.codes/api/v1/game/claim"
    url_balance = "https://game-domain.blum.codes/api/v1/user/balance"
    print("Начал играть...")
    try:
        head = {
            'Authorization': 'Bearer' + jwt,
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
        }
        resp = req.get(url_balance, headers=head)
        count = json.loads(resp.text)['playPasses']
        if count != 0:
            for i in range(count):
                post_id = req.post(url_play, headers=head)
                id = json.loads(post_id.text)['gameId']
                if id == 'cannot start game':
                    print('Не смог начать играть, пауза')
                    time.sleep(random.randint(10, 15))
                else:
                    time.sleep(random.randrange(30, 48, 3))
                    points = random.randint(150, 220)
                    req.post(url_claim, headers=head, json={"gameId": id, "points": points})
                    print(str(i + 1) + ' / ' + str(count) + " игр")
                    print('Зафармил очков -', points)
                    time.sleep(random.randint(5, 10))
        else:

            print("Нету кристалов для игры :(")
            print('Закончил фарм')
            exit()
    except Exception:
        print('Обновляю jwt token')
        get_jwt()


if __name__ == '__main__':
    file_path = 'query.txt'
    get_jwt()

