import pickle
import json
import os
import glob
import re
import csv
import base64

import pandas as pd
import flask
import dash_auth
import pandas as pd
import dash
import dash_table
import dash_core_components as dcc
import dash_cytoscape as cyto
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

# from cytograph import cytograph
from edge_generator import DataVersion_Manager
from my_style import generate_stylesheet
# from edge_generator import make_drug_table, make_indications_tabledata

# Load extra layouts
cyto.load_extra_layouts()

# app initialize
app = dash.Dash(__name__,
                # url_base_pathname='/interactive_cascade/',
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                # serve_locally=False,
                prevent_initial_callbacks=True, 
                # suppress_callback_exceptions=True
                )
server = app.server

VALID_USERNAME_PASSWORD_PAIRS = {
    'takedat': 'fronteot2021'
}

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

dm = DataVersion_Manager()
nodes, edges = dm.paging()
es = nodes+edges


cytograph =  cyto.Cytoscape(
                    id='cytoscape',
                    layout={
                        'name': 'dagre',
                        'padding': 1,
                        'spacingFactor': 1.7,
                        'animate': True,
                        'animationDuration': 1000
                    },
                    stylesheet=generate_stylesheet(),
                    style={'width': '70%',
                            'height': '580px',
                            'background-color':'#fafafa',
                            'border': 'solid thin #cedded',
                            'border-radius': '5px',
                            'border-color': '#3498DB'
                            },
                    elements=es,
                    boxSelectionEnabled=True,
            )

app.layout = html.Div( [
    html.Div([
        cytograph,
        # html.P('EdgeScore:, className="lead",', id='edge_score'),
        html.Div(dbc.Jumbotron([
            html.H2('Target', id='target'),
            html.Hr(className="my-2"),
            html.Div(id='info_sent'),
         ], style={'height': '580px'}), style={'height': '580px', 'width': '30%'}
        ),
    ], style={'display': 'flex'}),
    ], style={'padding': '5px'}
)


@app.callback([Output('info_sent', 'children'), Output('target', 'children')], [Input('cytoscape', 'mouseoverNodeData')])           
def update_info_by_tap(target):
    target = target['id']
    sent = html.P('')

    if target in dm.genes:
        sent = html.P(dm.info.loc[target, 'disease'], className="lead",)

    return sent, target


# @app.callback([Output('indication_table', 'data'), Output('ind_name', 'children')],
#             [Input('drug_table', 'selected_cells')],
#             [State('drug_table', 'data')])           
# def update_indications(cells, data):
#     cell = cells[0]
#     row = cell['row']

#     df = pd.DataFrame.from_dict(data)
#     target = df.iloc[row, 0]
#     return dm.make_indications_tabledata(target), 'Drug Indication: '+target


# @app.callback([Output('edge_score', 'children')],
#             [Input('cytoscape', 'tapEdgeData')])           
# def display_score_by_tap(target):
#     score = target['score']
#     return ['EdgeScore:{}'.format(score)]


# @app.callback([Output('cytoscape', 'elements')],
#             [Input('version_selector', 'value')])   
# def update_cytoscape_by_version(version):
#     dm.update_graph(version)
#     nodes, edges = dm.paging()
#     es = nodes+edges
#     return [es]

# if __name__ == "__main__":
#     app.run_server(debug=True)
#     # app.run_server()
