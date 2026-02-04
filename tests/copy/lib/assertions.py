import logging

class Assertions:
    """class with helper functions containing assertions for workflow tests"""

    def __init__(self):
        """Copy management class builder
        Args:
        """
        pass 

    def validate_value_on_constraint(self,value_to_validate,list_of_valid_values_with_typo):
        """
        Purpose: Validate a value is the expected on a typo list
        :param value_to_validate: value to be validated
        :param list_of_valid_values_with_typo: valid dictionary to compare with typo on first element of the array
        
        :return: None
        """

        data = list_of_valid_values_with_typo
        data_type = data[0]
        # Decisions depending type of data
        if data_type == "String" or data_type == "Enum":
            valid_values = data[1:len(data)]
            logging.info(f"Current value : {value_to_validate} in {valid_values}")
            # Check that current value is in range of acepted values
            assert value_to_validate in valid_values, f"Current value : {value_to_validate} not in {valid_values}" 
        elif data_type == "Double" or data_type == "Integer":
            min = max = data[1]
            if len(data) > 2:
                max = data[2]    
            # Check that current value is in range of acepted values
            assert value_to_validate >= min or value_to_validate <=max, f"Current value: {value_to_validate} not in range min: {min} and max: {max} "
            logging.info(f"Current value: {value_to_validate} in range min: {min} and max: {max} ")
        else:
            # Type not found
            assert False, f"Data type {data_type} not found or data type no expected"
    
    def aux_fields_validator(self,current,valid):
        """
        Purpose: Validate values for the related fields
        :param current: source dictionary to validate
        :param valid: valid dictionary to compare 
        
        :return: None
        """
        # Check number of fields
        assert len(current) == len (valid), f"Current number of readed fields {current} differ from valid ones {valid}"

        for i in range(len(current)):
            key = list(current)[i]
            value = current[key]
            # Check order and names
            assert key == list(valid)[i], f"Actual: {current} field differs from expected one {valid}"

            data = valid[key]
            self.validate_value_on_constraint(value,data)

    def compare_constraints_list(self,list_constraints_from_ticket,list_expected_constraints_with_typo):
        """
        Purpose: Validate that constraints received from code are the expected
        :param list_constraints_from_ticket: constraints from ticket
        :param list_expected_constraints_with_typo: valid expected constrains with typo on first element of the array
        
        :return: None
        """

        if not("disabled" in list_constraints_from_ticket and list_constraints_from_ticket["disabled"]["value"] == "true"):
            data_type = list_expected_constraints_with_typo[0]
            if data_type == "String" or data_type == "Enum":
                for value in list_constraints_from_ticket['options']:
                    if not("disabled" in value and value["disabled"] == "true"):
                        self.validate_value_on_constraint(value["seValue"],list_expected_constraints_with_typo)

            elif data_type == "Double":
                self.validate_value_on_constraint(list_constraints_from_ticket["minDouble"]["value"],list_expected_constraints_with_typo)
                self.validate_value_on_constraint(list_constraints_from_ticket["maxDouble"]["value"],list_expected_constraints_with_typo)

            elif data_type == "Integer":
                self.validate_value_on_constraint(list_constraints_from_ticket["min"]["value"],list_expected_constraints_with_typo)
                self.validate_value_on_constraint(list_constraints_from_ticket["max"]["value"],list_expected_constraints_with_typo)