from dunetuf.send.common import common


class Copy(object):
    """Copy manager class for basic copy management"""

    def __init__(self):
        """Copy management class builder

        Args:
            tcl: TCL instance
            cdm: CDM instance
            udw: UDW instance
            copy: Copy Class from dunetuf.copy.copy
        """
        self.tcl = None
        self.cdm = None
        self.udw = None
        self.copy = None

    """ SETTERS """

    def _set_tcl(self, tcl):
        """
        Set of TCL fixture

        Args:
            tcl: TCL instance

        Returns:
                self fixture
        """
        self.tcl = tcl
        return self

    def _set_cdm(self, cdm):
        """
        Set of CDM fixture

        Args:
            cdm: CDM instance

        Returns:
                self fixture
        """
        self.cdm = cdm
        return self

    def _set_udw(self, udw):
        """
        Set of UDW fixture

        Args:
            udw: UDW instance

        Returns:
                self fixture
        """
        self.udw = udw
        return self

    def _set_copy(self, copy):
        """
        Set of COPY fixture

        Args:
            copy: COPY instance

        Returns:
                self fixture
        """
        self.copy = copy
        return self

    """ ACTIONS """

    def create_run_configuration_copy(self, settings):
        """
        Create and run configuration copy

        Args:
            settings: configuration parameter copy 
        """ 
        payload = {
            "src":{settings["src"]:{"colorMode":settings["color_mode"], "resolution":settings["resolution"]}},
            "dest":{settings["dest"]:{"copies":settings["copies"]}}                   
        } 
        self.copy.do_copy_job(**payload)
