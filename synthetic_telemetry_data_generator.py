
import argparse
import csv
import math
import os
import random
from datetime import datetime, timedelta, timezone

import yaml


def generate_parameter_name(index: int) -> str:
    """
    Generate realistic spacecraft-style parameter names.
    """

    systems = [
        "THERMAL",
        "POWER",
        "PROP",
        "NAV",
        "COMMS",
        "ATT",
        "PAYLOAD"
    ]

    metrics = [
        "TEMP",
        "VOLT",
        "CURR",
        "PRESS",
        "RATE",
        "STATUS",
        "FLOW",
        "RPM"
    ]

    system = random.choice(systems)
    metric = random.choice(metrics)

    return f"{system}_{metric}_{index:03d}"



def generate_base_value(metric: str):
    """
    Returns a realistic baseline value and range.
    """

    if "TEMP" in metric:
        return random.uniform(15, 40), 5

    if "VOLT" in metric:
        return random.uniform(24, 48), 2

    if "CURR" in metric:
        return random.uniform(1, 15), 1.5

    if "PRESS" in metric:
        return random.uniform(50, 200), 10

    if "FLOW" in metric:
        return random.uniform(5, 30), 3

    if "RPM" in metric:
        return random.uniform(1000, 5000), 250

    if "RATE" in metric:
        return random.uniform(0, 5), 0.5

    return random.uniform(0, 1), 0.2

def generate_telemetry(
    params: int,
    duration_hours: int,
    sample_rate: int,
    out_folder: str
):
    """
    Generates:
    - synth_values.csv
    - synth_params.yaml
    """

    os.makedirs(out_folder, exist_ok=True)

    csv_path = os.path.join(out_folder, "synth_values.csv")
    yaml_path = os.path.join(out_folder, "synth_params.yaml")

    # Generate parameter metadata
    parameter_metadata = []

    for i in range(params):

        param_name = generate_parameter_name(i)

        base_value, noise = generate_base_value(param_name)

        param_info = {
            "name": param_name,
            "base_value": round(base_value, 3),
            "noise_amplitude": round(noise, 3),
            "unit": "arb"
        }

        parameter_metadata.append(param_info)

    #Write YAML metadata
    yaml_content = {
        "generator": "Synthetic Spacecraft Telemetry Generator",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "parameters": parameter_metadata
    }

    with open(yaml_path, "w") as yaml_file:
        yaml.dump(yaml_content, yaml_file, sort_keys=False)

    #Generate timestamps
    total_samples = duration_hours * 3600 // sample_rate

    start_time = datetime.now(timezone.utc)

    #Write CSV
    fieldnames = ["timestamp"] + [
        p["name"] for p in parameter_metadata
    ]

    with open(csv_path, "w", newline="") as csv_file:

        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()

        for sample_idx in range(total_samples):

            timestamp = (
                start_time +
                timedelta(seconds=sample_idx * sample_rate)
            )

            row = {
                "timestamp": timestamp.isoformat()
            }

            #Generate telemetry values
            for param in parameter_metadata:

                base = param["base_value"]
                noise_amp = param["noise_amplitude"]

                # Slow oscillation trend
                trend = math.sin(sample_idx / 300)

                # Random telemetry noise
                noise = random.uniform(-noise_amp, noise_amp)

                value = base + trend + noise

                # Occasional anomaly injection
                if random.random() < 0.0005:
                    value += random.uniform(5 * noise_amp, 15 * noise_amp)

                row[param["name"]] = round(value, 3)

            writer.writerow(row)

    print("Telemetry generation completed")
    print(f"CSV file: {csv_path}")
    print(f"YAML file: {yaml_path}")
    print(f"Total samples: {total_samples}")
    print(f"Parameters generated: {params}")



#CLI Entry Point
if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Synthetic telemetry data generator"
    )

    parser.add_argument(
        "--params",
        type=int,
        required=True,
        help="Number of telemetry parameters"
    )

    parser.add_argument(
        "--duration-hours",
        type=int,
        required=True,
        help="Telemetry duration in hours"
    )

    parser.add_argument(
        "--sample-rate",
        type=int,
        required=True,
        help="Sampling interval in seconds"
    )

    parser.add_argument(
        "--out",
        type=str,
        required=True,
        help="Output folder"
    )

    args = parser.parse_args()

    generate_telemetry(
        params=args.params,
        duration_hours=args.duration_hours,
        sample_rate=args.sample_rate,
        out_folder=args.out
    )
