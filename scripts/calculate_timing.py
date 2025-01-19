import os
import statistics
from consumer import TIMINGS_PATH

if __name__ == '__main__':
    tests = {}

    # Gather all .timings data
    for filename in os.listdir(TIMINGS_PATH):
        # Ensure it's actually a directory (and not a file).
        full_dir = TIMINGS_PATH / filename
        if not os.path.isdir(full_dir):
            continue

        tests[filename] = []
        for test_file in os.listdir(full_dir):
            if test_file.endswith(".timings"):
                with open(full_dir / test_file, "r") as f:
                    lines = f.readlines()
                    # Convert each line (microseconds) to milliseconds.
                    timings_in_ms = []
                    for line in lines:
                        line_stripped = line.strip()
                        if line_stripped.isdigit():
                            micro_val = int(line_stripped)      # microseconds
                            ms_val = micro_val / 1000.0         # convert µs to ms
                            timings_in_ms.append(ms_val)
                    tests[filename].extend(timings_in_ms)

    # Calculate and print statistics in milliseconds
    for test_name, timings in tests.items():
        if len(timings) == 0:
            print(f"Test: {test_name} => No data found")
            continue

        # Compute statistics (in ms)
        avg_ms = statistics.mean(timings)
        med_ms = statistics.median(timings)
        std_dev_ms = statistics.stdev(timings) if len(timings) > 1 else 0.0

        # Print results
        print(f"Test: {test_name} -- W -- Time In System")
        print(f"  Mean   : {avg_ms:.2f} ms")
        print(f"  Median : {med_ms:.2f} ms")
        print(f"  StdDev : {std_dev_ms:.2f} ms")
        print("-" * 40)
