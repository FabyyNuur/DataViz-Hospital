from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert import HTMLExporter
import nbformat
import os
import copy
from bs4 import BeautifulSoup, Comment

# import nbformat
import asyncio
import platform



def remove_html_comments(html_content):
    """
    Fonction pour supprimer les commentaires HTML du contenu.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    for comment in comments:
        comment.extract()
    return str(soup)



def get_custom_css():
    """
    Retourne le CSS personnalisé avec le thème bleu/orange du notebook.
    """
    return """
    <style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        line-height: 1.7;
        color: #2c3e50;
        background-color: #f5f7fa;
    }

    .cover-page {
        min-height: 100svh;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 40px 30px;
        background-color: #ffffff;
    }

    .cover-content {
        width: 100%;
        max-width: 1100px;
        min-height: calc(100svh - 80px);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
    }

    .cover-content > * {
        width: 100%;
        max-width: 900px;
        margin-left: auto;
        margin-right: auto;
    }

    .page-break {
        break-after: page;
        page-break-after: always;
    }

    .main-content {
        max-width: 1200px;
        margin: 0 auto;
        padding: 40px 30px;
        background-color: white;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #125481;
        margin-top: 35px;
        margin-bottom: 20px;
        font-weight: 600;
    }

    h1 {
        font-size: 2.5em;
        padding-bottom: 15px;
        margin-bottom: 35px;
    }

    h2 {
        font-size: 2em;
        padding-left: 15px;
    }

    h3 {
        font-size: 1.5em;
        color: #2c3e50;
        padding-left: 12px;
    }

    h4, h5, h6 {
        font-size: 1.1em;
        color: #34495e;
    }

    hr {
        width: 50%;
        margin: 12px auto;
        border: 0;
        border-top: 1px solid #bdc3c7;
    }

    p {
        margin: 15px 0;
        line-height: 1.8;
        color: #555;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        margin: 25px 0;
        box-shadow: 0 2px 8px rgba(18, 84, 129, 0.1);
        border-radius: 6px;
        overflow: hidden;
    }

    table thead {
        background-color: #125481;
        color: white;
    }

    table th {
        padding: 14px 16px;
        text-align: left;
        font-weight: 600;
        font-size: 0.95em;
    }

    table td {
        padding: 12px 16px;
        border-bottom: 1px solid #ecf0f1;
    }

    table tbody tr:hover {
        background-color: #f8fafb;
    }

    table tbody tr:nth-child(even) {
        background-color: #fafbfc;
    }

    .output_png, .output_jpeg, .output_svg, img {
        max-width: 100%;
        height: auto;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(18, 84, 129, 0.12);
        margin: 25px 0;
        border: 1px solid #ecf0f1;
    }

    .output {
        background-color: #f8fafb;
        border-left: 0.5px solid #df8116;
        padding: 16px 20px;
        margin: 20px 0;
        border-radius: 4px;
    }

    /* Texte monospace (code, résultats) */
    pre, code {
        background-color: #2c3e50;
        color: #ecf0f1;
        padding: 2px 6px;
        border-radius: 4px;
        font-family: 'Monaco', 'Courier New', monospace;
        font-size: 0.9em;
    }

    pre {
        padding: 16px;
        margin: 20px 0;
        overflow-x: auto;
        line-height: 1.5;
    }

    .interpretation {
        background-color: #f7fbff;
        border-left: 5px solid #125481;
        padding: 16px 20px;
        margin: 20px 0;
        border-radius: 4px;
        color: #2c3e50;
    }

    @media (max-width: 768px) {
        .main-content {
            padding: 20px 15px;
        }

        .cover-page {
            min-height: auto;
            padding: 20px 15px;
        }

        .cover-content {
            min-height: auto;
            align-items: center;
            justify-content: center;
            text-align: center;
        }

        h1 {
            font-size: 1.8em;
        }

        h2 {
            font-size: 1.5em;
        }

        h3 {
            font-size: 1.2em;
        }

        table {
            font-size: 0.9em;
        }

        table th, table td {
            padding: 10px 12px;
        }
    }

    @media print {
        html, body {
            height: 100%;
        }

        .cover-page {
            min-height: calc(100vh - 2cm);
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 0 20mm;
            page-break-after: always;
        }

        .cover-content {
            min-height: auto;
            width: 100%;
            align-items: center;
            justify-content: center;
            text-align: center;
        }
    }
    </style>
    """


def format_html_report(html_content, cover_html=""):
    """
    Formate le contenu HTML du rapport avec le thème bleu/orange.

    Parameters:
    html_content (str): Contenu HTML du notebook.

    Returns:
    str: Contenu HTML formaté sans table des matières.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = str(soup.body.decode_contents()) if soup.body else str(soup)

    # Construire le HTML final
    cover_section = ""
    if cover_html.strip():
        cover_section = f"""
        <section class="cover-page">
            <div class="cover-content">
                {cover_html}
            </div>
        </section>
        <div class="page-break"></div>
        """

    final_html = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Rapport d'Analyse Hospitalière</title>
        {get_custom_css()}
    </head>
    <body>
        {cover_section}
        <div class="main-content">
            {body_content}
        </div>
    </body>
    </html>
    """

    return final_html


if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())



def notebook_to_html_plotly(notebook_path, output_directory="."):
    """
    Convertit un fichier Jupyter Notebook en HTML, en exécutant toutes les cellules,
    tout en conservant les graphiques Plotly interactifs dans le rapport final.

    Paramètres
    ----------
    notebook_path : str
        Chemin vers le fichier Jupyter Notebook (.ipynb).
    output_directory : str
        Répertoire où enregistrer le fichier HTML (par défaut : répertoire courant).

    Retour
    ------
    str
        Chemin vers le fichier HTML créé.
    """

    # 1. Normaliser le chemin du notebook et lire son contenu
    notebook_path = os.path.abspath(notebook_path)
    with open(notebook_path, "r", encoding="utf-8") as f:
        notebook_content = f.read()

    # 2. Charger le notebook au format nbformat
    notebook = nbformat.reads(notebook_content, as_version=4)

    # 3. Construire la page de garde a partir des cellules 2 et 3.
    # Les cellules sont indexees en base 1 dans la demande utilisateur.
    cover_cells = [2, 3]
    cover_blocks = []
    for idx in cover_cells:
        if 1 <= idx <= len(notebook.cells):
            cell = notebook.cells[idx - 1]
            if cell.get("cell_type") == "markdown":
                source = cell.get("source", "")
                if isinstance(source, list):
                    source = "\n".join(source)
                cover_blocks.append(source)

    cover_html = "\n".join(block for block in cover_blocks if str(block).strip())


    notebook_dir = os.path.dirname(notebook_path)
    executor = ExecutePreprocessor(timeout=-1, allow_errors=False)
    executor.preprocess(notebook, resources={"metadata": {"path": notebook_dir}})


    notebook_for_export = copy.deepcopy(notebook)
    notebook_for_export.cells = [
        c for i, c in enumerate(notebook_for_export.cells, start=1) if i not in cover_cells
    ]

    html_exporter = HTMLExporter(template_name="classic")
    html_exporter.exclude_input = True  # Masquer le code
    html_exporter.exclude_input_prompt = True  # Masquer "In[x]"
    html_exporter.exclude_output_prompt = True  # Masquer "Out[x]"
    # IMPORTANT: Ne pas mettre "html_exporter.exclude_output = True"
    #            sinon les graphiques ne s'afficheront pas.

    # Passer 'embed_widgets': True dans resources
    resources = {"embed_widgets": True}

    (body, _) = html_exporter.from_notebook_node(notebook_for_export, resources=resources)

    body = remove_html_comments(body)

    body = format_html_report(body, cover_html=cover_html)


    notebook_name = os.path.splitext(os.path.basename(notebook_path))[0]
    output_directory = os.path.abspath(output_directory)

    if output_directory.lower().endswith(".html"):
        os.makedirs(os.path.dirname(output_directory), exist_ok=True)
        html_file_path = output_directory
    else:
        os.makedirs(output_directory, exist_ok=True)
        html_file_path = os.path.join(output_directory, f"{notebook_name}.html")

    with open(html_file_path, "w", encoding="utf-8") as f:
        f.write(body)

    return html_file_path
