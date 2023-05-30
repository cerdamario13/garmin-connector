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
total_distance_traveled = df['Distance'].astype('float').sum()
total_calories = df['Calories'].astype('float').sum()

# Averages
average_distance_per_activity = df['Distance'].astype('float').mean().round(2)
average_calories_per_activity = df['Calories'].astype('float').mean().round(2)
average_heart_rate_per_activity = df['Avg HR'].astype('float').mean().round(2)

tmp_time = df['TimeNew'].apply(lambda x: datetime.datetime.strptime(x, '%H:%M:%S').time())



print(df)
