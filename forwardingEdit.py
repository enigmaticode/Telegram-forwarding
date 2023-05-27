# forwarding and editing

import asyncio
import time
from telethon import TelegramClient

api_id = "ENTER API_ID"
api_hash = 'ENTER API_HAS'
phone_number = 'ENTER YOUR PHONE NUMBER'

# channel_id --> the target chat where we want to take the messages
channel_id = "ENTER THE ID OF MAIN CHAT WHERE YOU WANT TO TAKE MESSAGES"

# our destination chat
send_to_id = "ENTER THE ID OF YOUR DESTINATION CHAT "

main_dict = {'nl': 'nl'}
main_list = []
first_run = True
flag_list = False
LAST_ID = 0
number_check_edit = 5

class forward():
    async def connection(self, api_id, api_hash, phone_number):
        client = TelegramClient('session_name', api_id, api_hash)
        await client.connect()
        if not await client.is_user_authorized():
            await client.send_code_request(phone_number)
            await client.sign_in(phone_number, input('Enter the code: '))
        return client

    def dict_main(self, message, len_main_dict, n_mess):
        for i in range(len_main_dict):
            if message.date:
                date = message.date.strftime('%y%m%d_%H%M%S')
                main_dict[message.id] = [None, None, {}]
                main_dict[message.id][0] = date
                if message.edit_date != None:
                    edit_date = message.edit_date.strftime('%y%m%d_%H%M%S')
                    main_dict[message.id][1] = edit_date
        if len_main_dict >= n_mess:
            k = list(main_dict.keys())[0]
            del main_dict[k]
            len_main_dict = len(main_dict)-1

        last_nList = list(main_dict.keys())[len_main_dict]
        main_list.append(last_nList)
        l_main_list = len(main_list)
        # must be equal to the check number
        if l_main_list > number_check_edit:
            del main_list[0]
        return main_dict

    async def mess_type(self, client, message, mess, media_type):
        if media_type == 'MessageMediaPhoto':
            media = message.media
            photo = await client.download_media(media)
            file_path = f'ENTER THE PATH WHERE YOU WANT TO SAVE THE PHOTOS/{photo}'
            input_photo = await client.upload_file(file_path)
            if mess == '' or mess == ' ':
                await client.send_file(send_to_id, input_photo)
            else:
                caption = mess
                pass
                #await client.send_file(send_to_id, input_photo, caption=caption)
        elif media_type == 'MessageMediaDocument':
            document = message.document
            video = await client.download_media(document)
            file_path = f'ENTER THE PATH WHERE YOU WANT TO SAVE THE VIDEOS/{video}'
            input_video = await client.upload_file(file_path)
            if mess == '' or mess == ' ':
                await client.send_file(send_to_id, input_video)
            else:
                caption = mess
                await client.send_file(send_to_id, input_video, caption=caption)
        elif (mess != '' or mess != ' ') and message.media == None:
            print(message)
            await client.send_message(send_to_id, mess)
        elif message.out == False and message.fwd_from != None:
            print(message)
            await client.send_message(send_to_id, mess)
        else:
            print(f"SENDING THIS HAS NOT YET BEEN ENABLED")

    async def get_messages(self):
        global LAST_ID, lastId_temp
        global first_run
        client = await self.connection(api_id, api_hash, phone_number)
        await client.get_dialogs()
        messages = await client.get_messages(channel_id, None)
        # enter how many messages you want to check for sending
        n_mess = number_check_edit
        order_mes = n_mess - 1
        if first_run:
            LAST_ID = messages[n_mess].id
        else:
            LAST_ID = LAST_ID
        n_sent = 0
        n_run = 0
        for i in range(n_mess):
            len_main_dict = len(main_dict)
            message = messages[order_mes - i]
            if LAST_ID <= messages[order_mes - i].id:
                mess = message.message
                media_type = type(message.media).__name__
                if first_run:
                    await self.mess_type(client, message, mess, media_type)
                    self.dict_main(message, len_main_dict, n_mess)
                    if n_run == n_mess-1:
                        first_run = False
                    n_run += 1
                else:
                    if LAST_ID < message.id:
                        await self.mess_type(client, message, mess, media_type)
                        self.dict_main(message, len_main_dict, n_mess)
                        n_sent +=1
            lastId_temp = message.id
        LAST_ID = lastId_temp

        await client.disconnect()
        return n_sent

    async def event_edit(self):
        dict_edit = {}
        client = await self.connection(api_id, api_hash, phone_number)
        await client.get_dialogs()
        messages = await client.get_messages(channel_id, None)
        # enter the number of how many messages you want to check to see if they have been changed
        n_mess = number_check_edit
        order_mes = n_mess - 1
        for i in range(n_mess):
            message = messages[order_mes - i]
            mess = message.message
            if message.edit_date != None:
                edit_date = message.edit_date.strftime('%y%m%d_%H%M%S')
                len_id = len(main_dict)
                for i in range(len_id):
                    k = list(main_dict.keys())[i]
                    v = main_dict[k][1]
                    if k == message.id:
                        if v == edit_date:
                            pass
                        else:
                            main_dict[k][1] = edit_date
                            dict_edit[message.id] = mess

        await client.disconnect()
        return dict_edit

    async def recoveryId_sub(self, dict_edit, client, chat_to_edit):
        for i in dict_edit.keys():
            for j in main_dict.keys():
                if i == j:
                    id = list(main_dict[j][2].keys())[0]
                    new_text = dict_edit[i]
                    await client.edit_message(chat_to_edit, id, new_text)


    async def recovery_id(self, n_sent, dict_edit):
        global flag_list
        client = await self.connection(api_id, api_hash, phone_number)
        await client.get_dialogs()
        messages = await client.get_messages(send_to_id, None)
        if flag_list == False:
            # enter the number of how many messages you want to check to see if they have been changed
            n_mess = 5
            order_mes = n_mess - 1
        else:
            n_mess = n_sent
            order_mes = n_mess
        if flag_list == False:
            for i in range(n_mess):
                len_main_dict = len(main_dict)
                message = messages[order_mes - i]
                k = list(main_dict.keys())[i]
                main_dict[k][2][message.id] = [None, None]
                date = message.date.strftime('%y%m%d_%H%M%S')
                main_dict[k][2][message.id][0] = date
                if message.edit_date != None:
                    edit_date = message.edit_date.strftime('%y%m%d_%H%M%S')
                    main_dict[k][2][message.id][1] = edit_date
        else:
            len_main_dict = len(main_dict)
            for i in range(n_mess):
                message = messages[order_mes - i-1]
                k = list(main_dict.keys())[len_main_dict-n_sent+i]
                main_dict[k][2][message.id] = [None, None]
                date = message.date.strftime('%y%m%d_%H%M%S')
                main_dict[k][2][message.id][0] = date
                if message.edit_date != None:
                    edit_date = message.edit_date.strftime('%y%m%d_%H%M%S')
                    main_dict[k][2][message.id][1] = edit_date
        await self.recoveryId_sub(dict_edit, client, send_to_id)
        flag_list = True
        await client.disconnect()

n_run = 0
while True:
    n_run += 1
    instance = forward()
    get_messages = asyncio.run(instance.get_messages())
    event_edit = asyncio.run(instance.event_edit())
    asyncio.run(instance.recovery_id(get_messages, event_edit))

    time.sleep(5)
