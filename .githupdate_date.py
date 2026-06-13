import json
import re
from datetime import datetime

def update_tip_message_date(json_path="config.json"):
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"读取文件失败: {e}")
        return

    today = datetime.now().strftime('%Y年%m月%d日')
    # 去掉前导零
    today = re.sub(r'月0(\d)日', r'月\1日', today)
    today = re.sub(r'年0(\d)月', r'年\1月', today)

    # 更严格的日期匹配（四位年份+月+日，月/日可以是1-2位数字）
    date_pattern = r'\d{4}年\d{1,2}月\d{1,2}日'

    if 'tipMessage' not in data:
        print("错误：未找到 tipMessage 字段")
        return

    old_msg = data['tipMessage']
    match = re.search(date_pattern, old_msg)
    if not match:
        print(f"警告：tipMessage 中没有找到形如'2026年6月12日'的日期。当前内容开头：{old_msg[:50]}")
        return

    old_date = match.group(0)
    new_msg = re.sub(date_pattern, today, old_msg, count=1)
    data['tipMessage'] = new_msg

    print(f"找到旧日期: {old_date} -> 替换为: {today}")

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("config.json 已更新并保存")

if __name__ == "__main__":
    update_tip_message_date()
