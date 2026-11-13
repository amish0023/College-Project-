"""Train and evaluate 3 Machine Learning models for Student Topic Mastery."""
import json
from pathlib import Path
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix

FEATURES = [
    'quiz_score', 'accuracy', 'attempts', 'time_spent', 'previous_score',
    'assignment_score', 'study_hours', 'difficulty', 'lecture_completion', 'improvement'
]

def train():
    dataset_path = Path(__file__).parent / 'dataset.csv'
    if not dataset_path.exists():
        import generate_dataset
        generate_dataset.generate()
        
    df = pd.read_csv(dataset_path)
    X = df[FEATURES]
    y = df['mastery']
    
    # 80/20 Stratified train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    
    models = {
        'Decision Tree': DecisionTreeClassifier(max_depth=7, random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42),
        'Logistic Regression': Pipeline([
            ('scale', StandardScaler()),
            ('clf', LogisticRegression(max_iter=2000, random_state=42))
        ])
    }
    
    results = {}
    best_name = None
    best_pipeline = None
    best_f1 = -1.0
    
    for name, model in models.items():
        pipeline = Pipeline([
            ('imputer', SimpleImputer(strategy='median')),
            ('model', model)
        ])
        
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)
        
        acc = accuracy_score(y_test, y_pred)
        prec, rec, f1, _ = precision_recall_fscore_support(
            y_test, y_pred, average='weighted', zero_division=0
        )
        cm = confusion_matrix(y_test, y_pred).tolist()
        
        results[name] = {
            'accuracy': round(float(acc), 4),
            'precision': round(float(prec), 4),
            'recall': round(float(rec), 4),
            'f1': round(float(f1), 4),
            'confusion_matrix': cm
        }
        
        print(f"[{name}] Accuracy: {acc:.4f}, Precision: {prec:.4f}, Recall: {rec:.4f}, F1: {f1:.4f}")
        
        if f1 > best_f1:
            best_f1 = f1
            best_name = name
            best_pipeline = pipeline
            
    # Save best model
    model_path = Path(__file__).parent / 'model.pkl'
    joblib.dump(best_pipeline, model_path)
    
    eval_path = Path(__file__).parent / 'evaluation.json'
    eval_data = {
        'best_model': best_name,
        'best_f1': round(float(best_f1), 4),
        'total_records': len(df),
        'train_samples': len(X_train),
        'test_samples': len(X_test),
        'features': FEATURES,
        'target_classes': {'0': 'WEAK', '1': 'MODERATE', '2': 'STRONG'},
        'models': results
    }
    
    with open(eval_path, 'w', encoding='utf-8') as f:
        json.dump(eval_data, f, indent=2)
        
    print(f"\nSuccessfully trained! Best model: {best_name} (F1: {best_f1:.4f})")
    print(f"Model saved to: {model_path}")
    print(f"Evaluation metrics saved to: {eval_path}")

if __name__ == '__main__':
    train()
