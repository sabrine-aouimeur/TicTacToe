import csv

def export_q_table_to_csv(q_table_obj, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['State', 'Action', 'Value'])
        
        # Access the internal dictionary directly
        for (state, action), value in q_table_obj._q_table.items():
            writer.writerow([state, action, value])

    print(f"Q-Table exported to {filename}")