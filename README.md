# Projet de visualisation de données
Mini-Projet visant à fournir des représentations graphiques de données publiques selon un sujet choisi, le sujet de ce projet étant:

> Déterminer la filière la plus populaire en france et voir le lien de cette popularité avec le taux d'insertion  

Liens des sets de données utilisés:  
* [Voeux APB 2016/2017](https://data.education.gouv.fr/explore/dataset/apb-voeux-de-poursuite-detude-et-admissions/information/)
* [Voeux parcoursup 2018](https://data.education.gouv.fr/explore/dataset/fr-esr-parcoursup-2018/information/)
* [Voeux parcoursup 2019](https://data.education.gouv.fr/explore/dataset/fr-esr-parcoursup/information/)
* [Taux d'insertion des DUT](https://data.enseignementsup-recherche.gouv.fr/explore/dataset/fr-esr-insertion_professionnelle-dut_donnees_nationales/information/)
* [Taux d'insertion des Licence pro](https://data.enseignementsup-recherche.gouv.fr/explore/dataset/fr-esr-insertion_professionnelle-lp/information/)
* [Taux d'insertion des Masters](https://data.enseignementsup-recherche.gouv.fr/explore/dataset/fr-esr-insertion_professionnelle-master_donnees_nationales/information/)
* [Taux d'insertion des doctorats](https://data.enseignementsup-recherche.gouv.fr/explore/dataset/insertion-professionnelle-des-diplomes-de-doctorat-par-ensemble/information/)

## Rapport d'analyse
/!\ Afin d'avoir des données sur le plus de formation possible nous avons récupéré différents sets de donnée.

Afin de répondre à notre problématique nous avons élaboré:
* Un diagramme circulaire et un diagramme en barres représentant le nombre de voeux par filière
* Une carte qui représente les différents établissements sur la carte ainsi que leur nombre de voeux
* Un diagramme en lignes représentant le taux d'insertion de chaque filière de 2014 à 2017
* Un histogramme représentant en détails l'évolution du taux d'insertion d'une filière

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
* La filière ayant le meilleur de taux d'insertion est le master enseignement
* La filière ayant le moins bon de taux d'insertion est la licence pro en histoire géographie
* La filière informatique a connu une chute dans le taux d'insertion avant de remonter 2016-2017
* La filière Droit précédemment déterminée comme la plus populaire possède un taux d'insertion moyen d'environ 90% rentrant dans la moyenne du taux d'insertion entre toutes les formations


#### Interprétation des résultats sur les graphiques d'insertion:
Il est important de noter que de nombreux établissements ne renseignaient pas leur taux d'insertion, sur plus de 11k données récupérés, seul 141 données, soit un peu plus de 1% des données étaient renseignées.
C'est pourquoi, il n'y a pas assez de données pour tirer de vrai conclusion sur le taux d'insertion.

#### Conclusion:

Pour faire la liaison entre la filière la plus populaire et son taux d'insertion, nous n'avons pas réussi à déterminer un lien entre le taux d'insertion et la popularité.
En effet, bien que le droit possède un taux d'insertion assez élevé, d'autres filières possèdant un taux d'insertion supérieur à celui-ci tels que l'enseignement ou l'informatique ne figurent pas dans le podium des filières les plus populaires.  
L'une des raisons pour lesquelles il était impossible d'établir un lien entre ces deux facteurs était la taille des données (141 insertion vs 6000+ parcoursup).
Nous aurions pu prendre d'autre facteur en compte tels que le salaire cependant cela n'a pas été possible en raison du fait que les données sur chaque diplôme ont été récupérées sur des opendatas différentes. Bien qu'elles partagent tous des champs tels que le taux d'insertion, il y avait également des champs qui étaient renseignées dans certaines bases et pas d'autres ce qui rendaient la liaison des données impossible.


## Guide utilisateur

**Dépendances (Versions de développement) :**
* Python 3.8.3
* Pandas 1.1.4
* Plotly 4.13.0
* Dash 1.17.0  

**Installation (Versions de développement) :**
* `pip install pandas==1.1.4`
* `pip install plotly==4.13.0`
* `pip install dash==1.17.0`

**Exécution du projet :** `python main.py` ou `python3 main.py`  
**Url du dashboard :** `http://127.0.0.1:8050/`  
Le nombre de données à charger étant très grand, le chargement peut durer entre 30s et 5 minutes selon la rapidité du réseau.

## Guide développeur

### Fichier lib.py:

Contient toutes les fonctions utilitaires telles que l'extraction, le formatage, et le traitement des données.

### Fichier main.py:

#### Initialisation des données:
- A partir des url dans le dictionnaire url_dict, les dataframes sont chargés dans un dictionnaire avec la fonction loadResources.
- Ce dictionnaire sera utilisé pour créer les deux principaux dataframes, parcoursup_data contenant toutes les données de parcoursup et apb ainsi que insertion_data contenant toutes les données sur l'insertion professionnelle de chaque diplôme.
- Afin de séparer les affichages par sessions ou par discipline, des filtres sont initialisés en utilisant la fonction panda unique() qui renvoie une liste d'éléments unique.
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

* Programme principal (main):
    -Mise en page du dashboard  
    -Ajout de fonctions callback pour choisir l'année ou la filière à partir des sliders et menu déroulant