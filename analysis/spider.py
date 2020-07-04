import requests
from bs4 import BeautifulSoup
import re


class Spider:
    content = ''

    def html_downloader(self, url):
        headers = {'user-agent': 'Mozilla/5.0'}
        response = requests.get(url=url, headers=headers)
        response.encoding = 'utf-8'
        self.content = response.text

    def parser(self):
        list = []
        if None is self.content:
            return None
        soup = BeautifulSoup(self.content, 'html.parser')
        comments = soup.select('.comment > p')
        if len(comments) == 0:
            return None
        for comment in comments:
            list.append(comment.get_text().strip().replace('\n', ''))
        return list

    def get_count(self, url):
        headers = {'user-agent': 'Mozilla/5.0'}
        response = requests.get(url=url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        count = soup.select('.CommentTabs > li > span')[0].get_text()
        count = count.split('(')[1].split(')')[0]
        return count

    def url_dispose(self, raw_url):
        if 'movie.douban.com/subject/' not in str(raw_url):
            return None
        url = []
        url.append('https://movie.douban.com/subject/')
        url.append(re.findall('\d+', raw_url)[0])
        url.append('/comments?start=')
        url.append('&limit=20&sort=new_score&status=P')
        return url


def spider_excute(raw_url):
    list = []
    start = 0
    spider = Spider()
    url = spider.url_dispose(raw_url)
    if None is url:
        return None
    count = spider.get_count(url[0] + url[1] + '/comments?status=P')
    if None is count:
        return None

    while int(start)<=int(count):
        patch_url = url[0]+url[1]+url[2]+str(start)+url[3]
        spider.html_downloader(patch_url)
        list+=spider.parser()

        if start>=200:
            break
        start+=20
    return list


# if __name__ == '__main__':
#     url = 'https://movie.douban.com/subject/26930504/'
#     spider_excute(url)

