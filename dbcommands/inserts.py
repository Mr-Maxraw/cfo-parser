def to_job(con, data):
    con.execute('insert into Job values (?, ?, ?, ?, ?, ?, ?, ?, ?)', data)

def to_person(con, data):
    con.execute('insert into Person values (?, ?)', data)

def to_school(con, data):
    con.execute('insert into School values (?, ?, ?)', data)

def to_rating(con, data):
    con.execute('insert into Rating values (?, ?, ?)', data)

def to_pers_data(con, data):
    con.execute('insert into Pers_data values (?, ?, ?)', data)

def to_pay(con, data):
    con.execute('insert into Pay values (?, ?, ?)', data)

def to_load(con, data):
    con.execute('insert into Load values (?, ?, ?, ?)', data)

def to_job_title_desc(con, data):
    con.execute('insert into job_title_desc values (?, ?, ?, ?)', data)