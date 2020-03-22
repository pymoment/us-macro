# first line: 1
@memory.cache
def parseUnionPacificArchive2(u):
    theUrl = "http://up.com" + u

    try:
        week = re.search(".*_[\d]{4}-(\d\d?).pdf.*", u).group(1)
    except AttributeError:
        try:
            week = re.search(".*week_(\d\d?)\_[\d]{4}[^.]+.pdf.*", u).group(1)
        except AttributeError:
            try:
                week = re.search(".*_[\d]{4}_(\d\d?)[^\.]*.pdf.*", u).group(1)
            except AttributeError:
                print("Failed week: " + u)
                return None

    #print(week)

    try:
        df_up = read_pdf(theUrl, pages='all', multiple_tables=False)[0]
        df_up.columns = [str(df_up.columns[1]) + '-' + str(week)] + df_up.columns.to_list()[1:]

        tmp = df_up.set_index(df_up.columns[0])[df_up.columns[1]].rename(str(df_up.columns[1]) + '-' + str(week))

        return tmp
    except IndexError:
        print("Failed index: " + u)
        return None
