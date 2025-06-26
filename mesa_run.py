from mesa_server import server
import csv
import os

if __name__ == "__main__":
    filename = "rcc_simulation.csv"
    headers = [
        "activate_therapy",
        "patient_sex",
        "bmi",
        "cd8",
        "treg",
        "nk",
        "m1",
        "m2",
        "tumorCells",
        "immune_response_level",
        "tumor_proliferation_rate",
        "resistance_to_therapy",
        "result"  # result of simulation -> True = alive, False = dead
    ]

    # Verifying if file is empty
    write_header = not os.path.exists(filename) or os.stat(filename).st_size == 0

    with open(filename, mode="a", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        if write_header:
            writer.writerow(headers)

    server.port = 8531
    server.launch()




