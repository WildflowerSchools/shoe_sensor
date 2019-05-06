"""
Implement a measurement database as a local CSV file.
"""

########################################################################
## UNUSED CODE                                                        ##
########################################################################

from . import MeasurementDatabase
import os
import time
import logging

class MeasurementDatabaseCSVLocal(MeasurementDatabase):
    """
    Implementation of a MeasurementDatabase as a local CSV file.
    """
    def __init__(
        self,
        directory,
        filename_base,
        fields):
        """
        Constructor for MeasurementDatabaseCSVLocal.

        Included fields must include 'timestamp' and either 'device_id' or
        'short_device_id' (or both). Any data that is sent to this database that
        does not match the specified included fields will be silently dropped.
        Constructor will raise an exception if required fields are missing or
        any of the field names are not recognized.

        Parameters:
            directory (string): Path to directory for CSV file
            filename_base (string): Base of filename for CSV file; timestamp and .csv extension added automatically
            fields (list of string): Names of fields we want to include in the CSV file
        """
        if 'timestamp' not in fields:
            raise ValueError('Included fields must include timestamp')
        if 'device_id' not in fields and 'short_device_id' not in fields:
            raise ValueError('Included fields must include either device ID or short device ID')
        self._fields = fields
        file_timestamp = time.strftime('%y%m%d_%H%M%S', time.gmtime())
        path = os.path.join(
            directory,
            '{}_{}.csv'.format(
                filename_base,
                file_timestamp))
        csv_logger = logging.getLogger('measurement_database_local_csv')
        csv_logger.setLevel(logging.INFO)
        csv_logger.propagate = False
        file_handler = logging.FileHandler(
            path,
            'w')
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(message)s')
        file_handler.setFormatter(formatter)
        csv_logger.addHandler(file_handler)
        self.csv_logger = csv_logger
        # Build the header
        header_list = []
        for field in fields:
            field_info = locationsensor.shared_constants.DATA_FIELD_INFO.get(field)
            if field_info is None:
                raise ValueError('Field name {} not recognized'.format(field))
            if field_info.get('list'):
                for index in range(field_info['max_list_length']):
                    header_list.append('{}{:02}'.format(field, index))
            else:
                header_list.append(field)
        header_string = ','.join(header_list)
        # Write the header
        csv_logger.info(header_string)

    def put_device_data(
        self,
        device_data):
        """
        Write DWM1001 data to the database.

        Device data must include 'timestamp' and either 'device_id' or
        'short_device_id' (or both).

        Parameters:
            device_data (dict): Dictionary containing device data
        """
        # Buld the row
        if 'timestamp' not in device_data.keys():
            raise ValueError('Data must include timestamp')
        if 'device_id' not in device_data.keys() and 'short_device_id' not in device_data.keys():
            raise ValueError('Data must include either device ID or short device ID')
        row_list = []
        for field in self._fields:
            row_list.append(_format_datum(field, device_data.get(field)))
        row_string = ','.join(row_list)
        # Write the row
        self.csv_logger.info(row_string)

def _format_datum(field, datum):
    string_list = []
    field_info = locationsensor.shared_constants.DATA_FIELD_INFO.get(field)
    if field_info is None:
        raise ValueError('Field name {} not recognized'.format(field))
    if field_info.get('list'):
        for index in range(field_info['max_list_length']):
            if datum is not None and index < len(datum):
                string_list.append(field_info['string_format'].format(datum[index]))
            else:
                string_list.append('')
    else:
        if datum is not None:
            string_list.append(field_info['string_format'].format(datum))
        else:
            string_list.append('')
    datum_string = ','.join(string_list)
    return datum_string
