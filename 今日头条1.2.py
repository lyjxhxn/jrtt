import requests
import re
import random
import binascii
import base64

"""
破解原理：
那么接下来的问题就是探究上面的第2个请求http://i.snssdk.com/video/urls/v/1/toutiao/mp4/9583cca5fceb4c6b9ca749c214fd1f90?r=18723666135963302&s=3807690062&callback=tt_playerzfndr 是如何构造的。

在用Chrome的开发者工具监视网络请求的时候可以看到该请求是js脚本发出的，该js脚本是 http://s3.pstatp.com/tt_player/player/tt2-player.js?r=customer1
把该js下载下来，prettify一下，使用你最爱的编辑器看看该js到底做了些什么。

通过研究该js脚本，发现请求http://i.snssdk.com/video/urls/v/1/toutiao/mp4/9583cca5fceb4c6b9ca749c214fd1f90?r=18723666135963302&s=3807690062&callback=tt_playerzfndr 中的一些参数的含义如下：

9583cca5fceb4c6b9ca749c214fd1f90：这是视频的唯一ID
18723666135963302：这是一个随机数
3807690062：这是CRC32校验值
视频的唯一ID可以在播放页HTML源码中找到，即id为video的元素的tt-videoid属性值。
"""

class Run(object):
   
    def get_data(self,player_url):
        global title
        head = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
        }
        html = requests.get(player_url, headers = head).text
        vid = re.search(r"videoId: '(.*?)'",html)
        title = re.search(r"<title>(.*?)</title>",html)
        #print(vid.group(1))
        r = str(random.random())[2:]
        url = '/video/urls/v/1/toutiao/mp4/%s?r=%s' % (vid.group(1),r)
        b_n = bytes(url,encoding = "utf-8")
        c = binascii.crc32(b_n)
        #print("http://i.snssdk.com"+ url + "&s=%s" %c)
        json_html = requests.get("http://i.snssdk.com"+ url + "&s=%s" %c)
        datas = json_html.json()
        return datas


    def get_url(self,datas):
        if datas:
            video_list = datas["data"]["video_list"]
            m = 0
            print("标题：%s"%(title.group(1)))
            
            if video_list: 
                for i in video_list:
                    definition = video_list[i]["definition"]
                    m += 1
                    print(str(m)+"."+ definition)
                a = int(input("请输入想要下载的清晰度序号："))
                if a >= 1 and a <= len(video_list):
                    if a == 1:
                        main_url = video_list["video_1"]["main_url"]
                    elif a == 2:
                        main_url = video_list["video_2"]["main_url"]
                    elif a == 3:
                        main_url = video_list["video_3"]["main_url"]
                    elif a == 4:
                        main_url = video_list["video_4"]["main_url"]
                    return main_url  
                else:
                    print("输入有误")
                
                #print(main_url)
            else:
                print("没有找到该资源")


    def down(self,main_url):
        if main_url:
            bs64 = base64.standard_b64decode(main_url)
            down_url = str(bs64,'utf-8')
            resopnse = requests.get(down_url)
            move = resopnse.content
            with open("%s.mp4"%title.group(1).split("，")[0],"wb") as f:
                f.write(move)
                print("%s下载完成!"%title.group(1))


if __name__ == '__main__':
    __version__ = '1.2'
    NAME = '今日头条资源下载'   

    msg = """
            +------------------------------------------------------------+
            |                                                            |
            |              欢迎使用{} V_{}                |
            |                                                            |
            |                             Copyright (c) 2018   lyjxhxn   |
            +------------------------------------------------------------+
            """.format(NAME, __version__)
    print(msg)
    run = Run()  
    while True:
        player_url = input("请输入想要下载的网址：").strip()
        if player_url:
            datas = run.get_data(player_url)
            main_url = run.get_url(datas)
            run.down(main_url)


   



