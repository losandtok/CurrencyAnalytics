




def translate_date(start_day, start_month, start_year, end_day, end_month, end_year):
    if int(start_month) == 2:
        if int(start_year) % 4 == 0:
            if int(start_day) > 29:
                start_day = '29'
        else:
            if int(start_day) > 28:
                start_day = '28'
    elif (int(start_month) < 8 and int(start_month) % 2 == 0) or (int(start_month) > 7 and int(start_month) % 2 == 1):
        if int(start_day) > 30:
            start_day = '30'

    if int(end_month) == 2:
        if int(end_year) % 4 == 0:
            if int(end_day) > 29:
                end_day = '29'
        else:
            if int(end_day) > 28:
                end_day = '28'
    elif (int(end_month) < 8 and int(end_month) % 2 == 0) or (int(end_month) > 7 and int(end_month) % 2 == 1):
        if int(end_day) > 30:
            end_day = '30'
    return start_year + '-' + start_month + '-' + start_day, end_year + '-' + end_month + '-' + end_day
