import networkx as nx
import matplotlib.pyplot as plt
import copy
import argparse

def initialize_routing_tables(G, nodes):
    """Initialize routing tables for each router with infinite distances except for direct neighbors."""
    routing_tables = {}
    for node in nodes:
        routing_tables[node] = {}
        for dest in nodes:
            if dest == node:
                routing_tables[node][dest] = {'cost': 0, 'next_hop': node}
            elif dest in G.neighbors(node):
                routing_tables[node][dest] = {'cost': G[node][dest]['weight'], 'next_hop': dest}
            else:
                routing_tables[node][dest] = {'cost': float('inf'), 'next_hop': None}
    return routing_tables

def update_routing_tables(G, routing_tables, nodes):
    """Simulate one round of RIP distance vector exchange and update, tracking changes."""
    updated = False
    new_tables = copy.deepcopy(routing_tables)
    changes = []  # List to store change descriptions
    
    for router in nodes:
        router_changes = []
        for neighbor in G.neighbors(router):
            for dest in nodes:
                if dest != router:
                    current_cost = routing_tables[router][dest]['cost']
                    # Cost to neighbor + neighbor's cost to destination
                    new_cost = G[router][neighbor]['weight'] + routing_tables[neighbor][dest]['cost']
                    if new_cost < current_cost:
                        new_tables[router][dest]['cost'] = new_cost
                        new_tables[router][dest]['next_hop'] = neighbor
                        updated = True
                        # Record the change
                        router_changes.append(
                            f"Updated route to {dest}: cost changed from {current_cost} to {new_cost}, "
                            f"next hop set to {neighbor}"
                        )
        if router_changes:
            changes.append(f"- Router {router}: {', '.join(router_changes)}")
    
    return new_tables, updated, changes

def rip_algorithm(G, source, destination, max_iterations=10, selected_router=None):
    """Run RIP algorithm to find shortest path from source to destination."""
    nodes = list(G.nodes)
    routing_tables = initialize_routing_tables(G, nodes)
    
    # Validate selected_router if provided
    if selected_router and selected_router not in nodes:
        raise ValueError(f"Router {selected_router} not found in the network.")
    
    # Determine which routers to display
    display_nodes = [selected_router] if selected_router else nodes
    
    print("## Initial Routing Tables:")
    print_routing_tables(routing_tables, display_nodes)
    
    # Iterate until convergence or max iterations
    for i in range(max_iterations):
        routing_tables, updated, changes = update_routing_tables(G, routing_tables, nodes)
        print(f"\n## After Iteration {i+1}:")
        print_routing_tables(routing_tables, display_nodes)
        # Print summary of changes
        print(f"\n### Summary of Changes in Iteration {i+1}:")
        if changes:
            for change in changes:
                print(change)
        else:
            print("No changes occurred in this iteration.")
        if not updated:
            print("Converged!")
            break
    
    # Extract shortest path from source to destination
    path = []
    current = source
    while current != destination:
        path.append(current)
        next_hop = routing_tables[current][destination]['next_hop']
        if next_hop is None:
            return None, routing_tables
        current = next_hop
    path.append(destination)
    
    return path, routing_tables

def print_routing_tables(routing_tables, nodes):
    """Print routing tables for specified routers."""
    for router in nodes:
        print(f"\nRouter {router}'s Routing Table:\n")
        print("Destination | Cost | Next Hop")
        print("-" * 12 + "|" + "-" * 6 + "|" + "-" * 9)
        for dest in routing_tables[router]:
            cost = routing_tables[router][dest]['cost']
            next_hop = routing_tables[router][dest]['next_hop']
            print(f"{dest:11} | {cost:4} | {next_hop}")

def plot_network(G, source, destination):
    """Plot the network with nodes, edges, and weights, highlighting source and destination."""
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G)  # Layout for node positions
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=500)
    # Highlight source and destination nodes
    nx.draw_networkx_nodes(G, pos, nodelist=[source], node_color='green', node_size=600)
    nx.draw_networkx_nodes(G, pos, nodelist=[destination], node_color='red', node_size=600)
    
    # Draw edges
    nx.draw_networkx_edges(G, pos)
    
    # Draw edge labels (weights)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    
    # Draw node labels
    nx.draw_networkx_labels(G, pos, font_size=12)
    
    plt.title("Network Topology\n(Green: Source, Red: Destination)")
    plt.savefig('network_plot.png')
    plt.close()

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="RIP Protocol Simulation with Network Plot")
    parser.add_argument('--router', type=str, help="Specify a single router to display its routing table (e.g., 'A')")
    args = parser.parse_args()

    # Create a sample network
    G = nx.Graph()
    edges = [
        ('A', 'B', 4),
        ('A', 'C', 2),
        ('B', 'C', 1),
        ('B', 'D', 5),
        ('C', 'D', 8),
        ('C', 'E', 10),
        ('D', 'E', 2)
    ]
    G.add_weighted_edges_from(edges)

    # Run RIP algorithm and plot the network
    source = 'A'
    destination = 'E'
    plot_network(G, source, destination)
    
    print("\n![Network Plot](network_plot.png)\n")
    
    path, final_tables = rip_algorithm(G, source, destination, selected_router=args.router)

    print(f"\nShortest path from {source} to {destination}: {path}")
    print("\nNetwork plot saved as 'network_plot.png'")

if __name__ == "__main__":
    main()