import random
import json
import math

from typing import NamedTuple, List, Tuple

from prompts import conversionPrompt, duplicationPrompt, rotationPrompt

# Lookups, Conversions (Shape1 -> Shape), Deletions, Rotations, Duplications (Horizontal & Vertical)
# n, n(n-1), n, 3n, 2n
# n^2 + 4n = n(n+6)
# n=7


class Shape:
    @classmethod
    def premade(cls, id: str) -> 'Shape':
        with open(f"shapes.json") as f:
            shapes = json.load(f)
        vertices = shapes[id]["vertices"]
        lines = shapes[id]["lines"]
        return cls(vertices, lines)

    @classmethod
    def premade_random(cls) -> 'Shape':
        with open(f"shapes.json") as f:
            shapes = json.load(f)
        id = random.choice(list(shapes.keys()))
        print(f"Random shape ID: {id}")
        return cls.premade(id)

    @staticmethod
    def midpoint(p1: Tuple[float, float], p2: Tuple[float, float]) -> Tuple[float, float]:
        # Calculate the midpoint between two points
        return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)

    @staticmethod
    def center(ps: List[Tuple[float, float]]) -> Tuple[float, float]:
        # Calculate the center of a list of points
        x_sum = sum(p[0] for p in ps)
        y_sum = sum(p[1] for p in ps)
        return (x_sum / len(ps), y_sum / len(ps))

    def __init__(self, vertices: List[Tuple[float, float]], lines: List[Tuple[int, int]]):
        self.vertices = vertices
        self.lines = lines  # list of pairs of vertex indices

    def delete_line(self, line: Tuple[int, int]):
        # remove the line from the list of lines
        self.lines.remove(line)

    def delete_random_line(self):

        # remove a random line from the list of lines
        if self.lines:
            line = random.choice(self.lines)
            self.delete_line(line)

    def add_line(self, line: Tuple[int, int]):
        # add a line to the list of lines
        if line not in self.lines and Tuple(line[1], line[0]) not in self.lines:
            self.lines.append(line)
            return True
        else:
            print(f"Line {line} already exists in the shape.")
            return False

    def add_random_line(self):
        # Check if there are already too many lines
        v = len(self.vertices)
        if len(self.lines) >= v * (v - 1) / 2:
            print("Cannot add more lines, maximum number of lines reached.")
            return

        # Add a random line between two random vertices
        while True:
            v1 = random.randint(0, len(self.vertices) - 1)
            v2 = random.randint(0, len(self.vertices) - 1)
            if v1 != v2:
                line = (v1, v2)
                if self.add_line(line):
                    break
            else:
                # print(f"Skipping line {line} as it connects the same vertex.")
                continue

    def rotate(self, angle: float):
        # rotate the shape by the given angle (in degrees)
        angle_rad = math.radians(angle)
        cos_angle = math.cos(angle_rad)
        sin_angle = math.sin(angle_rad)

        for i, (x, y) in enumerate(self.vertices):
            x_new = x * cos_angle - y * sin_angle
            y_new = x * sin_angle + y * cos_angle
            self.vertices[i] = (x_new, y_new)

    def rotate_random(self):
        # rotate the shape by set interval of angles
        increment = 15
        angle = random.choice(range(0, 360, increment))
        self.rotate(angle)

    def duplicate(self, direction: str = "right"):
        # Duplicate the shape by mirroring it across the x-axis or y-axis
        if direction == "right":
            # Shift the shape to the left first
            left_most = min(self.vertices, key=lambda p: p[0])[0]
            right_most = max(self.vertices, key=lambda p: p[0])[0]
            width = right_most - left_most
            self.vertices = [(x - width / 2, y) for x, y in self.vertices]

            new_vertices = [(x + (width), y) for x, y in self.vertices]
            new_lines = [(v1 + len(self.vertices), v2 + len(self.vertices)) for v1, v2 in self.lines]
        elif direction == "down":
            # Shift the shape to the top first
            top_most = max(self.vertices, key=lambda p: p[1])[1]
            bottom_most = min(self.vertices, key=lambda p: p[1])[1]
            height = top_most - bottom_most
            self.vertices = [(x, y - height / 2) for x, y in self.vertices]

            new_vertices = [(x, y + (height)) for x, y in self.vertices]
            new_lines = [(v1 + len(self.vertices), v2 + len(self.vertices)) for v1, v2 in self.lines]
        self.vertices.extend(new_vertices)
        self.lines.extend(new_lines)

    def __str__(self):
        # svg
        lines = []
        for line in self.lines:
            x1, y1 = self.vertices[line[0]]
            x2, y2 = self.vertices[line[1]]
            lines.append(
                f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#000" stroke-width="1"/>')
        return "".join(lines)


def pick_shape(shape: Shape = None, change=None, value=None) -> Shape:
    if shape is None:
        shape = Shape.premade_random()
    match change:
        case "delete":
            shape.delete_random_line() if value is None else shape.delete_line(value)
        case "rotate":
            shape.rotate_random() if value is None else shape.rotate(value)
        case "duplicate":
            shape.duplicate(value) if value is not None else shape.duplicate("right")
        case _:
            pass
    return shape


def make_svg(shape: Shape,
             canvas_w: float = 200,
             canvas_h: float = 500,
             ref_marker: str = '<circle cx="100" cy="480" r="3" fill="red"/>'
             ) -> str:
    # Create the SVG header
    svg_header = f'<svg width="{canvas_w}" height="{canvas_h}" xmlns="http://www.w3.org/2000/svg">'
    # Add the reference marker
    svg_header += ref_marker
    # Add the shape lines
    svg_header += str(shape)
    # Close the SVG tag
    svg_header += '</svg>'
    return svg_header


def Shape_test():
    # Test the Shape class with a premade shape
    shape = Shape.premade_random()
    print(str(shape))


def test():
    start = pick_shape()
    with open("input.svg", "w") as f:
        f.write(make_svg(start))

    changed = pick_shape(start, "duplicate", "down")
    with open("output.svg", "w") as f:
        f.write(make_svg(changed))

# [[inputText, outputText, SVGLeft, SVGRight], ...]
prompts = []

def generateConversions():
    global prompts
    with open("shapes.json") as f:
        shapes = json.load(f)
    shape_ids = list(shapes.keys())
    for i in range(len(shape_ids)):
        for j in range(i, len(shape_ids)):
            shape1 = shape_ids[i]
            shape2 = shape_ids[j]
            # Generate conversion prompt
            out = conversionPrompt(shape1, shape2)
            svg_left = make_svg(Shape.premade(shape1))
            svg_right = make_svg(Shape.premade(shape2))
            # Generate SVGs for the prompt
            for input_text, output_text in out:
                
                # Create the shapes
                # Add the prompt to the list
                prompts.append([input_text, output_text, svg_left, svg_right])

def generateRotations():
    global prompts
    with open("shapes.json") as f:
        shapes = json.load(f)
    shape_ids = list(shapes.keys())
    for i in range(len(shape_ids)):
        shape = shape_ids[i]
        # Generate rotation prompt
        for angle in range(15, 360, 15):
            out = rotationPrompt(shape, angle)
            svg_left = make_svg(Shape.premade(shape))
            svg_right = make_svg(Shape.premade(shape), "rotate", angle)
            # Generate SVGs for the prompt
            for input_text, output_text in out:
                # Create the shapes
                # Add the prompt to the list
                prompts.append([input_text, output_text, svg_left, svg_right]) 

def generateDuplications():
    global prompts
    with open("shapes.json") as f:
        shapes = json.load(f)
    shape_ids = list(shapes.keys())
    for i in range(len(shape_ids)):
        shape = shape_ids[i]
        for dir in ["down", "right"]:
            # Generate duplication prompt
            out = duplicationPrompt(shape, dir)
            svg_left = make_svg(Shape.premade(shape))
            svg_right = make_svg(Shape.premade(shape), "duplicate", dir)
            # Generate SVGs for the prompt
            for input_text, output_text in out:
                # Create the shapes
                # Add the prompt to the list
                prompts.append([input_text, output_text, svg_left, svg_right])


def main():
    generateConversions()
    generateRotations()
    generateDuplications()

    with open("prompts.tsv", "w") as f:
        for prompt in prompts:
            f.write("\t".join(prompt) + "\n")


if __name__ == "__main__":
    # main()
    main()
