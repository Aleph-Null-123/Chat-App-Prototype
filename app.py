from User import AmbiguousUser, User, Server
from Database import Database
from constants import *
import os

def main():
    database = Database(SCOPE, CREDS, SHEET_NAME)
    data = database.db
    msg_db = Database(SCOPE, CREDS, CHAT_NAME)
    messages = msg_db.db
    user = User()
    server = Server()

    def get_all_users():
        return [
            AmbiguousUser(user['User IP Address'], user['User Nickname'])
             for user in data.get_all_records() if user['User IP Address'] != 'server'
        ]

    def print_users():
        print("Users: ")
        for user in get_all_users():
            print(user)
    
    def locate_user(ip = user.ip):
        try:
            return data.col_values(1).index(ip) + 1
        except:
            return None
    
    def set_nickname():
        print("Please set a display nickname.")
        user.get_nickname()

    def insert_message(ip =  '', nick = '', msg = '', time = ''):
        messages.update_acell('A2', ip)
        messages.update_acell('B2', nick)
        messages.update_acell('C2', msg)
        messages.update_acell('D2', str(time))

    def update_msg():
        data.update_cell(locate_user(), 2, user.most_recent_msg[0])
        data.update_cell(locate_user(), 3, user.most_recent_msg[1])
        insert_message(user.ip, user.nickname, user.most_recent_msg[0], user.most_recent_msg[1])

    def update_server():
        data.update_cell(locate_user('server'), 2, server.most_recent_msg[0])
        data.update_cell(locate_user('server'), 3, server.most_recent_msg[1])
        insert_message('server', 'Server Message', server.most_recent_msg[0], server.most_recent_msg[1])
    
    def cmd_help():
        print("Getting commands...")
        longest = max(map(len, list(commands)))
        for command, (description, function) in commands.items():
            print(f"- /{command}{(longest - len(command) + 5)*'.'}{description}")
        print()

    def cmd_leave():
        server.make_request(f"{user.ip} left the chat.")
        update_server()
        data.delete_rows(locate_user())
        print("Left the chat.")

    def cmd_kick():
        remove_ip = input("IP Address to kick: ")
        if locate_user(remove_ip) != None:
            if remove_ip != user.ip:
                data.delete_rows(locate_user(remove_ip))
                print(f"Kicked {remove_ip}")
                server.make_request(f"{remove_ip} kicked by {user.ip}")
                update_server()
            else:
                print("Can't kick yourself! Use /leave instead.")
        else:
            print("No such IP Address")

    def cmd_nick():
        old_nick = user.nickname
        set_nickname()
        if old_nick != user.nickname:
            print(f"Nickname updated to {user.nickname}")
            server.make_request(f"{user.ip} changed their nickname from {old_nick} to {user.nickname}")
            update_server()
        else:
            print("That was already your nickname!")

    def cmd_users():
        for user in get_all_users():
            print(user)

    commands = {
        'help': ('Displays a list of commands and what they do.', cmd_help),
        'leave': ('Allows you to safely exit the app. Using this command logs you out and revokes your access to incoming messages. Faliure to use this command allows you to keep access to the ongoing chat, and you will appear logged in.', cmd_leave),
        'kick': ('Kicks out a user given an IP Address.', cmd_kick),
        'nick': ('Changes the display nickname of a user.', cmd_nick),
        'users': ('Outputs a list of all active users.', cmd_users)
    }

    set_nickname()

    if locate_user() != None:
        data.delete_rows(locate_user())

    data.insert_row([user.ip, user.most_recent_msg[0], user.most_recent_msg[1], user.nickname], 2)
    server.make_request(f'{user.ip} joined the chat as {user.nickname}')
    update_server()

    print_users()

    print("Opening chat...")

    os.startfile('Chat.py')

    print("Chat opened in new window. Type messages in this window.")
    print("Please be sure to use the command /leave when exiting.")
    print("Type /help for a instructions on how to use commands.\n")

    while user.ip in data.col_values(1):
        typed = input("-> ").strip()

        if typed != '':
            if typed[0] == '/':
                cmd = typed[1:]
                if cmd not in commands:
                    print("No such command.")
                    continue
                else:
                    commands[cmd][1]()
                    continue
            
            user.type_msg(typed)
            update_msg()


main()
input("Enter to quit...")