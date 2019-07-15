import shoe_sensor.core
from database_connection.csv import DatabaseConnectionCSV
import logging
import argparse
import time
import os

def main():
    parser = argparse.ArgumentParser(
        description='Read data from devices and save to local CSV file.',
        epilog = 'If MAC addresses are not specified, script will scan for shoe sensors. If number of cycles is set to zero, data will be collected until a keyboard interrupt (e.g., CTRL-C) is detected.'
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
        default = 'measurement_data',
        help = 'base of filename for output file; timestamp and .csv extension added automatically (default is measurement_data)'
    )
    parser.add_argument(
        '-m',
        '--mac_addresses',
        help = 'path to text file with list of MAC addresses to scan for (colon-separated hex strings, one per line)'
    )
    parser.add_argument(
        '-t',
        '--timeout',
        type = int,
        default = 10,
        help = 'number of seconds for each data collection cycle (default is 10)'
    )
    parser.add_argument(
        '-c',
        '--cycles',
        type = int,
        default = 1,
        help = 'number of data collection cycles (default is 1)'
    )
    parser.add_argument(
        '-a',
        '--anchor_id',
        help = 'anchor ID'
    )
    parser.add_argument(
        '-l',
        '--loglevel',
        help = 'log level (e.g., debug or warning or info)'
    )
    # Read arguments
    args = parser.parse_args()
    directory = args.dir
    filename_base = args.output_file
    mac_addresses_path = args.mac_addresses
    timeout = args.timeout
    cycles = args.cycles
    anchor_id = args.anchor_id
    loglevel = args.loglevel
    # Check that anchor ID is specified
    if anchor_id is None:
        raise ValueError('Anchor ID must be specified')
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
