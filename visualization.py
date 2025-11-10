# visualization.py

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from models import profit

# --- Font Configuration for Persian/Farsi Fonts ---
# This block tries to set a font that supports Persian characters for plots.
try:
    plt.rcParams['font.family'] = 'Tahoma' # A common font on Windows that supports Farsi
    print("Font set to Tahoma.")
except:
    try:
        plt.rcParams['font.family'] = 'DejaVu Sans' # A common font on Linux
        print("Font set to DejaVu Sans.")
    except:
        print("Warning: Could not set a specific font for Persian characters. Plot labels might not render correctly.")
        # Fallback to default
        pass

plt.rcParams['axes.unicode_minus'] = False # Ensure minus sign is rendered correctly

def plot_profit_changes(results_df):
    """
    Plots the profit of each seller as a function of their price strategy iterations.

    Args:
        results_df (pd.DataFrame): DataFrame containing the simulation results with columns
                                  ['iteration', 'p1', 'profit1', 'p2', 'profit2', ...].
    """
    plt.figure(figsize=(12, 7))
    sns.lineplot(data=results_df, x='iteration', y='profit1', label='Seller 1 Profit ()')
    sns.lineplot(data=results_df, x='iteration', y='profit2', label='Seller 2 Profit ()')
    plt.title('Profit Convergence Over Iterations', fontsize=16)
    plt.xlabel('Iteration ()', fontsize=12)
    plt.ylabel('Profit ()', fontsize=12)
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_nash_equilibrium(results_df):
    """
    Visualizes the Nash Equilibrium point on a 2D plot of seller prices.

    Args:
        results_df (pd.DataFrame): DataFrame containing the simulation results.
                                  The last row is considered the equilibrium.
    """
    nash_eq = results_df.iloc[-1]
    p1_eq = nash_eq['p1']
    p2_eq = nash_eq['p2']

    plt.figure(figsize=(10, 8))
    # Plot the price strategies path
    plt.plot(results_df['p1'], results_df['p2'], marker='o', linestyle='--', label='Strategy Path ( )')
    # Highlight the equilibrium point
    plt.scatter(p1_eq, p2_eq, color='red', s=150, zorder=5, label=f'Nash Equilibrium ( )\nP1={p1_eq:.2f}, P2={p2_eq:.2f}')

    plt.title('Price Strategies and Nash Equilibrium ()', fontsize=16)
    plt.xlabel('Seller 1 Price ()', fontsize=12)
    plt.ylabel('Seller 2 Price ()', fontsize=12)
    plt.legend()
    plt.grid(True)
    plt.axhline(p2_eq, color='gray', linestyle=':', linewidth=1)
    plt.axvline(p1_eq, color='gray', linestyle=':', linewidth=1)
    plt.show()

def plot_social_influence_impact(results_no_influence, results_with_influence):
    """
    Compares the final profits of sellers with and without social influence.

    Args:
        results_no_influence (pd.DataFrame): Simulation results without social influence.
        results_with_influence (pd.DataFrame): Simulation results with social influence.
    """
    profit1_no_influence = results_no_influence['profit1'].iloc[-1]
    profit2_no_influence = results_no_influence['profit2'].iloc[-1]

    profit1_with_influence = results_with_influence['profit1'].iloc[-1]
    profit2_with_influence = results_with_influence['profit2'].iloc[-1]

    labels = ['Seller 1 (فروشنده ۱)', 'Seller 2 (فروشنده ۲)']
    profits_no_influence = [profit1_no_influence, profit2_no_influence]
    profits_with_influence = [profit1_with_influence, profit2_with_influence]

    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(12, 7))
    rects1 = ax.bar(x - width/2, profits_no_influence, width, label='Without Social Influence ()')
    rects2 = ax.bar(x + width/2, profits_with_influence, width, label='With Social Influence ()')

    ax.set_ylabel('Equilibrium Profit ( )', fontsize=12)
    ax.set_title('Impact of Social Influence on Seller Profits ( )', fontsize=16)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    # Attach a text label above each bar in rects, displaying its height.
    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)

    fig.tight_layout()
    plt.grid(axis='y', linestyle='--')
    plt.show()
