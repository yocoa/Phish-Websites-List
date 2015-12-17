# -*- coding: utf-8 -*  中文注释
import sys
import urllib2,httplib
import re
import smtplib,email 
from email.Message import Message
import getopt
import time

TARGET_URL = "http://www.phishtank.com/"

cur_date=time.strftime('%Y-%m-%d',time.localtime( time.time() ))
cur_time=time.strftime('%H-%M-%S',time.localtime( time.time() ))
SAVE_FILE = cur_date+"-"+cur_time+".txt"

smtpserver='smtp.163.com' #SMTP服务器根据具体情况修改
smtpuser='<sender@example.com>' #添加发送邮件人的EMAIL地址
smtppass='<password of sender@example.com>'     #添加上面邮箱的密码
smtpport='25' #SMTP的端口也根据具体情况修改
receviers=['receiver1@example.com','receiver2@example.com'] #添加收件人的邮箱，可以是多个。

total_num=5 

def connect(): 
	"connect to smtp server and return a smtplib.SMTP instance object" 
	server=smtplib.SMTP(smtpserver,smtpport) 
	server.ehlo() 
	server.login(smtpuser,smtppass) 
	return server 

def sendmessage(server,destination,subj,content): 
	"using server send a email" 
	msg=Message() 
	msg['Mime-Version']='1.0' 
	msg['From']=smtpuser 
	msg['To']=destination 
	msg['Subject']=subj 
	msg['Date']=email.Utils.formatdate() 
	msg.set_payload(content) 
	try: 
		failed=server.sendmail(smtpuser,destination,str(msg)) 
	except Exception,ex: 
		print Exception,ex 
		print 'Error - send failed' 
	else: 
		print "send success to " + destination

def sendemail():
	subj='Phishing Websites List' 
	content=open(SAVE_FILE).read()
	server=connect()
	for destination in receviers: 
		sendmessage(server,destination,subj,content)

def getcontent(id):
	'Done:Get the detail URL'
	
	url = TARGET_URL+"phish_detail.php?phish_id="+str(id)	
	header = {
	'Host': 'www.phishtank.com',
	'Connection': 'keep-alive',
	'Cache-Control': 'max-age=0',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36',
	'Referer': 'http://www.phishtank.com/',
	'Accept-Encoding': 'deflate',
	'Accept-Language': 'zh-CN,zh;q=0.8',
	'Cookie': 'PHPSESSID=a6273c454896a2a297331cbebeb2d2b8; __utmt=1; __utma=32426495.1485951876.1450230798.1450243687.1450251241.4; __utmb=32426495.1.10.1450251241; __utmc=32426495; __utmz=32426495.1450243687.3.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic'
	}
	req = urllib2.Request(url,None,header)
	response = urllib2.urlopen(req)
	htmlpage = response.read()
	match = re.compile(r'<b>http.*?</b>',re.DOTALL).findall(htmlpage)
	result = match[0][3:-4]
	print result
	fobj = open(SAVE_FILE,'a')
	print >> fobj,result
	fobj.close()

def getmaxnumber(url):
	'DONE:Get the biggest index num at this time.'
	header = {
	'Host': 'www.phishtank.com',
	'Connection': 'keep-alive',
	'Cache-Control': 'max-age=0',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36',
	'Accept-Encoding': 'deflate',
	'Accept-Language': 'zh-CN,zh;q=0.8',
	'Cookie': 'PHPSESSID=a6273c454896a2a297331cbebeb2d2b8; __utmt=1; __utma=32426495.1485951876.1450230798.1450230798.1450234449.2; __utmb=32426495.5.10.1450234449; __utmc=32426495; __utmz=32426495.1450234449.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic'
	}
	req = urllib2.Request(url,None,header)
	response = urllib2.urlopen(req)
	htmlpage = response.read()
	match = re.search(r"phish_detail.php\?phish_id=(\d+)",htmlpage)        
	if match:
		result_num = match.group(1)
		return result_num
	
def usage():
	print sys.argv[0] + """ -n <phish_websites_numbers>
	"""
	sys.exit(1)

def main():
	global total_num
	try:
		cmd_opts = "n:"
		opts, args = getopt.getopt(sys.argv[1:], cmd_opts)
	except getopt.GetoptError:
		usage()
	
	for opt in opts:
		if opt[0] == "-n":
			total_num = opt[1]
		else:
			usage()
	
	maxnum = getmaxnumber(TARGET_URL)
	maxnum = int(maxnum)
	minmun = maxnum-int(total_num)+1
	for i in range(minmun,maxnum+1):
		getcontent(i)
	sendemail()

if __name__=="__main__":
	main()