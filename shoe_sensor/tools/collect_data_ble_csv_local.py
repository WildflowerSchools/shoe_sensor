########################################################################
## UNUSED CODE                                                        ##
########################################################################

import locationsensor.ble.core
import locationsensor.ble.collect
import locationsensor.shared_constants
from locationsensor.databases.measurement_database.csv_local import MeasurementDatabaseCSVLocal
import logging
import argparse

def main():
    parser = argparse.ArgumentParser(
        description='Read data from devices and save to local CSV file.',
        epilog = 'If number of cycles is set to zero, data will be collected until a keyboard interrupt (e.g., CTRL-C) is detected. If field list is specified, list must include timestamp and either device_id or short_device_id or both. If field list is not specified, all available BLE data fields will be collected (plus timestamp and short_device_id)'
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
        '-c',
        '--cycles',
        type = int,
        default = 1,
        help = 'number of times to collect data from each device (default is 1)'
    )
    parser.add_argument(
        '-f',
        '--field_list',
        help = 'path to text file containing list of data fields to collect (one field per line)'
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
    cycles = args.cycles
    field_list_path = args.field_list
    loglevel = args.loglevel
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
    # Build field list
    fields = []
    if field_list_path is not None:
        with open(field_list_path, 'r') as file:
            for line in file:
                fields.append(line.strip())
        if 'timestamp' not in fields:
            raise ValueError('Field list must include timestamp')
        if 'device_id' not in fields and 'short_device_id' not in fields:
            raise ValueError('Field list must include either device ID or short device ID')
        logging.info('Data will be collected for the following fields: {}'.format(', '.join(fields)))
    else:
        fields = locationsensor.shared_constants.REQUIRED_AND_BLE_READ_FIELDS
        logging.info('Data will be collected for all available BLE fields (plus timestamp and short_device_id)')
    # Initialize measurement database
    logging.info('Initializing measurement database as local CSV file')
    measurement_database = MeasurementDatabaseCSVLocal(
        directory = directory,
        filename_base = filename_base,
        fields = fields
    )
    # Scan for Decawave devices
    logging.info('Scanning for Decawave devices')
    decawave_devices = locationsensor.ble.core.scan_for_decawave_devices()
    num_decawave_devices = len(decawave_devices)
    logging.info('Found {} Decawave devices'.format(num_decawave_devices))
    # Get data from Decawave devices and write to database
    logging.info('Getting data from Decawave devices and writing to measurement database')
    locationsensor.ble.collect.collect_data(
        measurement_database = measurement_database,
        decawave_devices = decawave_devices,
        fields = fields,
        cycles = cycles)

if __name__ == '__main__':
    main()
