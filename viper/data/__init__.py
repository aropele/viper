from pathlib import Path
import pandas as pd
    

mtcars = pd.read_csv(Path(__file__).parent / "mtcars.csv")