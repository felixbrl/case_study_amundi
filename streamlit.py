import streamlit as st
import re
import os
import glob
import graph

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# --- FONCTION POUR AFFICHER LE RÉSUMÉ FORMATÉ ---
def display_formatted_summary(text_with_guillemets):
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
                paragraph_html_content += f'<span class="ia-text">{ia_content}</span>'
            else:
                paragraph_html_content += para_text[start_match:end_match]
            last_index = end_match
        if last_index < len(para_text):
            paragraph_html_content += para_text[last_index:]
        if paragraph_html_content.strip():
            html_paragraphs.append(f'<p>{paragraph_html_content}</p>')
    final_html = "".join(html_paragraphs)
    st.markdown(final_html, unsafe_allow_html=True)

def render_summary_page():
    st.markdown("<h2>Partie 1 : Document Xasset 20250204.pdf</h2>", unsafe_allow_html=True)

    st.markdown("<h3>1. Résumé du document</h3>", unsafe_allow_html=True)
    summary_text = """Pour écrire ce résumé, je me suis aidé de l'IA NotebookLM pour synthétiser le rapport de la Société Générale. Le texte en gris désigne le texte généré par IA, en blanc, le mien. Sur Word, en police 12, cette première partie fait environ 40 lignes.

    Le document fourni pour cet exercice intitulé America First est issu du service de recherche Cross-Asset de la Société Générale, publié le 9 Décembre 2024. Son objectif principal est de fournir une stratégie et des perspectives pour le marché des actions américaines pour l'année 2025, en se focalisant sur le thème de l'America First et les impacts potentiels d'un nouveau gouvernement américain.  

    Le rapport se concentre d’abord sur les perspectives du S&P500. «  Des rendements concentrés en début d'année 2025 sont prévus, avec un objectif de 6 750 points pour la fin 2025, soutenu par une croissance attendue du bénéfice par action » de +11%. «  La sensibilité de l'indice aux rendements des bons du Trésor américain »  (prévus entre 3,75% et 4,75%) « pourrait le faire osciller entre 6 500 et 7 500. » « Un scénario très optimiste pourrait le porter à 8 000, tandis qu'une guerre commerciale intense pourrait le faire chuter à 5 000, pour un rendement annuel espéré d'environ 11% . »

    « Plusieurs facteurs liés aux potentielles politiques de la nouvelle administration américaine sont identifiés comme des catalyseurs majeurs : une baisse des impôts visant à accélérer la relocalisation, une réduction des réglementations, et potentiellement un prix du pétrole plus bas. » « La baisse des impôts sur la production domestique est estimée à un impact positif direct de 2 à 3% sur l'EPS du S&P 500. La réduction de la réglementation est vue comme un catalyseur important, notamment dans les secteurs manufacturier, énergétique et financier, visant à améliorer la productivité. » Cependant, une augmentation des tarifs douaniers (potentiellement 60% sur les biens chinois) pourrait réduire la croissance des EPS de 2-3%, neutralisant ainsi quasiment les avantages fiscaux. Une incertitude autour de l'inflation et de la politique monétaire de la Fed est également mentionnée.
    « D'un point de vue sectoriel, les signaux restent positifs pour les cycliques tels que les Financières (considérées attractives et bénéficiant de la déréglementation », notamment les plateformes américaines d’échange de cryptomonnaies), « la Consommation Discrétionnaire (soutenue par le faible endettement des ménages) et l'Industrie (avantagée par les politiques America First). » « Une extrême prudence est recommandée pour le secteur technologique, avec une préférence pour la SG Defensive Tech, car la croissance des EPS en 2025 devrait provenir majoritairement de l'extérieur du Nasdaq-100. Bien que l'exceptionnalisme américain doive persister, le risque de concentration du S&P 500 (où le S&P 500 Equal Weight est une alternative » puisque la Tech occupe 18% de moins dans la distribution de l’indice) « et le prix élevé au global des actions US sont des points d'attention. Enfin, un risque de stagflation au second semestre est mentionné, suggérant une couverture potentielle. »

    En termes de thèmes d'investissement, le rapport recommande fortement les paniers America First, tels que les bénéficiaires de la relocalisation américaine et le nouveau panier SG Domestic Supply-Chain. Il est aussi mention que de nombreuses opportunités en stock-picking sont à prévoir (cf. graph High vs Low Risk).
    Le rapport conclut que la valorisation actuelle du S&P 500 est chère selon plusieurs métriques historiques, mais que la croissance des bénéfices américains (qui représente une part croissante des bénéfices mondiaux) contribue à maintenir la valorisation sous contrôle."""
    display_formatted_summary(summary_text)

    st.markdown("<h3>2. Graphique/Tableau pertinent et explication</h3>", unsafe_allow_html=True)
    image_path_part1 = "pic.png"
    if os.path.exists(image_path_part1):
        st.image(image_path_part1, caption="Consensus 2025 sector EPS growth expectations and contribution (page 14)", use_container_width=True)
    else:
        st.warning(f"Image '{image_path_part1}' non trouvée.")

    description_graphique = """<p>Selon les prévisions de graphique pour 2025, la croissance des EPS sera largement portée par le secteur technologique, avec une progression attendue de 21,3 %, suivi de la santé (20,2%) et des matériaux (18,7%). À l’inverse, des secteurs comme l’énergie (4,0 %) ou les biens de consommation de base (5,4%) affichent des perspectives de croissance nettement plus faibles. Je trouve que ce graphique résume bien les conclusions du rapport : il montre clairement la prépondérance de la tech dans les perspectives de croissance, mais aussi les opportunités grandissantes (notamment pour le stock-picking ou l’investissement thématique) dans les autres secteurs.</p>"""
    st.markdown(description_graphique, unsafe_allow_html=True)

    st.markdown("<h3>3. Analyse des prédictions (5 mois après)</h3>", unsafe_allow_html=True)
    prediction_non_realisee_titre = "Prédiction non réalisée"
    prediction_non_realisee_texte = """Le rapport de la Société Générale souligne, dans son scénario optimiste, un engouement massif vis-vis des entreprises du S&P500, prévoyant l’indice à 6500 points d’ici Avril 2025. A date d’écriture du rapport, l’indice était aux alentours de 6000, et aura en réalité plongé sous les 5000 le 9 avril. Loin des ‘front-loaded returns’, c’est donc le scénario pessimiste (évoqué page 12 du rapport) qui s’est réalisé."""
    prediction_realisee_titre = "Prédiction réalisée"
    prediction_realisee_texte = """Malgré des cours à la baisse, la Société Générale a vu juste dans sa prédiction ‘tech vs non-tech’, puisqu’un article du Wall Street Journal (WSJ) souligne, fin avril, que la performance du S&P500 n’aurait pas été si désastreuse si l’indice ne comportait pas les Magnificent Seven (-5.7% avec, -1.2% sans). N’ayant pas accès à FactSet/Bloomberg/Refinitiv je ne suis pas en mesure de suivre précisément la pondération tech des performances du S&P500, mais les articles consultés semblent converger vers conclusion malgré la hausse des dernières semaines.
La prédiction sur la baisse du prix du baril s’est confirmée en ce début d’année, avec une baisse de l’ordre de 15% depuis l’écriture du rapport.

WSJ : [https://archive.ph/0HIMP](https://archive.ph/0HIMP)"""

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<div class="prediction-box"><h4 class="prediction-box-title">{prediction_non_realisee_titre}</h4><p class="prediction-box-content">{prediction_non_realisee_texte}</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="prediction-box"><h4 class="prediction-box-title">{prediction_realisee_titre}</h4><p class="prediction-box-content">{prediction_realisee_texte}</p></div>', unsafe_allow_html=True)

