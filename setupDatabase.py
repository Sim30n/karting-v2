from app import db, Race, Driver, Result, Lap
import datetime

db.create_all()

race1 = Race("Imatra", datetime.datetime(2021, 6, 5))
driver1 = Driver("Petteri")
driver2 = Driver("Lauri")

db.session.add_all([race1, driver1, driver2])
db.session.commit()

petteri = Driver.query.filter_by(name='Petteri').all()[0]
lauri = Driver.query.filter_by(name='Lauri').all()[0]
imatra = Race.query.filter_by(location='Imatra').all()[0]

result1 = Result(petteri.id, imatra.id, 3, "qualifying")
result2 = Result(lauri.id, imatra.id, 2, "qualifying")
print(result1)
lap1 = Lap(imatra.id, petteri.id, 52.34, 1, "qualifying")

db.session.add_all([result1, result2, lap1])
db.session.commit()