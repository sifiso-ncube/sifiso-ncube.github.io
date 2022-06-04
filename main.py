from flask import (Flask, request, render_template, make_response)    #flask is the platform that handles the webhook
# request is a request object from Flask used to handle GET and POST requests
from pyswmm import Simulation

from FINAL_ExtrCode import Ex_floodHrs, Ex_NodeFloodHrs, Ex_NodePonded_depth, Ex_Node_Time_maxflood,Ex_Nodemax_floodrate,Ex_floodHrs10, Ex_NodePonded_depth10, Ex_NodeFloodHrs10,simulate
import sqlalchemy
import os
from sqlalchemy.sql import text
from revGeocode import geocode,nodes_dict
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

# Remember - storing secrets in plaintext is potentially unsafe. Consider using
# something like https://cloud.google.com/secret-manager/docs/overview to help keep
# secrets secret.
db_user = os.environ["DB_USER"]          #these are the required inputs to connect to the database
db_pass = os.environ["DB_PASS"]           #gets environment variables from the os
db_name = os.environ["DB_NAME"]
db_socket_dir = os.environ.get("DB_SOCKET_DIR", "/cloudsql")
instance_connection_name = os.environ["INSTANCE_CONNECTION_NAME"]

pool = sqlalchemy.create_engine(
    # Equivalent URL:
    # mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=<socket_path>/<cloud_sql_instance_name>
    sqlalchemy.engine.url.URL.create(
        drivername="mysql+pymysql",
        username=db_user,  # e.g. "my-database-user"
        password=db_pass,  # e.g. "my-database-password"
        database=db_name,  # e.g. "my-database-name"
        query={
            "unix_socket": "{}/{}".format(
                db_socket_dir,  # e.g. "/cloudsql"
                instance_connection_name)  # i.e "<PROJECT-NAME>:<INSTANCE-REGION>:<INSTANCE-NAME>"
        }
    ),

)

app = Flask(__name__, static_folder= "static", static_url_path='')     #instance of the class flask

#create a route for webhook
@app.route('/webhook', methods = ['POST'])

