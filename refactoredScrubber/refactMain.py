from pyrogram import Client, filters
from urllib.request import urlopen
from bs4 import BeautifulSoup
from config import api_id, api_hash

tgstat_url = 'https://uk.tgstat.com/ratings/channels'
is_searching = False

client = Client("client", api_id=api_id, api_hash=api_hash)

@client.on_message(filters.command(commands='start', prefixes='/'))
def start_command(client, message):
    global is_searching
    if is_searching:
        return
    client.send_message(message.from_user.id, 'Введіть назву каналу/чату для пошуку')
    is_searching = True

@client.on_message()
def searching(client, message):
    global is_searching
    if not is_searching:
        return

    tgstat_page = urlopen(tgstat_url)
    html = tgstat_page.read().decode("utf-8")
    tgstat_soup = BeautifulSoup(html, "html.parser")
    all_cards = tgstat_soup.find_all(class_="card")
    final_channels = []
    
    query = message.text.lower()
    for card in all_cards:
        channel_name = card.find(class_='font-16').text
        if query in channel_name.lower():
            full_url = card.find('a').get('href')
            part_channel_url = full_url.split('/')[-2]
            if part_channel_url[0] == '@':
                full_channel_url = f'https://t.me/{part_channel_url[1:]}'
            else:
                full_channel_url = f'https://t.me/joinchat/{part_channel_url}'
            final_channels.append([full_channel_url, channel_name])
    
    final_response = 'Список знайдених каналів:\n\n' if final_channels else 'По заданому критерію не знайдено жодного чату\n'
    
    for channel in final_channels:
        final_response += f'<a href="{channel[0]}">{channel[1]}</a>\n'
    
    final_response += '\nЩоб здійснити пошук знову, введіть команду <code>/start</code>'
    is_searching = False
    client.send_message(message.from_user.id, final_response, disable_web_page_preview=True)

client.run()
