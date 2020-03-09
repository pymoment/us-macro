# first line: 1
@memory.cache
def parseCsxReport(urlAndWeek):
    try:
        url, weekAndYear = urlAndWeek
    
        # '2013 Week 29'
        year, week = weekAndYear.split(' Week ')
        
    except ValueError:
        try:
            url, weekAndYear = urlAndWeek
    
            # '2013 Week 29'
            year, week = weekAndYear.split('-WK')
        except ValueError:
            print(urlAndWeek)
            return None
    
    #            WEEK   28                QUARTER TO DATE           YEAR TO DATE
    baseCols = ['Cargo', 'Week {0} {1}', 'Week {0} {2}', 'Week {0} pct-change',
                'Week {0} {1} QTD', 'Week {0} {2} QTD', 'Week {0} QTD pct-change',
                'Week {0} {1} YTD', 'Week {0} {2} YTD', 'Week {0} YTD pct-change']

    try:
        cols = [c.format(week.split(' ')[0], int(year), int(year)-1) for c in baseCols]
    except ValueError:
        print(urlAndWeek)
        return None
    
    try:
        tmp = read_pdf(url, pages='all', pandas_options={ 'names': cols })
        df = pd.concat(tmp) if isinstance(tmp, list) else tmp
        return df.iloc[1:, :].set_index('Cargo').applymap(lambda v: float(re.sub('[^0-9.]', '', v)))
    except AttributeError:
        print(urlAndWeek)
        return None
    except ValueError:
        print(urlAndWeek)
        return None
