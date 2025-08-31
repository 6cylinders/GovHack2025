
from sentence_transformers import SentenceTransformer, util

# using the Q&A model for best performance
model = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1")
functions = {
    "findlowestleave": [
        "Identify employees with the lowest remaining leave balance. This is useful for spotting individuals at immediate risk of exhausting their entitlement, so HR can proactively warn them or ensure policy compliance. Helps prevent last-minute leave requests and operational disruptions.",
        "Who has the least number of leave days left?",
        "Which employees are about to run out of leave?",
        "Show me staff members with critically low leave balances",
        "Who is nearly out of annual leave entitlement?",
        "List employees at risk of exhausting their leave soon"
    ],
    "findhighestleave": [
        "Detect employees with unusually high unused leave balances. These employees may need reminders before carryover or expiry rules apply, and high balances may indicate burnout risks if they are not taking time off. Supports HR in encouraging a healthy work-life balance.",
        "Who has the most remaining leave left unused?",
        "Which staff are not taking their leave?",
        "Show me employees who might lose leave if they don’t use it",
        "Identify employees with excessive unused leave days",
        "Who has very high leave balances compared to others?",
        "List employees with very high leave balances"
    ],
    "leave_trends_by_department_role": [
        "Analyze how leave is being taken across different departments and job roles. This helps detect hotspots of high leave usage, which could signal workload imbalance, understaffing, or burnout. Managers can use this insight for resource allocation and forward planning.",
        "Which department takes the most leave days overall?",
        "Compare leave usage between different teams",
        "Show me leave distribution across job roles",
        "Which positions are responsible for the most leave taken?",
        "Are some departments showing unusually high leave rates?"
    ],
    "month_highest_leave": [
        "Identify which months record the highest total leave usage. Spotting seasonal or cyclical peaks helps HR and managers anticipate potential understaffing, plan ahead for busy holiday periods, or prepare for illness spikes such as flu season.",
        "Which month has the highest leave taken?",
        "Show me the busiest months for employee leave",
        "Are there seasonal patterns in leave usage?",
        "When do employees most frequently take time off?",
        "Highlight the months with unusually high leave days",

    ],
    "most_common_leave_type": [
        "Break down leave usage by category such as sick, annual, parental, or casual. This highlights which leave types are most common and reveals patterns in workforce wellbeing, time-off preferences, or potential policy issues.",
        "What type of leave is most common among employees?",
        "Which leave category is used the most overall?",
        "Show me the distribution of sick, annual, and parental leave",
        "Which types of leave account for the most days taken?",
        "Are employees mostly using annual leave or sick leave?"
    ],
    "sick_leave_trends": [
        "Monitor sick leave usage over time to detect unusual spikes. This may indicate seasonal illness trends, workplace wellness concerns, or broader employee health issues. HR can act to support affected teams.",
        "Are there spikes in sick leave at certain times of the year?",
        "Show me month-by-month sick leave totals",
        "Which months have unusually high sick leave taken?",
        "Are employees taking more sick leave than average?",
        "Does sick leave cluster around particular months?"
    ],
    "get_overall_leave_trends": [
        "Visualize leave trends over the year across different leave categories. This reveals how leave is distributed month by month, whether employees spread annual leave evenly, and if sick leave or other types cluster during specific periods. It provides a holistic view for HR and managers.",
        "Show overall leave trends by month across all types",
        "Plot annual leave and sick leave usage over the year",
        "How is leave spread throughout the calendar year?",
        "Give me a chart of leave days taken month by month",
        "Visualize employee leave distribution across different categories"
    ],
    "employees_near_entitlement": [
        "Identify employees who are close to using up their full leave entitlement. This is important for compliance, resource planning, and ensuring no employee exceeds policy limits. It can also help HR flag staff who may need adjustments in workload or schedule.",
        "Which employees are close to exhausting their leave entitlement?",
        "Show staff who have almost used all their leave days",
        "Who is approaching their maximum leave allocation?",
        "Alert me about employees at or near entitlement limits",
        "Which workers are running high on leave usage?"
    ],
    "employees_not_taking_leave": [
        "Detect employees who are not taking enough leave relative to their entitlement. Consistently low leave usage may signal overwork, burnout risks, or unhealthy work habits. HR can use this to encourage better rest and balance.",
        "Which employees rarely take leave?",
        "Show staff who have used very little of their leave entitlement",
        "Identify employees who might be overworking",
        "Who has taken the lowest percentage of their leave?",
        "Highlight employees at risk due to not taking leave",
        "Who doesn't take time off?"

    ],
    "department_sick_leave": [
        "Analyze sick leave across departments to identify hotspots of illness or wellbeing challenges. Departments with unusually high sick leave usage may require interventions, health programs, or workload adjustments.",
        "Which department records the most sick leave?",
        "Show me sick leave usage by department",
        "Compare departments by sick leave days taken",
        "Which teams are most affected by sick leave?",
        "Identify departments with unusually high sick leave totals"
    ]
}

