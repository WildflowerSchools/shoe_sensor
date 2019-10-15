import logging
import time
import os

import click
from database_connection.csv import DatabaseConnectionCSV

import shoe_sensor.core

@click.command()
@click.option('--directory', '-d', help='path to directory for output file (default is .)', default='.')
@click.option('--output_file', '-o', help='base of filename for output file; timestamp and .csv extension added automatically (default is measurement_data)', default='measurement_data')
@click.option('--timeout', '-t', type=int, help='number of seconds for each data collection cycle (default is 10)', default=10)
@click.option('--loglevel', '-l', help='log level (e.g., debug or warning or info)', default='WARNING')
@click.option('--mac_addresses', '-m', help='', default='mac_addresses.txt')
@click.option('--cycles', '-c', type=int, help='number of data collection cycles (default is 1)', default=1)
@click.option('--anchor_id', '-a', help='anchor ID')
def main(directory, output_file, mac_addresses, anchor_id, cycles, timeout, loglevel):
    """Read data from devices and save to local CSV file.

        If MAC addresses are not specified, script will scan for shoe sensors. If number of cycles is set to zero, data will be collected until a keyboard interrupt (e.g., CTRL-C) is detected.
    """
    filename_base = output_file
    mac_addresses_path = mac_addresses
    # Check that anchor ID is specified
    if anchor_id is None:
        anchor_id = os.getenv('ANCHOR_ID')
        if anchor_id is None:
            raise ValueError('Anchor ID must be specified on command line or in ANCHOR_ID environment variable')
    # Build path to output file
    file_timestamp = time.strftime('%y%m%d_%H%M%S', time.gmtime())
    path = os.path.join(
        directory,
        '{}_{}.csv'.format(
            filename_base,
            file_timestamp))
    # Set log level
    if loglevel is not None:
        numeric_loglevel = getattr(logging, loglevel.upper(), None)
        if not isinstance(numeric_loglevel, int):
            raise ValueError('Invalid log level: %s'.format(loglevel))
        logging.basicConfig(level=numeric_loglevel)
    # Set number of cycles
    if cycles == 0:
        logging.info('Data will be collected until keyboard interrupt is detected')
    else:
        logging.info('Data will be collected for {} cycles'.format(cycles))
    # Initialize database connection
    data_field_names = ['anchor_id', 'rssi']
    convert_from_string_functions = {'rssi': lambda string: int(string)}
    database_connection = DatabaseConnectionCSV(
        path,
        data_field_names = data_field_names,
        convert_from_string_functions = convert_from_string_functions
    )
    # Build list of MAC addresses
    if mac_addresses_path is not None:
        logging.info('Retrieving MAC addresses from {}'.format(mac_addresses_path))
        mac_addresses = []
        with open(mac_addresses_path, 'r') as file:
            for line in file:
                mac_address = line.strip()
                mac_addresses.append(mac_address)
    else:
        logging.info('Scanning for shoe sensors')
        mac_addresses = shoe_sensor.core.find_shoe_sensors()
    num_shoe_sensors = len(mac_addresses)
    logging.info('Found {} shoe sensors'.format(num_shoe_sensors))
    for mac_address in mac_addresses:
        logging.info('{}'.format(mac_address))
    # Get data from Decawave devices and write to database
    logging.info('Getting data from shoe sensors and writing to measurement database')
    shoe_sensor.core.collect_data(
        database_connection = database_connection,
        mac_addresses = mac_addresses,
        anchor_id = anchor_id,
        cycles = cycles,
        timeout = timeout)

if __name__ == '__main__':
    main()

