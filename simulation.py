# simulation.py

import numpy as np
import pandas as pd

# Import functions and constants from other modules
from data_loader import load_and_preprocess_data
from models import create_seller_models, demand, profit, COST, ALPHA, BETA, GAMMA
# NEW: Import social network functions
from social_network import create_customer_network, calculate_total_influence

def run_simulation(seller1_model, seller2_model, price_range, ad_budget_range, influence_score=0, iterations=15):
    """
    Runs the iterative game simulation to find the Nash Equilibrium.
    Now includes social influence in its calculations.
    """
    
    # Nested function to find the best response for a seller
    def find_best_response(opponent_price, opponent_ad_budget, base_demand):
        best_profit = -np.inf
        best_price = price_range[0]
        best_ad_budget = ad_budget_range[0]

        for p in price_range:
            for m in ad_budget_range:
                # UPDATED: Pass the influence_score to the demand function
                d = demand(p, m, opponent_price, base_demand, influence_score)
                current_profit = profit(p, m, d)
                
                if current_profit > best_profit:
                    best_profit = current_profit
                    best_price = p
                    best_ad_budget = m
        
        return best_price, best_ad_budget, best_profit

    # --- Simulation Initialization ---
    p1 = seller1_model['avg_price']
    p2 = seller2_model['avg_price']
    m1, m2 = 30, 30
    history = []
    
    print(f"\n--- Starting Nash Equilibrium Search (Influence Score: {influence_score:.2f}) ---")
    
    for i in range(iterations):
        p1_new, m1_new, _ = find_best_response(p2, m2, seller1_model['base_demand'])
        p2_new, m2_new, _ = find_best_response(p1_new, m1_new, seller2_model['base_demand'])

        history.append({'iter': i, 'p1': p1_new, 'm1': m1_new, 'p2': p2_new, 'm2': m2_new})
        
        if abs(p1_new - p1) < 0.01 and abs(p2_new - p2) < 0.01 and \
           abs(m1_new - m1) < 1 and abs(m2_new - m2) < 1:
            print(f"Convergence achieved at iteration {i+1}!")
            break
        
        p1, m1, p2, m2 = p1_new, m1_new, p2_new, m2_new

    nash_equilibrium = {'p1': p1, 'm1': m1, 'p2': p2, 'm2': m2}
    return nash_equilibrium, history


if __name__ == '__main__':
    # --- Task I & II: Data Loading and Model Creation ---
    data_file = 'online_retail_II.xlsx'
    cleaned_data = load_and_preprocess_data(data_file)
    s1_model, s2_model = create_seller_models(cleaned_data)

    # --- Task IV: Create Customer Network ---
    # Get all unique customer IDs from the dataset
    all_customer_ids = cleaned_data['Customer ID'].dropna().unique().tolist()

    # Define strategy spaces
    price_space = np.arange(2.0, 4.5, 0.1) # Expanded price range for new scenarios
    ad_budget_space = np.arange(10, 100, 5)

    # --- SCENARIO 1: LOW SOCIAL INFLUENCE ---
    print("\n=================================================")
    print("      SCENARIO 1: LOW SOCIAL INFLUENCE")
    print("=================================================")
    # Create a network with a small number of influencers
    low_influence_network = create_customer_network(all_customer_ids, n_influencers=10)
    low_influence_score = calculate_total_influence(low_influence_network)

    eq1, _ = run_simulation(
        s1_model, s2_model, price_space, ad_budget_space, 
        influence_score=low_influence_score
    )
    
    # Calculate profits at equilibrium for Scenario 1
    d1_eq1 = demand(eq1['p1'], eq1['m1'], eq1['p2'], s1_model['base_demand'], low_influence_score)
    profit1_eq1 = profit(eq1['p1'], eq1['m1'], d1_eq1)
    d2_eq1 = demand(eq1['p2'], eq1['m2'], eq1['p1'], s2_model['base_demand'], low_influence_score)
    profit2_eq1 = profit(eq1['p2'], eq1['m2'], d2_eq1)

    # --- SCENARIO 2: HIGH SOCIAL INFLUENCE (e.g., successful word-of-mouth campaign) ---
    print("\n=================================================")
    print("      SCENARIO 2: HIGH SOCIAL INFLUENCE")
    print("=================================================")
    # Create a network with a large number of influencers
    high_influence_network = create_customer_network(all_customer_ids, n_influencers=100)
    high_influence_score = calculate_total_influence(high_influence_network)

    eq2, _ = run_simulation(
        s1_model, s2_model, price_space, ad_budget_space, 
        influence_score=high_influence_score
    )
    
    # Calculate profits at equilibrium for Scenario 2
    d1_eq2 = demand(eq2['p1'], eq2['m1'], eq2['p2'], s1_model['base_demand'], high_influence_score)
    profit1_eq2 = profit(eq2['p1'], eq2['m1'], d1_eq2)
    d2_eq2 = demand(eq2['p2'], eq2['m2'], eq2['p1'], s2_model['base_demand'], high_influence_score)
    profit2_eq2 = profit(eq2['p2'], eq2['m2'], d2_eq2)


    # --- FINAL ANALYSIS AND COMPARISON ---
    print("\n\n*******************************************")
    print("         FINAL ANALYSIS & COMPARISON")
    print("*******************************************")
    print("\n--- Low Influence Scenario ---")
    print(f"Equilibrium: P1=${eq1['p1']:.2f}, M1=${eq1['m1']} | P2=${eq2['p1']:.2f}, M2=${eq1['m2']}")
    print(f"Profits:     Profit1=${profit1_eq1:.2f} | Profit2=${profit2_eq1:.2f}")

    print("\n--- High Influence Scenario ---")
    print(f"Equilibrium: P1=${eq2['p2']:.2f}, M1=${eq2['m2']} | P2=${eq2['p2']:.2f}, M2=${eq2['m2']}")
    print(f"Profits:     Profit1=${profit1_eq2:.2f} | Profit2=${profit2_eq2:.2f}")
    print("\n*******************************************")
