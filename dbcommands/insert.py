def to_job(con, data):
    con.execute('insert into job values (?, ?, ?, ?, ?)', data)

def to_person(con, data):
    con.execute('insert into job values (?, ?)', data)

def to_school(con, data):
    con.execute('insert into job values (?, ?, ?)', data)

def to_rating(con, data):
    con.execute('insert into job values (?, ?, ?)', data)

def to_pers_data(con, data):
    con.execute('insert into job values (?, ?, ?)', data)

def to_pay(con, data):
    con.execute('insert into job values (?, ?, ?)', data)

def to_load(con, data):
    con.execute('insert into job values (?, ?, ?, ?)', data)

def to_job_title_desc(con, data):
    con.execute('insert into job values (?, ?, ?, ?)', data)