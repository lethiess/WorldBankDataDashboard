import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.colors
import requests
from collections import OrderedDict


# default list of all countries of interest
country_default = OrderedDict([('Canada', 'CAN'), ('United States', 'USA'), 
  ('Brazil', 'BRA'), ('France', 'FRA'), ('India', 'IND'), ('Italy', 'ITA'), 
  ('Germany', 'DEU'), ('United Kingdom', 'GBR'), ('China', 'CHN'), ('Japan', 'JPN'),
  ('Australia', 'AUS'), ('Myanmar', 'MMR'), ('Netherlands', 'NLD'), ('Russia', 'RUS')])

def return_figures(countries=country_default):
    """
    Create the data visualization plots.

    Parameter:
    countries: Defines the country of which the data is shown.

    Return:
    A list of plotly graphs.

    """

    # use default country list if there is no selection     
    if not bool(countries):
      countries = country_default

    # prepare country filter for API request at World Bank Data
    # format: "xx;yy;zz" -> e.g.: "gb;us;id"
    country_filter = list(countries.values())
    country_filter = [x.lower() for x in country_filter]
    country_filter = ";".join(country_filter)

    # World Bank Data indicators
    indicators = []
    indicators.append("EG.USE.ELEC.KH.PC") # electic power consumption
    indicators.append("EG.ELC.ACCS.ZS")    # access to electricity
    indicators.append("EG.USE.COMM.FO.ZS") # fossil fuel energy consumption
    indicators.append("EG.USE.COMM.CL.ZS") # alternative and nuclear power

    data_frames = []
    urls = []

    # request data from World Bank API
    for indicator in indicators:
      url = "https://api.worldbank.org/v2/countries/" + country_filter +\
        "/indicators/" + indicator + "?date?1990:2015&per_page=1000&format=json"
      urls.append(url)

      try:
        r = requests.get(url)
        data = r.json()[1]
      except:
        print("could not load data") # TODO: use logging

      for i, value in enumerate(data):
        value["indicator"] = value["indicator"]["value"]
        value["country"] = value["country"]["value"]

      data_frames.append(data)

    # prepare plot 1
    graph_one = []
    df_one = pd.DataFrame(data_frames[0])

    df_one = df_one[(df_one["date"] == "2012") | (df_one["date"] == "1990")]
    df_one.sort_values("value", ascending=False, inplace=True)

    countrylist = df_one.country.unique().tolist()

    for country in countrylist:
      x_val = df_one[df_one["country"] == country].date.tolist()
      y_val = df_one[df_one["country"] == country].value.tolist()
      graph_one.append(
        go.Scatter(
          x = x_val,
          y = y_val,
          mode = "lines",
          name = country
        )
      )  

    layout_one = dict(title = "Electric power consumption (kWh per capita)",
                      xaxis = dict(title = "Country"),
                      yaxis = dict(title = "kWh per capita"))    

    
    # plot 2
    graph_two = []
    df_two = pd.DataFrame(data_frames[1])

    df_two = df_two[(df_two["date"] == "2012") | (df_two["date"] == "1990")]
    df_two.sort_values("value", ascending=False, inplace=True)

    for country in countrylist:
      x_val = df_two[df_two["country"] == country].date.tolist()
      y_val = df_two[df_two["country"] == country].value.tolist()
      graph_two.append(
        go.Scatter(
          x = x_val,
          y = y_val,
          mode = "lines",
          name = country
        )
      )  

    layout_two = dict(title = "Access to electricity (% of population)",
                      xaxis = dict(title = "Country"),
                      yaxis = dict(title = "% of population"))    

    # plot 3
    graph_three = []
    df_three = pd.DataFrame(data_frames[2])

    df_three = df_three[(df_three["date"] == "2015") | (df_three["date"] == "1990")]
    df_three.sort_values("value", ascending=False, inplace=True)

    countrylist = df_three.country.unique().tolist()

    for country in countrylist:
      x_val = df_three[df_three["country"] == country].date.tolist()
      y_val = df_three[df_three["country"] == country].value.tolist()
      graph_three.append(
        go.Scatter(
          x = x_val,
          y = y_val,
          mode = "lines",
          name = country
        )
      )  

    layout_three = dict(title = "Fossil fuel energy consumption (% of total)",
                      xaxis = dict(title = "Country"),
                      yaxis = dict(title = "% of total"))   

    # plot 4
    graph_four = []
    df_four = pd.DataFrame(data_frames[3])

    df_four = df_four[(df_four["date"] == "2015") | (df_four["date"] == "1990")]
    df_four.sort_values("value", ascending=False, inplace=True)

    for country in countrylist:
      x_val = df_four[df_four["country"] == country].date.tolist()
      y_val = df_four[df_four["country"] == country].value.tolist()
      graph_four.append(
        go.Scatter(
          x = x_val,
          y = y_val,
          mode = "lines",
          name = country
        )
      )  

    layout_four = dict(title = "Alternative and nuclear energy (% of total energy use)",
                      xaxis = dict(title = "Country"),
                      yaxis = dict(title = "% of total energy use")) 

    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))
    figures.append(dict(data=graph_four, layout=layout_four))

    return figures