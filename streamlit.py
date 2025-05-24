import streamlit as st
import re
import os
import glob

# Changement du répertoire de travail (spécifique à l'environnement de l'utilisateur)
os.chdir(r"D:\Téléchargements\Privé_ Exercices pour l'entretien du Stage Assistant Gestion Multi Asset")

# --- CONFIGURATION DES STYLES ---
STYLE_CONFIG = {
    "page_layout_cols": [1, 5, 1],  # Ratios pour marge_gauche, contenu_principal, marge_droite
    "titles": {
        1: {"text-align": "center", "text-decoration": "underline", "font-size": "2.4em", "margin-top": "20px", "margin-bottom": "30px"},
        2: {"text-align": "center", "text-decoration": "underline", "font-size": "1.7em", "margin-top": "40px", "margin-bottom": "25px"},
        3: {"text-align": "center", "text-decoration": "underline", "font-size": "1.2em", "margin-top": "30px", "margin-bottom": "20px"},
        "prediction_box_title": {"text-align": "center", "text-decoration": "underline", "margin-bottom": "10px", "color": "white", "font-size": "1.1em"},
    },
    "text": {
        "body_justify": {"text-align": "justify", "margin-bottom": "1em", "line-height": "1.6"}, # Modifié pour alignement justifié
        "ia_span_color": "darkgrey",
        "prediction_box_content": {"text-align": "justify", "color": "#CCC", "flex-grow": "1", "line-height": "1.6"}, # Modifié pour alignement justifié
        "list_justify": {"text-align": "justify", "list-style-position": "outside", "padding-left": "20px", "margin-bottom": "1em", "line-height": "1.6"}, # Modifié pour alignement justifié
    },
    "images": {
        "gallery_cols_count": 3,
    },
    "prediction_box_container": {
        "border": "1px solid #444", 
        "border-radius": "5px", 
        "padding": "15px", 
        "margin-bottom": "15px", 
        "background-color": "#1E1E1E", 
        "height": "100%", 
        "display": "flex", 
        "flex-direction": "column"
    }
}

# --- FONCTION POUR CONSTRUIRE LA CHAÎNE DE STYLE CSS ---
def build_style_string(style_dict):
    return "; ".join([f"{key}: {value}" for key, value in style_dict.items()])

# --- FONCTION POUR AFFICHER LE RÉSUMÉ FORMATÉ ---
def display_formatted_summary_v5(text_with_guillemets):
    color_ia_text = STYLE_CONFIG["text"]["ia_span_color"]
    # Utilisation du style aligné justifié pour le corps du résumé
    p_style = build_style_string(STYLE_CONFIG["text"]["body_justify"]) 
    
    paragraphs_raw = re.split(r'\n\s*\n', text_with_guillemets.strip())
    html_paragraphs = []
    for para_text_raw in paragraphs_raw:
        if not para_text_raw.strip():
            continue
        para_text = re.sub(r'\s*\n\s*', ' ', para_text_raw).strip()
        para_text = re.sub(r'\s+', ' ', para_text) 
        paragraph_html_content = ""
        last_index = 0
        for match in re.finditer(r'«(.*?)»', para_text, flags=re.DOTALL):
            start_match, end_match = match.span()
            ia_content = match.group(1).strip() 
            if start_match > last_index:
                human_part_before = para_text[last_index:start_match]
                paragraph_html_content += human_part_before 
            if ia_content: 
                paragraph_html_content += f'<span style="color: {color_ia_text};">{ia_content}</span>'
            else: 
                paragraph_html_content += para_text[start_match:end_match]
            last_index = end_match
        if last_index < len(para_text):
            paragraph_html_content += para_text[last_index:]
        if paragraph_html_content.strip():
            html_paragraphs.append(f'<p style="{p_style}">{paragraph_html_content}</p>')
    final_html = "".join(html_paragraphs)
    st.markdown(final_html, unsafe_allow_html=True)

