# I. Light Curves

## **1. Champs Généraux**

### **a. `Datasets`**
- **Description :**
  - **Liste des Jeux de Données** : Indique les différents segments ou modes d'observation pour lesquels les courbes de lumière ont été générées.
  - **Exemple :**
    - `'WT_incbad'`, `'WTHard_incbad'`, `'WTSoft_incbad'`, etc.

### **b. `Binning` : Counts**
- **Description :**
  - **Type de Binning** : Indique que les données sont regroupées par **comptages**. Cela signifie que les courbes de lumière sont créées en comptant le nombre de photons détectés dans des intervalles de temps spécifiques.

### **c. `TimeFormat` : MET**
- **Description :**
  - **Format du Temps** : **Mission Elapsed Time** (MET), qui représente le temps écoulé depuis le lancement de la mission. C'est une mesure temporelle standard utilisée dans les données spatiales pour assurer la cohérence des timings.

### **d. `T0` : 314995072**
- **Description :**
  - **Temps de Référence (T0)** : Un point de départ temporel utilisé pour calculer les temps relatifs dans les courbes de lumière. Ce nombre représente généralement le nombre de secondes écoulées depuis une date de référence spécifique (par exemple, le lancement de la mission).

### **e. `URLs`**
- **Description :**
  - **Liens vers les Fichiers de Données** : Fournissent les URLs où les fichiers de courbes de lumière correspondants peuvent être téléchargés.
  - **Exemple :**
    - `'WT_incbad': 'https://www.swift.ac.uk/xrt_curves/00441015/WTCURVE.qdp'`

---

## **2. Champs Spécifiques par Jeu de Données**

Chaque jeu de données (`WT_incbad`, `WTHard_incbad`, etc.) possède des champs spécifiques. Voici une explication détaillée de ces champs :

### **a. `WT_incbad`**
- **Modes :** `WT` (Windowed Timing)
- **Colonnes :**
  - **`Time`** : Temps relatif depuis `T0`, en secondes.
  - **`TimePos`** : Incertitude positive sur le temps.
  - **`TimeNeg`** : Incertitude négative sur le temps.
  - **`Rate`** : Taux de comptage des photons (comptes par seconde).
  - **`RatePos`** : Incertitude positive sur le taux de comptage.
  - **`RateNeg`** : Incertitude négative sur le taux de comptage.
  - **`FracExp`** : Fraction du temps d'exposition actif.
  - **`BGrate`** : Taux de comptage du fond (background rate).
  - **`BGerr`** : Incertitude sur le taux de comptage du fond.
  - **`CorrFact`** : Facteur de correction appliqué aux données.
  - **`CtsInSrc`** : Nombre de comptages dans la région source.
  - **`BGInSrc`** : Nombre de comptages du fond dans la région source.
  - **`Exposure`** : Temps d'exposition en secondes.
  - **`Sigma`** : Niveau de signification statistique.
  - **`SNR`** : Rapport signal/bruit (Signal-to-Noise Ratio).
  - **`SYS_NEG`** : Incertitude systématique négative.
  - **`SYS_POS`** : Incertitude systématique positive.

### **b. `WTHard_incbad` et `WTSoft_incbad`**
- **Modes :** `WT` (Windowed Timing) - sous-modes `Hard` et `Soft`
- **Colonnes :**
  - **`Time`** : Temps relatif depuis `T0`, en secondes.
  - **`TimePos`** : Incertitude positive sur le temps.
  - **`TimeNeg`** : Incertitude négative sur le temps.
  - **`Rate`** : Taux de comptage des photons (comptes par seconde).
  - **`RateErr`** : Incertitude sur le taux de comptage.
  - **`Exposure`** : Temps d'exposition en secondes.

### **c. `WTHR_incbad`**
- **Modes :** `WT` (Windowed Timing) - sous-mode `HR` (Hardness Ratio)
- **Colonnes :**
  - **`Time`** : Temps relatif depuis `T0`, en secondes.
  - **`TimePos`** : Incertitude positive sur le temps.
  - **`TimeNeg`** : Incertitude négative sur le temps.
  - **`HR`** : **Hardness Ratio** - Rapport entre les comptages dans les bandes d'énergie élevées et basses, utilisé pour évaluer la température ou l'état énergétique de la source.
  - **`HRErr`** : Incertitude sur le Hardness Ratio.
  - **`Exposure`** : Temps d'exposition en secondes.

