"""ML-backed topic mastery prediction and Explainable AI priority assessment."""
from config import Config
from ml.predict import predict, predict_mastery_from_metrics, FEATURES


def predict_mastery(metrics):
    """Predicts 'WEAK', 'MODERATE', or 'STRONG' using the real trained scikit-learn model."""
    return predict(metrics)


def calculate_priority(metrics, weights=None):
    """
    Computes a composite priority score (0-100) and categorical level ('HIGH','MEDIUM','LOW')
    evaluating multiple weakness vectors:
    - Score & accuracy deficit
    - Repeated errors / attempts
    - Time spent vs problem difficulty
    - Prior deficit and stagnant improvement
    - Incomplete lecture study
    """
    w = weights or Config.PRIORITY_WEIGHTS
    
    score = float(metrics.get('assignment_score', metrics.get('quiz_score', 0)) or 0.0)
    accuracy = float(metrics.get('accuracy', 0) or 0.0)
    previous = float(metrics.get('previous_score', 0) or 0.0)
    improvement = float(metrics.get('improvement', 0) or 0.0)
    completion = float(metrics.get('lecture_completion', 0) or 0.0)
    attempts = int(metrics.get('attempts', 1) or 1)
    time_spent = float(metrics.get('time_spent', 0) or 0.0)
    difficulty = float(metrics.get('difficulty', 1) or 1.0)
    
    # Normalized error/deficit factors [0.0 to 1.0]
    weakness_factor = max(0.0, 1.0 - (score / 100.0))
    inaccuracy_factor = max(0.0, 1.0 - (accuracy / 100.0))
    repeated_mistakes = min(1.0, max(0.0, (attempts - 1) / 3.0))
    time_difficulty = min(1.0, (time_spent / 45.0) * (difficulty / 3.0))
    prior_deficit = max(0.0, 1.0 - (previous / 100.0))
    stagnant_improvement = max(0.0, 1.0 - max(0.0, improvement) / 50.0)
    completion_deficit = max(0.0, 1.0 - (completion / 100.0))
    
    components = {
        'weakness': weakness_factor,
        'inaccuracy': inaccuracy_factor,
        'repeated_mistakes': repeated_mistakes,
        'time_difficulty': time_difficulty,
        'previous_performance': prior_deficit,
        'improvement': stagnant_improvement,
        'completion': completion_deficit
    }
    
    total_weight = sum(w.values())
    raw_score = sum(w[k] * components.get(k, 0.0) for k in w) / total_weight
    priority_score = round(raw_score * 100.0, 1)
    
    if priority_score >= 60.0:
        priority_level = 'HIGH'
    elif priority_score >= 35.0:
        priority_level = 'MEDIUM'
    else:
        priority_level = 'LOW'
        
    return priority_score, priority_level


def explain_priority(metrics):
    """
    Generates genuine Explainable AI explanations using the student's actual recorded metrics.
    Returns:
      reasons: List of factual data findings
      recommended_action: Actionable study prescription
    """
    reasons = []
    actions = []
    
    score = float(metrics.get('assignment_score', metrics.get('quiz_score', 0)) or 0.0)
    accuracy = float(metrics.get('accuracy', 0) or 0.0)
    previous = float(metrics.get('previous_score', 0) or 0.0)
    attempts = int(metrics.get('attempts', 1) or 1)
    time_spent = float(metrics.get('time_spent', 0) or 0.0)
    completion = float(metrics.get('lecture_completion', 0) or 0.0)
    improvement = float(metrics.get('improvement', 0) or 0.0)
    
    if accuracy < 60.0:
        reasons.append(f"Accuracy is low at {round(accuracy)}% across test attempts.")
        actions.append("Review key concept notes and definitions.")
        
    if previous > 0 and score < previous:
        reasons.append(f"Performance dipped from previous score of {round(previous)}% down to {round(score)}%.")
        actions.append("Identify concept confusion in previous missed questions.")
    elif improvement < 5.0 and attempts > 1:
        reasons.append(f"Stagnant improvement (+{round(improvement, 1)}%) despite repeated practice.")
        actions.append("Rewatch tricky lecture sections to clear misconceptions.")
        
    if attempts > 2:
        reasons.append(f"Repeated mistakes detected across {attempts} assignment attempts.")
        actions.append("Practice foundational questions before retrying harder items.")
        
    if time_spent > 25.0:
        reasons.append(f"High solving time ({round(time_spent)} mins) indicates conceptual friction.")
        actions.append("Time-box retrieval practice drills to build fluency.")
        
    if completion < 90.0:
        reasons.append(f"Lecture completion is only {round(completion)}%.")
        actions.append("Finish watching the complete lecture video.")
        
    if not reasons:
        reasons.append(f"Consistent accuracy ({round(accuracy)}%) and stable grasp of concepts.")
        recommended_action = "Maintain mastery with periodic spaced retrieval practice."
    else:
        recommended_action = " ".join(actions)
        
    return {
        'reasons': reasons,
        'summary_reason': " ".join(reasons),
        'recommended_action': recommended_action
    }
