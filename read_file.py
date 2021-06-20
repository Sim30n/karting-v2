import csv

class Result:
    def __init__(self, location, driver, race_type, race_date):
        self.location = location
        self.driver = driver
        self.race_type = race_type
        self.race_date = race_date
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
                new_result = Result(location, i, race_type, race_date)
                results.append(new_result)
        elif line_count > 2:
            for i in range(len(results)):
                results[i].lap_times.append(row[i])
        line_count += 1

print(results[0].driver, results[0].location, results[0].race_type, results[0].lap_times, results[0].race_date)