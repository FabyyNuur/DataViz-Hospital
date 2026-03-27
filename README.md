# DataViz-Hospital

Projet d'analyse de données hospitalières avec visualisations interactives Plotly, interprétations et génération automatique de rapport depuis un notebook Jupyter.

## Objectifs

- Charger et préparer un jeu de données hospitalier.
- Produire des visualisations claires (distribution, répartitions, comparaisons).
- Ajouter des interprétations automatiques pour faciliter la lecture des résultats.
- Exporter un notebook en rapport HTML présentable.

## Aperçu du projet

Le projet contient deux axes principaux :

- Analyse et visualisation dans le notebook principal.
- Génération de rapport à partir d'un notebook exécuté.

Données source : `hospital_data.csv`

Principales colonnes détectées :

- PatientID
- Age
- Sexe
- Departement
- Maladie
- DureeSejour
- Cout
- DateAdmission
- DateSortie
- Traitement

## Structure

```text
DataViz-hospital/
  generate.ipynb
  viz_hospital.ipynb
  hospital_data.csv
  rapport_hospital.html
  hospital_analysis/
    __init__.py
    chargement.py
    visualisations.py
    interpretations.py
  genere_rapport/
    _init_.py
    notebook_to_rapport.py
```

## Prérequis

- Python 3.10+
- Jupyter Notebook
- Environnement virtuel Python (recommandé)

Bibliothèques utilisées :

- pandas
- numpy
- plotly
- scikit-learn
- nbformat
- nbconvert
- beautifulsoup4
- ipython

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install pandas numpy plotly scikit-learn nbformat nbconvert beautifulsoup4 ipython jupyter
```

## Utilisation

### 1) Exécuter l'analyse dans le notebook

```bash
source .venv/bin/activate
jupyter notebook
```

Ouvrir ensuite `viz_hospital.ipynb` et exécuter les cellules.

### 2) Générer un rapport HTML depuis un notebook

Le module `genere_rapport/notebook_to_rapport.py` expose la fonction `notebook_to_html_plotly(notebook_path, output_directory='.')`.

Exemple :

```bash
python - << 'PY'
from genere_rapport.notebook_to_rapport import notebook_to_html_plotly

output = notebook_to_html_plotly('viz_hospital.ipynb', '.')
print(f'Rapport genere : {output}')
PY
```

## Modules Python

### hospital_analysis

- `chargement.py` : chargement du CSV (séparateur `;`) et configuration du renderer Plotly.
- `visualisations.py` : fonctions génériques (histogramme, barres, camembert, boxplot, nuage de points) + raccourcis métier prêts à l'emploi.
- `interpretations.py` : génération de blocs d'interprétation HTML stylisés dans le notebook.

### genere_rapport

- `notebook_to_rapport.py` :
  - exécute le notebook;
  - conserve les sorties et graphiques Plotly;
  - extrait une page de garde;
  - applique un style CSS;
  - exporte un rapport HTML final.

## Sorties

- Notebook d'analyse : `viz_hospital.ipynb`
- Rapport HTML généré : `rapport_hospital.html` (ou autre chemin selon paramètre de sortie)

## Bonnes pratiques recommandées

- Garder `hospital_data.csv` avec un séparateur `;` pour conserver la compatibilité avec le chargeur.
- Exécuter toutes les cellules avant export HTML pour garantir un rapport complet.
- Versionner le code source et, selon le besoin, versionner ou non les rapports HTML générés.

## Auteur

FabyyNuur - uicode.byfatoubintg@gmail.com
