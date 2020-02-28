# first line: 1
@memory.cache
def doGaFetch(url, retries=5):
    if retries < 0:
        return None
    try:
        req = Request(url, data=None, headers={ 'User-Agent': uaString })

        data = urlopen(req)

        tabs = read_pdf(BytesIO(data.read()), pages='all', pandas_options={ 'names': cols })

        # noop to test for the table
        tabs[0]
        
        return tabs
    except KeyError:
        sleep(1)
        return doGaFetch(url, retries-1)
