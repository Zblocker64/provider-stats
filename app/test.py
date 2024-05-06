import random
from datetime import datetime, timedelta


def generate_random_data(start_date, end_date, nodes):
    data = []
    current_date = start_date
    while current_date <= end_date:
        for node in nodes:
            sum_value = random.randint(10000, 100000)  # Adjust range as needed
            count_value = random.randint(1, 100)  # Adjust range as needed
            min_value = random.randint(1000, 5000)  # Adjust range as needed
            max_value = random.randint(min_value, 10000)  # Adjust range to ensure it's >= min_value

            sum_sqr_value = sum_value ** 2  # Or any other calculation you wish to use
            data.append({
                "key": [current_date.strftime("%Y-%m-%d"), node],
                "value": {
                    "sum": sum_value,
                    "count": count_value,
                    "min": min_value,
                    "max": max_value,
                    "sumsqr": sum_sqr_value
                }
            })
        current_date += timedelta(days=1)
    return data


# Define the start and end dates of April
start_date = datetime(2024, 4, 1)
end_date = datetime(2024, 4, 30)

# Define your node names
nodes = ["node1", "node2", "node3", "node4"]

# Generate the data
random_data = generate_random_data(start_date, end_date, nodes)

print(random_data)
