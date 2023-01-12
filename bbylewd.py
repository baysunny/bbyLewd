import discord
from datetime import datetime
import requests
import json
import random
from pytz import timezone
import io
import os
# import stay_alive


to = "NzU4MTUwMDU3MzcwNDUxOTc4.GYO15P."
ken = "e8yoTY5oSqmL15vSXZIY504bqk08z94DtxwIX4"
token = to+ken
intents = discord.Intents.all()
client = discord.Client(intents=intents)
my_id = 532366409531916288
lewdie_id = 747420254392811610
bbylewd_id = 758150057370451978
log_server_id = 792394312226570240
log_channels = {
    "log-users": 792394987961581619,
    "log-status": 792395682564669450,
    "log-activities": 792396184764416041,
    "log-messages": 792396537467895849,
    "log-edited-messages": 887409260240175104,
    "log-deleted-messages": 792396596486471691,
    "log-files": 792396630623911986
}

target_channel = {
    "chit-chat-channel": 757902469568135209,
    "welcum-channel": 757865221443289174,
    "bbyLewd-channel": 762607426582085642,
    "i have been missing": 785944833541537802,
    "channel-error-notification": 0
}

gif_keys = {
    "server-left": random.choice(["anime cry", "anime bye", "anime sad"]),
    "server-joined": random.choice(["anime hello", "anime hi", "anime happy"]),
}


class Server:
    log_channels = {
        "log-users": 792394987961581619,
        "log-status": 792395682564669450,
        "log-activities": 792396184764416041,
        "log-messages": 792396537467895849,
        "log-edited-messages": 887409260240175104,
        "log-deleted-messages": 792396596486471691,
        "log-files": 792396630623911986
    }

    def __init__(self):
        pass


def get_current_time():
    return str(datetime.now(timezone('Asia/Jakarta')).strftime('%I:%M:%S %p'))


def get_gif(search):
    api_key = "LIVDSRZULELA"
    lmt = 8
    r = requests.get("https://api.tenor.com/v1/anonid?key=%s" % api_key)

    if r.status_code == 200:
        anon_id = json.loads(r.content)["anon_id"]
    else:
        anon_id = ""

    r = requests.get(
        "https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s&anon_id=%s" %
        (search, api_key, lmt, anon_id))
    gifs = []
    if r.status_code == 200:
        top_8gifs = json.loads(r.content)
        for i in range(len(top_8gifs['results'])):
            url = top_8gifs['results'][i]['media'][0]['gif']['url']
            gifs.append(url)
    return random.choice(gifs) if len(gifs) > 0 else ""


def message_label(message):
    return f"```{get_current_time()} | {message.channel.name} | {message.author.display_name}```"


@client.event
async def on_ready():
    bbylewd = client.get_user(my_id)
    await bbylewd.send(f"```{get_current_time()} : 0.0kinsha is running```")
    print(f"logged in as {client.user}\n")


@client.event
async def on_message(message):
    emojis = [':Barbara_worried:', ':KeqingAyaya:', ':Hutao_sweat:', ':Nose_Bleed:', ':Satania_wut:', ':Satania_huh:',
              ':Satania_Evil_smile:']

    if message.author.id == bbylewd_id:
        return
    if str(message.content).lower() == "hello":
        for emoji in emojis:
            await message.add_reaction(emoji)
    else:
        message_type = ""
        if len(message.attachments) != 0:
            url = message.attachments[0].url
            print(url)
            message_type = "image"

        if message_type == "image":
            print("type : Image")
            files = []
            for file in message.attachments:
                fp = io.BytesIO()
                await file.save(fp)
                files.append(discord.File(fp, filename=file.filename, spoiler=file.is_spoiler()))
            channel = client.get_channel(log_channels["log-files"])
            await channel.send(content=f"{message_label(message)}{message.content}", files=files)

        else:
            print("type : Text")
            channel = client.get_channel(log_channels["log-messages"])
            print("\n=======! new message")
            print(f"{get_current_time()} | {message.author.display_name}: {message.content}")
            await channel.send(f"{message_label(message)}{message.content}")
            if message.author.id == lewdie_id:
                channel = client.get_user(my_id)
                await channel.send(f"{message_label(message)}{message.content}")


