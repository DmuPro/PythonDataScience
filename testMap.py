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

etablissement_df = readUrlJson("https://data.education.gouv.fr/api/records/1.0/search/?dataset=fr-esr-parcoursup&q=&sort=tri&facet=session&facet=contrat_etab&facet=cod_uai&facet=g_ea_lib_vx&facet=dep_lib&facet=region_etab_aff&facet=acad_mies&facet=fili&facet=form_lib_voe_acc&facet=regr_forma&facet=fil_lib_voe_acc&facet=detail_forma&facet=tri")
etablissement_df.to_csv(r'df_parcoursup.csv', index = False, header=True)
etablissement_df[['lat','lon']] = pd.DataFrame(etablissement_df.g_olocalisation_des_formations.tolist(), index= etablissement_df.index)
print(etablissement_df)

fig = px.scatter_mapbox(etablissement_df, lat="lat", lon="lon", hover_name="g_ea_lib_vx", hover_data=["acad_mies"],
                        color_discrete_sequence=["fuchsia"], zoom=3, height=300)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()