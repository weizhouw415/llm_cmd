from utils.llm import qianfan_invoke
from utils.logger import loginfo, logerror
from utils.prompt import PROMPT_SUMMARY_TOOLS
from components.win.volume import set_volume
from components.win.core import get_cpu_usage, get_memory_usage
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
    },
    {
        "name": "get_cpu_usage",
        "description": "获取电脑的CPU使用率",
        "parameters": {"type": "object", "properties": {}, "required": []},
        "responses": {},
    },
    {
        "name": "get_memory_usage",
        "description": "获取电脑的内存使用率",
        "parameters": {"type": "object", "properties": {}, "required": []},
        "responses": {},
    },
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
    elif function_name == "get_cpu_usage":
        return get_cpu_usage()
    elif function_name == "get_memory_usage":
        return get_memory_usage()
    # 其他工具
    else:
        return "未找到对应的工具"
    

def summary_tool_result(msg: str, result: str) -> str:
    reply = qianfan_invoke(
        PROMPT_SUMMARY_TOOLS.format(
            question=msg,
            result=result
        )
    )
    return reply