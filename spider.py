
import json
import time

import requests

import getGTK
import makefile


class SpiderList:
    gq = 0
    qq = 0
    cookies = ''
    gtk = ''

    def __init__(self, get_qq, from_qq, from_cookie):
        self.gq = get_qq
        self.qq = from_qq
        self.cookies = from_cookie
        self.gtk = getGTK.getGTK(from_cookie)

    def get_album_list(self):
        __ts = int(round(time.time() * 1000))
        __gq = self.gq
        __qq = self.qq
        __gtk = self.gtk

        header = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
            'cookie': self.cookies}
        url = 'https://user.qzone.qq.com/proxy/domain/photo.qzone.qq.com/fcgi-bin/fcg_list_album_v3?g_tk={}' \
              '&callback=shine0_Callback&hostUin={}&uin={}&appid=4&inCharset=utf-8&outCharset=utf-8&source=qzone&' \
              'plat=qzone&format=json&notice=0&filter=1&handset=4&pageNumModeSort=40&pageNumModeClass=15' \
              '&needUserInfo=1&idcNum=4&callbackFun=shine0&_={}'.format(__gtk, __gq, __qq, __ts)
        # url = f'https://user.qzone.qq.com/proxy/domain/photo.qzone.qq.com/fcgi-bin/fcg_list_album_v3?g_tk={__gtk}' \
        #       f'&callback=shine0_Callback&hostUin={__gq}&uin={__qq}&appid=4&inCharset=utf-8&outCharset=utf-8' \
        #       f'&source=qzone&plat=qzone&format=json&notice=0&filter=1&handset=4&pageNumModeSort=40' \
        #       f'&pageNumModeClass=15' \
        #       f'&needUserInfo=1&idcNum=4&callbackFun=shine0&_={__ts}'

        res = requests.get(url, headers=header)
        # print(res.text)
        res = json.loads(res.text)
        re = {}
        id_ = []
        name = []
        createtime = []
        lastuploadtime = []
        modifytime = []
        pre = []

        for i in res['data']['albumListModeSort']:
            if 'question' not in i.keys():
                id_.append(i['id'])
                name.append(i['name'])
                createtime.append(i['createtime'])
                lastuploadtime.append(i['lastuploadtime'])
                modifytime.append(i['modifytime'])
                pre.append(i['pre'].replace('/a/', '/b/'))

        re['id'] = id_
        re['name'] = name
        re['createtime'] = createtime
        re['lastuploadtime'] = lastuploadtime
        re['modifytime'] = modifytime
        re['pre'] = pre

        return re


class SpiderCover:
    header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}

    def get_cover(self, url):
        result = requests.get(url, headers=self.header)
        return result.content


def get_content(alid, gq, fq, cookies):
    """

    Args:
        alid: 相册ID
        gq: 需要获取的QQ
        fq: 爬取的QQ
        cookies: 用户Cookie
    """
    header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'cookie':cookies}
    __ts = int(round(time.time() * 1000))
    __gtk = getGTK.getGTK(cookies)

    resu = requests.get("https://h5.qzone.qq.com/proxy/domain/photo.qzone.qq.com/fcgi-bin/cgi_list_photo?"
                        "g_tk={}&callback=shine0_Callback&t=986281408&mode=0&idcNum=4"
                        "&hostUin={}&topicId={}&noTopic=0&uin={}&pageStart=0"
                        "&pageNum=99999999999999&skipCmtCount=0&singleurl=1&batchId=&notice=0&appid=4&inCharset=utf-8"
                        "&outCharset=utf-8&source=qzone&plat=qzone&outstyle=json&format=json&json_esc=1&question=&"
                        "answer=&callbackFun=shine0&_={}".format(__gtk, gq, alid, fq, __ts), headers=header)

    resu = json.loads(resu.text)
    totalInAlbum = resu['data']['totalInAlbum']
    photoList = resu['data']['photoList']
    desc = []
    is_video = []
    pre = []
    rawshoottime = []
    
    for i in photoList:
        pass

def get_time(ts):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))


if __name__ == "__main__":
    getQQ = 0
    cookies = ''
    s = SpiderList(getQQ, 0,
                    cookies)
    res = s.get_album_list()
    print(res)
    # print(type(res))
    mst = makefile.MakeST(getQQ)
    sc = SpiderCover()

    for name, pre, ctime, lutime, mdtime, ID in zip(res['name'], res['pre'], res['createtime'], res['lastuploadtime'], res['modifytime'], res['id']):
        # print(i)
        # print(e)
        mst.make_dir(name)
        mst.make_dir("{}/AlbumInfo".format(name))
        mst.make_file("{}/AlbumInfo".format(name), "Cover.jpg", "jpg", sc.get_cover(pre))
        mst.make_file("{}/AlbumInfo".format(name), "Info.txt", "txt",
                      "相册名字：{}\n"
                      "相册创建时间：{}\n"
                      "相册最后上传时间：{}\n"
                      "相册修改时间：{}\n"
                      "相册封面图片地址：{}\n"
                      "相册ID：{}".format(name, get_time(ctime), get_time(lutime), get_time(mdtime), pre, ID))
