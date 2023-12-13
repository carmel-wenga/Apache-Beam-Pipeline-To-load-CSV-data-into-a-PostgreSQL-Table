"""
@author: Carmel WENGA
"""

import argparse
import logging
import re

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from beam_postgres.io import WriteToPostgres


def parse_data(input_str):

    rows = dict()

    for row in re.split('\n', input_str):
        values = re.split(",", row)
        rows.update(
            {
                "age": values[0],
                "gender": values[1],
                "education_level": re.sub("'s", "", values[2]),
                "job_title": values[3],
                "year_of_experience": values[4],
                "salary": values[5]
            }
        )

    return rows


def run(argv=None):
    """The main function which creates the pipeline and runs it."""

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--src',
        dest='src',
        required=False,
        help='Please specify the input csv file to read.',
        default='source/salaries_data.csv'
    )

    parser.add_argument(
        '--dbhost',
        dest='dbhost',
        required=False,
        help='Please specify the hostname of the database',
        default='localhost'
    )

    parser.add_argument(
        '--dbport',
        dest='dbport',
        required=False,
        help='Please specify the expose port of the database',
        default=5432
    )

    # Parse all arguments from the command line.
    known_args, pipeline_args = parser.parse_known_args(argv)

    # Initiate the pipeline using the pipeline unknown arguments passed in from the command line.
    # Unknown arguments are the one not specified using the parser.add_argument() method.
    p = beam.Pipeline(options=PipelineOptions(pipeline_args))

    (p
        # Read the file. This is the source csv files of the pipeline.
        | 'Read from a File' >> beam.io.ReadFromText(known_args.src, skip_header_lines=1)

        # Convert csv rows to JSON
        | 'CSV to JSON' >> beam.Map(lambda s: parse_data(s))

        # Write data to Postgres
        | 'Write to Postgres' >> WriteToPostgres(
            host=known_args.dbhost,
            database='beamdb',
            table='public.salaries',
            user='beamdb',
            password='ra5hoxetRami5',
            port=known_args.dbport,
            batch_size=1000,
        )
     )
    p.run().wait_until_finish()


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()
