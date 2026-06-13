import json
import re
from datetime import datetime

with open('config.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

today = datetime.now().strftime('%Y年%m月%d日')
today = re.sub(r'月0(\d)日', r'月\1日', today)
today = re.sub(r'年0(\d)月', r'年\1月', today)

date_pattern = r'\d{4}年\d{1,2}月\d{1,2}日'
if 'tipMessage' in data:
    match = re.search(date_pattern, data['tipMessage'])
    if match:
        old_date = match.group(0)
        data['tipMessage'] = re.sub(date_pattern, today, data['tipMessage'], count=1)
        print(f"日期已更新: {old_date} → {today}")
    else:
        print("未找到日期格式")
else:
    print("没有 tipMessage 字段")

with open('config.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)