import pandas as pd
import plotly.graph_objs as go
import plotly
import math
import json
import urllib.request
import plotly.express as px

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
              "licencePro":"https://data.enseignementsup-recherche.gouv.fr/api/records/1.0/search/?dataset=fr-esr-insertion_professionnelle-lp&q=&rows=700&facet=annee&facet=diplome&facet=numero_de_l_etablissement&facet=etablissement&facet=academie&facet=domaine&facet=code_de_la_discipline&facet=discipline&facet=situation&facet=cle_etab&facet=cle_disc&facet=id_paysage",
              "doctorat":"https://data.enseignementsup-recherche.gouv.fr/api/records/1.0/search/?dataset=insertion-professionnelle-des-diplomes-de-doctorat-par-ensemble&q=&rows=424&sort=-annee&facet=annee&facet=situation&facet=disca",
              "DUT":"https://data.enseignementsup-recherche.gouv.fr/api/records/1.0/search/?dataset=fr-esr-insertion_professionnelle-dut_donnees_nationales&q=&rows=913&facet=annee&facet=diplome&facet=situation&facet=genre&facet=disciplines&facet=secteur_disciplinaire&facet=cle_disc"}
    df = readUrlJson(allInsertProfesionnelURL['licencePro'])
    df.to_csv (r'export_dataframe.csv', index = False, header=True)
    traces = go.Scatter(
        x = df['annee'],
        y = df['taux_dinsertion'],
        mode = 'markers',
        text = df['diplome'] + " " + df['domaine']
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


    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename='fig.html', auto_open=True, include_plotlyjs='cdn')
    
    """
    Histogramme
    Lien de la documentation: https://plotly.com/python/histograms/
    """
    #Génère des données aléatoires
    df = px.data.tips()
    fig = px.histogram(df, x="total_bill", nbins=20)
    plotly.offline.plot(fig, filename='historigram.html', auto_open=True, include_plotlyjs='cdn')


