import pandas as pd
import numpy as np
from pypfopt import EfficientFrontier, objective_functions, risk_models
from pypfopt.exceptions import OptimizationError # Gardé au cas où, mais pas de try/except
import cvxpy as cp # Gardé pour la compatibilité si ECOS est appelé via cp.ECOS

# 1. Chargement et Préparation des Données
# --- MODIFIEZ CETTE LIGNE AVEC LE CHEMIN DE VOTRE FICHIER CSV ---
csv_file_path = r"D:\Téléchargements\Privé_ Exercices pour l'entretien du Stage Assistant Gestion Multi Asset\data.csv"
# --- AJUSTEZ AUSSI sep (séparateur) ET decimal SI BESOIN ---

# Le bloc try...except pour le chargement du fichier est supprimé
df = pd.read_csv(csv_file_path, sep=';', decimal='.') 
print(f"Fichier '{csv_file_path}' chargé avec succès. Nombre de lignes initiales: {len(df)}")

# --- MODIFICATION : Ajout de 'mixte' aux colonnes requises ---
required_columns = ['Equity', '1 Year Total Return - Previous', 'Volatility 360 Day Calc',
                    'Upside with Target Price from Analyst (in %)', '12 Month Put Implied Volatility', 
                    'Sector (1)', 'mixte'] # 'mixte' est maintenant une colonne d'entrée
missing_cols = [col for col in required_columns if col not in df.columns]
if missing_cols:
    print(f"ERREUR : Colonnes manquantes dans votre CSV : {', '.join(missing_cols)}")
    exit() # Garde un exit simple si les colonnes de base manquent

# --- MODIFICATION : Ajout de 'mixte' aux colonnes à convertir en numérique ---
cols_to_numeric = ['1 Year Total Return - Previous', 'Volatility 360 Day Calc',
                   'Upside with Target Price from Analyst (in %)', '12 Month Put Implied Volatility', 'mixte']
for col in cols_to_numeric:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df_cleaned = df.dropna(subset=required_columns).copy()
epsilon_vol = 1e-6
df_cleaned = df_cleaned[df_cleaned['Volatility 360 Day Calc'] > epsilon_vol]
df_cleaned = df_cleaned[df_cleaned['12 Month Put Implied Volatility'] > epsilon_vol] # Gardé pour le calcul de la vol mixte de reporting
print(f"Nombre de lignes après nettoyage initial (NaN, volatilités non valides): {len(df_cleaned)}")

# 2. Préparation des Métriques par Actif (le score 'mixte' est maintenant une entrée)
# Le calcul du 'score_rendement_modele' est supprimé car 'mixte' le remplace pour l'optimisation.

# Calcul des métriques de reporting (restent utiles)
df_cleaned.loc[:, 'rendement_pct_mixte_reporting'] = \
    (df_cleaned['1 Year Total Return - Previous'] * 0.4 + 
     df_cleaned['Upside with Target Price from Analyst (in %)'] * 0.6)

df_cleaned.loc[:, 'volatilite_mixte_reporting'] = \
    (df_cleaned['Volatility 360 Day Calc'] * 0.4 +
     df_cleaned['12 Month Put Implied Volatility'] * 0.6)

# S'assurer que la colonne 'mixte' (pour l'optimisation) et les métriques de reporting n'ont pas de NaN
df_cleaned.dropna(subset=['mixte', 'rendement_pct_mixte_reporting', 'volatilite_mixte_reporting'], inplace=True)
print(f"Nombre de lignes après s'être assuré que 'mixte' et les métriques de reporting sont valides: {len(df_cleaned)}")

if df_cleaned.empty:
    print("Le DataFrame est vide après le nettoyage. Aucune action à optimiser.")
    exit() # Garde un exit simple

# 3. Optimisation du Portefeuille avec PyPortfolioOpt
df_for_opt_indexed = df_cleaned.set_index('Equity')
# --- MODIFICATION : mu_optimizer utilise maintenant directement la colonne 'mixte' ---
mu_optimizer = df_for_opt_indexed['mixte'] # C'est le score/critère à maximiser
# --- FIN MODIFICATION ---

variances = (df_for_opt_indexed['Volatility 360 Day Calc'] / 100)**2 # S est basée sur Vol historique
S_diag_values = variances.reindex(mu_optimizer.index).fillna(variances.mean())
S_optimizer = pd.DataFrame(np.diag(S_diag_values.values), index=mu_optimizer.index, columns=mu_optimizer.index)

