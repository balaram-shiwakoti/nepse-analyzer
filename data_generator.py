# data_generator.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_nepse_data():
    symbols = ["NTC", "GBIME", "NIL", "HDL"]
    base_prices = {"NTC": 900, "GBIME": 250, "NIL": 450, "HDL": 2200}
    
    start_date = datetime.now() - timedelta(days=180)
    date_list = [start_date + timedelta(days=x) for x in range(180)]
    
    all_records = []
    
    np.random.seed(42) # Ensure consistent data generation
    
    for symbol in symbols:
        price = base_prices[symbol]
        for date in date_list:
            # Skip weekends (Saturday and Sunday)
            if date.weekday() in [5, 6]:
                continue
                
            # Random price fluctuation with slight positive trend
            pct_change = np.random.normal(0.0005, 0.02) 
            open_price = price * (1 + pct_change * 0.2)
            close_price = price * (1 + pct_change)
            high_price = max(open_price, close_price) * (1 + abs(np.random.normal(0.005, 0.005)))
            low_price = min(open_price, close_price) * (1 - abs(np.random.normal(0.005, 0.005)))
            volume = int(np.random.exponential(15000) + 1000)
            
            all_records.append({
                "Date": date.strftime("%Y-%m-%d"),
                "Symbol": symbol,
                "Open": round(open_price, 2),
                "High": round(high_price, 2),
                "Low": round(low_price, 2),
                "Close": round(close_price, 2),
                "Volume": volume
            })
            # Carry over yesterday's close price as today's starting reference
            price = close_price
            
    df = pd.DataFrame(all_records)
    df.to_csv("nepse_data.csv", index=False)
    print("✅ Mock NEPSE historical data successfully saved to 'nepse_data.csv'!")

if __name__ == "__main__":
    generate_nepse_data()