import os, db, time, asyncio, random, shutil
from pySmartDL import SmartDL
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.types import InputMediaPhoto, InputMediaVideo, InputMediaAudio, InputMediaDocument
from pyrogram.errors import FloodWait

# Configs
API_HASH = os.environ['API_HASH']
APP_ID = int(os.environ['API_ID'])
BOT_TOKEN = os.environ['BOT_TOKEN']
CHANNEL_ID = int(os.environ['CHANNEL_ID'])
OWNER_ID = os.environ['OWNER_ID']
GAP = [1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 2, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3]

#Button
START_BUTTONS=[
    [
        InlineKeyboardButton('Source', url='https://t.me/PayYourBot'),
        InlineKeyboardButton('Project Channel', url='https://t.me/xTeamBots'),
    ],
    [InlineKeyboardButton('Author', url="https://t.me/xgorn")],
]

# Running bot
xbot = Client('Channel-Media-Group-Autopost', api_id=APP_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


# Start
@xbot.on_message(filters.command('start') & filters.private)
async def _start(bot, update):
    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)
    if update.from_user.id != OWNER_ID:
        return await update.reply('Only the owner can use this bot!\n\nCredit: @PayYourBot', True, reply_markup=InlineKeyboardMarkup(START_BUTTONS))
    await update.reply(f"Hi. Send media (photo / video / audio / document) and you're ready to go.\n\nCredit: @PayYourBot", True, reply_markup=InlineKeyboardMarkup(START_BUTTONS))

# Store media to database
@xbot.on_message(filters.media & filters.private)
async def _media(bot, update):
    dbx = await db.get_user(update.from_user.id)
    if dbx['limit'] == 'on':
        await asyncio.sleep(random.choice(GAP))
        await db.limit_off(update.from_user.id)
    else:
        await db.limit_on(update.from_user.id)
    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)
    if update.from_user.id != OWNER_ID:
        return
    if not update.photo:
        if not update.video:
            if not update.document:
                if not update.audio:
                    return
    if update.video:
        idx = update.video.file_id
    elif update.photo:
        idx = update.photo.file_id
    elif check.audio:
        idx = update.audio.file_id
    elif check.document:
        idx = update.document.file_id
    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)
    dbx = await db.get_user(update.from_user.id)
    if dbx['medias'] == '':
        await db.add_media(update.from_user.id, idx)
        await update.delete()
        return
    await db.add_media(update.from_user.id, f'{dbx["medias"]}|{idx}')
    await update.delete()

@xbot.on_message(filters.regex('http') & filters.private)
async def _urls(bot, update):
    dbx = await db.get_user(update.from_user.id)
    if dbx['limit'] == 'on':
        await asyncio.sleep(random.choice(GAP))
        await db.limit_off(update.from_user.id)
    else:
        await db.limit_on(update.from_user.id)
    await update.delete()
    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)
    if update.from_user.id != OWNER_ID:
        return
    url = update.text
    os.mkdir('./Downloads.')
    dest = './Downloads/'
    obj = SmartDL(url, dest)
    path = obj.get_dest()
    if dbx['medias'] == '':
        await db.add_media(update.from_user.id, path)
        await update.delete()
        return
    await db.add_media(update.from_user.id, f'{dbx["medias"]}|{path}')
    await update.delete()
    

@xbot.on_message(filters.command('post') & filters.private)
async def _post(bot, update):
    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)
    if update.from_user.id != OWNER_ID:
        return
    await update.delete()
    dbx = await db.get_user(update.from_user.id)
    if dbx['medias'] == '':
        await update.reply('You haven\'t send me a media yet. you can send photo, video, document and audio')
    if '|' in dbx['medias']:
        return await update.reply(
            'Send media group as?',
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton('Photo', 'photo'),
                    InlineKeyboardButton('Video', 'video'),
                ],
                [
                    InlineKeyboardButton('Document', 'document'),
                    InlineKeyboardButton('Audio', 'audio'),
                ]
            ]),
            quote=True
        )
    else:
        await update.reply('Send more medias.')


