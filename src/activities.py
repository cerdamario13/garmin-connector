import wrangles
import pandas as pd
import datetime

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
print(df)

