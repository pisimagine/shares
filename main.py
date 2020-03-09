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
results = em.GetBalance('SZ300822')
for result in results:
	db.Insert_Record(result,'balance')
db.close()
