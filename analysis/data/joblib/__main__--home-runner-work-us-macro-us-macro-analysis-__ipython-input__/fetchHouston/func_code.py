# first line: 1
@memory.cache
def fetchHouston(url, retries=5):
    if retries < 0:
        return pd.DataFrame()
    try:
        req = Request(url, data=None, headers={ 'User-Agent': uaString })

        data = urlopen(req)

        cols = ["Date", "Loaded Imports", "Loaded Exports", "Loaded Total",
                "Empty Imports", "Empty Exports", "Empty Total", "Loaded and Empty Total"]

        dfs_hs = read_pdf(BytesIO(data.read()), pages='all', pandas_options={ 'names': cols }) #.head(20)

        df_hs = pd.concat([dfs_hs[0].iloc[5:]] + dfs_hs[1:])

        df_hs[df_hs.columns.to_list()[1:]] = df_hs[df_hs.columns.to_list()[1:]]\
                .applymap(lambda v: pd.to_numeric(v.replace(",", "") if isinstance(v, str) else v, errors='coerce'))

        df_hs['dt'] = df_hs['Date'].map(lambda v: pd.to_datetime(str(v), format='%b-%y', errors='coerce'))

        return df_hs
    except KeyError:
        sleep(1)
        return fetchHouston(url, retries-1)
