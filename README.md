# 浙经院晨检自动签到python脚本
### 一&emsp;脚本背景说明
>   用于浙江经济职业技术学院的每日晨检
### 二&emsp;功能简介
>   访问mysql数据库，读取需要签到的用户。
    并为其签到，签到完成后用邮件通知结果
### 三&emsp;脚本使用时需要修改的参数
>   
    admin_email="xxx@xx.com"#管理员邮箱
    url = "https://msj.jinshuju.net"#主地址
    mydb = mysql.connector.connect(
        host="127.0.0.1",       # 数据库主机地址
        user="xxxxxxx",    # 数据库用户名
        passwd="xxxxxx",   # 数据库密码
        database="xxxxxx"   # 数据库
    )
>
    from_addr ='xxxxx@xxx.com'#邮箱
    password = 'xxxxx'#密码
    
    # 收信方邮箱
    to_addr = mail_url
    
    # 发信服务器
    smtp_server = 'smtp.ym.163.com'
### 四&emsp;脚本使用建议
>    1. mysql数据库
>    2. crontab（linux定时工具）
>    3. 腾讯云函数(没有服务器的话)