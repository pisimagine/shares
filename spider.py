import requests
import public
import json
import time
import re

class CNINF:			#垃圾、浪费表情。信息更新不及时。。。
	def __init__(self):
		self.s = requests.session()
	
	def GetShareList(self):
		shareListUrl = 'http://www.cninfo.com.cn/data/yellowpages/getYellowpageStockList'
		data = self.Get_Data(shareListUrl)
		data = json.loads(data)
		shareList = []
		for result in data['records']:
			shareList = shareList + [result['SECCODE']]
		return shareList
	
	def GetFinancialData(self,shareCode):
		financialDataUrl = 'http://www.cninfo.com.cn/data/yellowpages/singleStockData?scode=' + shareCode +'&mergerMark=financeData'
		#返回股票的财务报表：平衡表、利润表、现金流
		data = self.Get_Data(financialDataUrl)
		data = json.loads(data)
		financialData = []
		for tableName in data:				#tableName:assetsData、cashFlowData、profitsData
			for record in data[tableName]: 		#list[0、1、2、3、4....
				for columnName in record:		#2008、2009、2010、		
					print("飞起")
		return data
		
	def GetDividendData(self,shareCode):
		dividendUrl = 'http://www.cninfo.com.cn/data/yellowpages/singleStockData?scode=' + shareCode + '&mergerMark=shareData'
		data = self.Get_Data(dividendUrl)
		return data
		
	def GetHolderData(self,shareCode):
		holderUrl = 'http://www.cninfo.com.cn/data/yellowpages/singleStockData?scode=' + shareCode + '&mergerMark=shareHoldersData'
		data = self.Get_Data(holderUrl)
		return data
		
	def GetBasicInfData(self,shareCode):
		bsInfUrl = 'http://www.cninfo.com.cn/data/yellowpages/getIndexData?scode=' + shareCode
		data = self.Get_Data(bsInfUrl)
		data = json.loads(data)
		basicInf = {}
		print(shareCode)
		
		# if(data["cninfo5023Data"]==[]):
			# basicInf['BUSINESS_OVERVIEW'] = ""
			# basicInf['COMPANY_ADVANTAGE'] = ""
			# basicInf['RISK_TIPS'] = ""
		# else:
			# basicInf['BUSINESS_OVERVIEW'] = str(data["cninfo5023Data"][0]['F001V'])		#业务概况
			# basicInf['BUSINESS_OVERVIEW'] = r"/x"+r'/x'.join([hex(ord(c)).replace('0x', '') for c in basicInf['BUSINESS_OVERVIEW']])
			# basicInf['COMPANY_ADVANTAGE'] = str(data["cninfo5023Data"][0]['F002V'])		#公司亮点
			# basicInf['BUSINESS_OVERVIEW'] = r"/x"+r'/x'.join([hex(ord(c)).replace('0x', '') for c in basicInf['COMPANY_ADVANTAGE']])
			# basicInf['RISK_TIPS'] = str(data["cninfo5023Data"][0]['F003V'])		#风险提示
			# basicInf['RISK_TIPS'] = r"/x"+r'/x'.join([hex(ord(c)).replace('0x', '') for c in basicInf['RISK_TIPS']])
		
		if(data["cninfo5025Data"]==[]):
			basicInf['CHAIRMAN'] = ""
			basicInf['GENERAL_MANAGER'] = ""
			basicInf['FINANCIAL_CONTROL'] = ""
			basicInf['BOARD_SECRETARY'] = ""
			# basicInf['BOARD_MEMBERS'] = ""
		else:
			basicInf['CHAIRMAN'] = replace(data["cninfo5025Data"][0]['F001V']," ","")		#董事长
			basicInf['GENERAL_MANAGER'] = replace(data["cninfo5025Data"][0]['F002V']," ","")		#总经理
			basicInf['FINANCIAL_CONTROL'] = replace(data["cninfo5025Data"][0]['F003V']," ","")		#财务总监
			basicInf['BOARD_SECRETARY'] = replace(data["cninfo5025Data"][0]['F004V']," ","")		#董事会秘书
			# basicInf['BOARD_MEMBERS'] = data["cninfo5025Data"][0]['F005V']		#董事会成员
			# basicInf['BOARD_MEMBERS'] = r"/x"+r'/x'.join([hex(ord(c)).replace('0x', '') for c in basicInf['BOARD_MEMBERS']])
		
		basicInf['SHARE_CODE'] = replace(data["codeInfo"]['SECCODE']," ","")		#股票代码
		basicInf['COMPANY_NAME'] = replace(data["codeInfo"]['ORGNAME']," ","")		#公司名称
		basicInf['SHARE_NAME'] = replace(data["codeInfo"]['SECNAME']," ","")		#股票名称（简称）
		basicInf['SHARE_ABBR'] = replace(data["codeInfo"]['F001V']," ","")		#股票缩写
		
		if(data["snapshot5015Data"] == []):
			basicInf['ISIN'] = ""
			basicInf['ESTABLISH_DATE'] = ""
			basicInf['LISTING_DATE'] = ""
			basicInf['INDUSTRY'] = ""
			basicInf['SUBDIVISION_INDUSTRY'] = ""
			basicInf['MARKET'] = ""
		else:
			basicInf['ISIN'] = replace(data["snapshot5015Data"][0]['F001V']," ","")		#ISIN编码
			basicInf['ESTABLISH_DATE'] = replace(data["snapshot5015Data"][0]['F002V']," ","")	#成立日期
			basicInf['LISTING_DATE'] = replace(data["snapshot5015Data"][0]['F003V']," ","")		#上市日期
			basicInf['INDUSTRY'] = replace(data["snapshot5015Data"][0]['F010V']," ","")			#所属行业
			basicInf['SUBDIVISION_INDUSTRY'] = replace(data["snapshot5015Data"][0]['F011V']," ","")			#细分行业
			basicInf['MARKET'] = replace(data["snapshot5015Data"][0]['F012V']," ","")	#所属市场
		print("=="*60)
		return basicInf
	
	def Get_Data(self,url):
		s = self.s
		data = s.get(url)
		time.sleep(1)
		return data.text

