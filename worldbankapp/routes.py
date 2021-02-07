from worldbankapp import app

import json
import plotly
from flask import render_template, request, Response, jsonify
from .data import return_figures

@app.route("/", methods=["POST", "GET"])
@app.route("/index", methods=["POST", "GET"])
def index():
    """
        This function defines the behaviour and content of the 
        index page.
    """
    # country list (default)
    country_codes = [["Canada", "CAN"], ["United States", "USA"], ["Brazil", "BRA"],
     ["France", "FRA"], ["Germany", "DEU"], ["India", "IND"], ["Italy", "ITA"],
     ["United Kingdom", "GBR"], ["China", "CHN"], ["Japan", "JPN"], ["Australia", "AUS"],
     ["Myanmar", "MMR"], ["Netherlands", "NLD"], ["Russia", "RUS"]]

    # get figures depending on selected countries
    if (request.method == "POST") and request.form:
        figures = return_figures(request.form)

        countries_selected = []
        for country in request.form.lists():
            countries_selected.append(country[1][0])
    else:
        figures = return_figures()

        countries_selected = []
        for country in country_codes:
            countries_selected.append(country[1])   

    # prepare ids for the plot in the html file
    ids = ["figure-{}".format(i) for i, _ in enumerate(figures)]

    # convert plotly figures to JSON format  
    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    # render dashboard
    return render_template("index.html", 
                           ids=ids,
                           figuresJSON=figuresJSON,
                           all_countries=country_codes,
                           countries_selected=countries_selected)

