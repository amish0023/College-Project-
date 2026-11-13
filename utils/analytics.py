"""Analytics and performance insight generator for weekly reports."""

def generate_weekly_insights(stats, strong_topics, weak_topics, previous_stats=None):
    """
    Produces dynamic, evidence-based academic insights from actual student records.
    """
    lectures = stats.get('lectures_completed', 0)
    assignments = stats.get('assignments_completed', 0)
    accuracy = round(float(stats.get('average_accuracy', 0) or 0.0), 1)
    study_hours = round(float(stats.get('study_hours', 0) or 0.0), 1)
    
    sentences = []
    sentences.append(f"This week you completed {lectures} lecture(s) and {assignments} adaptive assignment(s), clocking {study_hours} active study hours.")
    
    if accuracy >= 80.0:
        sentences.append(f"Outstanding precision: Your overall accuracy reached {accuracy}%.")
    elif accuracy >= 60.0:
        sentences.append(f"Solid grasp: Your average assessment accuracy is {accuracy}%.")
    elif accuracy > 0.0:
        sentences.append(f"Opportunity for improvement: Current accuracy sits at {accuracy}%. Dedicating extra time to foundational lecture notes will elevate your scores.")
        
    if strong_topics:
        sentences.append(f"Your demonstrated strongest area was {strong_topics[0]}.")
        
    if weak_topics:
        sentences.append(f"Your primary conceptual hurdle this week was {weak_topics[0]}.")
        sentences.append(f"For next week, the AI Planner has scheduled focused practice blocks for {weak_topics[0]}.")
    else:
        sentences.append("All assessed topics are currently in moderate-to-strong standing. Maintain consistency.")
        
    if previous_stats and previous_stats.get('average_accuracy'):
        prev_acc = float(previous_stats['average_accuracy'])
        diff = round(accuracy - prev_acc, 1)
        if diff > 0:
            sentences.append(f"You improved by +{diff}% compared to your previous assessment period.")
        elif diff < 0:
            sentences.append(f"Performance dipped by {abs(diff)}% from last week. Refocus on core definitions.")
            
    return " ".join(sentences)
