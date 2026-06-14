import json
from datetime import datetime

with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# 更新日期字段
today = datetime.now().strftime('%Y年%m月%d日')
config['lastUpdateDate'] = today

# 如果 tipMessage 也需要包含日期，可以动态生成
config['tipMessage'] = f"{today}\n同步信息：每天凌晨起\n弹窗一遍十几秒钟\n返回即可查看同步最新动态!"

with open('config.json', 'w', encoding='utf-8') as f:
    json.dump(config, f, ensure_ascii=False, indent=4)

print(f"✅ Updated to: {today}")
