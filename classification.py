from objects import CompactSurface

# this program asks the user for a compact surface and classifies it according to the
# classification of compact surfaces theorem

def main():
    surface = CompactSurface.get()
    print(surface_classification_printing(surface))



# Algorithm for the classification of surfaces:
# In the following functions we will encode each of the steps in the classification of surfaces algorithm

# Step 1: remove spheres
def remove_adjacent_edges(surface):
    if not isinstance(surface, CompactSurface):
        raise TypeError("Input not a compact surface")

    for i in range(surface.vertices):
        # Calculate indices for the adjacent edges
        edge1 = (i, (i - 1) % surface.vertices)
        edge2 = (i, (i + 1) % surface.vertices)
        reverse_edge1 = ((i - 1) % surface.vertices, i)
        reverse_edge2 = ((i + 1) % surface.vertices, i)

        # Check if either the pair of edges or their reverses are in the gluing
        if (((edge1, edge2) in surface.gluing) or ((reverse_edge1, reverse_edge2) in surface.gluing)
             or ((edge2, edge1) in surface.gluing) or ((reverse_edge2, reverse_edge1) in surface.gluing)):
            # Create a new set of vertices
            new_vertices = surface.vertices - 2

            # Create a new set of edges excluding the removed edges
            new_edges = set()
            for edge in surface.edges:
                if edge in [edge1, edge2, reverse_edge1, reverse_edge2]:
                    continue  # Skip the edges to be removed
                new_u, new_v = edge
                if i == 0:
                    if new_u > i:
                        new_u -= 1
                    if new_v > i:
                        new_v -= 1
                else:
                    if new_u > i:
                        new_u -= 2
                    if new_v > i:
                        new_v -= 2
                new_edges.add((new_u % new_vertices, new_v % new_vertices))
            # Create a new set of gluing pairs, excluding the pairs involving the removed edges
            new_gluing = set()

            for pair in surface.gluing:
                if edge1 in pair or edge2 in pair or reverse_edge1 in pair or reverse_edge2 in pair:
                    continue  # Skip the pairs involving the removed edges
                new_pair = []
                for edge in pair:
                    new_u, new_v = edge
                    if i == 0:
                        if new_u > i:
                            new_u -= 1
                        if new_v > i:
                            new_v -= 1
                    else:
                        if new_u > i:
                            new_u -= 2
                        if new_v > i:
                            new_v -= 2
                    new_pair.append((new_u % new_vertices, new_v % new_vertices))
                new_gluing.add(tuple(new_pair))
            # Return the new CompactSurface object
            return CompactSurface(new_vertices, new_edges, new_gluing)

    # If no adjacent edges satisfying the condition are found, return the original surface
    return surface


# here we create some auxiliary functions,
# relevant to the algorithm due to how we decided to represent compact surfaces in python

def max_tuple(tuple1, tuple2):
    # degenerate case first edge of the form (n-1 mod n, 0) is the largest
    # it can also be characterised for being the unique edge with a difference greater than 1 between its vertices
    if (tuple1[1] - tuple1[0] > 1) or (tuple1[0] - tuple1[1] > 1):
        return tuple1
    elif (tuple2[1] - tuple2[0] > 1) or (tuple2[0] - tuple2[1] > 1):
        return tuple2
    # Normal case
    # Find the maximum value in each tuple
    max1 = max(tuple1)
    max2 = max(tuple2)

    # Return the tuple with the greater maximum value
    if max1 > max2:
        return tuple1
    else:
        return tuple2
def min_tuple(tuple1, tuple2):
    # degenerate case first edge of the form (n-1 mod n, 0) is the largest
    # it can also be characterised for being the unique edge with a difference greater than 1 between its vertices
    if (tuple1[1] - tuple1[0] > 1) or (tuple1[0] - tuple1[1] > 1):
        return tuple2
    elif (tuple2[1] - tuple2[0] > 1) or (tuple2[0] - tuple2[1] > 1):
        return tuple1

    # Normal case

    # Find the minimum value in each tuple
    max1 = max(tuple1)
    max2 = max(tuple2)

    # Return the tuple with the smallest maximum value

    if max1 < max2:
        return tuple1
    else:
        return tuple2
