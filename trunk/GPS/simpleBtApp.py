# Simple BT App
#$GPRMC,161229.487,A,3723.2475,N,12158.3416,W,0.13,309.62,120598, ,*10

import socket, location, urllib

class BTReader:
    def connect(self):
        self.sock = socket.socket(socket.AF_BT, socket.SOCK_STREAM)
        address, services = socket.bt_discover()
        print "Discovered: %s, %s" % (address, services)
        target = (address, services.values()[0])
        print "Connecting to " + str(target)
        self.sock.connect(target)

    def readposition(self):
        try:
            buffer=""
            ch = self.sock.recv(1)
            while(ch != '\n'):
                buffer += ch
                ch = self.sock.recv(1)
                # print buffer


                if (buffer[0:6]=="$GPRMC"):
                    (GPRMC,utc,status,lat,latns,lon,lonew,knots,course,date,xx1,xx2)=buffer.split(",")
                    return "GPS (%s,%s,%s,%s,%s)"%(utc,lat+latns,lon+lonew,knots,course)
        except Error:
            return "Error!\n"
        return ""

    def close(self):
        self.sock.close()

class GSM_loc:
    def upd(self):
        self.loc = location.gsm_location()
        return "GSM (MCC:%s MNC:%s LAC:%s CID=%s)"%(self.loc[0], self.loc[1], self.loc[2], self.loc[3])
    
gsm = GSM_loc()

bt=BTReader()
bt.connect()

i=0

while (i<15):
    print gsm.upd()
    print bt.readposition()
    i += 1

bt.close()
