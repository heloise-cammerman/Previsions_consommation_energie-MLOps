import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

def evaluer_modele(y_vrai, y_predit):
    return {
        "MAE": mean_absolute_error(y_vrai, y_predit),
        "RMSE": np.sqrt(mean_squared_error(y_vrai, y_predit)),
        "R2": r2_score(y_vrai, y_predit)}

def entrainer_et_evaluer_modeles(df):
    df_modele = df.select_dtypes(include = ["number", "bool"]).copy()
    df_modele = df_modele.drop(columns = [
        "Consommation brute gaz totale (MW PCS 0°C)",
        "Consommation brute électricité (MW) - RTE",
        "Consommation brute gaz (MW PCS 0°C) - NaTran",
        "Consommation brute gaz (MW PCS 0°C) - Teréga"])
    X = df_modele.drop(columns = ["Consommation brute totale (MW)"])
    y = df_modele["Consommation brute totale (MW)"]
    indice_coupure = int(len(df_modele) * 0.8)
    X_train, X_test = X.iloc[:indice_coupure], X.iloc[indice_coupure:]
    y_train, y_test = y.iloc[:indice_coupure], y.iloc[indice_coupure:]
    resultats = []
    # Baseline naïve (t-1)
    y_pred_naif = y_test.shift(1).dropna()
    y_test_naif = y_test.loc[y_pred_naif.index]
    res = evaluer_modele(y_test_naif, y_pred_naif)
    res["Modele"] = "Baseline naïve (t-1)"
    resultats.append(res)
    # Régression linéaire
    reg_lin = LinearRegression().fit(X_train, y_train)
    resultats.append({
        **evaluer_modele(y_test, reg_lin.predict(X_test)),
        "Modele": "Régression linéaire"})
    # Random Forest
    foret = RandomForestRegressor(
        n_estimators = 100,
        max_depth = 15,
        random_state = 42,
        n_jobs = -1)
    foret.fit(X_train, y_train)
    resultats.append({
        **evaluer_modele(y_test, foret.predict(X_test)),
        "Modele": "Random Forest"})
    # Gradient Boosting
    boosting = GradientBoostingRegressor(
        n_estimators = 300,
        learning_rate = 0.05,
        max_depth = 5,
        random_state = 42)
    boosting.fit(X_train, y_train)
    resultats.append({
        **evaluer_modele(y_test, boosting.predict(X_test)),
        "Modele": "Gradient Boosting"})
    return pd.DataFrame(resultats).sort_values("R2", ascending = False)
