import psutil
import platform


def get_cpu_usage():
    cpu_info = {
        "cpu_stats": psutil.cpu_stats()._asdict(),
        "cpu_times": psutil.cpu_times()._asdict(),
        "cpu_count_logical": psutil.cpu_count(logical=True),
        "cpu_count_physical": psutil.cpu_count(logical=False),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "cpu_name": platform.processor()
    }
    return cpu_info

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
        "total_memory": f"{total_memory} GB",
        "used_memory": f"{used_memory} GB",
        "available_memory": f"{available_memory} GB"
    }