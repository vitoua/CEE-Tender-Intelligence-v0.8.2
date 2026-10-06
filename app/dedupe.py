import re,unicodedata
def n(v):return re.sub(r'[^a-z0-9]+',' ',unicodedata.normalize('NFKD',str(v or '')).encode('ascii','ignore').decode().lower()).strip()
def duplicate(a,b):
 if a.country!=b.country:return False
 ids=lambda x:set(re.findall(r'(?:\d{6}-\d{4}|ocds-[a-z0-9-]+|ua-\d{4}-\d{2}-\d{2}-[a-z0-9-]+)',' '.join([x.id,x.procurement_id,x.url]).lower()))
 if ids(a)&ids(b):return True
 A=set(n(a.title).split());B=set(n(b.title).split());sim=len(A&B)/max(1,len(A|B));return sim>=.86 and n(a.buyer)==n(b.buyer) and (not a.deadline or not b.deadline or abs((a.deadline-b.deadline).days)<=2)
def merge(a,b):
 p=b if b.source!='ted' and a.source=='ted' else a;p.source_links={**a.source_links,**b.source_links};return p
