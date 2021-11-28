from telethon.sync import TelegramClient
# The TelegramClient aggregates several mixin classes to provide all the common functionality in a nice, Pythonic interface. Each mixin has its own methods, which you all can use.
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import sys
import csv
import traceback
import time
 
api_id = 1111111
api_hash = '526fvhe7i2hejkjy7t33vjf2ywgy'
phone = '+1111111111111'
client = TelegramClient(phone, api_id, api_hash)
 
client.connect()
# The connect() method of Python's socket module, connects a TCP(Transmission Control Protocol) based client socket to a TCP based server socket
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))
 
input_file ="users.txt"
# sys. argv is a list in Python, which contains the command-line arguments passed to the script.
# So if you run python sendMessage.py users.csv in the command line  sys.argv will return a list like this:
# ['sendMessage.py', 'users.csv']
users = []
with open(input_file, encoding='UTF-8') as f:
    # csv property when file is open it give , and \n at the end of a row
    rows = csv.reader(f,delimiter=",",lineterminator="\n")
    # skip first line all heading because we do not need heading we need data
    next(rows, None)
    for row in rows:
        user = {}
        user['username'] = row[0]
        user['id'] = int(row[1])
        user['access_hash'] = int(row[2])
        user['name'] = row[3]
        users.append(user)
#  Create an empty list for chats and populate with the results which you get from GetDialogsRequest
chats = []
last_date = None
chunk_size = 200
groups=[]
     # First get all groups using  GetDialogsRequest .
result = client(GetDialogsRequest(
    # offset_date and  offset_peer are used for filtering the chats. 
             offset_date=last_date,
            #   offset_id and limit are used for pagination
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=chunk_size,
             hash = 0
         ))
chats.extend(result.chats)
 
for chat in chats:
            groups.append(chat)
print('Choose a group to add members:')
i=0
for group in groups:
    print(str(i) + '- ' + group.title)
    i+=1
 
g_index = input("Enter a Number: ")
target_group=groups[int(g_index)]
 
target_group_entity = InputPeerChannel(target_group.id,target_group.access_hash)
 
mode = int(input("Enter 1 to add by username or 2 to add by ID: "))
 
for user in users:
    try:
        print ("Adding {}".format(user['id']))
        if mode == 1:
            if user['username'] == "":
                continue
            user_to_add = client.get_input_entity(user['username'])
        elif mode == 2:
            user_to_add = InputPeerUser(user['id'], user['access_hash'])
        else:
            sys.exit("Invalid Mode Selected. Please Try Again.")
        client(InviteToChannelRequest(target_group_entity,[user_to_add]))
        print("Waiting one Seconds...")
        time.sleep(1)
    except PeerFloodError:
        print("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
    except UserPrivacyRestrictedError:
        print("The user's privacy settings do not allow you to do this. Skipping.")
    except:
        traceback.print_exc()
        print("Unexpected Error")
        continue
 