class EastMoney:
	def __init__(self):
		self.session = requests.session()
	
	def GetBalance(self,shareCode):		#获得资产负债表
		'''
			#传入参数	：	股票代码，格式为SHXXXXXX或SZXXXXXX
			#返回值	：	列表，列表元素为字典
		'''
		financeUrl = 'http://f10.eastmoney.com/f10_v2/FinanceAnalysis.aspx?code=' + shareCode		#此处为个股详情的url
		print(financeUrl)
		pageSrc = self.GetSource(financeUrl)	
		if(pageSrc == False):
			return False
		companyType = re.search(r'id="hidctype".*?value="(4)"',pageSrc,re.S)
		if(companyType != None):
			companyType = companyType.group(1)
		else:
			public.writeLog("正则匹配时未找到" + shareCode + "的公司类型")
			return False
		url = 'http://f10.eastmoney.com/NewFinanceAnalysis/zcfzbAjax?companyType='+ companyType + '&reportDateType=0&reportType=1&endDate=&code=' +shareCode
		data = self.GetSource(url)
		if(data == False):
			return False
		data = json.loads(data)
		data = json.loads(data)		#需要两次json解析才能得到list
		'''
		数据说明：data为列表，列表内有多个元素，每个元素均为字典，字典内：
			#SUMLASSET -->流动资产合计；SUMNONLASSET-->固定资产合计；SUMASSET-->资产合计；
			#SUMLLIAB-->流动负债合计；SUMNONLLIAB-->非流动负债合计；SUMLIAB-->负债合计；
			#SUMSHEQUITY-->股东权益合计
		'''
		abbrList = []
		for balance in data:
			abbrList = abbrList + [{'SUMLASSET':balance["SUMLASSET"],"SUMNONLASSET":balance["SUMNONLASSET"],"SUMASSET":balance["SUMASSET"]}]
		
		return abbrList
		
	
	def GetSource(self,url):
		session = self.session
		try:
			pageSrc = session.get(url,timeout = 5)
		except Exception as e:
			public.writeLog('在请求"'+url+'"时出错：' + str(e))
			return False
		else:
			return pageSrc.text

def test():
	em = EastMoney()
	# data = c.BasicInfUrl('300339')
	# for key in data:
		# print("=="*60)
		# print(key + "： " + data[key])
	em.GetBalance('SZ300822')
		
    
#test()

