from .chargement import charger_donnees
from .visualisations import (
    histogramme,
    camembert,
    barres,
    boite,
    nuage_points,
    fig_distribution_age,
    fig_repartition_sexe,
    fig_patients_par_departement,
    fig_maladies_frequentes,
    fig_box_duree_par_departement,
    fig_duree_par_maladie,
    fig_repartition_traitements,
    fig_scatter_age_duree,
)
from .interpretations import (
    render_interpretation,
    interp_maladies,
    interp_box_departement,
    interp_duree_moyenne,
)

__all__ = [
    "charger_donnees",
    "histogramme",
    "camembert",
    "barres",
    "boite",
    "nuage_points",
    "fig_distribution_age",
    "fig_repartition_sexe",
    "fig_patients_par_departement",
    "fig_maladies_frequentes",
    "fig_box_duree_par_departement",
    "fig_duree_par_maladie",
    "fig_repartition_traitements",
    "fig_scatter_age_duree",
    "render_interpretation",
    "interp_maladies",
    "interp_box_departement",
    "interp_duree_moyenne",
]
