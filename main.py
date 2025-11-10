# main.py

"""
Main execution script for the E-commerce Game Theory Simulation project.
This script orchestrates the entire process from setup and simulation to visualization,
serving as the single entry point for running the project.

This version is compatible with the iterative best-response simulation model.
"""

import numpy as np
import pandas as pd

# Import necessary functions from other modules
from data_loader import load_and_preprocess_data  # NEW: Import the data loader function
from models import create_seller_models, demand, profit
from simulation import run_simulation
from visualization import (
    plot_profit_changes,
    plot_nash_equilibrium,
    plot_social_influence_impact
)
from social_network import create_customer_network, calculate_total_influence

def run_full_project():
    """
    Executes all tasks of the project sequentially and displays the results.
    """
    print("=========================================================")
    print("   شروع شبیه‌سازی رقابت قیمت در بازار تجارت الکترونیک   ")
    print("=========================================================\n")

    # --- بخش صفر: بارگذاری و پیش‌پردازش داده‌ها (Task I) ---
    # FIX: This step was missing. We must load data first.
    print("--- Task I: Loading and Preprocessing Data ---")
    file_path = 'online_retail_II.xlsx'  # Make sure this path is correct
    try:
        df = load_and_preprocess_data(file_path)
        print(f"✅ Data loaded and preprocessed successfully from '{file_path}'.")
    except FileNotFoundError:
        print(f"❌ ERROR: Data file not found at '{file_path}'. Please check the file path.")
        return # Stop execution if data is not found
    print("-" * 50)


    # --- بخش آماده‌سازی (Task II) ---
    print("\n--- Task II: Creating Seller Models and Strategy Spaces ---")
    # FIX: Pass the loaded dataframe 'df' to the function.
    seller1_model, seller2_model = create_seller_models(df)
    print("✅ Seller models created successfully.")

    # Define the strategy space for sellers to search within
    price_range = np.arange(10, 30, 0.5)
    ad_budget_range = np.arange(20, 80, 5)
    print("✅ Strategy spaces (price and ad budget ranges) defined.")
    print("-" * 50)


    # --- بخش سوم: شبیه‌سازی بدون تاثیر شبکه اجتماعی (Task III) ---
    print("\n--- Task III: Running Simulation without Social Influence ---")
    
    eq_no_influence, history_no_influence = run_simulation(
        seller1_model=seller1_model,
        seller2_model=seller2_model,
        price_range=price_range,
        ad_budget_range=ad_budget_range,
        influence_score=0,
        iterations=15
    )
    
    results_no_influence = pd.DataFrame(history_no_influence)
    results_no_influence['iteration'] = range(1, len(results_no_influence) + 1)

    results_no_influence['demand1'] = results_no_influence.apply(lambda row: demand(row['p1'], row['m1'], row['p2'], seller1_model['base_demand'], 0), axis=1)
    results_no_influence['profit1'] = results_no_influence.apply(lambda row: profit(row['p1'], row['m1'], row['demand1']), axis=1)
    results_no_influence['demand2'] = results_no_influence.apply(lambda row: demand(row['p2'], row['m2'], row['p1'], seller2_model['base_demand'], 0), axis=1)
    results_no_influence['profit2'] = results_no_influence.apply(lambda row: profit(row['p2'], row['m2'], row['demand2']), axis=1)

    print("\n✅ Equilibrium Found (Without Social Influence):")
    print(f"   - Seller 1 Final Price: {eq_no_influence['p1']:.2f}, Ad Budget: {eq_no_influence['m1']}")
    print(f"   - Seller 2 Final Price: {eq_no_influence['p2']:.2f}, Ad Budget: {eq_no_influence['m2']}")
    print("-" * 50)


       # --- بخش چهارم: شبیه‌سازی با تأثیر شبکه اجتماعی (Task IV) ---
        # --- بخش چهارم: شبیه‌سازی با تأثیر شبکه اجتماعی (Task IV) ---
    print("\n--- Task IV: Running Simulation WITH Social Influence ---")
    print("Creating social network and calculating influence score...")

    # ایجاد شبکه مشتری بر اساس تعریف جدید
    customer_graph = create_customer_network(
        customer_ids=df['Customer ID'].unique(),
        n_influencers=10,
        p_connection=0.05
    )

    influence_score = calculate_total_influence(customer_graph)
    print(f" Social network created. Total Influence Score: {influence_score:.2f}")

    eq_with_influence, history_with_influence = run_simulation(
        seller1_model=seller1_model,
        seller2_model=seller2_model,
        price_range=price_range,
        ad_budget_range=ad_budget_range,
        influence_score=influence_score,
        iterations=15
    )

    results_with_influence = pd.DataFrame(history_with_influence)
    results_with_influence['iteration'] = range(1, len(results_with_influence) + 1)

    results_with_influence['demand1'] = results_with_influence.apply(
        lambda row: demand(row['p1'], row['m1'], row['p2'],
                           seller1_model['base_demand'], influence_score), axis=1)
    results_with_influence['profit1'] = results_with_influence.apply(
        lambda row: profit(row['p1'], row['m1'], row['demand1']), axis=1)
    results_with_influence['demand2'] = results_with_influence.apply(
        lambda row: demand(row['p2'], row['m2'], row['p1'],
                           seller2_model['base_demand'], influence_score), axis=1)
    results_with_influence['profit2'] = results_with_influence.apply(
        lambda row: profit(row['p2'], row['m2'], row['demand2']), axis=1)

    print("\n✅ Equilibrium Found (With Social Influence):")
    print(f"   - Seller 1 Final Price: {eq_with_influence['p1']:.2f}, Ad Budget: {eq_with_influence['m1']}")
    print(f"   - Seller 2 Final Price: {eq_with_influence['p2']:.2f}, Ad Budget: {eq_with_influence['m2']}")
    print("-" * 50)

    # --- بخش پنجم: مصورسازی نتایج (Task V) ---
    print("\n--- Task V: Generating Visualizations ---")
    print("Displaying plots... Please close each plot window to proceed to the next one.")

    print(" -> Generating Plot 1: Profit Convergence...")
    plot_profit_changes(results_no_influence)

    print(" -> Generating Plot 2: Nash Equilibrium Point...")
    plot_nash_equilibrium(results_no_influence)

    print(" -> Generating Plot 3: Impact of Social Influence...")
    plot_social_influence_impact(results_no_influence, results_with_influence)

    print("\n=========================================================")
    print("         🚀 شبیه‌سازی و مصورسازی با موفقیت تمام شد         ")
    print("=========================================================")


if __name__ == "__main__":
    # Main entry point of the application
    run_full_project()
