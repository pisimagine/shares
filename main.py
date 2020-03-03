import public
from spider import CNINF
from DBoperate import DB

cn = CNINF()
db = DB()
db.Initialize_Share()
shareList = cn.GetShareList()

for shareCode in shareList:
	basicInf = cn.GetBasicInfData(shareCode)
	db.Update_Record(basicInf,'basicInf')
db.close()
