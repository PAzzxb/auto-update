import json
from datetime import datetime

# 读取 config.json
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# 获取日期和星期（不获取时间）
now = datetime.now()
today = now.strftime('%Y年%m月%d日')
weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
weekday = weekdays[now.weekday()]

# 设置倒计时秒数和图片URL
config['countdownSeconds'] = 8
config['imageUrl'] = "https://img.cdn1.vip/i/6a2e4678af9f9_1781417592.webp"

# 消息内容：只显示日期和星期，没有时间
tip_message = tip_message = f"""
━━━━━━━━━━━━━━━━━━━━━━
        📅 {today} {weekday}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    ℹ️ 状态信息：每天凌晨起弹窗一遍
    ⏱️ 二十秒钟后自动关闭
    🔄 按键返回即可查看同步最新资源！
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

config['tipMessage'] = tip_message

# 写回文件
with open('config.json', 'w', encoding='utf-8') as f:
    json.dump(config, f, ensure_ascii=False, indent=4)

print(f"✅ 更新完成: {today} {weekday}")
