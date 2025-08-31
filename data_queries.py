import pandas as pd
import matplotlib.pyplot as plt
import base64
import os
import io

df = pd.read_csv('leave_data\employee leave tracking data.csv')

def findlowestleave():
    # Who has the lowest remaining leave balance (at risk of running out)?
    min_leave = df["Remaining Leaves"].min()
    names = df.loc[df['Remaining Leaves'] == min_leave, "Employee Name"]
    result = names.tolist()

    # Format output like a mini table
    output = "--- Employee(s) with Lowest Remaining Leave ---<br>"
    output += "Employee Name | Remaining Leave<br>"
    output += "--- | ---<br>"

    for name in result:
        output += f"{name} | {min_leave}<br>"
    output = output.replace('\n', '<br>')
    return output

def findhighestleave():
    #trying to answer: Who has unusually high unused leave (might need reminders before carryover/expiry)?
    max_leave = df["Remaining Leaves"].max()
    names = df.loc[df["Remaining Leaves"] == max_leave, "Employee Name"]
    result = names.tolist()
    #still need to figure out the thought process being displayed
    output = (
        "--- Employee(s) with Highest Remaining Leave ---<br>"
        f"Remaining leave days: {max_leave}<br>"
        f"Employees: {', '.join(result)}"
    )
    output = output.replace('\n', '<br>')
    return output

def leave_trends_by_department_role():
    #trying to answer: Leave Trends by Department & Role
    dept_trend = df.groupby("Department")["Days Taken"].sum().reset_index()
    role_trend = df.groupby("Position")["Days Taken"].sum().reset_index()
    dept_role_trend = df.groupby(["Department", "Position"])["Days Taken"].sum().reset_index()

    output = (
        "\n--- Leave by Department ---\n"
        f"{dept_trend.to_string(index=False)}\n\n"
        "--- Leave by Role ---\n"
        f"{role_trend.to_string(index=False)}\n\n"
        "--- Leave by Department & Role ---\n"
        f"{dept_role_trend.to_string(index=False)}"
    )
    output = output.replace('\n', '<br>')
    return output


def month_highest_leave():
    #trying to answer: Are there hotspots of high leave usage that might signal burnout, understaffing, or poor workload balance?
    monthly_trend = df.groupby("month")["Days Taken"].sum().reset_index()
    max_days = monthly_trend["Days Taken"].max()
    highest_months = monthly_trend[monthly_trend["Days Taken"] == max_days]

    output = (
        "--- Leave Days by Month ---\n"
        f"{monthly_trend.to_string(index=False)}\n\n"
        "--- Month(s) with Highest Leave Days ---\n"
        f"{highest_months.to_string(index=False)}"
    )
    output = output.replace('\n', '<br>')
    return output


def most_common_leave_type():
    #trying to answer: What types of leave (e.g., sick, annual, parental) are most common?
    leave_counts = df["Leave Type"].value_counts().reset_index()
    leave_counts.columns = ["Leave Type", "Count"]

    leave_days = df.groupby("Leave Type")["Days Taken"].sum().reset_index().sort_values(
        by="Days Taken", ascending=False
    )
    output = (
        "--- Most Common Leave Types (by count) ---\n"
        f"{leave_counts.to_string(index=False)}\n\n"
        "--- Most Common Leave Types (by total days taken) ---\n"
        f"{leave_days.to_string(index=False)}"
    )

    output = output.replace('\n', '<br>')
    return output


def sick_leave_trends():
    #trying to answer: Are there spikes in sick leave that may indicate health/wellness issues?
    sick_df = df[df["Leave Type"].str.lower() == "sick leave"]
    sick_trend = sick_df.groupby("month")["Days Taken"].sum().reset_index()
    avg_sick = sick_trend["Days Taken"].mean()
    spikes = sick_trend[sick_trend["Days Taken"] > avg_sick]
    output = (
        "--- Sick Leave by Month ---\n"
        f"{sick_trend.to_string(index=False)}\n\n"
        f"Average sick leave days per month: {avg_sick:.2f}\n\n"
        "--- Potential Spikes (above average) ---\n"
        f"{spikes.to_string(index=False) if not spikes.empty else 'No significant spikes detected'}"
    )
    output = output.replace('\n', '<br>')
    return output
    
