from dunetuf.scan.ScanAction import ScanAction

"""
    Helpers class, mainly for parse tcl data related to scan counters
"""

class CounterHelpers:

    def __init__(self, tcl, udw, scanaction):
        self.tcl = tcl
        self.udw = udw
        self.scan_action = scanaction
        self.scan_action.set_udw(udw)
        self.scan_action.set_tcl(tcl)

    # Splits a string into a list from first_char appearance possition
    # Returns a list of elements
    def string_filter_helper(self, str, first_char):
        start_chr = (first_char)
        start = str.find(start_chr) + len (start_chr)
        substring = str[start:]
        splited_list = substring.replace(' ','').split (",")
        return splited_list

    # Recovers value from suplied counter "value" field 
    # Returns a filtered string with the value
    def value_filter_helper(self, str,filter_field="value"):
        start = str.find(filter_field) + len (filter_field)
        end =  str.find("}")
        substring = str[start:end]
        filtered_srt = substring.replace('"','').replace('\n','').replace(' ','')
        filter_field = ":"
        start = filtered_srt.find(filter_field) + len (filter_field)
        substring = filtered_srt[start:]
        return substring

    # Obtains all scan related counters using tcl
    # Returns a list of ID
    def get_all_scan_counters_by_tcl(self):
        tcl_result = self.scan_action.get_all_counters_ids_tcl(self.tcl)
        # Parse tcl result into a list 
        counter_list = self.string_filter_helper (tcl_result, ">")
        # Discard last element -> "(mainApp:9104)"
        counter_list.pop()
        # print ("La lista de contadores es: ",counter_list)
        return counter_list

    # Gets values for a list of counters
    # Returns a dictionary with key = counter id  and value = current value for that counter
    def get_all_scan_counters_values(self, counter_list):
        dict_counters_values ={}
        for counter in counter_list:
            counter_data = self.scan_action.get_counter_value_tcl(self.tcl, counter)
            value = self.value_filter_helper(counter_data)
            dict_counters_values[counter] = float(value)
        return dict_counters_values