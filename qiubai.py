import requests
import re
import traceback


class QSBK:
    def __init__(self):
        self.pageIndex = 1
        self.userAgent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        self.headers = {'User-Agent':self.userAgent}
        self.stories = []
        self.enable = False

    def getPage(self, pageIndex):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
            r = requests.get(url, headers=self.headers)
            r.raise_for_status()
            r.encoding = 'utf-8'
            return r.text
        except:
            traceback.print_exc()
            print("fuck it,获得获得网页错误，返回None")
            return None

    def getPageItems(self, pageIndex):
        pageHTML = self.getPage(pageIndex)
        if not pageHTML:
            print("草！从getPage获得网页为空，我也只能返回None了")
            return None
        pattern = re.compile('<div class=\"article.*?h2>(.*?)<.*?<span>(.*?)</.*?number\">(.*?)</', re.S)
        items = re.findall(pattern, pageHTML)
        pageStories = []

        replaceBR = re.compile('<br/>')
        for item in items:
            text = re.sub(replaceBR,"\n", item[1])
            pageStories.append([item[0].strip(), text.strip(), item[2].strip()])
        return pageStories

    def loadPage(self):
        if self.enable==True:
            if(len(self.stories)<2):
                pageStories = self.getPageItems(self.pageIndex)
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex += 1
    def getOneStory(self, pageStories, page):
        for story in pageStories:
            input_ = input()
            self.loadPage()
            if input_ == 'Q':
                self.enable = False
                return
            print("第%d页\t发布人： %s\t 赞：%s \n %s"%(page, story[0], story[2], story[1]))

    def start(self):
        print("正在读取，回车查看，输入Q结束")
        self.enable = True
        self.loadPage()
        nowPage = 0
        while self.enable:
            if len(self.stories)>0:
                pageStories = self.stories[0]
                nowPage += 1
                del self.stories[0]
                self.getOneStory(pageStories, nowPage)

spider = QSBK()
spider.start()