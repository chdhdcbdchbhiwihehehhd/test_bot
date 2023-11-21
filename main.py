import time
import requests
import re
import g4f
from g4f.Provider import (
    AItianhu,
    Aichat,
    Bard,
    Bing,
    ChatBase,
    ChatgptAi,
    OpenaiChat,
    Vercel,
    You,
    Yqcloud,
)

g4f.debug.logging = True  # Enable logging
g4f.check_version = False  # Disable automatic version checking


def change_cookies_fb(cookies: str):
    result = {}
    try:
        for i in cookies.split(';'):
            result.update({i.split('=')[0]: i.split('=')[1]})
        return result
    except(Exception,):
        for i in cookies.split('; '):
            result.update({i.split('=')[0]: i.split('=')[1]})
        return result


def chat_gpt(text):
    response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        provider=Bing,
        messages=[{"role": "user", "content": f"{text}"}],
    )
    return response


def get_messages(cookies: dict, id_messages):
    headers = {
        'authority': 'd.facebook.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/jxl,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'sec-ch-ua': '"Chromium";v="117", "Not;A=Brand";v="8"',
        'sec-ch-ua-full-version-list': '"Chromium";v="117.0.5938.157", "Not;A=Brand";v="8.0.0.0"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"15.0.0"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    }

    response = requests.get(f'https://d.facebook.com/messages/t/{id_messages}', cookies=cookies, headers=headers)
    new_user = re.findall(r'class="bx">([^"]*)</strong', response.text)
    user_new = new_user[len(new_user)-1]
    if "Duong Trung" == user_new:
        pass
    else:
        new_mess = re.findall(r'<div><span>([^"]*)</span><div', response.text)
        mess_new = new_mess[len(new_mess)-1]
        fb_dtsg = re.findall(r'name="fb_dtsg" value="([^"]*)"', response.text)[0]
        if '/chat' in str(mess_new):
            return mess_new.replace('/chat', '').strip(), fb_dtsg


def send(cookies: dict, id_messages, text, fb_dtsg):
    reply = chat_gpt(text)
    headers = {
        'authority': 'd.facebook.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/jxl,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded',
        'dnt': '1',
        'dpr': '1.25',
        'origin': 'https://d.facebook.com',
        'pragma': 'no-cache',
        'referer': 'https://d.facebook.com/messages/read/?fbid=100001206591333',
        'sec-ch-prefers-color-scheme': 'dark',
        'sec-ch-ua': '"Chromium";v="117", "Not;A=Brand";v="8"',
        'sec-ch-ua-full-version-list': '"Chromium";v="117.0.5938.157", "Not;A=Brand";v="8.0.0.0"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"15.0.0"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    }

    data = {
        'fb_dtsg': fb_dtsg,
        'body': str(reply),
        'send': 'Gửi',
        'tids': str(id_messages),
        'wwwupp': 'C3',
        'platform_xmd': '',
        'referrer': '',
        'ctype': '',
        'cver': 'legacy',
    }

    response = requests.post('https://d.facebook.com/messages/send/', cookies=cookies, headers=headers, data=data)
    print(response.status_code)


def main():
    cookie_input = input("\nNHẬP COOKIES FACEBOOK : ")
    id_messages = input("\nNHẬP ID MESSAGES FACEBOOK : ")
    cookie_re = re.sub(r"\s+", "", cookie_input, flags=re.UNICODE)
    cookies = change_cookies_fb(cookie_re)
    while True:
        time.sleep(5)
        messages = get_messages(cookies, id_messages)
        if messages is None:
            print("KO CÓ")
        else:
            send(cookies, id_messages, messages[0], messages[1])


if __name__ == '__main__':
    main()
