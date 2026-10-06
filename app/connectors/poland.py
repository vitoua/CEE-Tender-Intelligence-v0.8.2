from datetime import datetime
import httpx
from app.core import Tender
URL='https://ezamowienia.gov.pl/mo-board/api/v1/notice'
def dt(v):
 try:return datetime.fromisoformat(str(v).replace('Z','+00:00')).replace(tzinfo=None)
 except:return None
def p(x,*ks):
 for k in ks:
  if isinstance(x,dict) and x.get(k) not in (None,''):return x[k]
 return ''
async def fetch(countries=None,limit=100):
 variants=['ContractNotice','1','NoticeOfContract','Ogłoszenie o zamówieniu'];last=''
 async with httpx.AsyncClient(timeout=45,follow_redirects=True) as c:
  for nt in variants:
   r=await c.get(URL,params={'PageSize':limit,'PageNumber':1,'NoticeType':nt})
   if r.status_code==200:break
   last=f'NoticeType={nt}; HTTP {r.status_code}: {r.text[:800]}'
  else:raise RuntimeError('BZP API: '+last)
 body=r.json();rows=body if isinstance(body,list) else body.get('items') or body.get('data') or body.get('results') or body.get('content') or [];out=[];now=datetime.utcnow()
 for x in rows:
  no=str(p(x,'noticeNumber','noticeId','id','bzpNumber'));ddl=dt(p(x,'submissionDeadline','deadline'))
  if ddl and ddl<now:continue
  buyer=p(x,'organizationName','buyerName');url=str(p(x,'noticeUrl','url')) or f'https://ezamowienia.gov.pl/mo-client-board/bzp/notice-details/{no}';out.append(Tender('pl:'+no,'poland','POL',str(p(x,'orderObject','title','noticeTitle') or no),str(buyer),deadline=ddl,url=url,description=str(p(x,'description')),procurement_id=no))
 return out
