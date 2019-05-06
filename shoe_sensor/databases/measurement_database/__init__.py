"""
Define a database to contain data collected from Wildflower shoe sensors
"""

class MeasurementDatabase:
    """
    Class to represent a database containing data from devices.

    All methods must be implemented by derived classes.
    """
    def put_device_data(
        self,
        device_data):
        """
        Write measurement data to the database.

        Device data must include 'timestamp'.

        Parameters:
            device_data (dict): Dictionary containing device data
        """
        raise NotImplementedError('Method must be implemented by derived class')
