import jours_feries_france as jff
from vacances_scolaires_france import SchoolHolidayDates

def ajouter_variables_calendaires(df):
    df = df.copy()
    df["jour"] = df["Date"].dt.day
    df["mois"] = df["Date"].dt.month
    df["annee"] = df["Date"].dt.year
    df["jour_semaine_num"] = df["Date"].dt.weekday
    df["week_end"] = df["jour_semaine_num"] > =  5
    return df

def ajouter_vacances_scolaires(df):
    calendrier = SchoolHolidayDates()
    for zone in ["A", "B", "C"]:
        df[f"vacances_zone_{zone}"] = df["Date"].apply(
            lambda d: calendrier.is_holiday_for_zone(d.date(), zone))
    return df

def ajouter_jours_feries(df):
    jours_feries = set()
    for annee in range(2012, 2026):
        dictionnaire = jff.JoursFeries.for_year(annee)
        for valeur in dictionnaire.values():
            if hasattr(valeur, "year"):
                jours_feries.add(valeur)
    df["jour_ferie"] = df["Date"].dt.date.isin(jours_feries)
    return df

def supprimer_colonnes_inutiles(df):
    return df.drop(columns = [
        "horodatage",
        "Date - Heure",
        "Statut - Teréga",
        "flag_ignore"])
