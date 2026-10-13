# Tests d'implementation de l'algo :
## Tests sur [version 2 de l'algo](https://github.com/VCityTeam/VCity/blob/master/Projects/IArbre/Stage-Shadow_Modeling/Implementation/Algo_intervisibility_bvh_classification_user_choice.py) : 
(Classification et date choisie par l'utilisateur + améliorations + correction sur la position du soleil)
<br>

## [Lidar [18535_51805] [Fountain of Love]](https://data.grandlyon.com/portail/fr/jeux-de-donnees/nuage-de-points-lidar-2023-de-la-metropole-de-lyon/donnees) :

### Test 1 : [Vegetation ranging from <1.5 m to 15 m only]

<img width="800" height="600" alt="Capture d’écran 2026-07-06 155101" src="https://github.com/user-attachments/assets/0f1bd812-1e6a-40b6-9004-d7fd69a626ba" />

<br>
<br>

<img width="800" height="600" alt="Projection_18535_51805_2D" src="https://github.com/user-attachments/assets/fdcdc671-9c5b-454a-83e5-3a8ac32bcabb" />

<br>
<br>

### Code couleur : <br>
- Gray : Non classé. <br>
- Brown : Sol. <br>
- Lightgreen : Végétation faible <1.5m. <br>
- Green : Végétation moyenne 1.5-5m. <br>
- Darkgreen : Végétation forte 5-15m. <br>
- Red : Bâtiments. <br>
- Yellow : Réservé, végétation > 15m. <br>
- Blue : Eau. <br>

<br>
<br>
<br>

#### **Projection N°1** :

<img width="800" height="600" alt="Classification_végétation_faible_a_forte_18530_51805_index_time_1_date_2023_06_06" src="https://github.com/user-attachments/assets/c9c41858-b72f-4ef1-a246-7d92b01e9737" />

**Informations :** <br>
- Classification : 2 (Végétation de <1.5m à 15m uniquement). <br>
- Date : 2023-06-06. <br>
- Time_index = 1. <br>
- Position soleil : [élevation ; azimut ; angle horaire] = [29.4891902454722 ; 86.93292780672712 ; -70.36347446422826].
- Latitude_deg = 45.75.
- Tau_deg = 45.

<br>
<br>

#### **Projection N°2** :

<img width="800" height="600" alt="Classification_végétation_faible_a_forte_18530_51805_index_time_2_date_2023_06_06" src="https://github.com/user-attachments/assets/b8c5bd28-15cd-4154-be3f-a8b232acfae6" />

**Informations :** <br>
- Classification : 2 (Végétation de <1.5m à 15m uniquement). <br>
- Date : 2023-06-06. <br>
- Time_index = 2. <br>
- Position soleil : [élevation ; azimut ; angle horaire] = [59.06485876682362 ; 129.73526568769887 ; -25.36347446422826].
- Latitude_deg = 45.75.
- Tau_deg = 45.

<br>
<br>

#### **Projection N°3** :

<img width="800" height="600" alt="Classification_végétation_faible_a_forte_18530_51805_index_time_3_date_2023_06_06" src="https://github.com/user-attachments/assets/5ac45f68-5e33-4bbd-b64f-48c6a8d9f4e8" />

**Informations :** <br>
- Classification : 2 (Végétation de <1.5m à 15m uniquement). <br>
- Date : 2023-06-06. <br>
- Time_index = 3. <br>
- Position soleil : [élevation ; azimut ; angle horaire] = [61.92982761805288 ; 221.22999284869766 ; 19.63652553577174].
- Latitude_deg = 45.75.
- Tau_deg = 45.

<br>
<br>

#### **Projection N°4** :

<img width="800" height="600" alt="Classification_végétation_faible_a_forte_18530_51805_index_time_4_date_2023_06_06" src="https://github.com/user-attachments/assets/98ebbc08-7bea-4306-a5c2-d7f94275a7c3" />

**Informations :** <br>
- Classification : 2 (Végétation de <1.5m à 15m uniquement). <br>
- Date : 2023-06-06. <br>
- Time_index = 4. <br>
- Position soleil : [élevation ; azimut ; angle horaire] = [33.48389275064094 ; 269.0075015869622 ; 64.63652553577174].
- Latitude_deg = 45.75.
- Tau_deg = 45.

<br>
<br>

#### **Projection N°5** :

<img width="800" height="600" alt="Classification_végétation_faible_a_forte_18530_51805_index_time_5_date_2023_06_06" src="https://github.com/user-attachments/assets/607f6746-6944-44c1-b784-8080a8cceed8" />

**Informations :** <br>
- Classification : 2 (Végétation de <1.5m à 15m uniquement). <br>
- Date : 2023-06-06. <br>
- Time_index = 5. <br>
- Position soleil : [élevation ; azimut ; angle horaire] = [3.4078530164730294 ; 299.4550810098693 ; 109.63652553577174].
- Latitude_deg = 45.75.
- Tau_deg = 45.

<br>
<br>

### Autres [Tests](https://github.com/VCityTeam/VCity/blob/master/Projects/IArbre/Stage-Shadow_Modeling/Implementation/Generate_DSM_DTM_CHM_TIF_File.py) :
- Digital Surface Model :
<img width="640" height="480" alt="DSM" src="https://github.com/user-attachments/assets/afeebbe5-1860-4841-9b12-fc3103878e7e" />

<br>
<br>

- Digital Terrain Model :
<br>
<img width="640" height="480" alt="DTM" src="https://github.com/user-attachments/assets/e6ebe68e-adc1-431f-9480-252c8f2e13b2" />

<br>
<br>

- Canopy Height Model :
<br>
<img width="640" height="480" alt="CHM" src="https://github.com/user-attachments/assets/47bd8a13-7cb0-4b58-a8d4-0fa6381bd584" />

<br>
<br>
<br>
<br>

## [Lidar [18415_51750] [Fourvière]](https://data.grandlyon.com/portail/fr/jeux-de-donnees/nuage-de-points-lidar-2023-de-la-metropole-de-lyon/donnees) :

### Test 2 : [ALL Classification]

<img width="700" height="600" alt="Map_Fourviere_18415_51750l" src="https://github.com/user-attachments/assets/7eccd490-8ebb-4ba2-a3c8-749f596282a4" />

<br>
<br>

<img width="800" height="600" alt="Visualisation_2D_18415_51750" src="https://github.com/user-attachments/assets/7e3e8cdf-9c13-4f6e-a0b9-a4a261444af0" />

<br>
<br>

### Code couleur : <br>
- Gray : Non classé. <br>
- Brown : Sol. <br>
- Lightgreen : Végétation faible <1.5m. <br>
- Green : Végétation moyenne 1.5-5m. <br>
- Darkgreen : Végétation forte 5-15m. <br>
- Red : Bâtiments. <br>
- Yellow : Réservé, végétation > 15m. <br>
- Blue : Eau. <br>

<br>
<br>
<br>

#### **Projection N°1** :

<img width="800" height="600" alt="Index_time_0_Classification_ALL_18415_51750" src="https://github.com/user-attachments/assets/dc1591e6-0592-4d28-9ddb-ee2d40e804a6" />

**Informations :** <br>
- Classification : 1 (All classifications). <br>
- Date : 2023-10-17. <br>
- Time_index = 0. <br>
- Position soleil : [élevation ; azimut ; angle horaire] = [3.975693351829396e-15 ; 103.21232756056426 ; -80.45390787311284].
- Latitude_deg = 45.75.
- Tau_deg = 45.

<br>
<br>

#### **Projection N°2** :

<img width="800" height="600" alt="Index_time_1_Classification_ALL_18415_51750" src="https://github.com/user-attachments/assets/9aa7cfc7-3a2f-4628-ac68-7dff38e63113" />

**Informations :** <br>
- Classification : 1 (All classifications). <br>
- Date : 2023-10-17. <br>
- Time_index = 1. <br>
- Position soleil : [élevation ; azimut ; angle horaire] = [26.54440085786707 ; 140.2009528071764 ; -35.45390787311284].
- Latitude_deg = 45.75.
- Tau_deg = 45.

<br>
<br>

#### **Projection N°3** :

<img width="800" height="600" alt="Index_time_2_Classification_ALL_18415_51750" src="https://github.com/user-attachments/assets/78608a26-ebc1-465c-8eaf-726bc9950663" />

**Informations :** <br>
- Classification : 1 (All classifications). <br>
- Date : 2023-10-17. <br>
- Time_index = 2. <br>
- Position soleil : [élevation ; azimut ; angle horaire] = [34.407760997636665 ; 191.4455989599242 ; 9.546092126887157].
- Latitude_deg = 45.75.
- Tau_deg = 45.

<br>
<br>

#### **Projection N°4** :

<img width="800" height="600" alt="Index_time_3_Classification_ALL_18415_51750" src="https://github.com/user-attachments/assets/c85e9e21-ab34-4cc8-80cc-dcba97308c8c" />

**Informations :** <br>
- Classification : 1 (All classifications). <br>
- Date : 2023-10-17. <br>
- Time_index = 3. <br>
- Position soleil : [élevation ; azimut ; angle horaire] = [16.57857638410074 ; 237.03835712687686 ; 54.54609212688716].
- Latitude_deg = 45.75.
- Tau_deg = 45.

Comparative avec un [simulateur d'ombre](https://shadowmap.org/fr/) en ligne : 

<img width="800" height="600" alt="Compar_3D_coucher_soleil" src="https://github.com/user-attachments/assets/5b9f9d0e-a7bd-4856-a662-f77387221a25" />


<br>
<br>


## Tests sur [version 3 de l'algo](https://github.com/VCityTeam/VCity/blob/master/Projects/IArbre/Stage-Shadow_Modeling/Implementation/Shadow_Modeling_BVH_Intervisibility_Classification_LYON_API_LAZ.py) : 
(Classification, date et données d'entrées choisie par l'utilisateur + améliorations + API Data Grand Lyon)
<br>

## [Lidar [18480_51800] [Centre Aéré des Lônes]](https://data.grandlyon.com/portail/fr/jeux-de-donnees/nuage-de-points-lidar-2023-de-la-metropole-de-lyon/donnees) :

### Test 1 : [Classification ALL]

<img width="643" height="647" alt="Map_1848000_5180000" src="https://github.com/user-attachments/assets/66236b9b-2f73-401a-b8bc-50ad060fc0e5" />

<br>
<br>

<img width="800" height="600" alt="Representation_2D_1848000_5180000" src="https://github.com/user-attachments/assets/b99dcc7a-87df-4518-9793-a6df6bf54b85" />

<br>
<br>

### Code couleur : <br>
- Gray : Non classé. <br>
- Brown : Sol. <br>
- Lightgreen : Végétation faible <1.5m. <br>
- Green : Végétation moyenne 1.5-5m. <br>
- Darkgreen : Végétation forte 5-15m. <br>
- Red : Bâtiments. <br>
- Yellow : Réservé, végétation > 15m. <br>
- Blue : Eau. <br>

<br>
<br>
<br>

#### **Projection N°1 et Comparative avec le résultat de [ShadowMap.org](https://app.shadowmap.org)** :

**Projection de l'algorithme implémenté :**

<img width="800" height="600" alt="Shadow_1848000_5180000_index_0" src="https://github.com/user-attachments/assets/c6f5f298-7cb0-41fb-9029-cb5e9161d271" />

**Informations :** <br>
- Classification : 1 (Classification ALL). <br>
- Date : 2023-07-09. <br>
- Time_index = 0. <br>
- Position soleil : [élevation ; azimut ; angle horaire] = [3.1805546814635168e-15 ; 56.942840815065374 ; -114.99439377247822].
- Latitude_deg = 45.75.
- Tau_deg = 45.

<br>

**Projection de ShadowMap.org :**

<img width="800" height="600" alt="ShadoMap_Compar_index_0" src="https://github.com/user-attachments/assets/570db701-a875-47fd-9d11-c192664f5ced" />

**Informations :** <br>
- Date : 2026-07-09. <br>
- Période de l'année : Solstice d'été. <br>
- Dimention : 3D.
- Position soleil : [élevation ; azimuth] = [3.1 ; 60.6]. 

<br>
<br>

#### **Projection N°2 et Comparative avec le résultat de [ShadowMap.org](https://app.shadowmap.org)** :

**Projection de l'algorithme implémenté :**

<img width="800" height="600" alt="Shadow_1848000_5180000_index_1" src="https://github.com/user-attachments/assets/0568e30a-c560-4bc6-aa08-c5341ce5b6a4" />

**Informations :** <br>
- Classification : 1 (Classification ALL). <br>
- Date : 2023-07-09. <br>
- Time_index = 1. <br>
- Position soleil : [élevation ; azimut ; angle horaire] = [29.564153948733516 ; 87.43088978790263 ; -69.99439377247822].
- Latitude_deg = 45.75.
- Tau_deg = 45.

<br>

**Projection de ShadowMap.org :**

<img width="800" height="600" alt="ShadoMap_Compar_index_1" src="https://github.com/user-attachments/assets/c95f1a73-1916-4884-9dec-df7bf19afedc" />


**Informations :** <br>
- Date : 2026-07-09. <br>
- Période de l'année : Solstice d'été. <br>
- Dimention : 3D.
- Position soleil : [élevation ; azimuth] = [29.5 ; 87.4]. 

<br>
<br>

#### **Projection N°3 et Comparative avec le résultat de [ShadowMap.org](https://app.shadowmap.org)** :

**Projection de l'algorithme implémenté :**

<img width="800" height="600" alt="Shadow_1848000_5180000_index_2" src="https://github.com/user-attachments/assets/7ca1c34f-d9d1-45e2-b4f4-5afbfddc46a9" />

**Informations :** <br>
- Classification : 1 (Classification ALL). <br>
- Date : 2023-07-09. <br>
- Time_index = 2. <br>
- Position soleil : [élevation ; azimut ; angle horaire] = [59.03493203913864 ; 130.5883032054322 ; -24.994393772478226].
- Latitude_deg = 45.75.
- Tau_deg = 45.

<br>

**Projection de ShadowMap.org :**

<img width="800" height="600" alt="ShadoMap_Compar_index_2" src="https://github.com/user-attachments/assets/d3c6a83f-508e-4c43-80a4-7927400d09a9" />

**Informations :** <br>
- Date : 2026-07-09. <br>
- Période de l'année : Solstice d'été. <br>
- Dimention : 3D.
- Position soleil : [élevation ; azimuth] = [59.0 ; 130.6]. 

<br>
<br>

#### **Projection N°4 et Comparative avec le résultat de [ShadowMap.org](https://app.shadowmap.org)** :

**Projection de l'algorithme implémenté :**

<img width="800" height="600" alt="Shadow_1848000_5180000_index_3" src="https://github.com/user-attachments/assets/28a7c2bf-a4d6-4e65-9c08-0b1bff4c510e" />

**Informations :** <br>
- Classification : 1 (Classification ALL). <br>
- Date : 2023-07-09. <br>
- Time_index = 3. <br>
- Position soleil : [élevation ; azimut ; angle horaire] = [61.518963516511135 ; 221.56075915542365 ; 20.005606227521774].
- Latitude_deg = 45.75.
- Tau_deg = 45.

<br>

**Projection de ShadowMap.org :**

<img width="800" height="600" alt="ShadoMap_Compar_index_3" src="https://github.com/user-attachments/assets/59dd815f-0b70-41a4-9d67-65963a744ca8" />

**Informations :** <br>
- Date : 2026-07-09. <br>
- Période de l'année : Solstice d'été. <br>
- Dimention : 3D.
- Position soleil : [élevation ; azimuth] = [61.5 ; 221.4]. 

<br>
<br>

#### **Projection N°5 et Comparative avec le résultat de [ShadowMap.org](https://app.shadowmap.org)** :

**Projection de l'algorithme implémenté :**

<img width="800" height="600" alt="Shadow_1848000_5180000_index_4" src="https://github.com/user-attachments/assets/9c18c6be-c642-4a37-970d-5190e5d9ba64" />

**Informations :** <br>
- Classification : 1 (Classification ALL). <br>
- Date : 2023-07-09. <br>
- Time_index = 4. <br>
- Position soleil : [élevation ; azimut ; angle horaire] = [33.04438188653503 ; 269.02396565600895 ; 65.00560622752178].
- Latitude_deg = 45.75.
- Tau_deg = 45.

<br>

**Projection de ShadowMap.org :**

<img width="800" height="600" alt="ShadoMap_Compar_index_4" src="https://github.com/user-attachments/assets/0084e503-d7f5-4b89-be19-f83839e6233a" />

**Informations :** <br>
- Date : 2026-07-09. <br>
- Période de l'année : Solstice d'été. <br>
- Dimention : 3D.
- Position soleil : [élevation ; azimuth] = [32.9 ; 269.1]. 

<br>
<br>

#### **Projection N°6 et Comparative avec le résultat de [ShadowMap.org](https://app.shadowmap.org)** :

**Projection de l'algorithme implémenté :**

<img width="800" height="600" alt="Shadow_1848000_5180000_index_5" src="https://github.com/user-attachments/assets/0a1e384e-c820-49ae-8ede-cd53f260d28b" />

**Informations :** <br>
- Classification : 1 (Classification ALL). <br>
- Date : 2023-07-09. <br>
- Time_index = 5. <br>
- Position soleil : [élevation ; azimut ; angle horaire] = [2.9744555770199193 ; 299.5295335190389 ; 110.00560622752178].
- Latitude_deg = 45.75.
- Tau_deg = 45.

<br>

**Projection de ShadowMap.org :**

<img width="800" height="600" alt="ShadoMap_Compar_index_5" src="https://github.com/user-attachments/assets/05a31a69-2bac-4f78-9e33-e861c3b3766e" />

**Informations :** <br>
- Date : 2026-07-09. <br>
- Période de l'année : Solstice d'été. <br>
- Dimention : 3D.
- Position soleil : [élevation ; azimuth] = [3.0 ; 299.5]. 

<br>
<br>
<br>
<br>


## Tests avec classe arbre (code non finie)
## [Lidar [18460_51775] [IUT Lyon 1 - site de Villeurbanne Doua]](https://data.grandlyon.com/portail/fr/jeux-de-donnees/nuage-de-points-lidar-2023-de-la-metropole-de-lyon/donnees) :

<img width="553" height="519" alt="Map" src="https://github.com/user-attachments/assets/fc269fd3-27ea-41df-ba85-5e05d7f014e5" />

<br>
<br>

<img width="800" height="600" alt="Representation_2D" src="https://github.com/user-attachments/assets/a7fbd8b8-e7cd-4871-8536-5a206abb90b1" />

<br>
<br>

### Code couleur : <br>
- Gray : Non classé. <br>
- Brown : Sol. <br>
- Lightgreen : Végétation faible <1.5m. <br>
- Green : Végétation moyenne 1.5-5m. <br>
- Darkgreen : Végétation forte 5-15m. <br>
- Red : Bâtiments. <br>
- Yellow : Réservé, végétation > 15m. <br>
- Blue : Eau. <br>

<br>
<br>
<br>

#### **Projection N°1** :

<img width="800" height="600" alt="Index_time_0_avec_canopee" src="https://github.com/user-attachments/assets/b45fa07d-fc0e-4fcf-b7ae-9a26abb10384" />

**Informations :** <br>
- Classification : végétation. <br>
- Date : 2023-10-17. <br>
- Time_index = 0. <br>
- Position soleil : [élevation ; azimut ; angle horaire] = [3.975693351829396e-15 ; 103.21232756056426 ; -80.45390787311284].
- Latitude_deg = 45.75.
- Tau_deg = 45.

<br>
<br>

#### **Projection N°2** :

<img width="800" height="600" alt="Index_time_1_avec_canopee" src="https://github.com/user-attachments/assets/2c26b222-c487-4739-afef-034094b25b4a" />

**Informations :** <br>
- Classification : végétation.. <br>
- Date : 2023-10-17. <br>
- Time_index = 1. <br>
- Position soleil : [élevation ; azimut ; angle horaire] = [26.54440085786707 ; 140.2009528071764 ; -35.45390787311284].
- Latitude_deg = 45.75.
- Tau_deg = 45.

<br>
<br>

#### **Projection N°3** :

<img width="800" height="600" alt="Index_time_2_avec_canopee" src="https://github.com/user-attachments/assets/609288d2-bee2-425d-9fac-53afff6e3a03" />

**Informations :** <br>
- Classification : végétation. <br>
- Date : 2023-10-17. <br>
- Time_index = 2. <br>
- Position soleil : [élevation ; azimut ; angle horaire] = [34.407760997636665 ; 191.4455989599242 ; 9.546092126887157].
- Latitude_deg = 45.75.
- Tau_deg = 45.

<br>
<br>

#### **Projection N°4** :

<img width="800" height="600" alt="Index_time_3_avec_canopee" src="https://github.com/user-attachments/assets/8d7994eb-4098-42eb-a164-49a8f67846fd" />

**Informations :** <br>
- Classification : 2 végétation. <br>
- Date : 2023-10-17. <br>
- Time_index = 3. <br>
- Position soleil : [élevation ; azimut ; angle horaire] = [16.57857638410074 ; 237.03835712687686 ; 54.54609212688716].
- Latitude_deg = 45.75.
- Tau_deg = 45.

<br>
<br>
