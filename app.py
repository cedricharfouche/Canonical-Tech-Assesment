from flask import Flask, request, jsonify, abort
from datetime import datetime
from threading import Lock
import itertools

#Cedric Harfouche
#This is my first time ever doing anything like this, so please excuse my barebones, and simple approach. 

# Initializing Flask  app
app = Flask(__name__)


#event_log will store a list of the logged events that get posted
event_log = []
#Using lock() throughout this script ensures that concurrent access to the event_log list is safe and prevents race conditions. I've never used this before and after some research, I found it to be the simplest and best approach for me to implement. 
log_lock = Lock()
#This will generate unique IDs for each event that gets posted so that they may be retrieved by a get call to events/1
event_id_counter = itertools.count(1)



#Route for an endpoint called events
@app.route('/events', methods=['POST'])
def create_event():
    #parses body of the request to check for contents
    data = request.json
    #if any of the 3 required fields are missing, request gets aborted.
    if not data or 'event_type' not in data or 'service_name' not in data or 'additional_data' not in data:
        abort(400, 'Invalid request format')
    
    event = {
        'event_id': next(event_id_counter), #guarantees unique id for each event posted
        'event_creation_date': datetime.now(), #create simple timestamp
        'event_type': data['event_type'], #allows the user to input any description for event_type in a POST request
        'additional_data': data['additional_data'] # this is a field I added to allow for any other possible description or identifiers to be added to a specific event
    }
    
    with log_lock:
        event_log.append(event) #appends events to the logs in a thread-safe manner.
    
    return jsonify(event), 201 #simply return 201 if successful POSTrequest


#same route /events but a GET call.
#if no events were posted before this GET call gets made, then this will return an empty response. 
#returns all logged events. 
@app.route('/events', methods=['GET'])
def get_events():
    with log_lock:
        if not event_log:
            return jsonify({"Message" : "No events present in logs"}), 200
        return jsonify(event_log), 200
    

#This endpoint is to retrieve specific events by the associated event_id
#this is the value that gets created when a POST request gets sent
@app.route('/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    with log_lock:
        #This searches for the specific event with the event_id value, if no event with that event_id is found, then event gets set to None, triggering a 404 response. 
        event = next((e for e in event_log if e['event_id'] == event_id), None)
        if event is None:
            abort(404, 'Event not found')
        return jsonify(event), 200




#this allows for the Flask app to only run when the script is executed directly, rather than when it's imported as a module in another script. This is another chunk of code I was unfamiliar with but found to be a recommended implementation. 
if __name__ == '__main__':
    app.run(debug=True)