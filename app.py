import os
from datetime import date

import pandas as pd
import streamlit as st

FICHIER = "data.csv"

st.set_page_config(page_title="Reboisement & Déchets", page_icon="🌳", layout="wide")
st.title("🌳 Collecte de données : reboisement et gestion des déchets")

# ---------- Formulaire ----------
with st.form("formulaire", clear_on_submit=True):
	st.subheader("📍 Informations générales")
	col1, col2, col3 = st.columns(3)
	enqueteur = col1.text_input("Nom de l'enquêteur")
	village = col2.text_input("Village / Localité")
	date_collecte = col3.date_input("Date de collecte", date.today())

	menage = st.text_input("Nom du chef de ménage")
	taille_menage = st.number_input("Nombre de personnes dans le ménage", min_value=1, step=1)

	st.subheader("🌱 Reboisement")
	col4, col5, col6 = st.columns(3)
	arbres_plantes = col4.number_input("Arbres plantés", min_value=0, step=1)
	arbres_survivants = col5.number_input("Arbres survivants", min_value=0, step=1)
	espece = col6.text_input("Espèce(s) plantée(s)")

	st.subheader("♻️ Gestion des déchets")
	col7, col8 = st.columns(2)
	plastique = col7.number_input("Déchets plastiques (kg/semaine)", min_value=0.0, step=0.5)
	organique = col8.number_input("Déchets organiques (kg/semaine)", min_value=0.0, step=0.5)

	gestion_plastique = st.selectbox(
		"Que faites-vous des déchets plastiques ?",
		["Brûlage", "Décharge sauvage", "Collecte communale", "Recyclage / Revente", "Réutilisation", "Autre"],
	)
	gestion_organique = st.selectbox(
		"Que faites-vous des déchets organiques ?",
		["Compost", "Alimentation des animaux", "Décharge sauvage", "Brûlage", "Enfouissement", "Autre"],
	)
	tri = st.radio("Le ménage fait-il le tri des déchets ?", ["Oui", "Non"], horizontal=True)
	observations = st.text_area("Observations")

	envoyer = st.form_submit_button("✅ Enregistrer")

# ---------- Enregistrement ----------
if envoyer:
	if not village or not menage:
		st.error("Veuillez remplir au moins le village et le nom du ménage.")
	elif arbres_survivants > arbres_plantes:
		st.error("Les arbres survivants ne peuvent pas dépasser les arbres plantés.")
	else:
		ligne = pd.DataFrame([{
			"Date": date_collecte,
			"Enquêteur": enqueteur,
			"Village": village,
			"Ménage": menage,
			"Taille ménage": taille_menage,
			"Arbres plantés": arbres_plantes,
			"Arbres survivants": arbres_survivants,
			"Espèce": espece,
			"Plastique (kg/sem)": plastique,
			"Organique (kg/sem)": organique,
			"Gestion plastique": gestion_plastique,
			"Gestion organique": gestion_organique,
			"Tri": tri,
			"Observations": observations,
		}])
		ligne.to_csv(FICHIER, mode="a", header=not os.path.exists(FICHIER), index=False)
		st.success("Données enregistrées !")

# ---------- Affichage et analyse ----------
st.divider()
if os.path.exists(FICHIER):
	df = pd.read_csv(FICHIER)

	st.subheader("📊 Résumé")
	m1, m2, m3, m4 = st.columns(4)
	m1.metric("Ménages enquêtés", len(df))
	m2.metric("Arbres plantés", int(df["Arbres plantés"].sum()))
	m3.metric("Plastique total (kg/sem)", round(df["Plastique (kg/sem)"].sum(), 1))
	m4.metric("Organique total (kg/sem)", round(df["Organique (kg/sem)"].sum(), 1))

	g1, g2 = st.columns(2)
	g1.write("**Gestion des déchets plastiques**")
	g1.bar_chart(df["Gestion plastique"].value_counts())
	g2.write("**Gestion des déchets organiques**")
	g2.bar_chart(df["Gestion organique"].value_counts())

	st.subheader("🗂️ Toutes les données")
	st.dataframe(df, use_container_width=True)

	st.download_button(
		"⬇️ Télécharger en CSV",
		df.to_csv(index=False).encode("utf-8"),
		"donnees_reboisement_dechets.csv",
		"text/csv",
	)
else:
	st.info("Aucune donnée enregistrée pour le moment.")
