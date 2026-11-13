"""Generate a realistic, comprehensive 1,500+ record student learning dataset."""
import csv
import random
from pathlib import Path

random.seed(42)

SUBJECTS = {
    'Data Structures': ['Arrays', 'Linked Lists', 'Stack', 'Queue', 'Trees', 'Graphs', 'Sorting', 'Searching'],
    'Database Management Systems': ['ER Model', 'Normalization', 'SQL Queries', 'Transactions', 'Indexing'],
    'Machine Learning': ['Supervised Learning', 'Decision Trees', 'Neural Networks', 'Model Evaluation'],
    'Operating Systems': ['Process Management', 'CPU Scheduling', 'Deadlocks', 'Virtual Memory'],
    'Computer Networks': ['OSI Model', 'TCP/IP', 'Routing Protocols', 'Transport Layer', 'Network Security'],
    'Artificial Intelligence': ['Search Algorithms', 'Heuristics', 'Knowledge Representation', 'Game Playing']
}

OUTPUT_PATH = Path(__file__).parent / 'dataset.csv'

def generate():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    
    for i in range(1600):
        # Latent student aptitude: 0 (struggling) to 1 (high-performing)
        aptitude = random.betavariate(2.2, 2.0)
        
        subject = random.choice(list(SUBJECTS.keys()))
        topic = random.choice(SUBJECTS[subject])
        difficulty = random.randint(1, 3) # 1=Easy, 2=Medium, 3=Hard
        
        lecture_completion = max(15.0, min(100.0, aptitude * 70.0 + random.gauss(25.0, 15.0)))
        previous_score = max(0.0, min(100.0, aptitude * 80.0 + random.gauss(10.0, 14.0)))
        
        # Current quiz & assignment performance is influenced by aptitude, completion, and difficulty
        base_performance = aptitude * 72.0 + (lecture_completion * 0.16) - (difficulty * 4.0) + random.gauss(8.0, 12.0)
        quiz_score = max(0.0, min(100.0, base_performance))
        accuracy = max(0.0, min(100.0, quiz_score + random.gauss(0.0, 8.0)))
        assignment_score = max(0.0, min(100.0, quiz_score + random.gauss(2.0, 6.0)))
        
        attempts = random.randint(1, 4) if aptitude < 0.6 else random.randint(1, 2)
        time_spent = max(5.0, random.gauss(14.0 + difficulty * 8.0 + (1.0 - aptitude) * 18.0, 7.0))
        study_hours = max(0.5, random.gauss(2.0 + aptitude * 4.5, 1.2))
        improvement = round(assignment_score - previous_score, 2)
        
        # Ground truth topic mastery index:
        # 0 = WEAK, 1 = MODERATE, 2 = STRONG
        mastery_metric = (
            0.35 * assignment_score +
            0.25 * accuracy +
            0.15 * previous_score +
            0.10 * lecture_completion +
            0.10 * max(0.0, improvement) -
            0.05 * min(time_spent, 60.0)
        )
        
        if mastery_metric < 50.0:
            mastery = 0  # WEAK
        elif mastery_metric < 75.0:
            mastery = 1  # MODERATE
        else:
            mastery = 2  # STRONG
            
        rows.append({
            'student_id': random.randint(1001, 1400),
            'subject': subject,
            'topic': topic,
            'quiz_score': round(quiz_score, 2),
            'accuracy': round(accuracy, 2),
            'attempts': attempts,
            'time_spent': round(time_spent, 2),
            'previous_score': round(previous_score, 2),
            'assignment_score': round(assignment_score, 2),
            'study_hours': round(study_hours, 2),
            'difficulty': difficulty,
            'lecture_completion': round(lecture_completion, 2),
            'improvement': round(improvement, 2),
            'mastery': mastery
        })
        
    with open(OUTPUT_PATH, 'w', newline='', encoding='utf-8') as f:
        fieldnames = [
            'student_id', 'subject', 'topic', 'quiz_score', 'accuracy', 'attempts',
            'time_spent', 'previous_score', 'assignment_score', 'study_hours',
            'difficulty', 'lecture_completion', 'improvement', 'mastery'
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
        
    print(f"Dataset created with {len(rows)} records at {OUTPUT_PATH}")

if __name__ == '__main__':
    generate()
