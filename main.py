from jobs.preparation_donnees_job import (
    charger_et_preparer_donnees,
    charger_donnees_meteo,
    fusionner_meteo)

from jobs.feature_engineering_job import (
    ajouter_variables_calendaires,
    ajouter_vacances_scolaires,
    ajouter_jours_feries,
    supprimer_colonnes_inutiles
    )
from jobs.modelisation_job import entrainer_et_evaluer_modeles

df = charger_et_preparer_donnees("donnees/consommation-quotidienne-brute.csv")

meteo = charger_donnees_meteo()
df = fusionner_meteo(df, meteo)

df = ajouter_variables_calendaires(df)
df = ajouter_vacances_scolaires(df)
df = ajouter_jours_feries(df)
df = supprimer_colonnes_inutiles(df)

resultats = entrainer_et_evaluer_modeles(df)
print(resultats)
