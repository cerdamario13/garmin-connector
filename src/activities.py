import wrangles
import pandas as pd
import json
import datetime

def delete_col(df):
    """
    Delete the input columns
    """
    
    df.drop(["Training Stress Score®"], axis=1)
    
    return df

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

    df = wrangles.recipe.run(recipe=recipe_file, variables=vars, functions=[delete_col])
    df = df.to_json(orient="table")

    return json.loads(df)

def all_bike_rides():
    """
    Return all of the bike rides
    """
    
    # Inputs for bike activities
    data_file = "Garmin_Data.csv"
    data_path = f"data/{data_file}"
    recipe_file = "src/activities.wrgl.yaml"
    
    # Select Activities type that have the keyword (cycle)
    query = """
    SELECT *
    FROM df
    WHERE Activity_Type LIKE '%cyc%'
    """
    
    vars = {
        "data_path": data_path,
        "query": query
    }
    
    df = wrangles.recipe.run(recipe=recipe_file, variables=vars, functions=[delete_col])
    df = df.to_json(orient="table")
    
    return json.loads(df)
    

def all_runs_summaries(keyword):
    """
    Return a summary of activities
    """

    # Inputs for running activities
    data_file = "Garmin_Data.csv"
    data_path = f"data/{data_file}"
    recipe_file = "src/activities.wrgl.yaml"


    query = f"""
    SELECt *
    FROM df
    WHERE Activity_Type LIKE '%{keyword}%'
    """

    vars = {
        "data_path": data_path,
        "query": query
    }

    df = wrangles.recipe.run(recipe=recipe_file, variables=vars, functions=[delete_col])

    # Overall Sums
    total_distance = df['Distance'].astype('float').sum().round(2)
    total_calories = df['Calories'].astype('float').sum().round(2)
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

