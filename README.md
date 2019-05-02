# Chatbot
Test chatbot based on Baidu UNIT 2.0

Description
This bot is a test version which only support simple Q&A and 
Support language: Simplified Chinese
Function: Movie ticket bossting

User manual:

Via Wechat offical account:
1. Please put "movie-avalible/" ,"session_ids/", "app.py", "authentication.py" and "Chatbot.py" to your the website path of your server(E.g. For nginx, please put it in /var/www/html or its subfolders).
2. Make sure the port 80 is availble
3. Then visit https://mp.weixin.qq.com for setting WeChat official account for auto-reply

  (1) Choose "Development" -> "Basic Config", Record "AppID" and "AppSecret". (If you cannot find "AppSecret", Enable it)
  (2) Click "Server Config" -> Click "modify", fill the form with correspond content. The "URL" should be the path that "app.py" located. Set "token" by yourself and we suggest to use random "EncodingAESKey".
  (3) Modify the constructor of class "Get" in "app.py". set  self.token = "$token", self.Appid = "$AppID", self.AppSecret = "AppSecret".
  (4) Launch "app.py" in your server
  (5) Click "submit". If the reply is "sumbit successfully", it means the config is enabled.

4. Try to send message in your offcial account

Offline:
Use "jupyter" to run "Chatbot.ipynb" and run all column in orders, and you can enjoy in the "test" function

用户手册:
通过微信公众号:
1. 将"movie-avalible/" ,"session_ids/", "app.py", "authentication.py" 以及 "Chatbot.py" 放置于服务器网页目录下 （例如使用nginx，则放在/var/www/html或其子目录）
2. 确认服务器80端口开放
3. 进入微信公众平台， 设置自动回复：
(1) 点击左侧 开发 -> 基本配置，找到开发者ID和密码（没有则启用）;
(2) 点击 服务器配置 -> 修改，在服务器配置填写对应的内容， URL填写对应app所在的目录，token自选， EncodingAESKey建议随机生成。
(3) 将"app.py"的Get构造函数中 将self.token 的值改为(3)中的token, 将AppID和AppSeceret的值改为(1)中的开发值ID和密码。
(4) 启动服务器上"app.py";
(5) 点击“提交”，若提示“提交成功”，则服务器配置成功

4. 在公众号对话

离线模式：
使用"Jupyter" 打开 "Chatbot.ipynb", 依次跑完所有块， 再最后的test函数中进行对话测试。


Github link:
https://github.com/15103875d/Chatbot
