uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --app-dir /home/bhagavan/dev/netgenie/

### Queries
1. Will the J2 template generated from `cust101_interface.cfg` be identical to the one generated from `cust202_interface.cfg`?
1. 


### Mongodb
mongosh mongodb://admin:jnjnuh@localhost:27017/netgenie_db

show dbs
db
db.dropDatabase()

show collections
db.users.find()
db.counters.find()


