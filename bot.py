import discord
from datetime import datetime


token = "NzU4MTUwMDU3MzcwNDUxOTc4.X2qwQw.f4hIHfMr42IwoJkl8XwZDU4JevU"
client = discord.Client()

servers = {
    "lewd-server": 757865220604690443,
    "test-server": 739864997865455626
}
channels = {
    "log-channel": 739864997865455629
}

bot_id = 758150057370451978
member_id = [736028616764424195, 762590005314715659]


@client.event
async def on_ready():
    print(f"logged in as {client.user}\n")


@client.event
async def on_message(message):
    now = datetime.now()
    if message.author.id == bot_id:
        pass
    elif str(message.content).lower() == "hi":
        await message.channel.send("hello")
        await message.channel.send(f"{now.strftime('%H:%M:%S')} -- hi")
    # print(test_server.id)
    # print(message.channel)


@client.event
async def on_member_update(before, after):
    now = datetime.now()
    channel = client.get_channel(channels["log-channel"])
    await channel.send("test")
    await channel.send(channel)
    # if channel is not None:
    #     if after.status != before.status:
    #         print(f"[{now.strftime('%H:%M:%S')} status changed]")
    #         print(f"-{before.nick} : {after.status}\n")
    #         await channel.send(f"{now.strftime('%H:%M:%S')} ---:--- [{after.status}] {before.nick}")

client.run(token)
