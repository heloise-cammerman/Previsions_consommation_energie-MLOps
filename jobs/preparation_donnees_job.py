import pandas as pd
import requests

def charger_et_preparer_donnees(chemin_csv):
    df = pd.read_csv(chemin_csv, delimiter = ";")
    # Suppression des valeurs manquantes
    df = df.dropna()
    # Conversion des dates
    df["Date"] = pd.to_datetime(df["Date"], format = "%d/%m/%Y", errors = "coerce")
    df["Date - Heure"] = pd.to_datetime(df["Date - Heure"]).dt.tz_convert(None)
    return df


def charger_donnees_meteo():
    url = "https://archive-api.open-meteo.com/v1/archive"
    parametres = {
        "latitude": 48.8566,
        "longitude": 2.3522,
        "start_date": "2012-01-01",
        "end_date": "2025-10-31",
        "hourly": [
            "temperature_2m",
            "apparent_temperature",
            "relative_humidity_2m",
            "wind_speed_10m",
            "cloud_cover",
            "surface_pressure"],
        "timezone": "Europe/Paris"}
    reponse = requests.get(url, params = parametres)
    donnees = reponse.json()
    meteo = pd.DataFrame({
        "horodatage": pd.to_datetime(donnees["hourly"]["time"]),
        "temperature": donnees["hourly"]["temperature_2m"],
        "temperature_ressentie": donnees["hourly"]["apparent_temperature"],
        "humidite": donnees["hourly"]["relative_humidity_2m"],
        "vitesse_vent": donnees["hourly"]["wind_speed_10m"],
        "couverture_nuageuse": donnees["hourly"]["cloud_cover"],
        "pression": donnees["hourly"]["surface_pressure"]})
    return meteo

def fusionner_meteo(df, meteo):
    df = pd.merge(
        meteo,
        df,
        how = "right",
        left_on = "horodatage",
        right_on = "Date - Heure")
    df = df.dropna()
    return df