func_names = list(functions.keys())

func_embeddings = {}
for fname, texts in functions.items():
    func_embeddings[fname] = model.encode(texts, convert_to_tensor=True)

def interpret_query(query):
    """
    :param query: String
    :return: best function candidate as a String, best score as a Float
    """
    query_emb = model.encode(query, convert_to_tensor=True)
    best_score = -1
    best_func = None

    # Finds maximum score and returns the function with that score.

    for fname, embeddings in func_embeddings.items():
        scores = util.cos_sim(query_emb, embeddings)
        max_score = float(scores.max())
        if max_score > best_score:
            best_score = max_score
            best_func = fname
    return best_func, best_score

if __name__ == "__main__":
    queries = [
    # findlowestleave
    "Who’s about to run out of leave days?",
    "Which employees are at risk of having no leave left?",
    "Show me people with the lowest remaining balance",
    "Who’s nearly exhausted their annual leave entitlement?",

    # findhighestleave
    "Who has the most leave left unused?",
    "Show me employees who don’t take much time off",
    "Which staff are hoarding their leave?",
    "List employees with very high leave balances",

    # leave_trends_by_department_role
    "Which department takes the most time off?",
    "Show me leave usage across different roles",
    "Do managers take more leave than regular staff?",
    "Compare leave patterns between teams",

    # month_highest_leave
    "Which month do employees take the most leave?",
    "Show me the busiest time of year for leave",
    "Is December the peak for holidays?",
    "When are people most likely to take time off?",

    # most_common_leave_type
    "What’s the most popular type of leave?",
    "Do people use more sick leave or annual leave?",
    "Which leave category is used most often?",
    "Show me the breakdown of leave by type",

    # sick_leave_trends
    "When does sick leave spike?",
    "Are there seasonal flu-related sick leave increases?",
    "Show me trends in sick leave over time",
    "Does sick leave increase during winter?",

    # get_overall_leave_trends
    "How is leave spread across the year?",
    "Show me total leave trends by month",
    "Give me a chart of leave usage across the year",
    "Do people take more leave in the middle or end of the year?",

    # employees_near_entitlement
    "Which employees are close to finishing their leave entitlement?",
    "Who has nearly used all their leave days?",
    "Show staff who are running out of their entitlement",
    "Who’s almost at their annual leave limit?",

    # employees_not_taking_leave
    "Who hasn’t been taking any leave lately?",
    "Show me employees with very little leave taken",
    "Which staff are not taking their entitled days off?",
    "Identify employees who may be overworking",

    # department_sick_leave
    "Which department is sick leave highest in?",
    "Compare sick leave across different departments",
    "Which teams are hit hardest by sickness?",
    "Show me sick leave by department totals",

    # distractors / no-match
    "What’s the weather like in Sydney?",
    "Book me a meeting with John tomorrow",
    "Show me sales trends for last quarter"
    ]

    for q in queries:
        func, score = interpret_query(q)
        print(f"Query: {q}\n -> Matched Function: {func} (score={score:.3f})\n")