import json
from datetime import datetime
from zoneinfo import ZoneInfo

# 中文星期映射
WEEKDAY_MAP = {
    0: "星期一", 1: "星期二", 2: "星期三",
    3: "星期四", 4: "星期五", 5: "星期六", 6: "星期日"
}

# 获取当前北京时间对应的中文星期
tz = ZoneInfo("Asia/Shanghai")
current_weekday = WEEKDAY_MAP[datetime.now(tz).weekday()]

# 读取现有配置（若文件不存在则创建空字典）
try:
    with open("config.json", "r", encoding="utf-8") as f:
        data = json.load(f)
except FileNotFoundError:
    data = {}

# 仅当星期有变化时才更新，避免重复写入
if data.get("last_weekday") == current_weekday:
    print("ℹ️ 星期未变，跳过更新。")
    exit(0)

# 写入新的星期
data["last_weekday"] = current_weekday
with open("config.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✅ 星期已更新为: {current_weekday}")