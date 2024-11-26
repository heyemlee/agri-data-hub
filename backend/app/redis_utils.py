from redis import Redis
from .config import get_settings
import json
from datetime import datetime

settings = get_settings()
redis_client = Redis.from_url(settings.REDIS_URL, decode_responses=True)

LATEST_DATA_KEY = "latest_sensor_data"
SENSOR_DATA_STREAM = "sensor_data_stream"

def cache_sensor_data(data: dict):
    """缓存最新的传感器数据"""
    # 存储最新数据
    redis_client.set(
        LATEST_DATA_KEY,
        json.dumps(data),
        ex=300  # 5分钟过期
    )
    
    # 添加到时序数据流
    redis_client.xadd(
        SENSOR_DATA_STREAM,
        {
            "data": json.dumps(data)
        },
        maxlen=3600  # 保留最近一小时的数据
    )

def get_latest_data():
    """获取最新的传感器数据"""
    data = redis_client.get(LATEST_DATA_KEY)
    return json.loads(data) if data else None

def get_recent_data(count: int = 240):  # 默认一小时的数据(15秒间隔)
    """获取最近的传感器数据"""
    entries = redis_client.xrevrange(SENSOR_DATA_STREAM, count=count)
    return [json.loads(entry[1]["data"]) for entry in entries] 