### **d. `PC_incbad`**
- **Modes :** `PC` (Photon Counting)
- **Colonnes :**
  - **`Time`** : Temps relatif depuis `T0`, en secondes.
  - **`TimePos`** : Incertitude positive sur le temps.
  - **`TimeNeg`** : Incertitude négative sur le temps.
  - **`Rate`** : Taux de comptage des photons (comptes par seconde).
  - **`RatePos`** : Incertitude positive sur le taux de comptage.
  - **`RateNeg`** : Incertitude négative sur le taux de comptage.
  - **`FracExp`** : Fraction du temps d'exposition actif.
  - **`BGrate`** : Taux de comptage du fond (background rate).
  - **`BGerr`** : Incertitude sur le taux de comptage du fond.
  - **`CorrFact`** : Facteur de correction appliqué aux données.
  - **`CtsInSrc`** : Nombre de comptages dans la région source.
  - **`BGInSrc`** : Nombre de comptages du fond dans la région source.
  - **`Exposure`** : Temps d'exposition en secondes.
  - **`Sigma`** : Niveau de signification statistique.
  - **`SNR`** : Rapport signal/bruit (Signal-to-Noise Ratio).

### **e. `PCUL_incbad`**
- **Modes :** `PC` (Photon Counting) - sous-mode `UL` (Upper Limit)
- **Colonnes :**
  - **`Time`** : Temps relatif depuis `T0`, en secondes.
  - **`TimePos`** : Incertitude positive sur le temps.
  - **`TimeNeg`** : Incertitude négative sur le temps.
  - **`UpperLimit`** : Limite supérieure sur le taux de comptage, utilisée lorsque la source n'est pas détectée de manière significative.
  - **`RatePos`** : Incertitude positive sur le taux de comptage.
  - **`RateNeg`** : Incertitude négative sur le taux de comptage.
  - **`FracExp`** : Fraction du temps d'exposition actif.
  - **`BGrate`** : Taux de comptage du fond (background rate).
  - **`BGerr`** : Incertitude sur le taux de comptage du fond.
  - **`CorrFact`** : Facteur de correction appliqué aux données.
  - **`CtsInSrc`** : Nombre de comptages dans la région source.
  - **`BGInSrc`** : Nombre de comptages du fond dans la région source.
  - **`Exposure`** : Temps d'exposition en secondes.
  - **`Sigma`** : Niveau de signification statistique.
  - **`SNR`** : Rapport signal/bruit (Signal-to-Noise Ratio).

### **f. `PCHard_incbad` et `PCSoft_incbad`**
- **Modes :** `PC` (Photon Counting) - sous-modes `Hard` et `Soft`
- **Colonnes :**
  - **`Time`** : Temps relatif depuis `T0`, en secondes.
  - **`TimePos`** : Incertitude positive sur le temps.
  - **`TimeNeg`** : Incertitude négative sur le temps.
  - **`Rate`** : Taux de comptage des photons (comptes par seconde).
  - **`RateErr`** : Incertitude sur le taux de comptage.
  - **`Exposure`** : Temps d'exposition en secondes.

### **g. `PCHR_incbad`**
- **Modes :** `PC` (Photon Counting) - sous-mode `HR` (Hardness Ratio)
- **Colonnes :**
  - **`Time`** : Temps relatif depuis `T0`, en secondes.
  - **`TimePos`** : Incertitude positive sur le temps.
  - **`TimeNeg`** : Incertitude négative sur le temps.
  - **`HR`** : **Hardness Ratio** - Rapport entre les comptages dans les bandes d'énergie élevées et basses.
  - **`HRErr`** : Incertitude sur le Hardness Ratio.
  - **`Exposure`** : Temps d'exposition en secondes.

---

## **3. Explications des Champs Communs**

### **a. `Time`**
- **Description :**
  - **Temps Relatif** : Représente le temps écoulé depuis le **temps de référence `T0`**, exprimé en secondes. C'est l'axe des abscisses dans les courbes de lumière.

