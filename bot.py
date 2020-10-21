import discord
from datetime import datetime
import requests
import json
import random
from pytz import timezone


def get_current_time():
    fmt = '%I:%M:%S %p'
    eastern = timezone('Asia/Jakarta')
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
    return random.choice(gifs)


token = "NzU4MTUwMDU3MzcwNDUxOTc4.X2qwQw.f4hIHfMr42IwoJkl8XwZDU4JevU"
intents = discord.Intents.all()
client = discord.Client(intents=intents)

servers = {
    "lewd-server": 757865220604690443,
    "test-server": 739864997865455626
}
channels = {
    "log-channel": 739864997865455629,
    "bbyLewd-channel": 762607426582085642
}

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
    now = datetime.now()
    acts = ["hug", "slap", "kiss", "fuck", "lick", "snipe", "kill", "hide", "sneak"]

    if message.author.id == bot_id:
        pass
    elif str(message.content).lower() == "i":
        emojis = message.guild.emojis
        await message.channel.send(f"{get_current_time()} sent emoji:  {emojis[0]}")
    else:
        messages = str(message.content).lower().split()
        mentioned_members = message.mentions
        print("\n======= new message")
        print(f"{get_current_time()} | {message.author.display_name}: {message.content}")
        # print(f"author   : {message.author.display_name}")
        # print(f"mentioned: {mentioned_members} | {len(mentioned_members)}")
        # print(f"message  : {message.content} | {len(messages)}")
        # print(f"messages : {messages}")

        if len(mentioned_members) > 1 or len(mentioned_members) == 0:
            pass
        else:
            if len(messages) > 1:

                if messages[1][2:-1] == str(mentioned_members[0].id):
                    embed = discord.Embed(
                        title=f"{message.author.display_name} {messages[0]} {mentioned_members[0].display_name}",
                        description="im confused",
                        color=0x00ff00)
                    embed.set_image(url=get_gif(f"anime {messages[0]}"))
                    await message.channel.send(embed=embed)
                else:
                    print("error 1")
                    print(messages[1][2:-1])
                    print(mentioned_members[0].id)
            else:
                print(f"error 3: {len(messages)}")


@client.event
async def on_member_join(member):
    # server = client.get_guild(servers["lewd-server"])
    for channel in member.guild.channels:
        if channel.id == channels["bbyLewd-channel"] or channel.id == channels["log-channel"]:
            description = random.choice(
                ["who are you?",
                 "free whisshy whooshy for a week",
                 f"say hi to {member.display_name}",
                 "annyeong!"]
            )
            embed = discord.Embed(
                title=f"{member.display_name} joined the server",
                description=description,
                color=0x00ff00)
            embed.set_image(url=get_gif(gif_keys["server-joined"]))
            print("\n======= server update")
            print(f"{member.display_name} joined the server")
            await channel.send(embed=embed)


@client.event
async def on_member_remove(member):
    # server = client.get_guild(servers["lewd-server"])
    for channel in member.guild.channels:
        if channel.id == channels["bbyLewd-channel"] or channel.id == channels["log-channel"]:
            description = random.choice(
                ["bye bye",
                 "yay",
                 f"feel lonely",
                 "shoo shoo"]
            )
            embed = discord.Embed(
                title=f"{member.display_name} left the server!",
                description=description,
                color=0x00ff00)
            embed.set_image(url=get_gif(gif_keys["server-left"]))
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
                    await channel.send(f"{get_current_time()} --:-- [{after.status}] --:-- {before.display_name}")


client.run(token)
