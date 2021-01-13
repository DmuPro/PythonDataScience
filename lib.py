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

def getMapData():
    """
    Renvoie une figure de type scatter_mapbox affichant le nombre de chaque formation
    """
    etablissement_df_2019 = readUrlJson("https://data.education.gouv.fr/api/records/1.0/search/?dataset=fr-esr-parcoursup&q=&sort=tri&facet=session&facet=contrat_etab&facet=cod_uai&facet=g_ea_lib_vx&facet=dep_lib&facet=region_etab_aff&facet=acad_mies&facet=fili&facet=form_lib_voe_acc&facet=regr_forma&facet=fil_lib_voe_acc&facet=detail_forma&facet=tri")
    etablissement_df_2018 = readUrlJson("https://data.education.gouv.fr/api/records/1.0/search/?dataset=fr-esr-parcoursup-2018&q=&sort=tri&facet=session&facet=contrat_etab&facet=cod_uai&facet=g_ea_lib_vx&facet=dep_lib&facet=region_etab_aff&facet=acad_mies&facet=fili&facet=form_lib_voe_acc&facet=regr_forma&facet=fil_lib_voe_acc&facet=detail_forma&facet=tri")
    etablissement_df = pd.concat([etablissement_df_2018, etablissement_df_2019])
    etablissement_df = etablissement_df.groupby(['g_ea_lib_vx','session']).aggregate({
        'voe_tot':'sum',
        'g_olocalisation_des_formations':'first',
        'session':'first',
        'g_ea_lib_vx':'first',
        'acad_mies':'first'
    }) ### Ajouter les attributs necessaires au fur et à mesure ###

    etablissement_df[['lat','lon']] = pd.DataFrame(etablissement_df.g_olocalisation_des_formations.tolist(), index= etablissement_df.index)
    return etablissement_df
