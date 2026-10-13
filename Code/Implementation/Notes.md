## Liens Utilisé:
- [LAZ to LAS](https://github.com/LummiGIS/LAS_tools/blob/main/LAZ_to_LAS.py) : Don't work well.
- [A Quick Guide to Visualizing LiDAR Point Clouds in Python](https://medium.com/@BlanchR2/visualize-your-city-in-3d-a-quick-guide-to-lidar-point-clouds-in-python-00ae3cb2741b) : Work well (3D plot).
- [LiDAR Data .copc.laz](https://cartes.gouv.fr/telechargement/IGNF_NUAGES-DE-POINTS-LIDAR-HD).
- [LiDAR Point Cloud Vectorization: 3D Python Tutorial](https://www.youtube.com/watch?v=7SPLEDyCrmw).
- [IGNMap 3D/2D Viewer](https://github.com/IGNF/IGNMap/releases?page=1) : good for 3D.
- [LiDAR Point LAZ File Metropole Lyon](https://data.grandlyon.com/portail/fr/jeux-de-donnees/nuage-de-points-lidar-2023-de-la-metropole-de-lyon/donnees).
- [Numbering rectangles in 2D space to satisfy monotonicity](https://stackoverflow.com/questions/65349380/numbering-rectangles-in-2d-space-to-satisfy-monotonicity).
- [Algo Bounding Volume Hierarchies](https://pbr-book.org/3ed-2018/Primitives_and_Intersection_Acceleration/Bounding_Volume_Hierarchies).

<br>

## Notes :
- La végétation "**haute**" ne comprends que la partie "**haute**" de l'arbre :
<p align="center"><img width="283" height="131" alt="image" src="https://github.com/user-attachments/assets/e95ba22b-bd15-432f-ad13-f673cde9b965" /></p>
<br>
<br>

- Une zone avec **tout** les points [3D] :

<br>
<p align="center"><img width="500" height="400" alt="fig_all" src="https://github.com/user-attachments/assets/e186d2d6-f521-45ce-993d-2be004abf243" /></p>

<br>
<br>

- Une zone **(sans eau ni sol)** [3D] :
<br>

<p align="center"><img width="500" height="400" alt="fig_all_sauf_sol_eau" src="https://github.com/user-attachments/assets/659068db-910f-49be-9535-519783b7d90f" /></p>

<br>
<br>

- Combien de point par **m²** ?

<br>

### Classe :
- [1] **Non classé**, correspondant aux éléments du sur-sol non-identifiés.
- [2] **Sol**.
- [3] Végétation **faible**, correspondant à la végétation basse < 1,5 m.
- [4] Végétation **moyenne**, correspondant à la végétation moyenne de 1,5-5 m.
- [5] Végétation **forte**, correspondant à la végétation haute 5-15 m.
- [6] **Bâtiment**.
- [8] Réservé, correspondant à la **végétation haute** > 15 m.
- [9] **Eau**.

<br>

### Point de vue :
- **Vue d'en haut (XY) [2-8]** :
<p align="center"><img width="600" height="500" alt="X_Y_Axe_2_8" src="https://github.com/user-attachments/assets/0615f30f-0c0f-4ec7-8b2d-e169806e9725" /></p>

<br>
<br>

- **Vue de face (XZ) [2-8]** :
<p align="center"><img width="600" height="500" alt="X_Z_Axe_2_8_zoom" src="https://github.com/user-attachments/assets/4d656383-3c02-486a-bcad-8b2422bb3555" /></p>

<br>
<br>

- **Vue de profile (YZ) [2-8]** :
<p align="center"><img width="600" height="500" alt="Y_Z_Axe_2_8_zoom" src="https://github.com/user-attachments/assets/09013b31-5a2d-4e44-b1a3-87f35fcb2b82" /></p>

<br>
<br>

### Limitations/Questions :
- Les points LiDAR 3D sont en vue d'**en haut**.
- Comment définir plusieurs zones pour faire la grille / les grilles?
- Combien prendre de "**sample_size**".
- Comment automatiser les découpes et **optimiser** le temps de calcul?
- Comment ne pas couper à l'intérieur d'un bâtiment ou d'une végétation? **(choix du pas de X)**

<p align="center"><img width="353" height="329" alt="image" src="https://github.com/user-attachments/assets/357e415e-99cc-4472-81f7-32fc97d023b5" /></p>

- À la **fin**, on a une map, avec les ombres ou autre chose (donc retour à la **3D** à la fin ou **non**)?


## Solution supposée :
## Solution 1 (Pas utilisé) :

- **Nettoyer** les points qui ne nous intéressant pas.
- Prendre le point de vue **[XZ]**, faire des découpes *(de combien de mètre à chaque fois? **(le pas)**)*. -> On pourraît juste prendre une approximation (mais c'est pas idéale pour la **refaisabilité**...). 
- Faire un point de vue **[YZ]** de chaque découpe. *(Comment faire ça ?)*
- Prendre les **points** de chaque découpe finale et les mettre dans une **grille**.
- Utiliser des **boîtes** *(bounding volume hierarchies)*.
- Lancer des rayons **(raytracing)**.
- Tester l'**intervisibilité**.
- *[Si à la fin retour à la 3D]* Assembler toutes **les vues**. *(Comment faire ça ?)*

### [Lidar [18455_51780] [Chemin du bois Balmont] pas 5](https://data.grandlyon.com/portail/fr/jeux-de-donnees/nuage-de-points-lidar-2023-de-la-metropole-de-lyon/donnees) :

<br> 
<p align="center"><img width="550" height="450" alt="image" src="https://github.com/user-attachments/assets/d4c060c2-9f72-430d-9aea-4c4d53492355" /></p>

[Découpe 2D Profile](https://github.com/VCityTeam/VCity/blob/master/Projects/IArbre/Stage-Shadow_Modeling/Implementation/Lidar_2D_Visualisation_XY_Classification.py) :

<p align="center"><img width="550" height="450" alt="Decoupe1" src="https://github.com/user-attachments/assets/cac97811-8de9-4329-9c87-2d24c78091c9" /></p>
<p align="center"><img width="550" height="450" alt="decoupe2" src="https://github.com/user-attachments/assets/cd5dafbf-d7ca-456e-9683-e39fac3f37fb" /></p>

<br>
<br>

### [Lidar [18420_51760] [Croix-Rousse] pas 50](https://data.grandlyon.com/portail/fr/jeux-de-donnees/nuage-de-points-lidar-2023-de-la-metropole-de-lyon/donnees) :

<br>
<p align="center"><img width="800" height="600" alt="Croix-Rousse" src="https://github.com/user-attachments/assets/b0369e5b-1c7e-4e9a-abf6-4de7794a2a23" /></p>
<p align="center"><img width="800" height="600" alt="dec1_arond_1" src="https://github.com/user-attachments/assets/d902a2c3-0d10-4394-a539-47663635bbf4" /></p>
<p align="center"><img width="800" height="600" alt="dec2_arond_1" src="https://github.com/user-attachments/assets/2be91c92-9170-4026-ad39-2aafe708fa7e" /></p>
<p align="center"><img width="800" height="600" alt="dec3_arond_1" src="https://github.com/user-attachments/assets/8b121f93-9103-4baf-9c45-86f236ee0e0d" /></p>
<p align="center"><img width="800" height="600" alt="dec4_arond_1" src="https://github.com/user-attachments/assets/65cad484-1924-4ab3-9a60-8021ded8f47b" /></p>
<p align="center"><img width="800" height="600" alt="dec5_arond_1" src="https://github.com/user-attachments/assets/624ad7db-aa26-4368-a175-30787483497e" /></p>
<p align="center"><img width="800" height="600" alt="dec6_arond_1" src="https://github.com/user-attachments/assets/0571085a-ab99-4602-b085-fcaf7aea7aa3" /></p>

<br>

## [Solution 2 (utilisé)](https://www.mdpi.com/2220-9964/10/9/583) :

<br>

## Test 1 :

### [Lidar [18460_51765] [Rue Geoffray]](https://data.grandlyon.com/portail/fr/jeux-de-donnees/nuage-de-points-lidar-2023-de-la-metropole-de-lyon/donnees) :

<br>

<img width="800" height="600" alt="Capture d&#39;écran 2026-06-29 142510" src="https://github.com/user-attachments/assets/8fbb30c7-34b4-4d89-bce3-49bd773e51be" />

<br>
<br>

[Visualisation LiDAR 2D avec classification :](https://github.com/VCityTeam/VCity/blob/master/Projects/IArbre/Stage-Shadow_Modeling/Implementation/Lidar_2D_Visualisation_XY_Classification.py)

<img width="800" height="600" alt="tram_Roger Planchon" src="https://github.com/user-attachments/assets/383f15bc-ac76-48f1-ab16-346e0a935ea3" />

<br>

### Couleurs : 
- [1] : "gray" --> non classé.
- [2] : "brown"  --> sol.
- [3] : "lightgreen" --> végétation faible, <1.5m.
- [4] : "green" --> végétation moyenne 1.5-5m.
- [5] : "darkgreen" --> végétation forte 5-15m.
- [6] : "red"  --> bâtiments.
- [8] : "yellow" --> Réservé, végétation > 15m.
- [9] : "blue"  --> eau.

<br>
<br>

[Teste d'un algo de bvh](https://github.com/VCityTeam/VCity/blob/master/Projects/IArbre/Stage-Shadow_Modeling/Implementation/Bvh_laz_visualisation.py) :

<img width="800" height="600" alt="tram_RogerPlanchon_Bvh_laz" src="https://github.com/user-attachments/assets/c1bc31be-e55a-4171-91e0-ff4b6cabf0bb" />


<br>
<br>
<br>
<br>

### [Teste sans intervisibilité](https://github.com/VCityTeam/VCity/blob/master/Projects/IArbre/Stage-Shadow_Modeling/Implementation/Implementation_algo_2_5D_bvh_sans_intervisibility_.py) :

<br>

<img width="800" height="600" alt="Map_2_5_Sans_intervisibility" src="https://github.com/user-attachments/assets/c4aa53ae-77f4-4bff-ba2a-b9373ae2aa59" />

<br>

- latitude_deg = 45.75 .
- Tau_deg = 45 .
- datetime(2025, 6, 21) .
- time_index = 1 .

<br>

### [Teste avec intervisibilité](https://github.com/VCityTeam/VCity/blob/master/Projects/IArbre/Stage-Shadow_Modeling/Implementation/Implementation_algo_2_5_D_bvh_avec_intervisibility.py) :

<br> 

#### **Projection N°1** :

<img width="800" height="600" alt="Projection_18460_51765_index_1_tau_deg_45" src="https://github.com/user-attachments/assets/890a0851-cfba-41dc-9446-dc9665122c40" />


<br>
<br>

**Informations :** <br>
- time_index = 1 <br>
- position soleil : [alpha ; psi ; omega] = [29.264349742310962 ; 85.51137589043786 ; -71.42853114934448].

<br>

<br>

#### **Projection N°2** :

<img width="800" height="600" alt="Projection_18460_51765_index_5_tau_deg_45" src="https://github.com/user-attachments/assets/fb0bb778-561f-4e26-9700-c97e7e9cc66b" />


<br>
<br>

**Informations :** <br>
- time_index = 5 <br>
- position soleil : [alpha ; psi ; omega] = [4.648687025920685 ; 299.2415138716923 ; 108.57146885065552].

<br>
<br>

#### **Projection N°3** : 

<img width="800" height="600" alt="Projection_18460_51765_index_2_tau_deg_45" src="https://github.com/user-attachments/assets/8ace3b07-2a96-410d-b2f4-6d943f927e5c" />


<br>
<br>

**Informations :** <br>
- time_index = 2 <br>
- position soleil : [alpha ; psi ; omega] = [59.119477957772474 ; 127.28641218668238 ; -26.428531149344476].

<br>
<br>
<br>
<br>


## Test 2 : 

### [Lidar [18420_51760] [Croix-Rousse]](https://data.grandlyon.com/portail/fr/jeux-de-donnees/nuage-de-points-lidar-2023-de-la-metropole-de-lyon/donnees) :

<br>
<img width="800" height="600" alt="Croix-Rousse" src="https://github.com/user-attachments/assets/b0369e5b-1c7e-4e9a-abf6-4de7794a2a23" />

<br>

<img width="800" height="600" alt="Projection_18420_51760_2D" src="https://github.com/user-attachments/assets/05eba8e3-8245-4e39-8114-35081f1719a0" />

<br>
<br>
<br>
<!--
#### **Projection N°1** :
img
<br>
<br>
**Informations :** <br>
- time_index = 0 <br>
- position soleil : [alpha ; psi ; omega] = [3.1805546814635168e-15 ; 55.24412549809187 ; -116.42853114934448].
<br>
<br>
-->

#### **Projection N°1** :

<img width="800" height="600" alt="Projection_18420_51760_index_1_tau_deg_45" src="https://github.com/user-attachments/assets/f70729e8-ba8b-4cc6-9eee-d4c5aecea50e" />


<br>
<br>

**Informations :** <br>
- time_index = 1 <br>
- position soleil : [alpha ; psi ; omega] = [29.264349742310962 ; 85.51137589043786 ; -71.42853114934448].

<br>

<br>

#### **Projection N°2** :

<img width="800" height="600" alt="Projection_18420_51760_index_2_tau_deg_45" src="https://github.com/user-attachments/assets/4ab1d54a-6e69-4edc-b2db-85f1907ce74d" />


<br>
<br>

**Informations :** <br>
- time_index = 2 <br>
- position soleil : [alpha ; psi ; omega] = [59.119477957772474 ; 127.28641218668238 ; -26.428531149344476].

<br>
<br>

#### **Projection N°3** : 

<img width="800" height="600" alt="Projection_18420_51760_index_3_tau_deg_45" src="https://github.com/user-attachments/assets/302d4b96-4e99-41ee-8a46-cb5cd7a5c68c" />



<br>
<br>

**Informations :** <br>
- time_index = 3 <br>
- position soleil : [alpha ; psi ; omega] = [63.101547700941175 ; 220.23179929257847 ; 18.571468850655524]. 
<br>

<br>

#### **Projection N°4** :

<img width="800" height="600" alt="Projection_18420_51760_index_4_tau_deg_45" src="https://github.com/user-attachments/assets/ad4d0917-a416-4a3b-a3f0-98bb0e3e154e" />


<br>
<br>

**Informations :** <br>
- time_index = 4 <br>
- position soleil : [alpha ; psi ; omega] = [34.74225216903812 ; 268.9594184636189 ; 63.57146885065553].

<br>
<br>

#### **Projection N°5** :

<img width="800" height="600" alt="Projection_18420_51760_index_5_tau_deg_45" src="https://github.com/user-attachments/assets/4972f388-e828-41a3-a6f6-61c9bd24ab5f" />


<br>
<br>

**Informations :** <br>
- time_index = 5 <br>
- position soleil : [alpha ; psi ; omega] = [4.648687025920685 ; 299.2415138716923 ; 108.57146885065552].

<br>
<br>
<br>
<br>

## Explication de l'Algorithme :

### **1- chargement des données [file .laz]**

- laz -> las 
<br>

**Return** (column (x; y; z); classification)
<br>
<br>

### **2 - Construction du DSM (Mode de surface numérique) [(x, y, z, classification) ; résolution=1.0]**

- Récupère les plus petites coordonnées en x et en y parmi tous les points.<br>
- Récupère les plus grandes coordonnées en x et en y.<br>
- Calcule le nombre de colonnes nécessaires pour couvrir toute la zone.<br>
- Calcule le nombre de lignes nécessaires pour couvrir toute la zone.<br>
- Création d'une grille DSM.<br>
- Mets la valeur de la hauteur la plus grande dans chaque case de la grille.<br>
<br>

**Return** (DSM; xmin; ymin; résolution)
<br>
<br>

### **3- Transformation de la grille en cellules [DSM]**
- Crée un tableau pour les cellules<br>
- Récupère la hauteur de chaque case.<br>
- Vérifie que la case contient une valeur valide.<br>
- Ajoute à la liste les coordonnées (ix; iy) et la hauteur (z)<br>
- Convertie la liste en tableau NumPy.<br>
<br>

**Return** (tableau NumPy de cellule)
<br>
<br>

### **4- Création de la classe BVHNode [Tableau NumPy (cellule)]**
- Constructeur avec les cellules et la taille max des feuilles.<br>
- Récupère (x; y) des cellules.<br>
- Calcule les coordonnées minimales et maximales du nœud.<br>
- Trie les cellules selon la direction où les nœuds sont les plus étendues.<br>
- Création du sous-arbre droit et gauche.<br>
<br>

**Return** (deux sous-arbres)
<br>
<br>

### **5- Choix des données (Date ; Latitude en degrés; tau en degrés).**
<br>
<br>

### **6- Calcule de la position du soleil au cours d'une journée [Latitude en degrés; tau en degrés; date]** 
- Conversion en radians de latitude.<br>
- Récupère le numéro du jour dans l'année.<br>
- Calcule la position de la terre en fonction du jour donné<br>
- Calcule la position du soleil par rapport à l'équateur terrestre<br>
- Calcule l'angle horaire correspondant au coucher du soleil<br>
- Déduction de l'angle horaire correspondant au lever du soleil<br>
- Convertit le pas de calcul des angles "tau" en radians<br>
- Initialise l'angle horaire "oméga" au lever du soleil<br>
- Calcule depuis le lever du soleil jusqu'au coucher. (en avançant par angle solaire)<br>
- Calcule la hauteur du soleil dans le ciel.<br>
- Calcule l'azimut du soleil (sa direction dans le plan horizontal)<br>
<br>

**Return** (list alpha(élévations); list psi (azimuths); omega (hour_angles) ) en degré
<br>
<br>

### **7- On choisit un moment de la journée (time_index)**
<br>
<br>

### **8- Parcours de l'arbre BVH [noeud; alpha ; psi ; DSM ; shadow]**
- Parcourt toutes les cellules de chaque feuille.<br>
- Traite chaque cellule pour déterminer son effet sur les ombres.<br>
- Parcourt récursivement les sous-arbres gauche et droit.<br>
<br>

**Return** (Lance le traitement) 
<br>
<br>

### **9- Traitement de chaque cellule pour déterminer son effet sur les ombres []**
- Vérification si le soleil n'est pas sous l'horizon<br>
- Calcule "theta" la direction opposée au Soleil (direction de l'ombre)<br>
- Calcule la longueur théorique de l'ombre.<br>
- Calcule le déplacement horizontal de l'ombre<br>
- Calcule le déplacement vertical de l'ombre<br>
- Calcule la position finale de l'ombre selon l'axe X et Y<br>
- Calcule toutes les cellules situées sur la ligne représentant l'ombre<br>
- Convertie les coordonnées de la cellule en entiers.<br>
- Récupère la hauteur de la cellule d'origine.<br>
- Parcourt toutes les cellules situées sur la ligne de l'ombre.<br>
- Calcule la distance et l'angle "beta" entre la cellule d'origine et la cellule courante.<br>
- Vérifie si la cellule courante est masquée par rapport à la position du Soleil ( beta >= alpha)<br>
- Si Vrai, alors ajoute cette cellule à la liste de cellules à l'ombre.<br>
<br>

**Return** (tableau de cellules à l'ombre)
<br>
<br>

### **10- Afficher un Plot avec les ombres [tableau de cellules à l'ombre]**
<br>	

**Return** (Plot avec les ombres)












...