### **b. `TimePos` et `TimeNeg`**
- **Description :**
  - **Incertitudes sur le Temps** : Représentent les incertitudes positives et négatives associées à la mesure du temps. Elles indiquent la précision de la mesure temporelle.

### **c. `Rate`**
- **Description :**
  - **Taux de Comptage des Photons** : Nombre de photons détectés par seconde dans l'intervalle de temps spécifié. C'est l'axe des ordonnées dans les courbes de lumière.

### **d. `RatePos` et `RateNeg`**
- **Description :**
  - **Incertitudes sur le Taux de Comptage** : Représentent les incertitudes positives et négatives associées au taux de comptage des photons. Elles indiquent la précision de la mesure du taux.

### **e. `RateErr`**
- **Description :**
  - **Erreur sur le Taux de Comptage** : Indique l'incertitude globale (positif et négatif) sur le taux de comptage des photons.

### **f. `FracExp`**
- **Description :**
  - **Fraction d'Exposition** : Proportion du temps d'exposition actif pendant l'intervalle de temps considéré. Elle est utilisée pour corriger les variations dans le temps d'observation.

### **g. `BGrate`**
- **Description :**
  - **Taux de Comptage du Fond** : Nombre de photons détectés par seconde provenant du fond (background) dans l'intervalle de temps spécifié. Il est utilisé pour soustraire le fond du taux de comptage total.

### **h. `BGerr`**
- **Description :**
  - **Incertitude sur le Taux de Comptage du Fond** : Indique l'incertitude associée au taux de comptage du fond.

### **i. `CorrFact`**
- **Description :**
  - **Facteur de Correction** : Facteur appliqué aux données pour corriger les effets instrumentaux ou autres biais systématiques.

### **j. `CtsInSrc` et `BGInSrc`**
- **Description :**
  - **`CtsInSrc`** : Nombre de comptages détectés dans la région source d'intérêt.
  - **`BGInSrc`** : Nombre de comptages provenant du fond dans la région source. Utilisé pour soustraire le fond du total des comptages dans la source.

### **k. `Exposure`**
- **Description :**
  - **Temps d'Exposition** : Durée en secondes pendant laquelle l'instrument a collecté des données pour cet intervalle de temps spécifique.

### **l. `Sigma`**
- **Description :**
  - **Niveau de Signification** : Mesure statistique indiquant la confiance dans la détection des photons. Un sigma plus élevé indique une détection plus significative.

### **m. `SNR`**
- **Description :**
  - **Rapport Signal/Bruit (Signal-to-Noise Ratio)** : Indique la qualité de la mesure du taux de comptage. Un SNR élevé signifie que le signal est bien distinct du bruit de fond.

### **n. `SYS_NEG` et `SYS_POS`**
- **Description :**
  - **Incertitudes Systématiques** : Incertitudes négatives et positives provenant de sources systémiques, telles que des erreurs instrumentales ou des approximations dans le modèle.

### **o. `UpperLimit`**
- **Description :**
  - **Limite Supérieure** : Indique une limite supérieure sur le taux de comptage lorsqu'une détection significative n'est pas possible. Utilisé pour des intervalles de temps où la source n'est pas détectée avec suffisamment de confiance.

### **p. `HR` et `HRErr`**
- **Description :**
  - **Hardness Ratio** (`HR`) : Rapport entre les comptages dans une bande d'énergie élevée et une bande d'énergie basse. Il permet d'évaluer l'état énergétique ou la température de la source.
  - **Incertitude sur le Hardness Ratio** (`HRErr`) : Indique l'incertitude associée au calcul du Hardness Ratio.

---

## **4. Interprétation des Modes d'Observation**

### **a. `WT` (Windowed Timing)**
- **Description :**
  - **Mode de Temporisation par Fenêtre** : Offre une meilleure résolution temporelle au détriment d'une résolution spectrale légèrement réduite. Idéal pour observer des variations rapides dans les sources X-ray.

### **b. `PC` (Photon Counting)**
- **Description :**
  - **Mode de Comptage de Photons** : Fournit une meilleure résolution spectrale mais une résolution temporelle inférieure par rapport au mode `WT`. Utilisé pour des observations nécessitant une précision spectrale élevée.

