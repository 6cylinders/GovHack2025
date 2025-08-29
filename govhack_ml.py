
from sentence_transformers import SentenceTransformer, util

# using the Q&A model for best performance
model = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1")
functions = {
    "leave_balance_monitoring": [
        # Description
        "Monitor and track the leave balances of all employees. "
        "Identify employees who have the lowest remaining leave days or may soon run out of entitlement. "
        "Detect employees with unusually high unused leave and send reminders before expiry. "
        "Helps HR ensure compliance, fairness, and prevent last-minute leave requests.",
        # Synthetic queries / paraphrases
        "Show me who has the least leave left",
        "Which employees are running out of leave soon?",
        "Alert HR about employees with low remaining leave",
        "Who has the lowest number of leave days left?"
    ],
    "leave_trends_department_role": [
        "Analyze leave usage trends across departments and job roles. "
        "Check which department or team is taking the most leave. "
        "Detect hotspots of high leave usage that might indicate burnout or understaffing. "
        "Helps managers allocate resources and plan schedules effectively.",
        "Which department takes the most leave?",
        "Show leave trends by team or role",
        "Compare leave usage across departments",
        "Identify teams with high leave usage",
        "How is leave is being spread across departments"
    ],
    "leave_type_analysis": [
        "Examine leave requests by type, such as sick leave, annual leave, parental leave, or casual leave. "
        "Identify the most common leave categories and detect unusual spikes. "
        "Assess whether annual leave is being evenly spread or clustered across the year. "
        "Helps HR review policy effectiveness and employee wellness.",
        "What types of leave are most common?",
        "Are employees spreading annual leave evenly?",
        "Detect spikes in sick leave across teams",
        "Analyze leave usage by category"
    ],
    "absence_impact_operations": [
        "Evaluate how employee absences affect operations and team productivity. "
        "Identify when multiple employees in the same department are on leave simultaneously. "
        "Analyze seasonal trends in leave, such as holiday periods or flu season. "
        "Helps managers plan schedules, anticipate shortages, and reduce disruption.",
        "Do multiple team members have overlapping leave?",
        "Show seasonal leave overlaps",
        "How do absences affect department operations?",
        "Which teams are understaffed due to leave?",
        "Are multiple team members on leave within"
    ],
    "policy_compliance_exceptions": [
        "Monitor employee leave to ensure compliance with policies and entitlements. "
        "Identify employees who have exceeded or are close to exceeding their leave allowance. "
        "Detect employees taking too little leave, signaling overwork or burnout risk. "
        "Highlight unusual departmental leave patterns to enforce fair and healthy work habits.",
        "Who has exceeded their leave entitlement?",
        "Identify policy violations in leave usage",
        "Which employees take too little leave?",
        "Which departments have unusual leave patterns?"
    ]
}

func_names = list(functions.keys())

func_embeddings = {}
for fname, texts in functions.items():
    func_embeddings[fname] = model.encode(texts, convert_to_tensor=True)

def interpret_query(query):
    query_emb = model.encode(query, convert_to_tensor=True)
    best_score = -1
    best_func = None

    for fname, embeddings in func_embeddings.items():
        scores = util.cos_sim(query_emb, embeddings)
        max_score = float(scores.max())
        if max_score > best_score:
            best_score = max_score
            best_func = fname
    return best_func, best_score

if __name__ == "__main__":
    queries = [
        "Show me who has the least leave days left",
        "Which department takes the most sick leave?",
        "Is annual leave being spread across the year?",
        "Do any teams have multiple people off at the same time?",
        "Who has already used more leave than their entitlement?",
        "Who has the largest amount of unused leave?"
    ]

    for q in queries:
        func, score = interpret_query(q)
        print(f"Query: {q}\n -> Matched Function: {func} (score={score:.3f})\n")