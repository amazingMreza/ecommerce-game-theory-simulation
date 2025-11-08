import numpy as np  # <<<< این خط برای حل مشکل اضافه شده و ضروری است
import pandas as pd

# Import functions and constants from our other modules
from data_loader import load_and_preprocess_data
from models import create_seller_models, demand, profit, COST, ALPHA, BETA, GAMMA

def run_simulation(seller1_model, seller2_model, price_range, ad_budget_range, iterations=15):
    """
    Runs the iterative game simulation to find the Nash Equilibrium.
    
    Args:
        seller1_model (dict): The model dictionary for seller 1.
        seller2_model (dict): The model dictionary for seller 2.
        price_range (np.ndarray): Array of possible prices.
        ad_budget_range (np.ndarray): Array of possible advertising budgets.
        iterations (int): The maximum number of iterations for the simulation.

    Returns:
        tuple[dict, list]: A tuple containing the Nash Equilibrium and the history of strategies.
    """

    def find_best_response(opponent_price, opponent_ad_budget, base_demand):
        """
        Finds the best strategy (price and ad budget) in response to the opponent's strategy.
        This is a nested function because it's only used within the simulation process.
        """
        best_profit = -np.inf  # Requires numpy
        best_price = price_range[0]
        best_ad_budget = ad_budget_range[0]

        for p in price_range:
            for m in ad_budget_range:
                # Calculate demand and profit for the current strategy (p, m)
                d = demand(p, m, opponent_price, base_demand)
                current_profit = profit(p, m, d)
                
                if current_profit > best_profit:
                    best_profit = current_profit
                    best_price = p
                    best_ad_budget = m
        
        return best_price, best_ad_budget, best_profit

    # --- Simulation Initialization ---
    # Start with the historical average prices and a default ad budget
    p1 = seller1_model['avg_price']
    p2 = seller2_model['avg_price']
    m1, m2 = 30, 30  # Initial ad budgets

    history = []
    
    print("\n--- Starting Nash Equilibrium Search Process ---")
    print(f"Initial Strategy: P1={p1:.2f}, M1={m1} | P2={p2:.2f}, M2={m2}")

    for i in range(iterations):
        # Seller 1 finds its best response to Seller 2's current strategy
        p1_new, m1_new, _ = find_best_response(p2, m2, seller1_model['base_demand'])
        
        # Seller 2 finds its best response to Seller 1's *new* strategy
        p2_new, m2_new, _ = find_best_response(p1_new, m1_new, seller2_model['base_demand'])

        # Store history for visualization
        history.append({'iter': i, 'p1': p1_new, 'm1': m1_new, 'p2': p2_new, 'm2': m2_new})

        print(f"Iteration {i+1}: P1={p1_new:.2f}, M1={m1_new} | P2={p2_new:.2f}, M2={m2_new}")

        # Check for convergence
        if abs(p1_new - p1) < 0.01 and abs(p2_new - p2) < 0.01 and \
           abs(m1_new - m1) < 1 and abs(m2_new - m2) < 1:
            print("\nConvergence achieved!")
            break
            
        # Update strategies for the next iteration
        p1, m1 = p1_new, m1_new
        p2, m2 = p2_new, m2_new

    nash_equilibrium = {'p1': p1, 'm1': m1, 'p2': p2, 'm2': m2}
    return nash_equilibrium, history

# ==============================================================
# Main execution block for standalone testing
# ==============================================================
if __name__ == '__main__':
    print("--- EXECUTING 'simulation.py' FOR TASK III ---")

    # --- Task I: Data Loading ---
    data_file = 'online_retail_II.xlsx'
    cleaned_data = load_and_preprocess_data(data_file)
    
    # --- Task II: Model Creation ---
    s1_model, s2_model = create_seller_models(cleaned_data)

    # --- Task III: Simulation ---
    # Define the search space for strategies
    price_space = np.arange(2.0, 4.0, 0.1)      # Price range from $2.0 to $3.9
    ad_budget_space = np.arange(10, 100, 5)   # Ad budget range from $10 to $95

    # Run the simulation to find the equilibrium
    equilibrium, sim_history = run_simulation(
        s1_model, 
        s2_model,
        price_range=price_space,
        ad_budget_range=ad_budget_space,
        iterations=15
    )

    print("\n-------------------------------------------")
    print("      Nash Equilibrium Found:")
    print("-------------------------------------------")
    print(f"Seller 1 Strategy: Price = ${equilibrium['p1']:.2f}, Ad Budget = ${equilibrium['m1']}")
    print(f"Seller 2 Strategy: Price = ${equilibrium['p2']:.2f}, Ad Budget = ${equilibrium['m2']}")
    print("\n--- 'simulation.py' execution completed successfully ---")
