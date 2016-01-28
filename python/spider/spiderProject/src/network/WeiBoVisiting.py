import urllib2
import cookielib
import urllib
import sys

reload(sys)
# sys.set

cookiejar = cookielib.MozillaCookieJar()
cookieSupport = urllib2.HTTPCookieProcessor(cookiejar)

httpHandler = urllib2.HTTPHandler(debuglevel=1)
httpsHander = urllib2.HTTPSHandler(debuglevel=1)

opener = urllib2.build_opener(cookieSupport, httpHandler)
urllib2.install_opener(opener)

loginUrl = "http://weibo.com/"
postUrl = "http://weibo.com/login.php"

loginCookies = urllib2.urlopen(loginUrl)
print(cookiejar)

# cookies = ''
# for index,cookies in enumerate(cookiejar):
#     cookies = cookies + cookies.name + "="+cookies.value+";"

# print(cookies)
# cookie = cookies[:-1]
# print("cookies:", cookie)
