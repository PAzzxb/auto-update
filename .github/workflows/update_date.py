import json
from datetime import datetime

# ========== 1. 打印脚本开始 ==========
print("🚀 开始执行每日日期同步脚本")

# ========== 2. 打印当前时间（北京时间） ==========
now = datetime.now()
print(f"🕐 当前系统时间: {now.strftime('%Y-%m-%d %H:%M:%S')}")

# 获取日期和星期
today = now.strftime('%Y年%m月%d日')
weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
weekday = weekdays[now.weekday()]
print(f"📅 今日日期: {today} {weekday}")  # 打印日期，方便核对

# ========== 3. 读取配置文件 ==========
print("📂 读取 config.json...")
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)
print("✅ config.json 读取成功")

# ========== 4. 更新配置项 ==========
config['countdownSeconds'] = 8
config['imageUrl'] = "https://img.cdn1.vip/i/6a2e4678af9f9_1781417592.webp"
print("⚙️  已更新 countdownSeconds 和 imageUrl")

# ========== 5. 生成新的 tipMessage ==========
tip_message = f"""
******************************
🌟 温馨提醒
📅 {today} {weekday}
ℹ️ 状态：每日凌晨首次显示
⏱️ 8秒后自动关闭
🔄 按返回键刷新最新资源
******************************
"""
config['tipMessage'] = tip_message
print("✏️  已生成新的 tipMessage")

# ========== 6. 写回文件 ==========
print("💾 正在写入 config.json...")
with open('config.json', 'w', encoding='utf-8') as f:
    json.dump(config, f, ensure_ascii=False, indent=4)
print("✅ 写入完成")

# ========== 7. 最终确认 ==========
print(f"🎉 更新完成: {today} {weekday}")
print("👋 脚本执行结束")