### **c. Sous-Modes**
- **`Hard` et `Soft`** :
  - **Hard** : Se réfère généralement aux photons dans une bande d'énergie plus élevée.
  - **Soft** : Se réfère aux photons dans une bande d'énergie plus basse.
- **`HR`** :
  - **Hardness Ratio** : Utilisé pour analyser la distribution d'énergie des photons détectés.

---

# II. Spectra

## **1. Champs Générales**

### **a. `T0` : 314995072**
- **Description :** 
  - Il s'agit probablement d'un **timestamp** ou d'une **référence temporelle** utilisée comme point de départ pour les analyses ou les calculs ultérieurs. Ce nombre représente généralement le nombre de secondes ou de millisecondes écoulées depuis une date de référence (comme le 1er janvier 1970 pour les timestamps Unix).

### **b. `DeltaFitStat` : 2.706**
- **Description :**
  - **Delta Fit Statistic** : C'est une mesure de l'amélioration ou de la dégradation de la qualité de l'ajustement du modèle par rapport à un modèle précédent ou à une condition de base. Une valeur positive indique généralement une amélioration, tandis qu'une valeur négative indique une dégradation de l'ajustement.

### **c. `rnames` : ['interval0', 'late_time']**
- **Description :**
  - **Region Names** ou **Run Names** : Ce sont les **noms des différentes régions temporelles** ou segments de l'observation qui ont été analysés séparément. Dans ce cas, il y a deux régions :
    - **`interval0`** : La première intervalle d'observation.
    - **`late_time`** : Une seconde intervalle d'observation se situant probablement à une phase plus tardive de l'événement observé.

---

## **2. Détails par Région Temporelle**

Chaque région temporelle (`interval0`, `late_time`) contient plusieurs champs détaillant les données et les modèles utilisés pour l'analyse spectrale.

### **a. `DataFile`**
- **Description :**
  - **URL vers les fichiers de données** : C'est le **lien de téléchargement** des données brutes ou traitées pour cette région temporelle spécifique.
  - **Exemple :** 
    - `https://www.swift.ac.uk/xrt_spectra/00441015/interval0.tar.gz`

### **b. `Start` et `Stop`**
- **Description :**
  - **Start** : **Temps de début** de la région temporelle analysée, exprimé en secondes depuis un temps de référence.
  - **Stop** : **Temps de fin** de la région temporelle analysée.
  - **Exemple :**
    - `Start`: 1389.1578540206 secondes
    - `Stop`: 190027.391951978 secondes

### **c. `Modes` : ['WT', 'PC'] ou ['PC']**
- **Description :**
  - **Modes d'Observation** : Les différents **mode de fonctionnement** de l'instrument XRT durant l'observation.
    - **WT (Windowed Timing)** : Mode de temporisation par fenêtre, utilisé pour obtenir une meilleure résolution temporelle tout en maintenant une résolution spectrale raisonnable.
    - **PC (Photon Counting)** : Mode de comptage de photons, offrant une meilleure résolution spectrale mais une résolution temporelle inférieure.

### **d. Modes Spécifiques (`WT`, `PC`)**
Chaque mode contient des informations sur les **modèles spectrales** utilisés et leurs **paramètres de fit**.

#### **i. `Models` : ['PowerLaw']**
- **Description :**
  - **Modèles Spectrales Utilisés** : Liste des modèles spectrales appliqués pour ajuster les données. Ici, seul le modèle **PowerLaw** est utilisé.

#### **ii. `PowerLaw`**
- **Description :**
  - **Modèle PowerLaw** : Un modèle couramment utilisé en astrophysique pour décrire la distribution d'énergie des photons. Il est défini par une loi de puissance, caractérisée par un indice de puissance (`Gamma`).

##### **Paramètres du Modèle PowerLaw :**

1. **`GalacticNH` : 1.074411e+21**
   - **Description :**
     - **Colonisation de l'hydrogène neutre galactique** (`Galactic Neutral Hydrogen Column Density`) en cm⁻². Représente la densité de matière interstellaire entre la source et l'observateur dans notre galaxie.

2. **`NH` : 2.918439622e+21**
   - **Description :**
     - **Colonisation de l'hydrogène neutre intrinsèque** (`Intrinsic Neutral Hydrogen Column Density`) en cm⁻². Représente la densité de matière au niveau de la source ou dans la galaxie hôte de l'objet observé.

