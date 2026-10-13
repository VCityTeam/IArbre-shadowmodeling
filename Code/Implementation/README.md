# Comment lancer le [programme](https://github.com/VCityTeam/VCity/blob/master/Projects/IArbre/Stage-Shadow_Modeling/Implementation/Algo_intervisibility_bvh_classification_user_choice.py) : (Windows)

- Installer [Pycharm](https://www.jetbrains.com/pycharm/download/?section=windows).
- Crée un projet.
- Installer [Python](https://www.python.org/downloads/release/python-3110/) (J'ai utilisé Python 3.11 pour tester certaines librairies qui n'étaient disponibles que sur cette version).
- Installer un environnement Anaconda (Pour la librairie [PDAL](https://www.lizardtech.com/post/step-by-step-pdal-python-workflow-for-lidar-data-processing)).

<img width="600" height="400" alt="image" src="https://github.com/user-attachments/assets/8bcb9559-888a-4321-bd5d-c503c50458e9" />

- Copier-coller [le programme](https://github.com/VCityTeam/VCity/blob/master/Projects/IArbre/Stage-Shadow_Modeling/Implementation/Algo_intervisibility_bvh_classification_user_choice.py) dans le dossier.
- Copier-coller un [fichier LAZ](https://data.grandlyon.com/portail/fr/jeux-de-donnees/nuage-de-points-lidar-2023-de-la-metropole-de-lyon/donnees) dans le même dossier que le programme.

Par example :

<img width="520" height="113" alt="image" src="https://github.com/user-attachments/assets/b0dd6c7b-eb69-454d-baf3-03d38ab7ea13" />

- Changer dans le code le nom du fichier LAZ.

<img width="513" height="30" alt="image" src="https://github.com/user-attachments/assets/b495e691-6dae-4026-85ff-b96975c818b2" />

- Installer les **librairies** demandées.
- **Run** le programme.
- Entrer la classification souhaitée.
- Entrer la date souhaitée.
- Attendre.
- Entrer la phase de la journée souhaitée.
- Attendre le résultat.

<br>
<br>
<br>

# Comment lancer le [programme](https://github.com/VCityTeam/VCity/blob/master/Projects/IArbre/Stage-Shadow_Modeling/Implementation/Shadow_Modeling_BVH_Intervisibility_Classification_LYON_API_LAZ.py) : (Windows)

- Installer [Pycharm](https://www.jetbrains.com/pycharm/download/?section=windows).
- Crée un projet.
- Installer [Python](https://www.python.org/downloads/release/python-3110/) (J'ai utilisé Python 3.11 pour tester certaines librairies qui n'étaient disponibles que sur cette version).
- Installer un environnement Anaconda (Pour la librairie [PDAL](https://www.lizardtech.com/post/step-by-step-pdal-python-workflow-for-lidar-data-processing)).

<img width="600" height="400" alt="image" src="https://github.com/user-attachments/assets/8bcb9559-888a-4321-bd5d-c503c50458e9" />

- Copier-coller [le programme](https://github.com/VCityTeam/VCity/blob/master/Projects/IArbre/Stage-Shadow_Modeling/Implementation/Shadow_Modeling_BVH_Intervisibility_Classification_LYON_API_LAZ.py) dans le dossier.
- **Run**  le programme.
- Entrer la classification souhaitée.
- Entrer la date souhaitée.
- Entrer [**x_min** et **x_max**](https://data.grandlyon.com/portail/fr/jeux-de-donnees/nuage-de-points-lidar-2023-de-la-metropole-de-lyon/donnees) de la zone LiDAR souhaitée. *(le fichier laz correspondant est téléchargé dans le chemin chemin_du_projet/Data.)*
- Attendre.
- Entrer la phase de la journée souhaitée.
- Attendre le résultat.

<br>
<br>
<br>

# Comment lancer les programmes [SM1](https://github.com/VCityTeam/VCity/blob/master/Projects/IArbre/Stage-Shadow_Modeling/Implementation/Method1.py) et [SM2](https://github.com/VCityTeam/VCity/blob/master/Projects/IArbre/Stage-Shadow_Modeling/Implementation/Method2.py) : (Windows)

- Installer [Pycharm](https://www.jetbrains.com/pycharm/download/?section=windows).
- Crée un projet.
- Installer [Python](https://www.python.org/downloads/release/python-3110/) (J'ai utilisé Python 3.11 pour tester certaines librairies qui n'étaient disponibles que sur cette version).
- Installer un environnement Anaconda (Pour la librairie [PDAL](https://www.lizardtech.com/post/step-by-step-pdal-python-workflow-for-lidar-data-processing)).

<img width="600" height="400" alt="image" src="https://github.com/user-attachments/assets/8bcb9559-888a-4321-bd5d-c503c50458e9" />

- Copier-coller le programme dans le dossier.
- **Run**  le programme.
- Entrer la classification souhaitée.
- Entrer la date souhaitée. (ex : jour : 24 ; mois : 7 ; année : 2023)
- Entrer [**x_min** et **x_max**](https://data.grandlyon.com/portail/fr/jeux-de-donnees/nuage-de-points-lidar-2023-de-la-metropole-de-lyon/donnees) de la zone LiDAR souhaitée. (ex: x_min : 1848000 ; y_min : 5180000) *(le fichier laz correspondant est téléchargé dans le chemin chemin_du_projet/Data.)*
- Attendre.
- Entrer la phase de la journée souhaitée (ex : 1).
- Attendre le résultat. (Pour SM2, 3 ghraphes s'affichent à la suite, le premier représente la carte d'ombre hors végétation ; la seconde représente la carte d'ombre végétation ; la troisième représente la carte d'ombres globale).
