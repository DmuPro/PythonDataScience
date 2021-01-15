import plotly.express as px
import pandas as pd
import urllib.request
import json

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

def loadResources(url_dict):
    """Renvoie un dictionnaire de dataframe à partir des liens fournis en entrée

    Args:
        url_dict [Dict]: Clé= Donnée ciblée, Valeur= Url

    Returns:
        {key: Dataframe} [Dict]: Sets de données associés à un nom
    """
    return {key:readUrlJson(url) for key,url in url_dict.items()}

def getParcoursupData(etablissement_df_2018, etablissement_df_2019):
    """Renvoie une figure de type scatter_mapbox affichant le nombre de chaque formation
    
    Args:
        etablissement_df_2018 ([DataFrame]): [Données parcoursup des établissements en 2018]
        etablissement_df_2019 ([DataFrame]): [Données parcoursup des établissements en 2019]
    """
    etablissement_df = pd.concat([etablissement_df_2018, etablissement_df_2019])
    return etablissement_df

def group_by_years(df, year_list):
    return {session:df.query("session == @session") for session in year_list}

def getMapData(parcoursup_data):
    map_data = parcoursup_data.groupby(['g_ea_lib_vx','session']).aggregate({
        'voe_tot':'sum',
        'g_olocalisation_des_formations':'first',
        'session':'first',
        'g_ea_lib_vx':'first',
        'acad_mies':'first'
    })

    map_data[['lat','lon']] = pd.DataFrame(map_data.g_olocalisation_des_formations.tolist(), index= map_data.index)

    # On crée un dictionnaire séparant le dataframe par dates de session
    return map_data

def getBarGraphData(parcoursup_data):
    barGraph_data = parcoursup_data.groupby(['fil_lib_voe_acc','session']).aggregate({
        'voe_tot':'sum',
        'fil_lib_voe_acc':'first',
        'session':'first',
    })
    return barGraph_data