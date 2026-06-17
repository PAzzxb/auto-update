import json
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path

# ----- 配置 -----
CONFIG_PATH = Path("config.json")
LOG_PATH = Path("update.log")
MAX_LOG_LINES = 100

# 可配置的图片 URL（建议通过环境变量或单独配置文件管理）
IMAGE_URL = "https://img.cdn1.vip/i/6a2e4678af9f9_1781417592.webp"
COUNTDOWN_SECONDS = 8

# 星期映射
WEEKDAY_MAP = {
    0: "星期一", 1: "星期二", 2: "星期三",
    3: "星期四", 4: "星期五", 5: "星期六", 6: "星期日"
}

def get_beijing_time():
    """获取北京时间（带时区）"""
    return datetime.now(ZoneInfo("Asia/Shanghai"))

def get_current_date_weekday(dt):
    """返回 (日期字符串, 星期字符串)"""
    date_str = dt.strftime("%Y年%m月%d日")
    weekday = WEEKDAY_MAP[dt.weekday()]
    return date_str, weekday

def build_tip_message(date_str, weekday):
    """生成提示消息"""
    return f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━
🌟 温馨提醒
📅 {date_str} {weekday}
ℹ️ 状态：每日凌晨首次显示
⏱️ 20秒后自动关闭
🔄 按返回键刷新最新资源
━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

def append_log(message):
    """追加日志并自动裁剪"""
    lines = []
    if LOG_PATH.exists():
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()
    lines.append(message + "\n")
    if len(lines) > MAX_LOG_LINES:
        lines = lines[-MAX_LOG_LINES:]
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        f.writelines(lines)

def main():
    # 获取当前北京时间
    now = get_beijing_time()
    date_str, weekday = get_current_date_weekday(now)
    date_only = now.strftime("%Y-%m-%d")   # 仅日期，用于日志

    # 如果 config.json 不存在，则创建空字典
    if not CONFIG_PATH.exists():
        config = {}
    else:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config = json.load(f)

    # 检查日期是否变化（避免重复写入）
    if config.get("tipDate") == date_str:
        print(f"ℹ️ 日期未变 ({date_str})，跳过更新。")
        exit(0)

    # 更新配置
    config["countdownSeconds"] = COUNTDOWN_SECONDS
    config["imageUrl"] = IMAGE_URL
    config["tipMessage"] = build_tip_message(date_str, weekday)
    config["tipDate"] = date_str   # 记录本次更新的日期

    # 写入 config.json
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=4)

    # 写入日志（只记录日期，不含时间）
    log_entry = f"[{date_only}] 更新每日提示 → {date_str} {weekday}"
    append_log(log_entry)

    print(f"✅ 更新完成: {date_str} {weekday}")
    print(f"📝 日志已记录 (保留最近 {MAX_LOG_LINES} 条)")

if __name__ == "__main__":
    main()
