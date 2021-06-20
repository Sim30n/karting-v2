import csv
import datetime
from app import db, Race, Driver, Result, Lap

class Result_class:
    def __init__(self, location, driver, race_type, race_date):
        self.location = location
        self.driver = driver
        self.race_type = race_type
        self.race_date = race_date
        self.position = None
        self.lap_times = []


file_name = "imatra_qualifying_lap_times.csv"
results = []

with open(file_name, newline='') as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    list_of_drivers = None
    race_type = ""
    location = ""
    for row in reader:
        if line_count == 0:
            race_type = row[0]
        elif line_count == 1:
            location = row[0]
            race_date = row[1]
        elif line_count == 2:
            list_of_drivers = row
            for i in list_of_drivers:
                new_result = Result_class(location, i, race_type, race_date)
                results.append(new_result)
        elif line_count == 3:
            for i in range(len(row)):
                results[i].position = row[i]
        elif line_count > 3:
            for i in range(len(results)):
                results[i].lap_times.append(row[i])
        line_count += 1

db.create_all()

location = results[0].location
race_date = results[0].race_date.split(".")
race_date = [int(i) for i in race_date]
to_db = []

race = Race(location, datetime.datetime(race_date[2], race_date[1], race_date[0]))
to_db.append(race)
for result in results:
    to_db.append(Driver(result.driver))
db.session.add_all(to_db)
db.session.commit()
to_db.clear()

for r in results:
    driver = Driver.query.filter_by(name=r.driver).all()[0]
    location = Race.query.filter_by(location=r.location).all()[0]
    result = Result(driver.id, location.id, int(r.position), r.race_type)
    to_db.append(result)
    lap_num = 1
    for lap in r.lap_times:
        if lap != "":
           lap_to_db = Lap(location.id, driver.id, float(lap), lap_num, r.race_type)
        to_db.append(lap_to_db)
        lap_num += 1
db.session.add_all(to_db)
db.session.commit()

