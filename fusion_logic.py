import os
import pandas as pd
import re

def extraire_date_depuis_texte(texte):
    date_regex = r"\d{2}/\d{2}/\d{4}"
    match = re.search(date_regex, texte)
    if match:
        try:
            return pd.to_datetime(match.group(), format="%d/%m/%Y", errors='raise')
        except ValueError:
            return None
    return None


def fusionner_excel(dossier_excel, fichier_sortie="fusion_resultat.xlsx"):
    fichiers_excel = [f for f in os.listdir(dossier_excel) if f.endswith(".xlsx")]
    dfs = []
    fichiers_ignores = []

    for f in fichiers_excel:
        chemin = os.path.join(dossier_excel, f)

        try:
            df_temp = pd.read_excel(chemin, header=None)
        except:
            fichiers_ignores.append(f)
            continue

        date_extrait = extraire_date_depuis_texte(str(df_temp.iloc[0, 0]))
        if date_extrait is None:
            fichiers_ignores.append(f)
            continue

        try:
            df = pd.read_excel(chemin, header=1)
            df.columns = df.columns.str.strip()

            # Renommer les colonnes si nécessaire
            if "OPCVM" not in df.columns and "Dénomination OPCVM" in df.columns:
                df.rename(columns={"Dénomination OPCVM": "OPCVM"}, inplace=True)

            if "Indice Benchmark" not in df.columns and "Indice Bentchmark" in df.columns:
                df.rename(columns={"Indice Bentchmark": "Indice Benchmark"}, inplace=True)

            if "OPCVM" not in df.columns or "Indice Benchmark" not in df.columns:
                fichiers_ignores.append(f)
                continue

            df.insert(0, "Date", date_extrait)
            dfs.append(df)

        except:
            fichiers_ignores.append(f)
            continue

    if dfs:
        fusion = pd.concat(dfs, ignore_index=True).sort_values(by="Date")
        fusion.to_excel(fichier_sortie, index=False)
        print("Fusion réussie :", fichier_sortie)
    else:
        print("Aucun fichier fusionné.")

    # Afficher les fichiers ignorés à la fin
    if fichiers_ignores:
        print("\nFichiers ignorés (problème de format, date ou colonnes manquantes) :")
        for fichier in fichiers_ignores:
            print("-", fichier)

    return fusion if dfs else None
