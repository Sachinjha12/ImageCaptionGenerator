import logging
from time import sleep
from dunetuf.copy.copy import *
from dunetuf.job.job import Job


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: id copy ui color grayscale ui test
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-23144
    +timeout:250
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_idcopy_ui_flatbed_landingpage_color_grayscale
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:IDCopy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_idcopy_ui_flatbed_landingpage_color_grayscale
        +guid: d0d135e0-a3dc-4c68-b9fd-eb14ff722b03
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=IDCopy & ScannerInput=AutomaticDocumentFeeder & Copy=GrayScale
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_idcopy_ui_flatbed_landingpage_color_grayscale(cdm, spice, job, udw, net):
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'colorMode': 'Grayscale'
        }
        loadmedia='Flatbed'
        copy_path = 'IDCardLandingPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])

    finally:
        spice.goto_homescreen()
        spice.wait_ready()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: id copy ui color color ui test
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-23144
    +timeout:250
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_idcopy_ui_flatabed_landingpage_colormode_color
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:IDCopy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_idcopy_ui_flatabed_landingpage_colormode_color
        +guid: 09b283f1-89b3-41d7-87b0-58b6488255bb
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=IDCopy & ScannerInput=Flatbed & Copy=Color
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_idcopy_ui_flatabed_landingpage_colormode_color(cdm, spice, job, udw, net):
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'colorMode': 'Color'
        }
        loadmedia='Flatbed'
        copy_path = 'IDCardLandingPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])

    finally:
        spice.goto_homescreen()
        spice.wait_ready()