def webhook():
    req = request.get_json(silent=True, force= True)  # request is what the user types into the chatbot. It is in json format in Dialogflow.
    fulfillmentText = ''                            #initialise the fulfillment text, same as the response in the dialogflow console.
    query_result = req.get('queryResult')           # retrieve the query result. Give infor about what the user has typed. queryResult same as the one in the Diagnostic info of Dialogflow
    sessionID = req.get('session')
    intent = query_result.get("intent").get('displayName')
    params = query_result.get('parameters')
    action = query_result.get('action')
    query_text = query_result.get('queryText')
    node_name=params.get('Location_name')           # to get node name from Dialogflow


     #Welcome
    if action == 'input.welcome':
        output = AllFlood_nodes()
        fulfillmentText = "Hi! My name is SWMMBot, I can provide you with information on the flooding situation(maximum depth, duration, time of occurrence) in Do Lo, Hanoi, Vietnam. So, which location are you interested in? Please, enter your address in the format: House number [space] street, ward, district, city. OR enter the pin name closest to you from the map."

        return {
            "fulfillmentText": fulfillmentText, # return the fulfilment text to dialogflow for it to print out the response
            "displayText": '25',
            "source": "webhookdata",
        }
    # if user input is an address i.e. has more than 8 characters
    if node_name is not None and len(node_name) > 8:
        # if the user input is outside Do Lo
        try:
            lat1, long1 = geocode(node_name)
            point = Point(lat1, long1)
            polygon = Polygon([(20.940415, 105.739589), (20.943201, 105.744567), (20.946006, 105.744719), (20.948542, 105.743384),(20.951405, 105.743611),(20.957370, 105.738938), (20.954267, 105.735023), (20.948391, 105.738783),(20.942156, 105.736582)])
            rezult = polygon.contains(point)

            if rezult == False:
                fulfillmentText = "Sorry, the location you entered is outside DoLo, for now I can only provide you with information for Do Lo, Hanoi, Vietnam.Please enter another location."

                return {
                    "fulfillmentText": fulfillmentText,
                    # return the fulfilment text to dialogflow for it to print out the response
                    "displayText": '25',
                    "source": "webhookdata",
                }

        except IndexError:
            fulfillmentText = "I am failing to locate this address.Please, enter your address in the format: House number [space] street, ward, district, city. Also remember location names from the map are in the format N77-1"

            return {
                "fulfillmentText": fulfillmentText,
                # return the fulfilment text to dialogflow for it to print out the response
                "displayText": '25',
                "source": "webhookdata",
            }

        # IF USER INPUTS A NODE NAME
    if node_name == "" or node_name is None:
        with pool.connect() as con:  # its a way to connect to the db faster.pool is so that we can have many connections to the database.
            resultrows = (con.execute(text("SELECT location_name from swmm_dingsbums WHERE session_id =:sessionID"),
                                      # we filter the users based on session ID.
                                      sessionID=sessionID))  # SQl will take the parameter name after the : and look for a matching parameter outside the text and take the value of that parameter
            # we want to extract the latest location input from the user.
            for row in resultrows:
                node_name = row[0]  # gets all the node_names which the user inputs, which the only column. and since we are interested in the latest value that is the last one generated.

    # IF USER INPUTS AN ADDRESS get the nearest node name
    if len(node_name) > 8:  # if user input is an adress i.e. has more than 8 characters
        node_name = Find_nearest_node(node_name)  # here node_name is the address the user inputs and it calls the find_nearest_node function

    node_name = node_name.capitalize()
    # Flooding state 1 location
    if action == 'node.location':  # checking if the action key matches node.location
        if FloodedLoc(node_name) == True:
            fulfillmentText = "Your location " + params.get('Location_name')  + " is flooded. What else would you like to know about the flooding situation?"
        else :
            fulfillmentText = "Your location " + params.get('Location_name')  + " is not flooded. If you're interested in getting information for another location, please enter the address or the pin name from the map?"

    #Max flood depth(level)
    elif action =='maxponded.depth':
        if FloodedLoc(node_name) == True:
            depth = Ex_NodePonded_depth(node_name)
            fulfillmentText = "The maximum depth of flooding at your location " + " is " + str(depth) + " metres. Remember not to walk or drive in flood water especially if it's flowing above your ankles. Would you like to know anything else about the flooding situation?"
        else :
            fulfillmentText = "The requested location " + params.get('Location_name') + " is not flooded."

    # # 10 yr return Max flood depth(level)
    elif action == 'tenyr.depth':
        if FloodedLoc10(node_name) == True:
            depth10 = Ex_NodePonded_depth10(node_name)
            fulfillmentText = "The the maximum depth of flooding at your location for a flood with a return period of 10 years is " + str(depth10) + " metres. Is there anything else?"
        else:
            fulfillmentText = "The requested location will not be flooded."


    # flood duration
    elif action == 'flood.duration':
        if FloodedLoc(node_name):
            hours = Ex_NodeFloodHrs(node_name,"swmm.rpt", 759, 869)
            fulfillmentText = "Your requested location will be flooded for " + str(hours) + " hours. Is there anything else you would like to know about the flooding situation? "
        else :
            fulfillmentText = "Your location is not flooded."

    # # 10 yr return flood duration
    elif action == 'tenyr.duration':
        if FloodedLoc10(node_name):
            hours10 = Ex_NodeFloodHrs10(node_name)
            fulfillmentText = "For a flood with a return period of 10 years, your requested location will be flooded for " + str(hours10) + " hours. Can i help you with anything else about the flooding situation?"
        else:
            fulfillmentText = "Your location is not flooded."

        # Time of max flood
    elif action == 'Tmax.flood':
        if FloodedLoc(node_name) == True:
            tmaxfl= Ex_Node_Time_maxflood(node_name)
            fulfillmentText = "The day and time at which flooding will be maximum is at " + str(tmaxfl) + ". Is there something else about flooding you would be interested in knowing?"
        else :
            fulfillmentText = "The requested location " + params.get('Location_name')  + " is not flooded."

    #Max flood rate
    elif action =='max.floodrate':
        if FloodedLoc(node_name) == True:
            maxfloodrate = Ex_Nodemax_floodrate(node_name)
            fulfillmentText = "The maximum flooding rate at " + params.get('Location_name')  + " will be " + str(maxfloodrate) + " cubic metres per second. Is there anything else you would want to know about the flooding situation?"
        else :
            fulfillmentText = "The requested location " + params.get('Location_name')  + " is not flooded."

    # What to do?
    elif action =='act.respond':
        depth = Ex_NodePonded_depth(node_name)
        fulfillmentText = "Since the maximum water depth will be " + str(depth) + " metres, if you recieve an 'alert' to evacuate OR your house doesn't have a floor higher than this depth, please go to the nearest Emergency Shelter. IF you must drive, the water depth must be below 20cm or below half the height of your car wheels. Otherwise, here's what you can do: 1. when water depth is below 20cm ensure that all important items are stored at a high, dry place, switch off switches,gas and close taps 2. for water depths between 20-50 cm take your emergency package(food, water, warm clothing) with you to a higher floor, 3.between 80cm - 2m, the 1st floor of your house is safe, 4. between 2m - 5m, the second floor of your house is safe. Above 5m, go to the highest point in your house and wait for the emergency rescue team.Check radio and SMS alerts. For more tips visit: https://www.risicokaart.nl/en/what-risks-are-there/flood or  https://www.ready.gov/pfloods. That is all I have for you today? For information on another location, please enter the address or the pin name from the map. Otherwise, BE SAFE!"

        # All Flooded Locations
    if action == 'flood.locations':
        output = AllFlood_nodes()
        fulfillmentText = "Hi! Currently, there are " + str(len(output)) + " out of 167 " + "flooded locations in the area.  These are: " + str(output) + "Be careful out there"

    if action == 'model.run':
        sim = Simulation("DoLo.inp", "/tmp/DoLo.rpt", "/tmp/DoLo.out" ) # to write the report n output file into the temporary folder.
        # because App Engine doesnt allow writing of files in the normal folders hence the temp
        sim.execute() # executing take 4 mins but Dialogflow only allows 5 sec to generate a reply https://cloud.google.com/dialogflow/es/docs/fulfillment-webhook#webhook_response
        #Dialogflow will then show the response set in Dialogflow for this intent. So the webhook continues running SWMM and writes the output files.
        #the output file are temporary so when the next action is called they will have been deleted so we have to save them in the database:
        with open("/tmp/DoLo.rpt", "r") as f:
            report_lines = f.read()
            with pool.connect() as con:
                con.execute(text(
                    "INSERT INTO swmm_reportfile(session_id, content_data) values(:session_id, :content_data)"), # so we created a new row in the new table called swmm_reportfile created in Cloudshell
                            session_id=sessionID, content_data=report_lines)

    if action == "model.finish":  # this intent uses the values from the table in the database
        with pool.connect() as con:  # its a way to connect to the db faster.pool is so that we can have many connections to the database.
            resultrows = (con.execute(text("SELECT content_data from swmm_reportfile WHERE session_id =:sessionID"),
                                      # we filter the users based on session ID.
                                      sessionID=sessionID))
            for row in resultrows:
                report = row[0]  # we are getting the whole report from the table under the heading content_data and since we are interested in the latest value that is the last one generated.

            with open("/tmp/final_report", "w" ) as file: #we have to write the file because the Ex_NodeFloodHours function assumes its a file.
                 file.write(report[report.find("10^6 ltr    Meters"):])  # a way of extracting string from string

            hours = Ex_NodeFloodHrs(node_name, "/tmp/final_report",3,114) # the function takes 2 parameters because we now have two diffrent file to read from.
            fulfillmentText = "Yes, I am done running the model.Your Your requested location will be flooded for " + str(hours) + "hours."

            #else:
                #fulfillmentText = "No, I am not done yet."


    with pool.connect() as con:  # its a way to connect to the db faster.pool is so that we can have many connections to the database.
        # establishes a connection with the db. first you specify the headings and then what should go under the headings ie values
        con.execute(text("INSERT INTO swmm_dingsbums(session_id, intent, location_name) values(:session_id, :intent, :location_name)"),
                    session_id = sessionID, intent = intent, location_name = node_name )



    return{
        "fulfillmentText": fulfillmentText,     # return the fulfilment text to dialogflow for it to print out the response
        "displayText" : '25',
        "source": "webhookdata",
    }


