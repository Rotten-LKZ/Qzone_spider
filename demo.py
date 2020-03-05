
import json

import requests

import makefile

global con
with open("content.txt", 'r', encoding='utf-8') as f:
    con = f.read()
    # print(con)
    con = json.loads(con)
f.close()


def get_album(gq, alid):
    resu = con
    totalInAlbum = resu['data']['totalInAlbum']
    photoList = resu['data']['photoList']
    albumname = resu['data']['topic']['name']
    desc = ''
    mks = makefile.MakeST(gq)
    cookies = ''
    for i in photoList:
        a = True
        if desc != i['desc']:
            desc = i['desc']
            a = False
        print(i)
        path = '{}/{}'.format(albumname, i['batchId'])
        mks.make_dir(path)
        if i['is_video']:
            mks.make_file(path, "{}.mp4".format(str(i['rawshoottime']).replace(":", "-")), "mp4",
                          get_content(i['url'], cookies))
        else:
            mks.make_file(path, "{}.jpg".format(str(i['rawshoottime']).replace(":", "-")), "jpg",
                          get_content(i['url'], cookies))

        if a:
            mks.make_txt_a(path, "Info.txt",
                           "文字:{}\n"
                           "图片链接：{}\n"
                           "照相时间：{}\n"
                           "发布时间：{}\n"
                           "拍摄设备：{}\n"
                           "iso：{}\n\n".format(i['desc'], i['url'], i['rawshoottime'], i['uploadtime'],
                                               i['exif']['model'], i['exif']['iso']))
        else:
            mks.make_txt_a(path, "Info.txt",
                           "相册名：{}\n"
                           "相册照片总数：{}\n"
                           "相册ID：{}\n\n"
                           "文字：{}\n"
                           "图片链接：{}\n"
                           "照相时间：{}\n"
                           "发布时间：{}\n"
                           "拍摄设备：{}\n"
                           "iso：{}\n\n".format(albumname, totalInAlbum, alid, i['desc'], i['url'],
                                               i['rawshoottime'], i['uploadtime'], i['exif']['model'],
                                               i['exif']['iso']))


def get_content(url, cookies):
    # header = {
    #     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
    #                 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    #     'cookie': cookies}
    header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    result = requests.get(url, headers=header)
    return result.content


if __name__ == "__main__":
    get_album(2603091731, 'V108HyLh1DeKD5')
