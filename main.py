import sqlite3
import pandas as pd
from UliPlot.XLSX import auto_adjust_xlsx_column_width
import functools
import sys

# Перенаправление всех print-ов в файл, для чтения в консоли - закомментировать
sys.stdout = open('output.txt', 'wt', encoding='utf-8')

conn = sqlite3.connect('gpb.sqlite')
conn.executescript(open('create_db.sql', encoding='utf-8').read())


# Декоратор исключительно для красоты вывода
def decorator(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        print(function.__doc__)
        print('-' * 50)
        res = function(*args, **kwargs)
        print('-' * 50 + '\n')
        return res

    return wrapper


# Распечатка результата и дублирование в excel-файлики
def result_output(result, file_name, table_name):
    print(f'RESULT: {table_name}\n', result)
    with pd.ExcelWriter(file_name) as writer:
        result.to_excel(writer, index=False, sheet_name=table_name)
        auto_adjust_xlsx_column_width(result, writer, sheet_name=table_name, index=False, margin=1)


@decorator
def task_1():
    """Задание 1"""
    active_clients = pd.read_sql('''
    select * from ACTIVE_CLIENTS
    ''', conn)
    print('ACTIVE_CLIENTS\n', active_clients, '\n')

    result = pd.read_sql('''
    select t.report_month, count(t.client_id) as active_clients,
    coalesce(tt.outflow, 0)/cast(count(t.client_id) as REAL) as expired_part
    from ACTIVE_CLIENTS t left join
    
    (select report_month, count(client_id) as outflow
    from (select *, lead(report_month, 1, (select DATE(max(report_month), '+1 month') from ACTIVE_CLIENTS)) 
    over (partition by client_id) next_month
    from ACTIVE_CLIENTS
    order by report_month) as ttt
    where ttt.next_month > DATE(ttt.report_month, '+3 month')
    or ttt.next_month is null 
    group by report_month) as tt
    
    on t.report_month = tt.report_month
    group by t.report_month;
    ''', conn)
    result_output(result, 'task_1.xlsx', 'ACTIVE_AND_EXPIRED_CLIENTS')


@decorator
def task_2():
    """Задание 2"""
    offers = pd.read_sql('''
        select * from OFFERS
        ''', conn)
    print('OFFERS\n', offers, '\n')

    calendar_2018 = pd.date_range(start='2018-01-01', end='2018-12-31'). \
        strftime('%Y-%m-%d').to_frame(index=False, name='date_2018')
    conn.execute('drop table if exists CALENDAR_2018')
    calendar_2018.to_sql('CALENDAR_2018', conn, index=False)

    result = pd.read_sql('''
    select date_2018, count(offer_id) as offers_amount from CALENDAR_2018
    left join OFFERS
    on date_2018 between offer_start_date and offer_expiration_date
    or date_2018>=offer_start_date and offer_expiration_date is null 
    or offer_start_date is null and date_2018<=offer_expiration_date
    group by date_2018
    ''', conn)
    result_output(result, 'task_2.xlsx', 'OFFERS_EVERY_DAY_2018')


@decorator
def task_3():
    """Задание 3"""
    cards = pd.read_sql('''
    select * from CARDS order by open_date, close_date
    ''', conn)
    print('CARDS\n', cards, '\n')

    our_date = "'2018-09-01'"
    result = pd.read_sql(f'''
    select client_id, card_id from CARDS
    where ({our_date} between open_date and close_date
    or {our_date}>=open_date and close_date is null 
    or open_date is null and {our_date}<=close_date)
    and card_type='DC'
    order by open_date desc 
    limit 1
    ''', conn)
    result_output(result, 'task_3.xlsx', f'LAST_DC_OPENED_BY_{our_date[1:-1]}')


@decorator
def task_4():
    """Задание 4"""
    bonus = pd.read_sql('''
    select * from BONUS
    ''', conn)
    print('BONUS\n', bonus, '\n')
    mcc_categories = pd.read_sql('''
        select * from MCC_CATEGORIES
        ''', conn)
    print('MCC_CATEGORIES\n', mcc_categories, '\n')

    result = pd.read_sql(f'''
    with t as (select client_id, bonus_date, 
    sum(bonus_cnt) over (partition by client_id order by bonus_date) as current_sum 
    from BONUS
    natural join MCC_CATEGORIES
    where mcc_category in ('Авиабилеты', 'Отели')),
    
    ranked_data as (select *, 
    row_number() over (partition by client_id order by bonus_date) as row_num
    from t 
    where current_sum>=1000)
    
    select client_id, bonus_date, current_sum from ranked_data
    where row_num=1
    order by bonus_date
    limit 1000
    ''', conn)
    result_output(result, 'task_4.xlsx', f'FIRST_1000_AVIA_AND_HOTELS')


@decorator
def task_5(input_date):
    """Задание 5"""
    exchange_rates = pd.read_sql('''
    select * from EXCHANGE_RATES
    ''', conn)
    print('EXCHANGE_RATES\n', exchange_rates, '\n')

    result = pd.read_sql(f'''
    select * from EXCHANGE_RATES
    where value_day <= '{input_date}'
    and code = 'USD'
    order by value_day desc 
    limit 1
    ''', conn)
    result_output(result, 'task_5.xlsx', f'EXCHANGE_RATE_BY_{input_date}')


task_1()
task_2()
task_3()
task_4()
task_5('2021-06-01')
