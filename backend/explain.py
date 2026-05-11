import shap
import joblib

model = joblib.load("model.pkl")
explainer = shap.TreeExplainer(model)

def explain(features):
    shap_values = explainer.shap_values([features])

    return list(shap_values[1][0])