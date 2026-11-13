"""Adaptive Study Plan Generator for Dynamic Weekly Scheduling."""
from datetime import date, timedelta


def make_weekly_plan(recommendations, preferred_days_str, session_duration_minutes, available_hours_per_week):
    """
    Constructs an adaptive weekly study plan distributing recommendations across the student's
    preferred days and allocated study hours budget, with subject interleaving.
    """
    if not preferred_days_str:
        preferred_days = ['monday', 'wednesday', 'friday', 'saturday']
    else:
        preferred_days = [d.strip().lower() for d in preferred_days_str.split(',') if d.strip()]
        if not preferred_days:
            preferred_days = ['monday', 'wednesday', 'friday']
            
    session_minutes = max(20, min(120, int(session_duration_minutes or 45)))
    weekly_budget_minutes = max(60, int((available_hours_per_week or 10) * 60))
    
    # Map the next 14 days that match preferred days
    today = date.today()
    available_dates = []
    for offset in range(14):
        target_day = today + timedelta(days=offset)
        day_name = target_day.strftime('%A').lower()
        if day_name in preferred_days:
            available_dates.append(target_day)
            
    if not available_dates:
        available_dates = [today + timedelta(days=i) for i in range(7)]
        
    scheduled_tasks = []
    remaining_budget = weekly_budget_minutes
    
    if not recommendations:
        return scheduled_tasks
        
    # Interleave recommendations across distinct subjects to maintain balanced progress
    subject_groups = {}
    for r in recommendations:
        sid = r.get('subject_id')
        if sid not in subject_groups:
            subject_groups[sid] = []
        subject_groups[sid].append(r)
        
    interleaved_recs = []
    max_len = max((len(g) for g in subject_groups.values()), default=0)
    for i in range(max_len):
        for sid, group in subject_groups.items():
            if i < len(group):
                interleaved_recs.append(group[i])
                
    if not interleaved_recs:
        interleaved_recs = recommendations
        
    rec_index = 0
    date_index = 0
    
    # Allow multiple sessions per day if weekly budget exceeds available calendar slots
    max_sessions = max(1, weekly_budget_minutes // session_minutes)
    slots_per_day = max(1, (max_sessions + len(available_dates) - 1) // len(available_dates))
    day_session_counts = {d: 0 for d in available_dates}
    
    while remaining_budget >= session_minutes and rec_index < len(interleaved_recs) and rec_index < max_sessions:
        rec = interleaved_recs[rec_index]
        
        # Pick the next date that still has slot capacity
        task_date = available_dates[date_index % len(available_dates)]
        task_duration = min(session_minutes, remaining_budget)
        
        # Vary title and description depending on mastery
        if rec.get('mastery') == 'WEAK':
            title = f"{rec['subject']} — {rec['topic']} (Concept Mastery)"
            desc = f"{rec['activity']} [{rec['priority']} Priority]"
        elif rec.get('mastery') == 'MODERATE':
            title = f"{rec['subject']} — {rec['topic']} (Adaptive Practice)"
            desc = f"{rec['activity']} [{rec['priority']} Priority]"
        else:
            title = f"{rec['subject']} — {rec['topic']} (Spaced Revision)"
            desc = f"{rec['activity']} [{rec['priority']} Priority]"
            
        scheduled_tasks.append({
            'subject_id': rec.get('subject_id'),
            'topic_id': rec.get('topic_id'),
            'subject': rec.get('subject'),
            'topic': rec.get('topic'),
            'title': title,
            'description': desc,
            'priority': rec.get('priority', 'MEDIUM'),
            'duration': task_duration,
            'due_date': task_date,
            'source': 'AI'
        })
        
        remaining_budget -= task_duration
        rec_index += 1
        day_session_counts[task_date] = day_session_counts.get(task_date, 0) + 1
        if day_session_counts[task_date] >= slots_per_day:
            date_index += 1
            
    return scheduled_tasks
