# How to start?

0. `$ python3 -m pip install -r requirements.txt`

1. Установить в `config.json` поля :
    * `check_timeout` - время между автоматическими проверками хоста на доступность
    * `request_timeout` - время между опросами API телеграма на наличие новых сообщениий
    * `host_to_check` - хост, который будет проверяться на доступность
    * `proxies` (если необходимы для подключения к телеграму)  
        **примеры прокси:**
        * `{ "https": "ip:port" }`
        * `{ "https": "socks5://user:pass@ip:port/" }`
        * http://docs.python-requests.org/en/master/user/advanced/#proxies
    * `provider` - имя провайдера интернета на сенсоре (или удалить ключ со значением)

2. Создать в директории файл с названием `token.txt` (или как в конфиге) с токеном, выданным [@BotFather](https://t.me/BotFather)

3. Запустить бота с помощью команды `$ python3 ./bot.py` для проверки

4. Запустить бота в фоновый режим:  
**`$ nohup python3 ./bot.py 2>stderr_bot 1>stdout_bot &`**

5. Написать боту команду `/catch` для оформления подписки на обновления статуса хоста

# Остались вопросы?
* tg: [@anfinogenov](https://t.me/anfinogenov)
