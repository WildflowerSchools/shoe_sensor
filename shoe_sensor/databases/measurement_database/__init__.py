"""
Define a database to contain data collected from Wildflower shoe sensors
"""

########################################################################
## UNUSED CODE                                                        ##
########################################################################

class MeasurementDatabase:
    """
    Class to represent a database containing data from DWM1001 devices.

    All methods must be implemented by derived classes.
    """
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
        raise NotImplementedError('Method must be implemented by derived class')