def reverse_edges(edges_list):

        # Reverse the direction of each edge by swapping the elements in each tuple
        reversed_list = [(v, u) for u, v in edges_list]
        return reversed_list
def reverse_list(input_list):

    return input_list[::-1]

# end of auxiliary functions

# Step 2: removoe projective planes

def remove_projective_plane(surface):
    if not isinstance(surface, CompactSurface):
        raise TypeError("Input not a compact surface")

    # search for projective plane edges
    rplane = None
    for pair in surface.gluing:
        edge1, edge2 = pair
        x, y = edge1
        u, v = edge2
        # check for the desired orientation
        # degenerate case
        if (x + 1) % surface.vertices == 0 and y == 0 and (u < v):
            rplane = pair
            break
        elif (y + 1) % surface.vertices == 0 and x == 0 and (u > v):
            rplane = pair
            break
        elif (u + 1) % surface.vertices == 0 and v == 0 and (x < y):
            rplane = pair
            break
        elif (v + 1) % surface.vertices == 0 and u == 0 and (x > y):
            rplane = pair
            break
        # non degenerate case:
        elif (not((x + 1) % surface.vertices == 0 and y == 0) and not((y + 1) % surface.vertices == 0 and x == 0)
              and not((u + 1) % surface.vertices == 0 and v == 0) and not((v + 1) % surface.vertices == 0 and u == 0)
              and ((x > y and u > v) or (x < y and u < v))):
            rplane = pair
            break

    if rplane is None:
        # No projective plane found
        return surface

    # create new set of edges
    list1, list2 = surface.split_edges(min_tuple(rplane[0], rplane[1]), max_tuple(rplane[0], rplane[1]))
    m = len(list1)
    n = len(list2)
    list3 = reverse_list(reverse_edges(list2))
    new_vertices = m + n

    new_edges = set()
    list5 = []
    for i in range(n):
        u, v = list3[i]
        # degenerate case
        if (v + 1) % surface.vertices == 0 and u == 0:
            new_edges.add(((i+1) % new_vertices, i))
            list5.append(((i+1) % new_vertices, i))
        elif (u + 1) % surface.vertices == 0 and v == 0:
            new_edges.add((i, (i+1) % new_vertices))
            list5.append((i, (i+1) % new_vertices))
        # non-degenerate case
        else:
            if u < v:
                new_edges.add((i, (i+1) % new_vertices))
                list5.append((i, (i+1) % new_vertices))
            else:
                new_edges.add(((i+1) % new_vertices, i))
                list5.append(((i+1) % new_vertices, i))
    for i in range(m):
        u, v = list1[i]
        if (v + 1) % surface.vertices == 0 and u == 0:
            new_edges.add(((i+1+n) % new_vertices, i))
            list5.append(((i+1+n) % new_vertices, i))
        elif (u + 1) % surface.vertices == 0 and v == 0:
            new_edges.add((i, (i+1+n) % new_vertices))
            list5.append((i, (i+1+n) % new_vertices))
        else:
            if u < v:
                new_edges.add((i+n, (i+1+n) % new_vertices))
                list5.append((i+n, (i+1+n) % new_vertices))
            else:
                new_edges.add(((i+1+n) % new_vertices, i+n))
                list5.append(((i+1+n) % new_vertices, i+n))

    # create new gluing set

    list4 = reverse_list(list2) + list1 #list containing edges in the original orientation
    new_gluing = set()
    # we iterate over all pairs which are not the projective plane
    # Create a new gluing set excluding the projective plane pair
    remaining_gluing = surface.gluing.copy()  # Make a copy of the gluing set
    remaining_gluing.remove(rplane)           # Remove the projective plane pair

# Now, iterate over the remaining pairs in the gluing set
    for pair in remaining_gluing:
        edge1, edge2 = pair
        index1 = list4.index(edge1)
        index2 = list4.index(edge2)
        new_gluing.add((list5[index1], list5[index2]))



    return CompactSurface(new_vertices, new_edges, new_gluing)


# Step 3: remove torus

# again, we split this step in a bunch of functions that are integrated
# in the final one: remove_torus()


