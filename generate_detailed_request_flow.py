#!/usr/bin/env python3
import os
import subprocess

def generate_diagram():
    """Generate the detailed request flow diagram from the DOT file."""
    dot_file = "diagrams/detailed_request_flow.dot"
    output_file = "diagrams/detailed_request_flow.png"
    
    # Ensure the diagrams directory exists
    os.makedirs("diagrams", exist_ok=True)
    
    # Generate PNG from DOT file using Graphviz
    try:
        subprocess.run(["dot", "-Tpng", dot_file, "-o", output_file], check=True)
        print(f"Successfully generated {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error generating diagram: {e}")
    except FileNotFoundError:
        print("Error: Graphviz (dot) is not installed. Please install it to generate diagrams.")
        
if __name__ == "__main__":
    generate_diagram() 