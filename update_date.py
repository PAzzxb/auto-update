import json
from datetime import datetime

# 读取 config.json
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# 获取当前日期
today = datetime.now().strftime('%Y年%m月%d日')

# 设置倒计时秒数
config['countdownSeconds'] = 8

# 对齐修复 - 使用简单边框格式
tip_message = f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    {today}
    
    同步信息：每天凌晨起
    弹窗一遍十几秒钟
    返回即可查看同步最新动态！
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""

config['tipMessage'] = tip_message

# 写回文件
with open('config.json', 'w', encoding='utf-8') as f:
    json.dump(config, f, ensure_ascii=False, indent=4)

print(f"✅ 日期已更新: {today}")
print(f"✅ 倒计时秒数: {config['countdownSeconds']}秒")