common_idx = mu_optimizer.index.intersection(S_optimizer.index)
mu_optimizer = mu_optimizer.loc[common_idx]
S_optimizer = S_optimizer.loc[common_idx, common_idx]
df_for_opt_indexed = df_for_opt_indexed.loc[common_idx]

if mu_optimizer.empty:
    print("Aucune action disponible pour l'optimisation après préparation de mu et S.")
    exit() # Garde un exit simple

ef = EfficientFrontier(mu_optimizer, S_optimizer, weight_bounds=(0, 0.08), solver="ECOS")

sector_mapper = df_for_opt_indexed['Sector (1)']
unique_sectors = sector_mapper.unique()
print(f"Secteurs uniques identifiés pour les contraintes: {len(unique_sectors)} -> {', '.join(unique_sectors)}")

min_sector_alloc = 0.02
max_sector_alloc = 0.25
sector_lower = {sector: min_sector_alloc for sector in unique_sectors}
sector_upper = {sector: max_sector_alloc for sector in unique_sectors}

if len(unique_sectors) * min_sector_alloc > 1 + epsilon_vol :
    print(f"ERREUR : La somme des allocations minimales de secteur ({len(unique_sectors) * min_sector_alloc * 100}%) dépasse 100%.")
    exit() 
    
ef.add_sector_constraints(sector_mapper, sector_lower, sector_upper)
ef.max_quadratic_utility(risk_aversion=1e-9)

raw_weights = ef.weights 
print("\nPoids bruts retournés par l'optimiseur (avant nettoyage):")
for i, asset_name in enumerate(mu_optimizer.index): 
    if abs(raw_weights[i]) > 1e-7: 
         print(f"- {asset_name}: {raw_weights[i]:.6f}")

weights = ef.clean_weights() 

portfolio_composition_list = []
for stock_name, weight_val in weights.items(): 
    if weight_val > 0: 
        sector = sector_mapper.get(stock_name, 'N/A')
        action_data_row = df_cleaned[df_cleaned['Equity'] == stock_name]
        if not action_data_row.empty:
            action_data = action_data_row.iloc[0]
            # --- MODIFICATION : 'score_optimisation' est maintenant la valeur de la colonne 'mixte' ---
            action_score_optimisation = action_data['mixte'] 
            # --- FIN MODIFICATION ---
            action_rendement_pct_mixte = action_data['rendement_pct_mixte_reporting']
            action_volatilite_mixte = action_data['volatilite_mixte_reporting']
        else:
            action_score_optimisation, action_rendement_pct_mixte, action_volatilite_mixte = np.nan, np.nan, np.nan

        portfolio_composition_list.append({
            'Equity': stock_name,
            'Weight': weight_val,
            'Sector (1)': sector,
            'Score Optimisation (colonne mixte)': action_score_optimisation, # Libellé mis à jour
            'Rendement Mixte en % (Reporting)': action_rendement_pct_mixte,
            'Volatilite Mixte en % (Reporting)': action_volatilite_mixte
        })

portfolio_df = pd.DataFrame(portfolio_composition_list)

