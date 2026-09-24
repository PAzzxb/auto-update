import json
import datetime
import re
import glob
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

# ============ 中文字体 ============
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

# 每日轮换配色（背景光晕主色随星期变化，天天不一样）
PALETTES = [
    ((46,26,71),(12,14,38),[(120,80,200),(60,120,220),(200,80,160)]),   # 周一 紫蓝
    ((20,50,70),(8,20,40),[(60,180,200),(40,120,220),(80,200,180)]),    # 周二 青蓝
    ((60,30,40),(24,12,20),[(220,90,120),(200,120,60),(240,140,90)]),   # 周三 暖橙红
    ((30,50,40),(10,26,20),[(80,200,140),(60,180,120),(120,220,160)]),  # 周四 翠绿
    ((50,30,66),(18,12,34),[(180,90,220),(140,80,240),(220,120,200)]),  # 周五 梦紫
    ((30,40,66),(10,16,34),[(90,130,240),(70,160,230),(120,180,255)]),  # 周六 蓝
    ((60,40,30),(26,16,10),[(240,160,80),(230,120,60),(250,190,110)]),  # 周日 金橙
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
    spots=[(130,80,180),(600,340,220),(560,70,120)]
    for (cx,cy,r),col in zip(spots,glows):
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

# ============ 读 config ============
try:
    with open('config.json','r',encoding='utf-8') as f:
        config=json.load(f)
except FileNotFoundError:
    config={}

config['last_weekday']=weekday_cn
config['last_update']=full_time
config['tipDate']=new_date_str
# 文字精简：消除与图片的重复，只留一句空提示（弹窗以美化图为主）
config['tipMessage']=" "
# imageUrl 固定走 CF 中转（国内可达），图片内容每天由 banner.jpg 更新
config['imageUrl']="https://www.niuwa.ccwu.cc/img"

# 生成当天美化图（覆盖 banner.jpg，供 worker /img 代理）
try:
    if not FONT_PATH:
        raise RuntimeError("未找到中文字体")
    gen_banner('banner.jpg')
    print("🖼️ 已生成当天 banner.jpg")
except Exception as e:
    print(f"⚠️ 生成美化图失败：{e}")

with open('config.json','w',encoding='utf-8') as f:
    json.dump(config,f,indent=2,ensure_ascii=False)

# ============ update.log ============
LOG='update.log'
try:
    with open(LOG,'r',encoding='utf-8') as f: lines=f.readlines()
except FileNotFoundError: lines=[]
lines.append(f"[{now.strftime('%Y-%m-%d')}] 更新每日提示 → {new_date_str} {weekday_cn}\n")
if len(lines)>50: lines=lines[-50:]
with open(LOG,'w',encoding='utf-8') as f: f.writelines(lines)

# ============ README ============
try:
    with open('README.md','r',encoding='utf-8') as f: readme=f.read()
    readme=re.sub(r'^上次自动同步：.*$', f'上次自动同步：{full_time}', readme, flags=re.MULTILINE)
    with open('README.md','w',encoding='utf-8') as f: f.write(readme)
    print(f"✅ README 已更新：{full_time}")
except Exception as e:
    print(f"⚠️ README 更新失败：{e}")
