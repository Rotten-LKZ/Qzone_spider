
import spider

getQQ = 0
fromQQ = 0
cookies = ''

i = spider.Spider(getQQ, fromQQ, cookies)
print(i.get_album_list())
