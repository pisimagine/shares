import pymysql
import public
import sys
import re

class DB:
	def __init__(self):
		self.conn = pymysql.connect(host='127.0.0.1',port = 3306,user='root',passwd='Yjs3.1415926',charset='utf8',cursorclass=pymysql.cursors.DictCursor)
		self.cursor = self.conn.cursor()
		
	def Initialize_Share(self):
		conn = self.conn
		cursor = self.cursor
		dbName = "share"
		basicInf = "basicInf (ID int primary key auto_increment,UPDATE_TIME DATETIME not null,SHARE_CODE VarChar(45))"		#保存公司概况等基本信息
		balance = "balance (ID int primary key auto_increment,UPDATE_TIME DATETIME not null,SHARE_CODE VarChar(45))"	#保存资产负债表
		profit =  "profit (ID int primary key auto_increment,UPDATE_TIME DATETIME not null,SHARE_CODE VarChar(45))"	#保存利润表
		cashFlow =  "cashflow (ID int primary key auto_increment,UPDATE_TIME DATETIME not null,SHARE_CODE VarChar(45))"	#保存现金流表
		try:
			cursor.execute("create database if not exists %s;" % dbName)		#注意，mysql中【数据库名】和【表名】不能加''，故此处dbName不能作为cursor.execute的参数传入
			cursor.execute("use %s;" % dbName)			#选中债券信息数据表
			cursor.execute("create table if not exists %s;" % basicInf)
			cursor.execute("create table if not exists %s;" % balance)
			cursor.execute("create table if not exists %s;" % profit)
			cursor.execute("create table if not exists %s;" % cashFlow)
		except Exception as err:
			conn.rollback
			public.writeLog(str(err))
			return False
		else:
			return True
	
	def Update_Record(self,record,tableName):	#调用Compare_Record比较本地最新数据与网络数据是否相同，相同==>None,不同==>调用Insert_Record进行更新，成功==>True,失败==>False
		isDiff = self.Compare_Record(record,tableName)
		if(isDiff==None):
			return None
		else:
			flag = self.Insert_Record(record,tableName)
			return flag
	
	def Insert_Record(self,record,tableName):		#当本地数据与网络数据不符时，将网络数据更新到本地。更新成功==>True,失败==>False
		conn = self.conn 
		cursor = self.cursor
		
		if(isinstance(record,dict) != True):		#传入record参数不是dict变量，返回False
			public.writeLog("值错误:向" + tableName + "插入记录做比较时失败,Insert_Record(record,tableName)中record需传入dict变量")
			return False
			
		sqlColumns = []
		sqlValues = []
		columnHolder = []
		valueHolder = []
		for key in record.keys():
			if(record[key] == None):		#对nonetype进行预处理
				record[key] = ""
			sqlColumns = sqlColumns + [key.strip()]
			sqlValues = sqlValues + [record[key]]
			columnHolder = columnHolder + ["{}"]
			valueHolder = valueHolder + ["%s"]
		columnHolder = ",".join(columnHolder)
		valueHolder = ",".join(valueHolder)
		sql = "insert into {} ( UPDATE_TIME,{} ) values ( CURRENT_TIMESTAMP,{} );".format(tableName,columnHolder,valueHolder)
		sql = sql.format(*sqlColumns)
		try:
			cursor.execute(sql,sqlValues)	
			conn.commit()
		except Exception as err:
			conn.rollback()
			info = str(sys.exc_info()) 
			loseColumn = re.search("1054.*?column\s'(.*?)'.*?",info,re.S)		#当出现无字段1054错误时，增加该字段，然后回滚操作
			if(loseColumn != None):
				if self.Add_Column("share",tableName,loseColumn.group(1)):		
					self.Insert_Record(record,tableName)				#若增加字段成功，则重新执行该插入程序
				else:
					public.writeLog("发生数据库内部错误（1054：无相应字段）时，尝试用Add_Column()函数向数据库增加此字段，但未成功！")
					return False
			else:
				public.writeLog("发生错误："+ str(err))
				return 	False		#返回失败
		
	def Compare_Record(self,record,tableName):		#将传入函数的数据（record）与本地数据库中的最新数据（record）进行比较：不同==>返回True;相同==>返回None;失败==>返回False;
		try:
			conn = self.conn
			cursor = self.cursor
			
			if(isinstance(record,dict) !=True):		#判断record是否为dict变量
				public.write("值错误:和" + tableName + "中的记录做比较时失败,Compare_Record(record,tableName)中record需传入dict变量")
				return False
			
			sql = "select * from " +tableName+ " where %s = '%s' order by UPDATE_TIME desc;" % ("SHARE_CODE",record['SHARE_CODE'])
			cursor.execute(sql)
			result = cursor.fetchone()		#result[SHARE_CODE] == record[SHARE_CODE],且result[UPDATE_TIME]最大
			if(result == None):		#若本地不存在该证券记录，函数返回True
				return True
			else:
				for key in record:			#对比record中和result中的每一个值，若存在不同，则返回True
					if(record[key] != result[key]):
						return True
				return None		#record和result数据完全相同，返回False
		except Exception as err:
			public.writeLog(str(err))
			return False

	def Add_Column(self,databaseName,tableName,newColumnName):			#向本地数据库databaseName的数据表tableName中增加queryColumnName字段
		cursor = self.cursor
		conn = self.conn 
		cursor.execute("use %s;" % databaseName)
		try:
			sql = "ALTER TABLE %s add column %s varchar(45);" % (tableName,newColumnName)
			cursor.execute(sql)
			conn.commit()
		except:
			public.writeLog("错误：向数据库中写入新字段时失败！")
			conn.rollback()
			return False
		else:
			return True

	def close(self):
		conn = self.conn
		conn.close

	