def identify_torus(surface):
    if not isinstance(surface, CompactSurface):
        raise TypeError("Input not a compact surface")
    if surface.vertices < 4:
        raise ValueError("Too few vertices to contain a torus")

    def find_torus_pair(pair):
        edge1, edge2 = pair
        x, y = edge1
        u, v = edge2
        # check for the desired orientation
        # degenerate case
        if (x + 1) % surface.vertices == 0 and y == 0 and (u > v):
            return pair

        elif (y + 1) % surface.vertices == 0 and x == 0 and (u < v):
            return pair

        elif (u + 1) % surface.vertices == 0 and v == 0 and (x > y):
            return pair

        elif (v + 1) % surface.vertices == 0 and u == 0 and (x < y):
            return pair

        # non degenerate case:
        elif (not((x + 1) % surface.vertices == 0 and y == 0) and not((y + 1) % surface.vertices == 0 and x == 0)
              and not((u + 1) % surface.vertices == 0 and v == 0) and not((v + 1) % surface.vertices == 0 and u == 0)
              and ((x > y and u < v) or (x < y and u > v))):
            return pair

        else:
            return None


    # search for edges forming a torus
    torus1 = None
    torus2 = None
    sorted_edges = surface.edges_sorted_by_max()
    for pair in surface.gluing:
        torus1 = find_torus_pair(pair)

        if torus1 is None:
            continue
        # we move into finding the second pair
        else:
            remaining_gluing = surface.gluing.copy()  # Make a copy of the gluing set
            remaining_gluing.remove(torus1)

            for pair1 in remaining_gluing:
                torus2 = find_torus_pair(pair1)

                if torus2 is None:
                    continue
                else:
                    # Extract edges from torus1 and torus2
                    min_torus1, max_torus1 = min_tuple(torus1[0], torus1[1]), max_tuple(torus1[0], torus1[1])
                    min_torus2, max_torus2 = min_tuple(torus2[0], torus2[1]), max_tuple(torus2[0], torus2[1])

                    # Check the ordering criteria
                    min_torus1_pos = sorted_edges.index(min_torus1)
                    min_torus2_pos = sorted_edges.index(min_torus2)
                    max_torus1_pos = sorted_edges.index(max_torus1)
                    max_torus2_pos = sorted_edges.index(max_torus2)

                    if (min_torus1_pos < min_torus2_pos < max_torus1_pos < max_torus2_pos):
                        return torus1, torus2
                    elif (min_torus2_pos < min_torus1_pos < max_torus2_pos < max_torus1_pos):
                        return torus2, torus1

    return None



def remove_torus(surface):
    torus_pair = identify_torus(surface)
    if torus_pair is None:
        return surface
    else:
        torus1, torus2 = torus_pair

    edge1, edge3 = torus1
    edge2, edge4 = torus2

    list1, list2, list3, list4 = surface.split_edges_4(edge1, edge2, edge3, edge4)


    list5 = list3 + list4 + list2 + list1

    new_vertices = len(list5)

    new_edges = set()
    list6 = []

    for i in range(new_vertices):
        u, v = list5[i]
        # degenerate case
        if (v + 1) % surface.vertices == 0 and u == 0:
            new_edges.add(((i+1) % new_vertices, i))
            list6.append(((i+1) % new_vertices, i))
        elif (u + 1) % surface.vertices == 0 and v == 0:
            new_edges.add((i, (i+1) % new_vertices))
            list6.append((i, (i+1) % new_vertices))
        # non-degenerate case
        else:
            if u < v:
                new_edges.add((i, (i+1) % new_vertices))
                list6.append((i, (i+1) % new_vertices))
            else:
                new_edges.add(((i+1) % new_vertices, i))
                list6.append(((i+1) % new_vertices, i))

    new_gluing = set()
    # we iterate over all pairs which are not the projective plane
    # Create a new gluing set excluding the projective plane pair
    remaining_gluing = surface.gluing.copy()  # Make a copy of the gluing set
    remaining_gluing.remove(torus1)
    remaining_gluing.remove(torus2)         # Remove the projective plane pair

    # Now, iterate over the remaining pairs in the gluing set
    for pair in remaining_gluing:
        edge1, edge2 = pair
        index1 = list5.index(edge1)
        index2 = list5.index(edge2)
        new_gluing.add((list6[index1], list6[index2]))

    if new_vertices == 0:
        return None
    else:
        return CompactSurface(new_vertices, new_edges, new_gluing)


