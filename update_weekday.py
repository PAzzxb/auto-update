import re
import datetime
import pytz

# 1. 获取当前北京时间
beijing_tz = pytz.timezone('Asia/Shanghai')
now = datetime.datetime.now(beijing_tz)

# 格式化你想显示的内容（示例："2026-06-29 星期一 14:30:25"）
formatted_time = now.strftime("%Y-%m-%d %A %H:%M:%S")
# 如果你想用中文星期，可以手动映射（因为strftime英文环境下输出英文）
weekdays = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
weekday_cn = weekdays[now.weekday()]
final_text = f"{now.strftime('%Y-%m-%d')} {weekday_cn} {now.strftime('%H:%M:%S')}"

# 2. 读取 README.md
with open('README.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 3. 替换占位符（在 README 中写一个标记，比如 <!-- UPDATE_TIME -->）
# 假设你的 README 里有这行： `上次自动同步时间：<!-- UPDATE_TIME -->`
new_content = re.sub(
    r'<!-- UPDATE_TIME -->',  # 查找这个注释标记
    final_text,               # 替换成计算好的时间
    content
)

# 4. 写回 README.md
with open('README.md', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"README 时间已更新为：{final_text}")
