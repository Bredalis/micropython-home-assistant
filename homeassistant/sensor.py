class Sensor(object):
    """Sensor class for Home Assistant.

    Optionally allows a report_delta parameter to only report if current value
    differs more than `report_delta` from previously reported value.
    """

    def __init__(self, entity_id, value_func, unit_of_measurement,
                 report_delta=None):
        # Initialize sensor attributes
        self._entity_id = entity_id  # ID of the sensor entity in Home Assistant
        self._value_func = value_func  # Function to retrieve the sensor value
        self._value = None  # Initialize sensor value
        self._report_delta = report_delta  # Difference threshold for reporting
        self._attributes = {'unit_of_measurement': unit_of_measurement}  # Sensor measurement unit

    def report(self, hass):
        # Get the current value from the value function
        value = self._value_func()

        # Check if reporting is needed based on report_delta and current value difference
        do_report = (
            self._value is None or
            self._report_delta is None or
            abs(value - self._value) > self._report_delta
        )

        # If no reporting needed based on conditions, exit
        if not do_report:
            return

        # Report the sensor state to Home Assistant
        hass.set_state(self.entity_id, value, self._attributes)
        # Update the sensor value for future comparison
        self._value = value
