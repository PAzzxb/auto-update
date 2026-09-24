import json
import datetime
import re
import glob
import base64
import os
import urllib.request
from zoneinfo import ZoneInfo
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ================= 时间 =================
now = datetime.datetime.now(ZoneInfo('Asia/Shanghai'))
weekdays = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
weekday_cn = weekdays[now.weekday()]
full_time = now.strftime("%Y-%m-%d %H:%M:%S") + f" {weekday_cn}"
new_date_str = now.strftime("%Y年%m月%d日")
date_dot = now.strftime("%Y.%m.%d")

GH_TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
V_REPO = "PAzzxb/v"   # 图片+视频同仓（走 ghfast 代理，用户联通关代理可达）

# ================= 中文字体 =================
def find_font():
    for pat in ['/usr/share/fonts/**/NotoSansCJK*Bold*.*',
                '/usr/share/fonts/**/NotoSansCJK*.*',
                '/usr/share/fonts/**/*CJK*.*',
                '/usr/share/fonts/**/*wqy*.*',
                '/usr/share/fonts/**/*noto*.*']:
        g = glob.glob(pat, recursive=True)
        if g:
            return g[0]
    return None
FONT_PATH = find_font()

# 每日按星期换配色
PALETTES = [
    ((46,26,71),(12,14,38),[(120,80,200),(60,120,220),(200,80,160)]),
    ((20,50,70),(8,20,40),[(60,180,200),(40,120,220),(80,200,180)]),
    ((60,30,40),(24,12,20),[(220,90,120),(200,120,60),(240,140,90)]),
    ((30,50,40),(10,26,20),[(80,200,140),(60,180,120),(120,220,160)]),
    ((50,30,66),(18,12,34),[(180,90,220),(140,80,240),(220,120,200)]),
    ((30,40,66),(10,16,34),[(90,130,240),(70,160,230),(120,180,255)]),
    ((60,40,30),(26,16,10),[(240,160,80),(230,120,60),(250,190,110)]),
]

def gen_banner(out_path):
    W, H = 720, 420
    def font(sz): return ImageFont.truetype(FONT_PATH, sz, index=0)
    def vgrad(size, c1, c2):
        w,h=size; base=Image.new("RGB",size,c1); top=Image.new("RGB",size,c2)
        mask=Image.new("L",size); md=mask.load()
        for y in range(h):
            v=int(255*y/h)
            for x in range(w): md[x,y]=v
        return Image.composite(top,base,mask)
    def ctext(d,cx,y,text,f,fill,shadow=None):
        bb=d.textbbox((0,0),text,font=f); w=bb[2]-bb[0]; x=cx-w//2
        if shadow: d.text((x+2,y+2),text,font=f,fill=shadow)
        d.text((x,y),text,font=f,fill=fill)
    c1,c2,glows = PALETTES[now.weekday()]
    img = vgrad((W,H),c1,c2).convert("RGBA")
    for (cx,cy,r),col in zip([(130,80,180),(600,340,220),(560,70,120)],glows):
        g=Image.new("RGBA",(W,H),(0,0,0,0)); gd=ImageDraw.Draw(g)
        gd.ellipse([cx-r,cy-r,cx+r,cy+r],fill=col+(72,))
        img.alpha_composite(g.filter(ImageFilter.GaussianBlur(72)))
    d=ImageDraw.Draw(img,"RGBA")
    ctext(d,W//2,44,"温馨提示",font(46),(255,255,255,255),(0,0,0,120))
    ctext(d,W//2,128,date_dot,font(78),(255,255,255,255),(0,0,0,140))
    ctext(d,W//2,232,weekday_cn,font(40),(235,225,255,255))
    d.line([(W//2-150,300),(W//2+150,300)],fill=(255,255,255,90),width=2)
    ctext(d,W//2,320,"每日随机提醒一次 · 时间不固定",font(26),(220,225,245,255))
    img.convert("RGB").save(out_path,quality=88)

# ================= GitHub API 写文件 =================
def gh_put(repo, path, data_bytes, msg):
    api = f"https://api.github.com/repos/{repo}/contents/{path}"
    sha = None
    try:
        r = urllib.request.Request(api, headers={"Authorization": f"token {GH_TOKEN}", "User-Agent": "bot"})
        sha = json.loads(urllib.request.urlopen(r, timeout=30).read()).get("sha")
    except Exception:
        sha = None
    body = {"message": msg, "content": base64.b64encode(data_bytes).decode(), "branch": "main"}
    if sha:
        body["sha"] = sha
    req = urllib.request.Request(api, data=json.dumps(body).encode(), method="PUT",
          headers={"Authorization": f"token {GH_TOKEN}", "Accept": "application/vnd.github+json", "User-Agent": "bot"})
    urllib.request.urlopen(req, timeout=120)

# ================= 读 config =================
try:
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    config = {}

config['last_weekday'] = weekday_cn
config['last_update']  = full_time
config['tipDate']      = new_date_str

# 每日一言（GitHub Actions 海外拉取，写入弹窗上方文字；失败则用备用句）
def fetch_hitokoto():
    try:
        req = urllib.request.Request("https://v1.hitokoto.cn/?encode=json",
              headers={"User-Agent": "Mozilla/5.0"})
        d = json.loads(urllib.request.urlopen(req, timeout=15).read().decode("utf-8"))
        txt = d.get("hitokoto", "").strip()
        frm = d.get("from", "").strip()
        return txt, frm
    except Exception as e:
        print(f"⚠️ 一言获取失败：{e}")
        return "", ""

hito, hito_from = fetch_hitokoto()
if not hito:
    hito = "愿你所行皆坦途，所遇皆温柔。"
    hito_from = ""
_from_line = f"\n            —— {hito_from}" if hito_from else ""
config['tipMessage'] = (
    "\n"
    "╭─────────────╮\n"
    "     ✨ 每 日 一 言 ✨\n"
    f"     💬 {hito}{_from_line}\n"
    f"     🗓 {new_date_str} {weekday_cn}\n"
    "╰─────────────╯\n"
)
# 图片走视频同款 ghfast 通道（用户联通关代理可达；CF/niuwa 被墙弃用）
# banner.jpg 就在本仓(auto-update)，workflow 内置 token 可直接提交
config['imageUrl']     = "https://www.ghfast.top/github.com/PAzzxb/auto-update/raw/main/banner.jpg"

# 生成当天美化图 → 写到本仓 banner.jpg（每天自动换；由 git commit 步骤提交）
try:
    if not FONT_PATH:
        raise RuntimeError("未找到中文字体")
    gen_banner('banner.jpg')
    print(f"🖼️ 已生成当天 banner.jpg")
except Exception as e:
    print(f"⚠️ 生成美化图失败：{e}")

with open('config.json', 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

# ================= update.log =================
LOG = 'update.log'
try:
    with open(LOG, 'r', encoding='utf-8') as f:
        lines = f.readlines()
except FileNotFoundError:
    lines = []
lines.append(f"[{now.strftime('%Y-%m-%d')}] 更新每日提示 → {new_date_str} {weekday_cn}\n")
if len(lines) > 50:
    lines = lines[-50:]
with open(LOG, 'w', encoding='utf-8') as f:
    f.writelines(lines)

# ================= README =================
try:
    with open('README.md', 'r', encoding='utf-8') as f:
        readme = f.read()
    readme = re.sub(r'^上次自动同步：.*$', f'上次自动同步：{full_time}', readme, flags=re.MULTILINE)
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme)
    print(f"✅ README 已更新：{full_time}")
except Exception as e:
    print(f"⚠️ README 更新失败：{e}")
