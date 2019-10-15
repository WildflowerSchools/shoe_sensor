import logging
import os

import click

import shoe_sensor.core


@click.command()
@click.option('--directory', '-d', help='path to directory for output file (default is .)', default='.')
@click.option('--output_file', '-o', help='filename for output file (default is mac_addresses.txt)', default='mac_addresses.txt')
@click.option('--timeout', '-t', type=int, help='number of seconds for scan (default is 10)', default=10)
@click.option('--loglevel', '-l', help='log level (e.g., debug or warning or info)', default='WARNING')
def main(directory, output_file, timeout, loglevel):
    """Scan for devices and save MAC addresses to local text file."""
    # Read arguments
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
