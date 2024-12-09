from utils.llm import qianfan_invoke
from utils.logger import loginfo, logerror
from utils.prompt import PROMPT_SUMMARY_TOOLS, PROMPT_CHECK_TOOL
from components.win.volume import set_volume
from components.win.core import get_cpu_usage, get_memory_usage
import json

FUNCTIONS = [
    {
        "name": "set_volume",
        "description": "在0-100的区间内，调整电脑音量大小，不调节亮度",
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
        "name": "cpu_info",
        "description": "查看任何和CPU有关的信息，包括CPU的使用率、型号、核数等",
        "parameters": {"type": "object", "properties": {}, "required": []},
        "responses": {},
    },
    {
        "name": "get_memory_usage",
        "description": "仅获取电脑的内存使用率，不包含其他任何电脑信息",
        "parameters": {"type": "object", "properties": {}, "required": []},
        "responses": {},
    },
]

def check_if_tool(msg: str) -> bool:
    func_list = ""
    counter = 0
    for function in FUNCTIONS:
        counter += 1
        func_list += f"{counter}. {function['name']}: {function['description']}\n"
    result = qianfan_invoke(
        PROMPT_CHECK_TOOL.format(
            functions=func_list,
            msg=msg
        )
    )
    loginfo(f"check_if_tool llm result: {result}")
    if result == "Y" or result.startswith("Y"):
        return True
    return False

def use_tool(msg: str) -> str:
    result = qianfan_invoke(msg, tools=FUNCTIONS)
    if isinstance(result, dict):
        function_name = result.get("name", "")
        parameters = json.loads(result.get("arguments", {}))
        # 调整音量
        if function_name == "set_volume":
            volume = parameters.get("volume", 0)
            if 0 <= volume <= 100:
                if set_volume(volume):
                    return f"音量已调整至{volume}"
            return "音量调整失败"
        # CPU信息
        elif function_name == "cpu_info":
            return get_cpu_usage()
        # 内存使用率
        elif function_name == "get_memory_usage":
            return get_memory_usage()
        # 其他工具
        else:
            return "未找到对应的工具"
    else:
        return result

def summary_tool_result(msg: str, result: str) -> str:
    reply = qianfan_invoke(
        PROMPT_SUMMARY_TOOLS.format(
            question=msg,
            result=result
        )
    )
    return reply