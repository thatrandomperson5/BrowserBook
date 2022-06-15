import os
def Open(path):
  path = path.split('/')
  index = 0
  for val in path:
    index += 1
    if index == len(path)-1:
      
      if path[index].endswith('.pn'):
        path[index] = path[index].replace('.pn','.png')
      if path[index].endswith('.j'):
        path[index] = path[index].replace('.j','.jhtml')
        
      
      retur = open('/'.join(path[0:index+1]),'wb')
      return retur
    else:
    
      if not os.path.isdir('/'.join(path[0:index+1])):
        os.mkdir('/'.join(path[0:index+1]))
  