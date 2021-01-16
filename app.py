import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import lib

#
### Données
#

url_dict = {
    'etablissement_df_2018':'https://data.education.gouv.fr/api/records/1.0/search/?dataset=fr-esr-parcoursup-2018&q=&sort=tri&facet=session&facet=contrat_etab&facet=cod_uai&facet=g_ea_lib_vx&facet=dep_lib&facet=region_etab_aff&facet=acad_mies&facet=fili&facet=form_lib_voe_acc&facet=regr_forma&facet=fil_lib_voe_acc&facet=detail_forma&facet=tri',
    'etablissement_df_2019':'https://data.education.gouv.fr/api/records/1.0/search/?dataset=fr-esr-parcoursup&q=&sort=tri&facet=session&facet=contrat_etab&facet=cod_uai&facet=g_ea_lib_vx&facet=dep_lib&facet=region_etab_aff&facet=acad_mies&facet=fili&facet=form_lib_voe_acc&facet=regr_forma&facet=fil_lib_voe_acc&facet=detail_forma&facet=tri',
    'etablissement_df_2016-2017': 'https://data.education.gouv.fr/api/records/1.0/search/?dataset=apb-voeux-de-poursuite-detude-et-admissions&q=&facet=session&facet=cod_uai&facet=g_ea_lib_vx&facet=lib_dep&facet=acad_mies&facet=lib_reg&facet=fili&facet=form_lib_voe_acc&facet=fil_lib_voe_acc',
}
datasets = lib.loadResources(url_dict)

### Parcoursup ###
parcoursup_data = lib.getParcoursupData([datasets['etablissement_df_2016-2017'], datasets['etablissement_df_2018'], datasets['etablissement_df_2019']])
sessions = parcoursup_data["session"].unique()

map_data_sessions = lib.group_by_years(lib.getMapData(parcoursup_data.query("session == '2018' | session == '2019'")), ['2018','2019']) # Map (Nombre de voeux par établissements)
barGraph_data_sessions = lib.group_by_years(lib.getBarGraphData(parcoursup_data), sessions) # Graphe en barre (Nombre de voeux par filière)

#
### Figures
#

session_visible = 2018

# Map (Nombre de voeux par établissements)

map_fig = px.scatter_mapbox(
    map_data_sessions[f'{session_visible}'],
    lat="lat",
    lon="lon",
    hover_name="g_ea_lib_vx",
    hover_data=["acad_mies", "voe_tot"],
    color_discrete_sequence=["fuchsia"],
    zoom=4.5,
    height=500,
    size='voe_tot'
)
map_fig.update_layout(mapbox_style="open-street-map")
map_fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# Diagramme en barres (Nombre de voeux par filière)

bar_graph_fig = px.bar(
    barGraph_data_sessions[f'{session_visible}'],
    y='fil_lib_voe_acc',
    x='voe_tot',
    height=500,
    orientation='h'
)

#
### Main
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
                    html.Div(
                        children=[
                            dcc.Slider(
                                id="map-year-slider",
                                min=2018,
                                max=2019,
                                step=None,
                                marks={2018:'2018',2019:'2019'},
                                value=session_visible
                            ),
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
                    ),
                    html.Div(
                        children=[
                            dcc.Slider(
                                id="bargraph-year-slider",
                                min=2016,
                                max=2019,
                                step=None,
                                marks={2016:'2016',2018:'2018',2019:'2019'},
                                value=session_visible
                            ),
                            dcc.Graph(
                                id='bar_graph',
                                figure=bar_graph_fig
                            ),
                            html.P(
                                children="Taux d'insertion de chaque filière",
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
    ### CALLBACKS
    #

    # Modifie les figure 'map' et 'bar_graph' en fonction de la valeur du slider
    @app.callback(
        [Output(component_id='map', component_property='figure'),],
        [Input(component_id='map-year-slider', component_property='value')]
    )
    def update_graphs(input_value):
        map = px.scatter_mapbox(map_data_sessions[f'{input_value}'], lat="lat", lon="lon", hover_name="g_ea_lib_vx", hover_data=["acad_mies", "voe_tot"],
                        color_discrete_sequence=["fuchsia"], zoom=4.5, height=500, size='voe_tot')
        map.update_layout(mapbox_style="open-street-map")
        map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        return [map]
    
    @app.callback(
        [Output(component_id='bar_graph', component_property='figure')],
        [Input(component_id='bargraph-year-slider', component_property='value')]
    )
    def update_graphs(input_value):
        barGraph = px.bar(barGraph_data_sessions[f'{input_value}'], y='fil_lib_voe_acc', x='voe_tot', orientation='h')
        return [barGraph]

    #
    ### Lancement du serveur
    #

    app.run_server(debug=True)
