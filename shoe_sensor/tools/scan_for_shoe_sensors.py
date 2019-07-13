import shoe_sensor.core
from shoe_sensor.databases.measurement_database.csv_local import MeasurementDatabaseCSVLocal
import logging
import argparse
import os

def main():
    parser = argparse.ArgumentParser(
        description='Scan for devices and save MAC addresses to local text file.'
    )
    parser.add_argument(
        '-d',
        '--dir',
        default = '.',
        help = 'path to directory for output file (default is .)'
    )
    parser.add_argument(
        '-o',
        '--output_file',
        default = 'mac_addresses.txt',
        help = 'filename for output file (default is mac_addresses.txt)'
    )
    parser.add_argument(
        '-t',
        '--timeout',
        type = int,
        default = 10,
        help = 'number of seconds for scan (default is 10)'
    )
    parser.add_argument(
        '-l',
        '--loglevel',
        help = 'log level (e.g., debug or warning or info)'
    )
    # Read arguments
    args = parser.parse_args()
    directory = args.dir
    output_file = args.output_file
    timeout = args.timeout
    loglevel = args.loglevel
    # Set log level
    if loglevel is not None:
        numeric_loglevel = getattr(logging, loglevel.upper(), None)
        if not isinstance(numeric_loglevel, int):
            raise ValueError('Invalid log level: %s'.format(loglevel))
        logging.basicConfig(level=numeric_loglevel)
    # Build list of MAC addresses
    logging.info('Scanning for shoe sensors')
    mac_addresses = shoe_sensor.core.find_shoe_sensors(
        num_scans = 1,
        timeout = timeout
    )
    num_shoe_sensors = len(mac_addresses)
    logging.info('Found {} shoe sensors'.format(num_shoe_sensors))
    for mac_address in mac_addresses:
        logging.info('{}'.format(mac_address))
    mac_addresses_path = os.path.join(
        directory,
        output_file
    )
    logging.info('Writing MAC addresses to {}'.format(mac_addresses_path))
    with open(mac_addresses_path, 'w') as file:
        for mac_address in mac_addresses:
            file.write('{}\n'.format(mac_address))

if __name__ == '__main__':
    main()
