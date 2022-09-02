#!/usr/bin/env python3

# This script automatically sets up Steam avatars, nicknames and gathers the SteamID32 for bots.
# Change make_commands to False if you with to get just the SteamID32, instead of Cathook's change playerstate command
# You do not have to "set up" a steam profile on each account for this to work, evidently.
# Simply copy your accounts.txt and bot-profile.jpg here and run: ./auto-profile.py
# Image format can be PNG, this script just expects the filename to be .jpg

# Make sure you install dependencies first:
# pip3 install -U steam[client]

import json
import time

import steam.client

f = open('accounts.txt', 'r')
data = f.read()
f.close()

data = data.replace('\r\n', '\n')
accounts = data.split('\n')
accounts.remove('')
profile = open('bot-profile.jpg', 'rb')
nickname = '[NAME HERE]'  # Enter the nickname you wish your bots to have here

enable_debugging = False
enable_extra_info = False
enable_avatarchange = True
enable_namechange = True
enable_gatherid32 = True
dump_response = False
make_commands = True


def debug(message):
    if enable_debugging:
        print(message)


def extra(message):
    if enable_extra_info:
        print(message)


if enable_gatherid32:
    open('steamid32.txt', 'w').close()  # Erase any previous contents
    id_file = open('steamid32.txt', 'a')  # Open the file as append

for index, account in enumerate(accounts):
    username, password = account.split(':')
    print(f'Logging in as user #{index + 1}/{len(accounts)} ({username})...')

    client = steam.client.SteamClient()
    eresult = client.login(username, password=password)
    status = 'OK' if eresult == 1 else 'FAIL'
    print(f'Login status: {status} ({eresult})')
    if status == 'FAIL':
        raise RuntimeError(
            'Login failed; bailing out. See https://steam.readthedocs.io/en/stable/api/steam.enums.html#steam.enums'
            '.common.EResult for the relevant error code.')

    print(f'Logged in as: {client.user.name}')
    print(f'Community profile: {client.steam_id.community_url}')
    extra(f'Last logon (UTC): {client.user.last_logon}')
    extra(f'Last logoff (UTC): {client.user.last_logoff}')

    if enable_gatherid32:
        id32 = str(client.steam_id.as_32)
        if make_commands:
            id_file.write(f'cat_pl_add_id {id32} CAT\n')
            print('Saved the SteamID32 as a Cathook change playerstate command.')
        else:
            id_file.write(f'{id32}\n')
            print('Saved the SteamID32 as raw.')

    if enable_namechange:
        time.sleep(5)  # Needed, since Steam refuses to change status if we do it too soon
        client.change_status(persona_state=1, player_name=nickname)
        print(f'Changed Steam nickname to "{nickname}"')

    if enable_avatarchange:
        print('Getting web_session...')
        session = client.get_web_session()
        debug(f'session.cookies: {session.cookies}')

        url = 'https://steamcommunity.com/actions/FileUploader'
        id64 = client.steam_id.as_64  # type int
        data = {
            'MAX_FILE_SIZE': '1048576',
            'type': 'player_avatar_image',
            'sId': f'{id64}',
            'sessionid': session.cookies.get('sessionid', domain='steamcommunity.com'),
            'doSub': '1',
        }
        post_cookies = {
            'steamLogin': session.cookies.get('steamLogin', domain='steamcommunity.com'),
            'steamLoginSecure': session.cookies.get('steamLoginSecure', domain='steamcommunity.com'),
            'sessionid': session.cookies.get('sessionid', domain='steamcommunity.com')
        }
        debug(f'post_cookies: {post_cookies}')

        print('Setting profile picture...')

        r = session.post(url=url, params={'type': 'player_avatar_image', 'sId': str(id64)}, files={'avatar': profile},
                         data=data, cookies=post_cookies)
        content = r.content.decode('ascii')
        if dump_response:
            print(f'response: {content}')
        if not content.startswith('<!DOCTYPE html'):
            response = json.loads(content)
            raise RuntimeError(f'Error setting profile: {response["message"]}')

    print('Done; logging out.')
    client.logout()

    # Seek to beginning; reuse file
    profile.seek(0)

    # Spacing between accounts
    print()

    # Only pause if we're changing avatars, and we're not at the last account, or we have less than or equal to 10
    # accounts in total
    if enable_avatarchange and (index + 1 != len(accounts) or len(accounts) <= 10):
        # For file avatars no more than 10 avatars per 5 minutes from each IP address
        time.sleep(31)

if enable_gatherid32:
    id_file.close()

profile.close()

print('All done.')
