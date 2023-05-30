import wrangles
import pandas as pd
import json
import datetime

def all_runs():
    """
    Return all runs from the data file
    """
    # Inputs for running activities
    data_file = "Garmin_Data.csv"
    data_path = f"data/{data_file}"
    recipe_file = "src/activities.wrgl.yaml"

    # Select Activities Type Column that contains the a keyword (run)
    query = """
    SELECT *
    FROM df
    WHERE Activity_Type LIKE '%run%'
    """

    vars = {
        "data_path": data_path,
        "query": query,
    }

    df = wrangles.recipe.run(recipe=recipe_file, variables=vars)
    df = df.to_json(orient="table")

    return json.loads(df)
    

def all_runs_summaries():
    """
    Return a summary of activities
    """

    # Inputs for running activities
    data_file = "Garmin_Data.csv"
    data_path = f"data/{data_file}"
    recipe_file = "src/activities.wrgl.yaml"


    query = """
    SELECt *
    FROM df
    WHERE Activity_Type LIKE '%run%'
    """

    vars = {
        "data_path": data_path,
        "query": query
    }

    df = wrangles.recipe.run(recipe=recipe_file, variables=vars)

    # Overall Sums
    total_distance = df['Distance'].astype('float').sum()
    total_calories = df['Calories'].astype('float').sum()
    total_time = {
        'days': pd.to_timedelta(df['Time']).sum().components.days,
        'hours': pd.to_timedelta(df['Time']).sum().components.hours,
        'minutes': pd.to_timedelta(df['Time']).sum().components.minutes
    }

    # Averages
    average_distance_per_activity = df['Distance'].astype('float').mean().round(2)
    average_calories_per_activity = df['Calories'].astype('float').mean().round(2)
    average_heart_rate_per_activity = df['Avg HR'].astype('float').mean().round(2)

    summaries_dict = {
        'total_distance': total_distance,
        'total_calories': total_calories,
        'total_time': total_time,
        'average_distance_per_activity': average_distance_per_activity,
        'average_calories_per_activity': average_calories_per_activity,
        'average_heart_rate_per_activity': average_heart_rate_per_activity
    }

    return summaries_dict

