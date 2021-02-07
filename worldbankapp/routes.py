from worldbankapp import app

import json
import plotly
from flask import render_template, request, Response, jsonify
from .data import return_figures

@app.route("/")
@app.route("/index")
def index():
    """
    
    """
    
    # test list -> replace with full list
    country_codes = [["Canada", "CAN"], ["United States", "USA"], ["Brazil", "BRA"], ["France", "FRA"], ["Germany", "DEU"]]

    # create all figures
    figures = return_figures()
    
    # get country list
    countries_selected = []
    for country in country_codes:
        countries_selected.append(country[1])   

    ids = ["figure-{}".format(i) for i, _ in enumerate(figures)]

    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    # render dashboard
    return render_template("index.html", 
                           ids=ids,
                           figuresJSON=figuresJSON,
                           all_countries=country_codes,
                           countries_selected=countries_selected)