def render_data_analysis_page():
    st.markdown("<h2>Partie 2 : Fichier analyse de donnees 20250515.xlsx</h2>", unsafe_allow_html=True)
    intro_text_part2 = """<p>Pour cette sous-partie, j'ai présenté chaque variable à Gemini et lui ai demandé quels graphiques seraient pertinents à tracer. J'ai trié une douzaine de suggestions et les ai réparties en quatre catégories : Descriptif, Potentiel, Risque et Valorisation.</p>
<p>J'ai d'abord converti le fichier XLSX en CSV. Tout le code, dans graph.py, est généré par l'IA, hormis les spécifications techniques de mon environnement (correction du séparateur et du caractère décimal de mon CSV, chemin d'accès, noms de variables).</p>
<p>En plus des suggestions données, j'ai ajouté un top 20 basé sur le Sharpe Ratio, car c’est peut-être une métrique que je vais utiliser dans la partie 3, et il est toujours bon de connaître la performance rapportée au risque. J'ai arbitrairement choisi un taux sans risque de 3 %, puisque les taux en Europe (qui concernent les actions les plus représentées dans ce dataset) tournent autour de cette valeur.</p>
<p>Si je devais ne choisir que quelques graphiques clés :</p>
<ul>
<li>Le n°11, Returns vs Volatility, me semble crucial pour distinguer les différences de rendements rapportés aux risques par secteur.</li>
<li>Les n°13 et 19 permettent de cerner les pays et industries clés de l'année à venir selon les analystes.</li>
<li>La plupart des Top 20 me permettent simplement de souligner les éléments clés dans chaque catégorie, et me donnent une première idée des valeurs que je pourrais introduire à mon portefeuille en partie 3. Ces graphiques ne sont pas indispensables, mais j'ai décidé de les inclure pour montrer mon cheminement de pensée.</li>
</ul>"""
    st.markdown(intro_text_part2, unsafe_allow_html=True)
    st.markdown("---")

    df = graph.load_data()
    if df is not None:
        plot_choice = st.selectbox("Choose a plot to display:", list(graph.AVAILABLE_PLOTS.keys()))
        plot_function = graph.AVAILABLE_PLOTS[plot_choice]
        fig = plot_function(df)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Could not generate the plot.")
    else:
        st.error("Could not load the data. Please make sure 'data.csv' is in the correct directory.")

