import discord
from datetime import datetime
import requests
import json
import random
from pytz import timezone
import io


def get_current_time(tz='Asia/Jakarta'):
    fmt = '%I:%M:%S %p'
    eastern = timezone(tz)
    loc_dt = datetime.now(eastern)
    return loc_dt.strftime(fmt)


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


token = "NzU4MTUwMDU3MzcwNDUxOTc4.X2qwQw.f4hIHfMr42IwoJkl8XwZDU4JevU"
intents = discord.Intents.all()
client = discord.Client(intents=intents)

servers = {
    "lewd-server": 757865220604690443,
    "test-server": 739864997865455626
}
channels = {
    "chit-chat-channel": 757902469568135209,

    "user-channel": 764099351172874280,
    "log-channel": 768457244769517588,
    "channel-activity": 775349153017364500,
    "message-channel": 768457273554108447,
    "deleted-message-channel": 782182267895283733,
    "image-channel": 769195772897787943,

    "welcum-channel": 757865221443289174,
    "bbyLewd-channel": 762607426582085642,

    "channel-error-notification": 0
}


def logs_channel(channel, message_id):
    message = channel.fetch_message(message_id)
    message = str(message)
    log_setting = {
        "log-users": 1,
        "log-status": 1,
        "log-messages": 1,
        "log-files": 1,
        "log-activities": 1
    }

    # verify every key in message/database
    for key in log_setting:
        if key not in message:
            return log_setting
    extract = message.split(", ")
    for key_value in extract:
        key_value = key_value.replace(" ", "")
        if key_value.find("(on)") == -1 and key_value.find("(off)") == -1:
            client.get_channel(channels["channel-error-notification"]).send("```value error```")
            return {}
        else:
            # if logging is off
            if key_value.find("(on)") != -1:
                value = 0
            key = key_value.replace("(on)", "").replace("(off)", "")
            if key in log_setting:
                log_setting[key] = value
            else:
                # key from message not recognized
                client.get_channel(channels["channel-error-notification"]).send("```key not recognized```")
                return {}
    return log_setting


counter = {}
bot_id = 758150057370451978
member_id = [736028616764424195, 762590005314715659]

gif_keys = {
    "server-left": random.choice(["anime cry", "anime bye", "anime sad"]),
    "server-joined": random.choice(["anime hello", "anime hi", "anime happy"]),
}


@client.event
async def on_ready():
    print(f"logged in as {client.user}\n")


@client.event
async def on_message(message):

    if message.author.id == bot_id:
        return
    else:
        if message.author.id not in counter:
            counter[message.author.id] = [0, datetime.now()]
        else:
            print(counter)
            counter[message.author.id][0] += 1
            if counter[message.author.id][0] > 14:
                difference = (datetime.now() - counter[message.author.id][1]).seconds
                print(f"{message.author.display_name} : {difference}sec")
                if difference < 20:
                    await message.channel.purge(limit=2)
                    if counter[message.author.id][0] % 2 == 0:
                        await message.channel.send(f"```user {message.author.display_name} trying to spam```")
                    # delete
                else:
                    counter[message.author.id] = [0, datetime.now()]

    if str(message.content).lower() == "baysunny---":
        c = 0
        for m in message.guild.members:
            if not m.bot:
                c += 1
        embed = discord.Embed(
            description="testing",
            color=0x00ff00)
        embed.set_author(name=f"{message.author.display_name}")
        embed.set_thumbnail(url=message.author.avatar_url)
        embed.set_image(url=get_gif(gif_keys["server-joined"]))
        embed.set_footer(text=f"{message.author.display_name} / member-{c}")
        await message.channel.send(f"{get_current_time()} sent emoji: hi")
        await message.channel.send(embed=embed)
    elif str(message.content).lower() == ",,,,,,,,,,,,,,":
        await message.channel.send(message.id)
        # func (channel, message)
        # 1- receive message
        # 2- extract message
        # 3- check message
        # 4- delete message
        # 5- send response

        # last_message = await message.channel.history(limit=1).flatten()
        # test = ["1", "2"]
        # await message.channel.send(last_message[0])
        # await message.channel.send(message)
        # await message.channel.send("\n--")
        # await message.channel.send(type(test))
        # await message.channel.send(type(last_message))
        # await message.channel.send(type(message))

    # elif len(str(message.content)) > 12:
    #     if message.channel.id == 777713988054024212:
    #         if str(message.content)[:10] == "log-system":
    #             msg = str(message.content).replace("log-system", "")

    else:
        message_type = ""
        url = ""
        if len(message.attachments) != 0:
            url = message.attachments[0].url
            print(url)
            message_type = "image"

        if message_type == "image":

            files = []
            for file in message.attachments:
                fp = io.BytesIO()
                await file.save(fp)
                files.append(discord.File(fp, filename=file.filename, spoiler=file.is_spoiler()))

            print("image type")
            channel = client.get_channel(channels["image-channel"])
            await channel.send(f"```{get_current_time()} | {message.channel.name} | {message.author.display_name}``` {message.content}")
            await channel.send(files=files)
        else:
            print("text type")
            channel = client.get_channel(channels["message-channel"])
            messages = str(message.content).lower().split()
            mentioned_members = message.mentions
            print("\n======= new message")
            print(f"{get_current_time()} | {message.author.display_name}: {message.content}")
            await channel.send(f"```{get_current_time()} | {message.channel.name} | {message.author.display_name}``` {message.content}")
            # print(f"author   : {message.author.display_name}")
            # print(f"mentioned: {mentioned_members} | {len(mentioned_members)}")
            # print(f"message  : {message.content} | {len(messages)}")
            # print(f"messages : {messages}")

            if len(mentioned_members) > 1 or len(mentioned_members) == 0:
                pass
            else:
                if len(messages) > 1:
                    print(messages[1][3:-1])
                    print(str(mentioned_members[0].id))
                    if messages[1][3:-1] == str(mentioned_members[0].id):
                        embed = discord.Embed(
                            title=f"{message.author.display_name} {messages[0]} {mentioned_members[0].display_name}",
                            description="-",
                            color=0x00ff00)
                        url = get_gif(f"anime {messages[0]}")
                        if len(url) != 0:
                            print(url)
                            embed.set_image(url=url)
                            # await message.channel.send(embed=embed)
                            pass
                        else:
                            pass
                            # await message.channel.send("can't/can not/unable to can")
                    else:
                        print("error 1")
                        print(messages[1][2:-1])
                        print(mentioned_members[0].id)
                else:
                    print(f"error 3: {len(messages)}")


