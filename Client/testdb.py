import e32dbm

DB_FILE = u"E:\\flyingonwheel.db"

def write_db():
        db = e32dbm.open(DB_FILE, "cf")
        db[u"name"] = u"musli"
        db[u"password"] = u"my secret"
        db.close()

def read_db():
        db = e32dbm.open(DB_FILE, "r")
        name = db[u"name"]
        password = db[u"password"]
        print name
        print password
        db.close()

print "Writing db.."
write_db()
print "Reading db.."
read_db()
