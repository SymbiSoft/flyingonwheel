class MainPage(webapp.RequestHandler):
    def get(self):
        # choice which days to view
        startdate = self.request.get("startdate")
        enddate = self.request.get("enddate")
        if startdate == None or startdate == '' or not matchdateformat(startdate):
            startdate = date.today()
        else:
            # format the startdate
            startdate = stringtodate(startdate)
        if enddate == None or enddate == '' or not matchdateformat(enddate):
            enddate = date.today() + datetime.timedelta(days = 1)
        else:
            # format the enddate
            enddate = stringtodate(enddate)
        markedpoints = db.GqlQuery ("SELECT * FROM MarkedPoint WHERE date > :1 AND date < :2 ORDER BY date DESC", startdate, enddate)
        #html map starts here
        self.response.out.write('<html><head>')
        self.response.out.write("""
        <meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
        <meta http-equiv="content-type" content="text/html; charset=UTF-8"/>
        <title>Flying on Wheel~</title>
        <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
        <!-- JS Date Control -->
        <script language="javascript" src="/static/jquery-1.4.2.min.js" ></script>
        <script language="javascript" src="/static/jquery.date_input.js" ></script>
        <link rel="stylesheet" href="/static/date_input.css" type="text/css">
        """)
        self.response.out.write("""
        <script type="text/javascript">
            function detectBrowser() {
                var useragent = navigator.userAgent;
                //alert(useragent);
                var mapdiv = document.getElementById("map_canvas");
                //alert(useragent.indexOf('Mozilla'));
                if (useragent.indexOf('Mozilla') != -1 || useragent.indexOf('Android') != -1 ) {
                    //alert("computer");
                    mapdiv.style.width = '640px';
                    mapdiv.style.height = '360px';
                } else {
                    //alert("mobile");
                    mapdiv.style.width = '640px';
                    mapdiv.style.height = '360px';
                }
            }
        </script>
        """)
        tempString = "var waypoints = [];";#for waypoints' javascript array
        for mp in markedpoints:
            tempString += 'addLatLng("%s", %s);' % (mp.name, mp.point);
            tempString += 'waypoints.push("%s");' % mp.point;
        #self.response.out.write('<div>%s</div>' % tempString)
        tempString += 'calcRoute(waypoints);';
        
        self.response.out.write("""
        <script type="text/javascript">
            var map;
            var pathCoordinates = [];
            var poly;
            var directionDisplay;
            var directionsService = new google.maps.DirectionsService();
            
            var image = new google.maps.MarkerImage('/static/mark.png',
                new google.maps.Size(60, 60),
                new google.maps.Point(0,0),
                new google.maps.Point(-12, 32));
            var shadow = new google.maps.MarkerImage('/static/mark_shadow.png',
                new google.maps.Size(60, 60),
                new google.maps.Point(0,0),
                new google.maps.Point(-12, 32));
            
            function initialize() {
                directionsDisplay = new google.maps.DirectionsRenderer();
                var myLatLng = new google.maps.LatLng(34.506445,109.517914);
                var myOptions = {
                    zoom: 15,
                    center: myLatLng,
                    mapTypeId: google.maps.MapTypeId.ROADMAP
                };
                map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
                //pathCoordinates = new google.maps.MVCArray();
                var polyOptions = {
                    path: pathCoordinates,
                    strokeColor: "#FF0000",
                    strokeOpacity: 0.5,
                    strokeWeight: 1
                }
                poly = new google.maps.Polyline(polyOptions);
                poly.setMap(map);
                directionsDisplay.setMap(map);
                detectBrowser();
                %s
            }
            function addLatLng(name, lat, lng) {
                //alert("lat: " + lat);
                //alert("lng: " + lng);
                var latLng = new google.maps.LatLng(lat, lng);
                //alert(latLng);
                var path = poly.getPath();
                path.insertAt(pathCoordinates.length, latLng);
                var marker = new google.maps.Marker({
                    position: latLng,
                    map: map,
                    title: name,
                    icon: image,
                    shadow: shadow
                });
            }
            function calcRoute(points) {
                var start = points[0];
                //alert(start);
                var end = points[points.length-1];
                //alert(end);
                //alert(points.length)
                var waypts = [];
                for (var i = 1; i < points.length-1; i++) {
                    waypts.push({
                        location: points[i],
                        stopover: true});
                }
                var request = {
                    origin: start, 
                    destination: end,
                    waypoints: waypts,
                    optimizeWaypoints: true,
                    travelMode: google.maps.DirectionsTravelMode.DRIVING
                };
                directionsService.route(request, function(response, status) {
                    if (status == google.maps.DirectionsStatus.OK) {
                        directionsDisplay.setDirections(response);
                    }
                });
            }
        </script>
        """ % tempString)
        self.response.out.write('</head>')
        self.response.out.write("""<body style="margin:0px; padding:0px;" onload="initialize()">""")
        # init js date control
        self.response.out.write("""
        <script type="text/javascript">
            $($.date_input.initialize);
            $.extend(DateInput.DEFAULT_OPTS, {
                stringToDate: function(string) {
                    var matches;
                    if (matches = string.match(/^(\d{4,4})-(\d{2,2})-(\d{2,2})$/)) {
                        return new Date(matches[1], matches[2] - 1, matches[3]);
                    } else {
                        return null;
                    };
                },
                dateToString: function(date) {
                    var month = (date.getMonth() + 1).toString();
                    var dom = date.getDate().toString();
                    if (month.length == 1) month = "0" + month;
                        if (dom.length == 1) dom = "0" + dom;
                            return date.getFullYear() + "-" + month + "-" + dom;
                }
            });            
        </script>""")
        self.response.out.write("""
        <div>
            <form action=".">
                <input readonly type="text" name="startdate" id="startdate" class="date_input" value="%s">
                <input readonly type="text" name="enddate" id="enddate" class="date_input" value="%s">
                <input type="submit" value="SHOW"/>
            </form>
        </div>
        """ % (startdate, enddate))
        self.response.out.write("""<div id="map_canvas" style="width: 40%; height: 40%;"></div>""")
        self.response.out.write("""</body></html>""")
        #html map ends here
