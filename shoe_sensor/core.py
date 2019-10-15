"""
Provide core classes, methods, and functions for communicating with Wildflower shoe sensors devices via BLE.
"""
import bluepy.btle
# import bitstruct
# import tenacity
import logging
# import time
# import warnings
import datetime

logger = logging.getLogger(__name__)

# retry_initial_wait = 0.1 # seconds
# retry_num_attempts = 4
# exponential_retry = tenacity.retry(
#         stop = tenacity.stop_after_attempt(retry_num_attempts),
#         wait = tenacity.wait_exponential(multiplier=retry_initial_wait/2),
#         before = tenacity.before_log(logger, logging.DEBUG),
#         after = tenacity.after_log(logger, logging.DEBUG),
#         before_sleep = tenacity.before_sleep_log(logger, logging.WARNING))

# BLE advertising data codes
MANUFACTURER_SPECIFIC_TYPE_CODE = int('0xFF', 16)
SHOE_SENSOR_MANUFACTURER_SPECIFIC_VALUE = '8a07' # Should be  0x8a 0x07 in some format

def find_shoe_sensors(num_scans = 1, timeout = 10):
    scanner = bluepy.btle.Scanner()
    mac_addresses = []
    for scan_index in range(num_scans):
        scan_entries = scanner.scan(timeout)
        for scan_entry in scan_entries:
            scan_data = scan_entry.getScanData()
            for type_code, description, value in scan_data:
                if (type_code == MANUFACTURER_SPECIFIC_TYPE_CODE and
                    value == SHOE_SENSOR_MANUFACTURER_SPECIFIC_VALUE):
                    mac_address = scan_entry.addr
                    if mac_address not in mac_addresses:
                        mac_addresses.append(mac_address)
    return mac_addresses

def collect_data(
    database_connection,
    mac_addresses,
    anchor_id,
    cycles = 1,
    timeout = 10):
    """
    Collect specified data from specified devices and save in specified
    database.

    If the number of cycles is set to zero, data will be collected until a
    keyboard interrupt.

    Parameters:
        database_connection (DatabaseConnection): Database where data should be stored
        mac_addresses (list): MAC addresses for devices we want to collect from
        cycles (int): Number of times to collect data from each device (default is 1)
    """
    if cycles == 0:
        logger.info('Collecting data until keyboard interrupt is detected'.format(cycles))
    else:
        logger.info('Collecting data for {} cycles'.format(cycles))
    cycles_completed = 0
    scanner = bluepy.btle.Scanner().withDelegate(ShoeSensorDelegate(database_connection, mac_addresses, anchor_id))
    try:
        while cycles == 0 or cycles_completed < cycles:
            try:
                logger.info('Data collection cycle {}'.format(cycles_completed + 1))
                scanner.scan(timeout)
            except bluepy.btle.BTLEDisconnectError:
                logger.error('disconnect error, reconnecting')
            cycles_completed += 1
    except KeyboardInterrupt:
        logger.warning('Keyboard interrupt detected. Shutting down data collection.')

class ShoeSensorDelegate(bluepy.btle.DefaultDelegate):
    def __init__(self, database_connection, mac_addresses, anchor_id):
        bluepy.btle.DefaultDelegate.__init__(self)
        self.mac_addresses = mac_addresses
        self.database_connection = database_connection
        self.anchor_id = anchor_id

    def handleDiscovery(self, dev, isNewDev, isNewData):
        mac_address = dev.addr
        if mac_address in self.mac_addresses:
            timestamp = datetime.datetime.now(datetime.timezone.utc)
            rssi = dev.rssi
            logger.debug('{}: {} dB'.format(mac_address, rssi))
            device_data = {'anchor_id': self.anchor_id, 'rssi': rssi}
            self.database_connection.write_datapoint_object_time_series(
                timestamp = timestamp,
                object_id = mac_address,
                data = device_data
            )
