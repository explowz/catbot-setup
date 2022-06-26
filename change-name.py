#!/usr/bin/env python3

# This script automatically changes your bots' steam profile names.
# Change nickname to whatever you with your bots' steam profile names to be.

# Make sure you install dependencies first:
# pip3 install -U steam[client]

import time

import steam.client

f = open('accounts.txt', 'r')
data = f.read()
f.close()

data = data.replace('\r\n', '\n')
accounts = data.split('\n')
accounts.remove('')

enable_extra_info = False
nickname = '[NAME HERE]'


def extra(message):
    if enable_extra_info:
        print(message)


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

    print(f'Current profile name: {client.user.name}')
    print(f'Community profile: {client.steam_id.community_url}')
    extra(f'Last logon (UTC): {client.user.last_logon}')
    extra(f'Last logoff (UTC): {client.user.last_logoff}')

    time.sleep(5)

    client.change_status(persona_state=1, player_name=nickname)

    print('Done; logging out.')
    client.logout()

    # Spacing between accounts
    print()

print('All done.')
