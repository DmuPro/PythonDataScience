import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import lib

#
# Données
#

# Map
map_data = lib.getMapData()

session_visible = 2018
# On crée un dictionnaire séparant le dataframe par dates de session
sessions = map_data["session"].unique()
map_data_sessions = {session:map_data.query("session == @session") for session in sessions}

map_fig = px.scatter_mapbox(map_data_sessions[f'{session_visible}'], lat="lat", lon="lon", hover_name="g_ea_lib_vx", hover_data=["acad_mies", "voe_tot"],
                        color_discrete_sequence=["fuchsia"], zoom=4.5, height=500, size='voe_tot')
map_fig.update_layout(mapbox_style="open-street-map")
map_fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


#
# Main
#

if __name__ == '__main__':

    app = dash.Dash(__name__)

    app.layout = html.Div(
        children=[
            # SideBar
            html.Div(
                id="sidebar",
                children=[
                    html.H2(
                        children='Sommaire',
                    ),
                    # Liste de liens vers les différents diagrammes
                    html.Ul(
                        children=[
                            html.Li([
                                html.A(
                                    href="#map",
                                    children="Carte"
                                )
                            ]),
                            html.Li([
                                html.A(
                                    href="#map",
                                    children="Carte"
                                )
                            ]),
                        ]
                    ),
                ],
                style={}
            ),
            # Contenu
            html.Div(
                children=[
                    # Titre
                    html.H1(
                        children="Popularité et taux d'insertion professionnelle des formations supérieures",
                        style={'textAlign': 'center'}
                    ),
                    html.P(
                        children="Texte d'introduction",
                        style={'margin-bottom':'20px'}
                    ),
                    # Premier graphique, carte des formations post bac
                    dcc.Slider(
                        id="year-slider",
                        min=2018,
                        max=2019,
                        step=None,
                        marks={2018:'2018',2019:'2019'},
                        value=session_visible
                    ),
                    html.Div(
                        children=[
                            dcc.Graph(
                                id='map',
                                figure=map_fig
                            ),
                            html.P(
                                children="Carte de France des ",
                                style={'margin-top': '10px'}
                            )
                        ],
                        style={'margin': '10px 40px 10px 40px'}
                    )
                ],
                style={'width': '100%'}
            )
        ],
        style={'display': 'flex', 'height': '100vh'}
    )

    #
    # CALLBACKS
    #

    # Modifie la figure 'map' en fonction de la valeur du slider
    @app.callback(
        [Output(component_id='map', component_property='figure')],
        [Input(component_id='year-slider', component_property='value')]
    )
    def update_figure(input_value):
        map = px.scatter_mapbox(map_data_sessions[f'{input_value}'], lat="lat", lon="lon", hover_name="g_ea_lib_vx", hover_data=["acad_mies", "voe_tot"],
                        color_discrete_sequence=["fuchsia"], zoom=4.5, height=500, size='voe_tot')
        map.update_layout(mapbox_style="open-street-map")
        map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        return [map]

    #
    # Lancement du serveur
    #

    app.run_server(debug=True)
