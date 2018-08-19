# Imports -- you may add others but do not need to
import plotly.plotly as py
import plotly.graph_objs as go
import csv

# Code here should involve creation of the bar chart as specified in instructions
# And opening / using the CSV file you created earlier with noun data from tweets

###############################################################################
# README                                                                      #
# Author: Xizi Wang                                                           #
# UMID: 24226806                                                              #
###############################################################################

CSV_FILE = "noun_data.csv"
PNG_FILE = "part4_viz_image.png"
USERNAME = "wang3570"
API_KEY = "WSuToKptOYAs0TfXDikw"

def main():
    x_name = list()
    y_value = list()
    py.sign_in(username=USERNAME, api_key=API_KEY)
    
    with open(CSV_FILE, "rt") as csvfile:
        # fieldnames = ["Noun", "Number"]
        reader = csv.DictReader(csvfile, fieldnames=None)
        for row in reader:
            x_name.append(row["Noun"])
            y_value.append(row["Number"])

    # create a bar chart
    data = [go.Bar(x=x_name, y=y_value)]
    layout = go.Layout(title='The Five Most Frequent Noun', width=800, height=640)
    fig = go.Figure(data=data, layout=layout)

    py.image.save_as(fig, filename=PNG_FILE)


if __name__ == "__main__":
    main()

