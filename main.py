import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

import lib

#
### Données
#

url_dict = {
    'etablissement_df_2018':'https://data.education.gouv.fr/api/records/1.0/search/?dataset=fr-esr-parcoursup-2018&q=&sort=tri&facet=session&facet=contrat_etab&facet=cod_uai&facet=g_ea_lib_vx&facet=dep_lib&facet=region_etab_aff&facet=acad_mies&facet=fili&facet=form_lib_voe_acc&facet=regr_forma&facet=fil_lib_voe_acc&facet=detail_forma&facet=tri&rows=-1',
    'etablissement_df_2019':'https://data.education.gouv.fr/api/records/1.0/search/?dataset=fr-esr-parcoursup&q=&sort=tri&facet=session&facet=contrat_etab&facet=cod_uai&facet=g_ea_lib_vx&facet=dep_lib&facet=region_etab_aff&facet=acad_mies&facet=fili&facet=form_lib_voe_acc&facet=regr_forma&facet=fil_lib_voe_acc&facet=detail_forma&facet=tri&rows=-1',
    'etablissement_df_2016-2017': 'https://data.education.gouv.fr/api/records/1.0/search/?dataset=apb-voeux-de-poursuite-detude-et-admissions&q=&facet=session&facet=cod_uai&facet=g_ea_lib_vx&facet=lib_dep&facet=acad_mies&facet=lib_reg&facet=fili&facet=form_lib_voe_acc&facet=fil_lib_voe_acc&rows=-1',
    'insertionMaster': 'https://data.enseignementsup-recherche.gouv.fr/api/records/1.0/search/?dataset=fr-esr-insertion_professionnelle-master_donnees_nationales&q=&facet=annee&facet=diplome&facet=situation&facet=genre&facet=disciplines&facet=cle_disc&rows=-1',
    'insertionDoctorat':'https://data.enseignementsup-recherche.gouv.fr/api/records/1.0/search/?dataset=insertion-professionnelle-des-diplomes-de-doctorat-par-ensemble&q=&sort=-annee&facet=annee&facet=situation&facet=disca&rows=-1',
    'insertionDUT':'https://data.enseignementsup-recherche.gouv.fr/api/records/1.0/search/?dataset=fr-esr-insertion_professionnelle-dut_donnees_nationales&q=&facet=annee&facet=diplome&facet=situation&facet=genre&facet=disciplines&facet=secteur_disciplinaire&facet=cle_disc&rows=-1',
    'insertionLicencePro':'https://data.enseignementsup-recherche.gouv.fr/api/records/1.0/search/?dataset=fr-esr-insertion_professionnelle-lp&q=&facet=annee&facet=diplome&facet=numero_de_l_etablissement&facet=etablissement&facet=academie&facet=domaine&facet=code_de_la_discipline&facet=discipline&facet=situation&facet=cle_etab&facet=cle_disc&facet=id_paysage&rows=-1'
}

datasets = lib.loadResources(url_dict)

### Parcoursup ###
parcoursup_data = lib.getParcoursupData([datasets['etablissement_df_2016-2017'], datasets['etablissement_df_2018'], datasets['etablissement_df_2019']])
parcoursup_data = parcoursup_data.query("fil_lib_voe_acc != 'bac S'")
parcoursup_data = parcoursup_data.query("fil_lib_voe_acc != 'D.E Infirmier'")

sessions = parcoursup_data["session"].unique()

map_data_sessions = lib.group_by_years(lib.getMapData(parcoursup_data.query("session == '2018' | session == '2019'")), ['2018','2019']) # Map (Nombre de voeux par établissements)
barGraph_data_sessions = lib.group_by_years(parcoursup_data, sessions) # Graphe en barre (Nombre de voeux par filière)

## Données d'insertion ##
insertion_data = lib.getInsertionData([datasets['insertionMaster'],datasets['insertionDUT'],datasets['insertionLicencePro'],datasets['insertionDoctorat']])
insertion_data = insertion_data.dropna(subset=['discipline'])
filieres = insertion_data["discipline"].unique()
filieres = [{'label':val, 'value':val} for val in filieres]

line_data = lib.getDisciplineData(insertion_data)
disciplines = line_data['discipline'].unique()
lineGraph_data = lib.group_by_discipline(line_data,disciplines)

#
### Figures
#

session_visible = 2018
discipline_active = "Droit"
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
    height=1000,
    orientation='h'
)

# Diagramme en ligne (Evolution du taux d'insertion de chaque discipline)
traces = [go.Scatter(
    x = discipline['annee'],
    y = discipline['taux_dinsertion'],
    mode = 'lines',
    text = discipline['diplome'] + " " + discipline['discipline'],
    name = discipline['discipline'].iloc[0],
) for discipline in lineGraph_data]

data = traces
layout = go.Layout(title="Taux_insertion/Annee",
                    xaxis=dict(
                        title='annee',
                        ticklen=5,
                        zeroline=False,
                        gridwidth=2,
                    ),
                    yaxis=dict(
                        title='insertion',
                        ticklen=5,
                        zeroline=False,
                        gridwidth=2,
                    ))

lineGraph = go.Figure(data = data,layout = layout)