def render_portfolio_optimization_page():
    st.markdown("<h2>Partie 3 : Optimisation de Portefeuille</h2>", unsafe_allow_html=True)
    intro_text_part3 = """<p>Pour cette troisième partie, j'ai décidé d'écarter les colonnes qui ont des valeurs manquantes de mon modèle. J'ai également concentré mon attention sur les valeurs européennes, puisqu'il n'y  a que très peu d'actions chinoises et américaines. C'est un parti pris de renoncer à la diversification géographique au profit d'un portefeuille européen. En suivant les contraintes données, je suis alors parti sur un portefeuille qui maximise le rendement revenu aux risques.</p>
<p>Le critère à maximiser est un ratio que j'ai crée:</p>
<ul>
<li>60% des performances sont basés sur le forecast (Upside/12-Month Put Implied Volatility)</li>
<li>40% sont basés sur l'historique (1-Year Total Return/Volatility 360 Day)</li>
</ul>
<p>J'ai laissé l'IA me conseiller sur la librairie à utiliser, et je l'ai laissé rédiger le code (ayant déjà fait une optimisation de portefeuille sur Excel mais pas sur Python). J'ai également rajouté les contraintes suivantes :</p>
<ul>
<li>Aucun secteur ne doit dépasser 25% de concentration des titres</li>
<li>Les secteurs doivent avoir au minimum 2% de part dans le portefeuille</li>
</ul>
<p>Les résultats sont visibles sur l'image ci-dessous:</p>"""
    st.markdown(intro_text_part3, unsafe_allow_html=True)

    image_path_part3 = "results.png"
    if os.path.exists(image_path_part3):
        st.image(image_path_part3, caption="Résultat de l'optimisation de portefeuille", use_container_width=True)
    else:
        st.warning(f"Image '{image_path_part3}' non trouvée.")

    conclusion_part3 = """<p>Les 11 secteurs sont bien représentés dans le portefeuille final, avec une pondération de minimum 2% et de maximum 25% par secteur. Aucun titre ne dépasse 8%. Le rendement attendu du portefeuille est de 28%, je présume que les prédictions sont faites sur un an. La volatilité, elle, est de 26.8%.</p>
<p>Merci. Temps de travail estimé : 9 heures</p>"""
    st.markdown(conclusion_part3, unsafe_allow_html=True)

def main():
    st.set_page_config(layout="wide", page_title="Analyse de Document et Données")
    load_css("style.css")

    st.markdown("<h1>Case Study Félix Barloy, pour Ismael Miled</h1>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📄 Summary", "📊 Data Analysis", "📈 Portfolio Optimization"])

    with tab1:
        render_summary_page()
    with tab2:
        render_data_analysis_page()
    with tab3:
        render_portfolio_optimization_page()

if __name__ == "__main__":
    main()