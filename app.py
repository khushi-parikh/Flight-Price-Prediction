from flask import Flask, render_template, request
import pandas as pd
import pickle
from flask_cors import cross_origin

app = Flask(__name__)
model = pickle.load(open("final_model1.pkl", "rb"))

@app.route("/")
# @cross_origin()
def hello_world():
    return render_template("index.html")

@app.route("/predict", methods=['POST'])
# @cross_origin()
def predict():
    if request.method == 'POST':
        date_of_dep = request.form["Dep_Time"]
        journey_day = int(pd.to_datetime(date_of_dep, format="%Y-%m-%dT%H:%M").day)
        journey_month = int(pd.to_datetime(date_of_dep, format ="%Y-%m-%dT%H:%M").month)

        dep_hour = int(pd.to_datetime(date_of_dep, format="%Y-%m-%dT%H:%M").hour)
        dep_min = int(pd.to_datetime(date_of_dep, format="%Y-%m-%dT%H:%M").minute)

        date_of_arr = request.form["Arrival_Time"]
        arrival_hour = int(pd.to_datetime(date_of_arr, format ="%Y-%m-%dT%H:%M").hour)
        arrival_min = int(pd.to_datetime(date_of_arr, format ="%Y-%m-%dT%H:%M").minute)

        arrival_dur_min = 60*arrival_hour + arrival_min
        dep_dur_min = 60*dep_hour + dep_min
        duration_min = abs(arrival_dur_min - dep_dur_min)

        Total_Stops = int(request.form["stops"])
        airline = request.form["airline"]
        dict_air = {"Air Asia": 0, "Air India": 1, "GoAir": 2, "IndiGo": 3, "Jet Airways": 4, "Jet Airways Business": 5, "Multiple carriers": 6, "Multiple carriers Premium economy": 7, "SpiceJet": 8, "Trujet": 9, "Vistara": 10, "Vistara Premium economy": 11}
        Airline = dict_air[airline]

        source = request.form["Source"]
        dict_source = {"Banglore": 0, "Chennai": 1, "Delhi": 2, "Kolkata": 3, "Mumbai": 4}
        Source = dict_source[source]

        dest = request.form["Destination"]
        dict_dest = {"Banglore": 0, "Cochin": 1, "Delhi": 2, "Hyderabad": 3, "Kolkata": 4, "New Delhi": 5}
        Destination = dict_dest[dest]

        pred = model.predict(pd.DataFrame([[
            Airline,
            Source,
            Destination,
            Total_Stops,
            journey_day,
            journey_month,
            dep_hour,
            dep_min,
            arrival_hour,
            arrival_min,
            duration_min
        ]]))

        result = round(pred[0],2)
        
        # return render_template('index.html',prediction_text="The price of your flight is Rs. {}".format(result))

    # return render_template('index.html')
    return render_template("index.html",prediction_text="The price of your flight is Rs. {}".format(result))

if __name__ == "__main__":
    app.debug == True
    app.run()