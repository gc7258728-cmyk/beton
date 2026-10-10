from __future__ import annotations

from io import BytesIO, StringIO
import unicodedata

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st


APP_TITLE = "BETON INSIGHT PRO"
RESISTANCE_LABEL = "Résistance (MPa)"
DEMO_STRENGTH_COLUMN = "Résistance à 28 jours (MPa)"


def make_demo_data() -> pd.DataFrame:
    """Retourne un jeu d'exemple clairement identifié comme démonstration."""
    values_by_lot = {
        "Lot A": [32.8, 34.1, 35.7, 33.9, 36.2, 34.8],
        "Lot B": [37.2, 38.1, 36.5, 39.0, 37.8, 35.9],
        "Lot C": [29.8, 31.4, 30.7, 32.2, 28.9, 31.8],
        "Lot D": [40.1, 42.3, 39.6, 41.2, 43.0, 40.8],
        "Lot E": [33.5, 34.7, 32.9, 35.1, 36.0, 34.2],
    }

    start = pd.Timestamp("2026-01-05")
    records: list[dict[str, object]] = []
    for lot_index, (lot, values) in enumerate(values_by_lot.items()):
        for test_index, value in enumerate(values):
            date = start + pd.Timedelta(days=lot_index * 8 + test_index)
            records.append(
                {
                    "Date": date.strftime("%d/%m/%Y"),
                    "Lot": lot,
                    DEMO_STRENGTH_COLUMN: value,
                }
            )
    return pd.DataFrame(records)


def normalize_heading(value: object) -> str:
    text = unicodedata.normalize("NFKD", str(value))
    text = "".join(char for char in text if not unicodedata.combining(char))
    return "".join(char for char in text.lower() if char.isalnum())


def guess_column(columns: list[str], keywords: tuple[str, ...]) -> str | None:
    normalized_keywords = tuple(normalize_heading(keyword) for keyword in keywords)
    for column in columns:
        normalized = normalize_heading(column)
        if any(keyword in normalized for keyword in normalized_keywords):
            return column
    return None


def unique_column_names(columns: object) -> list[str]:
    result: list[str] = []
    used: dict[str, int] = {}
    for index, value in enumerate(columns):
        base = str(value).strip() or f"Colonne {index + 1}"
        count = used.get(base, 0) + 1
        used[base] = count
        result.append(base if count == 1 else f"{base} ({count})")
    return result


def read_uploaded_file(uploaded_file) -> pd.DataFrame:
    """Lit un fichier CSV ou Excel envoyé dans l'application."""
    filename = uploaded_file.name.lower()
    payload = uploaded_file.getvalue()

    if filename.endswith(".xlsx"):
        return pd.read_excel(BytesIO(payload))

    if not filename.endswith(".csv"):
        raise ValueError("Format non pris en charge. Utilise un fichier CSV ou XLSX.")

    decoded = None
    for encoding in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            decoded = payload.decode(encoding)
            break
        except UnicodeDecodeError:
            continue

    if decoded is None:
        raise ValueError("Le fichier CSV n'a pas pu être décodé.")

    candidates: list[pd.DataFrame] = []
    last_error: Exception | None = None

    for separator in (None, ";", ",", "\t"):
        try:
            if separator is None:
                candidate = pd.read_csv(
                    StringIO(decoded),
                    sep=None,
                    engine="python",
                    decimal=",",
                )
            else:
                candidate = pd.read_csv(
                    StringIO(decoded),
                    sep=separator,
                    decimal=",",
                )
            candidates.append(candidate)
            if candidate.shape[1] > 1:
                return candidate
        except Exception as error:
            last_error = error

    if candidates:
        return candidates[0]
    raise ValueError(f"Lecture du CSV impossible : {last_error}")


def parse_resistance(values: pd.Series) -> pd.Series:
    """Convertit des valeurs comme 34,5 ou 34.5 MPa en nombres."""
    cleaned = (
        values.astype("string")
        .str.replace("\u00a0", "", regex=False)
        .str.replace(" ", "", regex=False)
        .str.replace(r"(?i)mpa", "", regex=True)
        .str.replace(",", ".", regex=False)
    )
    return pd.to_numeric(cleaned, errors="coerce")


