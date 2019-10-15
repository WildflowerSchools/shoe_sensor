import shoe_sensor.core
from database_connection_honeycomb import DatabaseConnectionHoneycomb
import logging
import time
import os

import click


@click.command()
@click.option('--env_name', '-e', help='Honeycomb environment name (default is "TEST Ted home office")')
@click.option('--object_type', '-o', help='Honeycomb object type (default is DEVICE)', default="DEVICE")
@click.option('--object_id_field_name', '-f', help='name of Honeycomb field in which to store object ID (default is part_number)', default="part_number")
@click.option('--timeout', '-t', type=int, help='number of seconds for each data collection cycle (default is 10)', default=10)
@click.option('--loglevel', '-l', help='log level (e.g., debug or warning or info)', default='WARNING')
@click.option('--mac_addresses_path', '-m', help='', default='mac_addresses.txt')
@click.option('--cycles', '-c', type=int, help='number of data collection cycles (default is 1)', default=1)
@click.option('--anchor_id', '-a', help='anchor ID')
def main(env_name, object_type, object_id_field_name, mac_addresses_path, anchor_id, cycles, timeout, loglevel):
    """Read data from devices and save to Honeycomb.

    If MAC addresses are not specified, script will scan for shoe sensors. If number of cycles is set to zero, data will be collected until a keyboard interrupt (e.g., CTRL-C) is detected.
    """
    # Check for environment and anchor ID
    if env_name is None:
        raise ValueError('Honeycomb environment must be specified')
    if anchor_id is None:
        raise ValueError('Anchor ID must be specified')
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
    database_connection = DatabaseConnectionHoneycomb(
        environment_name_honeycomb = env_name,
        object_type_honeycomb = object_type,
        object_id_field_name_honeycomb = object_id_field_name
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
