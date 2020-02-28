# first line: 1
@memory.cache
def fetchLaData(u, year, cols, args = { 'skiprows': 1 }):
 
    req = Request(u, data=None, headers={ 'User-Agent': uaString })

    data = urlopen(req)

    tmp = pd.read_html(BytesIO(data.read()), **args)[0]
    try:
        tmp.columns = ['Month'] + cols
    except ValueError as e:
        #print(tmp.head())
        print(e)
        
    tmp['dt'] = tmp['Month'].apply(lambda v: pd.to_datetime("{}-{}".format(v, year), format="%B-%Y", errors='coerce'))
    
    return tmp
