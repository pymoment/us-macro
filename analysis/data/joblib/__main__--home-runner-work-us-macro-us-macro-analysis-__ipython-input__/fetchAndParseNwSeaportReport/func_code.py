# first line: 1
@memory.cache
def fetchAndParseNwSeaportReport(url):
    try:
        tmp = read_pdf(url, pages='all')[0]

        #print(tmp.iloc[:, 0].map(lambda v: re.sub("[\d,]", "", str(v)).strip()).values)
        if tmp.iloc[0, 1] == "Int'l Import full TEUs":
            #print('one')
            tmp.columns = ['Key'] + tmp.iloc[0, 1:].apply(lambda v: str(v).replace("\r", " ").strip()).to_list()

            tmp = tmp.iloc[1:].set_index("Key").T
        
        elif "Break Bulk" in tmp.iloc[:, 0].map(lambda v: re.sub("[\d,]", "", str(v)).strip()).values:

            if pd.isnull(tmp.iloc[0, 0]) and pd.isnull(tmp.iloc[0, 1]):
                #print('two')
                tmp = tmp.iloc[1:, :]
                
                tmp.columns = ['Key'] + tmp.iloc[0, 1:].apply(lambda v: str(v).strip()).to_list()

                tmp = tmp.set_index("Key").iloc[1:].T
                
            elif pd.isnull(tmp.iloc[0, 0]) and not pd.isnull(tmp.iloc[0, 1]):
                #print('twotwo')
                tmp.columns = ['Key'] + tmp.iloc[0, 1:].apply(lambda v: str(v).strip()).to_list()

                tmp = tmp.set_index("Key").iloc[1:].T
            
            else:
                #print('three')
                tmp.columns = ['Key'] + tmp.iloc[0, 1:].apply(lambda v: str(v).strip()).to_list()

                tmp = tmp.set_index("Key").iloc[1:].T
            
        else:
            #print('four')
            tmp.columns = ['Key'] + tmp.iloc[1, 1:].apply(lambda v: str(v).strip()).to_list()

            tmp = tmp.set_index("Key").iloc[2:, 1:].T
        
        tmp.columns = tmp.columns.map(lambda v: re.sub("[\d,]", "", str(v)).strip())
        
        tmp = tmp.rename({ "Break Bulk": "Breakbulk" }, axis=1)
        
        if 'Grain' not in tmp.columns:
            tmp['Grain'] = [''] * tmp.shape[0]
            
        if 'Gypsum' not in tmp.columns:
            tmp['Gypsum'] = [''] * tmp.shape[0]
            
        if 'Vessel Calls' not in tmp.columns:
            tmp['Vessel Calls'] = [''] * tmp.shape[0]
            
        tmp['src'] = [url] * tmp.shape[0]
        return tmp
    except HTTPError:
        print("Failed: " + url)
        return None
