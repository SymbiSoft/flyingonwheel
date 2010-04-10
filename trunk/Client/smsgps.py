########################################################
# Send an SMS with your current GPS co-ordinates using a
# Nokia SmartPhoneand PyS60
# Timothy Makobu, 01-01-2009
########################################################

import positioning
import messaging
import appuifw
import sys

# Get your GPS co-ordinates #
def getCoordinates():
    positioning.select_module(positioning.default_module())
    positioning.set_requestors([{'type': 'service', 'format': 'application', 'data': 'position'}])
    try:
        sys.stdout.write('Retrieving GPS co-ordinates ...\n')
        data = positioning.position(course=1, satellites=1)
    except:
        sys.stdout.write('Could not retrieve GPS co-ordinates\n\n\n')
        sys.exit(-1)
    else:
        sys.stdout.write('GPS co-ordinates retrieved\n')
    return (data['position']['latitude'], data['position']['longitude'])

# Send your GPS co-ordinates as an SMS #
def sendCoordinates(coords, number):
    message = u'I\'m at location:\nLatitute --> %f\nLongitute --> %f \n' % coords
    try:
        sys.stdout.write('Sending SMS ...\n')
        messaging.sms_send(number, message)
    except:
        sys.stdout.write('Could not send SMS \n\n\n')
        sys.exit(-1)
    else:
        sys.stdout.write('SMS sent \n')

if __name__ == '__main__':
    presetPhoneNumber = 15991660074
    phoneNumber = presetPhoneNumber or appuifw.query(u'Enter number: ', 'text')
    if not phoneNumber:
        sys.stdout.write('No number entered; exiting ...\n\n\n')
        sys.exit(-1)
    sendCoordinates(getCoordinates(), phoneNumber)
