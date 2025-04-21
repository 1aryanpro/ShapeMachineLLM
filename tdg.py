import csv

# Replace with your actual CSV file path
csv_file_path = "./TrainingData.csv"

formatted_rows = []

with open(csv_file_path, mode="r", newline='', encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        formatted = f"Input: {row['Input']}\nOutput: {
            row['Output']}\nSVG: {row['SVG']}\n"
        formatted_rows.append(formatted)

# Now `formatted_rows` contains each formatted string
for entry in formatted_rows:
    print(entry)

