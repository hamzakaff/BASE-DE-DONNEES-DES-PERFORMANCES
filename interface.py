import streamlit as st
import os
from download_logic import telecharger_fichiers_depuis_site
from fusion_logic import fusionner_excel

st.title("Téléchargement & Fusion de fichiers Excel (.xlsx)")

url = st.text_input("URL du site d'ASFIM")
download_dir = st.text_input("Chemin vers le dossier de téléchargement")
nb_pages = st.number_input("Nombre de pages à parcourir", min_value=1, max_value=3000, value=3)

if st.button("Lancer le téléchargement"):
    if not url or not download_dir:
        st.error("Merci de renseigner l'URL et le chemin du dossier.")
    elif not os.path.isdir(download_dir):
        st.error("Le dossier spécifié n'existe pas.")
    else:
        with st.spinner("Téléchargement en cours..."):
            succes = telecharger_fichiers_depuis_site(url, download_dir, nb_pages)
        if succes:
            st.success("Téléchargement terminé avec succès.")
        else:
            st.error("Une erreur est survenue pendant le téléchargement.")

if st.button("Fusionner les fichiers Excel"):
    if not os.path.isdir(download_dir):
        st.error("Le dossier spécifié est invalide.")
    else:
        fusion_path = os.path.join(download_dir, "fusion_resultat.xlsx")
        fusion_df = fusionner_excel(download_dir, fusion_path)

        if fusion_df is not None:
            st.success("Fusion réussie ! Voici un aperçu :")
            st.dataframe(fusion_df)

            with open(fusion_path, "rb") as f:
                st.download_button(
                    label="Télécharger le fichier fusionné Excel",
                    data=f,
                    file_name="fusion_resultat.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        else:
            st.error("Aucun fichier Excel fusionné ou erreur pendant la fusion.")
