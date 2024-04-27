import csv
import matplotlib.pyplot as plt

def read_csv(file_path):
    escaped_data = {"Panickers": [], "Wardens": []}
    with open(file_path, newline="") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        for row in reader:
            escaped_data["Panickers"].append(int(row[0]))
            escaped_data["Wardens"].append(int(row[1]))
    return escaped_data

def plot_line_chart(escaped_data):
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(escaped_data["Panickers"]) + 1), escaped_data["Panickers"], label="Panickers", marker='o')
    plt.plot(range(1, len(escaped_data["Wardens"]) + 1), escaped_data["Wardens"], label="Wardens", marker='o')
    plt.title("Number of Escaped Agents Over Time")
    plt.xlabel("Time Step")
    plt.ylabel("Number of Agents Escaped")
    plt.legend()
    plt.grid(True)
    plt.show()

def read_csv_bar(file_path):
    with open(file_path, newline="") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        total_panickers = 0
        total_wardens = 0
        for row in reader:
            total_panickers = int(row[0])
            total_wardens = int(row[1])
    return total_panickers, total_wardens

if __name__ == "__main__":
    file_path = "escape_data.csv"
    escaped_data = read_csv(file_path)
    plot_line_chart(escaped_data)
