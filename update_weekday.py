import json
import datetime
import re
import glob
import math
import urllib.request
from zoneinfo import ZoneInfo
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ============ 时间 ============
now = datetime.datetime.now(ZoneInfo('Asia/Shanghai'))
weekdays = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
weekday_cn = weekdays[now.weekday()]
full_time = now.strftime("%Y-%m-%d %H:%M:%S") + f" {weekday_cn}"
new_date_str = now.strftime("%Y年%m月%d日")
date_dot = now.strftime("%Y.%m.%d")

# ============ 找中文粗体字体 ============
def find_font():
    cands = []
    cands += glob.glob('/usr/share/fonts/**/NotoSansCJK*Bold*.*', recursive=True)
    cands += glob.glob('/usr/share/fonts/**/NotoSansCJK*.*', recursive=True)
    cands += glob.glob('/usr/share/fonts/**/*CJK*.*', recursive=True)
    cands += glob.glob('/usr/share/fonts/**/*wqy*.*', recursive=True)
    return cands[0] if cands else None

FONT_PATH = find_font()

# ============ 生成方案A美化图 ============
def gen_banner(out_path):
    W, H = 720, 420
    def font(sz):
        idx = 0
        return ImageFont.truetype(FONT_PATH, sz, index=idx)
    def vgrad(size, c1, c2):
        w, h = size
        base = Image.new("RGB", size, c1)
        top = Image.new("RGB", size, c2)
        mask = Image.new("L", size)
        md = mask.load()
        for y in range(h):
            v = int(255 * y / h)
            for x in range(w):
                md[x, y] = v
        return Image.composite(top, base, mask)
    def center_text(d, cx, y, text, f, fill, shadow=None):
        bb = d.textbbox((0, 0), text, font=f)
        w = bb[2] - bb[0]
        x = cx - w // 2
        if shadow:
            d.text((x + 2, y + 2), text, font=f, fill=shadow)
        d.text((x, y), text, font=f, fill=fill)

    img = vgrad((W, H), (46, 26, 71), (12, 14, 38)).convert("RGBA")
    for cx, cy, r, col in [(140, 90, 180, (120, 80, 200, 70)),
                           (600, 340, 220, (60, 120, 220, 60)),
                           (560, 80, 120, (200, 80, 160, 45))]:
        g = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        gd = ImageDraw.Draw(g)
        gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
        img.alpha_composite(g.filter(ImageFilter.GaussianBlur(70)))
    d = ImageDraw.Draw(img, "RGBA")
    center_text(d, W // 2, 46, "温馨提示", font(38), (255, 255, 255, 255), (0, 0, 0, 120))
    center_text(d, W // 2, 130, date_dot, font(76), (255, 255, 255, 255), (0, 0, 0, 140))
    center_text(d, W // 2, 232, weekday_cn, font(40), (210, 190, 255, 255))
    d.line([(W // 2 - 140, 300), (W // 2 + 140, 300)], fill=(255, 255, 255, 90), width=2)
    center_text(d, W // 2, 322, "每日随机提醒一次 · 时间不固定", font(26), (200, 210, 235, 255))
    img.convert("RGB").save(out_path, quality=88)

# ============ 上传 panurl.cn 拿国内直链 ============
def upload_panurl(path):
    import mimetypes
    boundary = "----minisboundary1234567890"
    with open(path, "rb") as f:
        filedata = f.read()
    body = b""
    body += ("--" + boundary + "\r\n").encode()
    body += b'Content-Disposition: form-data; name="file"; filename="banner.jpg"\r\n'
    body += b'Content-Type: image/jpeg\r\n\r\n'
    body += filedata + b"\r\n"
    body += ("--" + boundary + "\r\n").encode()
    body += b'Content-Disposition: form-data; name="format"\r\n\r\njson\r\n'
    body += ("--" + boundary + "--\r\n").encode()
    req = urllib.request.Request(
        "https://www.panurl.cn/api.php", data=body, method="POST",
        headers={"Content-Type": "multipart/form-data; boundary=" + boundary,
                 "User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        d = json.loads(r.read().decode("utf-8"))
    if d.get("code") == 0:
        return d.get("viewurl") or d.get("downurl")
    raise RuntimeError("panurl 上传失败: " + str(d))

# ============ 读 config ============
try:
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    config = {}

config['last_weekday'] = weekday_cn
config['last_update'] = full_time
config['tipDate'] = new_date_str
config['tipMessage'] = (
    "\n━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "🌟 温馨提醒\n"
    f"📅 {new_date_str} {weekday_cn}\n"
    "ℹ️ 每日随机提醒一次 · 时间不固定\n"
    "⏱️ 20秒后自动关闭\n"
    "🔄 按返回键刷新最新资源\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
)

# 生成美化图 + 上传，成功才更新 imageUrl（失败保留原图，不影响其它字段）
try:
    if not FONT_PATH:
        raise RuntimeError("未找到中文字体")
    gen_banner('/tmp/banner.jpg')
    url = upload_panurl('/tmp/banner.jpg')
    config['imageUrl'] = url
    print(f"🖼️ 今日美化图：{url}")
except Exception as e:
    print(f"⚠️ 生成/上传美化图失败，保留原 imageUrl：{e}")

with open('config.json', 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

# ============ update.log ============
LOG_FILE = 'update.log'
try:
    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()
except FileNotFoundError:
    lines = []
lines.append(f"[{now.strftime('%Y-%m-%d')}] 更新每日提示 → {new_date_str} {weekday_cn}\n")
if len(lines) > 50:
    lines = lines[-50:]
with open(LOG_FILE, 'w', encoding='utf-8') as f:
    f.writelines(lines)

# ============ README ============
try:
    with open('README.md', 'r', encoding='utf-8') as f:
        readme = f.read()
    new_readme = re.sub(r'^上次自动同步：.*$', f'上次自动同步：{full_time}', readme, flags=re.MULTILINE)
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(new_readme)
    print(f"✅ README 已更新为：{full_time}")
except Exception as e:
    print(f"⚠️ 更新 README 失败：{e}")
