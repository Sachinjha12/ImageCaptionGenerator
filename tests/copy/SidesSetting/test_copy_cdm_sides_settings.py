from dunetuf.copy.copy import *
from dunetuf.job.job import Job
from dunetuf.ssh import SSH

import pytest

payload = {
            'src': {
                'scan': {
                    'mediaSize':'na_letter_8.5x11in',
                    'plexMode':'simplex',
                    'resolution':'e300Dpi',
                },
            },
            'dest': {
                'print': {
                    'copies': 10,
                    'mediaSize':'na_letter_8.5x11in',
                    'plexMode':'simplex',
                }
            }
        }

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-32173
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_flatbedduplex_using_cdm
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test: 
        +title: test_copy_flatbedduplex_using_cdm
        +guid:c825bec5-d436-47c2-bb58-231a5eb74d77
        +dut: 
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_flatbedduplex_using_cdm(cdm, udw, media, configuration):
    udw.mainApp.ScanMedia.unloadMedia("ADF")
    payload = {
            'src': {
                'scan': {
                    'mediaSize':'na_letter_8.5x11in',
                    'plexMode':'duplex',
                    'mediaSource':'flatbed',
                },
            },
            'dest': {
                'print': {
                    'copies': 1,
                    'mediaSize':'na_letter_8.5x11in',
                    'plexMode':'duplex',
                }
            }
        }
    job_id = Copy(cdm, udw).start_copy_job(familyname = configuration.familyname,**payload)
    job = Job(cdm, udw)
    if configuration.familyname != "enterprise":
        job.wait_for_alerts('scanManualDuplexSecondPage')
        job.alert_action('scanManualDuplexSecondPage', 'Response_01')
    else:
        job.wait_for_alerts('flatbedAddPage')
        job.alert_action('flatbedAddPage', 'Response_02')
    job.check_job_state(job_id, 'completed', 60)
    udw.mainApp.ScanMedia.loadMedia("ADF")
    print('Completed Job Id : {}'.format(job_id))

    print('========== COPY Job Completed ==========')

    print('Copy Job completed. Removing possible generated output file.')
    SSH(cdm.ipaddress).run('rm -f /tmp/PUID_*.tiff')

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Simple copy job
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-9875
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_simple_job_adf_duplex_using_cdm
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_simple_job_adf_duplex_using_cdm
        +guid: 40d92ab4-a001-440d-9911-b355bbb50285
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""


def test_copy_simple_job_adf_duplex_using_cdm(cdm, udw,scan_emulation):
    scan_emulation.media.load_media('ADF',1)
    payload['src']['scan']['plexMode'] = 'duplex'
    Copy(cdm, udw).do_copy_job(**payload)

    payload['src']['scan']['plexMode'] = 'simplex'
    scan_emulation.media.unload_media('ADF')

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Simple copy job
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-9875
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_simple__adf_simplex_using_cdm
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_simple__adf_simplex_using_cdm
        +guid: 191e96e0-8b79-427a-9b87-cd77871cd74e
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder
            
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""


def test_copy_simple__adf_simplex_using_cdm(cdm, udw, scan_emulation):
    scan_emulation.media.load_media('ADF',1)
    Copy(cdm, udw).do_copy_job(**payload)
    scan_emulation.media.unload_media('ADF')

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Simple copy job
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-9875
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy__simple_flatbed_using_cdm
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy__simple_flatbed_using_cdm
        +guid: 3475b8e2-fdbc-4547-a7d4-0fb6eff5ef06
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed
            
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""


def test_copy__simple_flatbed_using_cdm(cdm, udw, scan_emulation):
    scan_emulation.media.unload_media('ADF')
    Copy(cdm, udw).do_copy_job(**payload)
    scan_emulation.media.load_media('ADF',1)