@client.event
async def on_message_delete(message):
    channel = client.get_channel(channels["deleted-message-channel"])
    message_type = ""
    url = ""
    if len(message.attachments) != 0:
        url = message.attachments[0].url
        print(url)
        message_type = "image"
    if message_type == "image":

        files = []
        for file in message.attachments:
            fp = io.BytesIO()
            await file.save(fp)
            files.append(discord.File(fp, filename=file.filename, spoiler=file.is_spoiler()))

        print("image type")
        await channel.send(f"```{get_current_time()} | {message.channel.name} | {message.author.display_name}``` {message.content}")
        await channel.send(files=files)
    else:
        print(f"{get_current_time()} | {message.author.display_name}: {message.content}")
        await channel.send(f"```{get_current_time()} | {message.channel.name} | {message.author.display_name}``` {message.content}")


@client.event
async def on_member_join(member):
    # server = client.get_guild(servers["lewd-server"])
    c = 0
    for m in member.guild.members:
        if not m.bot:
            c += 1
    for channel in member.guild.channels:
        if channel.id == channels["welcum-channel"] or channel.id == channels["log-channel"]:
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
    # server = client.get_guild(servers["lewd-server"])
    for channel in member.guild.channels:
        if channel.id == channels["welcum-channel"] or channel.id == channels["log-channel"]:
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
async def on_member_update(before, after):
    channel = client.get_channel(channels["log-channel"])
    if not before.bot:
        if channel is not None:
            if after.status != before.status:
                print(f"[{get_current_time()} status changed]")
                print(f"-{before.nick} : {after.status}\n")
                emoji = ""
                if str(after.status) == "online":
                    emoji = "<:Nep_owo_LC:762586025402826793>"
                elif str(after.status) == "offline":
                    emoji = "<:Paimon_dead_LC:762586355817381888>"
                else:
                    emoji = "<:Kelly_angel_LC:762586163500154900>"
                if before.guild.id != 739864997865455626:
                    await channel.send(f"```{get_current_time()} --:-- [{after.status}] --:-- {before.display_name}```")
            elif after.activity != before.activity:
                if before.guild.id != 739864997865455626:
                    channel = client.get_channel(channels["channel-activity"])
                    await channel.send(f"```{get_current_time()} --:-- {before.display_name} : [{after.activity}]```")


@client.event
async def on_user_update(before, after):
    channel = client.get_channel(channels["user-channel"])
    if not before.bot:
        if channel is not None:
            if after.avatar != before.avatar:
                await channel.send(f"```{get_current_time()} --:-- {before.display_name} updated avatar```")
                await channel.send(f"{after.avatar_url}")

client.run(token)
