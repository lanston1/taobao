# taobao
for windows system:

1. 打开cmd，在命令行中输入命令：
chrome.exe --remote-debugging-port=9999 --user-data-dir="C:\selenum\AutomationProfile"

2. 打开一个浏览器页面，我们输入淘宝网址（https://login.taobao.com/member/login.jhtml），输入用户名和密码，登录淘宝后用户信息就保存在 --user-data-dir="C:\selenum\AutomationProfile" 所指定的文件夹中。

3. 设置 chrome 允许弹出窗口
在 chrome 浏览器地址栏输入：chrome://settings/content/popups，把 已阻止(推荐)  改成 允许 即可。
或者 chrome -》设置 -》高级 -》隐私设置和安全性 -》网站设置 -》弹出式窗口和重定向，也可以设置。

4. 不要关闭上面的浏览器，然后执行python代码即可
