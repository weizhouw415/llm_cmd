import qianfan, json, requests, os
from openai import OpenAI

log_info = print
log_error = print

def usr_msg(msg: str) -> dict:
    return {"role": "user", "content": msg}

def ai_msg(msg: str) -> dict:
    return {"role": "assistant", "content": msg}

def sys_msg(msg: str) -> dict:
    return {"role": "system", "content": msg}


def openai_invoke(msg: str, system: str = "", functions: list[dict] = None) -> str:
    client = OpenAI(
        api_key=os.getenv("OPENAI_SK"),
        base_url=os.getenv("OPENAI_BASE_URL")
    )

    messages = []
    if system:
        messages.append(sys_msg(system))
    messages.append(usr_msg(msg))

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        functions=functions,
    )
    answer = completion.choices[0].dict()
    # return answer.get("message", {}).get("content", "")
    return answer


def qwen_vllm_invoke(msg: str, system: str = "") -> str:
    url = "https://qwen25-7b-test.baiying.com.cn/v1/chat/completions"
    params = {
        "model": "qwen2.5",
        "top_p": 0.9,
        "temperature": 0.01,
        "stream": False
    }

    messages = [sys_msg(system), usr_msg(msg)] if system else [usr_msg(msg)]
    params["messages"] = messages
    response = requests.post(url, json=params)
    result_dict = json.loads(response.text)
    content = result_dict["choices"][0]["message"]["content"]
    return content


def openai_ollama_generate(msg: str, model: str = "qwen2.5:latest", system: str = None, tools: list[dict] = None):
    client = OpenAI(
        api_key="none", 
        base_url="http://localhost:11434/v1"
    )

    messages = []
    if system is not None:
        messages.append(sys_msg(system))
    messages.append(usr_msg(msg))

    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
    )
    answer = completion.choices[0].dict()
    return answer.get("message", {}).get("content", "")


def qianfan_invoke(msg: str, system: str = None, tools: dict = None) -> str | dict:
    chat_comp = qianfan.ChatCompletion(model="ERNIE-4.0-Turbo-8K")
    resp = chat_comp.do(
        messages=[usr_msg(msg)], 
        top_p=0.9, 
        temperature=0.01, 
        penalty_score=1.0,
        disable_search=True,
        functions=tools,
        system=system
    )
    if resp.get("function_call"):
        return resp.get("function_call")
    else:
        return resp.get("result", "")


def qianfan_stream(msg_list: list[dict], functions: list[dict] = [], system_msg: str = None, ):
    try:
        chat_comp = qianfan.ChatCompletion(model="ERNIE-4.0-8K")
        resp = chat_comp.do(
            messages=msg_list, 
            top_p=0.9, 
            temperature=0.01, 
            penalty_score=1.0,
            stream=True,
            functions=functions,
            system=system_msg
        )
        check_func_call = True
        for chunk in resp:
            result = chunk.get("result", "")
            if not result and check_func_call:
                log_info("function calling")
                function_call = chunk.get("function_call", "")
                log_info(function_call)
                if not isinstance(function_call, dict):
                    try:
                        function_call = json.loads(function_call)
                    except Exception as e:
                        log_error(f"qianfan_stream function call error: {e}")
                        function_call = {}
                    log_info(f"qianfan_stream function call: {function_call}")
                yield function_call
            else:
                if check_func_call:
                    check_func_call = False
                yield result
        return
    except Exception as e:
        log_error("llm chat error: %s" % e)
        return ""
