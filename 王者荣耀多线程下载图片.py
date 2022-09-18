from urllib import parse
import requests
import threading
from queue import Queue
import os
from urllib import request

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36',
    'referer': 'https://pvp.qq.com/web201605/wallpaper.shtml'  # 对于动态网页要加上referer，这个值是当前网页的网址
}


def exact_url(data):
    image_url_list = []
    for i in range(1, 9):  # 下载图片地址中的八张大小不同的图片，
        image_url = parse.unquote(data['sProdImgNo_{}'.format(i)]).replace('200', '0')  # 数据解析和处理
        image_url_list.append(image_url)
    return image_url_list


# 生产者线程(放)
class Produce(threading.Thread):
    def __init__(self, page_queue, image_url_queue):
        super().__init__()
        self.page_queue = page_queue
        self.image_url_queue = image_url_queue

    def run(self):
        while not self.page_queue.empty():
            page_url = self.page_queue.get()
            resp = requests.get(page_url, headers=headers)
            json_data = resp.json()  # 解析数据，转换成json格式
            d = {}  # 定义一个字典
            data_lst = json_data['List']  # 查找到List标签，并且获取其中的值
            for data in data_lst:  # 遍历获取到的list标签的数据
                image_url_list = exact_url(data)  # 调佣自定义的exact_utl函数，从中的到该data的图片url网址
                sProdName = parse.unquote(data['sProdName'])  # 该图片的名称
                d[sProdName] = image_url_list  # 在字典中添加图片名字
            for key in d:  # 遍历d字典中的图片名字
                dirpath = os.path.join('image', key.strip(' '))  # 存放地址image，拼接存放地址，加上图片名字
                if not os.path.exists(dirpath):  # 判断dipahth是否存在
                    os.mkdir(dirpath)  # 创建该图片名字作为目录名字
                for index, image_url in enumerate(d[key]):  # index索引，image_url是图片url
                    # enumerate表示的是每次循环都获得一次index和image_url
                    # 生产图片的url
                    self.image_url_queue.put(  # 将生产的图片的url放入，并且命名，image_path:是图片存放路径，.jpg是图片名称以及后缀名，image_url是图片网址
                        {'image_path': os.path.join(dirpath, f"{index + 1}.jpg"), 'image_url': image_url})
                    print('{}下载完毕'.format(d[key][index]))


# 消费者线程(取)
class Customer(threading.Thread):
    def __init__(self, image_url_queue):
        super().__init__()
        self.image_url_queue = image_url_queue

    def run(self):
        while True:
            try:
                image_obj = self.image_url_queue.get(timeout=20)  # 检测时间，20秒结束
                request.urlretrieve(image_obj['image_url'], image_obj['image_path'])  # 从image_url下载到image_path的路径中
                print(f'{image_obj["image_path"]}下载完成')
            except:
                break  # 结束下载


def start():  # 开始程序
    page_queue = Queue(2)
    image_url_queue = Queue(1000)
    for i in range(1, 2):
        page_url = f'https://apps.game.qq.com/cgi-bin/ams/module/ishow/V1.0/query/workList_inc.cgi?activityId=2735&sVerifyCode=ABCD&sDataType=JSON&iListNum=20&totalpage=0&page={i}&iOrder=0&iSortNumClose=1&iAMSActivityId=51991&_everyRead=true&iTypeId=2&iFlowId=267733&iActId=2735&iModuleId=2735&_=1595215093279'
        # print(page_url)
        page_queue.put(page_url)

    # 创建生产者对象，五个生产者线程对象
    for i in range(5):
        t = Produce(page_queue, image_url_queue)
        t.start()

    # 创建消费者对象，十个线程对象
    for i in range(10):
        t = Customer(image_url_queue)
        t.start()


if __name__ == '__main__':
    start()
