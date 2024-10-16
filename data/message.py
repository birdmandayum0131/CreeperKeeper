import discord_colorize

colors = discord_colorize.Colors()


# * Define common used colors
def title(message: str) -> str:
    return f"{colors.colorize(message, fg='pink', bold=True)}"


def field(message: str) -> str:
    return f"{colors.colorize(message, fg='green', bold=True)}"


def value(message: str) -> str:
    return f"{colors.colorize(message, fg='blue', bold=True)}"


minecraft_server_message = f"""
**【Minecraft 伺服器】**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 如果你不知道該怎麼連線:point_down:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 :one: 安裝 Minecraft ，正版盜版都行。
 不知道盜版要裝啥，可以裝 TLauncher，
 但**安裝的時候記得不要裝它推薦的 Opera ( 勾勾要勾掉 )**，
 那就是一個比較冷門的瀏覽器。
 TLauncher連結 :point_right:  <https://tlauncher.org/en/#osselector>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 :two: 打開 Minecraft，版本選 **1.21.1**，
 多人遊戲 -> 右下角【新增伺服器】-> 下面填

> **伺服器名稱：** *取你自己喜歡的*
> **伺服器 IP：** `minecraft.bardbird.com`

 接著確認下方伺服器狀態有沒有開啟。


__ *( 伺服器啟動大約需要 30 秒到 1 分鐘 )* __
```ansi
{title('[伺服器資訊]')}
{field('伺服器位址 : ')}{value('minecraft.bardbird.com')}
{field('伺服器版本 : ')}{value('1.21.1')}
{field('伺服器狀態 : ')}{value('{serverStatus}')}
```
"""
