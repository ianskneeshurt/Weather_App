import plotly.graph_objects as go
from plotly.subplots import make_subplots
from NWS import NationalWeather
import math

desert_coordinates = {
    'North Wash': 'https://api.weather.gov/gridpoints/SLC/133,51/forecast/hourly',
    'Capitol Reef': 'https://api.weather.gov/gridpoints/SLC/110,60/forecast/hourly',
    'Escalante': 'https://api.weather.gov/gridpoints/SLC/106,30/forecast/hourly',
    'Swell': 'https://api.weather.gov/gridpoints/SLC/106,30/forecast/hourly',
    'Arches': 'https://api.weather.gov/gridpoints/GJT/58,88/forecast/hourly',
    'Indian Creek': 'https://api.weather.gov/gridpoints/GJT/56,59/forecast/hourly'
}

weather = NationalWeather()
weather_dict = weather.make_weather_dict(desert_coordinates)


def make_weather_data_dict(weather_dict):
    """takes weather dict with place and json values from National Weather class.
    Returns dict of place and data for graphing"""
    for place, data in weather_dict.items():
        dataset = data["properties"]["periods"]
        len_data = range(len(dataset))

        time = [dataset[num]["startTime"] for num in len_data]
        precip_vals = [dataset[num]["probabilityOfPrecipitation"]["value"] for num in len_data]
        temp = [dataset[num]["temperature"] for num in len_data]
        weather_dict[place] = {"time": time, "precip": precip_vals, "temp": temp}
    return weather_dict


def make_graphs():
    """takes name of location and weather json, creates graphs"""

    data_dict = make_weather_data_dict(weather_dict)

    fig_specs = []
    for _ in range(0, len(data_dict), 2):
        fig_specs.append([{"secondary_y": True}, {"secondary_y": True}])

    fig = make_subplots(
        rows=(int(len(weather_dict)/2)),
        cols=2, specs=fig_specs, vertical_spacing=0.05, horizontal_spacing=0.08, shared_xaxes=True,
        subplot_titles=[key for key in data_dict]
    )

    # fancy looking way to get a list from 1 to the length of the number of places/2, and duplicating each number
    row_num = [num for num in range(1, math.ceil(len(data_dict)/2)+1) for _ in range(2)]
    for i, key in enumerate(data_dict):
        place_dict = data_dict[key]
        if (i+1) % 2 == 0:
            column = 2
        else:
            column = 1

        fig.add_trace(
            go.Scatter(x=place_dict["time"], y=place_dict["precip"], name="Precipitation(cm)"),
            row=row_num[i], col=column, secondary_y=False
        )
        fig.add_trace(
            go.Scatter(x=place_dict["time"], y=place_dict["temp"], name="Temperature(F)"),
            row=row_num[i], col=column, secondary_y=True
        )

    fig.update_layout(
        height=750,
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=12, label="12 hour", step="hour", stepmode="backward"),
                    dict(count=36, label="36 hour", step="hour", stepmode="backward"),
                    dict(step="all"),
                ])
            ),
            rangeslider=dict(visible=False), type="date"
        )
    )
    fig.update_layout(showlegend=False, xaxis6_rangeslider_visible=True, xaxis_type="date")

    fig.show()


make_graphs()