# the previous functions are the core of the algorithm: the idea of the algorithm
# is to execute them in order at every iteration, and in every iteration, we execute
# only one of the functions. That is, if there is a spher to remove, we remove it. If not,
# we move on to try to remove a projective plane, if we succed then we go back to try to
# remove a sphere. If not, we move into trying to remove a torus. And so on, until we run out of vertices


def surface_classification(surface):
    if not isinstance(surface, CompactSurface):
        raise TypeError("Input not a compact surface")

    projective_planes = 0
    tori = 0
    sphere = 0

    if surface.vertices == 2:
        if (surface.edges == {(0,1)} and surface.gluing == {((0, 1), (0, 1))}) or (surface.edges == {(1, 0)} and surface.gluing == {((1, 0), (1, 0))}):
            sphere += 1
            return projective_planes, tori, sphere
        else:
            projective_planes += 1
            return projective_planes, tori, sphere

    while surface.vertices > 2:
        # Attempt to remove spheres
        new_surface = remove_adjacent_edges(surface)
        if new_surface != surface:
            sphere += 1
            surface = new_surface
            continue
        # Attempt to remove a projective plane
        new_surface = remove_projective_plane(surface)
        if new_surface != surface:
            projective_planes += 1
            surface = new_surface
            continue

        # Attempt to remove a torus
        new_surface = remove_torus(surface)
        if new_surface != surface:
            tori += 1
            if new_surface == None:
                break
            else:
                surface = new_surface
                continue

    if surface.vertices == 2:
        if (surface.edges == {(0,1)} and surface.gluing == {(0, 1), (0, 1)}) or (surface.edges == {(1, 0)} and surface.gluing == {((1, 0), (1, 0))}):
            sphere += 1
            return projective_planes, tori, sphere
        else:
            projective_planes += 1
            return projective_planes, tori, sphere

    return projective_planes, tori, sphere

# this function returns a tuple where the first entry indicates wether the suurface is orientable
# or not, and the second entry indicates the genus
def classification_2(surface):
    projective_planes, tori, sphere = surface_classification(surface)

    # Convert each torus and projective plane pair to 3 projective planes using Dyck's theorem
    if tori > 0 and projective_planes > 0:
        projective_planes += 2 * tori
        tori = 0  # All tori are converted into projective planes

    if projective_planes != 0:
        # the 0 represents non orientable
        return (0, projective_planes)

    else:
        # the 1 represents orientable
        return (1, tori)

def surface_classification_printing(surface):
    projective_planes, tori, sphere = surface_classification(surface)

    # Convert each torus and projective plane pair to 3 projective planes using Dyck's theorem
    if tori > 0 and projective_planes > 0:
        projective_planes += 2 * tori
        tori = 0  # All tori are converted into projective planes

    # Handle the case of a sphere
    if projective_planes == 0 and tori == 0 and sphere == 1:
        return "This is a sphere"

    # Handle the case of only projective planes
    elif tori == 0:
        if projective_planes == 1:
            return "This is a projective plane"
        elif projective_planes == 2:
            return "This is a Klein Bottle"
        else:
            return f"This is a connected sum of {projective_planes} projective planes"

    # Handle the case of only tori (no projective planes)
    elif projective_planes == 0:
        if tori == 1:
            return "This is a torus"
        else:
            return f"This is a connected sum of {tori} tori"



def compute_homology_groups(surface):
    a, b = surface[0], surface[1]
    if a == 1:
        return (1, 1, 2*b, 1)
    else:
        return (0, 1, b, 0)


if __name__ == "__main__":
    main()




#sphere = CompactSurface(
#vertices=2,
#edges={(0, 1)},
#gluing={((0, 1), (0, 1))}
#)

#projective_plane = CompactSurface(
    #vertices=2,
    #edges={(0, 1), (1, 0)},
    #gluing={((0, 1), (1, 0))}
#)

#torus = CompactSurface(
    #vertices=4,
    #edges={(0, 1), (2, 1), (3, 2), (3, 0)},
    #gluing={((0, 1), (3, 2)), ((2, 1), (3, 0))}
#)

#klein_bottle = CompactSurface(
    #vertices=4,
    #edges={(0, 1), (1, 2), (2, 3), (0, 3)},
    #gluing={((0, 1), (2, 3)), ((1, 2), (0, 3))}
#)



















