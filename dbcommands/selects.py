def monthly_report(con, month, year):
    return con.execute('''select s.inn, s."type", s.name, p.snils, p.fio, j.sum, j.part, j.type, j.status, j.title, j.day from Job as j
    join Person as p on p.snils = j.person_snils
    join School as s on s.inn = j.school_inn
    where month(j.date) = ? and year(j.date) = ?
    ''', [month, year]).fetchdf()