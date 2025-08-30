import pandas as pd
import numpy as np

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
    

def annual_earned_leave_trends():
    #trying to answer: Is annual leave being planned and spread evenly, or clumped at year-end?
    annual_df = df[df["Leave Type"].str.lower().str.contains("earned", na=False)]
    monthly_leave = annual_df.groupby("month")["Days Taken"].sum().reset_index()
    # Calculate percentage of total annual leave per month
    total_leave = monthly_leave["Days Taken"].sum()
    monthly_leave["Percentage of Total"] = (monthly_leave["Days Taken"] / total_leave * 100).round(2)
    month_order = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    monthly_leave["month"] = pd.Categorical(monthly_leave["month"], categories=month_order, ordered=True)
    monthly_leave = monthly_leave.sort_values("month").reset_index(drop=True)
    # Format output
    output = (
        "--- Annual Leave by Month ---\n"
        f"{monthly_leave.to_string(index=False)}\n\n"
    )
    return output
    


def overlapping_leave_trends():
    #trying to answer: Are multiple employees in the same department/team on leave at overlapping times?
     # Convert Start/End dates to datetime
    df["Start Date"] = pd.to_datetime(df["Start Date"])
    df["End Date"] = pd.to_datetime(df["End Date"])

    overlaps = []

    # Group by Department
    for dept, group in df.groupby("Department"):
        group = group.sort_values("Start Date").reset_index(drop=True)
        n = len(group)
        
        # Check each pair of employees for overlap
        for i in range(n):
            emp1 = group.iloc[i]
            for j in range(i+1, n):
                emp2 = group.iloc[j]
                
                # Check if dates overlap
                latest_start = max(emp1["Start Date"], emp2["Start Date"])
                earliest_end = min(emp1["End Date"], emp2["End Date"])
                
                if latest_start <= earliest_end:  # There is overlap
                    overlaps.append({
                        "Department": dept,
                        "Employee 1": emp1["Employee Name"],
                        "Employee 2": emp2["Employee Name"],
                        "Overlap Start": latest_start.date(),
                        "Overlap End": earliest_end.date()
                    })

    if not overlaps:
        return "No overlapping leaves found within any department."
    
    overlap_df = pd.DataFrame(overlaps)
    
    return overlap_df

    



test = overlapping_leave_trends()
print(test)