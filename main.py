import http
import requests
import html5lib
import smtplib
import sys
import io
import time
import mysql.connector
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr
from bs4 import BeautifulSoup

'''
    
@author: InkReturn
@description: 用于某个学校的晨检数据提交
@date: 2020/7/1

'''


'''
@description:   用于发送邮件的方法
@param {
    mail_url : 邮件的地址
    text     : 邮件的主体内容
    res      : 邮件标题的部分需要传入的文本
} 
@return:void 
'''

def sedMail(mail_url,text,res):
    from_addr ='xxxxx@xxx.com'
    password = 'xxxxx'
    
    # 收信方邮箱
    to_addr = mail_url
    
    # 发信服务器
    smtp_server = 'smtp.ym.163.com'
    
    # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
    msg = MIMEText(text,'plain','utf-8')
    
    # 邮件头信息
    msg['From'] = formataddr(pair=('自动签到系统通知',from_addr))
    msg['To'] = Header(to_addr)
    msg['Subject'] = Header('签到结果:'+res)
    
    # 开启发信服务，这里使用的是加密传输
    server=smtplib.SMTP_SSL('smtp.ym.163.com')
    server.connect(smtp_server,994)
    # 登录发信邮箱
    server.login(from_addr, password)
    # 发送邮件
    server.sendmail(from_addr, to_addr, msg.as_string())
    # 关闭服务器
    server.quit()



'''
@description: 用于签到的主体操作
@param {
    wx_openid   :   微信openid,用于登录请求
    url         :   主地址
    email       :   用户邮件，用于签到完成的通知发送
} 
@return:void 
'''
def morning(wx_openid, url,email):
    login_url = "/f/J30YUa/s/elVofh?q%5B0%5D%5Bx_field_weixin_openid%5D="
    session = requests.session()  # 会话开始
    login_res = session.get(url=(url+login_url+wx_openid))  # 访问登录
    soup = BeautifulSoup(login_res.text, "html5lib")  # 启动解析器
    csrf_token = soup.find(attrs={'name': 'csrf-token'})  # 获取token
    csrf_token_str = csrf_token.get('content')
    
    exit_post_data = {
        '_method': 'post',
        'authenticity_token': csrf_token_str
    }
    exit_url = soup.find(attrs={'data-method':'post'}).get('href')
    exit_res = session.post(url=url+exit_url,
                            data=exit_post_data)  # 访问修改页面  # 访问修改页面
    soup = BeautifulSoup(exit_res.text, "html5lib")
    # input_url = soup.find(name='form').get("action")
    csrf_token = soup.find(attrs={'name': 'csrf-token'})  # 获取token
    csrf_token_str = csrf_token.get('content')
    t = soup.find(attrs={'name': 't', 'id': 't'})
    t_str = t.get('value')

    input_url = soup.find(name='form').get('action')
    #设置提交表单
    input_post_data = {
        'utf8': "✓",
        '_method': 'patch',
        'authenticity_token': csrf_token_str,
        't': t_str,
        'entry[field_51][province]': '' ,
        'entry[field_51][city]': '' ,
        'entry[field_51][district]': '' ,
        'entry[field_51][street]': '' ,
        'entry[field_40][]': '' ,
        'entry[field_125]': '' ,
        'entry[field_46]': '' ,
        'entry[field_75]': '' ,
        'entry[field_101]': '' ,
        'entry[field_102_other]': '' ,
        'entry[field_67][]': '' ,
        'entry[field_67_other]': '' ,
        'entry[field_108_other]': '' ,
        'entry[field_123][]': '' ,
        'entry[field_144]': '' ,
        'entry[field_109]': '' ,
        'entry_field_111_files': '' ,
        'entry[field_97]': '' ,
        'entry[field_147]': '' ,
        'entry_field_112_files': '' ,
        'entry[field_112][]': '' ,
        'entry[field_113]': '' ,
        'entry[field_113_other]': '' ,
        'entry[field_114][]': '' ,
        'entry[field_128]': '' ,
        'entry[field_130]': '' ,
        'entry[field_96][]': '' ,
        'entry[field_96_other]': '' ,
        'commit': '提交'
    }
    dict = {
        'entry[field_113]': 1,
        'entry[field_114][]': 0,
        'entry[field_128]': 1,
        'entry[field_130]': 0,
        'entry[field_96][]': 0
    }
    for key in input_post_data:
        if input_post_data[key] == "":
            if key in dict:
                if soup.find_all(attrs={'name': key})[dict[key]].get("value") is not None:
                    input_post_data[key] = soup.find_all(attrs={'name': key})[
                        dict[key]].get("value")
                elif soup.find_all(attrs={'name': key})[dict[key]].get("data-value") is not None:
                    input_post_data[key] = soup.find_all(attrs={'name': key})[
                        dict[key]].get("data-value")
            elif soup.find(attrs={'name': key, 'checked': 'checked'}) is not None:
                if (soup.find(attrs={'name': key, 'checked': 'checked'})).get("data-value") is not None:
                    input_post_data[key] = soup.find(
                        attrs={'name': key, 'checked': 'checked'}).get("data-value")
                elif soup.find(attrs={'name': key, 'checked': 'checked'}).get("value") is not None:
                    input_post_data[key] = soup.find(
                        attrs={'name': key, 'checked': 'checked'}).get("value")
            else:
                if soup.find(attrs={'name': key}).get("value") is not None:
                    input_post_data[key] = soup.find(
                        attrs={'name': key}).get("value")
                elif soup.find(attrs={'name': key}).get("data-value") is not None :
                    input_post_data[key] = soup.find(attrs={'name': key}).get("data-value")


    input_res = session.post(url=(url+input_url), data=input_post_data)
    soup = BeautifulSoup(input_res.text, "html5lib")
    hed  = soup.find(attrs={'data-field':'field_113','class':"radiobutton"}).text
    sedMail(email,hed+input_res.text,hed)
    session.close()
if __name__ == "__main__":
    url = "https://msj.jinshuju.net"
    mydb = mysql.connector.connect(
        host="127.0.0.1",       # 数据库主机地址
        user="xxxxxxx",    # 数据库用户名
        passwd="xxxxxx",   # 数据库密码
        database="xxxxxx"   # 数据库
    )
    mycursor = mydb.cursor() 
    mycursor.execute("SELECT * FROM usr")#搜索全部用户
    myresult = mycursor.fetchall() 
    
    for result in myresult:
        try:
            email=result[0]
            wx_openid=result[1]
            morning(wx_openid, url,email)
        except:
            try:
                localtime = time.asctime( time.localtime(time.time()) )
                print(localtime+"|"+email+"签到出错")
                sedMail(email,'签到发生错误',"出错")
                sedMail('xxxxxxxx@qq.com',email+'签到出错',"出错")     
            except:
                try:
                    sedMail('xxxxx@qq.com',email+'邮件发送出错',"出错")
                except:
                    print("邮件发送异常似乎达到上限")
        else:
            localtime = time.asctime( time.localtime(time.time()) )
            print(localtime+"|"+email+"已签到")
        
