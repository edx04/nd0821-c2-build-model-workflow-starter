#!/usr/bin/env python
"""
Performs basic cleaning on the data and save the results in Weights & Biases
"""
import argparse
import logging
import wandb
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    ######################
    # YOUR CODE HERE     #
    ######################

    logger.info(f'Download input artifact {args.input_artifact}')
    artifact_local_path = run.use_artifact(args.input_artifact).file()
    df = pd.read_csv(artifact_local_path)

    logger.info(f"Removing outliers")
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()
   
    logger.info(f"Converting last_review column to datetime")
    df['last_review'] = pd.to_datetime(df['last_review'])

    logger.info(f"Saving the dataset")
    df.to_csv("clean_sample.csv", index=False)

    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file("clean_sample.csv")
    run.log_artifact(artifact)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This steps cleans the data")

    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="Input artifact name",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="Output artifact name",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="Output artifact type",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="Output artifact description",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help="Minimum price to filter outliers",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help="Maximum price to filter outliers",
        required=True
    )


    args = parser.parse_args()

    go(args)
