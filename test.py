import pandas as pd
import plotly.graph_objs as go
import plotly
import math
import json
import urllib.request
import plotly.express as px
from urllib.request import urlopen
from plotly.subplots import make_subplots
import plotly.io as pio

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
    #voe_tot
    parcoursSup = [readUrlJson("https://data.education.gouv.fr/api/records/1.0/search/?dataset=fr-esr-parcoursup&q=&sort=tri&facet=session&facet=contrat_etab&facet=cod_uai&facet=g_ea_lib_vx&facet=dep_lib&facet=region_etab_aff&facet=acad_mies&facet=fili&facet=form_lib_voe_acc&facet=regr_forma&facet=fil_lib_voe_acc&facet=detail_forma&facet=tri"),
                   readUrlJson("https://data.education.gouv.fr/api/records/1.0/search/?dataset=fr-esr-parcoursup-2018&q=&sort=tri&facet=session&facet=cod_uai&facet=g_ea_lib_vx&facet=dep_lib&facet=region_etab_aff&facet=acad_mies&facet=fili&facet=form_lib_voe_acc&facet=regr_forma&facet=fil_lib_voe_acc&facet=detail_forma&facet=tri"),
                   readUrlJson("https://data.education.gouv.fr/api/records/1.0/search/?dataset=apb-voeux-de-poursuite-detude-et-admissions&q=&facet=session&facet=cod_uai&facet=g_ea_lib_vx&facet=lib_dep&facet=acad_mies&facet=lib_reg&facet=fili&facet=form_lib_voe_acc&facet=fil_lib_voe_acc")]
    parcoursSup_df = pd.concat(parcoursSup,ignore_index=True)
    parcoursSup_df.to_csv (r'export_parcoursSUp.csv', index = False, header=True)
    allInsertProfesionnelURL = [readUrlJson("https://data.enseignementsup-recherche.gouv.fr/api/records/1.0/search/?dataset=fr-esr-insertion_professionnelle-lp&q=&rows=10&facet=annee&facet=diplome&facet=numero_de_l_etablissement&facet=etablissement&facet=academie&facet=domaine&facet=code_de_la_discipline&facet=discipline&facet=situation&facet=cle_etab&facet=cle_disc&facet=id_paysage"),
                                readUrlJson("https://data.enseignementsup-recherche.gouv.fr/api/records/1.0/search/?dataset=insertion-professionnelle-des-diplomes-de-doctorat-par-ensemble&q=&rows=10&sort=-annee&facet=annee&facet=situation&facet=disca"),
                                readUrlJson("https://data.enseignementsup-recherche.gouv.fr/api/records/1.0/search/?dataset=fr-esr-insertion_professionnelle-dut_donnees_nationales&q=&rows=10&facet=annee&facet=diplome&facet=situation&facet=genre&facet=disciplines&facet=secteur_disciplinaire&facet=cle_disc"),
                                readUrlJson("https://data.enseignementsup-recherche.gouv.fr/api/records/1.0/search/?dataset=fr-esr-insertion_professionnelle-master_donnees_nationales&q=&rows=22&facet=annee&facet=diplome&facet=situation&facet=genre&facet=disciplines&facet=cle_disc")
                                ]

    df = pd.concat(allInsertProfesionnelURL,ignore_index=True)
    
    df['taux_dinsertion'].fillna(df['taux_d_insertion'],inplace=True)
    df['taux_dinsertion'].fillna(df['taux_insertion'],inplace=True)
    df.to_csv (r'export_dataframe.csv', index = False, header=True)
    #Les années sont des strings ici, à ne pas comparer avec des int !

    print(df)


   
    
    traces = go.Scatter(
        x = df['domaine'],
        y = df['annee'],
        mode = 'markers',
        text = df['diplome'] + " " + df['domaine'],
        marker = dict(
            size = 0 if df['taux_dinsertion'] is not int else df['taux_dinsertion']
        ),
    )
    traces_popularite = go.Scatter(
        x = parcoursSup_df['session'],
        y = parcoursSup_df['voe_tot'],
        mode = 'markers',
        text = parcoursSup_df['fil_lib_voe_acc'] + " " + parcoursSup_df['form_lib_voe_acc'],
        marker = dict(
            size = [math.log(int(elem))*10 for elem in parcoursSup_df['voe_tot']]
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
    fig.add_trace(traces_popularite,
                            row=1, col=2)


    #fig = px.pie(parcoursSup_df, values='voe_tot', names='fil_lib_voe_acc', title='Insertion par domaine')
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
    fig = px.histogram(df, x="annee",y="taux_dinsertion", histfunc='avg')
    plotly.offline.plot(fig, filename='historigram.html', auto_open=True, include_plotlyjs='cdn')
    
    data = [dict(
        type = 'scatter',
        x = df['domaine'],
        y = df['annee'],
        mode = 'markers',
        transforms = [dict(
            type = 'aggregate',
            groups = df['domaine'],
            aggregations = [dict(
                target = 'y', func = 'avg', enabled = True),
                ]
            )]
    )]
    layout = dict(
        title = '<b>Gapminder</b><br>2007 Average GDP Per Cap & Life Exp. by Continent',
        yaxis = dict(
            type = 'log'
        )
    )

    fig_dict = dict(data=data, layout=layout)
    pio.show(fig_dict, validate=False)