#Diagramme camembert (Représentation du nombre de voeux par formation pour déterminer sa popularité)
pieChart_data = lib.filterHighVal(barGraph_data_sessions,session_visible)
pieChart = px.pie(pieChart_data,
            values='voe_tot', 
            names='fil_lib_voe_acc', 
            title='Insertion par domaine'
            )

#Histogramme représentant l'évolution du taux d'insertion d'une discipline
histogram = px.histogram(insertion_data.loc[insertion_data['discipline'] == discipline_active], x="annee",y="taux_dinsertion",histfunc = "avg")
histogram.update_layout(
    title="Evolution du taux d'insertion de la discipline suivante : "+discipline_active,
    xaxis = dict(
    title = "Annee",
    tick0 = 2010,
    dtick = 1
    ),
    yaxis = dict(
    title = "Taux d'insertion"
    ),
    font = dict(
        size = 18
    )
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
                                    href="#bar_graph",
                                    children="Diagramme en barre"
                                )
                            ]),
                            html.Li([
                                html.A(
                                    href="#pie-chart",
                                    children="Diagramme circulaire"
                                )
                            ]),
                            html.Li([
                                html.A(
                                    href="#line-graph",
                                    children="Diagramme en ligne"
                                )
                            ]),
                            html.Li([
                                html.A(
                                    href="#histogram",
                                    children="Histogramme"
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
                    # Carte
                    html.Div(
                        children=[
                            html.H2(
                                children="Carte du nombre de voeux par établissements"
                            ),
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
                        ],
                        style={'margin': '10px 40px 10px 40px'}
                    ),
                    # Diagramme en barre
                    html.Div(
                        children=[
                            html.H2(
                                children="Diagramme en barre du nombre de voeux total par filière"
                            ),
                            dcc.Slider(
                                id="bargraph-year-slider",
                                min=2016,
                                max=2019,
                                step=None,
                                marks={2016:'2016',2017:'2017',2018:'2018',2019:'2019'},
                                value=session_visible
                            ),
                            dcc.Graph(
                                id='bar_graph',
                                figure=bar_graph_fig
                            )
                        ],
                        style={'margin': '10px 40px 10px 40px'}
                    ),
                    # Diagramme circulaire (Camembert)
                    html.Div(
                        children=[
                            html.H2(
                                children="Diagramme circulaire de la filière la plus demandée"
                            ),
                            dcc.Graph(
                                id='pie-chart',
                                figure=pieChart
                            )
                        ],
                        style={'margin': '10px 40px 10px 40px'}
                    ),
                    # Graphe en ligne
                    html.Div(
                        children=[
                            html.H2(
                                children="Statistiques du taux d'insertion par année par filière"
                            ),
                            dcc.Graph(
                                id='line-graph',
                                figure=lineGraph
                            )
                        ],
                        style={'margin': '10px 40px 10px 40px'}
                    ),
                    # Histogramme
                    html.Div(
                        children=[
                            html.H2(
                                children="Histogrammes du taux d'insertion par filière"
                            ),
                            dcc.Dropdown(
                                id="histogram-dropdown",
                                options=filieres,
                                value='Droit'
                            ),
                            dcc.Graph(
                                id='histogram',
                                figure=histogram
                            )
                        ],
                        style={'margin': '10px 40px 10px 40px'}
                    )
                ],
                style={'width': '100%'}
            )
        ],
        style={'display': 'flex'}
    )

    #
    ### CALLBACKS
    #

    # Modifie la figure 'map' en fonction de la valeur du slider
    @app.callback(
        [Output(component_id='map', component_property='figure'),],
        [Input(component_id='map-year-slider', component_property='value')]
    )
    def update_map(input_value):
        map = px.scatter_mapbox(map_data_sessions[f'{input_value}'], lat="lat", lon="lon", hover_name="g_ea_lib_vx", hover_data=["acad_mies", "voe_tot"],
                        color_discrete_sequence=["fuchsia"], zoom=4.5, height=500, size='voe_tot')
        map.update_layout(mapbox_style="open-street-map")
        map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        return [map]
    
    # Modifie la figure 'bar_graph' en fonction de la valeur du slider
    @app.callback(
        [Output(component_id='bar_graph', component_property='figure')],
        [Input(component_id='bargraph-year-slider', component_property='value')]
    )
    def update_bargraph(input_value):
        barGraph = px.bar(barGraph_data_sessions[f'{input_value}'], y='fil_lib_voe_acc', x='voe_tot', orientation='h')
        return [barGraph]

    # Modifie la figure 'histogram' en fonction de la valeur du menu déroulant
    @app.callback(
        Output(component_id='histogram', component_property='figure'),
        [Input(component_id='histogram-dropdown', component_property='value')]
    )
    def update_histogram(input_value):
        histogram = px.histogram(insertion_data.loc[insertion_data['discipline'] == input_value], x="annee",y="taux_dinsertion",histfunc = "avg")
        histogram.update_layout(
            title="Evolution du taux d'insertion de la discipline suivante : "+input_value,
            xaxis = dict(
                title = "Annee",
                tick0 = 2010,
                dtick = 1
            ),
            yaxis = dict(
                title = "Taux d'insertion"
            ),
            font = dict(
                size = 18
            )
        )
        return histogram

    #
    ### Lancement du serveur
    #

    app.run_server(debug=True)