# --- TEXTE DU RÉSUMÉ ---
summary_text_updated = """Le document fourni pour cet exercice intitulé America First est issu du service de recherche Cross-Asset de la Société Générale, publié le 9 Décembre 2024. Son objectif principal est de fournir une stratégie et des perspectives pour le marché des actions américaines pour l'année 2025, en se focalisant sur le thème de l'America First et les impacts potentiels d'un nouveau gouvernement américain.  

Le rapport se concentre d’abord sur les perspectives du S&P500. «  Des rendements concentrés en début d'année 2025 sont prévus, avec un objectif de 6 750 points pour la fin 2025, soutenu par une croissance attendue du bénéfice par action » de +11%. «  La sensibilité de l'indice aux rendements des bons du Trésor américain »  (prévus entre 3,75% et 4,75%) « pourrait le faire osciller entre 6 500 et 7 500. » « Un scénario très optimiste pourrait le porter à 8 000, tandis qu'une guerre commerciale intense pourrait le faire chuter à 5 000, pour un rendement annuel espéré d'environ 11% . »

« Plusieurs facteurs liés aux potentielles politiques de la nouvelle administration américaine sont identifiés comme des catalyseurs majeurs : une baisse des impôts visant à accélérer la relocalisation, une réduction des réglementations, et potentiellement un prix du pétrole plus bas. » « La baisse des impôts sur la production domestique est estimée à un impact positif direct de 2 à 3% sur l'EPS du S&P 500. La réduction de la réglementation est vue comme un catalyseur important, notamment dans les secteurs manufacturier, énergétique et financier, visant à améliorer la productivité. » Cependant, une augmentation des tarifs douaniers (potentiellement 60% sur les biens chinois) pourrait réduire la croissance des EPS de 2-3%, neutralisant ainsi quasiment les avantages fiscaux. Une incertitude autour de l'inflation et de la politique monétaire de la Fed est également mentionnée.
« D'un point de vue sectoriel, les signaux restent positifs pour les cycliques tels que les Financières (considérées attractives et bénéficiant de la déréglementation », notamment les plateformes américaines d’échange de cryptomonnaies), « la Consommation Discrétionnaire (soutenue par le faible endettement des ménages) et l'Industrie (avantagée par les politiques America First). » « Une extrême prudence est recommandée pour le secteur technologique, avec une préférence pour la SG Defensive Tech, car la croissance des EPS en 2025 devrait provenir majoritairement de l'extérieur du Nasdaq-100. Bien que l'exceptionnalisme américain doive persister, le risque de concentration du S&P 500 (où le S&P 500 Equal Weight est une alternative » puisque la Tech occupe 18% de moins dans la distribution de l’indice) « et le prix élevé au global des actions US sont des points d'attention. Enfin, un risque de stagflation au second semestre est mentionné, suggérant une couverture potentielle. » 

En termes de thèmes d'investissement, le rapport recommande fortement les paniers America First, tels que les bénéficiaires de la relocalisation américaine et le nouveau panier SG Domestic Supply-Chain. Il est aussi mention que de nombreuses opportunités en stock-picking sont à prévoir (cf. graph High vs Low Risk).
Le rapport conclut que la valorisation actuelle du S&P 500 est chère selon plusieurs métriques historiques, mais que la croissance des bénéfices américains (qui représente une part croissante des bénéfices mondiaux) contribue à maintenir la valorisation sous contrôle."""

# --- FONCTION POUR AFFICHER LES TITRES STYLISÉS ---
def styled_title(text, title_key): 
    style_dict = STYLE_CONFIG["titles"].get(title_key, {})
    style_str = build_style_string(style_dict)
    
    if title_key == 1: tag = "h1"
    elif title_key == 2: tag = "h2"
    elif title_key == 3: tag = "h3"
    elif title_key == "prediction_box_title": tag = "h4"
    else: tag = "h3" 
        
    st.markdown(f"<{tag} style='{style_str}'>{text}</{tag}>", unsafe_allow_html=True)

# --- FONCTION POUR AFFICHER DU TEXTE STYLISÉ ---
def styled_text(text_content, style_key, tag='p'):
    style_dict = STYLE_CONFIG["text"].get(style_key, {})
    style_str = build_style_string(style_dict)
    
    paragraphs = text_content.split('\n\n')
    html_output = ""
    for paragraph in paragraphs:
        paragraph_html = paragraph.replace('\n', '<br>')
        html_output += f"<{tag} style='{style_str}'>{paragraph_html}</{tag}>"
    st.markdown(html_output, unsafe_allow_html=True)

# --- FONCTION POUR AFFICHER LES LISTES À PUCES STYLISÉES ---
def styled_list(list_block_text, style_key):
    style_dict = STYLE_CONFIG["text"].get(style_key, {})
    style_str = build_style_string(style_dict)
    
    list_items_text = []
    lines = list_block_text.strip().split('\n') 
    for line in lines:
        line_stripped = line.strip()
        if line_stripped.startswith("- "):
            list_items_text.append(line_stripped[2:]) 
    
    if list_items_text:
        html_list = f"<ul style='{style_str}'>"
        for item_text in list_items_text:
            html_list += f"<li>{item_text}</li>" 
        html_list += "</ul>"
        st.markdown(html_list, unsafe_allow_html=True)

