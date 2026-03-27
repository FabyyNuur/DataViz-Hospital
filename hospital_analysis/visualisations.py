import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def histogramme(
    df: pd.DataFrame,
    x: str,
    titre: str = "",
    labels: dict = None,
    couleur: str = "#df8116",
    nbins: int = 20,
    titre_y: str = "Effectif",
    bargap: float = 0.1,
) -> go.Figure:
    fig = px.histogram(
        df,
        x=x,
        nbins=nbins,
        title=titre,
        labels=labels or {},
        color_discrete_sequence=[couleur],
    )
    fig.update_layout(yaxis_title=titre_y, showlegend=False, bargap=bargap)
    return fig


def camembert(
    df: pd.DataFrame,
    noms: str,
    titre: str = "",
    couleurs: dict | list | None = None,
    trou: float = 0.4,
    position_texte: str = "inside",
    taille_texte: int = 15,
) -> go.Figure:
    kwargs = dict(names=noms, title=titre, hole=trou)
    if isinstance(couleurs, dict):
        kwargs["color"] = noms
        kwargs["color_discrete_map"] = couleurs
    elif isinstance(couleurs, list):
        kwargs["color_discrete_sequence"] = couleurs
    fig = px.pie(df, **kwargs)
    fig.update_traces(
        textposition=position_texte,
        textinfo="percent+label",
        textfont_size=taille_texte,
    )
    return fig


def barres(
    df: pd.DataFrame,
    x: str,
    y: str,
    titre: str = "",
    labels: dict = None,
    couleur: str | None = None,
    couleur_col: str | None = None,
    echelle_couleur: str | None = None,
    orientation: str = "v",
    texte: str | bool | None = None,
    tri_y: str | None = None,
    titre_x: str = "",
    titre_y: str = "",
) -> go.Figure:
    kwargs = dict(
        x=x,
        y=y,
        title=titre,
        labels=labels or {},
        orientation=orientation,
    )
    if couleur_col and echelle_couleur:
        kwargs["color"] = couleur_col
        kwargs["color_continuous_scale"] = echelle_couleur
    elif couleur:
        kwargs["color_discrete_sequence"] = [couleur]
    if texte is not None:
        kwargs["text"] = texte if isinstance(texte, str) else None
        if isinstance(texte, bool) and texte:
            kwargs["text_auto"] = ".2f"
    fig = px.bar(df, **kwargs)
    layout = dict(showlegend=False)
    if titre_x:
        layout["xaxis_title"] = titre_x
    if titre_y:
        layout["yaxis_title"] = titre_y
    if tri_y:
        layout["yaxis"] = {"categoryorder": tri_y}
    fig.update_layout(**layout)
    return fig


def boite(
    df: pd.DataFrame,
    x: str,
    y: str,
    titre: str = "",
    labels: dict = None,
    couleur_col: str | None = None,
    titre_x: str = "",
    titre_y: str = "",
) -> go.Figure:
    fig = px.box(
        df,
        x=x,
        y=y,
        color=couleur_col,
        title=titre,
        labels=labels or {},
    )
    fig.update_layout(
        xaxis_title=titre_x,
        yaxis_title=titre_y,
        showlegend=False,
    )
    return fig


def nuage_points(
    df: pd.DataFrame,
    x: str,
    y: str,
    titre: str = "",
    labels: dict = None,
    couleur_col: str | None = None,
    opacite: float = 0.7,
    titre_x: str = "",
    titre_y: str = "",
) -> go.Figure:
    fig = px.scatter(
        df,
        x=x,
        y=y,
        color=couleur_col,
        opacity=opacite,
        title=titre,
        labels=labels or {},
    )
    fig.update_layout(xaxis_title=titre_x, yaxis_title=titre_y)
    return fig


# ---------------------------------------------------------------------------
# Raccourcis prêts à l'emploi pour le TP hospitalier
# ---------------------------------------------------------------------------

def fig_distribution_age(df: pd.DataFrame, nbins: int = 20) -> go.Figure:
    return histogramme(
        df, x="Age", nbins=nbins,
        titre="Distribution de l'âge des patients",
        labels={"Age": "Âge du patient"},
        couleur="#df8116",
        titre_y="Nombre de patients",
    )


def fig_repartition_sexe(df: pd.DataFrame) -> go.Figure:
    return camembert(
        df, noms="Sexe",
        titre="Répartition des patients selon le sexe",
        couleurs={"M": "#125481", "F": "#ec7f26"},
    )


def fig_patients_par_departement(df: pd.DataFrame) -> go.Figure:
    data = df["Departement"].value_counts().reset_index(name="Nombre")
    return barres(
        data, x="Departement", y="Nombre",
        titre="Nombre de patients par département",
        labels={"Nombre": "Nombre de patients", "Departement": "Département"},
        couleur="#125481",
        titre_x="Département", titre_y="Nombre de patients",
    )


def fig_maladies_frequentes(df: pd.DataFrame) -> go.Figure:
    data = df["Maladie"].value_counts().reset_index()
    data.columns = ["Maladie", "Nombre de cas"]
    return barres(
        data, x="Nombre de cas", y="Maladie",
        orientation="h",
        titre="Maladies les plus fréquentes chez les patients",
        couleur_col="Nombre de cas", echelle_couleur="Blues",
        texte="Nombre de cas",
        tri_y="total ascending",
        titre_x="Nombre de cas", titre_y="Maladie",
    )


def fig_box_duree_par_departement(df: pd.DataFrame) -> go.Figure:
    return boite(
        df, x="Departement", y="DureeSejour",
        titre="Répartition de la durée de séjour par département",
        labels={"DureeSejour": "Durée de séjour (jours)", "Departement": "Département"},
        couleur_col="Departement",
        titre_x="Département", titre_y="Durée de séjour (jours)",
    )


def fig_duree_par_maladie(df: pd.DataFrame) -> go.Figure:
    data = (
        df.groupby("Maladie")["DureeSejour"]
        .mean()
        .reset_index()
        .sort_values(by="DureeSejour", ascending=True)
    )
    return barres(
        data, x="DureeSejour", y="Maladie",
        orientation="h",
        titre="Durée moyenne de séjour selon la maladie",
        labels={"DureeSejour": "Durée moyenne (jours)", "Maladie": "Maladie"},
        couleur_col="DureeSejour", echelle_couleur="Oranges",
        texte=True,
    )


def fig_repartition_traitements(df: pd.DataFrame) -> go.Figure:
    return camembert(
        df, noms="Traitement",
        titre="Répartition des différents types de traitements",
        couleurs=px.colors.qualitative.Set2,
        position_texte="outside",
    )


def fig_scatter_age_duree(df: pd.DataFrame) -> go.Figure:
    return nuage_points(
        df, x="Age", y="DureeSejour",
        titre="Relation entre l'âge et la durée de séjour",
        labels={"Age": "Âge", "DureeSejour": "Durée de séjour (jours)"},
        couleur_col="Maladie",
        titre_x="Âge du patient", titre_y="Durée de séjour (jours)",
    )
