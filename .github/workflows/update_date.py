import json
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from collections import deque

# --- 配置 ---
MAX_LOG_LINES = 100  # 保留最近100条日志
WEEKDAY_MAP = {0: "星期一", 1: "星期二", 2: "星期三",
               3: "星期四", 4: "星期五", 5: "星期六", 6: "星期日"}

# --- 获取当前星期 ---
tz = ZoneInfo("Asia/Shanghai")
now = datetime.now(tz)
current_weekday = WEEKDAY_MAP[now.weekday()]
timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

# --- 处理 config.json ---
config_path = Path("config.json")
if config_path.exists():
    with open(config_path, "r", encoding="utf-8") as f:
        data = json.load(f)
else:
    data = {}

if data.get("last_weekday") == current_weekday:
    print("ℹ️ 星期未变，跳过更新。")
    exit(0)

data["last_weekday"] = current_weekday
with open(config_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# --- 更新日志（并自动裁剪） ---
log_path = Path("update.log")
new_entry = f"[{timestamp}] 更新星期为: {current_weekday}\n"

# 读取已有日志行（若存在）
lines = []
if log_path.exists():
    with open(log_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

# 追加新行
lines.append(new_entry)

# 若行数超过最大保留数，只保留最后 MAX_LOG_LINES 行
if len(lines) > MAX_LOG_LINES:
    lines = lines[-MAX_LOG_LINES:]

# 写回文件
with open(log_path, "w", encoding="utf-8") as f:
    f.writelines(lines)

print(f"✅ 星期已更新为: {current_weekday}")
print(f"📝 日志已保留最近 {len(lines)} 条（最大 {MAX_LOG_LINES} 条）")