# --- APPLICATION STREAMLIT ---
def main():
    st.set_page_config(layout="wide", page_title="Analyse de Document et Données")

    page_cols_ratios = STYLE_CONFIG["page_layout_cols"]
    margin_left, main_content_col, margin_right = st.columns(page_cols_ratios)

    with main_content_col: 
        styled_title("Case Study Félix Barloy, pour Ismael Miled", title_key=1)

        # --- PARTIE 1 ---
        styled_title("Partie 1 : Document Xasset 20250204.pdf", title_key=2)
        
        styled_title("1. Résumé du document", title_key=3)
        display_formatted_summary_v5(summary_text_updated) 

        styled_title("2. Graphique/Tableau pertinent et explication", title_key=3)
        
        image_path_part1 = "pic.png" 
        image_caption_part1 = "Consensus 2025 sector EPS growth expectations and contribution (page 14)"
        st.image(image_path_part1, caption=image_caption_part1, use_container_width=True)

        description_graphique = """Selon les prévisions de graphique pour 2025, la croissance des EPS sera largement portée par le secteur technologique, avec une progression attendue de 21,3 %, suivi de la santé (20,2%) et des matériaux (18,7%). À l’inverse, des secteurs comme l’énergie (4,0 %) ou les biens de consommation de base (5,4%) affichent des perspectives de croissance nettement plus faibles. Je trouve que ce graphique résume bien les conclusions du rapport : il montre clairement la prépondérance de la tech dans les perspectives de croissance, mais aussi les opportunités grandissantes (notamment pour le stock-picking ou l’investissement thématique) dans les autres secteurs."""
        styled_text(description_graphique, style_key="body_justify") # Modifié pour alignement justifié

        styled_title("3. Analyse des prédictions (5 mois après)", title_key=3)
        
        prediction_non_realisee_titre = "Prédiction non réalisée"
        prediction_non_realisee_texte = """Le rapport de la Société Générale souligne, dans son scénario optimiste, un engouement massif vis-vis des entreprises du S&P500, prévoyant l’indice à 6500 points d’ici Avril 2025. A date d’écriture du rapport, l’indice était aux alentours de 6000, et aura en réalité plongé sous les 5000 le 9 avril. Loin des ‘front-loaded returns’, c’est donc le scénario pessimiste (évoqué page 12 du rapport) qui s’est réalisé."""
        prediction_realisee_titre = "Prédiction réalisée"
        prediction_realisee_texte = """Malgré des cours à la baisse, la Société Générale a vu juste dans sa prédiction ‘tech vs non-tech’, puisqu’un article du Wall Street Journal (WSJ) souligne, fin avril, que la performance du S&P500 n’aurait pas été si désastreuse si l’indice ne comportait pas les Magnificent Seven (-5.7% avec, -1.2% sans). N’ayant pas accès à FactSet/Bloomberg/Refinitiv je ne suis pas en mesure de suivre précisément la pondération tech des performances du S&P500, mais les articles consultés semblent converger vers conclusion malgré la hausse des dernières semaines.
La prédiction sur la baisse du prix du baril s’est confirmée en ce début d’année, avec une baisse de l’ordre de 15% depuis l’écriture du rapport.

WSJ : [https://archive.ph/0HIMP](https://archive.ph/0HIMP)"""
        
        col_pred1, col_pred2 = st.columns(2)
        box_style_str = build_style_string(STYLE_CONFIG["prediction_box_container"])
        pred_title_style_str = build_style_string(STYLE_CONFIG["titles"]["prediction_box_title"])
        pred_text_style_str = build_style_string(STYLE_CONFIG["text"]["prediction_box_content"]) 

        with col_pred1:
            st.markdown(f"<div style='{box_style_str}'><h4 style='{pred_title_style_str}'>{prediction_non_realisee_titre}</h4><div style='{pred_text_style_str}'>{prediction_non_realisee_texte}</div></div>", unsafe_allow_html=True)
        with col_pred2:
            st.markdown(f"<div style='{box_style_str}'><h4 style='{pred_title_style_str}'>{prediction_realisee_titre}</h4><div style='{pred_text_style_str}'>{prediction_realisee_texte}</div></div>", unsafe_allow_html=True)
        
        # --- PARTIE 2 ---
        styled_title("Partie 2 : Fichier analyse de donnees 20250515.xlsx", title_key=2)
        
        intro_text_part2_raw = """Pour cette sous-partie, j'ai présenté chaque variable à Gemini et lui ai demandé quels graphiques seraient pertinents à tracer. J'ai trié une douzaine de suggestions et les ai réparties en quatre catégories : Descriptif, Potentiel, Risque et Valorisation.

J'ai d'abord converti le fichier XLSX en CSV. Tout le code, dans graph.py, est généré par l'IA, hormis les spécifications techniques de mon environnement (correction du séparateur et du caractère décimal de mon CSV, chemin d'accès, noms de variables).

En plus des suggestions données, j'ai ajouté un top 20 basé sur le Sharpe Ratio, car c’est peut-être une métrique que je vais utiliser dans la partie 3, et il est toujours bon de connaître la performance rapportée au risque. J'ai arbitrairement choisi un taux sans risque de 3 %, puisque les taux en Europe (qui concernent les actions les plus représentées dans ce dataset) tournent autour de cette valeur.

Si je devais ne choisir que quelques graphiques clés :
Le n°11, Returns vs Volatility, me semble crucial pour distinguer les différences de rendements rapportés aux risques par secteur.

Les n°13 et 19 permettent de cerner les pays et industries clés de l'année à venir selon les analystes.

La plupart des Top 20 me permettent simplement de souligner les éléments clés dans chaque catégorie, et me donnent une première idée des valeurs que je pourrais introduire à mon portefeuille en partie 3. Ces graphiques ne sont pas indispensables, mais j'ai décidé de les inclure pour montrer mon cheminement de pensée."""
        styled_text(intro_text_part2_raw, style_key="body_justify") # Modifié pour alignement justifié
        st.markdown("---") 

        base_rapport_folder = "rapport" 
        subfolders = ["Descriptive", "Potentiel", "Risque", "Valo"]

        for folder_name in subfolders:
            expander_title = f"Graphiques : {folder_name}"
            folder_path = os.path.join(base_rapport_folder, folder_name)
            with st.expander(expander_title):
                if not os.path.isdir(folder_path): 
                    st.info(f"Dossier '{folder_name}' non trouvé.")
                    continue
                image_files = sorted(glob.glob(os.path.join(folder_path, "*.png")))
                if not image_files:
                    st.info(f"Aucune image PNG trouvée dans '{folder_name}'.")
                else:
                    num_cols_gallery = STYLE_CONFIG["images"]["gallery_cols_count"]
                    gallery_cols = st.columns(num_cols_gallery)
                    for i, img_file_gallery in enumerate(image_files):
                        col_idx_gallery = i % num_cols_gallery
                        with gallery_cols[col_idx_gallery]:
                            img_filename_gallery = os.path.basename(img_file_gallery)
                            st.image(img_file_gallery, caption=f"{img_filename_gallery[:30]}...", use_container_width=True) 

        # --- PARTIE 3 ---
        styled_title("Partie 3 : Optimisation de Portefeuille", title_key=2) 

        intro_text_part3_raw = """Pour cette troisième partie, j'ai décidé d'écarter les colonnes qui ont des valeurs manquantes de mon modèle. J'ai également concentré mon attention sur les valeurs européennes, puisqu'il n'y  a que très peu d'actions chinoises et américaines. C'est un parti pris de renoncer à la diversification géographique au profit d'un portefeuille européen. En suivant les contraintes données, je suis alors parti sur un portefeuille qui maximise le rendement revenu aux risques.

Le critère a maximiser est un ratio que j'ai crée:

- 60% des performances sont basés sur le forecast (Upside/12-Month Put Implied Volatility)
- 40% sont basés sur l'historique (1-Year Total Return/Volatility 360 Day)

J'ai laissé l'IA me conseiller sur la librairie à utiliser et le code, ayant déjà fait une optimisation de portefeuille sur Excel mais pas sur Python. J'ai également rajouté les contraintes suivantes :

- Aucun secteur ne doit dépasser 25% de concentration des titres
- Les secteurs doivent avoir au minimum 2% de part dans le portefeuille

Les résultats sont visibles sur l'image ci-dessous:"""
        
        intro_paragraphs_part3 = intro_text_part3_raw.split('\n\n')
        for paragraph_p3 in intro_paragraphs_part3:
            current_paragraph_stripped = paragraph_p3.strip()
            if current_paragraph_stripped.startswith("- "):
                styled_list(current_paragraph_stripped, style_key="list_justify") # Modifié pour alignement justifié
            else: 
                styled_text(paragraph_p3, style_key="body_justify") # Modifié pour alignement justifié

        image_path_part3 = "results.png"
        image_caption_part3 = "Résultat de l'optimisation de portefeuille"
        st.image(image_path_part3, caption=image_caption_part3, use_container_width=True)

        conclusion_part3_raw = """Les 11 secteurs sont bien représentés dans le portefeuille final, avec une pondération de minimum 2% et de maximum 25% par secteur. Aucun titre ne dépasse 8%. Le rendement attendu du portefeuille est de 28%, je présume que les prédictions sont faites sur un an. La volatilité, elle, est de 26.8%."""
        styled_text(conclusion_part3_raw, style_key="body_justify") # Modifié pour alignement justifié

if __name__ == "__main__":
    main()
