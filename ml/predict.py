"""ML Prediction interface for real runtime mastery inference."""
from pathlib import Path
import joblib
import pandas as pd

FEATURES = [
    'quiz_score', 'accuracy', 'attempts', 'time_spent', 'previous_score',
    'assignment_score', 'study_hours', 'difficulty', 'lecture_completion', 'improvement'
]

LABELS = {0: 'WEAK', 1: 'MODERATE', 2: 'STRONG'}
_CACHED_MODEL = None

def get_model():
    global _CACHED_MODEL
    if _CACHED_MODEL is None:
        model_path = Path(__file__).parent / 'model.pkl'
        if not model_path.exists():
            raise FileNotFoundError(f"Model file not found at {model_path}. Run ml/train_model.py first.")
        _CACHED_MODEL = joblib.load(model_path)
    return _CACHED_MODEL

def predict_mastery_from_metrics(metrics):
    """
    Given a metrics dict containing the 10 features, returns:
    mastery_label: 'WEAK' | 'MODERATE' | 'STRONG'
    mastery_code: 0 | 1 | 2
    """
    model = get_model()
    # Construct a DataFrame with exact column names to match model pipeline training features
    row = {f: [float(metrics.get(f, 0.0) or 0.0)] for f in FEATURES}
    df = pd.DataFrame(row)
    pred_code = int(model.predict(df)[0])
    pred_label = LABELS.get(pred_code, 'MODERATE')
    return pred_label, pred_code

def predict(metrics):
    label, _ = predict_mastery_from_metrics(metrics)
    return label
