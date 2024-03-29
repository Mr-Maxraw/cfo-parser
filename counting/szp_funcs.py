import pandas as pd
import numpy as np
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows as df_to_row
from fuzzywuzzy import process, fuzz

path_to_docs = 'C:/Users/posochovais/Desktop/Python/справочники/'
path_to_data = 'C:/Users/posochovais/Desktop/Python/отработанные выгрузки 2022/'
gku = ["ГБУ МГДУ","ГАОУ ДПО ЦПМ","ГАОУ ДПО МЦКО","ГКУ ЦФО ДОНМ","ГБУ ГППЦ ДОНМ","ГКУ СФК ДОНМ","ГКУ Дирекция ДОНМ","ГБОУ ДПО МЦПС","ГБОУ ГМЦ ДОНМ","ГКУ Дирекция по строительству и реконструкции ДОНМ","ГАОУ ДПО ""Корпоративный университет""","ГАУ ""Центр цифровизации образования""","ГАУ Медиацентр","ГАОУ ДПО МЦРПО"]
gku_inn = [7702061938, 7725618950, 7725539709, 9718071371, 7726317748, 7704191153, 9705101759, 7719210793, 7705399348, 7705020295, 7714239823, 7727190237, 7718924940, 7707329480, 	7725663400]
vosp = ['Старший воспитатель', 'Воспитатель']
day_types = ['Основное место работы', 'Внутреннее совместительство', 'Внешнее совместительство']
months_year = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
months_year_rus = ['янв', 'фев', 'мар', 'апр', 'май', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек']
bad_satus = [np.nan, 'Увольнение', 'Отпуск по уходу за ребенком', 'Отпуск по беременности и родам']

def matcher(row, look_up, name):
    if pd.isna(row[name]):
        return np.nan
    ans = process.extractOne(row[name], look_up, scorer=fuzz.WRatio, score_cutoff=60)
    if ans:
        return ans[0]
    return ans

def get_nouvp_grps(file = 'input'):
    big = pd.read_excel(path_to_docs + file + '.xlsx', sheet_name='isp')
    oo = big['oo'].to_list()
    udo = big['udo'].to_list()
    spo = big['spo'].to_list()
    vpo = big['vpo'].to_list()
    return {'ОО': oo, 'ДОУ': oo, 'ЦГУ': udo, 'УДО': udo, 'СПО': spo, 'ВУЗ': vpo}

def get_otv():
    otv = pd.read_excel(path_to_docs + 'Ответственные.xlsx').rename(columns={'инн орг': 'inn', 'округ': 'okr', 'Зарпл. Обслуживание': 'otv', 'Наименование': 'sch_name'})
    otv = otv[['inn', 'okr', 'otv', 'sch_name', 'ekis']]
    return otv

def get_fio():
    fio = pd.read_excel(path_to_docs + 'ФИО+СНИЛС.xlsx').rename(columns={'СНИЛС': 'snils', 'ФИО': 'fio'})
    return fio

def to_double(row, f_name):
    if type(row[f_name]) is float:
        return row[f_name] 
    t = str(row[f_name]).split(',')
    if t[0] == 'nan':
        return 0.0
    if len(t) == 1:
        return float(t[0])
    return float(t[0]+'.'+t[1])

def re_szp(row, months):
    active_months = 0
    fot = 0
    for month in months:
        if row['day_' + month] == 1 and row['stv_' + month] >= 1 and row['status_' + month] == row['status_pref_' + month] and row['status_' + month] == 'Работа':
            fot += row['sum_' + month]
            active_months += 1
    if active_months == 0:
        return np.nan
    return fot / active_months

def re_szp_job(row, months, jobs):
    active_months = 0
    fot = 0
    for month in months:
        if row['job_' + month] in jobs and row['day_' + month] == 1 and row['stv_' + month] >= 1 and row['status_' + month] == row['status_pref_' + month] and row['status_' + month] == 'Работа':
            fot += row['sum_' + month]
            active_months += 1
    if active_months == 0:
        return np.nan
    return fot / active_months

def re_fot(row, months):
    fot = 0
    for month in months:
        if pd.isna(row['sum_all_' + month]) == False:
            fot += row['sum_all_' + month]
    if fot == 0:
        return np.nan
    return fot

def re_fot_job(row, months, jobs):
    fot = 0
    for month in months:
        if row['job_' + month] in jobs and pd.isna(row['sum_all_' + month]) == False:
            fot += row['sum_all_' + month]
    if fot == 0:
        return np.nan
    return fot

def accum_fot_job(row, months, jobs):
    fot = 0
    for month in months:
        if row['job'] in jobs and pd.isna(row['sum_all_' + month]) == False:
            fot += row['sum_all_' + month]
    if fot == 0:
        return np.nan
    return fot

def accum_fot_nouvp(row, months, grouped_jobs):
    fot = 0
    if pd.isna(row['sch_type']):
        return np.nan
    if row['sch_type'] not in grouped_jobs:
        return np.nan
    jobs = grouped_jobs[row['sch_type']]
    for month in months:
        if row['job'] in jobs and pd.isna(row['sum_all_' + month]) == False:
            fot += row['sum_all_' + month]
    if fot == 0:
        return np.nan
    return fot

def load_month(file, path_to_data = path_to_data):
    df = pd.read_excel(path_to_data + file + '.xlsx')
    df['stv'] = df.apply(lambda row: to_double(row, 'stv'), axis=1)
    df = df[df.type.isin(day_types[:2])]
    sums = df[['inn', 'snils', 'sum', 'sum_all']].groupby(['inn', 'snils']).sum()
    sums = pd.merge(sums.reset_index(), df[(df.status != 'Увольнение')], how='left', on=['inn', 'snils']).drop(columns=['sum_y', 'sum_all_y']).rename(columns={'sum_x': 'sum', 'sum_all_x': 'sum_all'})
    sums = sums[sums.type == day_types[0]]
    sums.columns = ['inn', 'snils'] + [i + '_' + file for i in sums.columns][2:]
    return sums

def load_month_all(file, path_to_data = path_to_data):
    df = pd.read_excel(path_to_data + file + '.xlsx')
    df['stv'] = df.apply(lambda row: to_double(row, 'stv'), axis=1)
    df = df[df.type.isin(day_types)]
    sums = df[['inn', 'snils', 'sum', 'sum_all']].groupby(['inn', 'snils']).sum()
    sums = pd.merge(sums.reset_index(), df, how='left', on=['inn', 'snils']).drop(columns=['sum_y', 'sum_all_y']).rename(columns={'sum_x': 'sum', 'sum_all_x': 'sum_all'})
    sums = sums[(sums.type == day_types[0]) | (sums.type == day_types[2])]
    sums.columns = ['inn', 'snils'] + [i + '_' + file for i in sums.columns][2:]
    return sums

def load_month_sum_by_job(file, path_to_data= path_to_data):
    df = pd.read_excel(path_to_data + file + '.xlsx')
    df['stv'] = df.apply(lambda row: to_double(row, 'stv'), axis=1)
    df.rename(columns={'sum': 'sum_' + file, 'sum_all': 'sum_all_' + file}, inplace=True)
    df = df[['inn', 'snils', 'type', 'job', 'sum_all_' + file]].groupby(['inn', 'snils', 'type', 'job']).sum().reset_index()
    return df

def load_month_by_type(file, type, path_to_data = path_to_data):
    df = pd.read_excel(path_to_data + file + '.xlsx')
    df['stv'] = df.apply(lambda row: to_double(row, 'stv'), axis=1)
    df = df[df.type == day_types[type]]
    sums = df[['inn', 'snils', 'sum', 'sum_all']].groupby(['inn', 'snils']).sum()
    sums = pd.merge(sums.reset_index(), df[(df.status != 'Увольнение')], how='left', on=['inn', 'snils']).drop(columns='sum_y').rename(columns={'sum_x': 'sum'})
    sums = sums[sums.type == day_types[type]]
    sums.columns = ['inn', 'snils'] + [i + '_' + file for i in sums.columns][2:]
    return sums

def custom_create_res(months, func, type = -1, data = path_to_data, on=['inn', 'snils']):
    if type == -1:
        res = 0
        for i in range(len(months)):
            if i == 0:
                res = func(months[i], path_to_data = data)
            else:
                res = pd.merge(res, func(months[i], path_to_data = data), how='outer', on=on)
        return res
    res = 0
    for i in range(len(months)):
        if i == 0:
            res = func(months[i], type, path_to_data = data)
        else:
            res = pd.merge(res, func(months[i], type, path_to_data = data), how='outer', on=on)
    return res

def load_data(file):
    df = pd.read_excel(path_to_data + file + '.xlsx')
    df.stv = df.apply(lambda row: to_double(row, 'stv'), axis=1)
    sample = df[(df.type == 'Основное место работы') | (df.type == 'Внутреннее совместительство')]
    sums = sample.iloc[:, [0,1,2,3]].groupby(['inn', 'snils']).sum().reset_index().groupby('snils').max().reset_index()
    sums = pd.merge(sums, sample[sample.type == 'Основное место работы'], how='left', on=['inn', 'snils'])
    sums = sums[(sums.stv >= 1.0) & (sums.status == 'Работа') & (sums.day == 1) & (sums.status_pref == 'Работа')]
    sums = sums[['inn', 'snils', 'sum_x', 'stv', 'job']].drop_duplicates(['inn', 'snils', 'sum_x'])
    sums = sums.rename(columns = {'inn_y': 'inn', 'sum_x': 'sum_' + file, 'job':'job_' + file, 'stv': 'stv_' + file})
    return sums

def create_res(months):
    res = 0
    for i in range(len(months)):
        if i == 0:
            res = load_data(months[i])
        else:
            res = pd.merge(res, load_data(months[i]), how='outer', on=['inn', 'snils'])
    return res

def load_data_all(file):
    df = pd.read_excel(path_to_data + file + '.xlsx')
    df.stv = df.apply(lambda row: to_double(row, 'stv'), axis=1)
    sample = df[~(df.type == 'Внешнее совместительство')]
    sums = sample.iloc[:, [0,1,2,3]].groupby(['inn', 'snils']).sum().reset_index().groupby('snils').max().reset_index()
    sums = pd.merge(sums, sample[sample.type == 'Основное место работы'], how='left', on=['inn', 'snils'])
    sums = sums[['inn', 'snils', 'sum_x', 'stv', 'job', 'status']].drop_duplicates(['inn', 'snils', 'sum_x'])
    sums = sums.rename(columns = {'inn': 'inn', 'sum_x': 'sum_' + file, 'job':'job_' + file, 'stv': 'stv_' + file, 'status': 'status_' + file})
    return sums


def create_full_res(months):
    res = 0
    for i in range(len(months)):
        if i == 0:
            res = load_data_all(months[i])
        else:
            res = pd.merge(res, load_data_all(months[i]), how='outer', on=['inn', 'snils'])
    return res


def print_df(df, name):
    wb = Workbook()
    ws = wb.active
    for  i in df_to_row(df, header=True, index=False):
        ws.append(i)
    wb.save(name + '.xlsx')

def szp(row, months):
    # if pd.isna(row['job_' + months[-1]]):
    #     return np.nan
    cnt = 0
    sum_szp = 0
    for month in months:
        if pd.isna(row['sum_' + month]):
            continue
        cnt += 1
        sum_szp += row['sum_' + month]
    # if row['inn'] == 9715217689 and row['snils'] == '173-260-871 66':
    #     print(cnt, sum_szp)
    if cnt == 0:
        return np.nan
    return sum_szp / cnt

def szp_ped(row, months):
    sum_szp = 0
    cnt = 0
    for month in months:
        if row['job_' + month] in ped:
            cnt += 1
            sum_szp += row['sum_' + month]
    if cnt == 0 or pd.isna(row['job_' + months[-1]]):
        return np.nan
    return sum_szp / cnt


def szp_teach(row, months):
    sum_szp = 0
    cnt = 0
    for month in months:
        if row['job_' + month] in ['Учитель']:
            cnt += 1
            sum_szp += row['sum_' + month]
    if cnt == 0 or row['job_' + months[-1]] != 'Учитель':
        return np.nan
    return sum_szp / cnt

def szp_vosp(row, months):
    sum_szp = 0
    cnt = 0
    for month in months:
        if row['job_' + month] in vosp:
            cnt += 1
            sum_szp += row['sum_' + month]
    if cnt == 0 or row['job_' + months[-1]] not in vosp:
        return np.nan
    return sum_szp / cnt

def sum_fot(row, months):
    sum = 0
    for month in months:
        if pd.isna(row['sum_' + month]) == False:
            sum += row['sum_' + month]
    return sum

def sum_fot_jobs(row, months, jobs):
    sum = 0
    for month in months:
        if pd.isna(row['sum_' + month]) == False and pd.isna(row['job_' + month]) == False and row['job_' + month] in jobs:
            sum += row['sum_' + month]
    return sum

def load_groups(file = 'input'):
    df = pd.read_excel(path_to_docs + file + '.xlsx', sheet_name='УГД')
    ped = df[df['Педагогический'] == 1]['Должность'].tolist()
    isp = df[df['Работники непосредственно осуществляющие и обеспечивающие основной учебно-вспомогательный процесс во взаимодействии с детьми'] == 1]['Должность'].tolist()
    aup = df[df['УГД'] == 'Административно-управленческий персонал']['Должность'].to_list()
    return ped, isp, aup

def load_pay_types(file = 'pay_type'):
    return pd.read_excel(path_to_docs + file + '.xlsx', sheet_name='Все').rename(columns={'Вид ': 'type', 'Наименование ': 'name'})[['type', 'name']]

def load_jobs(file = 'input'):
    jobs = pd.read_excel(path_to_docs + file + '.xlsx', sheet_name='должности')
    jobs.columns = ['pre_job', 'job_106']
    return jobs

def load_sch_types(file = 'school_types'):
    return pd.read_excel(path_to_docs + file + '.xlsx')