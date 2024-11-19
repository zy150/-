# 微博Gephi关系图生成

自动爬取微博转发关系，用于生成Gephi下的节点图

Powered By [zy150 (一只懒虫)](https://github.com/zy150)

repository： [zy150/-Weibo](https://github.com/zy150/-Weibo)

## 配置文件

配置文件在properties.json中,以下为样例

```json
{
  "url": "https://weibo.com/ajax/statuses/repostTimeline",
  "topic": "#哈利波特海格扮演者去世",
  "sleep_time":2,
  "mid": "P0KULo1yE",
  "id": "5101803435725864",
  "limit": 1000,
  "pages":1000,
  "save_path": "./WeiBo_data/",
  "headers": {
    "authority": "weibo.com",
    "x-requested-with": "XMLHttpRequest",
    "sec-ch-ua-mobile": "?0",
    "cookie": "SCF=Alud2Q7aqlV5oX5tsYzdMHaF2Yiu47pnO-acCQPKtDFngGTuz2R2B4is-OtXnqfDKfaIXKdvDcWH_sucdfrRux8.; SINAGLOBAL=3888515822091.3584.1731225435266; ULV=1731225435330:1:1:1:3888515822091.3584.1731225435266:; PC_TOKEN=17d705145c; ALF=1734591982; SUB=_2A25KOEi-DeRhGeFL7FUT9inLyT-IHXVpNMR2rDV8PUJbkNANLU3gkW1NfblupkR04qq-q1RW3DmgfGiW2KzzkJG0; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5Sfa8yDsmSxFC63lqWQAwb5JpX5KMhUgL.FoMfS0MESoMNeoe2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMNSKMNeoqNS0z0; XSRF-TOKEN=_Pxmi327oXRJpVAsm29l56JB; WBStorage=fcc86192|undefined; WBPSESS=NI5tmsiRcfXGnErssJsJXLa9deUK-ry1_A8i1HVR0hPF7cvvSTq_CGe4vpzTUPZ2Vxem_E38mu-7qo_jyMxOPbtDNIaTk8bKsKwvXgZE6zIdzBdmemr7CXHtcuERgVgGwTmLcilMD4K-e4QhRUbSOQ==",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "content-type": "application/x-www-form-urlencoded",
    "accept": "*/*",
    "sec-fetch-site": "same-origin",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": "https://weibo.com/1192329374/KnnG78Yf3?filter=hot&root_comment_id=0&type=comment",
    "accept-language": "zh-CN,zh;q=0.9,en-CN;q=0.8,en;q=0.7,es-MX;q=0.6,es;q=0.5"
  },
  "params": {
    "moduleID": "feed"
  }
}
```

 **必须填写**

- id: 必须填写
- mid: 必须填写
- topic: 必须填写

- headers: 请求头 ,必须填写，里面有cookie参数，这里可以用下面的网站一键复制

 ***无需填写***

- sleep_time: 爬取间隔 默认为3
- pages: 爬取多少页 默认为500 每页大概15条数据，爬虫已经自动判断最大有多少页，到最大页就会停止
- result_file: 结果保存路径 默认为 ./WeiBo_data/mid+id.csv
- params: 请求参数 无需填写
- url: 请求url ***无需填写***

## 参数获取

**mid**：点开任意一条具体博文，红框里就是mid

<img src="C:\Users\zy150\AppData\Roaming\Typora\typora-user-images\image-20241119162430685.png" alt="image-20241119162430685" style="zoom: 67%;" />





**id&header**:

第一步：

<img src="C:\Users\zy150\AppData\Roaming\Typora\typora-user-images\image-20241119162819035.png" alt="image-20241119162819035" style="zoom:67%;" />



第二步：

<img src="C:\Users\zy150\AppData\Roaming\Typora\typora-user-images\image-20241119162952364.png" alt="image-20241119162952364" style="zoom:67%;" />



第三步：进入此网站[Convert curl commands to code](https://curlconverter.com/)

![image-20241119163308823](C:\Users\zy150\AppData\Roaming\Typora\typora-user-images\image-20241119163308823.png)

## 用法说明

更改id，mid，cookie之后，直接跑就行

- crawl()方法为爬取并存为csv
- process()方法为处理crawl生成的csv，转为供Gephi使用的csv，保存路径 默认为 ./WeiBo_data/mid+id+_nodes.csv
- 将最终的_nodes.csv导入到Gephi即可
- **注意**：建议数据量少时auto_direct_topic设置为true，代码有具体解释，默认为true