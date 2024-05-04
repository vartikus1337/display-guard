#!/usr/bin/env python3

import imageio, os, requests, yaml
from tkinter import Tk, ttk

class App(Tk):
    def __init__(self, bot_token: str, chat_id: str | None, password: str):
        super().__init__()

        self.password = password

        # Bot

        self.bot_token = bot_token

        if chat_id == None:
            self.chat_id = self.get_chat_id(bot_token)
        else:
            self.chat_id = chat_id

        # GUI

        self.title('Protect by PashaCoder')
        self.geometry('555x555')
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_leave)
        self.bind('<Control_L>', self.on_leave)
        self.bind('<Alt_L>', self.on_leave)
        self.bind('<Return>', self.on_leave)

        self.frame = ttk.Frame(self)
        self.frame.bind('<Leave>', self.on_leave)

        self.entry = ttk.Entry(self.frame)
        self.entry.pack(anchor='center', pady=200)

        self.frame.pack(expand=True, fill='both', anchor='center')
        
    def on_leave(self, *args) -> None:
        if self.entry.get() == self.password:
            self.destroy()
        else:
            self.shot_photo_send()
            os.system("systemctl suspend")

    def shoot_photo_send(self) -> None:
        reader = imageio.get_reader('<video0>')
        frame = reader.get_next_data()
        imageio.imwrite('protect_photo.png', list(frame))
        reader.close()
        with open('protect_photo.png', 'rb') as file:
            print(file)
            r = requests.post(f'https://api.telegram.org/bot{self.bot_token}/sendPhoto',
                            data={'chat_id': self.chat_id},
                            files={"photo": file})
        os.remove('protect_photo.png')

    @classmethod
    def get_chat_id(cls, token: str) -> str:
        url = f'https://api.telegram.org/bot{token}/getUpdates' 
        res = requests.post(url).json()
        return res['result'][0]['message']['chat']['id']


def get_config() -> dict[str, str]:
    try:
        with open('config.yaml', 'r') as file: 
            config = yaml.safe_load(file)
    except FileNotFoundError:
        print('Not exist config.yml file, creating...')
        config = dict(bot_token=input('Bot token: '))
        config['chat_id'] = App.get_chat_id(config['bot_token'])
        config['password'] = input('set password: ')
        with open('config.yaml', 'w') as file:
            yaml.dump(config, file)
    return config


if __name__ == "__main__":
    config = get_config()
    app = App(config['bot_token'], config['chat_id'], config['password'])
    app.mainloop()
