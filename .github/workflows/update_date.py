```python
import json
import re
from datetime import datetime

def update_tip_message_date(json_path="config.json"):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    today = datetime.now().strftime('%Y年%m月%d日')
    # 去掉月份和日期的前导零（例如 "06月" -> "6月"）
    today = re.sub(r'月0(\d)日', r'月\1日', today)
    today = re.sub(r'年0(\d)月', r'年\1月', today)

    old_date_pattern = r'\d{4}年\d{1,2}月\d{1,2}日'

    if 'tipMessage' in data:
        new_msg = re.sub(old_date_pattern, today, data['tipMessage'], count=1)
        data['tipMessage'] = new_msg
        print(f"日期已更新为: {today}")
    else:
        print("未找到 tipMessage 字段")

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    update_tip_message_date()
```
