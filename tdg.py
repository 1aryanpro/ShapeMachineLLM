import csv

tsv_filename = './prompts.tsv'
output_filename = 'prompts.txt'


def svgTemplate(left, right):
    return f"""
<svg xmlns="http://www.w3.org/2000/svg"
     width="500" height="500"
     viewBox="0 0 500 500">
     {left}
 <line x1="250" y1="100" x2="250" y2="405" stroke="#000" stroke-width="1"/>
 <g transform="translate(300, 0)">
 {right}
 </g>
</svg>
"""


with open(tsv_filename, newline='') as tsvfile, open(output_filename, 'w') as outfile:
    reader = csv.reader(tsvfile, delimiter='\t')

    for row in reader:
        if len(row) >= 4:
            input_val = row[0]
            output_val = row[1]
            svg_left = row[2]
            svg_right = row[3]

            result_string = f"Input:\n{input_val}\n\nOutput:\n{
                output_val}\n\n##STARTING-SVG-CODE##{
                svgTemplate(svg_left, svg_right)}##ENDING-SVG-CODE##\n\n"
            outfile.write(result_string + '\n')
