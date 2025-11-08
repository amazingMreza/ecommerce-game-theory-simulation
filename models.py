# file: models.py

import pandas as pd
from data_loader import load_and_preprocess_data 

TARGET_PRODUCT_CODE = '85123A'
COST = 1.5                  
ALPHA = 0.8                 
BETA = 25                   
GAMMA = 0.5                 

def demand(price_i: float, ad_budget_i: float, price_j: float, base_demand: float, influence_score: float = 0) -> float:
    price_effect = BETA * (price_j - price_i)
    ad_effect = ALPHA * ad_budget_i
    social_effect = GAMMA * influence_score
    
    
    calculated_demand = base_demand + ad_effect + price_effect + social_effect
    return max(0, calculated_demand)

def profit(price_i: float, ad_budget_i: float, demand_i: float) -> float:
    return (price_i - COST) * demand_i - ad_budget_i

def create_seller_models(df: pd.DataFrame) -> tuple[dict, dict]:
    print("\n--- Task II: Seller, Demand, and Profit Modeling ---")
    
    df_product = df[df['StockCode'] == TARGET_PRODUCT_CODE].copy()

    print(f"تحلیل برای کالای انتخاب شده با کد: {TARGET_PRODUCT_CODE}")
    print(f"قیمت‌های مختلف فروش این کالا: {df_product['Price'].unique()}")

    # ایجاد دو فروشنده فرضی بر اساس میانه قیمت
    median_price = df_product['Price'].median()
    seller1_data = df_product[df_product['Price'] < median_price]
    seller2_data = df_product[df_product['Price'] >= median_price]
    
    # محاسبه تقاضای پایه
    base_demand_1 = seller1_data['Quantity'].mean()
    base_demand_2 = seller2_data['Quantity'].mean()

    # ایجاد مدل فروشندگان به صورت دیکشنری برای دسترسی آسان
    seller1_model = {
        'name': 'Seller 1 (Low Price)',
        'base_demand': base_demand_1,
        'avg_price': seller1_data['Price'].mean(),
        'data': seller1_data
    }
    
    seller2_model = {
        'name': 'Seller 2 (High Price)',
        'base_demand': base_demand_2,
        'avg_price': seller2_data['Price'].mean(),
        'data': seller2_data
    }
    
    print(f"\nمیانه قیمت برای این کالا: {median_price:.2f}")
    print(f"مدل فروشنده ۱ ایجاد شد: {seller1_model['name']} با تقاضای پایه {seller1_model['base_demand']:.2f}")
    print(f"مدل فروشنده ۲ ایجاد شد: {seller2_model['name']} با تقاضای پایه {seller2_model['base_demand']:.2f}")
    print("\nتوابع تقاضا و سود با موفقیت تعریف شدند.")
    print("-" * 50)

    return seller1_model, seller2_model

# ==============================================================
# Testing
# ==============================================================
if __name__ == '__main__':
    print("--- TESTING 'models.py' ---")
    
    data_file = 'online_retail_II.xlsx'
    cleaned_data = load_and_preprocess_data(data_file)
    
    s1_model, s2_model = create_seller_models(cleaned_data)
    
    print("\n--- Testing Demand and Profit Functions (Example Scenario) ---")
    p1 = 2.0  # 1st Seller's Offer Price
    m1 = 10   # 1st Seller's budjet
    p2 = 2.5  # 2nd Seller's Offer Price
    m2 = 15   # 2nd Seller's budjet
    
    # محاسبه تقاضا و سود برای فروشنده ۱
    d1 = demand(price_i=p1, ad_budget_i=m1, price_j=p2, base_demand=s1_model['base_demand'])
    prof1 = profit(price_i=p1, ad_budget_i=m1, demand_i=d1)
    
    # محاسبه تقاضا و سود برای فروشنده ۲
    d2 = demand(price_i=p2, ad_budget_i=m2, price_j=p1, base_demand=s2_model['base_demand'])
    prof2 = profit(price_i=p2, ad_budget_i=m2, demand_i=d2)

    print(f"Scenario: P1=${p1}, M1=${m1} | P2=${p2}, M2=${m2}")
    print(f"1st Seller: Demand = {d1:.2f}, Profit = ${prof1:.2f}")
    print(f"2nd Seller: Demand = {d2:.2f}, Profit = ${prof2:.2f}")
    print("\n--- 'models.py' test completed successfully ---")
