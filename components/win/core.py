import psutil

def get_cpu_usage():
    """
    获取CPU使用情况
    :return: 当前CPU使用率的百分比
    """
    cpu_usage = psutil.cpu_percent(interval=1)
    return cpu_usage

def get_memory_usage():
    """
    获取内存使用情况
    :return: 一个字典，包含总内存、已用内存和可用内存（单位：GB）
    """
    memory_info = psutil.virtual_memory()
    total_memory = memory_info.total / (1024 ** 3)  # 转换为GB
    used_memory = memory_info.used / (1024 ** 3)    # 转换为GB
    available_memory = memory_info.available / (1024 ** 3)  # 转换为GB
    return {
        "total_memory": total_memory,
        "used_memory": used_memory,
        "available_memory": available_memory
    }