import click
import pandas as pd
import numpy as np
import math
from pathlib import Path

@click.command()
@click.argument("input", type=click.Path(exists=True, path_type=Path))
@click.option("--output", default=Path("./output.csv"), type=click.Path(path_type=Path))
def wrangle(input: Path(), output: Path()) -> None:

    df = pd.read_csv(input)
    df.drop(columns="WOODLAND_COVER", inplace=True)

    df.rename(
    columns={"LAD20CD": "Local authority code", 
             "LAD20NM": "Local authority",
             "WOODLAND_AREA": "Woodland Area", 
             "AREALHECT": "Standard Area",
             "Percentage of area": "Woodland area as percentage of standard area"
             },
    inplace=True,
    )

    id_vars = ["Local authority code", "Local authority"]
    value_vars = ["Standard Area", "Woodland Area", "Woodland area as percentage of standard area"]

    df = pd.melt(df, id_vars, value_vars, var_name="Measure", value_name="Observation")
    
    df['Year'] = 2020
    df['Unit'] = df.apply(lambda x: 'Hectares' if x['Measure'] == "Standard Area" 
                      else 'Hectares' if x['Measure'] == 'Woodland Area' 
                      else 'Percent' if x['Measure'] == 'Woodland area as percentage of standard area'
                      else '',
                      axis=1)

    df["Observation"] = df["Observation"].astype(float).round(2)

    df = df[['Year', 'Local authority code', 'Local authority', 'Measure', 'Unit', 'Observation']]
    df.to_csv(output, index=False)
    return

if __name__ == "__main__":
    wrangle()