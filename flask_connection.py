from flask import Flask    #flask is the platform that handles the webhook
from SWMM_Ha.node_flood4rmRpt import Ex_flooding
#from SWMM_Ha.SWMM_ExtrCode2 import Ex_node_pondedvol, simulate, Ex_ponded_volume
app = Flask(__name__)     #instance of the class flask
#
# @app.route("/try")                         #defines the relation between the route and the function that follows
# def home():
#     return "Hello, World! This is our first Flask app."
#
# @app.route("/pondvol")
# def pondvol():
#     return Ex_node_pondedvol("N33-1")
#
# @app.route("/nonFlood")
# def nonFlood():
#     node_pondvol, index_list, non_ponded = Ex_ponded_volume()  # assigning the function outputs to the list variables
#     return non_ponded

@app.route("/floodHrs")
def floodHrs():
    output = ""
    nodes, floodHrs = Ex_flooding()
    for i in range (len(nodes)):
        output += nodes[i]+ " " + str(floodHrs[i])+ "<br>"
    return output

app.run(debug=True)                 #the run fn starts the web server, and the program waits for connections from either a web browser or webhook





