import json
from datetime import datetime

with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

today = datetime.now().strftime('%Y年%m月%d日')

config['countdownSeconds'] = 8
config['imageUrl'] = "https://img.cdn1.vip/i/6a2e4678af9f9_1781417592.webp"  # 👈 添加这一行

tip_message = f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    {today}
    
    同步信息：每天凌晨起
    弹窗一遍十几秒钟
    返回即可查看同步最新动态！
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""

config['tipMessage'] = tip_message

with open('config.json', 'w', encoding='utf-8') as f:
    json.dump(config, f, ensure_ascii=False, indent=4)

print(f"✅ 日期已更新: {today}")
