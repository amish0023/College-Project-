"""AI Recommendation Engine for Individualized Student Focus."""
from utils.mastery import calculate_priority, explain_priority


def build_recommendations(topic_rows, hours_per_week=10, days_remaining=None):
    """
    Generates personalized learning recommendations computed directly from each student's
    actual stored performance metrics, topic mastery, and subject priorities.
    """
    recommendations = []
    
    # Priority multipliers
    subject_weights = {'HIGH': 1.25, 'MEDIUM': 1.0, 'LOW': 0.75}
    urgency_multiplier = 1.2 if (days_remaining is not None and days_remaining < 30) else 1.0
    
    for row in topic_rows:
        score, level = calculate_priority(row)
        subj_weight = subject_weights.get(row.get('subject_priority', 'MEDIUM'), 1.0)
        
        # Adjusted priority score
        weighted_score = round(min(100.0, score * subj_weight * urgency_multiplier), 1)
        
        # Adaptive duration based on weakness and available hours
        base_duration = 30 + int(weighted_score * 0.4)
        # Round to 15-minute intervals
        duration = max(20, min(90, (base_duration // 15) * 15))
        
        explanation = explain_priority(row)
        
        if level == 'HIGH' or weighted_score >= 60.0:
            activity = f"Intensive concept review: Rewatch difficult sections & solve foundational practice questions"
            rec_level = 'HIGH'
        elif level == 'MEDIUM' or weighted_score >= 35.0:
            activity = f"Targeted practice: Review AI lecture notes and solve 5-10 medium-difficulty questions"
            rec_level = 'MEDIUM'
        else:
            activity = f"Retrieval mastery: Rapid flash-quiz and concept summarization"
            rec_level = 'LOW'
            
        recommendations.append({
            'subject': row.get('subject_name', ''),
            'subject_id': row.get('subject_id'),
            'topic': row.get('topic_name', ''),
            'topic_id': row.get('topic_id'),
            'module_id': row.get('module_id'),
            'mastery': row.get('mastery', 'MODERATE'),
            'priority': rec_level,
            'priority_score': weighted_score,
            'reason': explanation['summary_reason'],
            'explanation_details': explanation['reasons'],
            'action': explanation['recommended_action'],
            'activity': activity,
            'duration': duration
        })
        
    # Sort by descending priority score
    recommendations.sort(key=lambda x: x['priority_score'], reverse=True)
    return recommendations
