import public
from spider import EastMoney
from DBoperate import DB

# cn = CNINF()
# db = DB()
# db.Initialize_Share()
# shareList = cn.GetShareList()
em = EastMoney()
db = DB()
db.Initialize_Share()
results = em.GetFinancialData('SZ300822')
for key in results:
	for record in results[key]:
		db.Insert_Record(record,key)