if not portfolio_df.empty:
    print("\n--- Composition Détaillée du Portefeuille et Métriques Individuelles ---")
    for index, row in portfolio_df.iterrows():
        print(f"- {row['Equity']}: Poids={row['Weight']:.4f}, Secteur='{row['Sector (1)']}', "
              # --- MODIFICATION : Affichage du score d'optimisation (colonne 'mixte') ---
              f"Score Optimisation (mixte)={row['Score Optimisation (colonne mixte)']:.4f}, "
              # --- FIN MODIFICATION ---
              f"Rdt Mixte % (Report)={row['Rendement Mixte en % (Reporting)']:.2f}%, "
              f"Vol Mixte % (Report)={row['Volatilite Mixte en % (Reporting)']:.2f}%")

    # 4. Outputs : Performance Globale du Portefeuille
    # `optimized_portfolio_score` sera maintenant la moyenne pondérée des scores 'mixte'
    optimized_portfolio_score, ptf_vol_decimal_S_based, _ = ef.portfolio_performance(verbose=False, risk_free_rate=0.0)
    ptf_vol_percentage_S_based = ptf_vol_decimal_S_based * 100
    
    ptf_rendement_pct_mixte_reporting = (portfolio_df['Weight'] * portfolio_df['Rendement Mixte en % (Reporting)']).sum()
    ptf_volatilite_mixte_reporting_ponderee = (portfolio_df['Weight'] * portfolio_df['Volatilite Mixte en % (Reporting)']).sum()

    print("\n--- Performance Globale du Portefeuille ---")
    # --- MODIFICATION : Libellé mis à jour ---
    print(f"Score d'Optimisation du Portefeuille (basé sur colonne 'mixte'): {optimized_portfolio_score:.4f}")
    # --- FIN MODIFICATION ---
    print(f"Rendement Mixte en % du Portefeuille (Reporting): {ptf_rendement_pct_mixte_reporting:.2f}%")
    print(f"Volatilité Mixte Pondérée du Portefeuille (Reporting): {ptf_volatilite_mixte_reporting_ponderee:.2f}%")
    print(f"Volatilité Annuelle du Portefeuille (calculée par l'optimiseur via S): {ptf_vol_percentage_S_based:.2f}%")

    csv_filename_output = r"D:\Téléchargements\Privé_ Exercices pour l'entretien du Stage Assistant Gestion Multi Asset\portfolio_composition_final.csv"
    portfolio_df.to_csv(csv_filename_output, sep=';', index=False, float_format='%.4f')
    
    with open(csv_filename_output, 'a', newline='', encoding='utf-8') as f:
        f.write("\n") 
        f.write("Indicateurs Globaux du Portefeuille;\n") 
        # --- MODIFICATION : Libellé mis à jour ---
        f.write(f"Score d'Optimisation du Portefeuille (basé sur colonne 'mixte');{optimized_portfolio_score:.4f}\n")
        # --- FIN MODIFICATION ---
        f.write(f"Rendement Mixte en % du Portefeuille (Reporting);{ptf_rendement_pct_mixte_reporting:.2f}\n")
        f.write(f"Volatilite Mixte Ponderee du Portefeuille (Reporting en %);{ptf_volatilite_mixte_reporting_ponderee:.2f}\n")
        f.write(f"Volatilite Annuelle du Portefeuille (calculee par l'optimiseur via S en %);{ptf_vol_percentage_S_based:.2f}\n")
    print(f"\nComposition détaillée ET indicateurs globaux sauvegardés dans {csv_filename_output}")

    print("\n--- Vérification des Contraintes ---")
    print(f"Somme des poids: {portfolio_df['Weight'].sum():.4f}")
    max_weight_in_pf = portfolio_df['Weight'].max() if not portfolio_df.empty else 0
    print(f"Poids maximum par action: {max_weight_in_pf:.4f} (Contrainte: <= 0.08)")
    if max_weight_in_pf > 0.080001:
         print(f"ATTENTION: Contrainte de poids max par action violée: {max_weight_in_pf}")

    print("\nVérification des contraintes sectorielles:")
    for sector_name in unique_sectors:
        sector_weight_sum = portfolio_df[portfolio_df['Sector (1)'] == sector_name]['Weight'].sum()
        stocks_in_sector = portfolio_df[portfolio_df['Sector (1)'] == sector_name].shape[0]
        print(f"Secteur '{sector_name}': Poids Total = {sector_weight_sum:.4f} ({stocks_in_sector} actions), "
              f"Min Attendu={sector_lower.get(sector_name,0):.2%}, Max Attendu={sector_upper.get(sector_name,0):.2%}")
        
        if not (sector_lower.get(sector_name,0) - epsilon_vol <= sector_weight_sum <= sector_upper.get(sector_name,0) + epsilon_vol):
            if sector_weight_sum < sector_lower.get(sector_name,0) - epsilon_vol :
                print(f"  ATTENTION: Poids du secteur '{sector_name}' ({sector_weight_sum:.4f}) est INFÉRIEUR au min ({sector_lower.get(sector_name,0):.2%}).")
            if sector_weight_sum > sector_upper.get(sector_name,0) + epsilon_vol :
                print(f"  ATTENTION: Poids du secteur '{sector_name}' ({sector_weight_sum:.4f}) est SUPÉRIEUR au max ({sector_upper.get(sector_name,0):.2%}).")
else:
    print("\n--- AUCUNE ACTION SÉLECTIONNÉE POUR LE PORTEFEUILLE ---")
    print("L'optimisation a abouti à un portefeuille vide après nettoyage des poids.")
    print("Vérifiez les 'Poids bruts retournés par l'optimiseur' ci-dessus.")
    print("Causes possibles : contraintes trop restrictives, scores ('mixte') d'actions globalement trop bas, problèmes numériques.")
