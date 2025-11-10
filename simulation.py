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
