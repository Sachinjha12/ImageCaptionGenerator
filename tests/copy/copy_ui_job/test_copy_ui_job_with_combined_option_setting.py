import logging
import time

from dunetuf.copy.copy import *

def check_duplex_support(cdm):
    response = cdm.get(cdm.SCAN_STATUS_ENDPOINT)
    if(response['adf']['duplexSupported'] == 'false'):
        return False
    return True

def enable_duplex_supported(cdm,udw):
    udw.mainApp.ScanMedia.unloadMedia("ADF")
    udw.mainApp.ScanCapabilities.setHasDuplexSupport(True)
    result = check_duplex_support(cdm)
    assert result == True
    udw.mainApp.ScanMedia.loadMedia("ADF")

def disable_duplex_supported(cdm,udw):
    udw.mainApp.ScanMedia.unloadMedia("ADF")
    udw.mainApp.ScanCapabilities.setHasDuplexSupport(False)
    result = check_duplex_support(cdm)
    assert result == False
    udw.mainApp.ScanMedia.loadMedia("ADF")

def check_duplex_support(cdm):
    response = cdm.get(cdm.SCAN_STATUS_ENDPOINT)
    if(response['adf']['duplexSupported'] == 'false'):
        return False
    return True

def enable_duplex_supported(cdm,udw):
    udw.mainApp.ScanMedia.unloadMedia("ADF")
    udw.mainApp.ScanCapabilities.setHasDuplexSupport(True)
    result = check_duplex_support(cdm)
    assert result == True
    udw.mainApp.ScanMedia.loadMedia("ADF")

def disable_duplex_supported(cdm,udw):
    udw.mainApp.ScanMedia.unloadMedia("ADF")
    udw.mainApp.ScanCapabilities.setHasDuplexSupport(False)
    result = check_duplex_support(cdm)
    assert result == False
    udw.mainApp.ScanMedia.loadMedia("ADF")
