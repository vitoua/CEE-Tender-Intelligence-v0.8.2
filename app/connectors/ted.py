from datetime import datetime,timedelta
import httpx
from app.core import Tender
URL='https://api.ted.europa.eu/v3/notices/search';LANGS=('eng','en','pol','ukr','uk','deu','fra','spa','ita')
def first(v):
 if isinstance(v,dict):
  for k in LANGS:
   if v.get(k):return first(v[k])
  return first(next(iter(v.values()),''))
 if isinstance(v,list):return first(v[0]) if v else ''
 return str(v or '')
def dt(v):
 try:return datetime.fromisoformat(first(v)[:10])
 except:return None
async def fetch(countries=None,limit=200):
 fields=['publication-number','notice-title','buyer-name','buyer-country','publication-date','deadline','description-proc','form-type'];q='FT~"SSD" OR FT~"NVMe" OR FT~"DDR4" OR FT~"DDR5" OR FT~"memory card"';payload={'query':q,'fields':fields,'page':1,'limit':limit,'scope':'ALL','paginationMode':'PAGE_NUMBER','onlyLatestVersions':True}
 async with httpx.AsyncClient(timeout=45) as c:r=await c.post(URL,json=payload)
 if r.status_code!=200:raise RuntimeError(f'TED HTTP {r.status_code}: {r.text[:800]}')
 out=[];now=datetime.utcnow();cut=now-timedelta(days=90)
 for x in r.json().get('notices',[]):
  co=first(x.get('buyer-country'))[:3] or 'EU';pub=dt(x.get('publication-date'));ddl=dt(x.get('deadline'));form=first(x.get('form-type')).lower()
  if countries and co not in countries or not pub or pub<cut or not ddl or ddl<now or any(z in form for z in ('result','award','completion')):continue
  no=first(x.get('publication-number'));url=f'https://ted.europa.eu/en/notice/-/detail/{no}';out.append(Tender('ted:'+no,'ted',co,first(x.get('notice-title')) or no,first(x.get('buyer-name')),deadline=ddl,url=url,description=first(x.get('description-proc')),procurement_id=no))
 return out
