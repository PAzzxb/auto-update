import json
from datetime import datetime
from zoneinfo import ZoneInfo

# 获取准确的北京时间
tz = ZoneInfo("Asia/Shanghai")
current_date = datetime.now(tz).strftime("%Y-%m-%d")

# 读取现有配置
try:
    with open("config.json", "r", encoding="utf-8") as f:
        data = json.load(f)
except FileNotFoundError:
    data = {}

# 仅当日期有变化时才更新，避免无意义提交
if data.get("last_update") == current_date:
    print("ℹ️ Date unchanged, skip update.")
    exit(0)

# 写入新日期
data["last_update"] = current_date
with open("config.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✅ Date updated to: {current_date}")
