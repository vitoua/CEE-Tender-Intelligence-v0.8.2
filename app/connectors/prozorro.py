from datetime import datetime
import httpx
from app.core import Tender
B='https://public-api.prozorro.gov.ua/api/2.5/tenders'
def dt(v):
 try:return datetime.fromisoformat(str(v).replace('Z','+00:00')).replace(tzinfo=None)
 except:return None
async def fetch(countries=None,limit=40):
 out=[]
 async with httpx.AsyncClient(timeout=45) as c:
  f=await c.get(B,params={'limit':limit,'descending':1});f.raise_for_status()
  for row in f.json().get('data',[]):
   r=await c.get(f"{B}/{row['id']}");r.raise_for_status();x=r.json().get('data',{});no=x.get('tenderID',row['id']);url=f'https://prozorro.gov.ua/tender/{no}';out.append(Tender('prozorro:'+no,'prozorro','UKR',x.get('title') or no,(x.get('procuringEntity') or {}).get('name',''),deadline=dt((x.get('tenderPeriod') or {}).get('endDate')),status=x.get('status','active'),url=url,description=x.get('description',''),procurement_id=no))
 return out
