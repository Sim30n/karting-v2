from app import db, Race
import datetime

db.create_all()

race1 = Race("Imatra", datetime.datetime(2021, 6, 5))

db.session.add_all([race1])

db.session.commit()