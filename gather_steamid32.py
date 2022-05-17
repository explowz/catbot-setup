#!/usr/bin/env python3

# This script automatically gathers all SteamID32s for your bots.
# Change make_commands to False if you'd the like SteamID32s not
# in Cathook's change player state command, but plain.

# Make sure you install dependencies first:
# pip3 install -U steam[client]

import steam.client

f = open('accounts.txt', 'r')
data = f.read()
f.close()

data = data.replace('\r\n', '\n')
accounts = data.split('\n')
accounts.remove('')

enable_extra_info = False
make_commands = True


def extra(message):
    if enable_extra_info:
        print(message)


open('steamid32.txt', 'w').close()  # Erase any previous contents

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

    id32 = str(client.steam_id.as_32)
    id_file = open('steamid32.txt', 'a')
    if make_commands:
        id_file.write(f'cat_pl_add_id {id32} CAT\n')
    else:
        id_file.write(f'{id32}\n')

    id_file.close()

    print('Done; logging out.')
    client.logout()

    # Spacing between accounts
    print()

print('All done.')
