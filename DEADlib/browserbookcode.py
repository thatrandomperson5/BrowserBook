import requests
from DEADlib.tools.canOpener import Open
from DEADlib.tools.URIreader import read
from bs4 import BeautifulSoup
import shutil
from uuid import uuid4
import os
import json
import warnings
def jsonParama(chunk):
  chunk = chunk.replace('?','')
  BP = chunk.split('&')
  BPO = {}
  for b in BP:
    b = b.split('=')
    b.append('')
    BPO[b[0]] = b[1]
  return BPO
  
class SessionObject:
  def __init__(self, name, id):
    self.id = id
    self.name = name
    self.location = f'{os.getcwd()}/{self.name}/sessions/{id}'
    self.baseParams = {}
    self.url = ''
    self.localize = False
    self.log = True
    self.URI = False
  def get(self, url):
    self.url = url[:url.rfind('?')]
    if not 'www.' in self.url:
      warnings.warn('"www" is recommend and the lack of it may cause issues.', SyntaxWarning)
    if not self.url.endswith('/'):
      if not '?' in self.url:
        d = "'"
        error = f'"{self.url}" is not considered a valid url because there is no trailing //, adding both won{d}t produce a different outcome and will only help prevent errors.'
        raise SyntaxError(error)
    
    if url.rfind('?')> 0:
        BP = url[url.rfind('?'):]
        json = jsonParama(BP)
        self.baseParams = json
    
    headers = {'Accept-Encoding': 'identity', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    
    
    req = requests.get(url, headers=headers, params=self.baseParams)
    return {'stat':req.status_code, 'html':req.content, 'headers':req.headers, 'json':req.json}
  def parseSRC(self, html):
    soup = BeautifulSoup(html, 'html.parser')
    output = {'src':[],'href':[]}
    for href in soup.find_all(attrs={'href':True}):
       output['href'].append(href.get('href'))
    for src in soup.find_all(attrs={'src':True}):
       output['src'].append(src.get('src'))
    
    return output
      
  def getAllSaveAll(self, reqlist):
    core = self.url[0:len(self.url)-1]
    host = self.url[0:len(self.url)-1]
    host = host.split('/')
    
    host = '/'.join(host[0:3])+'/'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36', 'Referer':host}
    reqlist.insert(0, '/index.html')
    
    
    print(f'From {core} getting data.')
    for req in reqlist:
      if not req.startswith(host) and not req.startswith('/'):
        if self.localize == True:
          if self.log:
            print(f'[GET]: {req}')
          if req.startswith('data:image'):
            if not self.URI:
              warnings.warn(f'Encounterd a Data url source.', SyntaxWarning)
            else:
              red = read(req)
              f = Open(f'{os.getcwd()}/{self.name}/sessions/{self.id}/externalSRC/URI/{str(uuid4())[:8]}.{red["filetype"]}') 
              
              f.write(red['bytes'])
            
          else:
            r = requests.get(req, headers=headers)
            c = r.content
            if req.rfind('?') > 0:
              req=req[:req.rfind('?')]
            else:
            
              req = req
          
            path = req
            path = path.replace('https://','')
          
            path = path.replace('http://','')
            path = path.split('/')[1:]
            path = '/'.join(path)
            file =Open(f'{os.getcwd()}/{self.name}/sessions/{self.id}/externalSRC/{path}')
            file.write(c)
            file.close
      else:
        if req.startswith('data:'):
            warnings.warn(f'Unable to read source url: {req}', SyntaxWarning)
        req = req.replace(host, '')
        if req.rfind('?') > 0:
          params = req[req.rfind('?'):]
          params = jsonParama(params)
          req=req[:req.rfind('?')]
        else:
          params = {}
          req = req
          if self.log:
            print(f'[GET]: {host+req}')
        
      
        req = req.replace('https://','')
        req = req.replace('http://','')
        
      
        if req == '/index.html':
          r = requests.get(core+'/', headers=headers, params=params)
        else:
          r = requests.get(host+req, headers=headers, params=params)
        c = r.content
        type = r.encoding
        reqpath = req
#        Old code
#        if req.startswith('/'):
#          
#          reqpath = req
#        
#        else:
#          reqpath = req
#          
#        
#          reqpath = reqpath.replace('https://','')
#          reqpath = reqpath.replace('http://','')
#        
#          reqpath = req.split('/')[3:len(req)-1]
#        
#          reqpath = '/'.join(reqpath)
#          reqpath = reqpath

        file = Open(f'{os.getcwd()}/{self.name}/sessions/{self.id}/source/{reqpath}')
        file.write(c)
        file.close
  def Get(self, url):
    if '?' in url:
      urla=url[url.rfind('?'):]
      url=url[:url.rfind('?')]
      url = f'{url}/'
      url = url+urla
    else:
      url = url+'/'
    
    phase1 = self.get(url)['html']
    parsed = self.parseSRC(phase1)
    self.getAllSaveAll(parsed['src'])
    #remember all urls end with an extra /
  def dump(self):
    with open(self.location+'/nav.json', 'r+') as nav:
      
      navjs = json.load(nav)
      
      navjsp = navjs['page']
      navjsp['Status'] = 'Dumping'
      navjs['page'] = navjsp
      nav.seek(0)
      json.dump(navjs, nav, indent=4)
      nav.truncate()
      path = self.location
      shutil.rmtree(f'{path}/source')
      shutil.rmtree(f'{path}/externalSRC')
      os.mkdir(f'{path}/source')
      os.mkdir(f'{path}/externalSRC')
      navjsp['Status'] = None
      navjsp['from'] = None
      navjsp['loaded'] = None
      navjsp['requests'] = None
      navjs['page'] = navjsp
      
      nav.seek(0)
      json.dump(navjs, nav, indent=4)
      nav.truncate()
class brbook():
  def __init__(self, name):
    self.name = name
    
    if not os.path.isdir(f'{os.getcwd()}/{name}'):
      
      os.mkdir(name)
      os.mkdir(f'{name}/sessions')
    else:
      shutil.rmtree(f'{os.getcwd()}/{self.name}/sessions')
      os.mkdir(f'{name}/sessions')
  def sessionStart(self):
    session = uuid4()
    
    if os.path.isdir(f'{os.getcwd()}/{self.name}/sessions/{session}'):
      raise OSError('Duplicate session, try again')
    os.mkdir(f'{self.name}/sessions/{session}')
    os.mkdir(f'{self.name}/sessions/{session}/source')
    os.mkdir(f'{self.name}/sessions/{session}/externalSRC')
    with open(f'{self.name}/sessions/{session}/nav.json', 'w') as nav:
      jnav = {'RouteDir':f'{self.name}/sessions/{session}/source', 
              'Dir':f'{self.name}/sessions/{session}/source', 
              'SourcePath':f'{os.getcwd()}/{self.name}/sessions/{session}',
              'PATH':f'{self.name}/sessions/{session}/source/index.html',
              'page':{'from':None, 'loaded':None, 'Status':None, 'requests':None}}
      nav.write(json.dumps(jnav, sort_keys=True, indent=4))
    return session
  def EndSession(self, session):
    dir_path = f'{os.getcwd()}/{self.name}/sessions/{session}'
    shutil.rmtree(dir_path)
  def getSessionObject(self, name, id):
    sessionObject = SessionObject(name, id)
    return sessionObject
  