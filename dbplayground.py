import duckdb
from numpy import delete
from dbcommands.selects import monthly_report

con = duckdb.connect(database='test.duckdb')

#con.execute('delete from job where true')
print(monthly_report(con, 1, 1999))
# con.execute('insert into Job values ( ?, ?, ?, ?, ?)', ['123123', 'job', '1999-01-01', 123, 213123])
# con.execute('insert into Person values (?, ?)', ['123123', 'Sampe Samplovich'])
# con.execute('insert into School values (?, ?, ?)', ['School #1', 'normal school', 213123])
# s = '123,23'
# s1 = '123'

# tmp = s.split(',')
# print(tmp)
# tmp = s1.split(',')
# print(tmp)