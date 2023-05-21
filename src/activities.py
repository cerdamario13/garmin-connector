import wrangles
import pandas as pd
import datetime


data_file = "Garmin_Data.csv"
data_path = f"data/{data_file}"
recipe_file = "src/activities.wrgl.yaml"


vars = {
    "data_path": data_path
}

df = wrangles.recipe.run(recipe=recipe_file, variables=vars)
print(df)

