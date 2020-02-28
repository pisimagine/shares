import requests

financialDataUrl = 'http://www.cninfo.com.cn/data/yellowpages/singleStockData?scode=300339&mergerMark=financeData'
	#返回股票的财务报表：平衡表、利润表、现金流
incomeUrl = 'http://www.cninfo.com.cn/data/yellowpages/singleStockData?scode=300339&mergerMark=incomeData'
	#返回股票的营业收入
dividendUrl = 'http://www.cninfo.com.cn/data/yellowpages/singleStockData?scode=300339&mergerMark=dividendData'
	#返回股票分红数据
shareUrl = 'http://www.cninfo.com.cn/data/yellowpages/singleStockData?scode=300339&mergerMark=shareData'
	#每股数据：每股收益、每股最高成交价、每股最低成交价
shareHolderUrl = 'http://www.cninfo.com.cn/data/yellowpages/singleStockData?scode=300339&mergerMark=shareHoldersData'
	#前五大股东数据
cninfoUrl = 'http://www.cninfo.com.cn/data/yellowpages/getIndexData?scode=300339'
	#基本信息：业务、交易信息、董事及高管
