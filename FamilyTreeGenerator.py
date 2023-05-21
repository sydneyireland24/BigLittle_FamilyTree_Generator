# @Author Sydney Gibbs - TB 569
# Last Updated: 5/20/23
# Hello! If you're reading this, you're probably Tau Beta's newest Historian. I was in your shoes once too, and took
# on the task of trying to get accurate and consistent records of the Tau Beta Family Trees. I wanted to A. get
# the right data for the trees, and B. make it easy to update the trees for future generations (as I figured drawing
# a new family tree each year would be tedious and annoying). I landed on writing a program that would make family
# tree images for you, provided you feed in big/little data. The format of these big/little files are as follows:
#
# Big           |   Little
# ---------------------------
# Joe Mama      |  John Doe
# Joe Mama      |  Jane Doe
# Jane Doe      |  Alan Turing
# etc.
#
# NOTE: ALL ELEMENTS MUST BE DISTINCT NAMES OR ELSE YOU MIGHT GET SOME WEIRD RESULTS
# these files can be found in the tau beta officer resources. Or if you're reading this off my GitHub, there's a
# sample file in this repo.
#
# feel free to improve upon this code as you see fit, as I imagine eventually the libraries I use will be updated
# and may not function like they used to.
#
# If for some reason you find this code to be difficult/it wont work, don't hesitate to reach out to me
# @sydneyireland24@gmail.com

# imports needed
import pandas as pd
import graphviz
import os

# file names (hint: you probably need to change these on your end)
data_file = 'Family_Lines_Orphan.csv' # file you're getting your data from
family_tree_file = 'family_tree_orphan' # name of the final image of the family tree

# actual function for building the tree
# ARGUMENTS
# family_tree - dictionary that holds your family tree data
# big - current "big" you are working with
# dot - the GraphViz dot object
# edges - list of all known edges in the family tree
def build_family_tree(family_tree, big, dot, edges):
    if big in family_tree:  # holds true until we get to the end of a particular family line
        littles = family_tree[big]  # get list of littles from the big
        with dot.subgraph() as subgraph:  # creating a subgraph of all the littles associated with the big
            for little in littles:
                subgraph.node(little)  # add current little to subgraph
                edge = (big, little)  # create edge between big and little
                if edge not in edges:  # used to avoid duplicate edges
                    edges.add(edge)  # adds edge to list of known edges
                    subgraph.edge(*edge)  # adds visualization of edge to subgraph
                    build_family_tree(family_tree, little, dot, edges)  # recursive call until we get to bottom of tree


os.environ["PATH"] += os.pathsep + 'C:\Program Files\Graphviz\\bin'
# replace the above with "/usr/local/graphviz-X.XX/bin" if you're on a MAC OS (where X.XX is the version)
# if you're on Linux, you're probably 10x more competent than I am so figure out your own program path nerd

ancestry = pd.read_csv(data_file) # read the data from the file and store it in a DataFrame

family_tree = {} # this final dictionary will store the associations between bigs/littles
for index, row in ancestry.iterrows():  # for each row in the DataFrame
    big = row['Big']  # this gets you the big (left hand side)
    little = row['Little']  # this gets you the little (right hand side)
    if big in family_tree:  # if the big is already in the dictionary
        family_tree[big].append(little)  # add their little to the already existing list of littles
    elif big not in family_tree:  # if the big isn't already in the dictionary
        family_tree[big] = [little]  # add big to the dictionary with a littles list of the current little

# print(family_tree) # debugging code

# Create a Graphviz dot object (actual visual family tree: not clickbait)
dot = graphviz.Digraph(
    comment='Family Tree',
    graph_attr={'rankdir': 'TB'}
)

# Build the family tree
edges = set()  # Set to keep track of edges (this prevents an issue of having multiples edges between nodes)
for big, littles in family_tree.items():  # big is the big (duh), and littles is list of littles associated with big
    dot.node(big)  # create a node of the current big
    build_family_tree(family_tree, big, dot, edges)  # call actual tree building function

# Render and save image
dot.format = 'png'  # Set the output format to png (or jpeg if you're not like other girls)
dot.render(family_tree_file)  # Saves final product to whatever file name you choose
