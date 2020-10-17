import discord
import random
from datetime import datetime
import requests, json
apikey = "LIVDSRZULELA"  # test value
lmt = 1

# our test search
search_term = "excited"

# get the top 8 GIFs for the search term
r = requests.get(f"https://api.tenor.com/v1/search?q={search_term}&key={apikey}&limit={lmt}")

if r.status_code == 200:
    # load the GIFs using the urls for the smaller GIF sizes
    top_8gifs = json.loads(r.content)
    # print(top_8gifs)
    # print(len(top_8gifs))
    # print(top_8gifs["weburl"])
    # print(top_8gifs["results"])
    # print(top_8gifs["next"])


else:
    top_8gifs = None



def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


l = "https://discordapp.com/oauth2/authorize?client_id=758150057370451978&scope=bot&permissions=0"
token = read_token()
client = discord.Client()

short_memory = [
]
morning_greeting = {}


@client.event
async def on_member_update(before, after):
    now = datetime.now()
    if after.status != before.status:
        print("==status changed==")
        print(f"{before.nick} : {after.status}")

    if str(before.id) == "736028616764424195" or str(before.id) == "762590005314715659":
        new_nick = after.nick
        old_nick = before.nick
        if new_nick:
            current_time = now.strftime("%H:%M:%S")
            print(f"{current_time}")
            last = old_nick
            print(new_nick)
            if last:
                if new_nick != last:
                    await after.edit(nick=last)
            else:
                await after.edit(nick="verified uke")


@client.event
async def on_message(message):
    # server_owner = message.guild.owner

    sender = message.author
    msg = str(message.content).lower()

    if str(sender.id) != "758150057370451978":
        print("--received new message--")
        print(f"auth id: {sender.id}")
        print(f"sender : {sender.display_name}")
        print(f"message: {msg}")
        random_greeting = ["hi", "hello", "hiya", "annyeong", "hiya!"]
        if msg[:5] == "ohayo":
            sender_name = str(sender.display_name)
            if sender_name not in morning_greeting:
                morning_greeting[sender_name] = [msg, 1]
                answers = ["ohayoo", "ohayouu",
                           f"{sender_name} ohayoo!", f"{sender_name} ohayo~",
                           f"{sender_name} ohayou"]
                answer = random.choice(answers)
                print(f"answer : {answer}")
                await message.channel.send(answer)
            else:
                if morning_greeting[sender_name][1] < 2:
                    await message.channel.send("are you lonely?")
                elif morning_greeting[sender_name][1] == 2:
                    answers = ["don't try me please", "don't spam!",
                               "don't spam please!", "you don't try"]
                    answer = random.choice(answers)
                    print(f"answer : {answer}")
                    await message.channel.send(answer)
                elif morning_greeting[sender_name][1] == 3:
                    answers = ["okai i'm tired", "you hurting me",
                               "mama help!", "good bye :'(", "//whipeu whipeu//"]
                    answer = random.choice(answers)
                    print(f"answer : {answer}")
                    await message.channel.send(answer)
                else:
                    await message.channel.send(f"[{sender_name}] spam [{morning_greeting[sender_name][1]}times]")
                morning_greeting[sender_name][1] += 1

        elif msg[:6] == "mornin":

            sender_name = str(sender.display_name)
            if sender_name not in morning_greeting:
                morning_greeting[sender_name] = [msg, 1]
                answers = ["morning", "gud morning!",
                           f"gud morning {sender_name}!", f"gud moaning {sender_name}",
                           f"good MOANing {sender_name}"]
                answer = random.choice(answers)
                print(f"answer : {answer}")
                await message.channel.send(answer)
            else:
                if morning_greeting[sender_name][1] < 2:
                    await message.channel.send("Hi")
                elif morning_greeting[sender_name][1] == 2:
                    answers = ["don't try me please", "don't spam!",
                               "don't spam please!", "you don't try"]
                    answer = random.choice(answers)
                    print(f"answer : {answer}")
                    await message.channel.send(answer)
                elif morning_greeting[sender_name][1] == 3:
                    answers = ["okai i'm tired", "you hurting me",
                               "mama help!", "good bye :'(", "//whipeu whipeu//"]
                    answer = random.choice(answers)
                    print(f"answer : {answer}")
                    await message.channel.send(answer)
                else:
                    await message.channel.send(f"[{sender_name}] spam [{morning_greeting[sender_name][1]}times]")
                morning_greeting[sender_name][1] += 1

        elif msg[:8] == "eli kill":
            got_killed = message.mentions
            if got_killed[0].id == "747420254392811610" or "532366409531916288":
                await message.channel.purge(limit=1)
                embed = discord.Embed(
                    title=f"{sender.display_name} trying to kill mama",
                    description="mama under my protection",
                    color=0x00ff00)
                embed.set_image(url="https://tenor.com/view/genshin-impact-paimon-gif-18640817")
                await message.channel.send(embed=embed)
            # await message.channel.send(f"Eli kill @{sender}")

        elif msg in random_greeting:
            temp = random.choice([sender.display_name, ""])
            answer = f"{random.choice(random_greeting)} {temp}!"
            await message.channel.send(answer)

        else:
            pass


print("running...")
client.run(token)

#
#

#
#
# banned_users = []
#
#
# @client.event
# async def on_message(message):
#
#     author = str(message.author)
#     msg = str(message.content).lower()
#     print(f"user:{author}")
#     print(f"msg :{msg}")
#     print("list banned user:")
#     for user in banned_users:
#         print(user, len(user))
#     if author != "bbyLewd#2503":
#         # print(message.guild.owner.display_name)
#         if str(message.author.id) in banned_users:
#             print(f"{author} sent message and got deleted")
#             await message.channel.purge(limit=1)
#         else:
#             if msg[0:4].lower() == "hug ":
#                 user = str(msg[6:-1])
#                 banned_users.append(user)
#                 print(f"msg :{msg}")
#                 print(f"banned user :{user}")
#                 print(len(user))
#                 print(f"{author} was added to banned list")
#                 print(banned_users)
#                 await message.channel.send(f"{user} added")
#             else:
#                 if msg == "hi":
#                     await message.channel.send(f"hi")
#
#             print("========")
#
#
