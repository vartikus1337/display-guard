#!/usr/bin/env python3

import io, os, requests, yaml
import imageio.v2 as iio2
import imageio.v3 as iio3
from tkinter import Tk, ttk

class TelegramBot:
    def __init__(self, bot_token: str, chat_id: str) -> None:
        self.bot_token = bot_token
        self.chat_id = chat_id
        
    def shot_photo_send(self) -> None:
        frame = iio2.get_reader('<video0>').get_next_data()
        buffer = io.BytesIO()
        iio3.imwrite(buffer, frame, plugin='pillow', extension=".png") # type: ignore
        buffer.seek(0)
        requests.post(
            f'https://api.telegram.org/bot{self.bot_token}/sendPhoto',
            data={'chat_id': self.chat_id},
            files={'photo': ('image.png', buffer, 'image/png')}
        )

    @classmethod
    def get_chat_id(cls, token: str) -> str:
        res = requests.post(f'https://api.telegram.org/bot{token}/getUpdates').json()
        return res['result'][0]['message']['chat']['id']


class App(Tk):
    def __init__(self, bot: TelegramBot, password: str) -> None:
        super().__init__()

        self.bot = bot
        self.password = password

        self.title('Protect by PashaCoder')
        self.geometry('555x555')
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_leave)

        for key in ['<Control_L>', '<Alt_L>', '<Return>']:
            self.bind(key, self.on_leave)

        self.frame = ttk.Frame(self)
        self.frame.bind('<Leave>', self.on_leave)

        self.entry = ttk.Entry(self.frame)
        self.entry.pack(anchor='center', pady=200)

        self.frame.pack(expand=True, fill='both', anchor='center')
        
    def on_leave(self, *args) -> None:
        if self.entry.get() == self.password:
            self.destroy()
        else:
            self.bot.shot_photo_send()
            os.system("systemctl suspend")


def get_config() -> dict[str, str]:
    try:
        config = yaml.safe_load(open('config.yaml', 'r'))
    except FileNotFoundError:
        print('Not exist config.yml file, creating...')
        config = dict(bot_token=input('Bot token: '))
        config['chat_id'] = TelegramBot.get_chat_id(config['bot_token'])
        config['password'] = input('set password:' )
        yaml.dump(config, open('config.yaml', 'w'))
    return config


if __name__ == "__main__":
    config = get_config()
    bot = TelegramBot(config['bot_token'], config['chat_id'])
    app = App(bot, config['password'])
    app.mainloop()
