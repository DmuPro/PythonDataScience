# Projet de visualisation de données
Mini-Projet visant à fournir des représentations graphiques de données publiques selon un sujet choisi, le sujet de ce projet étant:

> Déterminer la filière la plus populaire en france et voir le lien de cette popularité avec le taux d'insertion

## Rapport d'analyse
/!\ Afin d'avoir des données sur le plus de formation possible nous avons récupéré différents open-datas, le programme est très ralenti dû à l'importante quantité de données à traiter.

Afin de répondre à notre problématique nous avons élaborer:
* Un graphique camembert et un graphique à barres représentant le nombre de voeux par filière
* Une carte qui représente les différents établissements sur la carte
* Un graphique à ligne représentant le taux d'insertion de chaque filière de 2014 à 2017
* Un histogramme représentant en détails l'évolution d'une filière

### Résultat des analyses:  
### Observation par rapport aux graphiques de popularité:
#### Top 5 des filières les plus populaires:
* Droit
* D E Infirmier
* PACES - Médecine,Pharmacie,Odontologie,Maieutique
* Sciences et Techniques des Activités Physiques et Sportives
* Techniques de commercialisation  
La plupart des filières populaires sont centrées en Île de france.

#### Interprétation des résultats sur les graphiques de popularités:  
Après la visualisation des données, il est évident que la filière la plus populaire est le droit. Cependant, les données que nous avons recupérées sont issues d'open-data de parcoursup ainsi nous ne prenons en compte que les inscriptions par parcoursup.

#### Observation par rapport aux graphiques d'insertion:
* La filière ayant le plus de taux d'insertion est l'enseignement en master
* La filière ayant le moins de taux d'insertion est la licence pro en histoire géo
* La filière informatique connaît une chute dans le taux d'insertion avant de remonter 2016-2017
* La filière précédemment déterminée comme la plus populaire possède un taux d'insertion moyen d'environ 90% rentrant dans la moyenne du taux d'insertion entre tous les établissements

    
    #### Interprétation des résultats sur les graphiques d'insertion:
    Il est important de noter que de nombreuses établissements ne renseignaient pas leur taux d'insertion, sur plus de 11k données récupérés, seul 141 données, soit un peu plus de 1% des données ont pu être récupérées.
    C'est pourquoi, il n'y a pas assez de données pour tirer de vrai conclusion sur le taux d'insertion.

    #### Conclusion:

    Pour faire la liaison entre la filière la plus populaire et son taux d'insertion, nous n'avons pas réussi à déterminer un lien entre le taux d'insertion et la popularité.
    En effet, bien que le droit possède un taux d'insertion assez élevé, d'autres filières possèdant un taux d'insertion que celui-ci tels que l'enseignement ou l'informatique ne figurent pas dans le podium des filières les plus populaires.  
    L'une des raisons pourquoi il était impossible d'établir un lien entre ses deux facteurs était la taille des données (141 insertion vs 6000+ paroursup).
    Nous aurions pu prendre d'autre facteur en compte tels que le salaire cependant cela n'a pas été possible en raison du fait que les données sur chaque diplome ont été récupérées sur des opendatas différentes. Bien qu'elles partagent tous des champs tels que le taux d'insertion, il y avait également des champs qui étaient renseignées dans certaines bases et pas d'autres ce qui rendaient l'extraction des données impossible.


## Guide utilisateur

**Dépendances (Versions de développement) :**
* Python 3.8.3
* Pandas 1.1.4
* Plotly 4.13.0
* Dash 1.17.0  

**Installation (Versions de développement) :**
* `pip install 'package==version'`
* `pip install pandas`
* `pip install plotly==4.13.0`
* `pip install dash==1.17.0`

**Exécution du projet:**
Afin de lancer le projet, il suffit d'exécuter le fichier main.py

## Guide développeur
Toutes les fonctions d'extractions de données, de formatage de données et de traitage de données sont présents sur le fichier lib.py
### Fichier main:

#### Initialisation des données:
- A partir des url dans le dictionnaire url_dict, les données sont chargées dans un dataset avec la fonction loadRessources.
- Ce dataset sera utilisé pour créer les deux principaux dataframes, parcoursup_data contenant toutes les données de parcoursup et apb ainsi que insertion_data contenant toutes les données sur l'insertion professionnelle de chaque diplôme.
- Afin de grouper les données par paramètres par sessions et par discipline, les filtres sont initialisés en utilisant la fonction panda unique() qui renvoie une liste d'éléments unique.

- Puis les données sont traités et groupées en utilisant leurs fonctions respectives group_by_discipline et group_by_years, qui groupe les éléments en coupant la dataframe. Cela renvoie un dictionnaire de dataframe ayant pour clé l'année de la session pour la session et le nom de discipline pour la discipline.

- Après avoir initialisé les données nécessaires à la visualisation, nous créons les figures:

    -Map:
    Prends en paramètre la dataframe de la session visible, le nom de chaque filière et le nombre total de voeux.

    -Diagramme en barres:
    Prends en paramètre la dataframe de la session visible, le nom de chaque filière dans l'axe y et le nombre total de voeux dans l'axe X.



    -Diagramme en ligne:
    Prends en paramètre la dataframe de la session visible, le nom du diplome ainsi que la discipline dans l'axe y et le nombre total de voeux dans l'axe X.
    Les données sont groupées par disciplines.

    -Diagramme circulaire:
    Avant de créer la figure, les données sont filtrés à l'aide de la fonction filterHighVal qui nous renvoie une dataframe possédant les 20 premières filières possédant le plus de voeux.
    Prends en paramètre la dataframe de la session visible, le nombre de voeux totals et le nom des formations.

    -Histogramme:
    Prends en paramètre la dataframe de la session visible, discipline active dans l'axe x et le taux d'insertion dans l'axe X.


    Main:
    -Mise en page du dashboard