import pandas as pd
from IPython.display import display, HTML

_STYLE_DIV = (
    "margin-top:14px; padding:16px 18px; border-left:6px solid #1f5a7a; "
    "background:linear-gradient(135deg, #f7fbff 0%, #eef6fb 100%); "
    "border-radius:12px; color:#10222f; box-shadow:0 6px 16px rgba(21, 52, 72, 0.10); "
    "font-family:'Segoe UI', Tahoma, sans-serif; line-height:1.55;"
)
_STYLE_H3 = "margin:0 0 10px 0; color:#174964; font-size:1.05rem; letter-spacing:0.2px;"
_STYLE_P = "margin:8px 0; color:#163447;"


def _afficher(html: str) -> None:
    display(HTML(html))


def render_interpretation(
    paragraphs: list[str],
    title: str = "Interprétation",
    container_style: str = _STYLE_DIV,
    title_style: str = _STYLE_H3,
    paragraph_style: str = _STYLE_P,
) -> None:
    """
    Affiche un bloc d'interprétation réutilisable.

    Parameters
    ----------
    paragraphs : list[str]
        Liste des paragraphes HTML à afficher.
    title : str
        Titre du bloc.
    container_style : str
        Style inline du conteneur principal.
    title_style : str
        Style inline du titre.
    paragraph_style : str
        Style inline des paragraphes.
    """
    paragraphs_html = "".join(
        f'<p style="{paragraph_style}">{paragraph}</p>' for paragraph in paragraphs
    )
    title_html = f'<h3 style="{title_style}">{title}</h3>' if title else ""
    html = f"""
<div style="{container_style}">
  {title_html}
  {paragraphs_html}
</div>
"""
    _afficher(html)


def interp_maladies(df: pd.DataFrame) -> None:
    data = df["Maladie"].value_counts().reset_index()
    data.columns = ["Maladie", "Nombre de cas"]
    total = int(data["Nombre de cas"].sum())
    top1_nom = data.iloc[0]["Maladie"]
    top1_nb = int(data.iloc[0]["Nombre de cas"])
    top1_pct = (top1_nb / total * 100) if total else 0
    top3_nb = int(data.head(3)["Nombre de cas"].sum())
    top3_pct = (top3_nb / total * 100) if total else 0

    paragraphs = [
        (
            f"La maladie la plus fréquente est <b>{top1_nom}</b> avec <b>{top1_nb}</b> cas, "
            f"soit <b>{top1_pct:.1f}%</b> de l'ensemble des cas."
        ),
        (
            f"Les 3 maladies les plus représentées cumulent <b>{top3_nb}</b> cas, "
            f"soit <b>{top3_pct:.1f}%</b> du total."
        ),
        (
            "Il existe une hyper-concentration de l'activité sur un nombre limité de maladies. "
            "Cela peut constituer un avantage pour prioriser l'allocation des ressources médicales."
        ),
    ]
    render_interpretation(paragraphs)


def interp_box_departement(df: pd.DataFrame) -> None:
    stats = (
        df.groupby("Departement")["DureeSejour"]
        .agg(
            mediane="median",
            q1=lambda s: s.quantile(0.25),
            q3=lambda s: s.quantile(0.75),
        )
    )
    stats["iqr"] = stats["q3"] - stats["q1"]
    stats = stats.sort_values("mediane", ascending=False)

    dept_long = stats.index[0]
    med_long = stats.iloc[0]["mediane"]
    dept_court = stats.index[-1]
    med_court = stats.iloc[-1]["mediane"]
    dept_variable = stats["iqr"].idxmax()
    iqr_max = stats["iqr"].max()

    paragraphs = [
        (
            f"Dans le département <b>{dept_long}</b>, la durée habituelle de séjour est la plus élevée : "
            f"<b>{med_long:.0f}</b> jours (valeur exacte : {med_long})."
        ),
        (
            f"À l'inverse, dans <b>{dept_court}</b>, la durée habituelle de séjour est la plus courte : "
            f"<b>{med_court:.0f}</b> jours (valeur exacte : {med_court})."
        ),
        (
            f"Le département <b>{dept_variable}</b> présente les écarts de durée les plus marqués "
            f"(écart central = <b>{iqr_max:.0f}</b> jours, valeur exacte : {iqr_max}), "
            "ce qui signifie que les séjours y sont moins homogènes d'un patient à l'autre."
        ),
    ]
    render_interpretation(paragraphs)


def interp_duree_moyenne(df: pd.DataFrame) -> None:
    duree = df["DureeSejour"].mean()
    paragraphs = [
        (
            f"La durée habituelle d'un séjour est de <b>{duree:.0f}</b> jours "
            f"<span style=\"color:#555;\">(valeur exacte : {duree})</span>."
        )
    ]
    render_interpretation(paragraphs, title="")
