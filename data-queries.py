import pandas as pd
import matplotlib as plt
import base64
import os
import io

df = pd.read_csv('leave_data\employee leave tracking data.csv')

def findlowestleave():
    #trying to answer: Who has the lowest remaining leave balance (at risk of running out)?
    min_leave = df["Remaining Leaves"].min()
    names = df.loc[df['Remaining Leaves'] == min_leave, "Employee Name"]
    result = names.tolist()
    #still need to figure out the thought process being displayed
    return("Employee(s) with lowest remaining leave:", result)

def findhighestleave():
    #trying to answer: Who has unusually high unused leave (might need reminders before carryover/expiry)?
    max_leave = df["Remaining Leaves"].max()
    names = df.loc[df["Remaining Leaves"] == max_leave, "Employee Name"]
    result = names.tolist()
    #still need to figure out the thought process being displayed
    return("Employee(s) with highest remaining leave:", result)

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

    return output
    
def get_overall_leave_trends(save_path=None):
    df['Start Date'] = pd.to_datetime(df['Start Date'])
    df['End Date'] = pd.to_datetime(df['End Date'])

    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    df['month'] = pd.Categorical(df['month'], categories=month_order, ordered=True)

    monthly_trends = df.groupby(['Leave Type', 'month'])['Days Taken'].sum().reset_index()

    # pivot for plotting
    pivot_trends = monthly_trends.pivot(index='month', columns='Leave Type', values='Days Taken').fillna(0)

    fig, ax = plt.subplots(figsize=(12, 6))
    pivot_trends.plot(kind='bar', ax=ax)
    ax.set_title('Monthly Leave Trends by Leave Type')
    ax.set_xlabel('Month')
    ax.set_ylabel('Total Days Taken')
    ax.tick_params(axis='x', rotation=45)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "wb") as f:
            f.write(buf.getvalue())

    # Encode to base64
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    html_img = f'<img src="data:image/png;base64,{img_base64}" />'

    return html_img

get_overall_leave_trends(save_path="leave_data/leave_trends.png")

test = sick_leave_trends()
print(test)