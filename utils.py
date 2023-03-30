import openpyxl


def wright_name(src):
    n = 1
    a = openpyxl.load_workbook('schedule.xlsx')
    ws = a.active
    while ws[f'A{n}'].value is not None:
        n += 1
    ws[f'A{n}'] = src
    print(ws[f'A{n}'].value)
    a.save('schedule.xlsx')
    return n


def wright_time(src, n):
    a = openpyxl.load_workbook('schedule.xlsx')
    ws = a.active
    ws[f'B{n}'] = src
    print(ws[f'B{n}'].value)
    a.save('schedule.xlsx')
    return n


def wright_date(src, n):
    a = openpyxl.load_workbook('schedule.xlsx')
    ws = a.active
    ws[f'C{n}'] = src
    print(ws[f'C{n}'].value)
    a.save('schedule.xlsx')
    return n