def FloodedLoc(node_name):
    nodes, floodHrs = Ex_floodHrs()
    return node_name in nodes    # checks if the specified node is in the flooded nodes list


def FloodedLoc10(node_name):
    nodes, floodHrs = Ex_floodHrs10()
    return node_name in nodes     # checks if the specified node is in the flooded nodes list


def AllFlood_nodes():
    output = []
    nodes, floodHrs = Ex_floodHrs()
    for i in range(len(nodes)):
        output.append(nodes[i] + ",")
    return output

def Find_nearest_node(node_name):
    min_distance = 10000000000
    min_distnode = None                 # the node with the min distance
    lat_user_input, lon_user_input = geocode(node_name)
    with pool.connect() as con:  # its a way to connect to the db faster.pool is so that we can have many connections to the database.
        for i in nodes_dict:
            node = nodes_dict[i]

            distances = (con.execute(text("SELECT ST_Distance_Sphere(point(:lon, :lat),point(:node_lon,:node_lat ))"),    # lat n lon are the output of the geocoding from user's adress. so we want to compare with the node coordinates that we have
                                         lon=lon_user_input, lat=lat_user_input, node_lon= node.get("lon"), node_lat= node.get("lat")))  # SQl will take the parameter name after the : and look for a matching parameter outside the text and take the value of that parameter

            for row in distances:
                    distance = row[0]  # give the distance between the user input and the selected node
            if distance < min_distance:
               min_distance = distance
               min_distnode = node       #it will go through all the nodes checking the min distances and retains the node with the min distance.
        return min_distnode.get("name")

#Adding the HTML page
@app.route('/', methods = ['GET'])         # the route function is a decorator function. decorator functions give additional functionality to existing functions
def home():
    return render_template("index3.html")

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True) #the run fn starts the web server, and the program waits for connections from either a web browser or webhook


#cloud shell link for database  https://console.cloud.google.com/sql/instances/swmmbot-db/overview?project=swmmbot&cloudshell=true
#googleApp engine file system is read only https://cloud.google.com/appengine/docs/standard/python3/runtime#filesystem

#to create the application on GAE: https://www.youtube.com/watch?v=ZGn5ahF6Bv0



# This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. You
    # can configure startup instructions by adding `entrypoint` to app.yaml.




