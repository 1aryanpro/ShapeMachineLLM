# LLM for Shape Grammers

This is a project for generating a training dataset for the purpose of training
an LLM to answer questions about shape grammars as well as generate SVGs that
visualize the rules it's talking about. Our dataset can train a model to
understand rotation, conversion, lookup and deletion rules.

## File Structure

### Main Files
- **`main.py`**: 
  - Contains the core `Shape` class and methods for shape manipulation.
  - Includes utilities for generating SVGs and prompts.
  - Defines the main workflow for generating transformations and exporting prompts.

- **`prompts.py`**:
  - Contains functions for generating textual prompts for shape transformations.

- **`tdg.py`**:
  - Generates a text file that shows what the output of the model should actually look like.
  - This model can 

### Supporting Files
- **`shapes.json`**:
  - A JSON file defining premade shapes with their vertices and lines.

- **`prompts.tsv`**:
  - A TSV file where generated prompts and their corresponding SVGs are stored.

- **`prompts.txt`**:
  - A formatted text file containing the prompts and SVGs for easy readability.

## Usage

### Prerequisites
- Python 3.x

### Running the Project
1. **Generate Prompts**:
   - Run the main.py script to generate prompts for shape transformations:
     ```bash
     python main.py
     ```

2. **View SVGs**:
   - Generated SVGs are embedded in the prompts and can be viewed in any SVG-compatible viewer.

3. **Export Prompts**:
    - Use tdg.py to convert the TSV file into a formatted text file:
     ```bash
     python tdg.py
     ```
    - This file can be inputted directly into any LLM to see if it can output
    some reasonable answers. You can add the file as an attachment or
    copy-pasted into after running the following script. Note: make sure you run
    `main.py` first so that the 
    ```bash
    python tdg.py && cat prompts.txt | pbcopy
    ```

## Key Functions

### main.py
- **`Shape` Class**:
  - `add_random_line()`: Adds a random line between vertices.
  - `delete_random_line()`: Deletes a random line.
  - `rotate(angle)`: Rotates the shape by a specified angle.
  - `duplicate(direction)`: Duplicates the shape in a specified direction.

- **Prompt Generators**:
  - `generateConversions()`: Generates prompts for shape conversions.
  - `generateRotations()`: Generates prompts for shape rotations.
  - `generateDuplications()`: Generates prompts for shape duplications.

- **SVG Utilities**:
  - `make_svg(shape)`: Creates an SVG representation of a shape.

### prompts.py
- **Prompt Functions**:
  - `duplicationPrompt(shape, dir)`: Generates duplication prompts.
  - `rotationPrompt(shape, angle)`: Generates rotation prompts.
  - `conversionPrompt(shape1, shape2)`: Generates conversion prompts.

### tdg.py
- **`svgTemplate(left, right)`**:
  - Creates an SVG template for side-by-side visualization of transformations.

## Example Output

### Prompt Example
```
Input:
Create a ShapeMachine rule that duplicates all triangles down.

Output:
Since we want to duplicate something, that requires us to have one copy of the object on the left side of the rule, and two copies of the object on the right side of the rule. Here we want to duplicate down so the new copy should be below the original one. The object in question here is a triangle. So the left-hand side will contain one triangle and the right-hand side will contain two triangles with the new one below the original.
```

### SVG Example
```xml
<svg xmlns="http://www.w3.org/2000/svg" width="500" height="500" viewBox="0 0 500 500">
    <svg width="200" height="500" xmlns="http://www.w3.org/2000/svg">
        <circle cx="100" cy="480" r="3" fill="red"/>
        <line x1="50" y1="200" x2="50" y2="300" stroke="#000" stroke-width="1"/><line x1="50" y1="300" x2="150" y2="300" stroke="#000" stroke-width="1"/><line x1="150" y1="300" x2="50" y2="200" stroke="#000" stroke-width="1"/></svg>
 <line x1="250" y1="100" x2="250" y2="405" stroke="#000" stroke-width="1"/>
 <g transform="translate(300, 0)">
 <svg width="duplicate" height="down" xmlns="http://www.w3.org/2000/svg"><circle cx="100" cy="480" r="3" fill="red"/><line x1="50" y1="200" x2="50" y2="300" stroke="#000" stroke-width="1"/><line x1="50" y1="300" x2="150" y2="300" stroke="#000" stroke-width="1"/><line x1="150" y1="300" x2="50" y2="200" stroke="#000" stroke-width="1"/></svg>
 </g>
</svg>
```

