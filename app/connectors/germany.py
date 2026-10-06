import io,json,zipfile,httpx
from datetime import date,datetime,timedelta
from app.core import Tender
def dt(v):
 try:return datetime.fromisoformat(str(v).replace('Z','+00:00')).replace(tzinfo=None)
 except:return None
async def fetch(countries=None,days=3):
 out=[]
 async with httpx.AsyncClient(timeout=60) as c:
  for i in range(1,days+1):
   r=await c.get('https://oeffentlichevergabe.de/api/notice-exports',params={'pubDay':(date.today()-timedelta(days=i)).isoformat(),'format':'ocds.zip'})
   if r.status_code in (400,404):continue
   r.raise_for_status()
   with zipfile.ZipFile(io.BytesIO(r.content)) as z:
    for f in z.namelist():
     rel=(json.loads(z.read(f)).get('releases') or [{}])[0];t=rel.get('tender') or {};ps=rel.get('parties') or [];b=next((p.get('name','') for p in ps if 'buyer' in p.get('roles',[])),'');oc=rel.get('ocid') or rel.get('id') or f;url=f'https://oeffentlichevergabe.de/ui/de/notices/{oc}';out.append(Tender('de:'+oc,'germany','DEU',t.get('title') or oc,b,deadline=dt((t.get('tenderPeriod') or {}).get('endDate')),status=t.get('status','active'),url=url,description=t.get('description',''),procurement_id=oc))
 return out
