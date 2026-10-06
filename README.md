# BETON INSIGHT PRO

BETON INSIGHT PRO est une application académique développée avec Python et Streamlit pour l'analyse statistique, probabiliste et prédictive des résistances du béton à 28 jours.

## Objectif

L'application permet d'exploiter les résultats d'essais de résistance du béton afin de :

- calculer les principales statistiques descriptives ;
- comparer les résistances à un seuil de référence ;
- estimer des probabilités sous hypothèse de normalité ;
- étudier les corrélations entre certaines variables ;
- réaliser des régressions linéaires simples ;
- réaliser une régression linéaire multiple ;
- effectuer une simulation prédictive ;
- exporter les résultats sous forme de rapport et de fichier CSV.

## Fonctionnalités

### Vue d'ensemble
Affichage des principaux indicateurs :
- nombre d'essais ;
- résistance moyenne ;
- taux de valeurs supérieures ou égales au seuil ;
- risque estimé de résistance sous le seuil.

### Données
- saisie manuelle des résistances ;
- import de fichiers Excel ou CSV ;
- affichage du tableau des essais.

### Statistiques
Calcul de :
- moyenne ;
- médiane ;
- variance ;
- écart-type ;
- coefficient de variation ;
- minimum ;
- maximum.

### Analyse probabiliste
Estimation de :

P(R >= seuil)

et

P(R < seuil)

sous hypothèse de distribution normale.

### Modélisation
Étude de la relation entre :
- le rapport eau/ciment ;
- le dosage en ciment ;
- la résistance du béton à 28 jours.

L'application propose :
- une régression simple sur le rapport E/C ;
- une régression simple sur le dosage en ciment ;
- une régression linéaire multiple.

### Simulateur
Le simulateur permet d'estimer une résistance à partir :
- du rapport eau/ciment ;
- du dosage en ciment.

### Rapport
L'application permet d'exporter :
- un rapport texte ;
- les résultats au format CSV.

## Technologies utilisées

- Python
- Streamlit
- Pandas
- NumPy
- Matplotlib
- OpenPyXL

## Lancement local

Dans le terminal, exécuter :

```bash
streamlit run app.py