def get_overall_leave_trends(save_path=None):

    """
    Creates a graph of monthly leave usage from the dataset grouped by leave categories
    :param save_path: String. An optional file save path used for testing
    :return: Returns an embedded HTML image of the graph
    """

    df['Start Date'] = pd.to_datetime(df['Start Date'])
    df['End Date'] = pd.to_datetime(df['End Date'])

    # stops the graph from displaying months in alphabetical order
    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    df['month'] = pd.Categorical(df['month'], categories=month_order, ordered=True)

    monthly_trends = df.groupby(['Leave Type', 'month'])['Days Taken'].sum().reset_index()

    # pivot for plotting
    pivot_trends = monthly_trends.pivot(index='month', columns='Leave Type', values='Days Taken').fillna(0)
    colors = ["#1f3b73", "#2ca6a4", "#f28e2b", "#edc948", "#e15759"]

    fig, ax = plt.subplots(figsize=(8, 4))
    pivot_trends.plot(kind='bar', ax=ax, color=colors)
    ax.set_title('Monthly Leave Trends by Leave Type')
    ax.set_xlabel('Month')
    ax.set_ylabel('Total Days Taken')
    ax.tick_params(axis='x', rotation=45)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    # converting the graph to bytes in memory
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "wb") as f:
            f.write(buf.getvalue())

    # Encoding the image to base64 for HTML embedding
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    html_img = f'<img src="data:image/png;base64,{img_base64}" />'

    return html_img

def employees_near_entitlement(threshold=0.9):

    """
    Calculates when employees are getting close to their maximum entitled leave
    :param threshold: Float. The cutoff for percent of leave used up.
    :return: String. HTML-ready list output of all employees close to their threshold.
    """

    # Creating threshold
    df['Fraction Used'] = df['Leave Taken So Far'] / df['Total Leave Entitlement']

    # Filter employees who are above the threshold
    alert_df = df[df['Fraction Used'] >= threshold].copy()

    if alert_df.empty:
        return "--- Employees Near Entitlement ---<br>No employees are close to exhausting their leave."

    # Format output as a table-like string
    output = "--- Employees Near Entitlement ---<br>"
    output += "Employee Name | Leave Type | % Used | Department<br>"
    output += "--- | --- | --- | ---<br>"

    for _, row in alert_df.iterrows():
        output += f"{row['Employee Name']} | {row['Leave Type']} | {round(row['Fraction Used']*100, 1)}% | {row['Department']}<br>"

    output = output.replace('\n', '<br>')
    return output

def employees_not_taking_leave(threshold=0.1):

    """
    :param threshold: Float. The maximum percentage for leave used up.
    :return: String. HTML-ready list output of all employees not using leave.
    """

    df['Fraction Used'] = df['Leave Taken So Far'] / df['Total Leave Entitlement']
    low_leave_df = df[df['Fraction Used'] <= threshold].copy()

    if low_leave_df.empty:
        return "--- Employees Not Taking Leave ---<br>No employees found below the threshold."

    # Format output as a table-like string
    output = "--- Employees Not Taking Leave ---<br>"
    output += "Employee Name | Leave Type | % Used<br>"
    output += "--- | --- | ---<br>"

    for _, row in low_leave_df.iterrows():
        output += f"{row['Employee Name']} | {row['Leave Type']} | {round(row['Fraction Used']*100, 1)}%<br>"

    output = output.replace('\n', '<br>')
    return output


def department_sick_leave():

    """
    :return: String. HTML-ready list output of all departments with total sick leave days.
    """
    sick_df = df[df["Leave Type"].str.lower().str.contains("sick leave", na=False)]

    if sick_df.empty:
        return "No sick leave records found."
    # Group by department and sum sick leave days
    dept_sick = sick_df.groupby("Department")["Days Taken"].sum().reset_index()
    # Sort descending to see departments with most sick leave
    dept_sick = dept_sick.sort_values(by="Days Taken", ascending=False).reset_index(drop=True)
    output = "--- Departments with Sick Leave Totals ---\n" + dept_sick.to_string(index=False)
    output = output.replace('\n', '<br>')
    return output
