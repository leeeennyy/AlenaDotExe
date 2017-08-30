import socket
import re
import urllib.request
import config

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
        'commands': '!coolkids | !discord | !elo | !girth | !overkill | !social',
        'coolkids': 'Dane [twitch.tv/dhQk] | Jordan [twitch.tv/IncredFruityTV] | Leon [twitch.tv/LeoniLive] | Mitchell [twitch.tv/SenOokami] | MK [twitch.tv/Zexy_DemoN] | Rag [twitch.tv/Ragnarok1stx] | Sam [twitch.tv/Amorisaiya] | Sav [twitch.tv/Amorisaiya]',
        'discord': 'Come have some yarns with me at discord.gg/xGBFGZx',
        'elo': 'goo.gl/DUhU6j',
        #'emotes': 'leeeenLove leeeenKiss',
        'girth': 'I thought the Witcher card game was GIRTH instead of GWENT',
        'overkill': 'A tabletop RPG developed by Joseph Barber goo.gl/bmV3vq',
		'sens': '1600 dpi; 1.92 in game',
        'social': 'Get updates on my life at twitter.com/leeeennyy',
		'yusss' : 'Thank you for all the support everyone! We made it to 100+ followers!',
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

                command = None
                # Check if message is a command
                if (len(message.split(' ')) == 1):
                    command = get_search('(?<=!)[a-zA-Z]+', message)

                if not (command == None):
                    send_message(ts, '@' + username + ' ' + commands(command))
                elif (message.lower() == 'hey'):
                    send_message(ts, 'Welcome to the stream @' + username + '!')

def testshit():
    message = '!aasdasd5475 asds'
    if (len(message.split(' ')) == 1):
        ping = get_search('(?<=!)[a-zA-Z]+', message)
    else:
        ping = None

    if (ping == None):
        print('noo')
    else: print(ping)

    print(commands(ping))

if __name__ == '__main__':
    #testshit()
    main()
