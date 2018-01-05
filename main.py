import socket
import re
import urllib.request
import config
import time

def send_message(socket, message):
    socket.send(('PRIVMSG #' + config.CHAN + ' :' + message + '\r\n').encode())
    print('[BOT] -> ' + config.CHAN + ': ' + message + '\n')

def send_pong(socket):
    socket.send(('PONG :tmi.twitch.tv\r\n').encode())
    print('[BOT] -> Sent a pong \n')

def get_search(pattern, text):
    same = re.search(pattern, text)
    return None if same == None else same.group(0)

start_time = time.time()

def uptime():
    #diff = time.gmtime(time.time() - start_time)
    uptime = "Leeny has been streaming for "

    minutes, seconds = divmod(int(time.time() - start_time), 60)
    hours, minutes = divmod(minutes, 60)

    if (hours == 0):
        if (minutes == 0):
            return uptime + f'{seconds} seconds.'
        else:
            return uptime + f'{minutes} minutes and {seconds} seconds.'
    else:
        return uptime + f'{hours} hours, {minutes} minutes and {seconds} seconds.'
    #return time.strftime("Leeny has been streaming for %H hours, %M minutes and %S seconds.", time.gmtime(time.time() - start_time))

def commands(x):
    return {
        'commands': '!discord | !elo | !girth | !overkill | !rekt | !sens | !social | !subtember | !thanks | !uptime',
        #'coolkids': 'Dane [twitch.tv/dhQk] | Jordan [twitch.tv/IncredFruityTV] | Leon [twitch.tv/LeoniLive] | Mitchell [twitch.tv/SenOokami] | MK [twitch.tv/Zexy_DemoN] | MyselfWhat [twitch.tv/MyselfWhat] | Rag [twitch.tv/Ragnarok1stx] | Sam [twitch.tv/SamKayNZ] | Sav [twitch.tv/Amorisaiya]',
        'discord': 'Come have some yarns with me at discord.gg/xGBFGZx',
        'elo': 'goo.gl/DUhU6j',
        #'emotes': 'leeeenLove leeeenKiss',
        'girth': 'I thought the Witcher card game was GIRTH instead of GWENT',
        'overkill': 'A tabletop RPG developed by Joseph Barber goo.gl/bmV3vq',
        'rekt': '☐ Not rekt ☑ Rekt',
        'sens': '1600 dpi; 1.92 in game',
        'social': 'Get updates on my life at twitter.com/leeeennyy',
		'subtember': 'They\'re half price at the moment if you want to sub',
		'thanks': 'Thank you for all the support everyone! We made it to 100+ followers!',
        'uptime': uptime(),
    }.get(x, 'This isn\'t a command. Please look at !commands')

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
                    if (command == 'rekt'):
                        send_message(ts, commands(command))
                    else:
                        send_message(ts, '@' + username + ' ' + commands(command))
                elif (message.lower() == 'hey'):
                    send_message(ts, 'Welcome to the stream @' + username + '!')

def testshit():
    message = '!uptime'
    time.sleep(3);
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
