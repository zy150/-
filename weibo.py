import json
import os
import re
from time import sleep

import requests
import pandas as pd



class Weibo:
    def __init__(self, auto_direct_topic=True):
        """微博转发关系爬取

        字段只有用户名和转发信息

        # 对于init方法的说明
        __init__方法首先会读取该py文件存放路径下的配置文件properties.json
        爬取所需要的id，mid，cookie等参数俊存放在配置文件中

        Attributes:
           auto_direct_topic: 是否将孤立点指向topic，默认为True
                              topic即为爬取的话题，例如#哈利波特海格扮演者去世
                              孤立点是指，爬虫可能爬不完所有的转发数据，那么可能会出现A转发的D
                              而爬取的数据中并没有D的转发信息，那么D就是孤立点
                              当为Ture时，会将孤立点指向topic
                              False时，不会将孤立点指向topic，但可能会造成最终图像孤立点过多
        properties.json:
            id: 必须填写
            mid: 必须填写
            topic: 必须填写

            sleep_time: 爬取间隔 默认为2
            pages: 爬取多少页 默认为150 每页大概15条数据
            result_file: 结果保存路径 默认为 ./WeiBo_data/mid+id.csv

            params: 请求参数 无需填写
            headers: 请求头 无需填写
            url: 请求url 无需填写

        """

        # 读取配置文件
        with open('./properties.json', 'r', encoding='utf-8') as file:
            configure = json.load(file)
        # 请求参数设置
        self.params = configure["params"]
        self.params['id'] = configure["id"]
        self.params['mid'] = configure["mid"]
        self.headers = configure["headers"]
        # 爬取参数设置
        self.url = configure["url"]
        self.sleep_time = configure["sleep_time"]
        self.limit = configure["limit"]
        # 爬取多少页 1页20条
        self.pages = configure["pages"]
        self.result_file = os.path.join(configure["save_path"], self.params['mid'] + '.csv')
        self.data = []
        self.topic = configure["topic"]
        self.auto_direct_topic = auto_direct_topic
        # 创建保存文件夹
        os.makedirs(configure["save_path"], exist_ok=True)
        self.header_csv = True
        self.max_page = 10
    def crawl(self):
        """爬取方法"""
        for page in range(1, self.pages + 1):
            self.params['page'] = page
            response = requests.get(url=self.url, headers=self.headers, params=self.params)
            print(response.url)
            data = response.json()['data']
            self.max_page = response.json()['max_page']
            for item in data:
                mid = item['idstr']
                user_name = item['user']['screen_name']
                content = item['text_raw']
                tempt = {
                    'user_name': user_name,
                    'content': content if r"@" in content else "",
                }

                self.data.append(tempt)
            print("============第{}页爬取完成============".format(page))
            sleep(self.sleep_time)
            if len(self.data) >= 3000:
                self.save()
                self.data = []
            if page == self.max_page:
                print("已到达当前微博转发最大页数------>{}".format(self.max_page))
                break
        if self.data:
            self.save()

    def save(self):
        """保存数据,自动保存为csv文件,编码为utf-8-sig"""
        df = pd.DataFrame(self.data)
        df.to_csv(self.result_file, mode="a",index=False, encoding='utf-8-sig',header=self.header_csv)
        self.header_csv = False

    def process(self):
        """处理数据,生成nodes结尾的csv,用于绘图"""
        df = pd.read_csv(self.result_file)
        # df = pd.read_csv("./WeiBo_data/test.csv")
        nodes = []
        for index, row in df.iterrows():
            row["user_name"] = "@" + row["user_name"]
            if str(row["content"]) == "nan":
                tempt = {
                    "first": self.topic,
                    "second": row["user_name"],
                }
                nodes.append(tempt)
            else:
                send_list = []
                for i in str(row["content"]).split(r"//"):
                    if i!="" and "@" ==i[0]:
                        send_list.append(re.sub("[：:].*", "", i).strip())
                # print(send_list)
                # 转发指向
                if self.auto_direct_topic and len(send_list) > 0:
                    try :
                        nodes.append({
                            "first": self.topic,
                            "second": send_list[len(send_list) - 1],
                        })
                    except IndexError :
                        print(row["user_name"])
                        print(index)

                for i in range(len(send_list) - 1, 0, -1):
                    tempt = {
                        # 防止被excel当作公式
                        "first": send_list[i],
                        "second": send_list[i - 1],
                    }

                    nodes.append(tempt)
                if len(send_list) > 0: # 转发只有回复
                    nodes.append({
                    "first": send_list[0],
                    "second": row["user_name"],
                    })
                else:
                    nodes.append({
                    "first": self.topic,
                    "second": row["user_name"],
                })
                # print(str(row["content"]).split(r"//"))

        pd.DataFrame(nodes).to_csv(self.result_file.replace(".csv", "_nodes.csv"), index=False, encoding='utf-8-sig')
        # print(str(row["content"]).split(r"//"))


if __name__ == '__main__':
    weibo = Weibo()
    weibo.crawl()
    weibo.process()
    print('done')

