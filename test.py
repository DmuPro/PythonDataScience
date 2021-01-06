import pandas as pd
import plotly.graph_objs as go
import plotly
import math
import json
import urllib.request
import plotly.express as px
from urllib.request import urlopen
from plotly.subplots import make_subplots

def readUrlJson(url):
    """Renvoie un dataframe à partir d'une URL renvoyant un JSON

    Args:
        url ([string]): [string de l'url]
    """
    url = urllib.request.urlopen(url)
    data = url.read()
    jsonData = json.loads(data)
    jsonDataPrecise = [x['fields'] for x in jsonData['records']]
    return  pd.DataFrame(jsonDataPrecise)






if __name__ == "__main__":
    #Toutes les URLS des insertions professionnelles
    allInsertProfesionnelURL = {"master":"https://data.enseignementsup-recherche.gouv.fr/api/records/1.0/search/?dataset=fr-esr-insertion_professionnelle-master_donnees_nationales&q=&rows=22&facet=annee&facet=diplome&facet=situation&facet=genre&facet=disciplines&facet=cle_disc",
              "licencePro":"https://data.enseignementsup-recherche.gouv.fr/api/records/1.0/search/?dataset=fr-esr-insertion_professionnelle-lp&q=&rows=10&facet=annee&facet=diplome&facet=numero_de_l_etablissement&facet=etablissement&facet=academie&facet=domaine&facet=code_de_la_discipline&facet=discipline&facet=situation&facet=cle_etab&facet=cle_disc&facet=id_paysage",
              "doctorat":"https://data.enseignementsup-recherche.gouv.fr/api/records/1.0/search/?dataset=insertion-professionnelle-des-diplomes-de-doctorat-par-ensemble&q=&rows=10&sort=-annee&facet=annee&facet=situation&facet=disca",
              "DUT":"https://data.enseignementsup-recherche.gouv.fr/api/records/1.0/search/?dataset=fr-esr-insertion_professionnelle-dut_donnees_nationales&q=&rows=10&facet=annee&facet=diplome&facet=situation&facet=genre&facet=disciplines&facet=secteur_disciplinaire&facet=cle_disc"}
    licence_df = readUrlJson(allInsertProfesionnelURL['licencePro'])
    doctorat_df = readUrlJson(allInsertProfesionnelURL['doctorat'])
    DUT_df = readUrlJson(allInsertProfesionnelURL['DUT'])
    master_df = readUrlJson(allInsertProfesionnelURL['master'])

    frames = [licence_df,doctorat_df,DUT_df]

    df = pd.concat(frames,ignore_index=True)
    
    df['taux_dinsertion'].fillna(df['taux_d_insertion'],inplace=True)
    df['taux_dinsertion'].fillna(df['taux_insertion'],inplace=True)
    print(df)
    df.to_csv (r'export_dataframe.csv', index = False, header=True)
    #Les années sont des strings ici, à ne pas comparer avec des int !

    print(df['taux_dinsertion'])
    
    traces = go.Scatter(
        x = df['annee'],
        y = df['taux_dinsertion'],
        mode = 'markers',
        text = df['diplome'] + " " + licence_df['domaine'],
        marker = dict(
            size = 0 if df['taux_dinsertion'] is not int else df['taux_dinsertion']
        )
    )

    
    data = traces
    layout = go.Layout(title="Taux_insertion/Annee",
                        xaxis=dict(
                            title='insertion',
                            ticklen=5,
                            zeroline=False,
                            gridwidth=2,
                        ),
                        yaxis=dict(
                            title='annee',
                            ticklen=5,
                            zeroline=False,
                            gridwidth=2,
                        ))

    fig = make_subplots(rows=1, cols=2)
    fig.add_trace(data,
                            row=1, col=1)
    fig.add_trace(data,
                            row=1, col=2)


    plotly.offline.plot(fig, filename='fig.html', auto_open=True, include_plotlyjs='cdn')
    
    """
    Histogramme
    Lien de la documentation: https://plotly.com/python/histograms/
    """
    #Génère des données aléatoires
    licence_df = px.data.tips()
    print(licence_df)
    print(data)
    # otherdata = df.query("discipline == 'Informatique'")
    # print(otherdata)
    fig = px.histogram(df, x="annee",y="taux_dinsertion", nbins=20)
    plotly.offline.plot(fig, filename='historigram.html', auto_open=True, include_plotlyjs='cdn')


    
    
    #Génère la carte 
    """
    Lien de la documentation https://plotly.com/python/choropleth-maps/ 
    """
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)

    df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",dtype={"fips": str})
    subfig = px.choropleth(df, geojson=counties, locations='fips', color='unemp',
                           color_continuous_scale="Viridis",
                           range_color=(0, 12),
                           scope="usa",
                           labels={'unemp':'unemployment rate'}
    )
    plotly.offline.plot(fig, filename='grandefigure.html', auto_open=True, include_plotlyjs='cdn')