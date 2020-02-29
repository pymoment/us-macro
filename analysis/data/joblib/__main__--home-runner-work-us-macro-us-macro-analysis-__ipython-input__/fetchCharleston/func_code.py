# first line: 1
@memory.cache
def fetchCharleston(url, retries=5):
    if retries < 0:
        return None
    try:
        req = Request(url, data=None, headers={ 'User-Agent': uaString })

        data = urlopen(req, timeout=5)

        dfs_ch = read_pdf(BytesIO(data.read()), pages='all')

        # noop
        dfs_ch[0]
        
        return dfs_ch
    except KeyError:
        print("Response code: {}".format(data.getcode()))
        sleep(1)
        return fetchCharleston(url, retries-1)
    except URLError:
        sleep(1)
        return fetchCharleston(url, retries-1)       
