import requests
import os
import re
import parsel
import time
from bs4 import BeautifulSoup
import concurrent.futures


def get_response(html_url):
    """
    发送请求
    """
    headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
    response = requests.get(url=html_url,headers=headers)
    return response

def get_url(html_url):
    '''
    获取每章节url
    '''
    html_data = get_response(html_url).text
    name = re.findall('<h1>(.*?)</h1>',html_data)[0]
    url_list = re.findall('<dd><a href="(.*?)">',html_data)
    return name,url_list

def get_content(content_url):
    '''
    获取正文
    '''
    content_data = get_response(content_url).text
    title = re.findall('<h1>(.*?)</h1>',content_data)[0]
    selector = parsel.Selector(content_data)
    content = selector.css('.box_con #gonggao, .box_con #content, .box_con #content div, .box_con #content a::text').getall()
    para = ''
    for i in range(0,len(content[0])):
        if(content[0][i]!='<' and content[0][i] != '/' and content[0][i] != 'p' and content[0][i] != '>'):
            para = para + content[0][i]
        else:
            if(content[0][i] == '>' and content[0][i-3]=='>'):
                para = para + '\n'
    return title,para

def save(name,title,content):
    '''
    保存章节
    '''
    file = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(file, name)
    if not os.path.exists(path):
        os.mkdir(path)
    file_path = path + '\\' + title + '.txt'
    fixed_file_path = file_path.replace('?', '')
    with open(fixed_file_path,'a',encoding='utf-8') as f:
        f.write(title)
        f.write('\n')
        f.write(content)
        f.write('\n')


def main(index_url,name):
    title,content = get_content(index_url)
    save(name,title,content)
        
if __name__ == '__main__':
    home_url = input('请输入URL:')
    name,url_list = get_url(home_url)
    exe = concurrent.futures.ThreadPoolExecutor(max_workers=7) # 多线程下载
    for url in url_list:
        index_url= 'http://www.ibiqu.net' + url
        exe.submit(main,index_url,name)
        time.sleep(0.5)  #防止请求过快