class Mark(webapp.RequestHandler):
    """A database of the points"""
    def get(self):
#        user = users.get_current_user()
#        if user:
#            pass
#        else:
#            self.redirect(users.create_login_url(self.request.uri))
        """show the points which choice which days to view"""
        # choice which days to view
        startdate = self.request.get("startdate")
        enddate = self.request.get("enddate")
        if startdate == None or startdate == '' or not matchdateformat(startdate):
            startdate = date.today()
        else:
            # format the startdate
            startdate = stringtodate(startdate)
        if enddate == None or enddate == '' or not matchdateformat(enddate):
            enddate = date.today() + datetime.timedelta(days = 1)
        else:
            # format the enddate
            enddate = stringtodate(enddate)
        markedpoints = db.GqlQuery ("SELECT * FROM MarkedPoint WHERE date > :1 AND date < :2 ORDER BY date DESC", startdate, enddate)
        # html form starts here
        # html head and impot the lib
        self.response.out.write("""
        <html>
            <head>
                <meta http-equiv="content-type" content="text/html; charset=UTF-8"/>
                <title>Flying on Wheel</title>
                <!-- JS Date Control -->
                <script language="javascript" src="/static/jquery-1.4.2.min.js" ></script>
                <script language="javascript" src="/static/jquery.date_input.js" ></script>
                <link rel="stylesheet" href="/static/date_input.css" type="text/css">
            </head>
            <body>        
        """)
        # init js date control
        self.response.out.write("""
        <script type="text/javascript">
            $($.date_input.initialize);
            $.extend(DateInput.DEFAULT_OPTS, {
                stringToDate: function(string) {
                    var matches;
                    if (matches = string.match(/^(\d{4,4})-(\d{2,2})-(\d{2,2})$/)) {
                        return new Date(matches[1], matches[2] - 1, matches[3]);
                    } else {
                        return null;
                    };
                },
                dateToString: function(date) {
                    var month = (date.getMonth() + 1).toString();
                    var dom = date.getDate().toString();
                    if (month.length == 1) month = "0" + month;
                        if (dom.length == 1) dom = "0" + dom;
                            return date.getFullYear() + "-" + month + "-" + dom;
                }
            });            
        </script>
        """)
        # the control of date
        self.response.out.write("""
        <div>
            <form action="/mark">
                <input readonly type="text" name="startdate" id="startdate" class="date_input" value="%s">
                <input readonly type="text" name="enddate" id="enddate" class="date_input" value="%s">
                <input type="submit" value="SHOW"/>
            </form>
        </div>
        """ % (startdate, enddate))
        # show the points in a table
        self.response.out.write("""
        <table style="width: 40%" align="left">
            <tr align="left">
                <th>Adress Name</th>
                <th>Coordinate Point</th>
                <th>Time</th>
            </tr>
        """)
        for markedpoint in markedpoints:
            self.response.out.write('<tr><td>%s</td><td>%s</td><td>%s</td></tr>' % (markedpoint.name, markedpoint.point, markedpoint.date))
        self.response.out.write("""
        </table>
        """)
        # a post form for update the point
        self.response.out.write("""
                <div style="width: 40%" align="left">
                <form action="/mark" method="post">
                    <div><label>Adress Name:</label></div>
                    <div><textarea name="name" rows="3" cols="60"></textarea></div>
                    <div><label>Coordinates:</label></div>
                    <div><textarea name="point" rows="3" cols="60"></textarea></div>
                    <div><input type="submit" value="Mark"/></div>
                </form>
                </div>
            </body>
        </html>
        """)
        #html form ends here
    def post(self):
        """Catch the post which update the points"""
        markedpoint = MarkedPoint(date=datetime.datetime.now() + datetime.timedelta(hours = 8))
        markedpoint.name = self.request.get("name")
        markedpoint.point = self.request.get("point")
        markedpoint.put()
        self.redirect('/mark')
