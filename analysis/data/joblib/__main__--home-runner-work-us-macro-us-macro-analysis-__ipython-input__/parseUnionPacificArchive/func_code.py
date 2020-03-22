# first line: 1
@memory.cache
def parseUnionPacificArchive(u):
    theUrl = "http://up.com" + u

    try:
        week = re.search(".*[0-9]{4}/(\d\d).pdf.*", u).group(1)
    except AttributeError:
        try:
            week = re.search(".*[0-9]{4}/week(\d\d)\_\d\d.pdf.*", u).group(1)
        except AttributeError:
            print("Failed: " + u)
            return None

    #print(week)

    try:
        df_up = read_pdf(theUrl, pages='all', multiple_tables=False)[0]
        originalColumns = df_up.columns.to_list()
        df_up.columns = [str(originalColumns[1]) + '-' + str(week)] + originalColumns[1:]
        
        year = str(df_up.columns[1])
        
        if year[:2] in ['5,', '6,', '7,', '8,']:
            print(f"Invalid year for {u}")
            print(originalColumns)
            return None

        if year == '2009':
            # fetch 2008 data from the 2009 previous year column
            tmp = pd.concat([df_up.set_index(df_up.columns[0])[df_up.columns[1]].rename(year + '-' + str(week)),
                             df_up.set_index(df_up.columns[0])[df_up.columns[2]].rename("2008" + '-' + str(week))], axis=1)
        else:
            tmp = df_up.set_index(df_up.columns[0])[df_up.columns[1]].rename(year + '-' + str(week))

        return tmp
    except IndexError:
        print("Failed: " + u)
        return None
