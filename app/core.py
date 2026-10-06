from dataclasses import dataclass,field
from datetime import datetime
@dataclass
class Tender:
 id:str;source:str;country:str;title:str;buyer:str='';value:float|None=None;currency:str='';deadline:datetime|None=None;status:str='active';url:str='';description:str='';procurement_id:str='';source_links:dict=field(default_factory=dict)
class Store:
 def __init__(self):self.data={};self.runs=[]
 def add(self,src,rows):
  from app.dedupe import duplicate,merge
  a=d=0
  for x in rows:
   x.source_links=x.source_links or ({x.source:x.url} if x.url else {});k=next((k for k,y in self.data.items() if duplicate(x,y)),None)
   if k is None:self.data[x.id]=x;a+=1
   else:self.data[k]=merge(self.data[k],x);d+=1
  self.runs.insert(0,{'source':src,'status':'ok','count':len(rows),'added':a,'duplicates':d,'error':''})
 def error(self,s,e):self.runs.insert(0,{'source':s,'status':'error','count':0,'added':0,'duplicates':0,'error':str(e)})
store=Store()
def active(x):return x.status.lower() not in {'complete','completed','awarded','cancelled','closed'} and (not x.deadline or x.deadline>=datetime.utcnow())
