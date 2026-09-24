import json
import datetime
import re
import urllib.request
from zoneinfo import ZoneInfo   # Python 3.9+ 内置，无需安装

# 1. 获取北京时间
now = datetime.datetime.now(ZoneInfo('Asia/Shanghai'))
weekdays = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
weekday_cn = weekdays[now.weekday()]
full_time = now.strftime("%Y-%m-%d %H:%M:%S") + f" {weekday_cn}"

# 1.5 获取必应每日一图（小尺寸 640x360，约 40KB），失败则保留原图
def fetch_bing_image():
    try:
        api = "https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=zh-CN"
        req = urllib.request.Request(api, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.loads(r.read().decode("utf-8"))
        urlbase = data["images"][0]["urlbase"]          # 形如 /th?id=OHR.xxxx
        # 640x360 固定尺寸后缀（实测可用、体积小）
        return f"https://cn.bing.com{urlbase}_640x360.jpg"
    except Exception as e:
        print(f"⚠️ 获取必应每日图失败：{e}")
        return None

# 2. 更新 config.json（覆盖写入，永远只保留最新1条）
try:
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    config = {}
config['last_weekday'] = weekday_cn
config['last_update'] = full_time
# 更新提示内容中的日期
new_date_str = now.strftime("%Y年%m月%d日")
config['tipDate'] = new_date_str
config['tipMessage'] = (
    "\n━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "🌟 温馨提醒\n"
    f"📅 {new_date_str} {weekday_cn}\n"
    "ℹ️ 状态：每日首次显示\n"
    "⏱️ 20秒后自动关闭\n"
    "🔄 按返回键刷新最新资源\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
)
# 每日一图：必应壁纸，取到才更新
bing = fetch_bing_image()
if bing:
    config['imageUrl'] = bing
    print(f"🖼️ 今日图片：{bing}")
with open('config.json', 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

# 3. 更新 update.log（自动保留最后 100 行）
LOG_FILE = 'update.log'
try:
    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()
except FileNotFoundError:
    lines = []

# 追加新的一行
lines.append(f"[{now.strftime('%Y-%m-%d')}] 更新每日提示 → {now.strftime('%Y年%m月%d日')} {weekday_cn}\n")

# 如果超过50行，只保留最后100行（砍掉最旧的开头）
if len(lines) > 50:
    lines = lines[-50:]

# 写回文件
with open(LOG_FILE, 'w', encoding='utf-8') as f:
    f.writelines(lines)

# 4. 更新 README.md（匹配固定文字）
try:
    with open('README.md', 'r', encoding='utf-8') as f:
        readme = f.read()
    # 用正则替换整行（不管原来是什么时间，都换成当前时间）
    new_readme = re.sub(r'^上次自动同步：.*$', f'上次自动同步：{full_time}', readme, flags=re.MULTILINE)
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(new_readme)
    print(f"✅ README 已更新为：{full_time}")
except Exception as e:
    print(f"⚠️ 更新 README 失败：{e}")
