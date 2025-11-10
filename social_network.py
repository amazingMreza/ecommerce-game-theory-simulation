# social_network.py

import networkx as nx
import random
import numpy as np

# A higher weight for influencers
INFLUENCER_WEIGHT = 5.0
# Base weight for regular customers
REGULAR_WEIGHT = 1.0

def create_customer_network(customer_ids, n_influencers=10, p_connection=0.05):
 
    # Create an Erdos-Renyi random graph. This model assumes that any two customers
    # have a small probability 'p' of being connected.
    num_customers = len(customer_ids)
    G = nx.erdos_renyi_graph(n=num_customers, p=p_connection, seed=42)
    
    # Map graph nodes (0, 1, 2...) to actual CustomerIDs for clarity
    mapping = {i: customer_id for i, customer_id in enumerate(customer_ids)}
    G = nx.relabel_nodes(G, mapping)

    # Assign a base influence score to all nodes
    for node in G.nodes():
        G.nodes[node]['influence_score'] = REGULAR_WEIGHT

    # Randomly select some nodes as influencers and give them a higher score
    if n_influencers > 0 and num_customers > n_influencers:
        influencer_nodes = random.sample(list(G.nodes()), n_influencers)
        for node in influencer_nodes:
            G.nodes[node]['influence_score'] = INFLUENCER_WEIGHT
            
    return G

def calculate_total_influence(graph):
    """
    Calculates the total influence score of the entire network.
    This is a simple sum of the influence scores of all nodes.

    Args:
        graph (nx.Graph): The customer network graph.

    Returns:
        float: The sum of all influence scores in the network.
    """
    total_influence = sum(data['influence_score'] for node, data in graph.nodes(data=True))
    return total_influence