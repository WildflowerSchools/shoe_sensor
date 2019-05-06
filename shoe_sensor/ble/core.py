"""
Provide core classes, methods, and functions for communicating with Decawave DWM1001 devices via BLE.
"""
import bluepy.btle
import bitstruct
import tenacity
import logging
import time
import warnings

logger = logging.getLogger(__name__)

retry_initial_wait = 0.1 # seconds
retry_num_attempts = 4
exponential_retry = tenacity.retry(
        stop = tenacity.stop_after_attempt(retry_num_attempts),
        wait = tenacity.wait_exponential(multiplier=retry_initial_wait/2),
        before = tenacity.before_log(logger, logging.DEBUG),
        after = tenacity.after_log(logger, logging.DEBUG),
        before_sleep = tenacity.before_sleep_log(logger, logging.WARNING))

# BLE advertising data codes
MANUFACTURER_SPECIFIC_TYPE_CODE = int('0xFF', 16)
MANUFACTURER_SPECIFIC_VALUE = 'TBD' # Should be  0x8a 0x07

########################################################################
## UNUSED CODE                                                        ##
########################################################################

def scan_for_decawave_devices():
    """
    Scan all nearby BLE devices to find DWM1001 devices.

    Returns a dictionary in which the keys are 8-byte device IDs and
    the values are DecawaveDeviceBLE objects.

    Returns:
        dict: Dictionary of found DWM1001 devices
    """
    scan_entries = _get_scan_entries()
    decawave_devices = {}
    for scan_entry in scan_entries:
        scan_data = scan_entry.getScanData()
        for type_code, description, value in scan_data:
            if (type_code == SERVICE_DATA_TYPE_CODE and
                description == SERVICE_DATA_DESCRIPTION and
                value.startswith(SERVICE_DATA_VALUE_FIXED_PORTION)):
                decawave_device = DecawaveDeviceBLE(scan_entry)
                decawave_devices[decawave_device.device_id] = decawave_device
    return decawave_devices

    def read_scan_data(self):
        """
        Retrieve basic BLE scan and BLE advertising data from device.

        Data is returned as a dictionary containing:
            mac_address (str): MAC address of device
            address_type (str): Address type (public or random)
            interface (int): Interface number (e.g. 0 = /dev/hci0)
            rssi (int): RSSI of received signal in dB
            connectable (bool): Boolean indicating whether device is connectable
            num_advertising_data (int): Number of advertising data received
            advertising_type_code (list of int): Advertising data type codes
            advertising_description (list of str): Advertising data descriptions
            advertising_value (list of str): Advertising data values

        Returns:
            dict: Dictionary containing retrieved scan data
        """
        raw_scan_data = self._get_raw_scan_data()
        scan_data = _convert_from_raw(
            raw_scan_data,
            'scan_data')
        return scan_data


# Function for retrieving scan entries
@exponential_retry
def _get_scan_entries():
    scanner = bluepy.btle.Scanner()
    scan_entries = scanner.scan()
    return scan_entries
