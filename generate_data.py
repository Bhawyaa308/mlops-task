import pandas as pd
import numpy as np

np.random.seed(42)

df = pd.DataFrame({
    "open": np.random.uniform(100, 200, 10000),
    "high": np.random.uniform(100, 200, 10000),
    "low": np.random.uniform(100, 200, 10000),
    "close": np.random.uniform(100, 200, 10000),
    "volume": np.random.randint(1000, 5000, 10000)
})

df.to_csv("data.csv", index=False)

print("✅ data.csv generated successfully")