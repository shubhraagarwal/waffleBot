import discord
import requests
import json
import datetime


my_secret = 'OTcxMDEyOTcwNDY3NDUwODgw.YnEUTA.dj0j4N2SWFwVWSfET8N7rLkCF9I'
client = discord.Client()

def get_syrups(author):
    response = requests.get("http://localhost:3000/api/v1/users/getAllUser")
    json_data = json.loads(response.text)
    resp = ''
    for i in json_data:
        if i['discord_id'] == author:
            resp = i['syrups']
    return (resp)

def get_winners():
    response = requests.get("http://localhost:3000/api/v1/users/getAllWinner")
    json_dat = json.loads(response.text)
    nu = []
    for i in range(0,10):
        nu.append(json_dat[0]['discord_id'+str(i)])
    return (nu)

def get_gift(author):
    response = requests.get("http://localhost:3000/api/v1/users/getAllUser")
    json_data = json.loads(response.text)
    for i in json_data:
        if i['discord_id'] == author:
            if i['syrups'] < 8:
                return ('Do not have sufficient syrups')
            else:
                data = {
                    "walletAddress": i["walletAddress"],
                    "discord_id": i["discord_id"],
                    "syrups":  (i['syrups']) - 8
                }
                response = requests.post('http://localhost:3000/api/v1/users/enterWaffle', json=data)
                print(json.loads(response.text))
                # print(data)
                return ("whitelisted")
    return ("Your Account is  Not linked with us")

def get_time(author):
    response = requests.get("http://localhost:3000/api/v1/users/getAllUser")
    json_data = json.loads(response.text)
    nxtDate = ""
    for i in json_data:
        if i['discord_id'] == author:
            jstime = i['entryTime']
            dt = datetime.datetime.fromtimestamp(jstime)
            date_1 = datetime.datetime.strptime(str(dt), "%Y-%m-%d %H:%M:%S")
            end_date = date_1 + datetime.timedelta(days=1)
            nxtDate = end_date
    return (nxtDate)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$s'):
        usersyrups = get_syrups(str(message.author))
        await message.channel.send(usersyrups)

    if message.content.startswith('$w'):
        winner = get_winners()
        # for i in range(0,10):
        await message.channel.send("```Winner List\n\n"+"1 -> "+winner[0]+"\n2 -> "+winner[1]+"\n3 -> "+winner[2]+"\n4 -> "+winner[3]+"\n5 -> "+winner[4]+"\n6 -> "+winner[5]+"\n7 -> "+winner[6]+"\n8 -> "+winner[7]+"\n9 -> "+winner[8]+"\n10 -> "+winner[9]+"```")

    if message.content.startswith('$t'):
        nexttime = get_time(str(message.author))
        await message.channel.send(nexttime)

    if message.content.startswith('$g'):
        gift = get_gift(str(message.author))
        await message.channel.send(gift)

    if message.content.startswith('$help'):
        await message.channel.send(
            "**Commands \n 1. $s - for syrups\n 2. $w - for winners list \n 3. $t - Nnext time \n 4. $g - for gift**")

client.run(my_secret)

