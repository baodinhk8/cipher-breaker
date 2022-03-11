import websocket
import json
import threading
import time
import requests
import os


def send_json_request(ws, request):
    ws.send(json.dumps(request))


def receive_json_response(ws):
    response = ws.recv()
    if response:
        return json.loads(response)


def heartbeat(interval, ws):
    print("heartbeat begin")
    while True:
        time.sleep(interval)
        heartbeatJSON = {
            "op": 1,
            "d": "null"
        }
        send_json_request(ws, heartbeatJSON)
        print("Heartbeat sent")


ws = websocket.WebSocket()
ws.connect("wss://gateway.discord.gg/?v=6&encording=json")
event = receive_json_response(ws)

heartbeat_interval = event['d']['heartbeat_interval']/1000
threading._start_new_thread(heartbeat, (heartbeat_interval, ws))

token = "OTUwMzExMTUxMTc3MTkxNDU2.YiXHDg.lVO7l0IeKOVw0rXrFYDOlJRR9vY"

payload = {
    "op": 2,
    "d": {
        "token": token,
        "properties": {
            "$os": "windows",
            "$browser": "chrome",
            "$device": "pc"
        }
    }
}

header = {
    'authorization': token,
}

send_json_request(ws, payload)

while True:
    event = receive_json_response(ws)

    try:
        username = event['d']['author']['username']
        content = event['d']['content']
        channel_id = event['d']['channel_id']

        f = open("log.csv", "a")
        f.write(channel_id+","+username+","+content+"\n")
        f.close()

        if".bfattack" in content:
            for i in range(1000000001):
                if i % 100000000 == 0:
                    message = "Trying " + \
                        str(i)+" times. Result in the .result command"
                    r = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", headers=header, data={
                        "content": message})

        if ".checkalpha" in content:
            alpha = "abcdefghijklmnopqrstuvwxyz"
            content = content.lower()
            a = content.split("$")

            check = 1
            mis = "Missing char is : "

            for char in alpha:
                for cchar in a[1]:
                    if(char == cchar):
                        check = 0
                if(check):
                    mis += (char+" ")
                check = 1
            r = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", headers=header, data={
                "content": str(mis)})

        if ".decode2" in content:
            content = content.lower()
            a = content.split("$")
            dc = []
            arr = []
            for char in a[1]:
                if char == " ":
                    arr.append(dc)
                    dc = []
                else:
                    dc.append((ord(char)-ord('a')+1))
            lst = []
            for i in a[2]:
                lst.append(int(i))

            x = 0
            new_dc = []
            new_arr = []
            for i in arr:
                for j in i:
                    try:
                        new_dc.append(j-lst[x])
                        x += 1
                    except:
                        x = 0
                        new_dc.append(j-lst[x])
                        x += 1
                new_arr.append(new_dc)
                new_dc = []

            s = ""

            for i in new_arr:
                for j in i:
                    try:
                        s += chr(j+ord('a')-1)
                    except:
                        s += "?"
                s += " "

            r = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", headers=header, data={
                "content": str(s)})

        elif ".decode" in content:
            content = content.lower()
            a = content.split("$")
            dc = []
            arr = []
            for char in a[1]:
                if char == " ":
                    arr.append(dc)
                    dc = []
                else:
                    dc.append((ord(char)-ord('a')+1))
            print(content, a, dc)
            r = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", headers=header, data={
                "content": str(arr)})

        if username == "i have no brain" and content == ".log":
            files = {
                "file": ("./log.csv", open("./log.csv", 'rb'))
            }

            r = requests.post(
                f"https://discord.com/api/v9/channels/{channel_id}/messages", headers=header, files=files)
        elif username == "i have no brain" and content == ".status":
            r = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", headers=header, data={
                "content": "Looking good, if I can survive until 1/4, this method will work fine, discord forget to fix bug, hopefully :D"})
        elif username == "i have no brain" and content == ".clear":
            os.remove("log.csv")
            f = open("log.csv", "a")
            f.write("channel_id,author,message_content\n")
            f.close()
            r = requests.post(
                f"https://discord.com/api/v9/channels/{channel_id}/messages", headers=header, data={"content": "Done!"})

        op_code = event("op")
        if op_code == 11:
            print("heartbeat received")
    except Exception as e:
        pass
