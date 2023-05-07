import asyncio
import json
import os

import chats_writer
import loader as l

from telebot import async_telebot
from telebot import types

print(os.getcwd())

PATH = "config.json"
PATH_DB = "chats.json"
PATH_SL = "save.json"
PATH_LANG = "lang"

ANONIM_CHANNEL = 136817688 #DON'T EDIT THIS CONSTANT!!!

BOT_CONFIG = l.load_config(PATH)
Chats = l.load_chats(PATH_DB)["chats"]

bot_lang = l.load_lang(str(l.load_save(PATH_SL)["lang"]), PATH_LANG)
bot = async_telebot.AsyncTeleBot(BOT_CONFIG["token"])
bot_info = types.User(0, True, "Null")

@bot.message_handler(content_types=["text"])
async def messages(msg: types.Message):
    global bot_lang, lang
    bot_info = await bot.get_me()
    chat = {"id": msg.chat.id, "enabled": False}
    if(len(Chats) > 0):
        for i in range(0, len(Chats)):
            if int(Chats[i]["id"]) == msg.chat.id:
                chat = Chats[i]
                break

    if msg.chat.id != msg.from_user.id and msg.from_user.id == ANONIM_CHANNEL and bool(chat["enabled"]) == True:
        bot_rights = await bot.get_chat_member(msg.chat.id, bot_info.id)
        if bot_rights.can_delete_messages == False:
            await bot.send_message(msg.chat.id, bot_lang["BOT_IS_NOT_ADMIN"], parse_mode="html")
        else:
            await bot.delete_message(msg.chat.id, msg.message_id)

    if msg.chat.id != msg.from_user.id and msg.from_user.id == int(BOT_CONFIG["owner"]):
        if msg.text.lower() == "/initialize_chat" or msg.text.lower() == "/initialize_chat@" + bot_info.username.lower():
            chat_writen = False
            if(len(Chats) > 0):
                for i in range(0, len(Chats)):
                    if int(Chats[i]["id"]) == msg.chat.id:
                        chat_writen = True
                        break

            if chat_writen == False:
                Chats.append({"id": msg.chat.id, "enabled": True})
                chats_writer.update_config(PATH_DB, {"chats": Chats})
                await bot.send_message(msg.chat.id, bot_lang["CHAT_INITIALIZED"], parse_mode='html')
            else:
                await bot.send_message(msg.chat.id, bot_lang["CHAT_IS_INITIALIZED"], parse_mode='html')
        if msg.text.lower() == "/help" or msg.text.lower() == "/help@" + bot_info.username.lower():
            await bot.send_message(msg.chat.id, bot_lang["HELP"], parse_mode='html')
        if msg.text.lower() == "/disable_chat" or msg.text.lower() == "/disable_chat@" + bot_info.username.lower():
            chat_writen = False
            if(len(Chats) > 0):
                for i in range(0, len(Chats)):
                    if int(Chats[i]["id"]) == msg.chat.id:
                        chat_writen = True
                        break

            if chat_writen == False:
                await bot.send_message(msg.chat.id, bot_lang["CHAT_NOT_FOUND"], parse_mode='html')
            else:
                for i in range(0, len(Chats)):
                    if int(Chats[i]["id"]) == msg.chat.id:
                        Chats[i]["enabled"] = False
                        break
                chats_writer.update_config(PATH_DB, {"chats": Chats})
                await bot.send_message(msg.chat.id, bot_lang["BOT_IN_CHAT_DISABLED"], parse_mode='html')
        if msg.text.lower() == "/enable_chat" or msg.text.lower() == "/enable_chat@" + bot_info.username.lower():
            chat_writen = False
            if(len(Chats) > 0):
                for i in range(0, len(Chats)):
                    if int(Chats[i]["id"]) == msg.chat.id:
                        chat_writen = True
                        break

            if chat_writen == False:
                await bot.send_message(msg.chat.id, bot_lang["CHAT_NOT_FOUND"], parse_mode='html')
            else:
                for i in range(0, len(Chats)):
                    if int(Chats[i]["id"]) == msg.chat.id:
                        Chats[i]["enabled"] = True
                        break
                chats_writer.update_config(PATH_DB, {"chats": Chats})
                await bot.send_message(msg.chat.id, bot_lang["BOT_IN_CHAT_ENABLED"], parse_mode='html')
        if msg.text.lower().startswith("/set_lang ") or msg.text.lower().startswith(f"/set_lang@{bot_info.username.lower()} "):
            new_lang = msg.text.lower().split(msg.text.lower().split(" ")[0])[1].lower().replace(" ", "")
            try:
                temp_lang = l.load_lang(new_lang, PATH_LANG)
                bot_lang = temp_lang
                chats_writer.update_lang(PATH_SL, {"lang": new_lang})
                await bot.send_message(msg.chat.id, bot_lang["LANG_INSTALLED"], parse_mode="html")
            except FileNotFoundError:
                lang = l.load_lang(l.load_save(PATH_SL)["lang"], PATH_LANG)
                await bot.send_message(msg.chat.id, bot_lang["LANG_NOT_FOUND"], parse_mode='html')

    elif msg.chat.id == msg.from_user.id:
         if msg.text.lower().startswith("/set_lang "):
            new_lang = msg.text.lower().split(msg.text.lower().split(" ")[0])[1].lower().replace(" ", "")
            try:
                temp_lang = l.load_lang(new_lang, PATH_LANG)
                bot_lang = temp_lang
                chats_writer.update_lang(PATH_SL, {"lang": new_lang})
                await bot.send_message(msg.chat.id, bot_lang["LANG_INSTALLED"], parse_mode="html")
            except FileNotFoundError:
                lang = l.load_lang(l.load_save(PATH_SL)["lang"], PATH_LANG)
                await bot.send_message(msg.chat.id, bot_lang["LANG_NOT_FOUND"], parse_mode='html')
        if msg.text.lower() == "/help":
            await bot.send_message(msg.chat.id, bot_lang["HELP"], parse_mode='html')
        if msg.text.lower() == "/getmyid":
            await bot.send_message(msg.from_user.id, f"{msg.from_user.id}")

