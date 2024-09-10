from flask import Flask, render_template, request, redirect, url_for
import json
from objects import CompactSurface
from classification import surface_classification_printing, classification_2, compute_homology_groups

app = Flask(__name__)

@app.route('/')
def input_page():
    return render_template('input.html')

@app.route('/output', methods=['POST'])
def output_page():
    if request.method == 'POST':
        # Get the surface data from the form input
        surface_data = request.form['surface_input']

        # Parse the JSON string into a Python dictionary
        surface_data = json.loads(surface_data)

        # Extract vertices, edges, and pairs from the surface data
        vertices = int(surface_data['vertices'])  # Ensure it's an integer
        edges = surface_data['edges']  # List of edge pairs
        pairs = surface_data['pairs']  # List of edge pairings

        # Convert edges and pairs into sets of tuples for CompactSurface
        EDGES = set()
        gluing = set()

        # Create a set of edges
        for edge in edges:
            u, v = edge[0], edge[1]
            EDGES.add((u, v))  # Add the edge as a tuple (u, v)

        # Create the gluing (pairing) set
        for pair in pairs:
            edge1 = pair[0]
            edge2 = pair[1]
            u, v = edge1[0], edge1[1]
            x, y = edge2[0], edge2[1]
            gluing.add(((u, v), (x, y)))  # Add the paired edges as a tuple of tuples

        # Create a CompactSurface object with the vertices, edges, and gluing data
        surface = CompactSurface(vertices, EDGES, gluing)

        # Classify the surface (e.g., find its genus, orientability, etc.)
        classified_surface = surface_classification_printing(surface)

        # classification_2 returns a tuple with orientability and genus info
        surface1 = classification_2(surface)

        # Compute the homology groups based on the classified surface
        homology = compute_homology_groups(surface1)

        # Determine the fundamental group based on the surface type and genus
        orientability, genus = surface1
        if orientability == 1:
            # Orientable surface fundamental group
            if genus == 0:
                fundamental_group = "{1}"  # Trivial group for the sphere
            else:
                fundamental_group = "⟨ a_1, b_1, ..., a_{g}, b_{g} | [a_1, b_1]...[a_{g}, b_{g}] = 1 ⟩"
        else:
            # Non-orientable surface fundamental group
            fundamental_group = "⟨ a_1, a_2, ..., a_{g} | a_1^2...a_{g}^2 = 1 ⟩"

        # Render the output page and pass the computed data to the template
        return render_template(
            'output.html',
            classified_surface=classified_surface,
            homology=homology,
            fundamental_group=fundamental_group,
            surface1=surface1  # Pass surface1 to the template
        )

if __name__ == '__main__':
    app.run(debug=True)
