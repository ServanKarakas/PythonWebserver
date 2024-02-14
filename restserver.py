from flask import Flask, Response, request, json
from flask_cors import CORS
from datetime import datetime, timedelta
import traceback 

api = Flask(__name__)
CORS(api)



# Your existing route to get all data
@api.route('/data', methods=['GET'])
def get_data():
    with open("data.json", "r") as infile:
        data = json.load(infile)
        return Response(json.dumps(data),mimetype='application/json')



@api.route('/datalog', methods=['GET'])
def get_datalog():
    try:
        # ?time=60&endTime=2023-01-01T00:00:00
        time = request.args.get('time')

        # Check if endTime is missing in the request
        if time is None:
           return Response(json.dumps({"error": "Parameter time is not defined"}, mimetype='application/json'), status=400)

        # Parse end_time from string to datetime object
        time_difference = datetime.now() - timedelta(minutes=int(time))

        with open("datalog.json", "r") as infile:  
            lines = infile.readlines()
            linearray = []

            for line in lines:
                line_json = json.loads(line)
                log_time = datetime.strptime(str(line_json['time']), "%Y-%m-%d %H:%M:%S")

                # Überprüfe, ob log_time im spezifizierten Zeitbereich liegt
                if time_difference != log_time:
                    linearray.append(line_json)

            return Response(json.dumps(linearray), mimetype='application/json')

    except Exception as e:
    # Fange alle möglichen Fehler ab und logge sie
        print(f"Exception: {e}")
        traceback.print_exc()
        return Response(json.dumps({'error': 'Interner Serverfehler'}), status=500, mimetype='application/json')

if __name__ == '__main__':
    api.run(debug=True, host='0.0.0.0', port=8081)

