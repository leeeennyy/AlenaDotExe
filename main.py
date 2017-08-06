import socket
import config
import re

def send_message(socket, message):
    socket.send(('PRIVMSG #' + config.CHAN + ' :' + message + '\r\n').encode())
    print('[BOT] -> ' + config.CHAN + ': ' + message + '\n')

def send_pong(socket):
    socket.send(('PONG :tmi.twitch.tv\r\n').encode())
    print('[BOT] -> Sent a pong \n')

def get_search(pattern, text):
    same = re.search(pattern, text)
    return None if same == None else same.group(0)

def commands(x):
    return {
        'commands': '!coolkids | !discord | !donate | !elo | !emotes | !girth | !social',
        'coolkids': 'Dane [twitch.tv/dhQk] | Jordan [twitch.tv/IncredFruityTV] | Rag [twitch.tv/Ragnarok1stx]',
        'discord': 'Come have some yarns with me at discord.gg/xGBFGZx',
        'donate': 'Thanks for thinking about donating',
        'elo': 'goo.gl/DUhU6j',
        'emotes': 'leeeenLove leeeenKiss',
        'girth': 'I thought the Witcher card game was GIRTH instead of GWENT',
        'social': 'Get updates on my life at twitter.com/leeeennyy'
    }.get(x, 'This ain\'t a command. Please look at !commands')

def main():
    ts = socket.socket()
    ts.connect((config.HOST, config.PORT))
    ts.send(('PASS ' + config.PASS + '\r\n').encode())
    ts.send(('NICK ' + config.NICK + '\r\n').encode())
    ts.send(('CAP REQ :twitch.tv/membership\r\n').encode())
    ts.send(('JOIN #' + config.CHAN + '\r\n').encode())

    while True:
        data = ts.recv(1024).decode()
        # Split by ':' to help us get messages easier
        # ['PING ', 'tmi.twitch.tv\r\n']
        # ['', 'leeeennyy!leeeennyy@leeeennyy.tmi.twitch.tv PRIVMSG #leeeennyy ', 'message\r\n']
        line = data.split(':')
        if not (data == ''):
            print(line)
            ping = get_search('PING', line[0])
            if not (ping == None):
                send_pong(ts)
                continue

            isMessage = get_search('(PRIVMSG)', line[1])
            if not (isMessage == None):
                username = get_search('.+?(?=!)', line[1])
                message = line[2].strip().lower()
                command = get_search('(?<=!)[^\s]+', message)

                if not (command == None):
                    send_message(ts, '@' + username + ' ' + commands(command))
                elif (message.lower() == 'hey'):
                    send_message(ts, 'Welcome to the stream @' + username + '!')

def testshit():
    ping = get_search('(?<=!)[^\s]+', '!girth\r\n'.strip())
    if (ping == None):
        print('noo')
    else: print(ping)

    print(commands('social'))

if __name__ == '__main__':
    #testshit()
    main()
