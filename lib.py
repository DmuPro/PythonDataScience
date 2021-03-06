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

def getParcoursupData(etablissements_df):
    """Renvoie une figure de type scatter_mapbox affichant le nombre de chaque formation
    
    Args:
        etablissement_df_2018 ([DataFrame]): [Données parcoursup des établissements en 2018]
        etablissement_df_2019 ([DataFrame]): [Données parcoursup des établissements en 2019]
    """
    etablissement_df = pd.concat(etablissements_df)
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
    map_data = map_data.dropna()
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

def getInsertionData(insertion_data):
    """Renvoie une figure de type scatter_mapbox affichant le nombre de chaque formation
    
    Args:
        insertion_data ([DataFrame]) : [Données des taux d'insertion des masters, licences pros, DUT et doctorats]
    """
    insertion_data = pd.concat(insertion_data)
    #On remplit les colonnes vides par leurs valeurs correspondantes
    insertion_data['taux_dinsertion'].fillna(insertion_data['taux_d_insertion'],inplace=True)
    insertion_data['taux_dinsertion'].fillna(insertion_data['taux_insertion'],inplace=True)
    #On filtre les données pour enlevé les taux d'insertion non renseigné et non déterminé
    insertion_data = insertion_data.query("taux_dinsertion != 'ns' & taux_dinsertion != 'nd'")
    insertion_data = insertion_data.assign(taux_dinsertion=insertion_data['taux_dinsertion'].astype('float64'))

    return insertion_data

def getDisciplineData(insertion_data):
    discipline_data = insertion_data.groupby(['discipline','annee']).aggregate({
        'taux_dinsertion':'mean',
        'annee':'first',
        'diplome':'first',
        'domaine':'first',
        'discipline':'first'
    })
    return discipline_data

def group_by_discipline(insertion_data,disciplines):
    """[summary]
    Args:
        insertion_data ([Dataframe de l'insertion]): [Données des taux d'insertions des ]
        disciplines ([type]): [description]
    Returns:
        [Dictionnaire]: [Dictionnaire de dataframe : clé = discipline, valeur = dataframe de la discipline]
    """
    return [insertion_data.query(f'discipline=="{discipline}"') for discipline in disciplines]


def filterHighVal(parcoursupData):
    """[summary]
    Args:
        parcoursupData ([Dictionnaire de dataframe]): [Dictionnaire contenant les dataframes des différentes disciplines]
    Returns:
        [DataFrame]: [Renvoie une dataframe contenant les vingts premières disicplines contenant le plus de voeux]
    """
    parcourSupDataFormat = pd.concat(parcoursupData).query("voe_tot != 'inconnu'")
    parcourSupDataFormat = parcourSupDataFormat.assign(voe_tot=parcourSupDataFormat['voe_tot'].astype('int64'))
    data = parcourSupDataFormat.groupby(['fil_lib_voe_acc']).aggregate({
        'fil_lib_voe_acc':'first',
        'voe_tot':'sum'
    })
    return data.sort_values('voe_tot',ascending=False).head(20)