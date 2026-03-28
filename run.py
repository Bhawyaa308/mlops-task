import argparse
import pandas as pd
import numpy as np
import yaml
import logging
import time
import sys
import json
import os

def setup_logging(log_file):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

def write_error(output_path, version, message):
    error_output = {
        "version": version,
        "status": "error",
        "error_message": message
    }
    with open(output_path, "w") as f:
        json.dump(error_output, f, indent=2)
    print(json.dumps(error_output))
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--log-file", required=True)

    args = parser.parse_args()

    setup_logging(args.log_file)
    logging.info("Job started")

    start_time = time.time()

    # -------- LOAD CONFIG --------
    try:
        with open(args.config, "r") as f:
            config = yaml.safe_load(f)

        required_keys = ["seed", "window", "version"]
        for key in required_keys:
            if key not in config:
                raise ValueError(f"Missing config key: {key}")

        seed = config["seed"]
        window = config["window"]
        version = config["version"]

        np.random.seed(seed)

        logging.info(f"Config loaded: seed={seed}, window={window}, version={version}")

    except Exception as e:
        logging.error(str(e))
        write_error(args.output, "unknown", str(e))

    # -------- LOAD DATA --------
    try:
        if not os.path.exists(args.input):
            raise FileNotFoundError("Input file not found")

        df = pd.read_csv(args.input)

        if df.empty:
            raise ValueError("CSV is empty")

        if "close" not in df.columns:
            raise ValueError("Missing 'close' column")

        logging.info(f"Rows loaded: {len(df)}")

    except Exception as e:
        logging.error(str(e))
        write_error(args.output, version, str(e))

    # -------- PROCESS --------
    try:
        # Rolling mean
        df["rolling_mean"] = df["close"].rolling(window=window).mean()
        logging.info("Rolling mean computed")

        # Signal (keep all rows, handle NaN properly)
        df["signal"] = (df["close"] > df["rolling_mean"]).astype(float)
        df["signal"] = df["signal"].fillna(0).astype(int)
        logging.info("Signal generation completed")

        rows_processed = len(df)
        signal_rate = df["signal"].mean()

        latency_ms = int((time.time() - start_time) * 1000)

        output = {
            "version": version,
            "rows_processed": rows_processed,
            "metric": "signal_rate",
            "value": float(round(signal_rate, 4)),
            "latency_ms": latency_ms,
            "seed": seed,
            "status": "success"
        }

        with open(args.output, "w") as f:
            json.dump(output, f, indent=2)

        logging.info(f"Metrics: {output}")
        logging.info("Job completed successfully")

        print(json.dumps(output))

    except Exception as e:
        logging.error(str(e))
        write_error(args.output, version, str(e))


if __name__ == "__main__":
    main()