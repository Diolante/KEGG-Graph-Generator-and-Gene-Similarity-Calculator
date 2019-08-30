# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 21:35:56 2018

@author: Douglas R. Violante
"""

import igraph as igr          
from re import search

data = []
placeholderA = 0
graph = igr.Graph(directed = True) # Creates a directed igraph instance

keg_filename = 'eco00001.keg'   # Name of the input file

# -------------------------------------------------------------------------------------------------------------

for line in open(keg_filename, 'r'):
    if(line.startswith('A') or line.startswith('B  ') or line.startswith('C    ') or line.startswith('D      ')):
        line = line.rstrip()    # Remove \n from every line
        data.append(line)

# -------------------------------------------------------------------------------------------------------------
 

graph.add_vertex(idg = 0, name = 'OBJECT', label = 'OBJECT', level = "root")


for n in range(1, len(data)):       # Starts in 1 because of root node, and needs to add an 'A' em the file
    
    
    if(data[n].startswith('A')):    # No Spaces
        placeholderA = n
        
        a_name_regex = search(r'[A]\d[0-9]{4,5}', data[n])
        a_label_regex = search(r'\s[A-Za-z].*', data[n])
        
        graph.add_vertex(idg = n,
                            name = a_name_regex.group(0),
                            label = a_label_regex.group(0), 
                            level = 'A', 
                            KO = '',
                            description = '')
        
        
        graph.add_edge(graph.vs[n]['idg'], graph.vs[0]['idg'])
        
# -------------------------------------------------------------------------------------------------------------
        
    if(data[n].startswith('B  ')):  # 2 Spaces
        placeholderB = n
        
        b_name_regex = search(r'[B]\s+\d[0-9]{4,5}', data[n])
        b_label_regex = search(r'\s[A-Za-z].*', data[n])
        
        graph.add_vertex(idg = n,
                             name = b_name_regex.group(0),
                             label = b_label_regex.group(0),
                             level = 'B',
                             KO = '',
                             description = '')
        
        graph.add_edge(graph.vs[n]['idg'], graph.vs[placeholderA]['idg'])
        
# -------------------------------------------------------------------------------------------------------------
            
    if(data[n].startswith('C    ')):    # 4 Spaces
        placeholderC = n   
        
        c_name_regex = search(r'[C]\s+\d[0-9]{4,5}', data[n])  # RegEX to find name identifier and letter
        c_label_regex = search(r'\s[A-Za-z].*', data[n])    # RegEX to find description of the process in C level
        
        graph.add_vertex(idg = n,
                             name = c_name_regex.group(0),
                             label = c_label_regex.group(0),
                             level = 'C',
                             KO = '',
                             description = '')
        
        graph.add_edge(graph.vs[n]['idg'], graph.vs[placeholderB]['idg'])
           
# -------------------------------------------------------------------------------------------------------------
                
    if(data[n].startswith('D      ')):    # 6 Spaces
       placeholderD = n
                      
       ko_regex = search(r'[K]\d{5}', data[n]) # RegEX to find KO identifier
       d_name_regex = search(r'b\d{4}\s[a-zA-Z]{3,5}(-\d)?', data[n]) # RegEX to find gene name and synonym

       graph.add_vertex(idg = n,
                            name = d_name_regex.group(0),
                            label = d_name_regex.group(0),
                            level = 'D',
                            KO = ko_regex.group(0),
                            description = ''.join(data[n].split(' ')[8:]))
               
       graph.add_edge(graph.vs[n]['idg'], graph.vs[placeholderC]['idg'])
       
# -------------------------------------------------------------------------------------------------------------

def searchGene(graph, gene): # Searches corresponding node with the given keyword, and print them
    
    genes = []
    
    for vertex in range(graph.vcount()):
        geneReturned = graph.vs[vertex]['name'] # Checks only the name attribute 
        
        if(gene == geneReturned):
            
            genes.append(graph.vs[vertex].index)
        
    return genes

# -------------------------------------------------------------------------------------------------------------        

def exportGraph(): # Export generate regulation list to a txt file
        
    str(graph.write(f='EColi_K-12_MG1655.graphml',format="graphml"))
    
# -------------------------------------------------------------------------------------------------------------

def similarity(graph, from_gene, to_gene): # Implements the similarity calculus as cited in the article
    
    found_from_genes = []
    found_to_genes = []
    
    shortests_paths_from = []
    shortests_paths_to = []
    
    from_list = []
    to_list = []
    
    intersection_between_paths = []
    distance_between_genes = 0
    

    found_from_genes = searchGene(graph, from_gene)         # Get all indexes of same names genes
    from_lenght = len(found_from_genes)
        
    found_to_genes = searchGene(graph, to_gene)            # Get all indexes of same names genes
    to_lenght = len(found_to_genes)
        
# ------------------------------------------------- BASE ALGORITHM ----------------------------------------------------
    
    if(to_lenght and from_lenght == 1):   # If there is only a single gene with no duplicates, in to and from
    
        shortests_paths_from = graph.get_all_shortest_paths(from_gene, 0, mode = 'out')
        shortests_paths_to = graph.get_all_shortest_paths(0, to_gene, mode = 'in')
        
                
        intersection_between_paths = [value for value in shortests_paths_to[0] if value in shortests_paths_from[0]] 
    
        intersection_between_paths = max(intersection_between_paths)        # By the nature of how the graph is constructed, the max is always the lowest common ancestor
    
        depth_lca = graph.shortest_paths(0,  intersection_between_paths, mode='in')[0][0]     # Calculates de depth of the lowest common ancestor
            
    
        halfDistanceGenes = graph.shortest_paths(from_gene, intersection_between_paths, mode = 'out')     # Returns a list inside a list, shortest_path returns a number, get_shortest_paths returns a list
        fullDistanceGenes = graph.shortest_paths(to_gene, intersection_between_paths, mode = 'out')[0][0] + halfDistanceGenes[0][0]    
        
        similarity = fullDistanceGenes / ((2.0 * depth_lca) + fullDistanceGenes)        # Implements the calculation cited in the GFD-Net article
    
        return 1 - similarity
# -------------------------------------------------------------------------------------------------------------
        
    else:
        
        for f in range(0, from_lenght):
            
            from_list.append(graph.get_all_shortest_paths(found_from_genes[f], 0, mode = 'out'))     # Tests and all paths from root to all found genes by searchGene()
        
        for t in range(0, to_lenght):
            
            to_list.append(graph.get_all_shortest_paths(found_to_genes[t], 0, mode = 'out'))  # Tests and all paths from root to all found genes by searchGene()
        
        
        shortests_paths_from = [e for sl in from_list for e in sl]  # Converts a 3-D list to a 2-D list
        shortests_paths_to   = [e for sl in to_list for e in sl]    # Converts a 3-D list to a 2-D list
    
        
        for path_to in range(len(shortests_paths_to)):
            for path_from in range(len(shortests_paths_from)):
                
                intersection_between_paths.append([value for value in shortests_paths_to[path_to] if value in shortests_paths_from[path_from]])     # Compute a intersection between the to and from nested lists
        

        common_path = max((x) for x in intersection_between_paths)  # Return the last largest list found with intersection
        
        depth_lca = graph.shortest_paths(0,  max(common_path), mode='in')[0][0]     # Calculates de depth of the lowest common ancestor
        
        # Structure based in the organism graph topology, D "Gene" levels, are always distance 5 from root
        
        if(len(common_path) == 4):
            distance_between_genes = 2.0
            
        elif(len(common_path) == 3):
            distance_between_genes = 4.0
            
        elif(len(common_path) == 2):
            distance_between_genes = 6.0
            
        elif(len(common_path) == 1):
            distance_between_genes = 8.0
            
            
        similarity = distance_between_genes /  ((2.0 * depth_lca)  + distance_between_genes)      # Implements the calculation cited in the GFD-Net article
                    
        return 1 - similarity
    
def first_hundred_genes_check():
    
    for i in range(100):
        print(similarity(graph, 'b4025 pgi', graph.vs[i]['name']))
        
        