3. **`NHPos` : 2.7513307600000038e+20** & **`NHNeg` : -2.647083119999999e+20**
   - **Description :**
     - **Incertitudes sur `NH`** : Les erreurs positives et négatives associées à la valeur de `NH`.

4. **`Redshift_abs` : 0.847**
   - **Description :**
     - **Décalage vers le rouge absolu** (`Absolute Redshift`). Indique l'éloignement cosmologique de l'objet observé, affectant la longueur d'onde des photons reçus.

5. **`Gamma` : 1.643419493** & **`GammaPos` : 0.01842260200000001** & **`GammaNeg` : -0.018219364999999987**
   - **Description :**
     - **Indice de puissance** (`Photon Index`). Décrit la pente de la loi de puissance. Les incertitudes associées sont indiquées par `GammaPos` et `GammaNeg`.

6. **`ObsFlux` : 7.610325459576917e-10** & **`ObsFluxPos` : 9.501175797100376e-12** & **`ObsFluxNeg` : -9.429078522841411e-12**
   - **Description :**
     - **Flux Observé** (`Observed Flux`) en erg cm⁻² s⁻¹. Représente le flux mesuré directement depuis l'objet observé.
     - **Incertitudes** : Erreurs positives et négatives sur le flux observé.

7. **`UnabsFlux` : 9.08915301940309e-10** & **`UnabsFluxPos` : 8.858758869499253e-12** & **`UnabsFluxNeg` : -8.801270001682984e-12**
   - **Description :**
     - **Flux Non Absorbé** (`Unabsorbed Flux`) en erg cm⁻² s⁻¹. Représente le flux théorique si aucune absorption n'était présente le long de la ligne de visée.
     - **Incertitudes** : Erreurs positives et négatives sur le flux non absorbé.

8. **`Cstat` : 935.4102634**
   - **Description :**
     - **Statistique C** (`C-Statistic`). Une mesure de la qualité de l'ajustement du modèle aux données, particulièrement adaptée aux données de faible comptage.

9. **`Dof` : 856**
   - **Description :**
     - **Degrés de liberté** (`Degrees of Freedom`). Nombre de points de données moins le nombre de paramètres ajustés.

10. **`FitChi` : 995.7730869**
    - **Description :**
      - **Chi carré du fit** (`Chi-squared Fit`). Une autre mesure de la qualité de l'ajustement, principalement utilisée lorsque les conditions pour son application sont remplies (comme des données avec comptages suffisants).

11. **`Image` : 'https://www.swift.ac.uk/xrt_spectra/00441015/interval0wt_plot.gif'**
    - **Description :**
      - **Lien vers l'image du spectre ajusté**. Permet de visualiser graphiquement l'ajustement du modèle aux données observées.

12. **`Exposure` : 2690.77328449488**
    - **Description :**
      - **Temps d'exposition** en secondes. Durée pendant laquelle l'instrument a collecté des données pour cette région temporelle et ce mode.

13. **`MeanTime` : 4452.85550957918**
    - **Description :**
      - **Temps moyen** en secondes. Point central temporel de l'observation pour cette région et ce mode.

### **iii. Mode PC (Photon Counting)**
- **Description :**
  - Similaire au mode WT, mais généralement avec une résolution spectrale meilleure et une résolution temporelle inférieure.
  - Les paramètres sont analogues à ceux décrits pour le mode WT.

---

## **3. Interprétation Globale des Champs**

### **a. `interval0`**
- **Description :**
  - **Première région temporelle** de l'observation.
  - **Modes** : WT et PC.
  - **Modèles** : PowerLaw pour les deux modes.
  - **Paramètres** : Les valeurs des paramètres spectrales (NH, Gamma, Flux, etc.) sont ajustées séparément pour chaque mode.

### **b. `late_time`**
- **Description :**
  - **Deuxième région temporelle**, probablement une phase plus tardive de l'événement observé.
  - **Modes** : Uniquement PC.
  - **Modèles** : PowerLaw.
  - **Paramètres** : Ajustements similaires à ceux de `interval0` en mode PC.

---
