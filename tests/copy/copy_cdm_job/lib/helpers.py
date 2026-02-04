class Helpers:
    """class with helper functions for workflow tests"""

    def __init__(self):
        """Copy management class builder

        Args:
        """
        pass 

    def aux_get_valid_values_jupiter(self,which="all"):
        """
        Purpose: Return all possible field values for the related fields
        :param which: ("onlydefault"/"all") : String, indicates whether we want 
            only the default values or all. The default values are the first 
            value of each field (after the type). 
        
        :return: dictionary with full valid values for the fields or only the 
            default ones.
        """
        # Default values are the first one of each field
        valid_values_jupiter = {
            'outputCanvasMediaSize' :["String",
                                        "any",
                                        "custom",
                                        "iso_a0_841x1189mm",
                                        "iso_a1_594x841mm",
                                        "iso_a2_420x594mm",
                                        "iso_a3_297x420mm",
                                        "iso_a4_210x297mm",
                                        "iso_b0_1000x1414mm",
                                        "iso_b1_707x1000mm",
                                        "iso_b2_500x707mm",
                                        "iso_b3_353x500mm",
                                        "iso_b4_250x353mm",
                                        "na_arch-a_9x12in",
                                        "na_arch-b_12x18in",
                                        "na_arch-c_18x24in",
                                        "na_arch-d_24x36in",
                                        "na_arch-e_36x48in",
                                        "na_arch_a_9x12in",
                                        "na_arch_b_12x18in",
                                        "na_arch_c_18x24in",
                                        "na_arch_d_24x36in",
                                        "na_arch_e_36x48in",
                                        "na_letter_8.5x11in",
                                        "na_ledger_11x17in",
                                        "na_c_17x22in",
                                        "na_d_22x34in",
                                        "na_e_34x44in"
                                    ],
            'outputCanvasMediaId'   :["String",
                                        "auto",
                                        "roll_1",
                                        "roll_2",
                                        "roll-1",
                                        "roll-2"
                                    ],
            'outputCanvasCustomWidth'   :["Double",
                                        66,
                                        914
                                    ],
            'outputCanvasCustomLength'  :["Double",
                                        66,
                                        2377
                                    ],
            'outputCanvasAnchor'    :["Enum",
                                        "topLeft",
                                        "topCenter",
                                        "topRight",
                                        "middleLeft",
                                        "middleCenter",
                                        "middleRight",
                                        "bottomLeft",
                                        "bottomCenter",
                                        "bottomRight"
                                    ],
            'outputCanvasOrientation':["Enum",
                                        "portrait",
                                        "landscape"
                                    ],
            'backgroundColorRemoval':["Enum",
                                        "false",
                                        "true"
                                    ],
            'backgroundColorRemovalLevel':["Integer",
                                            -6,
                                            6
                                        ],
            'blackEnhancementLevel':["Integer",
                                        0,
                                        255
                                    ],
        }
        # default filtered values for each field
        if which == "onlydefault":
            for k,v in valid_values_jupiter.items():
                valid_values_jupiter[k] = v[0:2]
        return valid_values_jupiter

    def aux_filter_target_fields(self,current,default_values):
        """
        Purpose: Filter fields in a dictionary with other
        :param current: source dictionary
        
        :return: filtered dictionary with only present
            fields in other (valid_values in aux_get_valid_values).
        """
        filtered={}
        if current != {}:
            for k,v in default_values.items():
                filtered[k] = current[k]
        return filtered

    def find_constraint(self,constraints_json, constraint_path):
        """
        Purpose: find a specific constraint based on a constraint cdm path
        :param constraints_json: complete json dictionary with all constraints
        :param constraint_path: path to find the expected

        :return: Validator requested, or NONE if any constraint is found
        """
        for validator in constraints_json['validators'] :
            if validator['propertyPointer'] == constraint_path :
                return validator
        return None