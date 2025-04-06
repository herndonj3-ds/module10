import json
import requests
from flask import Flask

# API endpoint URL's and access keys
WMATA_API_KEY = "06ee69ac29194053a97ee88d0d9610f0"
INCIDENTS_URL = "https://api.wmata.com/Incidents.svc/json/ElevatorIncidents"
headers = {"api_key": WMATA_API_KEY, 'Accept': '*/*'}

################################################################################

app = Flask(__name__)

# get incidents by machine type (elevators/escalators)
# field is called "unit_type" in WMATA API response
@app.route("/incidents/<unit_type>", methods=["GET"])
def get_incidents(unit_type):
    # create an empty list called 'incidents'
    incidents = []
    # use 'requests' to do a GET request to the WMATA Incidents API
    # retrieve the JSON from the response
    incident_info = requests.get(INCIDENTS_URL, headers=headers).json()

    # Get incident info out of dictionary
    parsed_incidents = incident_info['ElevatorIncidents']

    # Change unit type depending on input
    if unit_type == 'elevators':
        unit_type = 'ELEVATOR'
    elif unit_type == 'escalators':
        unit_type = 'ESCALATOR'

  # iterate through the JSON response and retrieve all incidents matching 'unit_type'
    for incident in parsed_incidents:
        # empty dictionary for each iteration
        incident_dict = {}
        if incident['UnitType'] == unit_type:
            # for each incident, create a dictionary containing the 4 fields from the Module 7 API definition
            incident_dict = {
                'StationCode': incident['StationCode'],
                'StationName': incident['StationName'],
                'UnitType': incident['UnitType'],
                'UnitName': incident['UnitName'],
                }
            # append incident dictionary to list
            incidents.append(incident_dict)

  #   -StationCode, StationName, UnitType, UnitName
  # add each incident dictionary object to the 'incidents' list

    # return the list of incident dictionaries using json.dumps()
    return json.dumps(incidents)

if __name__ == '__main__':
    app.run(debug=True)
