import codecs
def read(uri):
  data = {}
  data['datatype'] = uri[:uri.find('/')]
  
  data['datatype'] = data['datatype'].split(':')[1]
  data['filetype'] = uri[uri.find('/'):uri.find(';')][1:]
  data['encoding'] = uri[uri.find(';'):uri.find(',')][1:]
  data['raw'] = uri[uri.find(','):][1:]
  print(data['encoding'])
  data['bytes'] = codecs.decode(str.encode(data['raw']), data['encoding'])
  return data