@xbot.on_callback_query()
async def buttons(bot, update):
    cb = update.data
    await update.message.delete()
    dbx = await db.get_user(update.from_user.id)
    if cb == 'photo':
        photos = dbx['medias'].split('|')
        for i in range(0, len(photos), 10):
            chunk = photos[i:i + 10]
            media = []
            for photo in chunk:
                media.append(InputMediaPhoto(media=photo))
            try:
                await bot.send_media_group(chat_id=CHANNEL_ID, media=media, disable_notification=True)
                time.sleep(3)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await bot.send_media_group(chat_id=CHANNEL_ID, media=media, disable_notification=True)
                time.sleep(3)
            except ValueError:
                await update.message.reply('You selected wrong button or maybe you sended two different file type. i\'ll remove all stored files.')
                await db.remove_all_media(update.from_user.id)
                try:
                    shutil.rmtree('./Downloads/')
                except:
                    return
                return
            await db.remove_all_media(update.from_user.id)
            try:
                shutil.rmtree('./Downloads/')
            except:
                return
    elif cb == 'video':
        videos = dbx['medias'].split('|')
        for i in range(0, len(videos), 10):
            chunk = videos[i:i + 10]
            media = []
            for video in chunk:
                media.append(InputMediaVideo(media=video))
            try:
                await bot.send_media_group(chat_id=CHANNEL_ID, media=media, disable_notification=True)
                time.sleep(3)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await bot.send_media_group(chat_id=CHANNEL_ID, media=media, disable_notification=True)
                time.sleep(3)
            except ValueError:
                await update.message.reply('You selected wrong button or maybe you sended two different file type. i\'ll remove all stored files.')
                await db.remove_all_media(update.from_user.id)
                try:
                    shutil.rmtree('./Downloads/')
                except:
                    return
                return
            await db.remove_all_media(update.from_user.id)
            try:
                shutil.rmtree('./Downloads/')
            except:
                return
    elif cb == 'audio':
        audios = dbx['medias'].split('|')
        for i in range(0, len(audios), 10):
            chunk = audios[i:i + 10]
            media = []
            for audio in chunk:
                media.append(InputMediaAudio(media=audio))
            try:
                await bot.send_media_group(chat_id=CHANNEL_ID, media=media, disable_notification=True)
                time.sleep(3)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await bot.send_media_group(chat_id=CHANNEL_ID, media=media, disable_notification=True)
                time.sleep(3)
            except ValueError:
                await update.message.reply('You selected wrong button or maybe you sended two different file type. i\'ll remove all stored files.')
                await db.remove_all_media(update.from_user.id)
                try:
                    shutil.rmtree('./Downloads/')
                except:
                    return
                return
            await db.remove_all_media(update.from_user.id)
            try:
                shutil.rmtree('./Downloads/')
            except:
                return
    elif cb == 'document':
        documents = dbx['medias'].split('|')
        for i in range(0, len(documents), 10):
            chunk = documents[i:i + 10]
            media = []
            for document in chunk:
                media.append(InputMediaDocument(media=document))
            try:
                await bot.send_media_group(chat_id=CHANNEL_ID, media=media, disable_notification=True)
                time.sleep(3)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await bot.send_media_group(chat_id=CHANNEL_ID, media=media, disable_notification=True)
                time.sleep(3)
            except ValueError:
                await update.message.reply('You selected wrong button or maybe you sended two different file type. i\'ll remove all stored files.')
                await db.remove_all_media(update.from_user.id)
                try:
                    shutil.rmtree('./Downloads/')
                except:
                    return
                return
            await db.remove_all_media(update.from_user.id)
            try:
                shutil.rmtree('./Downloads/')
            except:
                return

@xbot.on_message(filters.command('reset') & filters.private)
async def _reset(bot, update):
    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)
    if update.from_user.id != OWNER_ID:
        return
    await update.delete()
    await db.remove_all_media(update.from_user.id)
    try:
        shutil.rmtree('./Downloads/')
    except:
        pass
    await update.reply('Cleared all stored files.')


xbot.run()