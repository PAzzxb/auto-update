import json
from datetime import datetime
from zoneinfo import ZoneInfo

# 获取当前星期几（英文）
tz = ZoneInfo("Asia/Shanghai")
current_weekday = datetime.now(tz).strftime("%A")

# 读取现有配置（若文件不存在则创建空字典）
try:
    with open("config.json", "r", encoding="utf-8") as f:
        data = json.load(f)
except FileNotFoundError:
    data = {}

# 仅当星期有变化时才更新，避免重复写入
if data.get("last_weekday") == current_weekday:
    print("ℹ️ Weekday unchanged, skip update.")
    exit(0)

# 写入新的星期
data["last_weekday"] = current_weekday
with open("config.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✅ Weekday updated to: {current_weekday}")