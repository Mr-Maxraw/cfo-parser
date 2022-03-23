import duckdb
from numpy import delete

# con = duckdb.connect(database='test.duckdb')

# con.execute('delete from job where cnt=1')

#con.execute('insert into job values (?, ?, ?, ?, ?, ?)', [1, '123123', 'job', '1999-01-01', 123, 213123])
s = '123,23'
s1 = '123'

tmp = s.split(',')
print(tmp)
tmp = s1.split(',')
print(tmp)