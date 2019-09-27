from cerberus import Validator
from engine.config import config as cf


class SherlockValidator(Validator):
    def _validate_relativemin(self, relativemin, field, value):
        """ Test if the value of a field is greater than the value of another field

        The rule's arguments are validated against this schema:
        {'type': 'string'}
        """
        min_date = self.document[relativemin]
        if (min_date is not None) & (value is not None):
            if value < min_date:
                self._error(field, cf.err_msg_relativemin % relativemin)

    def _validate_relativemax(self, relativemax, field, value):
        """ Test if the value of a field is smaller than the value of another field

        The rule's arguments are validated against this schema:
        {'type': 'string'}
        """

        max_date = self.document[relativemax]
        if (max_date is not None) & (value is not None):
            if value > max_date:
                self._error(field, cf.err_msg_relativemax % relativemax)
