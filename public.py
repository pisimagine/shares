import os
import datetime


def createPath(path):
	path=path.strip()	#去掉收尾空格
	path=path.rstrip("\\")		#去掉尾部的\
	if os.path.exists(path):
		return False	#已存在，返回False
	else:
		os.makedirs(path)
		return True
		
def writeLog(content):
	folderPath = os.path.join(os.getcwd(),'record','Log')
	createPath(folderPath)
	nowDate = datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d")	#获取当前时间并转化为str，输出格式：YYYY/mm/dd
	logPath =os.path.join(folderPath,nowDate + '.txt')
	with open(logPath,'a+',encoding='utf-8') as Log:
		nowTime = datetime.datetime.strftime(datetime.datetime.now(),"%H:%M:%S")	#获取当前时间并转化为str，输出格式：HH/MM/SS
		content = nowTime + ' >> ' + content + '\n'
		Log.write(content)

def test():
	writeLog("口吐芬芳，我去你妈的")
	
	
#test()