@client.event
async def on_message_edit(before, after):
    channel = client.get_channel(log_channels["log-edited-messages"])
    if after.author.avatar == before.author.avatar:
        await channel.send(f"```{get_current_time()} | {before.channel.name} | {before.author.display_name}```"
                           f"**Original-Message** : \n{before.content}\n"
                           f"**Edited-Message** : \n{after.content}")


@client.event
async def on_message_delete(message):
    channel = client.get_channel(log_channels["log-deleted-messages"])

    if message.channel.id == log_channels["log-deleted-messages"]:
        return

    message_type = ""
    if len(message.attachments) != 0:
        url = message.attachments[0].url
        print(url)
        message_type = "image"

    if message_type == "image":
        print("type : Image")
        files = []
        for file in message.attachments:
            fp = io.BytesIO()
            await file.save(fp)
            files.append(discord.File(fp, filename=file.filename, spoiler=file.is_spoiler()))
        await channel.send(content=f"{message_label(message)}{message.content}", files=files)

    else:
        print(f"{get_current_time()} | {message.author.display_name}: {message.content}")
        await channel.send(f"{message_label(message)}{message.content}")


@client.event
async def on_member_join(member):

    c = 0
    for m in member.guild.members:
        if not m.bot:
            c += 1
    for channel in member.guild.channels:
        if channel.id == target_channel["welcum-channel"]:
            description = random.choice(
                ["who are you?",
                 "free whisshy whooshy for a week",
                 f"say hi to {member.display_name}",
                 "annyeong!",
                 "enjoy the lewdness"]
            )
            embed = discord.Embed(
                description=description,
                color=0x00ff00)
            embed.set_author(name=f"welcum {member.display_name}")
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_image(url=get_gif(gif_keys["server-joined"]))
            embed.set_footer(text=f"{member.display_name} joined the server as member-{c}")
            print("\n======= server update")
            print(f"{member.display_name} joined the server")
            await channel.send(embed=embed)


@client.event
async def on_member_remove(member):
    for channel in member.guild.channels:
        if channel.id == target_channel["welcum-channel"]:
            description = random.choice(
                ["bye bye",
                 "yay",
                 f"feel lonely",
                 "shoo shoo"]
            )
            embed = discord.Embed(
                description=description,
                color=0x00ff00)
            embed.set_author(name=f"{member.display_name} left the server!")
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_image(url=get_gif(gif_keys["server-left"]))
            embed.set_footer(text=f"{member.display_name} bye bye")
            print("\n======= server update")
            print(f"{member.display_name} left the server")
            await channel.send(embed=embed)


@client.event
async def on_presence_update(before, after):
    channel = client.get_channel(log_channels["log-status"])
    if after.status != before.status:
        # print(f"=====test {before.id}")
        if before.guild.id != log_server_id and before.id != my_id:
            print(f"```{get_current_time()} --:-- [{after.status}] --:-- {before.display_name}```")
            await channel.send(f"```{get_current_time()} --:-- [{after.status}] --:-- {before.display_name}```")
            if after.id == lewdie_id:
                channel = client.get_user(my_id)
                await channel.send(f"```{get_current_time()} --:-- [{after.status}] --:-- {before.display_name}```")
    elif after.activity != before.activity:
        if not before.bot:
            if before.guild.id != log_server_id:
                channel = client.get_channel(log_channels["log-activities"])
                await channel.send(f"```{get_current_time()} --:-- {before.display_name} : [{after.activity}]```")
                if after.id == lewdie_id:
                    channel = client.get_user(my_id)
                    await channel.send(f"```{get_current_time()} --:-- {before.display_name} : [{after.activity}]```")


@client.event
async def on_user_update(before, after):
    channel = client.get_channel(log_channels["log-users"])
    if after.avatar != before.avatar:
        await channel.send(f"```{get_current_time()} --:-- {before.display_name} updated avatar```{after.avatar}")


# client.run(token)
while __name__ == '__main__':
    try:
        # keep_alive()
        # replNeverSleep.awake('', True)
        client.run(token)
    except discord.errors.HTTPException as e:
        print(e)
        print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
        os.system('kill 1')
