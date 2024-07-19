import re
import random

def generate_color_map(labels):
    """
    Generate a color map with distinct colors for each label.
    """
    color_map = {}
    for label in labels:
        # Generate random colors
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        a = 255  # Alpha value
        color_map[label] = (r, g, b, a)
    return color_map

def parse_labels(file_path):
    """
    Parse the input file to extract labels and their coordinates.
    """
    labels = []
    with open(file_path, "r") as file:
        for line in file:
            match = re.search(r'<label index="(\d+)" x="([0-9.]+)" y="([0-9.]+)" z="([0-9.]+)">(.*?)</label>', line)
            if match:
                index, x, y, z, name = match.groups()
                labels.append((int(index), float(x), float(y), float(z), name))
    return labels

def format_labels(labels, color_map):
    """
    Format the labels with their corresponding colors.
    """
    formatted_data = []
    for index, x, y, z, name in labels:
        if name in color_map:
            r, g, b, a = color_map[name]
            formatted_data.append(f"{index}\t{name.replace('_', '-')}\t{r}\t{g}\t{b}\t{a}")
    return formatted_data

def main():
    input_file = "labels.txt"
    labels = parse_labels(input_file)
    
    # Extract unique label names
    unique_labels = list(set(label[4] for label in labels))
    
    # Generate color map dynamically
    color_map = generate_color_map(unique_labels)
    
    formatted_data = format_labels(labels, color_map)

    header = "#No.\tLabel Name:\t\tR\tG\tB\tA"
    print(header)
    for data in formatted_data:
        print(data)

if __name__ == "__main__":
    main()
