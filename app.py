import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from io import StringIO


# ============================================================
# 1. CONFIGURATION DE L'APPLICATION
# ============================================================

st.set_page_config(
    page_title="BETON INSIGHT PRO",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# 2. DESIGN GLOBAL + RESPONSIVE MOBILE
# ============================================================

st.html(
    """
    <style>

    /* ======================================================
       COULEURS
    ====================================================== */

    :root {
        --bg: #07111F;
        --sidebar: #091525;

        --card: #101F33;
        --card-light: #152941;

        --border: #2C435C;

        --white: #FFFFFF;
        --text: #E2E8F0;
        --muted: #AFC0D0;

        --cyan: #38BDF8;
        --cyan-light: #7DD3FC;

        --green: #34D399;
        --yellow: #FBBF24;
        --red: #FB7185;
    }


    /* ======================================================
       APPLICATION
    ====================================================== */

    html,
    body {
        font-family: "Segoe UI", Arial, sans-serif;
    }

    .stApp {
        background: #07111F;
        color: #E2E8F0;
    }

    h1,
    h2,
    h3,
    h4,
    h5,
    h6 {
        color: #FFFFFF !important;
    }

    p {
        color: #E2E8F0;
    }


    /* ======================================================
       SIDEBAR
    ====================================================== */

    section[data-testid="stSidebar"] {
        background: #091525;
        border-right: 1px solid #2C435C;
    }

    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p {
        color: #E2E8F0 !important;
    }

    .sidebar-logo {
        color: #FFFFFF;
        font-size: 24px;
        font-weight: 900;
        letter-spacing: -0.5px;
    }

    .sidebar-logo span {
        color: #38BDF8;
    }

    .sidebar-caption {
        color: #AFC0D0;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1.4px;
        margin-top: 4px;
        margin-bottom: 15px;
    }


    /* ======================================================
       HERO
    ====================================================== */

    .hero {
        background:
            linear-gradient(
                135deg,
                #102945,
                #101F33
            );

        border: 1px solid #2C435C;

        border-radius: 22px;

        padding: 34px 38px;

        margin-bottom: 28px;

        box-shadow:
            0 18px 40px rgba(0, 0, 0, 0.28);
    }

    .hero-eyebrow {
        color: #7DD3FC;

        font-size: 12px;

        font-weight: 800;

        letter-spacing: 2px;

        text-transform: uppercase;

        margin-bottom: 9px;
    }

    .hero-title {
        color: #FFFFFF;

        font-size: 45px;

        font-weight: 900;

        line-height: 1;

        letter-spacing: -1px;

        margin-bottom: 14px;
    }

    .hero-title span {
        color: #38BDF8;
    }

    .hero-subtitle {
        color: #D3DEE8;

        font-size: 16px;

        line-height: 1.6;

        max-width: 850px;
    }

    .hero-badges {
        margin-top: 20px;
    }

    .badge {
        display: inline-block;

        padding: 7px 12px;

        margin-right: 7px;

        margin-bottom: 6px;

        border-radius: 999px;

        background: #152941;

        border: 1px solid #38BDF8;

        color: #BAE6FD;

        font-size: 11px;

        font-weight: 700;
    }


    /* ======================================================
       TITRES
    ====================================================== */

    .eyebrow {
        color: #38BDF8;

        font-size: 11px;

        font-weight: 800;

        text-transform: uppercase;

        letter-spacing: 1.5px;

        margin-top: 8px;
    }

    .section-title {
        color: #FFFFFF;

        font-size: 26px;

        font-weight: 850;

        margin-top: 4px;

        margin-bottom: 16px;
    }

    .section-description {
        color: #AFC0D0;

        font-size: 14px;

        margin-top: -8px;

        margin-bottom: 20px;
    }


    /* ======================================================
       KPI
    ====================================================== */

    .kpi-card {
        background: #101F33;

        border: 1px solid #2C435C;

        border-top: 3px solid #38BDF8;

        border-radius: 17px;

        padding: 21px;

        min-height: 135px;

        box-shadow:
            0 12px 28px rgba(0, 0, 0, 0.22);
    }

    .kpi-label {
        color: #AFC0D0;

        font-size: 11px;

        font-weight: 800;

        text-transform: uppercase;

        letter-spacing: 1px;

        margin-bottom: 10px;
    }

    .kpi-value {
        color: #FFFFFF;

        font-size: 33px;

        font-weight: 900;
    }

    .kpi-unit {
        color: #A3B4C5;

        font-size: 12px;

        margin-top: 5px;
    }


    /* ======================================================
       CARTES
    ====================================================== */

    .glass-card {
        background: #101F33;

        border: 1px solid #2C435C;

        border-radius: 18px;

        padding: 23px;

        margin-bottom: 16px;

        box-shadow:
            0 12px 30px rgba(0, 0, 0, 0.20);
    }

    .micro-label {
        color: #A3B4C5;

        font-size: 10px;

        font-weight: 800;

        text-transform: uppercase;

        letter-spacing: 1.4px;
    }

    .major-number {
        color: #FFFFFF;

        font-size: 41px;

        font-weight: 900;

        margin-top: 8px;
    }

    .small-note {
        color: #C0CCD8;

        font-size: 12px;

        line-height: 1.5;

        margin-top: 8px;
    }


    /* ======================================================
       MODELE
    ====================================================== */

    .model-card {
        background: #102945;

        border: 1px solid #38BDF8;

        border-radius: 19px;

        padding: 25px;

        margin-bottom: 20px;
    }

    .model-title {
        color: #7DD3FC;

        font-size: 11px;

        font-weight: 800;

        text-transform: uppercase;

        letter-spacing: 1.5px;
    }

    .model-equation {
        color: #FFFFFF;

        font-size: 23px;

        font-weight: 850;

        margin-top: 12px;

        margin-bottom: 8px;

        line-height: 1.5;
    }

    .model-subtitle {
        color: #C0CCD8;

        font-size: 12px;
    }


    /* ======================================================
       STATUTS
    ====================================================== */

    .status-success {
        background: #10372F;

        border: 1px solid #34D399;

        color: #A7F3D0;

        padding: 18px;

        border-radius: 15px;

        font-weight: 800;

        line-height: 1.5;
    }

    .status-warning {
        background: #3B3011;

        border: 1px solid #FBBF24;

        color: #FDE68A;

        padding: 18px;

        border-radius: 15px;

        font-weight: 800;

        line-height: 1.5;
    }

    .status-danger {
        background: #421A26;

        border: 1px solid #FB7185;

        color: #FECDD3;

        padding: 18px;

        border-radius: 15px;

        font-weight: 800;

        line-height: 1.5;
    }


    /* ======================================================
       JAUGE
    ====================================================== */

    .gauge-container {
        display: flex;

        flex-direction: column;

        align-items: center;

        justify-content: center;

        padding: 15px;
    }

    .gauge {
        width: 185px;

        height: 185px;

        border-radius: 50%;

        display: flex;

        align-items: center;

        justify-content: center;
    }

    .gauge-inner {
        width: 140px;

        height: 140px;

        border-radius: 50%;

        background: #07111F;

        border: 1px solid #2C435C;

        display: flex;

        align-items: center;

        justify-content: center;

        flex-direction: column;
    }

    .gauge-value {
        color: #FFFFFF;

        font-size: 35px;

        font-weight: 900;
    }

    .gauge-text {
        color: #A3B4C5;

        font-size: 11px;

        text-transform: uppercase;

        letter-spacing: 1px;
    }


    /* ======================================================
       STREAMLIT METRICS
    ====================================================== */

    div[data-testid="stMetric"] {
        background: #101F33;

        border: 1px solid #2C435C;

        border-radius: 15px;

        padding: 18px;
    }

    div[data-testid="stMetric"] label {
        color: #AFC0D0 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #FFFFFF !important;
    }


    /* ======================================================
       INPUTS
    ====================================================== */

    div[data-baseweb="input"] > div {
        background: #101F33 !important;

        border: 1px solid #3C5570 !important;

        color: #FFFFFF !important;
    }

    input {
        color: #FFFFFF !important;

        caret-color: #38BDF8 !important;
    }

    textarea {
        background: #101F33 !important;

        color: #FFFFFF !important;

        border: 1px solid #3C5570 !important;

        border-radius: 10px !important;
    }

    input::placeholder,
    textarea::placeholder {
        color: #8EA1B4 !important;
    }


    /* ======================================================
       SELECTBOX
    ====================================================== */

    div[data-baseweb="select"] > div {
        background: #101F33 !important;

        border: 1px solid #3C5570 !important;

        color: #FFFFFF !important;
    }

    div[data-baseweb="select"] span {
        color: #FFFFFF !important;
    }

    ul[role="listbox"] {
        background: #101F33 !important;

        border: 1px solid #3C5570 !important;
    }

    li[role="option"] {
        color: #FFFFFF !important;

        background: #101F33 !important;
    }

    li[role="option"]:hover {
        background: #19324D !important;
    }


    /* ======================================================
       RADIO
    ====================================================== */

    div[role="radiogroup"] label,
    div[role="radiogroup"] p {
        color: #E2E8F0 !important;
    }


    /* ======================================================
       BOUTONS
    ====================================================== */

    .stButton > button,
    .stDownloadButton > button {

        width: 100%;

        min-height: 47px;

        border-radius: 11px;

        border: 1px solid #38BDF8;

        background: #087CA7;

        color: #FFFFFF !important;

        font-weight: 800;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {

        background: #1299CE;

        border-color: #7DD3FC;

        color: #FFFFFF !important;
    }


    /* ======================================================
       DATAFRAME
    ====================================================== */

    div[data-testid="stDataFrame"] {
        border: 1px solid #2C435C;

        border-radius: 15px;

        overflow: hidden;
    }


    /* ======================================================
       EXPANDERS
    ====================================================== */

    details {
        background: #101F33 !important;

        border: 1px solid #2C435C !important;

        border-radius: 12px !important;
    }

    details summary {
        color: #FFFFFF !important;
    }


    /* ======================================================
       FILE UPLOADER
    ====================================================== */

    section[data-testid="stFileUploaderDropzone"] {
        background: #101F33 !important;

        border: 1px dashed #38BDF8 !important;
    }

    section[data-testid="stFileUploaderDropzone"] span,
    section[data-testid="stFileUploaderDropzone"] small {
        color: #DCE7F2 !important;
    }


    /* ======================================================
       DIVIDERS
    ====================================================== */

    hr {
        border-color: #2C435C !important;
    }


    /* ======================================================
       VERSION MOBILE
    ====================================================== */

    @media (max-width: 768px) {

        /* Réduction des marges principales */

        .block-container {
            padding-left: 14px !important;
            padding-right: 14px !important;
            padding-top: 20px !important;
        }


        /* HERO */

        .hero {
            padding: 22px 18px;

            border-radius: 16px;

            margin-bottom: 20px;
        }

        .hero-eyebrow {
            font-size: 9px;

            letter-spacing: 1.4px;
        }

        .hero-title {
            font-size: 30px;

            line-height: 1.1;

            letter-spacing: -0.5px;
        }

        .hero-subtitle {
            font-size: 13px;

            line-height: 1.5;
        }

        .hero-badges {
            margin-top: 14px;
        }

        .badge {
            font-size: 9px;

            padding: 5px 8px;

            margin-right: 4px;
        }


        /* TITRES */

        .eyebrow {
            font-size: 9px;
        }

        .section-title {
            font-size: 21px;

            margin-bottom: 12px;
        }

        .section-description {
            font-size: 12px;

            line-height: 1.5;
        }


        /* CARTES KPI */

        .kpi-card {
            min-height: 105px;

            padding: 15px;

            border-radius: 14px;
        }

        .kpi-label {
            font-size: 9px;
        }

        .kpi-value {
            font-size: 27px;
        }

        .kpi-unit {
            font-size: 10px;
        }


        /* CARTES */

        .glass-card {
            padding: 16px;

            border-radius: 14px;
        }

        .micro-label {
            font-size: 9px;
        }

        .major-number {
            font-size: 32px;
        }

        .small-note {
            font-size: 11px;
        }


        /* MODELE */

        .model-card {
            padding: 17px;

            border-radius: 14px;
        }

        .model-title {
            font-size: 9px;
        }

        .model-equation {
            font-size: 17px;

            line-height: 1.55;
        }


        /* JAUGE */

        .gauge {
            width: 150px;

            height: 150px;
        }

        .gauge-inner {
            width: 112px;

            height: 112px;
        }

        .gauge-value {
            font-size: 28px;
        }

        .gauge-text {
            font-size: 9px;
        }


        /* BOUTONS */

        .stButton > button,
        .stDownloadButton > button {
            min-height: 44px;

            font-size: 12px;
        }


        /* ===============================
           COLONNES RESPONSIVES

           Sur téléphone, les colonnes
           deviennent verticales.
        =============================== */

        div[data-testid="stHorizontalBlock"] {
            flex-wrap: wrap !important;
        }

        div[data-testid="column"] {
            width: 100% !important;

            flex: 1 1 100% !important;

            min-width: 100% !important;
        }


        /* TABLEAUX */

        div[data-testid="stDataFrame"] {
            font-size: 11px;
        }

    }


    /* ======================================================
       TRÈS PETITS TÉLÉPHONES
    ====================================================== */

    @media (max-width: 420px) {

        .hero-title {
            font-size: 27px;
        }

        .section-title {
            font-size: 19px;
        }

        .kpi-value {
            font-size: 25px;
        }

        .major-number {
            font-size: 29px;
        }

        .model-equation {
            font-size: 15px;
        }

    }

    </style>
    """
)


# ============================================================
# 3. FONCTIONS D'AFFICHAGE
# ============================================================

def titre_section(surtitre, titre, description=None):

    html = f"""
    <div class="eyebrow">
        {surtitre}
    </div>

    <div class="section-title">
        {titre}
    </div>
    """

    if description:

        html += f"""
        <div class="section-description">
            {description}
        </div>
        """

    st.html(html)


def carte_kpi(label, valeur, unite=""):

    st.html(
        f"""
        <div class="kpi-card">

            <div class="kpi-label">
                {label}
            </div>

            <div class="kpi-value">
                {valeur}
            </div>

            <div class="kpi-unit">
                {unite}
            </div>

        </div>
        """
    )


def carte_nombre(label, valeur, note=""):

    st.html(
        f"""
        <div class="glass-card">

            <div class="micro-label">
                {label}
            </div>

            <div class="major-number">
                {valeur}
            </div>

            <div class="small-note">
                {note}
            </div>

        </div>
        """
    )


def style_graphique(fig, ax):

    fig.patch.set_facecolor(
        "#101F33"
    )

    ax.set_facecolor(
        "#101F33"
    )

    ax.tick_params(
        colors="#CBD5E1"
    )

    ax.xaxis.label.set_color(
        "#E2E8F0"
    )

    ax.yaxis.label.set_color(
        "#E2E8F0"
    )

    ax.title.set_color(
        "#FFFFFF"
    )

    for spine in ax.spines.values():

        spine.set_color(
            "#3C5570"
        )

    ax.grid(
        color="#3C5570",
        alpha=0.30
    )


# ============================================================
# 4. FONCTIONS STATISTIQUES
# ============================================================

def regression_simple(x, y):

    x = np.asarray(
        x,
        dtype=float
    )

    y = np.asarray(
        y,
        dtype=float
    )


    if len(x) < 2:

        return None


    if np.std(x) == 0:

        return None


    a, b = np.polyfit(
        x,
        y,
        1
    )


    prediction = (
        a * x + b
    )


    ss_res = np.sum(
        (
            y - prediction
        ) ** 2
    )


    ss_tot = np.sum(
        (
            y - np.mean(y)
        ) ** 2
    )


    r2 = (
        1 - ss_res / ss_tot
        if ss_tot > 0
        else 0
    )


    correlation = np.corrcoef(
        x,
        y
    )[0, 1]


    mae = np.mean(
        np.abs(
            y - prediction
        )
    )


    rmse = np.sqrt(
        np.mean(
            (
                y - prediction
            ) ** 2
        )
    )


    return {

        "a":
        a,

        "b":
        b,

        "pred":
        prediction,

        "r2":
        r2,

        "corr":
        correlation,

        "mae":
        mae,

        "rmse":
        rmse
    }


def regression_multiple(ec, dosage, y):

    ec = np.asarray(
        ec,
        dtype=float
    )

    dosage = np.asarray(
        dosage,
        dtype=float
    )

    y = np.asarray(
        y,
        dtype=float
    )


    if len(y) < 3:

        return None


    X = np.column_stack(
        [
            np.ones(
                len(y)
            ),

            ec,

            dosage
        ]
    )


    coefficients = np.linalg.lstsq(
        X,
        y,
        rcond=None
    )[0]


    prediction = (
        X @ coefficients
    )


    ss_res = np.sum(
        (
            y - prediction
        ) ** 2
    )


    ss_tot = np.sum(
        (
            y - np.mean(y)
        ) ** 2
    )


    r2 = (
        1 - ss_res / ss_tot
        if ss_tot > 0
        else 0
    )


    mae = np.mean(
        np.abs(
            y - prediction
        )
    )


    rmse = np.sqrt(
        np.mean(
            (
                y - prediction
            ) ** 2
        )
    )


    rang = np.linalg.matrix_rank(
        X
    )


    return {

        "beta0":
        coefficients[0],

        "beta1":
        coefficients[1],

        "beta2":
        coefficients[2],

        "pred":
        prediction,

        "r2":
        r2,

        "mae":
        mae,

        "rmse":
        rmse,

        "rang":
        rang
    }


# ============================================================
# 5. SESSION
# ============================================================

if "analyse" not in st.session_state:

    st.session_state.analyse = None


# ============================================================
# 6. SIDEBAR
# ============================================================

with st.sidebar:

    st.html(
        """
        <div class="sidebar-logo">
            BETON <span>INSIGHT</span>
        </div>

        <div class="sidebar-caption">
            Structural Materials Intelligence
        </div>
        """
    )


    st.divider()


    page = st.radio(
        "Navigation",
        [
            "▣ Vue d'ensemble",
            "◫ Données",
            "◉ Statistiques",
            "⌁ Modélisation",
            "◇ Simulateur",
            "▤ Rapport",
            "ⓘ Méthodologie"
        ],
        label_visibility="collapsed"
    )


    st.divider()


    st.subheader(
        "Configuration"
    )


    mode_source = st.radio(
        "Source des données",
        [
            "Saisie manuelle",
            "Importer un fichier"
        ]
    )


    dataframe_importe = None

    colonne_resistance = None

    fichier = None


    # ========================================================
    # SAISIE MANUELLE
    # ========================================================

    if mode_source == "Saisie manuelle":

        texte_resistances = st.text_area(
            "Résistances à 28 jours (MPa)",
            value="24,26,27,25,28,29,23,27,26,30",
            height=110,
            help="Séparez les valeurs par des virgules."
        )


    # ========================================================
    # IMPORTATION
    # ========================================================

    else:

        fichier = st.file_uploader(
            "Importer un fichier Excel ou CSV",
            type=[
                "xlsx",
                "csv"
            ]
        )


        if fichier is not None:

            try:

                if fichier.name.lower().endswith(
                    ".csv"
                ):

                    dataframe_importe = pd.read_csv(
                        fichier
                    )

                else:

                    dataframe_importe = pd.read_excel(
                        fichier
                    )


                liste_colonnes = (
                    dataframe_importe
                    .columns
                    .tolist()
                )


                index_defaut = 0


                if (
                    "Resistance_28j_MPa"
                    in liste_colonnes
                ):

                    index_defaut = (
                        liste_colonnes.index(
                            "Resistance_28j_MPa"
                        )
                    )


                colonne_resistance = st.selectbox(
                    "Colonne contenant les résistances",
                    liste_colonnes,
                    index=index_defaut
                )


                st.success(
                    "Fichier chargé avec succès."
                )


            except Exception as erreur:

                st.error(
                    f"Erreur de lecture : {erreur}"
                )


    seuil = st.number_input(
        "Seuil de référence (MPa)",
        min_value=0.0,
        value=25.0,
        step=0.5
    )


    bouton_analyser = st.button(
        "⚡ ANALYSER LES DONNÉES"
    )


    st.divider()


    st.caption(
        "BETON INSIGHT PRO • Projet académique"
    )


# ============================================================
# 7. TRAITEMENT
# ============================================================

if bouton_analyser:

    try:

        # =====================================================
        # RÉCUPÉRATION DES RÉSISTANCES
        # =====================================================

        if mode_source == "Saisie manuelle":

            resistances = [
                float(x.strip())
                for x
                in texte_resistances
                .replace(
                    "\n",
                    ","
                )
                .split(",")
                if x.strip()
            ]


            dataframe_brut = pd.DataFrame(
                {
                    "Resistance_28j_MPa":
                    resistances
                }
            )


        else:

            if dataframe_importe is None:

                st.error(
                    "Veuillez importer un fichier."
                )

                st.stop()


            resistances = (
                pd.to_numeric(
                    dataframe_importe[
                        colonne_resistance
                    ],
                    errors="coerce"
                )
                .dropna()
                .tolist()
            )


            dataframe_brut = (
                dataframe_importe
                .copy()
            )


        if len(
            resistances
        ) == 0:

            st.error(
                "Aucune résistance exploitable."
            )

            st.stop()


        # =====================================================
        # STATISTIQUES DESCRIPTIVES
        # =====================================================

        serie = pd.Series(
            resistances,
            dtype=float
        )


        n = len(
            serie
        )


        moyenne = serie.mean()

        mediane = serie.median()

        minimum = serie.min()

        maximum = serie.max()


        ecart_type = (
            serie.std()
            if n > 1
            else 0
        )


        variance = (
            serie.var()
            if n > 1
            else 0
        )


        coefficient_variation = (
            ecart_type
            / moyenne
            * 100
            if moyenne != 0
            else 0
        )


        # =====================================================
        # ANALYSE PAR RAPPORT AU SEUIL
        # =====================================================

        conformes = sum(
            valeur >= seuil
            for valeur
            in resistances
        )


        non_conformes = (
            n - conformes
        )


        taux = (
            conformes
            / n
            * 100
        )


        # =====================================================
        # PROBABILITÉS
        # =====================================================

        if ecart_type > 0:

            z = (
                seuil - moyenne
            ) / (
                ecart_type
                * math.sqrt(2)
            )


            probabilite_sous_seuil = (
                0.5
                * (
                    1
                    + math.erf(z)
                )
            )


        else:

            probabilite_sous_seuil = (
                0
                if moyenne >= seuil
                else 1
            )


        probabilite_sur_seuil = (
            1
            - probabilite_sous_seuil
        )


        # =====================================================
        # TABLEAU DÉTAILLÉ
        # =====================================================

        details = pd.DataFrame(
            {

                "Essai":
                range(
                    1,
                    n + 1
                ),

                "Résistance (MPa)":
                resistances,

                "Écart au seuil (MPa)":
                [
                    round(
                        valeur - seuil,
                        2
                    )
                    for valeur
                    in resistances
                ],

                "Statut":
                [
                    "Au-dessus du seuil"
                    if valeur >= seuil
                    else "Sous le seuil"
                    for valeur
                    in resistances
                ]
            }
        )


        # =====================================================
        # MODÉLISATION
        # =====================================================

        donnees_modele = None

        modele_ec = None

        modele_dosage = None

        modele_multiple = None


        colonnes_avancees = [

            "Rapport_EC",

            "Dosage_ciment_kg_m3",

            "Resistance_28j_MPa"
        ]


        if (
            dataframe_importe is not None
            and
            all(
                col in dataframe_importe.columns
                for col
                in colonnes_avancees
            )
        ):


            donnees_modele = pd.DataFrame(
                {

                    "Rapport_EC":
                    pd.to_numeric(
                        dataframe_importe[
                            "Rapport_EC"
                        ],
                        errors="coerce"
                    ),

                    "Dosage":
                    pd.to_numeric(
                        dataframe_importe[
                            "Dosage_ciment_kg_m3"
                        ],
                        errors="coerce"
                    ),

                    "Resistance":
                    pd.to_numeric(
                        dataframe_importe[
                            "Resistance_28j_MPa"
                        ],
                        errors="coerce"
                    )
                }
            ).dropna()


            if len(
                donnees_modele
            ) >= 3:


                y = donnees_modele[
                    "Resistance"
                ].values


                ec = donnees_modele[
                    "Rapport_EC"
                ].values


                dosage = donnees_modele[
                    "Dosage"
                ].values


                modele_ec = regression_simple(
                    ec,
                    y
                )


                modele_dosage = regression_simple(
                    dosage,
                    y
                )


                modele_multiple = regression_multiple(
                    ec,
                    dosage,
                    y
                )


        # =====================================================
        # ENREGISTREMENT DANS SESSION STATE
        # =====================================================

        st.session_state.analyse = {

            "dataframe":
            dataframe_brut,

            "resistances":
            resistances,

            "details":
            details,

            "n":
            n,

            "moyenne":
            moyenne,

            "mediane":
            mediane,

            "minimum":
            minimum,

            "maximum":
            maximum,

            "ecart_type":
            ecart_type,

            "variance":
            variance,

            "cv":
            coefficient_variation,

            "seuil":
            seuil,

            "conformes":
            conformes,

            "non_conformes":
            non_conformes,

            "taux":
            taux,

            "p_sous":
            probabilite_sous_seuil,

            "p_sur":
            probabilite_sur_seuil,

            "donnees_modele":
            donnees_modele,

            "modele_ec":
            modele_ec,

            "modele_dosage":
            modele_dosage,

            "modele_multiple":
            modele_multiple
        }


    except ValueError:

        st.error(
            """
            Vérifiez la saisie des résistances.

            Utilisez par exemple :

            24,26,27,25,28,29
            """
        )


    except Exception as erreur:

        st.error(
            f"Une erreur est survenue : {erreur}"
        )


# ============================================================
# 8. RÉSULTATS DE SESSION
# ============================================================

R = st.session_state.analyse


# ============================================================
# 9. EN-TÊTE PRINCIPAL
# ============================================================

st.html(
    """
    <div class="hero">

        <div class="hero-eyebrow">
            Structural Materials Intelligence
        </div>

        <div class="hero-title">
            BETON <span>INSIGHT</span> PRO
        </div>

        <div class="hero-subtitle">

            Plateforme d'aide à l'analyse statistique,
            probabiliste et prédictive des performances
            du béton à 28 jours.

        </div>

        <div class="hero-badges">

            <span class="badge">
                STATISTIQUES
            </span>

            <span class="badge">
                PROBABILITÉS
            </span>

            <span class="badge">
                RÉGRESSION
            </span>

            <span class="badge">
                GÉNIE CIVIL
            </span>

        </div>

    </div>
    """
)


# ============================================================
# 10. PAGE : VUE D'ENSEMBLE
# ============================================================

if page == "▣ Vue d'ensemble":


    if R is None:

        titre_section(
            "Bienvenue",
            "Centre d'analyse",
            "Configurez les données dans le menu puis lancez l'analyse."
        )


        st.info(
            "Aucune analyse active pour le moment."
        )


    else:

        titre_section(
            "Overview",
            "Vue générale du lot",
            "Synthèse des principaux indicateurs statistiques."
        )


        # =====================================================
        # KPI
        # =====================================================

        c1, c2, c3, c4 = st.columns(4)


        with c1:

            carte_kpi(
                "Échantillon",
                R["n"],
                "essais"
            )


        with c2:

            carte_kpi(
                "Résistance moyenne",
                f'{R["moyenne"]:.2f}',
                "MPa"
            )


        with c3:

            carte_kpi(
                "Au-dessus du seuil",
                f'{R["taux"]:.1f}%',
                f'Seuil : {R["seuil"]:.1f} MPa'
            )


        with c4:

            carte_kpi(
                "Risque estimé",
                f'{R["p_sous"] * 100:.1f}%',
                "sous hypothèse normale"
            )


        st.write("")


        # =====================================================
        # HISTOGRAMME + JAUGE
        # =====================================================

        gauche, droite = st.columns(
            [2, 1]
        )


        with gauche:

            titre_section(
                "Distribution",
                "Profil des résistances"
            )


            fig, ax = plt.subplots(
                figsize=(9, 4.5)
            )


            style_graphique(
                fig,
                ax
            )


            nombre_classes = min(
                8,
                max(
                    3,
                    int(
                        math.sqrt(
                            R["n"]
                        )
                    )
                )
            )


            ax.hist(
                R["resistances"],

                bins=nombre_classes,

                color="#0EA5E9",

                edgecolor="#BAE6FD",

                alpha=0.90
            )


            ax.axvline(
                R["seuil"],

                color="#FBBF24",

                linestyle="--",

                linewidth=2.5,

                label=f'Seuil {R["seuil"]:.1f} MPa'
            )


            ax.axvline(
                R["moyenne"],

                color="#34D399",

                linewidth=2.5,

                label=f'Moyenne {R["moyenne"]:.2f} MPa'
            )


            ax.set_xlabel(
                "Résistance à 28 jours (MPa)"
            )


            ax.set_ylabel(
                "Effectif"
            )


            ax.set_title(
                "Distribution expérimentale"
            )


            legende = ax.legend(
                frameon=False
            )


            for texte in legende.get_texts():

                texte.set_color(
                    "#E2E8F0"
                )


            fig.tight_layout()


            st.pyplot(
                fig,
                use_container_width=True
            )


            plt.close(
                fig
            )


        with droite:

            titre_section(
                "Quality index",
                "Position par rapport au seuil"
            )


            pourcentage = max(
                0,
                min(
                    100,
                    float(
                        R["taux"]
                    )
                )
            )


            angle = (
                pourcentage
                * 3.6
            )


            st.html(
                f"""
                <div class="glass-card">

                    <div class="gauge-container">

                        <div
                            class="gauge"

                            style="
                            background:
                            conic-gradient(
                                #38BDF8 0deg {angle}deg,
                                #2C435C {angle}deg 360deg
                            );
                            "
                        >

                            <div class="gauge-inner">

                                <div class="gauge-value">
                                    {pourcentage:.0f}%
                                </div>

                                <div class="gauge-text">
                                    ≥ seuil
                                </div>

                            </div>

                        </div>

                        <div class="small-note">

                            {R["conformes"]} / {R["n"]}
                            essais atteignent le seuil
                            de référence.

                        </div>

                    </div>

                </div>
                """
            )


            if R[
                "non_conformes"
            ] == 0:

                st.html(
                    """
                    <div class="status-success">

                        ✓ Toutes les valeurs sont
                        au-dessus ou égales au seuil.

                    </div>
                    """
                )


            else:

                st.html(
                    f"""
                    <div class="status-warning">

                        ⚠ {R["non_conformes"]}
                        essai(s) sont sous
                        le seuil de référence.

                    </div>
                    """
                )


        # =====================================================
        # RÉSUMÉ STATISTIQUE
        # =====================================================

        titre_section(
            "Statistical snapshot",
            "Résumé statistique"
        )


        r1, r2, r3, r4 = st.columns(4)


        r1.metric(
            "Minimum",
            f'{R["minimum"]:.2f} MPa'
        )


        r2.metric(
            "Maximum",
            f'{R["maximum"]:.2f} MPa'
        )


        r3.metric(
            "Médiane",
            f'{R["mediane"]:.2f} MPa'
        )


        r4.metric(
            "Coefficient de variation",
            f'{R["cv"]:.2f}%'
        )


        if R[
            "non_conformes"
        ] > 0:

            st.info(
                f"""
                {R["non_conformes"]} valeur(s)
                sont inférieures au seuil de
                {R["seuil"]:.2f} MPa.

                Cette conclusion est statistique.
                L'acceptation réglementaire d'un béton
                dépend des normes et prescriptions du projet.
                """
            )


# ============================================================
# 11. PAGE : DONNÉES
# ============================================================

elif page == "◫ Données":


    titre_section(
        "Data management",
        "Jeu de données",
        "Visualisation des observations utilisées dans l'analyse."
    )


    if R is None:

        st.info(
            "Lancez une analyse pour afficher les données."
        )


    else:

        d1, d2, d3 = st.columns(3)


        d1.metric(
            "Observations",
            R["n"]
        )


        d2.metric(
            "Valeurs ≥ seuil",
            R["conformes"]
        )


        d3.metric(
            "Valeurs < seuil",
            R["non_conformes"]
        )


        st.subheader(
            "Données originales"
        )


        st.dataframe(
            R["dataframe"],
            use_container_width=True,
            hide_index=True
        )


        st.subheader(
            "Tableau de contrôle"
        )


        st.dataframe(
            R["details"],
            use_container_width=True,
            hide_index=True
        )


        csv = (
            R["details"]
            .to_csv(
                index=False
            )
            .encode(
                "utf-8"
            )
        )


        st.download_button(
            "↓ Exporter les résultats CSV",
            csv,
            file_name="beton_insight_donnees.csv",
            mime="text/csv"
        )


# ============================================================
# 12. PAGE : STATISTIQUES
# ============================================================

elif page == "◉ Statistiques":


    titre_section(
        "Statistical analysis",
        "Analyse statistique",
        "Dispersion, distribution et analyse probabiliste."
    )


    if R is None:

        st.info(
            "Lancez d'abord une analyse."
        )


    else:

        a1, a2, a3, a4 = st.columns(4)


        a1.metric(
            "Moyenne",
            f'{R["moyenne"]:.2f} MPa'
        )


        a2.metric(
            "Écart-type",
            f'{R["ecart_type"]:.2f} MPa'
        )


        a3.metric(
            "Variance",
            f'{R["variance"]:.2f}'
        )


        a4.metric(
            "CV",
            f'{R["cv"]:.2f}%'
        )


        st.write("")


        gauche, droite = st.columns(2)


        # =====================================================
        # BOÎTE À MOUSTACHES
        # =====================================================

        with gauche:

            fig, ax = plt.subplots(
                figsize=(7, 4.5)
            )


            style_graphique(
                fig,
                ax
            )


            ax.boxplot(
                R["resistances"],

                vert=False,

                patch_artist=True,

                boxprops=dict(
                    facecolor="#0EA5E9",
                    edgecolor="#BAE6FD"
                ),

                medianprops=dict(
                    color="#34D399",
                    linewidth=2.5
                ),

                whiskerprops=dict(
                    color="#CBD5E1"
                ),

                capprops=dict(
                    color="#CBD5E1"
                ),

                flierprops=dict(
                    markerfacecolor="#FB7185",
                    markeredgecolor="#FB7185"
                )
            )


            ax.axvline(
                R["seuil"],

                color="#FBBF24",

                linestyle="--",

                linewidth=2,

                label="Seuil"
            )


            ax.set_xlabel(
                "Résistance (MPa)"
            )


            ax.set_title(
                "Boîte à moustaches"
            )


            fig.tight_layout()


            st.pyplot(
                fig,
                use_container_width=True
            )


            plt.close(
                fig
            )


        # =====================================================
        # PROBABILITÉS
        # =====================================================

        with droite:

            carte_nombre(
                "Probabilité estimée R ≥ seuil",

                f'{R["p_sur"] * 100:.1f}%',

                f'Seuil étudié : {R["seuil"]:.1f} MPa'
            )


            carte_nombre(
                "Probabilité estimée R < seuil",

                f'{R["p_sous"] * 100:.1f}%',

                "Calcul sous hypothèse de normalité."
            )


        st.warning(
            """
            Ces probabilités reposent sur une hypothèse
            de distribution approximativement normale des résistances.
            """
        )


# ============================================================
# 13. PAGE : MODÉLISATION
# ============================================================

elif page == "⌁ Modélisation":


    titre_section(
        "Predictive analytics",
        "Comparaison des modèles",
        "Étude de l'influence du rapport E/C et du dosage en ciment."
    )


    if (
        R is None
        or
        R["donnees_modele"] is None
    ):

        st.warning(
            """
            Pour utiliser la modélisation, importez
            un fichier contenant les colonnes :

            - Rapport_EC
            - Dosage_ciment_kg_m3
            - Resistance_28j_MPa
            """
        )


    else:

        donnees = R[
            "donnees_modele"
        ]


        modele_ec = R[
            "modele_ec"
        ]


        modele_dosage = R[
            "modele_dosage"
        ]


        modele_multiple = R[
            "modele_multiple"
        ]


        # =====================================================
        # COMPARAISON DES MODELES
        # =====================================================

        c1, c2, c3 = st.columns(3)


        if modele_ec:

            with c1:

                carte_nombre(
                    "Modèle 01 — Rapport E/C",

                    f'{modele_ec["r2"]:.3f}',

                    "Coefficient R²"
                )


        if modele_dosage:

            with c2:

                carte_nombre(
                    "Modèle 02 — Dosage ciment",

                    f'{modele_dosage["r2"]:.3f}',

                    "Coefficient R²"
                )


        if modele_multiple:

            with c3:

                carte_nombre(
                    "Modèle 03 — Régression multiple",

                    f'{modele_multiple["r2"]:.3f}',

                    "Coefficient R²"
                )


        # =====================================================
        # MEILLEUR AJUSTEMENT
        # =====================================================

        liste_modeles = []


        if modele_ec:

            liste_modeles.append(
                (
                    "Rapport E/C",
                    modele_ec["r2"]
                )
            )


        if modele_dosage:

            liste_modeles.append(
                (
                    "Dosage ciment",
                    modele_dosage["r2"]
                )
            )


        if modele_multiple:

            liste_modeles.append(
                (
                    "Régression multiple",
                    modele_multiple["r2"]
                )
            )


        if liste_modeles:

            meilleur = max(
                liste_modeles,
                key=lambda x: x[1]
            )


            st.success(
                f"""
                Meilleur ajustement sur cet échantillon :
                **{meilleur[0]}**

                R² = **{meilleur[1]:.3f}**
                """
            )


        # =====================================================
        # MODELE MULTIPLE
        # =====================================================

        if modele_multiple:

            st.html(
                f"""
                <div class="model-card">

                    <div class="model-title">
                        Modèle prédictif principal
                    </div>

                    <div class="model-equation">

                        R =
                        {modele_multiple["beta0"]:.2f}

                        + ({modele_multiple["beta1"]:.2f} × E/C)

                        + ({modele_multiple["beta2"]:.4f} × Dosage)

                    </div>

                    <div class="model-subtitle">

                        R représente la résistance
                        estimée à 28 jours en MPa.

                    </div>

                </div>
                """
            )


            m1, m2, m3 = st.columns(3)


            m1.metric(
                "R²",
                f'{modele_multiple["r2"]:.3f}'
            )


            m2.metric(
                "MAE",
                f'{modele_multiple["mae"]:.2f} MPa'
            )


            m3.metric(
                "RMSE",
                f'{modele_multiple["rmse"]:.2f} MPa'
            )


            if modele_multiple[
                "rang"
            ] < 3:

                st.warning(
                    """
                    Les variables explicatives présentent
                    une dépendance importante.

                    Les coefficients β doivent donc être
                    interprétés avec prudence.
                    """
                )


        # =====================================================
        # GRAPHIQUES
        # =====================================================

        g1, g2 = st.columns(2)


        if modele_ec:

            with g1:

                x = donnees[
                    "Rapport_EC"
                ].values


                y = donnees[
                    "Resistance"
                ].values


                fig, ax = plt.subplots(
                    figsize=(6.5, 4.5)
                )


                style_graphique(
                    fig,
                    ax
                )


                ax.scatter(
                    x,
                    y,

                    color="#38BDF8",

                    s=60,

                    label="Observations"
                )


                ligne = np.linspace(
                    x.min(),
                    x.max(),
                    100
                )


                ax.plot(
                    ligne,

                    modele_ec["a"]
                    * ligne
                    + modele_ec["b"],

                    color="#34D399",

                    linewidth=2.5,

                    label="Régression"
                )


                ax.set_title(
                    "Rapport E/C → Résistance"
                )


                ax.set_xlabel(
                    "Rapport eau/ciment"
                )


                ax.set_ylabel(
                    "Résistance (MPa)"
                )


                legende = ax.legend(
                    frameon=False
                )


                for texte in legende.get_texts():

                    texte.set_color(
                        "#E2E8F0"
                    )


                fig.tight_layout()


                st.pyplot(
                    fig,
                    use_container_width=True
                )


                plt.close(
                    fig
                )


        if modele_dosage:

            with g2:

                x = donnees[
                    "Dosage"
                ].values


                y = donnees[
                    "Resistance"
                ].values


                fig, ax = plt.subplots(
                    figsize=(6.5, 4.5)
                )


                style_graphique(
                    fig,
                    ax
                )


                ax.scatter(
                    x,
                    y,

                    color="#38BDF8",

                    s=60,

                    label="Observations"
                )


                ligne = np.linspace(
                    x.min(),
                    x.max(),
                    100
                )


                ax.plot(
                    ligne,

                    modele_dosage["a"]
                    * ligne
                    + modele_dosage["b"],

                    color="#34D399",

                    linewidth=2.5,

                    label="Régression"
                )


                ax.set_title(
                    "Dosage ciment → Résistance"
                )


                ax.set_xlabel(
                    "Dosage ciment (kg/m³)"
                )


                ax.set_ylabel(
                    "Résistance (MPa)"
                )


                legende = ax.legend(
                    frameon=False
                )


                for texte in legende.get_texts():

                    texte.set_color(
                        "#E2E8F0"
                    )


                fig.tight_layout()


                st.pyplot(
                    fig,
                    use_container_width=True
                )


                plt.close(
                    fig
                )


        # =====================================================
        # OBSERVÉ VS PRÉDIT
        # =====================================================

        if modele_multiple:

            titre_section(
                "Model validation",
                "Résistances observées vs prédites"
            )


            y = donnees[
                "Resistance"
            ].values


            pred = modele_multiple[
                "pred"
            ]


            fig, ax = plt.subplots(
                figsize=(8, 5)
            )


            style_graphique(
                fig,
                ax
            )


            ax.scatter(
                y,
                pred,

                color="#38BDF8",

                s=65
            )


            minimum_graphique = min(
                y.min(),
                pred.min()
            )


            maximum_graphique = max(
                y.max(),
                pred.max()
            )


            ax.plot(
                [
                    minimum_graphique,
                    maximum_graphique
                ],

                [
                    minimum_graphique,
                    maximum_graphique
                ],

                color="#FBBF24",

                linestyle="--",

                linewidth=2,

                label="Prédiction parfaite"
            )


            ax.set_xlabel(
                "Résistance observée (MPa)"
            )


            ax.set_ylabel(
                "Résistance prédite (MPa)"
            )


            ax.set_title(
                "Performance du modèle multiple"
            )


            legende = ax.legend(
                frameon=False
            )


            for texte in legende.get_texts():

                texte.set_color(
                    "#E2E8F0"
                )


            fig.tight_layout()


            st.pyplot(
                fig,
                use_container_width=True
            )


            plt.close(
                fig
            )


        st.caption(
            """
            Un R² élevé indique un bon ajustement sur les
            données étudiées. Il ne garantit cependant pas
            automatiquement de bonnes performances sur
            de nouvelles données.
            """
        )


# ============================================================
# 14. PAGE : SIMULATEUR
# ============================================================

elif page == "◇ Simulateur":


    titre_section(
        "Engineering simulator",
        "Simulation prédictive",
        "Estimation expérimentale de la résistance du béton."
    )


    if (
        R is None
        or
        R["modele_multiple"] is None
    ):

        st.warning(
            """
            Importez d'abord des données comportant :

            - Rapport_EC
            - Dosage_ciment_kg_m3
            - Resistance_28j_MPa
            """
        )


    else:

        modele = R[
            "modele_multiple"
        ]


        st.html(
            f"""
            <div class="model-card">

                <div class="model-title">
                    Modèle actif
                </div>

                <div class="model-equation">

                    R =
                    {modele["beta0"]:.2f}

                    + ({modele["beta1"]:.2f} × E/C)

                    + ({modele["beta2"]:.4f} × Dosage)

                </div>

            </div>
            """
        )


        s1, s2 = st.columns(2)


        with s1:

            rapport_ec = st.slider(
                "Rapport eau/ciment E/C",
                min_value=0.20,
                max_value=0.80,
                value=0.50,
                step=0.01
            )


        with s2:

            dosage = st.slider(
                "Dosage ciment (kg/m³)",
                min_value=200,
                max_value=500,
                value=350,
                step=5
            )


        prediction = (
            modele["beta0"]
            +
            modele["beta1"]
            * rapport_ec
            +
            modele["beta2"]
            * dosage
        )


        ecart = (
            prediction
            - R["seuil"]
        )


        gauche, droite = st.columns(
            [2, 1]
        )


        with gauche:

            carte_nombre(
                "Résistance prédite",

                f"{prediction:.2f} MPa",

                "Estimation obtenue avec la régression multiple."
            )


        with droite:

            if prediction >= R[
                "seuil"
            ]:

                st.html(
                    f"""
                    <div class="status-success">

                        ✓ AU-DESSUS DU SEUIL

                        <br><br>

                        +{ecart:.2f} MPa

                    </div>
                    """
                )


            else:

                st.html(
                    f"""
                    <div class="status-danger">

                        ⚠ SOUS LE SEUIL

                        <br><br>

                        {ecart:.2f} MPa

                    </div>
                    """
                )


        st.warning(
            """
            Cette simulation est exploratoire.

            Elle ne constitue pas une formulation
            réglementaire du béton et ne doit pas être
            utilisée directement pour le dimensionnement
            d'un ouvrage.
            """
        )


# ============================================================
# 15. PAGE : RAPPORT
# ============================================================

elif page == "▤ Rapport":


    titre_section(
        "Reporting center",
        "Rapport automatique",
        "Synthèse exportable de l'analyse statistique."
    )


    if R is None:

        st.info(
            "Effectuez d'abord une analyse."
        )


    else:

        rapport = StringIO()


        rapport.write(
            "BETON INSIGHT PRO\n"
        )


        rapport.write(
            "ANALYSE STATISTIQUE ET PREDICTIVE DU BETON\n"
        )


        rapport.write(
            "==========================================\n\n"
        )


        # ----------------------------------------------------
        # STATISTIQUES
        # ----------------------------------------------------

        rapport.write(
            "1. STATISTIQUES DESCRIPTIVES\n"
        )


        rapport.write(
            "----------------------------\n"
        )


        rapport.write(
            f"Nombre d'essais : {R['n']}\n"
        )


        rapport.write(
            f"Moyenne : {R['moyenne']:.2f} MPa\n"
        )


        rapport.write(
            f"Médiane : {R['mediane']:.2f} MPa\n"
        )


        rapport.write(
            f"Ecart-type : {R['ecart_type']:.2f} MPa\n"
        )


        rapport.write(
            f"Variance : {R['variance']:.2f}\n"
        )


        rapport.write(
            f"Coefficient de variation : {R['cv']:.2f}%\n"
        )


        rapport.write(
            f"Minimum : {R['minimum']:.2f} MPa\n"
        )


        rapport.write(
            f"Maximum : {R['maximum']:.2f} MPa\n\n"
        )


        # ----------------------------------------------------
        # SEUIL
        # ----------------------------------------------------

        rapport.write(
            "2. ANALYSE PAR RAPPORT AU SEUIL\n"
        )


        rapport.write(
            "-------------------------------\n"
        )


        rapport.write(
            f"Seuil choisi : {R['seuil']:.2f} MPa\n"
        )


        rapport.write(
            f"Essais >= seuil : {R['conformes']}\n"
        )


        rapport.write(
            f"Essais < seuil : {R['non_conformes']}\n"
        )


        rapport.write(
            f"Taux >= seuil : {R['taux']:.2f}%\n\n"
        )


        # ----------------------------------------------------
        # PROBABILITÉS
        # ----------------------------------------------------

        rapport.write(
            "3. ANALYSE PROBABILISTE\n"
        )


        rapport.write(
            "-----------------------\n"
        )


        rapport.write(
            f"P(R >= seuil) = {R['p_sur'] * 100:.2f}%\n"
        )


        rapport.write(
            f"P(R < seuil) = {R['p_sous'] * 100:.2f}%\n\n"
        )


        # ----------------------------------------------------
        # MODELE
        # ----------------------------------------------------

        if R[
            "modele_multiple"
        ] is not None:

            modele = R[
                "modele_multiple"
            ]


            rapport.write(
                "4. MODELE PREDICTIF\n"
            )


            rapport.write(
                "-------------------\n"
            )


            rapport.write(
                f"R = {modele['beta0']:.3f} "
                f"+ ({modele['beta1']:.3f} x E/C) "
                f"+ ({modele['beta2']:.5f} x Dosage)\n"
            )


            rapport.write(
                f"R2 = {modele['r2']:.3f}\n"
            )


            rapport.write(
                f"MAE = {modele['mae']:.3f} MPa\n"
            )


            rapport.write(
                f"RMSE = {modele['rmse']:.3f} MPa\n\n"
            )


        # ----------------------------------------------------
        # CONCLUSION
        # ----------------------------------------------------

        rapport.write(
            "5. CONCLUSION\n"
        )


        rapport.write(
            "-------------\n"
        )


        if R[
            "non_conformes"
        ] == 0:

            rapport.write(
                "Toutes les valeurs analysees sont "
                "superieures ou egales au seuil choisi.\n"
            )


        else:

            rapport.write(
                f"{R['non_conformes']} essai(s) sur {R['n']} "
                "presentent une resistance inferieure au seuil.\n"
            )


        rapport.write(
            "\nCette conclusion est statistique. "
            "Une decision reglementaire doit s'appuyer "
            "sur les normes et prescriptions applicables."
        )


        texte_rapport = (
            rapport.getvalue()
        )


        st.text_area(
            "Aperçu du rapport",
            texte_rapport,
            height=480
        )


        c1, c2 = st.columns(2)


        with c1:

            st.download_button(
                "↓ Télécharger le rapport TXT",
                texte_rapport,
                file_name="BETON_INSIGHT_PRO_Rapport.txt",
                mime="text/plain"
            )


        with c2:

            csv = (
                R["details"]
                .to_csv(
                    index=False
                )
                .encode(
                    "utf-8"
                )
            )


            st.download_button(
                "↓ Télécharger les résultats CSV",
                csv,
                file_name="BETON_INSIGHT_PRO_Resultats.csv",
                mime="text/csv"
            )


# ============================================================
# 16. PAGE : MÉTHODOLOGIE
# ============================================================

elif page == "ⓘ Méthodologie":


    titre_section(
        "Knowledge base",
        "Méthodologie scientifique",
        "Comprendre les outils statistiques utilisés par l'application."
    )


    # ========================================================
    # MOYENNE
    # ========================================================

    with st.expander(
        "01 — Moyenne",
        expanded=True
    ):

        st.latex(
            r"""
            \bar{x}
            =
            \frac{1}{n}
            \sum_{i=1}^{n} x_i
            """
        )


        st.write(
            """
            La moyenne représente le niveau central
            des résistances mesurées.
            """
        )


    # ========================================================
    # VARIANCE
    # ========================================================

    with st.expander(
        "02 — Variance et écart-type"
    ):

        st.latex(
            r"""
            s^2
            =
            \frac{1}{n-1}
            \sum_{i=1}^{n}
            (x_i-\bar{x})^2
            """
        )


        st.latex(
            r"""
            s=\sqrt{s^2}
            """
        )


        st.write(
            """
            La variance et l'écart-type mesurent
            la dispersion des résistances autour
            de la moyenne.
            """
        )


    # ========================================================
    # CV
    # ========================================================

    with st.expander(
        "03 — Coefficient de variation"
    ):

        st.latex(
            r"""
            CV
            =
            \frac{s}{\bar{x}}
            \times 100
            """
        )


        st.write(
            """
            Le coefficient de variation permet
            de mesurer la dispersion relativement
            à la valeur moyenne.
            """
        )


    # ========================================================
    # LOI NORMALE
    # ========================================================

    with st.expander(
        "04 — Loi normale"
    ):

        st.latex(
            r"""
            X
            \sim
            \mathcal{N}
            (\mu,\sigma^2)
            """
        )


        st.write(
            """
            L'application utilise cette hypothèse
            pour estimer la probabilité qu'une
            résistance soit supérieure ou inférieure
            au seuil choisi.
            """
        )


    # ========================================================
    # CORRELATION
    # ========================================================

    with st.expander(
        "05 — Corrélation de Pearson"
    ):

        st.latex(
            r"""
            -1 \leq r \leq 1
            """
        )


        st.write(
            """
            **r proche de +1** : forte liaison linéaire positive.

            **r proche de -1** : forte liaison linéaire négative.

            **r proche de 0** : faible liaison linéaire.
            """
        )


        st.warning(
            "Une corrélation statistique ne prouve pas une relation de causalité."
        )


    # ========================================================
    # REGRESSION SIMPLE
    # ========================================================

    with st.expander(
        "06 — Régression linéaire simple"
    ):

        st.latex(
            r"""
            Y=aX+b
            """
        )


        st.write(
            """
            La régression simple permet d'étudier
            séparément la relation entre une variable
            explicative et la résistance.
            """
        )


    # ========================================================
    # REGRESSION MULTIPLE
    # ========================================================

    with st.expander(
        "07 — Régression linéaire multiple"
    ):

        st.latex(
            r"""
            R
            =
            \beta_0
            +
            \beta_1(E/C)
            +
            \beta_2D
            """
        )


        st.write(
            """
            Le modèle multiple combine ici :

            - le rapport eau/ciment E/C ;
            - le dosage en ciment D ;

            pour obtenir une estimation de la résistance R.
            """
        )


    # ========================================================
    # R2
    # ========================================================

    with st.expander(
        "08 — Coefficient de détermination R²"
    ):

        st.write(
            """
            R² mesure la proportion de la variabilité
            observée qui est expliquée par le modèle.

            Plus R² est proche de 1, plus le modèle
            s'ajuste aux données étudiées.

            Cela ne suffit cependant pas à prouver
            que le modèle sera performant sur de
            nouvelles données.
            """
        )


    # ========================================================
    # MAE RMSE
    # ========================================================

    with st.expander(
        "09 — MAE et RMSE"
    ):

        st.latex(
            r"""
            MAE
            =
            \frac{1}{n}
            \sum_{i=1}^{n}
            |y_i-\hat{y}_i|
            """
        )


        st.latex(
            r"""
            RMSE
            =
            \sqrt{
            \frac{1}{n}
            \sum_{i=1}^{n}
            (y_i-\hat{y}_i)^2
            }
            """
        )


        st.write(
            """
            Plus MAE et RMSE sont faibles,
            plus les prédictions du modèle
            sont proches des observations.
            """
        )


    # ========================================================
    # LIMITES
    # ========================================================

    st.warning(
        """
        BETON INSIGHT PRO est un prototype académique.

        Il ne remplace :

        - ni les essais réglementaires ;
        - ni les normes techniques ;
        - ni une étude de formulation complète ;
        - ni la validation d'un ingénieur responsable.
        """
    )