import networkx as nx
import matplotlib.pyplot as plt
import random

#Generate random graph
def generate_random_graph(num_nodes=6, num_edges=11):
    if num_nodes < 6:
        raise ValueError("The graph must have at least 6 nodes")
    max_edges = num_nodes * (num_nodes - 1) // 2

    if num_edges < num_nodes - 1 or num_edges > max_edges:
        raise ValueError(
            "A connected simple graph needs between num_nodes - 1 and num_nodes*(num_nodes-1)//2 edges."
        )

    G = nx.Graph()
    G.add_nodes_from(range(1, num_nodes + 1))

    #create a random spanning tree
    nodes = list(G.nodes())
    random.shuffle(nodes)

    for i in range(1, num_nodes):
        u = nodes[i]
        v = random.choice(nodes[:i])
        weight = random.randint(1, 20)
        G.add_edge(u, v, weight=weight)
    #add random extra edges
    while G.number_of_edges() < num_edges:
        u, v = random.sample(list(G.nodes()), 2)
        if not G.has_edge(u, v):
            G.add_edge(u, v, weight=random.randint(1, 20))

    return G


#display each step of the MST

def show_mst_step(Graph, mst, pos, candidate, accepted, step):
    plt.figure(figsize=(8, 6))
     #daw original graph in light grey
    nx.draw(Graph, pos, with_labels=True, node_color="lightblue", node_size=900,font_weight="bold", edge_color="lightgray", width=2)

    #use red to show accepted edges
    nx.draw_networkx_edges(mst,pos,edgelist=list(mst.edges()),edge_color="red",width=3)

    #use orange  and dashed lines to show rejected edges
    if not accepted:
        nx.draw_networkx_edges(Graph,pos,edgelist=[candidate],edge_color="orange",width=3,style="dashed")
    #display edge weights
    nx.draw_networkx_edge_labels(Graph,pos,edge_labels=nx.get_edge_attributes(Graph, "weight"))
    #display step by step information
    if not accepted:
        decision = "Accepted"
    else:
        decision = "Rejected, Cycle created"
    plt.title(f"MST Step {step}: {decision}")
    plt.axis("off")
    # plt.tight_layout() 

    # Pause to allow the user to see each step
    plt.show(block=False)
    plt.pause(1.5)
    plt.close()
    


#Use Kruskals algorithm to create MST

def MyMinimumSpanningTree(Graph, pos):
    mst = nx.Graph()
    mst.add_nodes_from(Graph.nodes(data=True))
    # Sort edges from smallest to largest weight
    edges = sorted( Graph.edges(data=True),key=lambda edge: edge[2]["weight"])

    print("\n--- Kruskal's Algorithm ---")

    step = 0

    for u, v, data in edges:

        weight = data["weight"]
        # temporarily add the edge
        mst.add_edge(u, v, **data)
        # check whether adding the edge creates a cycle
        if nx.is_forest(mst):
            accepted = True
            print(f"ACCEPT: {u} -- {v}, weight = {weight}")
        else:
            accepted = False
            # Remove edge if it creates a cycle
            mst.remove_edge(u, v)
            print(f"REJECT: {u} -- {v}, weight = {weight} (cycle created)")

        step += 1

        # Display the graph after every decision
        show_mst_step(Graph,mst,pos,(u, v),accepted,step)

        # Stop when V - 1 edges have been accepted
        if mst.number_of_edges() == Graph.number_of_nodes() - 1:
            break

    # Check that the final MST is a valid tree
    if not nx.is_tree(mst):
        raise ValueError("Input graph must be connected.")

    # Calculate total MST weight
    total_weight = sum(
        data["weight"]
        for _, _, data in mst.edges(data=True)
    )

    print("\nMST edges:")

    for u, v, data in mst.edges(data=True):
        print(f"{u} -- {v}: {data['weight']}")

    print("\nTotal MST weight:", total_weight)

    return mst





#display original graph and final MST
def display_graph(G, pos, title, edge_color="black"):
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=900,font_weight="bold", edge_color=edge_color, width=2)

    nx.draw_networkx_edge_labels(G,pos, edge_labels=nx.get_edge_attributes(G, "weight"))
    plt.title(title)
    plt.axis("off")
    # plt.tight_layout() commenting out as it seems to create an incorrect mst
    plt.show()




def main():
    #Generate random graph
    G = generate_random_graph(num_nodes=6, num_edges=11)
    print("Original Graph")
    print("Number of nodes:", G.number_of_nodes())
    print("Number of edges:", G.number_of_edges())
    print("Connected:", nx.is_connected(G))

    #use same node positions for every visualisation
    pos = nx.spring_layout(G, seed=42)

    #display original graph
    display_graph(G,pos,"Original Random Weighted Graph")

    #calculate MST and display every step
    MST = MyMinimumSpanningTree(G, pos)

    #display final results
    print("\nMST node count:", MST.number_of_nodes())
    print("MST edge count:", MST.number_of_edges())
    print("MST is a tree:", nx.is_tree(MST))

       # Display final MST
    display_graph(MST,pos,"Final Minimum Spanning Tree (Kruskal)",edge_color="red")






if __name__ == "__main__":
    main()