@bot.message_handler(content_types=["video"])
async def messages(msg: types.Message):
    bot_info = await bot.get_me()
    chat = {"id": msg.chat.id, "enabled": False}
    if(len(Chats) > 0):
        for i in range(0, len(Chats)):
            if int(Chats[i]["id"]) == msg.chat.id:
                chat = Chats[i]
                break

    if msg.chat.id != msg.from_user.id and msg.from_user.id == ANONIM_CHANNEL and bool(chat["enabled"]) == True:
        bot_rights = await bot.get_chat_member(msg.chat.id, bot_info.id)
        if bot_rights.can_delete_messages == False:
            await bot.send_message(msg.chat.id, bot_lang["BOT_IS_NOT_ADMIN"], parse_mode="html")
        else:
            await bot.delete_message(msg.chat.id, msg.message_id)

@bot.message_handler(content_types=["photo"])
async def messages(msg: types.Message):
    bot_info = await bot.get_me()
    chat = {"id": msg.chat.id, "enabled": False}
    if(len(Chats) > 0):
        for i in range(0, len(Chats)):
            if int(Chats[i]["id"]) == msg.chat.id:
                chat = Chats[i]
                break

    if msg.chat.id != msg.from_user.id and msg.from_user.id == ANONIM_CHANNEL and bool(chat["enabled"]) == True:
        bot_rights = await bot.get_chat_member(msg.chat.id, bot_info.id)
        if bot_rights.can_delete_messages == False:
            await bot.send_message(msg.chat.id, bot_lang["BOT_IS_NOT_ADMIN"], parse_mode="html")
        else:
            await bot.delete_message(msg.chat.id, msg.message_id)

@bot.message_handler(content_types=["sticker"])
async def messages(msg: types.Message):
    bot_info = await bot.get_me()
    chat = {"id": msg.chat.id, "enabled": False}
    if(len(Chats) > 0):
        for i in range(0, len(Chats)):
            if int(Chats[i]["id"]) == msg.chat.id:
                chat = Chats[i]
                break

    if msg.chat.id != msg.from_user.id and msg.from_user.id == ANONIM_CHANNEL and bool(chat["enabled"]) == True:
        bot_rights = await bot.get_chat_member(msg.chat.id, bot_info.id)
        if bot_rights.can_delete_messages == False:
            await bot.send_message(msg.chat.id, bot_lang["BOT_IS_NOT_ADMIN"], parse_mode="html")
        else:
            await bot.delete_message(msg.chat.id, msg.message_id)

@bot.message_handler(content_types=["document"])
async def messages(msg: types.Message):
    bot_info = await bot.get_me()
    chat = {"id": msg.chat.id, "enabled": False}
    if(len(Chats) > 0):
        for i in range(0, len(Chats)):
            if int(Chats[i]["id"]) == msg.chat.id:
                chat = Chats[i]
                break

    if msg.chat.id != msg.from_user.id and msg.from_user.id == ANONIM_CHANNEL and bool(chat["enabled"]) == True:
        bot_rights = await bot.get_chat_member(msg.chat.id, bot_info.id)
        if bot_rights.can_delete_messages == False:
            await bot.send_message(msg.chat.id, bot_lang["BOT_IS_NOT_ADMIN"], parse_mode="html")
        else:
            await bot.delete_message(msg.chat.id, msg.message_id)

@bot.message_handler(content_types=["animation"])
async def messages(msg: types.Message):
    bot_info = await bot.get_me()
    chat = {"id": msg.chat.id, "enabled": False}
    if(len(Chats) > 0):
        for i in range(0, len(Chats)):
            if int(Chats[i]["id"]) == msg.chat.id:
                chat = Chats[i]
                break

    if msg.chat.id != msg.from_user.id and msg.from_user.id == ANONIM_CHANNEL and bool(chat["enabled"]) == True:
        bot_rights = await bot.get_chat_member(msg.chat.id, bot_info.id)
        if bot_rights.can_delete_messages == False:
            await bot.send_message(msg.chat.id, bot_lang["BOT_IS_NOT_ADMIN"], parse_mode="html")
        else:
            await bot.delete_message(msg.chat.id, msg.message_id)

@bot.message_handler(content_types=["audio"])
async def messages(msg: types.Message):
    bot_info = await bot.get_me()
    chat = {"id": msg.chat.id, "enabled": False}
    if(len(Chats) > 0):
        for i in range(0, len(Chats)):
            if int(Chats[i]["id"]) == msg.chat.id:
                chat = Chats[i]
                break

    if msg.chat.id != msg.from_user.id and msg.from_user.id == ANONIM_CHANNEL and bool(chat["enabled"]) == True:
        bot_rights = await bot.get_chat_member(msg.chat.id, bot_info.id)
        if bot_rights.can_delete_messages == False:
            await bot.send_message(msg.chat.id, bot_lang["BOT_IS_NOT_ADMIN"], parse_mode="html")
        else:
            await bot.delete_message(msg.chat.id, msg.message_id)


@bot.message_handler(content_types=["new_chat_members"])
async def ncm(msg: types.Message):
    if msg.new_chat_members[0].id == bot_info.id:
        await bot.send_message(msg.chat.id, bot_lang["BOT_JOINED"], parse_mode='html')

asyncio.run(bot.infinity_polling(skip_pending=True))