def prepare_quality_and_analysis(
    raw: pd.DataFrame,
    strength_column: str,
    lot_column: str | None,
    date_column: str | None,
    include_duplicates: bool,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    raw_strength = raw[strength_column]
    resistance = parse_resistance(raw_strength)

    missing = raw_strength.isna()
    if raw_strength.dtype == object or isinstance(raw_strength.dtype, pd.StringDtype):
        missing = missing | raw_strength.astype("string").str.strip().eq("").fillna(False)

    unreadable = (~missing) & resistance.isna()
    non_positive = resistance.le(0).fillna(False)
    valid = resistance.gt(0).fillna(False)
    duplicates = raw.duplicated(keep="first")

    status = pd.Series("Valide", index=raw.index, dtype="string")
    status.loc[missing] = "Résistance manquante"
    status.loc[unreadable] = "Valeur illisible"
    status.loc[non_positive] = "Valeur nulle ou négative"
    status.loc[duplicates & status.eq("Valide")] = "Doublon exact"

    included = valid & (~duplicates | include_duplicates)

    quality = raw.copy()
    quality["Résistance interprétée (MPa)"] = resistance
    quality["Contrôle qualité"] = status
    quality["Doublon exact"] = duplicates
    quality["Incluse dans l'analyse"] = included

    analysis_columns: dict[str, pd.Series] = {
        RESISTANCE_LABEL: resistance.loc[included].astype(float).reset_index(drop=True)
    }

    if lot_column is not None:
        lots = raw[lot_column].astype("string").str.strip()
        lots = lots.replace("", pd.NA).fillna("Lot non renseigné")
        analysis_columns["Lot"] = lots.loc[included].astype(str).reset_index(drop=True)

    if date_column is not None:
        dates = pd.to_datetime(raw[date_column], errors="coerce", dayfirst=True)
        analysis_columns["Date"] = dates.loc[included].reset_index(drop=True)

    analysis = pd.DataFrame(analysis_columns)
    return quality, analysis, valid, duplicates


def format_number(value: float | int | None, decimals: int = 2) -> str:
    if value is None or pd.isna(value):
        return "—"
    return f"{value:,.{decimals}f}".replace(",", " ").replace(".", ",")


def get_statistics(values: pd.Series, threshold: float) -> dict[str, float | int | None]:
    values = pd.to_numeric(values, errors="coerce").dropna()
    if values.empty:
        return {
            "count": 0,
            "mean": None,
            "median": None,
            "std": None,
            "cv": None,
            "minimum": None,
            "maximum": None,
            "compliance": None,
            "below": 0,
        }

    mean = float(values.mean())
    std = float(values.std(ddof=1)) if len(values) > 1 else None
    cv = (std / mean * 100) if std is not None and mean != 0 else None

    return {
        "count": int(values.size),
        "mean": mean,
        "median": float(values.median()),
        "std": std,
        "cv": cv,
        "minimum": float(values.min()),
        "maximum": float(values.max()),
        "compliance": float((values >= threshold).mean() * 100),
        "below": int((values < threshold).sum()),
    }


def make_lot_summary(analysis: pd.DataFrame, threshold: float) -> pd.DataFrame:
    if "Lot" not in analysis.columns or analysis.empty:
        return pd.DataFrame()

    rows: list[dict[str, object]] = []
    for lot, group in analysis.groupby("Lot", dropna=False):
        values = group[RESISTANCE_LABEL].dropna()
        rows.append(
            {
                "Lot": str(lot),
                "Essais": int(values.size),
                "Moyenne (MPa)": float(values.mean()),
                "Médiane (MPa)": float(values.median()),
                "Minimum (MPa)": float(values.min()),
                "Maximum (MPa)": float(values.max()),
                "Conformes (%)": float((values >= threshold).mean() * 100),
            }
        )

    return (
        pd.DataFrame(rows)
        .sort_values("Moyenne (MPa)", ascending=False)
        .reset_index(drop=True)
    )


def draw_histogram(values: pd.Series, threshold: float) -> None:
    fig, ax = plt.subplots(figsize=(9, 4.4))
    bin_count = max(5, min(15, int(np.sqrt(len(values)) + 1)))
    ax.hist(values, bins=bin_count, color="#3B82F6", edgecolor="white", alpha=0.9)
    ax.axvline(
        threshold,
        color="#DC2626",
        linestyle="--",
        linewidth=2,
        label=f"Seuil : {format_number(threshold)} MPa",
    )
    ax.set_title("Distribution des résistances")
    ax.set_xlabel("Résistance (MPa)")
    ax.set_ylabel("Nombre d'essais")
    ax.grid(axis="y", alpha=0.2)
    ax.legend(frameon=False)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


def draw_lot_chart(summary: pd.DataFrame, threshold: float) -> None:
    fig, ax = plt.subplots(figsize=(10, 4.6))
    ax.bar(
        summary["Lot"].astype(str),
        summary["Moyenne (MPa)"],
        color="#2563EB",
        alpha=0.9,
    )
    ax.axhline(
        threshold,
        color="#DC2626",
        linestyle="--",
        linewidth=2,
        label=f"Seuil : {format_number(threshold)} MPa",
    )
    ax.set_title("Résistance moyenne par lot")
    ax.set_xlabel("Lot")
    ax.set_ylabel("Résistance moyenne (MPa)")
    ax.tick_params(axis="x", labelrotation=30)
    ax.grid(axis="y", alpha=0.2)
    ax.legend(frameon=False)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


def render_overview(
    analysis: pd.DataFrame,
    stats: dict[str, float | int | None],
    threshold: float,
    invalid_count: int,
    duplicate_count: int,
    include_duplicates: bool,
) -> None:
    st.subheader("Vue d'ensemble")
    st.caption(
        "Le taux conforme compare chaque résistance au seuil que tu as choisi. "
        "Ce résultat ne remplace pas les règles de contrôle de ton projet."
    )

    metric_columns = st.columns(4)
    metric_columns[0].metric("Essais analysés", f"{stats['count']}")
    metric_columns[1].metric(
        "Résistance moyenne",
        f"{format_number(stats['mean'])} MPa",
    )
    metric_columns[2].metric(
        "Au-dessus du seuil",
        f"{format_number(stats['compliance'])} %",
    )
    metric_columns[3].metric(
        "Résistances invalides",
        f"{invalid_count}",
    )

    if invalid_count or duplicate_count:
        duplicate_note = (
            " Les doublons exacts sont inclus dans l'analyse."
            if include_duplicates
            else " Les doublons exacts sont exclus de l'analyse par défaut."
        )
        st.warning(
            f"{invalid_count} ligne(s) avec une résistance manquante, illisible "
            f"ou non positive; {duplicate_count} doublon(s) exact(s)."
            f"{duplicate_note}"
        )
    else:
        st.success("Toutes les lignes contiennent une résistance exploitable.")

    left, right = st.columns([1.6, 1])
    with left:
        with st.container(border=True):
            draw_histogram(analysis[RESISTANCE_LABEL], threshold)

    with right:
        with st.container(border=True):
            st.markdown("#### Repères")
            st.write(f"**Seuil choisi :** {format_number(threshold)} MPa")
            st.write(f"**Médiane :** {format_number(stats['median'])} MPa")
            st.write(f"**Écart-type :** {format_number(stats['std'])} MPa")
            st.write(f"**Coefficient de variation :** {format_number(stats['cv'])} %")
            st.write(f"**Minimum :** {format_number(stats['minimum'])} MPa")
            st.write(f"**Maximum :** {format_number(stats['maximum'])} MPa")
            st.write(f"**Sous le seuil :** {stats['below']}")

    if "Lot" in analysis.columns:
        summary = make_lot_summary(analysis, threshold)
        if not summary.empty:
            st.markdown("#### Comparaison rapide des lots")
            st.dataframe(summary.round(2), hide_index=True)


def render_analysis(
    analysis: pd.DataFrame,
    stats: dict[str, float | int | None],
    threshold: float,
) -> None:
    st.subheader("Analyse statistique")
    st.write(
        "Les statistiques sont calculées uniquement sur les essais retenus "
        "après le contrôle qualité."
    )

    left, right = st.columns(2)
    with left:
        with st.container(border=True):
            st.markdown("#### Résumé statistique")
            summary = pd.DataFrame(
                {
                    "Indicateur": [
                        "Nombre d'essais",
                        "Moyenne (MPa)",
                        "Médiane (MPa)",
                        "Écart-type (MPa)",
                        "Coefficient de variation (%)",
                        "Minimum (MPa)",
                        "Maximum (MPa)",
                        f"Essais sous {format_number(threshold)} MPa",
                    ],
                    "Valeur": [
                        stats["count"],
                        format_number(stats["mean"]),
                        format_number(stats["median"]),
                        format_number(stats["std"]),
                        format_number(stats["cv"]),
                        format_number(stats["minimum"]),
                        format_number(stats["maximum"]),
                        stats["below"],
                    ],
                }
            )
            st.dataframe(summary, hide_index=True)

    with right:
        with st.container(border=True):
            st.markdown("#### Quartiles")
            values = analysis[RESISTANCE_LABEL]
            quartiles = pd.DataFrame(
                {
                    "Quantile": ["10 %", "25 %", "50 %", "75 %", "90 %"],
                    "Résistance (MPa)": [
                        format_number(values.quantile(0.10)),
                        format_number(values.quantile(0.25)),
                        format_number(values.quantile(0.50)),
                        format_number(values.quantile(0.75)),
                        format_number(values.quantile(0.90)),
                    ],
                }
            )
            st.dataframe(quartiles, hide_index=True)


def render_lots(analysis: pd.DataFrame, threshold: float) -> None:
    st.subheader("Comparaison des lots")
    if "Lot" not in analysis.columns:
        st.info(
            "Aucune colonne de lot n'est sélectionnée. "
            "Choisis une colonne de lot dans la barre latérale pour comparer les groupes."
        )
        return

    summary = make_lot_summary(analysis, threshold)
    if summary.empty:
        st.info("Aucun lot ne contient d'essai exploitable.")
        return

    st.caption(
        "Les lots sont classés par résistance moyenne. "
        "Le taux conforme utilise le seuil défini dans la barre latérale."
    )
    with st.container(border=True):
        draw_lot_chart(summary, threshold)
    st.dataframe(summary.round(2), hide_index=True)


def render_data_quality(
    raw: pd.DataFrame,
    quality: pd.DataFrame,
    invalid_count: int,
    duplicate_count: int,
) -> None:
    st.subheader("Données et contrôle qualité")
    summary_columns = st.columns(3)
    summary_columns[0].metric("Lignes importées", f"{len(raw)}")
    summary_columns[1].metric("Résistances à vérifier", f"{invalid_count}")
    summary_columns[2].metric("Doublons exacts", f"{duplicate_count}")

    if raw.empty:
        st.info("Le fichier ne contient aucune ligne.")
        return

    with st.container(border=True):
        st.markdown("#### Valeurs manquantes par colonne")
        missing = raw.isna().sum()
        missing_summary = pd.DataFrame(
            {
                "Colonne": missing.index.astype(str),
                "Valeurs manquantes": missing.values,
                "Part manquante (%)": [
                    round(float(value) / len(raw) * 100, 2) for value in missing.values
                ],
            }
        )
        st.dataframe(missing_summary, hide_index=True)

    with st.container(border=True):
        st.markdown("#### Lignes importées et résultat des contrôles")
        st.caption("Affichage limité aux 1 000 premières lignes.")
        st.dataframe(quality.head(1000), hide_index=True)


def build_report(
    source_name: str,
    stats: dict[str, float | int | None],
    threshold: float,
    invalid_count: int,
    duplicate_count: int,
    include_duplicates: bool,
    lot_summary: pd.DataFrame,
) -> str:
    lines = [
        APP_TITLE,
        "Rapport de synthèse des résistances du béton",
        "",
        f"Source : {source_name}",
        f"Seuil choisi : {format_number(threshold)} MPa",
        f"Essais analysés : {stats['count']}",
        f"Résistance moyenne : {format_number(stats['mean'])} MPa",
        f"Médiane : {format_number(stats['median'])} MPa",
        f"Écart-type : {format_number(stats['std'])} MPa",
        f"Coefficient de variation : {format_number(stats['cv'])} %",
        f"Minimum : {format_number(stats['minimum'])} MPa",
        f"Maximum : {format_number(stats['maximum'])} MPa",
        f"Taux au-dessus du seuil : {format_number(stats['compliance'])} %",
        f"Essais sous le seuil : {stats['below']}",
        f"Lignes avec résistance invalide : {invalid_count}",
        f"Doublons exacts détectés : {duplicate_count}",
        (
            "Les doublons exacts ont été inclus dans l'analyse."
            if include_duplicates
            else "Les doublons exacts ont été exclus de l'analyse."
        ),
        "",
        "Les résultats dépendent des données importées et du seuil choisi. "
        "Ils ne remplacent pas les règles de contrôle du projet.",
    ]

    if not lot_summary.empty:
        lines.extend(["", "Résumé par lot :"])
        for _, row in lot_summary.iterrows():
            lines.append(
                f"- {row['Lot']} : moyenne {format_number(row['Moyenne (MPa)'])} MPa, "
                f"{row['Essais']} essai(s), "
                f"{format_number(row['Conformes (%)'])} % au-dessus du seuil"
            )

    return "\n".join(lines)


def main() -> None:
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon="🏗️",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.title("🏗️ BETON INSIGHT PRO")
    st.caption("Analyse simple et lisible des essais de résistance du béton à 28 jours.")

    with st.sidebar:
        st.header("Données")
        source = st.radio(
            "Source des données",
            ["Démonstration", "Importer un fichier"],
            help="Le jeu de démonstration est fictif et sert uniquement à découvrir l'application.",
        )

        uploaded_file = None
        if source == "Importer un fichier":
            uploaded_file = st.file_uploader(
                "Choisis un fichier CSV ou Excel",
                type=["csv", "xlsx"],
                help="Pour un fichier Excel, la première feuille est utilisée.",
            )

        st.divider()
        threshold = st.number_input(
            "Seuil de conformité (MPa)",
            min_value=0.0,
            max_value=200.0,
            value=25.0,
            step=0.5,
            help="À adapter aux spécifications de ton projet.",
        )
        include_duplicates = st.checkbox(
            "Inclure les doublons exacts dans l'analyse",
            value=False,
            help="Les lignes entièrement identiques sont détectées. Par défaut, les répétitions sont exclues des statistiques.",
        )

    if source == "Démonstration":
        raw = make_demo_data()
        source_name = "Données de démonstration (fictives)"
    else:
        if uploaded_file is None:
            st.info("Importe un fichier CSV ou XLSX pour commencer.")
            st.download_button(
                "Télécharger un exemple CSV",
                data=make_demo_data().to_csv(index=False).encode("utf-8-sig"),
                file_name="exemple_essais_beton.csv",
                mime="text/csv",
            )
            st.stop()

        try:
            raw = read_uploaded_file(uploaded_file)
        except Exception as error:
            st.error(f"Impossible de lire le fichier : {error}")
            st.stop()

        if raw.empty or len(raw.columns) == 0:
            st.error("Le fichier ne contient pas de tableau exploitable.")
            st.stop()

        source_name = uploaded_file.name

    raw = raw.copy()
    raw.columns = unique_column_names(raw.columns)
    columns = list(raw.columns)

    if not columns:
        st.error("Aucune colonne n'a été trouvée dans les données.")
        st.stop()

    with st.sidebar:
        st.divider()
        st.header("Associer les colonnes")

        suggested_strength = guess_column(
            columns,
            ("resistance", "compressive", "strength", "mpa", "fc28", "r28", "28j"),
        )
        default_strength_index = (
            columns.index(suggested_strength) if suggested_strength in columns else 0
        )
        strength_column = st.selectbox(
            "Colonne de résistance",
            options=columns,
            index=default_strength_index,
            help="Choisis la colonne qui contient les valeurs en MPa.",
        )

        optional_columns = ["— Aucune —", *columns]
        suggested_lot = guess_column(
            columns,
            ("lot", "batch", "groupe", "serie", "sample", "echantillon", "chantier"),
        )
        lot_index = (
            optional_columns.index(suggested_lot)
            if suggested_lot in optional_columns
            else 0
        )
        lot_choice = st.selectbox(
            "Colonne de lot (facultative)",
            options=optional_columns,
            index=lot_index,
        )

        suggested_date = guess_column(columns, ("date", "datetime", "timestamp"))
        date_index = (
            optional_columns.index(suggested_date)
            if suggested_date in optional_columns
            else 0
        )
        date_choice = st.selectbox(
            "Colonne de date (facultative)",
            options=optional_columns,
            index=date_index,
        )

        navigation = st.radio(
            "Navigation",
            [
                "Vue d'ensemble",
                "Analyse statistique",
                "Lots",
                "Données et qualité",
                "Rapport et exports",
            ],
        )

    lot_column = None if lot_choice == "— Aucune —" else lot_choice
    date_column = None if date_choice == "— Aucune —" else date_choice

    quality, analysis, valid_mask, duplicate_mask = prepare_quality_and_analysis(
        raw=raw,
        strength_column=strength_column,
        lot_column=lot_column,
        date_column=date_column,
        include_duplicates=include_duplicates,
    )

    if analysis.empty:
        st.error(
            "Aucun essai exploitable. Vérifie la colonne de résistance et les valeurs "
            "dans l'onglet Données et qualité."
        )
        st.dataframe(quality.head(1000), hide_index=True)
        st.stop()

    threshold = float(threshold)
    stats = get_statistics(analysis[RESISTANCE_LABEL], threshold)
    invalid_count = int((~valid_mask).sum())
    duplicate_count = int(duplicate_mask.sum())
    lot_summary = make_lot_summary(analysis, threshold)

    st.caption(f"Source : {source_name}")

    if navigation == "Vue d'ensemble":
        render_overview(
            analysis=analysis,
            stats=stats,
            threshold=threshold,
            invalid_count=invalid_count,
            duplicate_count=duplicate_count,
            include_duplicates=include_duplicates,
        )
    elif navigation == "Analyse statistique":
        render_analysis(analysis, stats, threshold)
    elif navigation == "Lots":
        render_lots(analysis, threshold)
    elif navigation == "Données et qualité":
        render_data_quality(raw, quality, invalid_count, duplicate_count)
    else:
        st.subheader("Rapport et exports")
        st.write(
            "Télécharge le résumé de l'analyse, les essais retenus ou le tableau "
            "complet avec les résultats des contrôles."
        )

        report = build_report(
            source_name=source_name,
            stats=stats,
            threshold=threshold,
            invalid_count=invalid_count,
            duplicate_count=duplicate_count,
            include_duplicates=include_duplicates,
            lot_summary=lot_summary,
        )

        left, right = st.columns(2)
        with left:
            st.download_button(
                "Télécharger le rapport texte",
                data=report.encode("utf-8"),
                file_name="rapport_beton_insight.txt",
                mime="text/plain",
            )
            st.download_button(
                "Télécharger les essais analysés (CSV)",
                data=analysis.to_csv(index=False).encode("utf-8-sig"),
                file_name="essais_analyses.csv",
                mime="text/csv",
            )
        with right:
            st.download_button(
                "Télécharger les contrôles qualité (CSV)",
                data=quality.to_csv(index=False).encode("utf-8-sig"),
                file_name="controle_qualite.csv",
                mime="text/csv",
            )

        with st.expander("Aperçu du rapport"):
            st.text(report)


if __name__ == "__main__":
    main()
