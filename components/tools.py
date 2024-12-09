from utils.llm import qianfan_invoke
from utils.logger import loginfo, logerror
from components.win.volume import set_volume
from pprint import pprint
import json

FUNCTIONS = [
    {
        "name": "set_volume",
        "description": "在0-100的区间内，调整电脑音量大小",
        "parameters": {
            "type": "object",
            "properties": {
                "volume": {
                    "type": "integer",
                    "description": "要调整至的音量大小，取值范围为0-100",
                }
            },
            "required": ["volume"],
        },
        "responses": {},
    }
]

def use_tool(function_call: dict) -> str:
    function_name = function_call.get("name", "")
    parameters = json.loads(function_call.get("arguments", {}))
    # 调整音量
    if function_name == "set_volume":
        volume = parameters.get("volume", 0)
        if 0 <= volume <= 100:
            if set_volume(volume):
                return f"音量已调整至{volume}"
        return "音量调整失败"
    # 其他工具
    else:
        return "未找到对应的工具"

def invoke_to_use_tool(query: str) -> str:
    response = qianfan_invoke(query, tools=FUNCTIONS)
    if isinstance(response, dict):
        loginfo(f"Function Calling: {response}")
        function_name = response.get("name", "")
        parameters = json.loads(response.get("arguments", {}))
        # 调整音量
        if function_name == "set_volume":
            volume = parameters.get("volume", 0)
            if 0 <= volume <= 100:
                if set_volume(volume):
                    return f"音量已调整至{volume}"
            return "音量调整失败"
        # 其他工具
        else:
            return "未找到对应的工具"
    else:
        return ""


if __name__ == "__main__":
    msg = input("请输入指令：")
    print(invoke_to_use_tool(msg))