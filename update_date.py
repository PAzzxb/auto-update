import json
from datetime import datetime

# 读取 config.json
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# 获取完整时间信息
now = datetime.now()
today = now.strftime('%Y年%m月%d日')
weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
weekday = weekdays[now.weekday()]
current_time = now.strftime('%H:%M:%S')

# 设置倒计时秒数
config['countdownSeconds'] = 8

# 显示完整信息（日期 + 星期 + 时间）
tip_message = f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    {today} {weekday}
    {current_time} 更新
    
    同步信息：每天凌晨起
    弹窗一遍十几秒钟
    返回即可查看同步最新动态！
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""

config['tipMessage'] = tip_message

# 写回文件
with open('config.json', 'w', encoding='utf-8') as f:
    json.dump(config, f, ensure_ascii=False, indent=4)

print(f"✅ 更新完成: {today} {weekday} {current_time}")
