from Crypto.Cipher import AES
import base64
import binascii
from urllib.request import *
import urllib.parse
import json

# 这里并不需要JS中的parse
# 这两个函数参考 路人甲 的！https://www.zhihu.com/question/21471960
def aesEncrypt(text, secKey):
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encryptor = AES.new(secKey, 2, '0102030405060708')
    ciphertext = encryptor.encrypt(text)
    ciphertext = base64.b64encode(ciphertext)
    return ciphertext
def rsaEncrypt(text, pubKey, modulus):
    text = text[::-1]
    text=binascii.hexlify(text)
    rs = int( text,16)**int(pubKey, 16) % int(modulus, 16)
    return format(rs, 'x').zfill(256)


p1='{"rid":"R_SO_4_66842","offset":"0","total":"true","limit":"20","csrf_token":""}'
# 以下参数是固定的，参考https://www.jianshu.com/p/155112988fe9
p2=b"010001"
p3='00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
p4='0CoJUm6Qyw8W8jud'
i=b'aaaaaaaaaaaaaaaa'

p5=aesEncrypt(p1,p4)
p5=str(p5,'ascii')
params=aesEncrypt(p5,i)
params=str(params,'ascii')
encSecKey=rsaEncrypt(i,p2,p3)
url='http://music.163.com/weapi/v1/resource/comments/R_SO_4_66842'
#这里经过 wuhtt的文章(http://www.jianshu.com/p/2146469bb29c)提醒加上两个字段
myheaders = {
    'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    'Origin':'http://music.163.com',
    'Content-Type':'application/x-www-form-urlencoded',
}#浏览器请求头

data={
    'params':params,
    'encSecKey':encSecKey
}
request=Request(url,headers=myheaders,data=urllib.parse.urlencode(data).encode(encoding='UTF8'))
response=urlopen(request)
restext=json.load(response)
hotcomments=restext['hotComments']
for i in hotcomments:
    print(i['content'])