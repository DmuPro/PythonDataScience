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



def getParcoursSupData(*insertiondf):
    """
    Renvoie une dataframe contenant toutes les données de l'opendata de parcoursup
    """
    parcoursSup_df = pd.concat(insertiondf,ignore_index=True)
    return parcoursSup_df


if __name__ == "__main__":
    #voe_tot
    parcoursSup = (readUrlJson("https://data.education.gouv.fr/api/records/1.0/search/?dataset=fr-esr-parcoursup&q=&sort=tri&facet=session&facet=contrat_etab&facet=cod_uai&facet=g_ea_lib_vx&facet=dep_lib&facet=region_etab_aff&facet=acad_mies&facet=fili&facet=form_lib_voe_acc&facet=regr_forma&facet=fil_lib_voe_acc&facet=detail_forma&facet=tri"),
                   readUrlJson("https://data.education.gouv.fr/api/records/1.0/search/?dataset=fr-esr-parcoursup-2018&q=&sort=tri&facet=session&facet=cod_uai&facet=g_ea_lib_vx&facet=dep_lib&facet=region_etab_aff&facet=acad_mies&facet=fili&facet=form_lib_voe_acc&facet=regr_forma&facet=fil_lib_voe_acc&facet=detail_forma&facet=tri"),
                   readUrlJson("https://data.education.gouv.fr/api/records/1.0/search/?dataset=apb-voeux-de-poursuite-detude-et-admissions&q=&facet=session&facet=cod_uai&facet=g_ea_lib_vx&facet=lib_dep&facet=acad_mies&facet=lib_reg&facet=fili&facet=form_lib_voe_acc&facet=fil_lib_voe_acc"))
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
    dfV2 = df
    df = df.query("taux_dinsertion != 'ns' & emplois_stables != 'ns'")
    df = df.assign(taux_dinsertion=df['taux_dinsertion'].astype('float64'))
    df = df.assign(emplois_stables=df['emplois_stables'].astype('float64'))
    #Les années sont des strings ici, à ne pas comparer avec des int !


    df = df.groupby(['domaine','annee']).aggregate({
        'taux_dinsertion':'mean',
        'emplois_stables':'mean',
        'annee':'first',
        'diplome':'first',
        'domaine':'first'
    })
    
    domaines = df['domaine'].unique()
    domaines_df = [df.query(f"domaine=='{domaine}'") for domaine in domaines]

    traces = [go.Scatter(
        x = domaine['annee'],
        y = domaine['taux_dinsertion'],
        mode = 'markers',
        text = domaine['diplome'] + " " + domaine['domaine'],
        name = domaine['domaine'].iloc[0],
        marker = dict(
            size = [element/5 for element in domaine['taux_dinsertion']]
            )
        
    ) for domaine in domaines_df]

    traces_stable = go.Scatter(
        x = df['annee'],
        y = df['emplois_stables'],
        mode = 'markers',
        text = df['diplome'] + " " + df['domaine']
        
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
    
    fig = go.Figure(data = data,layout = layout)
    fig.show()
    fig = px.pie(parcoursSup_df, values='voe_tot', names='fil_lib_voe_acc', title='Insertion par domaine')
    fig.show()
    plotly.offline.plot(fig, filename='fig.html', auto_open=True, include_plotlyjs='cdn')
    
    """
    Histogramme
    Lien de la documentation: https://plotly.com/python/histograms/
    """
    #Génère des données aléatoires
    licence_df = px.data.tips()
    # otherdata = df.query("discipline == 'Informatique'")
    # print(otherdata)
    df_histogram = dfV2.loc[dfV2['domaine'] == "Droit, économie et gestion"]
    df_histogram.to_csv (r'a.csv', index = False, header=True)
    print(df)
    fig = px.histogram(df_histogram, x="annee",y="taux_dinsertion",histfunc = "avg",labels=dict(x='Annee', y='Insertion'),color = "diplome")
    fig.update_layout(
        title="Evolution du taux d'insertion",
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
    print(fig)
    plotly.offline.plot(fig, filename='historigram.html', auto_open=True, include_plotlyjs='cdn')