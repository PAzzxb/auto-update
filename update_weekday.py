import json
import datetime
import re
from zoneinfo import ZoneInfo   # Python 3.9+ 标准库

# 1. 获取北京时间
now = datetime.datetime.now(ZoneInfo('Asia/Shanghai'))
weekdays = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
weekday_cn = weekdays[now.weekday()]
full_time = now.strftime("%Y-%m-%d %H:%M:%S") + f" {weekday_cn}"

# 2. 更新 config.json
try:
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    config = {}
config['last_weekday'] = weekday_cn
config['last_update'] = full_time
with open('config.json', 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

# 3. 追加 update.log
with open('update.log', 'a', encoding='utf-8') as f:
    f.write(f"{full_time} 更新完成\n")

# 4. 更新 README.md（替换占位符）
try:
    with open('README.md', 'r', encoding='utf-8') as f:
        readme = f.read()
    new_readme = re.sub(r'<!-- UPDATE_TIME -->', full_time, readme)
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(new_readme)
except FileNotFoundError:
    pass

print(f"✅ 更新时间：{full_time}")
