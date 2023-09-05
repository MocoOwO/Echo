try:
    from Builtin import eventclass, Action, CONFIG, Color
except:
    import sys
    import os

    sys.path.append(os.path.join(os.path.dirname(__file__), f'../../Builtin'))
    from Builtin import eventclass, Action, CONFIG, Color
import re
import requests
import json

PluginName = 'Echo'
VersionCode = "NumList"
Version = [0, 0, 1]
Developer = "Moco"

Host = CONFIG.Host

HaveReply = True
HaveLog = True


def IsReply(data: eventclass.Message):
    if isinstance(data.message, list):
        # array格式的消息,推荐
        pass
    else:
        pass
    msg = data.raw_message
    if re.match("/echo .+", msg):
        return True
    return False


def Reply(data: eventclass.Message, Host):
    msg = data.raw_message[6:]
    if isinstance(data, eventclass.GroupMessage):
        Action.SendMsg(msg=msg, type=data.message_type, Host=Host, id=data.group_id)
    if isinstance(data, eventclass.PrivateMessage):
        Action.SendMsg(msg=msg, type=data.message_type, Host=Host, id=data.user_id)
    Log(data, msg)


def Log(data, msg):
    if isinstance(data, eventclass.PrivateMessage):
        print(
            f"[MocoBot][Echo] 已完成来自好友 {data.sender['nickname']}({data.sender['user_id']}) 的ECHO请求:"
            f" {Color.color['bright_yellow'] + data.raw_message}{Color.color['reset']} -> {Color.color['bright_green'] + msg}")
    elif isinstance(data, eventclass.GroupMessage):
        d = requests.get(f"{Host}get_group_info?group_id={data.group_id}").text
        name = json.loads(d)['data']['group_name']
        print(f"[MocoBot][Echo] 已完成来自群 {name}({data.group_id}) 内 {data.sender['nickname']} "
              f"({data.sender['user_id']}) 的ECHO请求: {Color.color['bright_yellow'] + data.raw_message}{Color.color['reset']} -> {Color.color['bright_green'] + msg}")
