import copy
from dunetuf.copy.copy import Copy
from tests.copy.quicksets.copy_common import *
from tests.copy.quicksets.copy_combination import *
from tests.send.quicksets.quicksets_common import get_local_time
from tests.copy.quicksets.quickset_combination import *
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds
from dunetuf.ews.quicksets import Quicksets
from dunetuf.cdm.CdmShortcuts import CDMShortcuts
from dunetuf.job.job import Job
import logging
import uuid
_logger = logging.getLogger(__name__)


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Home->Copy APP, perform copy job with created quickset.
    +test_tier:3
    +is_manual: False
    +reqid:DUNE-28198
    +timeout:420
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_home_copyapp_combi1
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_home_copyapp_combi1
        +guid:b7d82c48-145f-499e-93b8-5bbe5c0ee60b
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy &ScannerInput=AutomaticDocumentFeeder & ADFMediaSize=Letter & ScanContentType=Auto & ScanColorMode=Automatic & ScanSettings=LighterDarker & ADFMediaSize=A4Landscape & Copy=2PagesPerSheet & Copy=2Sided1To2 & Copy=2SidedFormatFlip & Copy=Collation & Copy=NumberOfCopies & Copy=PaperSize & Copy=PaperType & Copy=PaperTray
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_home_copyapp_combi1(setup_teardown_quickset, spice, ews, job, cdm, net, tray):
    """
    quickset_copy_common_combi1 = lambda: {
    "original_size": "letter_8.5x11in", # value from key of copy_original_size_option_dict
    "content_type": "automatic", # value from key of copy_content_type_option_dict
    "color_mode": "automatic", # value from key of copy_color_mode_option_dict
    "lighter_darker": 5, # int [1-9]
    "number_of_copies" : 1, # int [1-999]
    "output_scale" : "fit_to_page", # value from key of copy_output_scale_option_dict
    "paper_size" : "a4_210x297_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "plain", # value from key of copy_paper_type_option_dict
    "paper_tray" : "automatic", # value from key of copy_paper_tray_option_dict
    "quality" : "best", # value from key of copy_file_quality_option_dict
    "sides" : "1_to_2_sided", # value from key of copy_sides_option_dict
    "pages_per_sheet" : "one", # value from key of copy_pagesper_sheet_option_dict
    "two_sided_pages_flip_up" : True, # True/False
    "collate" : True # True/False
    }
    """
    default_tray = tray.get_default_source()
    tray.configure_tray(default_tray, 'iso_a4_210x297mm', 'stationery')
    quickset_copy_setting = {
        "name" : "copy_quickset_combi1",
        "start_option": "user presses start", # value from key of start_option_dict
        }

    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi1())
    spice.quickset_ui.perform_quickset_job_from_home_app(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Menu->Quickset APP, perform copy job with created quickset.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:720
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi2
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi2
        +guid:db35e03f-0e36-4402-91d0-288dc1678ece
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy &ScannerInput=AutomaticDocumentFeeder & ScanContentType=Lines & ADFMediaSize=A4Landscape & Copy=2Sided2To1 & Copy=2SidedFormatFlip & Copy=Collation & Copy=NumberOfCopies & Copy=PaperSize
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi2(setup_teardown_quickset, spice, ews, job, cdm, net, tray):
    """
    quickset_copy_common_combi2 = lambda: {
    "content_type": "line", # value from key of copy_content_type_option_dict
    "number_of_copies" : 5, # int [1-999]
    "output_scale" : "None", # value from key of copy_output_scale_option_dict
    "paper_size" : "a4_210x297_mm", # value from key of copy_paper_size_option_dict
    "quality" : "standard", # value from key of copy_file_quality_option_dict
    "sides" : "2_to_1_sided", # value from key of copy_sides_option_dict
    "two_sided_pages_flip_up" : True, # True/False
    "collate" : False # True/False
    }
    """
    default_tray = tray.get_default_source()
    tray.configure_tray(default_tray, 'iso_a4_210x297mm', 'stationery')

    quickset_copy_setting = {
        "name" : "copy_quickset_combi2",
        "start_option": "user presses start", # value from key of start_option_dict
        }
    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi2())
    spice.quickset_ui.perform_quickset_job_from_menu_quicksetapp(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Menu->Copy APP, perform copy job with created quickset.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:720
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_menu_copyapp_combi3
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_menu_copyapp_combi3
        +guid:8b0559b0-65ae-4003-b699-08f0b019483e
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScanContentType=Mixed & ScannerInput=AutomaticDocumentFeeder & Copy=2Sided2To2 & Copy=Collation & ADFMediaSize=A4Landscape & Copy=2SidedFormatFlip & Copy=NumberOfCopies & Copy=PaperSize
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_menu_copyapp_combi3(setup_teardown_quickset, spice, ews, job, cdm, net, udw, tray):
    """
    quickset_copy_common_combi3 = {
    "content_type": "mixed", # value from key of copy_content_type_option_dict
    "number_of_copies" : 99, # int [1-999]
    "paper_size" : "a4_210x297_mm", # value from key of copy_paper_size_option_dict
    "quality" : "draft", # value from key of copy_file_quality_option_dict
    "sides" : "2_to_2_sided", # value from key of copy_sides_option_dict
    "two_sided_pages_flip_up" : True, # True/False
    "collate" : False # True/False
    }
    """
    default_tray = tray.get_default_source()
    if tray.is_size_supported('iso_a4_210x297mm', default_tray):
        tray.configure_tray(default_tray, 'iso_a4_210x297mm', 'stationery')
    spice.copy_ui().enable_duplex_supported(cdm,udw)
    quickset_copy_setting = {
        "name" : "copy_quickset_combi3",
        "start_option": "user presses start", # value from key of start_option_dict
        }
    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi3())
    spice.quickset_ui.perform_quickset_job_from_menu_app(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Menu->QuickSet APP, perform copy job with created quickset.
    +test_tier:3
    +is_manual: False
    +reqid:DUNE-28198
    +timeout:420
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi4
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi4
        +guid:22ec28bb-a1f8-4aff-888d-957d113f4206
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScanContentType=Text & ADFMediaSize=A4Landscape & Copy=NumberOfCopies & Copy=PaperSize & EWS=Quicksets
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi4(setup_teardown_quickset, spice, ews, job, cdm, net, tray):
    """
    combi4 custom settings:
    quickset_copy_common_combi4 = {
    "content_type": "text", # value from key of copy_content_type_option_dict
    "number_of_copies" : 10, # int [1-999]
    "paper_size" : "a4_210x297_mm", # value from key of copy_paper_size_option_dict
    "quality" : "draft", # value from key of copy_file_quality_option_dict
    }
    """
    default_tray = tray.get_default_source()
    if tray.is_size_supported('iso_a4_210x297mm', default_tray):
        tray.configure_tray(default_tray, 'iso_a4_210x297mm', 'stationery')

    quickset_copy_setting = {
        "name" : "copy_quickset_combi4",
        "start_option": "user presses start", # value from key of start_option_dict
        }
    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi4())
    spice.quickset_ui.perform_quickset_job_from_menu_quicksetapp(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Home->Copy APP, perform copy job with created quickset.
    +test_tier:3
    +is_manual: False
    +reqid:DUNE-28198
    +timeout:420
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_home_copyapp_combi5
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_home_copyapp_combi5
        +guid:7c22465d-8b79-4957-84d8-fe6b9cf7f853
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScanContentType=Image & ADFMediaSize=A4Landscape & Copy=PaperSize & Copy=Quality
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_home_copyapp_combi5(setup_teardown_quickset, spice, ews, job, cdm, net, tray):
    """
    quickset_copy_common_combi5 = lambda: {
    "content_type": "image", # value from key of copy_content_type_option_dict
    "paper_size" : "a4_210x297_mm", # value from key of copy_paper_size_option_dict
    "quality" : "standard", # value from key of copy_file_quality_option_dict
    }
    """
    default_tray = tray.get_default_source()
    tray.configure_tray(default_tray, 'iso_a4_210x297mm', 'stationery')
    quickset_copy_setting = {
        "name" : "copy_quickset_combi5",
        "start_option": "user presses start", # value from key of start_option_dict
        }

    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi5())
    spice.quickset_ui.perform_quickset_job_from_home_app(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Home->Copy APP, perform copy job with created quickset.
    +test_tier:3
    +is_manual: False
    +reqid:DUNE-28198
    +timeout:360
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_home_copyapp_combi6
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_home_copyapp_combi6
        +guid:b71006d6-e523-4717-8176-40882558febc
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScanContentType=Photograph & ADFMediaSize=A4Landscape & Copy=PaperSize & Copy=PaperType & EWS=Quicksets & Copy=Quality
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_home_copyapp_combi6(setup_teardown_quickset, spice, ews, job, cdm, net, tray):
    """
    combi5 custom settings:
    quickset_copy_common_combi6 = {
    "content_type": "photograph", # value from key of copy_content_type_option_dict
    "paper_size" : "a4_210x297_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "hp_ecofficient", # value from key of copy_paper_type_option_dict
    "quality" : "best", # value from key of copy_file_quality_option_dict
    }
    """
    default_tray = tray.get_default_source()
    tray.configure_tray(default_tray, 'iso_a4_210x297mm', 'com.hp.EcoSMARTLite')
    quickset_copy_setting = {
        "name" : "copy_quickset_combi6",
        "start_option": "user presses start", # value from key of start_option_dict
        }

    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi6())

    spice.quickset_ui.perform_quickset_job_from_home_app(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Menu->QuickSet APP, perform copy job with created quickset with auto select start option job.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:400
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_one_touch_combi7
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_one_touch_combi7
        +guid:11ba4e0a-6251-4cbd-82f7-5d75cf86badd
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScanContentType=Photograph & ADFMediaSize=A4Landscape & ScanColorMode=Color & MediaInputInstalled=Tray2 & Copy=PaperSize & Copy=PaperType & Copy=PaperTray
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_menu_quicksetapp_one_touch_combi7(setup_teardown_quickset, spice, ews, job, cdm, net, tray):
    """
    quickset_copy_common_combi7 = lambda: {
    "color_mode": "color", # value from key of copy_color_mode_option_dict
    "paper_size" : "a4_210x297_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "hp_matte_90g", # value from key of copy_paper_type_option_dict
    "paper_tray" : "tray2", # value from key of copy_paper_tray_option_dict
    }
    """
    tray.configure_tray('tray-2', 'iso_a4_210x297mm', 'com.hp.matte-90gsm')
    quickset_copy_setting = {
        "name" : "copy_quickset_combi7",
        "start_option": "start automatically", # value from key of start_option_dict
        }
    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi7())
    spice.quickset_ui.perform_quickset_job_from_menu_quicksetapp(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Home->Copy APP, perform copy job with created quickset.
    +test_tier:3
    +is_manual: False
    +reqid:DUNE-28198
    +timeout:360
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_home_copyapp_combi8
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_home_copyapp_combi8
        +guid:15f68743-6738-483f-a490-87b96b4531d6
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ADFMediaSize=A4Landscape & ScanColorMode=GrayScale & MediaInputInstalled=Tray1 & Copy=PaperSize & Copy=PaperType & Copy=PaperTray
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_home_copyapp_combi8(setup_teardown_quickset, spice, ews, job, cdm, net, tray):
    """
    quickset_copy_common_combi8 = lambda: {
    "color_mode": "grayscale", # value from key of copy_color_mode_option_dict
    "paper_size" : "a4_210x297_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "hp_matte_105g", # value from key of copy_paper_type_option_dict
    "paper_tray" : "tray1", # value from key of copy_paper_tray_option_dict
    }
    """
    tray.configure_tray('tray-1', 'iso_a4_210x297mm', 'com.hp.matte-105gsm')
    quickset_copy_setting = {
        "name" : "copy_quickset_combi8",
        "start_option": "user presses start", # value from key of start_option_dict
        }
    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi8())
    spice.quickset_ui.perform_quickset_job_from_home_app(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Menu->QuickSet APP, perform copy job with created quickset.
    +test_tier:3
    +is_manual: False
    +reqid:DUNE-28198
    +timeout:300
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi9
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi9
        +guid:0a8ede11-afae-4329-a3f7-d383b31f258b
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScanColorMode=BlackOnly & ADFMediaSize=A4Landscape & MediaInputInstalled=Tray3 & Copy=PaperSize & Copy=PaperType & Copy=PaperTray
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi9(setup_teardown_quickset, spice, ews, job, cdm, net, tray):
    """
    quickset_copy_common_combi9 = lambda: {
    "color_mode": "blackonly", # value from key of copy_color_mode_option_dict
    "paper_size" : "a4_210x297_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "hp_matte_120g", # value from key of copy_paper_type_option_dict
    "paper_tray" : "tray3", # value from key of copy_paper_tray_option_dict
    }
    """
    tray.configure_tray('tray-3', 'iso_a4_210x297mm', 'com.hp.matte-120gsm')
    quickset_copy_setting = {
        "name" : "copy_quickset_combi9",
        "start_option": "user presses start", # value from key of start_option_dict
        }
    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi9())
    spice.quickset_ui.perform_quickset_job_from_menu_quicksetapp(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Menu->Copy APP, perform copy job with created quickset.
    +test_tier:3
    +is_manual: False
    +reqid:DUNE-28198
    +timeout:360
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_menu_copyapp_combi10
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_menu_copyapp_combi10
        +guid:a2bec009-1c1b-44e1-a01b-6e7c79e4536d
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ADFMediaSize=Legal & ADFMediaSize=A4Landscape & MediaInputInstalled=Tray1 & ScanSettings=LighterDarker & Copy=PaperSize & Copy=PaperType & Copy=PaperTray
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_menu_copyapp_combi10(setup_teardown_quickset, spice, ews, job, cdm, net, tray):
    """
    quickset_copy_common_combi10 = lambda: {
    "original_size": "legal_8.5x14in", # value from key of copy_original_size_option_dict
    "lighter_darker": 1, # int [1-9]
    "paper_size" : "a4_210x297_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "hp_matte_150g", # value from key of copy_paper_type_option_dict
    "paper_tray" : "tray1", # value from key of copy_paper_tray_option_dict
    }
    """
    tray.configure_tray("tray-1", 'iso_a4_210x297mm', 'com.hp.matte-160gsm')

    quickset_copy_setting = {
        "name" : "copy_quickset_combi10",
        "start_option": "user presses start", # value from key of start_option_dict
        }
    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi10())
    spice.quickset_ui.perform_quickset_job_from_menu_app(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Menu->Quickset APP, perform copy job with created quickset.
    +test_tier:3
    +is_manual: False
    +reqid:DUNE-28198
    +timeout:460
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi11
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi11
        +guid:969b4558-20c6-4be7-955e-63ff7bb19b2c
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ADFMediaSize=Executive & ADFMediaSize=A4Landscape & ScanSettings=LighterDarker & Copy=2PagesPerSheet & Copy=PaperSize & Copy=PaperType
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi11(setup_teardown_quickset, spice, ews, job, cdm, net, tray):
    """
    quickset_copy_common_combi11 = lambda: {
    "original_size": "executive_7.25x10.5in", # value from key of copy_original_size_option_dict
    "lighter_darker": 9, # int [1-9]
    "paper_size" : "a4_210x297_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "hp_matte_200g", # value from key of copy_paper_type_option_dict
    "pages_per_sheet" : "two", # value from key of copy_pagesper_sheet_option_dict
    }
    """
    default_tray = tray.get_default_source()
    tray.configure_tray(default_tray, 'iso_a4_210x297mm', 'com.hp.matte-200gsm')

    quickset_copy_setting = {
        "name" : "copy_quickset_combi11",
        "start_option": "user presses start", # value from key of start_option_dict
        }
    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi11())
    spice.quickset_ui.perform_quickset_job_from_menu_quicksetapp(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Menu->Quickset APP, perform copy job with created quickset with auto select start option job.
    +test_tier:3
    +is_manual: False
    +reqid:DUNE-28198
    +timeout:360
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_auto_start_combi12
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_auto_start_combi12
        +guid:56db86ae-f1ec-4650-87f7-58aef56c1f94
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & MediaType=HPPremiumPresentationGlossy120g & ADFMediaSize=Oficio216x340mm & ScanSettings=LighterDarker & ADFMediaSize=A4Landscape & Copy=ResizeCustom & Copy=PaperSize & Copy=PaperType
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_menu_quicksetapp_auto_start_combi12(setup_teardown_quickset, spice, ews, job, cdm, net, tray):
    """
    quickset_copy_common_combi12 = lambda: {
    "original_size": "oficio_8.5x13in", # value from key of copy_original_size_option_dict
    "lighter_darker": 6, # int [1-9]
    "paper_size" : "a4_210x297_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "hp_glossy_120g", # value from key of copy_paper_type_option_dict
    "output_scale" : "custom", # value from key of copy_output_scale_option_dict
    }
    """
    default_tray = tray.get_default_source()
    tray.configure_tray(default_tray, 'iso_a4_210x297mm', 'com.hp.glossy-130gsm')

    quickset_copy_setting = {
        "name" : "copy_quickset_combi12",
        "start_option": "start automatically", # value from key of start_option_dict
        }
    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi12())
    spice.quickset_ui.perform_quickset_job_from_menu_quicksetapp(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Menu->Quickset APP, perform copy job with created quickset job.
    +test_tier:3
    +is_manual: False
    +reqid:DUNE-28198
    +timeout:360
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi13
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi13
        +guid:571ecf08-7068-4c05-b56b-12fef1129ca0
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & MediaType=HPBrochureGlossy150g & ADFMediaSize=5x8 & ScanSettings=LighterDarker & ADFMediaSize=A4Landscape & Copy=ResizeCustom & Copy=PaperSize & Copy=PaperType
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi13(setup_teardown_quickset, spice, ews, job, cdm, net, tray):
    """
    quickset_copy_common_combi13 = lambda: {
    "original_size": "5x8in", # value from key of copy_original_size_option_dict
    "paper_size" : "a4_210x297_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "hp_glossy_150g", # value from key of copy_paper_type_option_dict
    "output_scale" : "custom", # value from key of copy_output_scale_option_dict
    "precise_scaling_amount": "25" # value for custom output_scale, string[25% - 400%]
    }
    """
    default_tray = tray.get_default_source()
    tray.configure_tray(default_tray, 'iso_a4_210x297mm', 'com.hp.glossy-160gsm')

    quickset_copy_setting = {
        "name" : "copy_quickset_combi13",
        "start_option": "user presses start", # value from key of start_option_dict
        }
    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi13())
    spice.quickset_ui.perform_quickset_job_from_menu_quicksetapp(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Menu->Copy APP, perform copy job with created quickset.
    +test_tier:3
    +is_manual: False
    +reqid:DUNE-28198
    +timeout:360
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_menu_copyapp_combi14
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_menu_copyapp_combi14
        +guid:d6322e2f-ab49-49bf-8b34-bcc389141171
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ADFMediaSize=A4 & ADFMediaSize=A4Landscape & Copy=ResizeCustom & Copy=PaperSize & Copy=PaperType & MediaType=HPBrochureGlossy200g
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_menu_copyapp_combi14(setup_teardown_quickset, spice, ews, job, cdm, net, tray):
    """
    quickset_copy_common_combi14 = lambda: {
    "original_size": "a4_210x297_mm", # value from key of copy_original_size_option_dict
    "paper_size" : "a4_210x297_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "hp_glossy_200g", # value from key of copy_paper_type_option_dict
    "output_scale" : "custom", # value from key of copy_output_scale_option_dict
    "precise_scaling_amount": "400" # value for custom output_scale, string[25% - 400%]
    }
    """
    default_tray = tray.get_default_source()
    tray.configure_tray(default_tray, 'iso_a4_210x297mm', 'com.hp.glossy-220gsm')

    quickset_copy_setting = {
        "name" : "copy_quickset_combi14",
        "start_option": "user presses start", # value from key of start_option_dict
        }
    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi14())
    spice.quickset_ui.perform_quickset_job_from_menu_app(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Home->Copy APP, perform copy job with created quickset.
    +test_tier:3
    +is_manual: False
    +reqid:DUNE-28198
    +timeout:360
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_home_copyapp_combi15
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_home_copyapp_combi15
        +guid:133d090c-7ad5-4512-b798-6a0854fc08fd
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ADFMediaSize=A5 & Copy=PaperSize & Copy=PaperType & MediaType=HPTri-foldBrochureGlossy150g
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_home_copyapp_combi15(setup_teardown_quickset, spice, ews, job, cdm, net, tray):
    """
    quickset_copy_common_combi15 = lambda: {
    "original_size": "a5_148x210_mm", # value from key of copy_original_size_option_dict
    "paper_size" : "a4_210x297_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "hp_trifold_glossy", # value from key of copy_paper_type_option_dict
    "output_scale" : "custom", # value from key of copy_output_scale_option_dict
}
    """
    default_tray = tray.get_default_source()
    tray.configure_tray(default_tray, 'iso_a4_210x297mm', 'com.hp-trifold-brochure-glossy-150gsm')
    quickset_copy_setting = {
        "name" : "copy_quickset_combi15",
        "start_option": "user presses start", # value from key of start_option_dict
        }
    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi15())
    spice.quickset_ui.perform_quickset_job_from_home_app(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Menu->Quickset APP, perform copy job with created quickset with auto select start option job.
    +test_tier:3
    +is_manual: False
    +reqid:DUNE-28198
    +timeout:400
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_auto_start_combi16
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_auto_start_combi16
        +guid:c8766df8-4f5c-4d05-9823-1f0efd78328e
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & MediaType=Plain & DeviceFunction=Copy & ADFMediaSize=B5-JIS & Copy=PaperSize & Copy=PaperType
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_menu_quicksetapp_auto_start_combi16(setup_teardown_quickset, spice, ews, job, cdm, net, tray):
    """
    quickset_copy_common_combi16 = lambda: {
    "original_size": "b5_jis", # value from key of copy_original_size_option_dict
    "paper_size" : "a4_210x297_mm", # value from key of copy_paper_size_option_dict
    "pages_per_sheet" : "one", # value from key of copy_pagesper_sheet_option_dict
    "paper_type" : "light", # value from key of copy_paper_type_option_dict
    "output_scale" : "custom", # value from key of copy_output_scale_option_dict
}
    """
    default_tray = tray.get_default_source()
    tray.configure_tray(default_tray, 'iso_a4_210x297mm', 'stationery-lightweight')

    quickset_copy_setting = {
        "name" : "copy_quickset_combi16",
        "start_option": "start automatically", # value from key of start_option_dict
        }
    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi16())
    spice.quickset_ui.perform_quickset_job_from_menu_quicksetapp(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Menu->Copy APP, perform copy job with created quickset job.
    +test_tier:3
    +is_manual: False
    +reqid:DUNE-28198
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_menu_copyapp_combi17
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_menu_copyapp_combi17
        +guid:8226de3e-9ef9-4d96-bf8d-34b7e652a342
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ADFMediaSize=B6-JIS & Copy=PaperSize & Copy=PaperType & MediaType=Intermediate85-95g
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_menu_copyapp_combi17(setup_teardown_quickset, spice, ews, job, cdm, net, tray):
    """
    quickset_copy_common_combi17 = lambda: {
    "original_size": "b6_jis_128x182_mm", # value from key of copy_original_size_option_dict
    "paper_size" : "a4_210x297_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "intermediate", # value from key of copy_paper_type_option_dict
    "output_scale" : "custom", # value from key of copy_output_scale_option_dict
}
    """
    default_tray = tray.get_default_source()
    tray.configure_tray(default_tray, 'iso_a4_210x297mm', 'com.hp.intermediate')
    quickset_copy_setting = {
        "name" : "copy_quickset_combi17",
        "start_option": "user presses start", # value from key of start_option_dict
        }
    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi17())
    spice.quickset_ui.perform_quickset_job_from_menu_app(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Menu->Quickset APP, perform copy job with created quickset with auto select start option job.
    +test_tier:3
    +is_manual: False
    +reqid:DUNE-28198
    +timeout:400
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_auto_start_combi18
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_auto_start_combi18
        +guid:decdcba4-c495-4ee9-b891-820df5f532f2
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & MediaType=PlainPaper-Thick & ADFMediaSize=Oficio216x340mm & Copy=PaperSize & Copy=PaperType
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_menu_quicksetapp_auto_start_combi18(setup_teardown_quickset, spice, ews, job, cdm, net, tray):
    """
    quickset_copy_common_combi18 = lambda: {
    "original_size": "oficio_216x340_mm", # value from key of copy_original_size_option_dict
    "paper_size" : "a4_210x297_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "midweight", # value from key of copy_paper_type_option_dict
    "output_scale" : "custom", # value from key of copy_output_scale_option_dict
}
    """
    default_tray = tray.get_default_source()
    tray.configure_tray(default_tray, 'iso_a4_210x297mm', 'com.hp.midweight')
    quickset_copy_setting = {
        "name" : "copy_quickset_combi18",
        "start_option": "start automatically", # value from key of start_option_dict
        }
    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi18())
    spice.quickset_ui.perform_quickset_job_from_menu_quicksetapp(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()
    
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Home->Copy APP, perform copy job with created quickset.
    +test_tier:3
    +is_manual: False
    +reqid:DUNE-28198
    +timeout:360
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_home_copyapp_combi19
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_home_copyapp_combi19
        +guid:cab3563e-5b74-49ae-a426-024a681ec62f
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ADFMediaSize=16K195x270mm & Copy=PaperSize & MediaType=PlainPaper-Thick & EWS=Quicksets
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_home_copyapp_combi19(setup_teardown_quickset, spice, ews, job, cdm, net, tray, udw):
    """
    quickset_copy_common_combi19 = lambda: {
    "original_size": "16k_195x270_mm", # value from key of copy_original_size_option_dict
    "paper_size" : "a4_210x297_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "heavy", # value from key of copy_paper_type_option_dict
    }
    """
    udw.mainApp.ScanMedia.loadMedia("ADF")
    default_tray = tray.get_default_source()
    tray.configure_tray(default_tray, 'iso_a4_210x297mm', 'stationery-heavyweight')
    quickset_copy_setting = {
        "name" : "copy_quickset_combi19",
        "start_option": "user presses start", # value from key of start_option_dict
        }
    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi19())
    spice.quickset_ui.perform_quickset_job_from_home_app(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Menu->Quickset APP, perform copy job with created quickset.
    +test_tier:3
    +is_manual: False
    +reqid:DUNE-28198
    +timeout:360
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi20
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi20
        +guid:8f67baa3-f72f-4523-bca6-ff1e106f66f1
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & MediaType=ExtraHeavy131-175g & ADFMediaSize=16K184x260mm & Copy=PaperSize & Copy=PaperType
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi20(setup_teardown_quickset, spice, ews, job, cdm, net, tray):
    """
    quickset_copy_common_combi20 = lambda: {
    "original_size": "16k_184x260_mm", # value from key of copy_original_size_option_dict
    "paper_size" : "a4_210x297_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "extra_heavy", # value from key of copy_paper_type_option_dict
    }
    """
    default_tray = tray.get_default_source()
    tray.configure_tray(default_tray, 'iso_a4_210x297mm', 'com.hp.extra-heavy')
    quickset_copy_setting = {
        "name" : "copy_quickset_combi20",
        "start_option": "user presses start", # value from key of start_option_dict
        }
    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi20())
    spice.quickset_ui.perform_quickset_job_from_menu_quicksetapp(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Home->Copy APP, perform copy job with created quickset.
    +test_tier:3
    +is_manual: False
    +reqid:DUNE-28198
    +timeout:360
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_home_copyapp_combi21
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_home_copyapp_combi21
        +guid:aab93d2e-1848-468f-a761-aeaf139f33e6
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & MediaType=HeavyGlossy111-130g & DeviceFunction=Copy & ADFMediaSize=Letter & Copy=PaperSize & Copy=PaperType
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_home_copyapp_combi21(setup_teardown_quickset, spice, ews, job, cdm, net, tray):
    """
    quickset_copy_common_combi21 = lambda: {
    "original_size": "16k_197x273_mm", # value from key of copy_original_size_option_dict
    "paper_size" : "letter_8.5x11in", # value from key of copy_paper_size_option_dict
    "paper_type" : "heavy_glossy", # value from key of copy_paper_type_option_dict
    }
    """
    default_tray = tray.get_default_source()
    tray.configure_tray(default_tray, 'na_letter_8.5x11in', 'com.hp.heavy-glossy')
    quickset_copy_setting = {
        "name" : "copy_quickset_combi21",
        "start_option": "user presses start", # value from key of start_option_dict
        }
    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi21())
    spice.quickset_ui.perform_quickset_job_from_home_app(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Menu->Copy APP, perform different settings copy quickset job.
    +test_tier: 3
    +is_manual: False
    +reqid:DUNE-28198
    +timeout:360
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_menu_copyapp_combi22
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_menu_copyapp_combi22
        +guid:e86bec4e-052a-4ea7-9bdc-c93c8c7b2017
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ADFMediaSize=DoubleJapanPostcardRotated & ADFMediaSize=Legal & Copy=PaperSize & Copy=PaperType & MediaSizeSupported=na_legal_8.5x14in & MediaType=ExtraHeavyGlossy131-175g
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_menu_copyapp_combi22(setup_teardown_quickset, setup_teardown_flatbed, spice, ews, job, cdm, net, udw, tray):
    """
    quickset_copy_common_combi22 = lambda: {
    "original_size": "double_postcard_jis", # value from key of copy_original_size_option_dict
    "paper_size" : "legal_8.5x14in", # value from key of copy_paper_size_option_dict
    "paper_type" : "extra_heavy_glossy", # value from key of copy_paper_type_option_dict
    }
    """
    udw.mainApp.ScanMedia.loadMedia("ADF")
    default_tray = tray.get_default_source()
    if tray.is_size_supported('na_legal_8.5x14in', default_tray):
        tray.configure_tray(default_tray, 'na_legal_8.5x14in', 'com.hp.extra-heavy-gloss')

    #According to DUNE-94637, 2_to_1_sided/2_to_2_sided options only support on Flatbed.
    quickset_copy_setting = {
        "name" : "copy_quickset_combi22",
        "start_option": "user presses start", # value from key of start_option_dict
        }
    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi22())
    spice.quickset_ui.perform_quickset_job_from_menu_app(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()
    udw.mainApp.ScanMedia.unloadMedia("ADF")


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Menu->QuickSet APP, perform different settings copy quickset job.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:360
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi23
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi23
        +guid:ec195bfe-4e3e-4bf0-8372-4d3e3684aeb2
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & MediaType=CardGlossy176-220g & ADFMediaSize=Statement & ADFMediaSize=Executive & Copy=PaperSize & Copy=PaperType
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi23(setup_teardown_quickset, spice, ews, job, cdm, net, tray):
    """
    quickset_copy_common_combi23 = lambda: {
    "original_size": "statement_8.5x5.5in", # value from key of copy_original_size_option_dict
    "paper_size" : "executive_7_25x10_5in", # value from key of copy_paper_size_option_dict
    "paper_type" : "cardstock_glossy", # value from key of copy_paper_type_option_dict
    }
    """
    default_tray = tray.get_default_source()
    if tray.is_size_supported('na_executive_7.25x10.5in', default_tray):
        tray.configure_tray(default_tray, 'na_executive_7.25x10.5in', 'com.hp.cardstock-glossy')

    quickset_copy_setting = {
        "name" : "copy_quickset_combi23",
        "start_option": "user presses start", # value from key of start_option_dict
        }
    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi23())
    spice.quickset_ui.perform_quickset_job_from_menu_quicksetapp(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Home->Copy APP, perform different settings copy quickset job.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:360
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_home_copyapp_combi24
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_home_copyapp_combi24
        +guid:e601ccb9-7ff8-45e4-95dc-cc8c00cee1d2
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ADFMediaSize=Oficio8.5x13 & Copy=PaperSize & Copy=PaperType
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_home_copyapp_combi24(setup_teardown_quickset, spice, ews, job, cdm, net, tray):
    """
    combi24 custom settings:
    quickset_copy_common_combi24 = lambda: {
    "paper_size" : "oficio_8_5x13in", # value from key of copy_paper_size_option_dict
    "paper_type" : "letterhead", # value from key of copy_paper_type_option_dict
    }
    """
    default_tray = tray.get_default_source()
    tray.configure_tray(default_tray, 'na_foolscap_8.5x13in', 'stationery-letterhead')
    quickset_copy_setting = {
        "name" : "copy_quickset_combi24",
        "start_option": "user presses start", # value from key of start_option_dict
        }

    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi24())

    spice.quickset_ui.perform_quickset_job_from_home_app(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Menu->QuickSet APP, perform different settings copy quickset with auto select start option job.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:360
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_one_touch_combi25
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_one_touch_combi25
        +guid:c61cfcb2-ade2-4c63-bd34-8d9609d1a345
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ADFMediaSize=B5-JIS & Copy=PaperSize & Copy=PaperType & EWS=Quicksets & MediaType=Preprinted
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_menu_quicksetapp_one_touch_combi25(setup_teardown_quickset, spice, ews, job, cdm, net, tray):
    """
    quickset_copy_common_combi25 = lambda: {
    "paper_size" : "b5_jis", # value from key of copy_paper_size_option_dict
    "paper_type" : "preprinted", # value from key of copy_paper_type_option_dict
    }
    """
    default_tray = tray.get_default_source()
    tray.configure_tray(default_tray, 'jis_b5_182x257mm', 'stationery-preprinted')
    quickset_copy_setting = {
        "name" : "copy_quickset_combi25",
        "start_option": "start automatically", # value from key of start_option_dict
        }
    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi25())
    spice.quickset_ui.perform_quickset_job_from_menu_quicksetapp(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Menu->Copy APP, perform different settings copy quickset job.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:360
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_menu_copyapp_combi26
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_menu_copyapp_combi26
        +guid:583b434c-ec3d-4463-a396-a8aec6503fdb
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ADFMediaSize=Oficio8.5x13 & Copy=PaperSize & Copy=PaperType & MediaSizeSupported=na_oficio_8.5x13.4in & MediaType=Prepunched
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_menu_copyapp_combi26(setup_teardown_quickset, setup_teardown_flatbed, spice, ews, job, cdm, net, udw, tray):
    """
    quickset_copy_common_combi26 = lambda: {
    "paper_size" : "oficio_216x340_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "prepunched", # value from key of copy_paper_type_option_dict
    }
    """
    default_tray = tray.get_default_source()
    if tray.is_size_supported('na_oficio_8.5x13.4in', default_tray):
        tray.configure_tray(default_tray, 'na_oficio_8.5x13.4in', 'stationery-prepunched')

    quickset_copy_setting = {
        "name" : "copy_quickset_combi26",
        "start_option": "user presses start", # value from key of start_option_dict
        }
    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi26())
    spice.quickset_ui.perform_quickset_job_from_menu_app(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Menu->QuickSet APP, perform different settings copy quickset job.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:360
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi27
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi27
        +guid:999ed247-3970-4c09-be79-8b55f000b04e
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & MediaType=ColouredPaper & DeviceFunction=Copy & ADFMediaSize=16K195x270mm & Copy=PaperSize & Copy=PaperType
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi27(setup_teardown_quickset, spice, ews, job, cdm, net, tray):
    """
    quickset_copy_common_combi27 = lambda: {
    "paper_size" : "16k_195x270_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "colored", # value from key of copy_paper_type_option_dict
    }
    """
    default_tray = tray.get_default_source()
    if tray.is_size_supported('om_16k_195x270mm', default_tray):
        tray.configure_tray(default_tray, 'om_16k_195x270mm', 'stationery-colored')

    quickset_copy_setting = {
        "name" : "copy_quickset_combi27",
        "start_option": "user presses start", # value from key of start_option_dict
        }
    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi27())
    spice.quickset_ui.perform_quickset_job_from_menu_quicksetapp(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Home->Copy APP, perform different settings copy quickset job.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:360
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_home_copyapp_combi28
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_home_copyapp_combi28
        +guid:d6872493-bfb7-4571-8f85-e631713e0cdc
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & MediaType=Bond & Copy=PaperSize & Copy=PaperType & ADFMediaSize=16K184x260mm
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_home_copyapp_combi28(setup_teardown_quickset, spice, ews, job, cdm, net, tray):
    """
    combi28 custom settings:
    quickset_copy_common_combi28 = lambda: {
    "paper_size" : "16k_184x260_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "bond", # value from key of copy_paper_type_option_dict
    }
    """
    default_tray = tray.get_default_source()
    tray.configure_tray(default_tray, 'om_16k_184x260mm', 'stationery-bond')
    quickset_copy_setting = {
        "name" : "copy_quickset_combi28",
        "start_option": "user presses start", # value from key of start_option_dict
        }

    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi28())

    spice.quickset_ui.perform_quickset_job_from_home_app(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Menu->QuickSet APP, perform different settings copy quickset with auto select start option job.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:360
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_one_touch_combi29
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_one_touch_combi29
        +guid:6c76bdf0-1ed3-4c3f-9d73-c93e761d939a
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & MediaType=Plain & Copy=PaperSize & Copy=PaperType & ADFMediaSize=16K197x273mm
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_menu_quicksetapp_one_touch_combi29(setup_teardown_quickset, spice, ews, job, cdm, net, tray):
    """
    quickset_copy_common_combi29 = lambda: {
    "paper_size" : "16k_197x273_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "light", # value from key of copy_paper_type_option_dict
    }
    """
    default_tray = tray.get_default_source()
    tray.configure_tray(default_tray, 'roc_16k_7.75x10.75in', 'stationery-lightweight')
    quickset_copy_setting = {
        "name" : "copy_quickset_combi29",
        "start_option": "start automatically", # value from key of start_option_dict
        }
    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi29())
    spice.quickset_ui.perform_quickset_job_from_menu_quicksetapp(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()


	
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Menu->Copy APP, perform different settings copy quickset job.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:800
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_menu_copyapp_combi30
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_menu_copyapp_combi30
        +guid:b325a724-bcd6-4a77-85ae-c0d9674c8125
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=PaperSize & Copy=PaperType & ADFMediaSize=Custom & EWS=Quicksets & MediaSizeSupported=custom & MediaType=Rough
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_menu_copyapp_combi30(setup_teardown_quickset, setup_teardown_flatbed, spice, ews, job, cdm, net, udw, tray):
    """
    quickset_copy_common_combi30 = lambda: {
    "paper_size" : "custom", # value from key of copy_paper_size_option_dict
    "paper_type" : "rough", # value from key of copy_paper_type_option_dict
    }
    """
    default_tray = tray.get_default_source()
    if tray.is_size_supported('custom', default_tray):
        tray.configure_tray(default_tray, 'custom', 'com.hp.rough')

    quickset_copy_setting = {
        "name" : "copy_quickset_combi30",
        "start_option": "user presses start", # value from key of start_option_dict
        }
    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi30())
    spice.quickset_ui.perform_quickset_job_from_menu_app(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Menu->Quickset APP, perform copy job with created quickset.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi31
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi31
        +guid:77396918-b4cb-42f0-a530-e67fb6667325
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & MediaType=Rough & Copy=PaperSize & Copy=PaperType & ADFMediaSize=16K184x260mm
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi31(setup_teardown_quickset, spice, ews, job, cdm, net, tray):
    """
    quickset_copy_common_combi31 = lambda: {
    "paper_size" : "16k_184x260_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "heavy_rough", # value from key of copy_paper_type_option_dict
    }
    """
    default_tray = tray.get_default_source()
    tray.configure_tray(default_tray, 'om_16k_184x260mm', 'com.hp.heavy-rough')

    quickset_copy_setting = {
        "name" : "copy_quickset_combi31",
        "start_option": "user presses start", # value from key of start_option_dict
        }
    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi31())
    spice.quickset_ui.perform_quickset_job_from_menu_quicksetapp(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()




"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Menu->Quickset APP, perform copy job with created quickset.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:360
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi35
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi35
        +guid:bc917b5c-4456-4dee-b1f3-9fdd7f16c5d1
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=PaperSize & Copy=PaperType & ADFMediaSize=A3
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi35(setup_teardown_quickset, spice, ews, job, cdm, net, tray):
    """
    quickset_copy_common_combi35 = lambda: {
    "paper_size" : "a3_297x420_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "hp_matte_105g", # value from key of copy_paper_type_option_dict
    }
    """
    default_tray = tray.get_default_source()
    tray.configure_tray(default_tray, 'iso_a3_297x420mm', 'com.hp.matte-105gsm')

    quickset_copy_setting = {
        "name" : "copy_quickset_combi35",
        "start_option": "user presses start", # value from key of start_option_dict
        }
    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi35())
    spice.quickset_ui.perform_quickset_job_from_menu_quicksetapp(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Menu->Copy APP, perform copy job with created quickset.
    +test_tier:3
    +is_manual: False
    +reqid:DUNE-28198
    +timeout:360
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_menu_copyapp_combi36
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_menu_copyapp_combi36
        +guid:2ffc7ca2-cd59-448a-ae94-2c934696fa95
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & Copy=PaperSize & Copy=PaperType & ADFMediaSize=A4Landscape & MediaType=HPPremiumChoiceMatte120g & MediaSizeSupported=iso_a4_210x297mm
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_menu_copyapp_combi36(setup_teardown_quickset, spice, ews, job, cdm, net, tray):
    """
    quickset_copy_common_combi36 = lambda: {
    "paper_size" : "a4_210x297_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "hp_matte_120g", # value from key of copy_paper_type_option_dict
    }
    """
    default_tray = tray.get_default_source()
    tray.configure_tray(default_tray, "iso_a4_210x297mm", 'com.hp.matte-120gsm')

    quickset_copy_setting = {
        "name" : "copy_quickset_combi36",
        "start_option": "user presses start", # value from key of start_option_dict
        }
    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi36())
    spice.quickset_ui.perform_quickset_job_from_menu_app(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Home->Copy APP, perform different settings copy quickset job.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_home_copyapp_combi38
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_home_copyapp_combi38
        +guid:18ee4b88-f093-4b80-b149-9b908ce7aeb9
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy  & ADFMediaSize=A6 & EWS=Quicksets 
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_home_copyapp_combi38(setup_teardown_quickset, spice, ews, job, cdm, net, tray):
    """
    quickset_copy_common_combi38 = lambda: {
    "paper_size" : "a6_105x148_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "hp_matte_150g", # value from key of copy_paper_type_option_dict
    }
    """
    default_tray = tray.get_default_source()
    tray.configure_tray(default_tray, 'iso_a6_105x148mm', 'com.hp.matte-160gsm')
    quickset_copy_setting = {
        "name" : "copy_quickset_combi38",
        "start_option": "user presses start", # value from key of start_option_dict
        }

    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi38())

    spice.quickset_ui.perform_quickset_job_from_home_app(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()



"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Menu->Quickset APP, perform copy job with created quickset.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:360
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi44
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi44
        +guid:8d72e149-4dd9-4dcd-828d-35e860503662
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=PaperSize & Copy=PaperType & ADFMediaSize=B5-JIS & MediaType=HPAdvancedPhotoPapers
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi44(setup_teardown_quickset, spice, ews, job, cdm, net, tray):
    """
    quickset_copy_common_combi44 = lambda: {
    "paper_size" : "envelope_b5_176x250_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "hp_advanced_photo", # value from key of copy_paper_type_option_dict
    }
    """
    default_tray = tray.get_default_source()
    tray.configure_tray(default_tray, 'iso_b5_176x250mm', 'com.hp.advanced-photo')

    quickset_copy_setting = {
        "name" : "copy_quickset_combi44",
        "start_option": "user presses start", # value from key of start_option_dict
        }
    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi44())
    spice.quickset_ui.perform_quickset_job_from_menu_quicksetapp(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()



"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Menu->Quickset APP, perform copy job with created quickset.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:360
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi53
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi53
        +guid:93df6748-5090-4200-9b4d-2a3f6ae415bf
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=PaperSize & Copy=PaperType & ADFMediaSize=RA3
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi53(setup_teardown_quickset, spice, ews, job, cdm, net, tray, scan_emulation):
    try:
        """
        quickset_copy_common_combi53 = lambda: {
        "paper_size" : "ra3_305x430mm", # value from key of copy_paper_size_option_dict
        "paper_type" : "heavy", # value from key of copy_paper_type_option_dict
        }
        """
        scan_emulation.media.load_media('ADF',1)

        # Check if the tray supports the media size and paper type else assign the default media size and paper type values
        default_tray = int(tray.get_default_source()[-1])
        media_size_data = cdm.media.get_cdm_mediasizes(default_tray)
        paper_type_data = cdm.media.get_cdm_mediatypes(default_tray)

        is_ra3_media_size_supported = spice.quickset_ui.is_tray_support_mediaSize(media_size_data, default_tray, 'iso_ra3_305x430mm')
        is_heavy_media_type_supported = spice.quickset_ui.is_tray_support_mediaType(paper_type_data, default_tray, 'stationery-heavyweight')
        
        if(is_ra3_media_size_supported and is_heavy_media_type_supported):
            logging.info("Tray-%s supports media size %s and paper type %s", default_tray, 'iso_ra3_305x430mm', 'stationery-heavyweight')
            tray.configure_tray(default_tray, 'iso_ra3_305x430mm', 'stationery-heavyweight')
        else:
            raise Exception("Tray-%s does not support media size iso_ra3_305x430mm and paper type stationery-heavyweight", default_tray)

        quickset_copy_setting = {
            "name" : "copy_quickset_combi53",
            "start_option": "user presses start", # value from key of start_option_dict
            }
        quickset_copy_payload = {}
        quickset_copy_payload.update(quickset_copy_setting)
        quickset_copy_payload.update(quickset_copy_common_combi53())
        spice.quickset_ui.perform_quickset_job_from_menu_quicksetapp(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    finally:
        tray.reset_trays()
        scan_emulation.media.load_media('ADF')
        spice.goto_homescreen()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Menu->Copy APP, perform copy job with created quickset.
    +test_tier:3
    +is_manual: False
    +reqid:DUNE-28198
    +timeout:360
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_menu_copyapp_combi54
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_menu_copyapp_combi54
        +guid:5bd746f5-156b-438f-9829-b6925e4d77b4
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=PaperType & Copy=PaperSize & ADFMediaSize=RA3 & MediaSizeSupported=iso_ra4_215x305mm & MediaType=ExtraHeavy131-175g
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_menu_copyapp_combi54(setup_teardown_quickset, spice, ews, job, cdm, net, tray):
    """
    quickset_copy_common_combi54 = lambda: {
    "paper_size" : "ra4_215x305mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "extra_heavy", # value from key of copy_paper_type_option_dict
    }
    """
    default_tray = tray.get_default_source()
    tray.configure_tray(default_tray, 'iso_ra4_215x305mm', 'com.hp.extra-heavy')

    quickset_copy_setting = {
        "name" : "copy_quickset_combi54",
        "start_option": "user presses start", # value from key of start_option_dict
        }
    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi54())
    spice.quickset_ui.perform_quickset_job_from_menu_app(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Menu->Copy APP, perform copy job with created quickset.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:360
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_menu_copyapp_combi56
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_menu_copyapp_combi56
        +guid:e474c302-1ba8-4b98-9ac3-19cef5015cd4
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=PaperSize & Copy=PaperType & ADFMediaSize=SRA4 & MediaSizeSupported=iso_sra4_225x320mm & MediaType=PlainPaper-Thick
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_menu_copyapp_combi56(setup_teardown_quickset, spice, ews, job, cdm, net, tray):
    """
    quickset_copy_common_combi56 = lambda: {
    "paper_size" : "sra4_225x320mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "hp_midweight_glossy", # value from key of copy_paper_type_option_dict
    }
    """
    default_tray = tray.get_default_source()
    tray.configure_tray(default_tray, 'iso_sra4_225x320mm', 'com.hp.midweight-glossy')

    quickset_copy_setting = {
        "name" : "copy_quickset_combi56",
        "start_option": "user presses start", # value from key of start_option_dict
        }
    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi56())
    spice.quickset_ui.perform_quickset_job_from_menu_quicksetapp(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Menu->Quickset APP, perform copy job with created quickset.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:360
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi61
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi61
        +guid:56359530-1a8a-4b1b-ba82-f1d390745ffb
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=PaperSize & Copy=PaperType & ADFMediaSize=B4-JIS & Quicksets=DefaultQuickset
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi61(setup_teardown_quickset, spice, ews, job, cdm, net, tray):
    """
    quickset_copy_common_combi61 = lambda: {
    "paper_size" : "b4_jis_257x364mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "labels", # value from key of copy_paper_type_option_dict
    }
    """
    default_tray = tray.get_default_source()
    tray.configure_tray(default_tray, 'jis_b4_257x364mm', 'labels')

    quickset_copy_setting = {
        "name" : "copy_quickset_combi61",
        "start_option": "user presses start", # value from key of start_option_dict
        }
    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi61())
    spice.quickset_ui.perform_quickset_job_from_menu_quicksetapp(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Menu->Quickset APP, perform copy job with created quickset.
    +test_tier:3
    +is_manual: False
    +reqid:DUNE-28198
    +timeout:360
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi62
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi62
        +guid:c8828770-301e-47cf-88d5-ac647bd07610
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & MediaType=Envelope & Copy=PaperSize & Copy=PaperType & ADFMediaSize=B5-JIS
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi62(setup_teardown_quickset, spice, ews, job, cdm, net, tray):
    """
    quickset_copy_common_combi62 = lambda: {
    "paper_size" : "b5_jis", # value from key of copy_paper_size_option_dict
    "paper_type" : "envelope", # value from key of copy_paper_type_option_dict
    }
    """
    default_tray = tray.get_default_source()
    tray.configure_tray(default_tray, "jis_b5_182x257mm", 'envelope')

    quickset_copy_setting = {
        "name" : "copy_quickset_combi62",
        "start_option": "user presses start", # value from key of start_option_dict
        }
    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi62())
    spice.quickset_ui.perform_quickset_job_from_menu_quicksetapp(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Menu->Quickset APP, perform copy job with created quickset with auto select start option job.
    +test_tier:3
    +is_manual: False
    +reqid:DUNE-28198
    +timeout:360
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_one_touch_combi63
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_one_touch_combi63
        +guid:77e9d688-df54-44b4-b665-6700819521d6
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy &MediaType=HeavyEnvelope & Copy=PaperSize & Copy=PaperType & FlatbedMediaSize=B6-JIS
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_menu_quicksetapp_one_touch_combi63(setup_teardown_quickset, spice, ews, job, cdm, net, tray):
    """
    quickset_copy_common_combi63 = lambda: {
    "paper_size" : "b6_jis_128x182_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "heavy_envelope", # value from key of copy_paper_type_option_dict
    }
    """
    default_tray = tray.get_default_source()
    tray.configure_tray(default_tray, "jis_b6_128x182mm", 'envelope-heavyweight')

    quickset_copy_setting = {
        "name" : "copy_quickset_combi63",
        "start_option": "start automatically", # value from key of start_option_dict
        }
    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi63())
    spice.quickset_ui.perform_quickset_job_from_menu_quicksetapp(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Menu->Copy APP, perform copy job with created quickset.
    +test_tier:3
    +is_manual: False
    +reqid:DUNE-28198
    +timeout:360
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_menu_copyapp_combi64
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_menu_copyapp_combi64
        +guid:671d8722-1958-44dc-9626-7462b02b1988
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=PaperSize & Copy=PaperType & ADFMediaSize=JapaneseEnvelopeChou-3 & EWS=Quicksets & MediaSizeSupported=jpn_chou3_120x235mm & MediaType=Letterhead
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_menu_copyapp_combi64(setup_teardown_quickset, spice, ews, job, cdm, net, tray):
    """
    quickset_copy_common_combi64 = lambda: {
    "paper_size" : "japanese_envelope_chou_3_120x235_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "letterhead", # value from key of copy_paper_type_option_dict
    }
    """
    default_tray = tray.get_default_source()
    tray.configure_tray(default_tray, "jpn_chou3_120x235mm", 'stationery-letterhead')

    quickset_copy_setting = {
        "name" : "copy_quickset_combi64",
        "start_option": "user presses start", # value from key of start_option_dict
        }
    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi64())
    spice.quickset_ui.perform_quickset_job_from_menu_app(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Menu->Quickset APP, perform copy job with created quickset.
    +test_tier:3
    +is_manual: False
    +reqid:DUNE-28198
    +timeout:360
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi65
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi65
        +guid:d90fb7d4-4edb-4139-987d-387ba140b1d5
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=PaperSize & Copy=PaperType & ADFMediaSize=JapaneseEnvelopeChou-3 & EWS=Quicksets
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi65(setup_teardown_quickset, spice, ews, job, cdm, net, tray):
    """
    quickset_copy_common_combi65 = lambda: {
    "paper_size" : "japanese_envelope_chou_4_90x205_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "preprinted", # value from key of copy_paper_type_option_dict
    }
    """
    default_tray = tray.get_default_source()
    tray.configure_tray(default_tray, "jpn_chou4_90x205mm", 'stationery-preprinted')

    quickset_copy_setting = {
        "name" : "copy_quickset_combi65",
        "start_option": "user presses start", # value from key of start_option_dict
        }
    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi65())
    spice.quickset_ui.perform_quickset_job_from_menu_quicksetapp(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Menu->Copy APP, perform copy job with created quickset.
    +test_tier:3
    +is_manual: False
    +reqid:DUNE-28198
    +timeout:360
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_menu_copyapp_combi66
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_menu_copyapp_combi66
        +guid:c51c7295-a5c5-42c5-a570-8a7e29efb741
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy  & ADFMediaSize=JapanesePostcard & MediaType=Prepunched & MediaSizeSupported=jpn_hagaki_100x148mm
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_menu_copyapp_combi66(setup_teardown_quickset, spice, ews, job, cdm, net, tray):
    """
    quickset_copy_common_combi66 = lambda: {
    "paper_size" : "postcard_jis", # value from key of copy_paper_size_option_dict
    "paper_type" : "prepunched", # value from key of copy_paper_type_option_dict
    }
    """
    default_tray = tray.get_default_source()
    tray.configure_tray(default_tray, "jpn_hagaki_100x148mm", 'stationery-prepunched')

    quickset_copy_setting = {
        "name" : "copy_quickset_combi66",
        "start_option": "user presses start", # value from key of start_option_dict
        }
    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi66())
    spice.quickset_ui.perform_quickset_job_from_menu_app(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Home->Copy APP, perform different settings copy quickset job.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:360
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_home_copyapp_combi67
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_home_copyapp_combi67
        +guid:55bbd8a2-ce2e-45db-990d-4cf982ae9129
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & MediaType=ColouredPaper & Copy=PaperSize & Copy=PaperType & ADFMediaSize=DoubleJapanPostcardRotated
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_home_copyapp_combi67(setup_teardown_quickset, spice, ews, job, cdm, net, tray):
    """
    quickset_copy_common_combi67 = lambda: {
    "paper_size" : "double_postcard_jis", # value from key of copy_paper_size_option_dict
    "paper_type" : "colored", # value from key of copy_paper_type_option_dict
    }
    """
    default_tray = tray.get_default_source()
    tray.configure_tray(default_tray, 'jpn_oufuku_148x200mm', 'stationery-colored')
    quickset_copy_setting = {
        "name" : "copy_quickset_combi67",
        "start_option": "user presses start", # value from key of start_option_dict
        }

    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi67())

    spice.quickset_ui.perform_quickset_job_from_home_app(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Menu->Quickset APP, perform copy job with created quickset with auto select start option job.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:360
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_one_touch_combi68
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_one_touch_combi68
        +guid:84d221eb-6004-4c87-8d49-d6a0de321e0c
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=PaperSize & Copy=PaperType & ADFMediaSize=2L127x178mm & EWS=Quicksets
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_menu_quicksetapp_one_touch_combi68(setup_teardown_quickset, spice, ews, job, cdm, net, tray):
    """
    quickset_copy_common_combi68 = lambda: {
    "paper_size" : "2l_127x178_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "lightbond", # value from key of copy_paper_type_option_dict
    }
    """
    default_tray = tray.get_default_source()
    tray.configure_tray(default_tray, "jpn_photo-2l_127x177.8mm", 'com.hp.lightbond')

    quickset_copy_setting = {
        "name" : "copy_quickset_combi68",
        "start_option": "start automatically", # value from key of start_option_dict
        }
    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi68())
    spice.quickset_ui.perform_quickset_job_from_menu_quicksetapp(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()



"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Menu->QuickSet APP, perform copy job with created quickset with auto select start option job.
    +test_tier:3
    +is_manual: False
    +reqid:DUNE-28198
    +timeout:300
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_one_touch_combi83
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_one_touch_combi83
        +guid:e2e34832-6ef2-4eeb-a6a2-15cc0ff2e29f
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=PaperType & Copy=PaperSize & ADFMediaSize=Executive & EWS=Quicksets & MediaType=HPMattePresentationPaper
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_menu_quicksetapp_one_touch_combi83(setup_teardown_quickset, spice, ews, job, cdm, net, tray):
    """
    quickset_copy_common_combi83 = lambda: {
    "paper_size" : "executive_7_25x10_5in", # value from key of copy_paper_size_option_dict
    "paper_type" : "hp_matte_presentation", # value from key of copy_paper_type_option_dict
    }
    """
    default_tray = tray.get_default_source()
    tray.configure_tray(default_tray, 'na_executive_7.25x10.5in', 'com.hp-matte-presentation')
    quickset_copy_setting = {
        "name" : "copy_quickset_combi83",
        "start_option": "start automatically", # value from key of start_option_dict
        }
    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi83())
    spice.quickset_ui.perform_quickset_job_from_menu_quicksetapp(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Menu->Copy APP, perform copy job with created quickset.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:360
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_menu_copyapp_combi84
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_menu_copyapp_combi84
        +guid:977bf7e5-9c14-4e2c-aca2-85e6048cf4a2
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=PaperSize & Copy=PaperType & ADFMediaSize=Oficio8.5x13 & MediaType=OtherMatteInkjetPapers & MediaSizeSupported=na_foolscap_8.5x13in
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_menu_copyapp_combi84(setup_teardown_quickset, spice, ews, job, cdm, net, tray):
    """
    quickset_copy_common_combi84 = lambda: {
    "paper_size" : "oficio_8_5x13in", # value from key of copy_paper_size_option_dict
    "paper_type" : "hp_matte_inkjet", # value from key of copy_paper_type_option_dict
    }
    """
    default_tray = tray.get_default_source()
    tray.configure_tray(default_tray, 'na_foolscap_8.5x13in', 'com.hp-matte-inkjet')

    quickset_copy_setting = {
        "name" : "copy_quickset_combi84",
        "start_option": "user presses start", # value from key of start_option_dict
        }
    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi84())
    spice.quickset_ui.perform_quickset_job_from_menu_quicksetapp(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Menu->Copy APP, perform different settings copy quickset job.
    +test_tier: 3
    +is_manual: False
    +reqid:DUNE-28198
    +timeout:360
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_menu_copyapp_combi90
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_menu_copyapp_combi90
        +guid:1045b48b-cf2e-4fa0-8cae-1ffb4c2ee47e
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ADFMediaSize=11x17 & Copy=PaperSize & MediaSizeSupported=na_ledger_11x17in & MediaType=Plain
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_menu_copyapp_combi90(setup_teardown_quickset, setup_teardown_flatbed, spice, ews, job, cdm, net, udw, tray):
    """
    quickset_copy_common_combi90 = lambda: {
    "paper_size" : "ledger_11x17in", # value from key of copy_paper_size_option_dict
    }
    """
    udw.mainApp.ScanMedia.loadMedia("ADF")
    default_tray = tray.get_default_source()
    if tray.is_size_supported('na_ledger_11x17in', default_tray):
        tray.configure_tray(default_tray, 'na_ledger_11x17in', 'stationery')

    quickset_copy_setting = {
        "name" : "copy_quickset_combi90",
        "start_option": "user presses start", # value from key of start_option_dict
        }
    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi90())
    spice.quickset_ui.perform_quickset_job_from_menu_app(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()
    udw.mainApp.ScanMedia.unloadMedia("ADF")


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Menu->QuickSet APP, perform different settings copy quickset job.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:360
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi91
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi91
        +guid:871d78c0-238c-45a4-b4d3-a5abe4da658f
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ADFMediaSize=Legal & Copy=PaperSize & Quicksets=DefaultQuickset
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi91(setup_teardown_quickset, spice, ews, job, cdm, net, tray):
    """
    quickset_copy_common_combi91 = lambda: {
    "paper_size" : "legal_8.5x14in", # value from key of copy_paper_size_option_dict
    }
    """
    default_tray = tray.get_default_source()
    if tray.is_size_supported('na_legal_8.5x14in', default_tray):
        tray.configure_tray(default_tray, 'na_legal_8.5x14in', 'stationery')

    quickset_copy_setting = {
        "name" : "copy_quickset_combi91",
        "start_option": "user presses start", # value from key of start_option_dict
        }
    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi91())
    spice.quickset_ui.perform_quickset_job_from_menu_quicksetapp(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Home->Copy APP, perform different settings copy quickset job.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:360
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_home_copyapp_combi92
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_home_copyapp_combi92
        +guid:84a1e74e-69e9-46cb-ae08-01c080e6e69d
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ADFMediaSize=Letter & Copy=PaperSize & Quicksets=DefaultQuickset
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_home_copyapp_combi92(setup_teardown_quickset, spice, ews, job, cdm, net, tray):
    """
    combi92 custom settings:
    quickset_copy_common_combi92 = lambda: {
    "paper_size" : "letter_8.5x11in", # value from key of copy_paper_size_option_dict
    }
    """
    default_tray = tray.get_default_source()
    tray.configure_tray(default_tray, 'na_letter_8.5x11in', 'stationery')
    quickset_copy_setting = {
        "name" : "copy_quickset_combi92",
        "start_option": "user presses start", # value from key of start_option_dict
        }

    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi92())

    spice.quickset_ui.perform_quickset_job_from_home_app(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Menu->QuickSet APP, perform different settings copy quickset with auto select start option job.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:360
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_one_touch_combi93
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_one_touch_combi93
        +guid:dc001d79-4fbe-4a4d-ac9a-32485ff56bc1
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ADFMediaSize=EnvelopeMonarch & EWS=Quicksets
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_menu_quicksetapp_one_touch_combi93(setup_teardown_quickset, spice, ews, job, cdm, net, tray):
    """
    quickset_copy_common_combi93 = lambda: {
    "paper_size" : "envelop_monarch", # value from key of copy_paper_size_option_dict
    }
    """
    default_tray = tray.get_default_source()
    tray.configure_tray(default_tray, 'na_monarch_3.875x7.5in', 'stationery')
    quickset_copy_setting = {
        "name" : "copy_quickset_combi93",
        "start_option": "start automatically", # value from key of start_option_dict
        }
    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi93())
    spice.quickset_ui.perform_quickset_job_from_menu_quicksetapp(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Menu->Copy APP, perform different settings copy quickset job.
    +test_tier: 3
    +is_manual: False
    +reqid:DUNE-28198
    +timeout:360
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_menu_copyapp_combi94
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_menu_copyapp_combi94
        +guid:e84e9843-3fe4-4f13-ad98-e5165314ee38
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ADFMediaSize=Envelope-10 & EWS=Quicksets & MediaSizeSupported=na_number-10_4.125x9.5in & MediaType=Plain
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_menu_copyapp_combi94(setup_teardown_quickset, setup_teardown_flatbed, spice, ews, job, cdm, net, udw, tray):
    """
    quickset_copy_common_combi94 = lambda: {
    "paper_size" : "envelope_10_4.1x9.5in", # value from key of copy_paper_size_option_dict
    }
    """
    default_tray = tray.get_default_source()
    if tray.is_size_supported('na_number-10_4.125x9.5in', default_tray):
        tray.configure_tray(default_tray, 'na_number-10_4.125x9.5in', 'stationery')

    quickset_copy_setting = {
        "name" : "copy_quickset_combi94",
        "start_option": "user presses start", # value from key of start_option_dict
        }
    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi94())
    spice.quickset_ui.perform_quickset_job_from_menu_app(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Menu->QuickSet APP, perform different settings copy quickset job.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:360
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi96
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi96
        +guid:27132826-12bd-403f-99e6-1c44ca415973
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ADFMediaSize=Oficio8.5x13 & Copy=PaperSize
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi96(setup_teardown_quickset, spice, ews, job, cdm, net, tray):
    """
    quickset_copy_common_combi96 = lambda: {
    "paper_size" : "oficio_216x340_mm", # value from key of copy_paper_size_option_dict
    }
    """
    default_tray = tray.get_default_source()
    if tray.is_size_supported('na_oficio_8.5x13.4in', default_tray):
        tray.configure_tray(default_tray, 'na_oficio_8.5x13.4in', 'stationery')

    quickset_copy_setting = {
        "name" : "copy_quickset_combi96",
        "start_option": "user presses start", # value from key of start_option_dict
        }
    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi96())
    spice.quickset_ui.perform_quickset_job_from_menu_quicksetapp(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Home->Copy APP, perform different settings copy quickset job.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:360
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_home_copyapp_combi113
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_home_copyapp_combi113
        +guid:7d31b9ad-fbc5-4b23-bb26-66bb6f217f2c
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ADFMediaSize=16K184x260mm & Copy=PaperSize
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_home_copyapp_combi113(setup_teardown_quickset, spice, ews, job, cdm, net, tray):
    """
    combi113 custom settings:
    quickset_copy_common_combi113 = lambda: {
    "paper_size" : "16k_184x260_mm", # value from key of copy_paper_size_option_dict
    }
    """
    default_tray = tray.get_default_source()
    tray.configure_tray(default_tray, 'om_16k_184x260mm', 'stationery')
    quickset_copy_setting = {
        "name" : "copy_quickset_combi113",
        "start_option": "user presses start", # value from key of start_option_dict
        }

    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi113())

    spice.quickset_ui.perform_quickset_job_from_home_app(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Menu->QuickSet APP, perform different settings copy quickset with auto select start option job.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:360
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_one_touch_combi114
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_one_touch_combi114
        +guid:3e02cdd9-dde7-4685-bc4a-4754b790ebac
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ADFMediaSize=16K195x270mm & Copy=PaperSize
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_menu_quicksetapp_one_touch_combi114(setup_teardown_quickset, spice, ews, job, cdm, net, tray):
    """
    quickset_copy_common_combi114 = lambda: {
    "paper_size" : "16k_195x270_mm", # value from key of copy_paper_size_option_dict
    }
    """
    default_tray = tray.get_default_source()
    tray.configure_tray(default_tray, 'om_16k_195x270mm', 'stationery')
    tray.load_media(default_tray)
    quickset_copy_setting = {
        "name" : "copy_quickset_combi114",
        "start_option": "start automatically", # value from key of start_option_dict
        }
    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi114())
    spice.quickset_ui.perform_quickset_job_from_menu_quicksetapp(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Menu->QuickSet APP, perform different settings copy quickset job.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:360
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi116
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi116
        +guid:e85c022c-134b-4029-a026-656a93ea7f32
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ADFMediaSize=8K270x390mm & Copy=PaperSize
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi116(setup_teardown_quickset, spice, ews, job, cdm, net, tray):
    """
    quickset_copy_common_combi116 = lambda: {
    "paper_size" : "8K_270x390mm", # value from key of copy_paper_size_option_dict
    }
    """
    default_tray = tray.get_default_source()
    if tray.is_size_supported('om_8k_270x390mm', default_tray):
        tray.configure_tray(default_tray, 'om_8k_270x390mm', 'stationery')

    quickset_copy_setting = {
        "name" : "copy_quickset_combi116",
        "start_option": "user presses start", # value from key of start_option_dict
        }
    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi116())
    spice.quickset_ui.perform_quickset_job_from_menu_quicksetapp(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Menu->Copy APP, perform different settings copy quickset job.
    +test_tier: 3
    +is_manual: False
    +reqid:DUNE-28198
    +timeout:360
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_menu_copyapp_combi123
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_menu_copyapp_combi123
        +guid:704c6aa0-b75d-46e8-8487-cb173cdac41e
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ADFMediaSize=10x15cm & Copy=PaperSize & EWS=Quicksets & MediaSizeSupported=om_small-photo_100x150mm & MediaType=Plain
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_menu_copyapp_combi123(setup_teardown_quickset, setup_teardown_flatbed, spice, ews, job, cdm, net, udw, tray):
    """
    quickset_copy_common_combi123 = lambda: {
    "paper_size" : "100x150mm", # value from key of copy_paper_size_option_dict
    }
    """
    default_tray = tray.get_default_source()
    if tray.is_size_supported('om_small-photo_100x150mm', default_tray):
        tray.configure_tray(default_tray, 'om_small-photo_100x150mm', 'stationery')

    quickset_copy_setting = {
        "name" : "copy_quickset_combi123",
        "start_option": "user presses start", # value from key of start_option_dict
        }
    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi123())
    spice.quickset_ui.perform_quickset_job_from_menu_app(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Menu->QuickSet APP, perform different settings copy quickset job.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:360
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi124
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi124
        +guid:a8956b2a-6731-4d4b-85df-1723a7d7de36
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ADFMediaSize=16K197x273mm & Copy=PaperSize
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_menu_quicksetapp_combi124(setup_teardown_quickset, spice, ews, job, cdm, net, tray):
    """
    quickset_copy_common_combi124 = lambda: {
    "paper_size" : "16k_197x273_mm", # value from key of copy_paper_size_option_dict
    }
    """
    default_tray = tray.get_default_source()
    if tray.is_size_supported('roc_16k_7.75x10.75in', default_tray):
        tray.configure_tray(default_tray, 'roc_16k_7.75x10.75in', 'stationery')

    quickset_copy_setting = {
        "name" : "copy_quickset_combi124",
        "start_option": "user presses start", # value from key of start_option_dict
        }
    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi124())
    spice.quickset_ui.perform_quickset_job_from_menu_quicksetapp(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()    


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create corresponding quickset app from EWS, check corresponding quickset app setting via UI CDM. From Menu->QuickSet APP, perform different settings copy quickset with auto select start option job.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_one_touch_combi126
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_ui_job_from_menu_quicksetapp_one_touch_combi126
        +guid:649cbbac-0740-498b-b974-cb5dbe0cdfd9
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ADFMediaSize=Custom & Copy=PaperSize & EWS=Quicksets
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_ui_job_from_menu_quicksetapp_one_touch_combi126(setup_teardown_quickset, spice, ews, job, cdm, net, tray):
    """
    quickset_copy_common_combi126 = lambda: {
    "paper_size" : "custom", # value from key of copy_paper_size_option_dict
    }
    """
    default_tray = tray.get_default_source()
    tray.configure_tray(default_tray, 'custom', 'stationery')
    quickset_copy_setting = {
        "name" : "copy_quickset_combi126",
        "start_option": "start automatically", # value from key of start_option_dict
        }
    quickset_copy_payload = {}
    quickset_copy_payload.update(quickset_copy_setting)
    quickset_copy_payload.update(quickset_copy_common_combi126())
    spice.quickset_ui.perform_quickset_job_from_menu_quicksetapp(net, job, ews_quicksets_app=ews.quicksets_app, quickset_type="copy", payload=quickset_copy_payload)
    tray.reset_trays()

def edit_quickset_helper(qs, title, qsType, shared_folder_type=Quicksets.SharedFolderType.SMB):
    _logger.info("Editing " + title)
    qs.csc.shortcuts_init(title)
    qs.create_quickset(qsType, title, shared_folder_type)
    if (qsType == qs.QuicksetType.COPY):
        qs.edit_copy_quickset(title, 42)
        qs.check_quickset_value(qsType, title, 'copies', 42)
    elif (shared_folder_type == qs.SharedFolderType.PERSONAL):
        qs.edit_quickset_filename(qsType, title, 'newfile')
        qs.check_quickset_value(qsType, title, 'fileName', 'newfile')
    else:
        qs.edit_quickset_filename(qsType, title, 'newfile')
        qs.check_quickset_value(qsType, title, 'fileName', 'newfile')
    qs.delete_quickset_by_title(title)
    qs.ews.driver.close()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:edit a copy quickset
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-28218
    +timeout:360
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_ews_quicksets_edit_copy
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_ews_quicksets_edit_copy
        +guid:c995b13a-9f7a-4c1e-b643-4094dc92a090
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & EWS=Quicksets
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ews_quicksets_edit_copy(ews, net):
    qs = Quicksets(ews, net)
    edit_quickset_helper(qs, 'Copy Quickset', qs.QuicksetType.COPY)


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:copy created copy quickset job from menu quicksets
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_add_defaultsettings_startoption_from_home_copyjob_from_menu_quicksets
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_add_defaultsettings_startoption_from_home_copyjob_from_menu_quicksets
        +guid:41ea964c-802e-4aef-8fb4-d8d03f3cfa6f
        +dut:
            +type:Simulator
            +configuration: DeviceFunction=Copy & Quicksets=DefaultQuickset
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_add_defaultsettings_startoption_from_home_copyjob_from_menu_quicksets(spice, net, job, ews):
    try:
        updated_expected_settings_cdm = expected_cdm_for_copy_default_from_actual_cdm(ews)
        verify_create_copy_quick_set_from_ews(
            ews=ews,
            expected_settings_cdm=updated_expected_settings_cdm,
            title=copy_title_name,
            description=copy_description,
            start_option=QuickSetStartOption.start_automatically,
            copy_options=None
        )
        copy_job_from_fp_menu_quickset(spice, net, job, copy_title_name, start_option=QuickSetStartOption.start_automatically)
    finally:
        logging.info("Close the current browser")
        ews.close_browser()
        logging.info("Clean up quickset when finish test")
        qs = ews.quick_sets_app
        qs.csc.shortcuts_init(copy_title_name)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:copy created copy quickset job from menu copy
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_add_defaultsettings_startoption_from_home_copyjob_from_menu_copy
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_add_defaultsettings_startoption_from_home_copyjob_from_menu_copy
        +guid:462335af-1724-4199-8897-868092418b58
        +dut:
            +type:Simulator
            +configuration: DeviceFunction=Copy & Quicksets=DefaultQuickset
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_add_defaultsettings_startoption_from_home_copyjob_from_menu_copy(spice, net, job, ews, configuration):
    try:
        updated_expected_settings_cdm = expected_cdm_for_copy_default_from_actual_cdm(ews)
        verify_create_copy_quick_set_from_ews(
            ews=ews,
            expected_settings_cdm=updated_expected_settings_cdm,
            title=copy_title_name,
            description=copy_description,
            start_option=QuickSetStartOption.start_automatically,
            copy_options=None
        )
        qs = ews.quick_sets_app
        short_cut_id = qs.csc.get_shortcut_id(copy_title_name)
        copy_job_from_fp_menu_copy(spice, net, job, short_cut_id, configuration)
    finally:
        logging.info("Close the current browser")
        ews.close_browser()
        logging.info("Clean up quickset when finish test")
        qs = ews.quick_sets_app
        qs.csc.shortcuts_init(copy_title_name)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:copy created copy quickset job from home copy app
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_add_defaultsettings_startoption_from_home_copyjob_from_copyapp
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_add_defaultsettings_startoption_from_home_copyjob_from_copyapp
        +guid:e5f4daa2-2def-4e22-8202-0a47e775c510
        +dut:
            +type:Simulator
            +configuration: DeviceFunction=Copy & ScannerInput=Flatbed & EWS=Quicksets
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_add_defaultsettings_startoption_from_home_copyjob_from_copyapp(spice, net, job, ews, configuration):
    try:
        updated_expected_settings_cdm = expected_cdm_for_copy_default_from_actual_cdm(ews)
        verify_create_copy_quick_set_from_ews(
            ews=ews,
            expected_settings_cdm=updated_expected_settings_cdm,
            title=copy_title_name,
            description=copy_description,
            start_option=QuickSetStartOption.start_automatically,
            copy_options=None
        )
        qs = ews.quick_sets_app
        short_cut_id = qs.csc.get_shortcut_id(copy_title_name)
        copy_job_from_fp_copy_app(spice, net, job, short_cut_id, configuration)
    finally:
        logging.info("Close the current browser")
        ews.close_browser()
        logging.info("Clean up quickset when finish test")
        qs = ews.quick_sets_app
        qs.csc.shortcuts_init(copy_title_name)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:copy created copy quickset job from menu quicksets
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_add_defaultsettings_start_from_landingapp_copyjob_from_menu_quicksets
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_add_defaultsettings_start_from_landingapp_copyjob_from_menu_quicksets
        +guid:34566484-cc48-498e-bedd-039ace04ac26
        +dut:
            +type:Simulator
            +configuration: DeviceFunction=Copy & ScannerInput=Flatbed & EWS=Quicksets
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_add_defaultsettings_start_from_landingapp_copyjob_from_menu_quicksets(spice, net, job, ews):
    try:
        updated_expected_settings_cdm = expected_cdm_for_copy_default_from_actual_cdm(ews)
        updated_expected_settings_cdm["summary_info"]["action"] = "open"
        verify_create_copy_quick_set_from_ews(
            ews=ews,
            expected_settings_cdm=updated_expected_settings_cdm,
            title=copy_title_name,
            description=copy_description,
            start_option=QuickSetStartOption.user_presses_start,
            copy_options=None
        )
        copy_job_from_fp_menu_quickset(spice, net, job, copy_title_name, start_option=QuickSetStartOption.user_presses_start)
    finally:
        logging.info("Close the current browser")
        ews.close_browser()
        logging.info("Clean up quickset when finish test")
        qs = ews.quick_sets_app
        qs.csc.shortcuts_init(copy_title_name)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:copy created copy quickset job from copy app
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_add_defaultsettings_start_from_landingapp_copyjob_from_copyapp_validate
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_add_defaultsettings_start_from_landingapp_copyjob_from_copyapp_validate
        +guid:a0d8df63-dfeb-4004-b7a6-c8714780f006
        +dut:
            +type:Simulator
            +configuration: DeviceFunction=Copy & ScannerInput=Flatbed & EWS=Quicksets
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_add_defaultsettings_start_from_landingapp_copyjob_from_copyapp_validate(spice, net, job, ews, configuration, udw):
    udw.mainApp.ScanMedia.loadMedia("ADF")
    try:
        updated_expected_settings_cdm = expected_cdm_for_copy_default_from_actual_cdm(ews)
        updated_expected_settings_cdm["summary_info"]["action"] = "open"
        if ews.cdm.device_feature_cdm.is_color_supported()== False:
            updated_expected_settings_cdm["settings_info"]["src"]["scan"]["colorMode"] = "grayscale"

        verify_create_copy_quick_set_from_ews(
            ews=ews,
            expected_settings_cdm=updated_expected_settings_cdm,
            title=copy_title_name,
            description=copy_description,
            start_option=QuickSetStartOption.user_presses_start,
            copy_options=None
        )
        qs = ews.quick_sets_app
        short_cut_id = qs.csc.get_shortcut_id(copy_title_name)
        copy_job_from_fp_copy_app(spice, net, job, short_cut_id, configuration)
    finally:
        logging.info("Close the current browser")
        ews.close_browser()
        logging.info("Clean up quickset when finish test")
        qs = ews.quick_sets_app
        qs.csc.shortcuts_init(copy_title_name)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:copy created copy quickset job from menu copy
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_add_defaultsettings_start_from_landingapp_copyjob_from_menu_copy
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_add_defaultsettings_start_from_landingapp_copyjob_from_menu_copy
        +guid:d5c9c13b-bea9-482c-9d19-06662c36da78
        +dut:
            +type:Simulator
            +configuration: DeviceFunction=Copy & ScannerInput=Flatbed & EWS=Quicksets
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_add_defaultsettings_start_from_landingapp_copyjob_from_menu_copy(spice, net, job, ews, configuration):
    try:
        updated_expected_settings_cdm = expected_cdm_for_copy_default_from_actual_cdm(ews)
        updated_expected_settings_cdm["summary_info"]["action"] = "open"
        verify_create_copy_quick_set_from_ews(
            ews=ews,
            expected_settings_cdm=updated_expected_settings_cdm,
            title=copy_title_name,
            description=copy_description,
            start_option=QuickSetStartOption.user_presses_start,
            copy_options=None
        )
        qs = ews.quick_sets_app
        short_cut_id = qs.csc.get_shortcut_id(copy_title_name)
        copy_job_from_fp_menu_copy(spice, net, job, short_cut_id, configuration)
    finally:
        logging.info("Close the current browser")
        ews.close_browser()
        logging.info("Clean up quickset when finish test")
        qs = ews.quick_sets_app
        qs.csc.shortcuts_init(copy_title_name)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:copy created copy quickset job from menu quicksets
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_add_customsettings_start_from_home_copyjob_from_menu_quicksets
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_add_customsettings_start_from_home_copyjob_from_menu_quicksets
        +guid:06aa4685-50cc-41c8-b237-5d8ad97e8124
        +dut:
            +type:Simulator
            +configuration: DeviceFunction=Copy & FlatbedMediaSize=Letter & EWS=Quicksets
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_add_customsettings_start_from_home_copyjob_from_menu_quicksets(spice, net, job, ews, udw):
    udw.mainApp.ScanMedia.loadMedia("ADF")
    try:
        updated_expected_settings_cdm = expected_cdm_copy_combi3_from_actual_cdm(ews)
        
        verify_create_copy_quick_set_from_ews(
            ews=ews,
            expected_settings_cdm=updated_expected_settings_cdm,
            title=copy_title_name,
            description=copy_description,
            start_option=QuickSetStartOption.start_automatically,
            copy_options=copy_option_combi3
        )
        copy_job_from_fp_menu_quickset(spice, net, job, copy_title_name, start_option=QuickSetStartOption.start_automatically)
    finally:
        logging.info("Close the current browser")
        ews.close_browser()
        logging.info("Clean up quickset when finish test")
        qs = ews.quick_sets_app
        qs.csc.shortcuts_init(copy_title_name)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:copy created copy quickset job from copy app
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:700
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_add_customsettings_start_from_home_copyjob_from_copyapp
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_add_customsettings_start_from_home_copyjob_from_copyapp
        +guid:00d2ee30-c0ad-4134-a338-91617a177dc1
        +dut:
            +type:Simulator
            +configuration: DeviceFunction=Copy & FlatbedMediaSize=Letter & EWS=Quicksets
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_add_customsettings_start_from_home_copyjob_from_copyapp(spice, net, job, ews, configuration, udw):
    try:
        udw.mainApp.ScanMedia.loadMedia("ADF")         
        updated_expected_settings_cdm = expected_cdm_copy_combi3_from_actual_cdm(ews)
        
        verify_create_copy_quick_set_from_ews(
            ews=ews,
            expected_settings_cdm=updated_expected_settings_cdm,
            title=copy_title_name,
            description=copy_description,
            start_option=QuickSetStartOption.start_automatically,
            copy_options=copy_option_combi3
        )
        qs = ews.quick_sets_app
        short_cut_id = qs.csc.get_shortcut_id(copy_title_name)
        copy_job_from_fp_copy_app(spice, net, job, short_cut_id, configuration)
    finally:
        logging.info("Close the current browser")
        ews.close_browser()
        logging.info("Clean up quickset when finish test")
        qs = ews.quick_sets_app
        qs.csc.shortcuts_init(copy_title_name)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:copy created copy quickset job from menu copy
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:700
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_add_customsettings_start_from_home_copyjob_from_menu_copy
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_add_customsettings_start_from_home_copyjob_from_menu_copy
        +guid:6236af2e-09aa-470b-82cb-22740409847c
        +dut:
            +type:Simulator
            +configuration: DeviceFunction=Copy & FlatbedMediaSize=Letter & EWS=Quicksets
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_add_customsettings_start_from_home_copyjob_from_menu_copy(spice, net, job, ews, configuration):
    try:
        updated_expected_settings_cdm = expected_cdm_copy_combi3_from_actual_cdm(ews)
        verify_create_copy_quick_set_from_ews(
            ews=ews,
            expected_settings_cdm=updated_expected_settings_cdm,
            title=copy_title_name,
            description=copy_description,
            start_option=QuickSetStartOption.start_automatically,
            copy_options=copy_option_combi3
        )
        qs = ews.quick_sets_app
        short_cut_id = qs.csc.get_shortcut_id(copy_title_name)
        copy_job_from_fp_menu_copy(spice, net, job, short_cut_id, configuration)
    finally:
        logging.info("Close the current browser")
        ews.close_browser()
        logging.info("Clean up quickset when finish test")
        qs = ews.quick_sets_app
        qs.csc.shortcuts_init(copy_title_name)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:copy created copy quickset job from menu quicksets
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_add_customsettings_start_from_landingapp_copyjob_from_menu_quicksets
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_add_customsettings_start_from_landingapp_copyjob_from_menu_quicksets
        +guid:1fff3cec-8149-4992-a854-cd3dc91fe807
        +dut:
            +type:Simulator
            +configuration: DeviceFunction=Copy & FlatbedMediaSize=Custom
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_add_customsettings_start_from_landingapp_copyjob_from_menu_quicksets(spice, net, job, ews, tray):
    try:
        default_tray = tray.get_default_source()
        tray.configure_tray(default_tray, "any", 'stationery')
        updated_expected_settings_cdm = expected_cdm_copy_combi2_from_actual_cdm(ews)
        
        # this test will be failed since custom size is not showed in EWS and we submit issue https://hp-jira.external.hp.com/browse/HMDE-564 and it still under confirmation
        verify_create_copy_quick_set_from_ews(
            ews=ews,
            expected_settings_cdm=updated_expected_settings_cdm,
            title=copy_title_name,
            description=copy_description,
            start_option=QuickSetStartOption.user_presses_start,
            copy_options=copy_option_combi2
        )
        copy_job_from_fp_menu_quickset(spice, net, job, copy_title_name, start_option=QuickSetStartOption.user_presses_start)
    finally:
        logging.info("Close the current browser")
        ews.close_browser()
        logging.info("Clean up quickset when finish test")
        qs = ews.quick_sets_app
        qs.csc.shortcuts_init(copy_title_name)
        tray.reset_trays()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:copy created copy quickset job from copy app
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_add_customsettings_start_from_landingapp_copyjob_from_copyapp
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_add_customsettings_start_from_landingapp_copyjob_from_copyapp
        +guid:576214c5-ad93-4613-9a33-9fc2c1c1b260
        +dut:
            +type:Simulator
            +configuration: DeviceFunction=Copy & FlatbedMediaSize=Custom
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_add_customsettings_start_from_landingapp_copyjob_from_copyapp(spice, net, job, ews, tray, configuration):
    # Case may fail since no "Custom" option in "Original Size" list, wait for confirmation in bug HMDE-564
    try:
        default_tray = tray.get_default_source()
        tray.configure_tray(default_tray, "any", 'stationery')
        updated_expected_settings_cdm = expected_cdm_copy_combi2_from_actual_cdm(ews)
        
        verify_create_copy_quick_set_from_ews(
            ews=ews,
            expected_settings_cdm=updated_expected_settings_cdm,
            title=copy_title_name,
            description=copy_description,
            start_option=QuickSetStartOption.user_presses_start,
            copy_options=copy_option_combi2
        )
        qs = ews.quick_sets_app
        short_cut_id = qs.csc.get_shortcut_id(copy_title_name)
        copy_job_from_fp_copy_app(spice, net, job, short_cut_id, configuration)
    finally:
        logging.info("Close the current browser")
        ews.close_browser()
        logging.info("Clean up quickset when finish test")
        qs = ews.quick_sets_app
        qs.csc.shortcuts_init(copy_title_name)
        tray.reset_trays()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:copy created copy quickset job from copy app
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_add_customsettings_start_from_landingapp_copyjob_from_menu_copy
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_add_customsettings_start_from_landingapp_copyjob_from_menu_copy
        +guid:a1505e6d-1284-42cc-885c-79361f76b0cb
        +dut:
            +type:Simulator
            +configuration: DeviceFunction=Copy & FlatbedMediaSize=Custom
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_add_customsettings_start_from_landingapp_copyjob_from_menu_copy(spice, net, job, ews, tray, configuration):
    try:
        default_tray = tray.get_default_source()
        tray.configure_tray(default_tray, "any", 'stationery')
        updated_expected_settings_cdm = expected_cdm_copy_combi2_from_actual_cdm(ews)
        # this test will be failed since custom size is not showed in EWS and we submit issue https://hp-jira.external.hp.com/browse/HMDE-564 and it still under confirmation
        verify_create_copy_quick_set_from_ews(
            ews=ews,
            expected_settings_cdm=updated_expected_settings_cdm,
            title=copy_title_name,
            description=copy_description,
            start_option=QuickSetStartOption.user_presses_start,
            copy_options=copy_option_combi2
        )
        qs = ews.quick_sets_app
        short_cut_id = qs.csc.get_shortcut_id(copy_title_name)
        copy_job_from_fp_menu_copy(spice, net, job, short_cut_id, configuration)
    finally:
        logging.info("Close the current browser")
        ews.close_browser()
        logging.info("Clean up quickset when finish test")
        qs = ews.quick_sets_app
        qs.csc.shortcuts_init(copy_title_name)
        tray.reset_trays()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:copy created copy quickset job from menu quicksets
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_edit_customsettings_start_from_landingapp_copyjob_from_menu_quicksets
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_edit_customsettings_start_from_landingapp_copyjob_from_menu_quicksets
        +guid:fcfe1958-f4ed-40d3-a720-43590808a7eb
        +dut:
            +type:Simulator
            +configuration: DeviceFunction=Copy & FlatbedMediaSize=Custom
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_edit_customsettings_start_from_landingapp_copyjob_from_menu_quicksets(spice, net, job, ews, tray):
    # this test will be failed since custom size is not showed in EWS and we submit issue https://hp-jira.external.hp.com/browse/HMDE-564 and it still under confirmation
    try:
        default_tray = tray.get_default_source()
        tray.configure_tray(default_tray, "any", 'stationery')
        updated_expected_settings_cdm = expected_cdm_for_copy_default_from_actual_cdm(ews)
        
        # Create copy quick set with default settings
        verify_create_copy_quick_set_from_ews(
            ews=ews,
            expected_settings_cdm=updated_expected_settings_cdm,
            title=copy_title_name,
            description=copy_description,
            start_option=QuickSetStartOption.start_automatically,
            copy_options=None
        )

        logging.info("Close the current browser")
        ews.close_browser()
        # Reopen browser to edit the quickset
        qs = ews.quick_sets_app
        qs.start_to_edit_quick_set_by_title(copy_title_name)
        # Modify form content
        updated_copy_title_name = f"{copy_title_name}_{get_local_time()}"
        qs.complete_copy_quick_sets_from_setup_page(
            title=updated_copy_title_name,
            description=copy_description,
            start_option=QuickSetStartOption.user_presses_start,
            copy_options=copy_option_combi2
        )

        logging.info("Check quickset in EWS")
        qs_index = qs.find_quick_set_by_title(updated_copy_title_name)
        assert qs_index != -1
        # Check in cdm
        updated_expected_settings_cdm = expected_cdm_copy_combi2_from_actual_cdm(ews)
        updated_expected_settings_cdm ["summary_info"]["title"] = updated_copy_title_name
        updated_expected_settings_cdm ["summary_info"]["action"] = "open"
        check_with_cdm_on_ews_quick_sets_copy(qs, updated_copy_title_name, updated_expected_settings_cdm)
        copy_job_from_fp_menu_quickset(spice, net, job, updated_copy_title_name, start_option=QuickSetStartOption.user_presses_start)
    finally:
        logging.info("Close the current browser")
        ews.close_browser()
        logging.info("Clean up quickset when finish test")
        qs = ews.quick_sets_app
        qs.csc.shortcuts_init(updated_copy_title_name)
        tray.reset_trays()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:copy created copy quickset job from copyapp
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_edit_customsettings_start_from_landingapp_copyjob_from_copyapp
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_edit_customsettings_start_from_landingapp_copyjob_from_copyapp
        +guid:0e4b23a0-bd34-47ac-9dd4-74d5f0eaf4b8
        +dut:
            +type:Simulator
            +configuration: DeviceFunction=Copy & FlatbedMediaSize=Custom
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_edit_customsettings_start_from_landingapp_copyjob_from_copyapp(spice, net, job, ews, tray, configuration):
    # this test will be failed since custom size is not showed in EWS and we submit issue https://hp-jira.external.hp.com/browse/HMDE-564 and it still under confirmation
    try:
        default_tray = tray.get_default_source()
        tray.configure_tray(default_tray, "any", 'stationery')
        updated_expected_settings_cdm = expected_cdm_for_copy_default_from_actual_cdm(ews)
        
        # Create copy quick set with default settings
        verify_create_copy_quick_set_from_ews(
            ews=ews,
            expected_settings_cdm=updated_expected_settings_cdm,
            title=copy_title_name,
            description=copy_description,
            start_option=QuickSetStartOption.start_automatically,
            copy_options=None
        )

        logging.info("Close the current browser")
        ews.close_browser()
        # Reopen browser to edit the quickset
        qs = ews.quick_sets_app
        qs.start_to_edit_quick_set_by_title(copy_title_name)
        # Modify form content
        updated_copy_title_name = f"{copy_title_name}_{get_local_time()}"
        qs.complete_copy_quick_sets_from_setup_page(
            title=updated_copy_title_name,
            description=copy_description,
            start_option=QuickSetStartOption.user_presses_start,
            copy_options=copy_option_combi2
        )

        logging.info("Check quickset in EWS")
        qs_index = qs.find_quick_set_by_title(updated_copy_title_name)
        assert qs_index != -1
        # Check in cdm
        updated_expected_settings_cdm = expected_cdm_copy_combi2_from_actual_cdm(ews)
        updated_expected_settings_cdm ["summary_info"]["title"] = updated_copy_title_name
        updated_expected_settings_cdm ["summary_info"]["action"] = "open"
        short_cut_id = qs.csc.get_shortcut_id(updated_copy_title_name)
        check_with_cdm_on_ews_quick_sets_copy(qs, updated_copy_title_name, updated_expected_settings_cdm)
        copy_job_from_fp_copy_app(spice, net, job, short_cut_id, configuration)
    finally:
        logging.info("Close the current browser")
        ews.close_browser()
        logging.info("Clean up quickset when finish test")
        qs = ews.quick_sets_app
        qs.csc.shortcuts_init(updated_copy_title_name)
        tray.reset_trays()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:copy created copy quickset job from menu copy app
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_edit_defaultsettings_startoption_from_home_copyjob_from_menu_copy
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_edit_defaultsettings_startoption_from_home_copyjob_from_menu_copy
        +guid:18b37853-0f22-44ea-ac36-3457e1eb73fc
        +dut:
            +type:Simulator
            +configuration: DeviceFunction=Copy & FlatbedMediaSize=Custom
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_edit_defaultsettings_startoption_from_home_copyjob_from_menu_copy(spice, net, job, ews, tray, configuration):
    # this test will be failed since custom size is not showed in EWS and we submit issue https://hp-jira.external.hp.com/browse/HMDE-564 and it still under confirmation
    try:
        default_tray = tray.get_default_source()
        tray.configure_tray(default_tray, "any", 'stationery')
        updated_expected_settings_cdm = expected_cdm_for_copy_default_from_actual_cdm(ews)
        
        # Create copy quick set with default settings
        verify_create_copy_quick_set_from_ews(
            ews=ews,
            expected_settings_cdm=updated_expected_settings_cdm,
            title=copy_title_name,
            description=copy_description,
            start_option=QuickSetStartOption.start_automatically,
            copy_options=None
        )

        logging.info("Close the current browser")
        ews.close_browser()
        # Reopen browser to edit the quickset
        qs = ews.quick_sets_app
        qs.start_to_edit_quick_set_by_title(copy_title_name)
        # Modify form content
        updated_copy_title_name = f"{copy_title_name}_{get_local_time()}"
        qs.complete_copy_quick_sets_from_setup_page(
            title=updated_copy_title_name,
            description=copy_description,
            start_option=QuickSetStartOption.user_presses_start,
            copy_options=copy_option_combi2
        )

        logging.info("Check quickset in EWS")
        qs_index = qs.find_quick_set_by_title(updated_copy_title_name)
        assert qs_index != -1
        # Check in cdm
        updated_expected_settings_cdm = expected_cdm_copy_combi2_from_actual_cdm(ews)
        updated_expected_settings_cdm ["summary_info"]["title"] = updated_copy_title_name
        updated_expected_settings_cdm ["summary_info"]["action"] = "open"
        short_cut_id = qs.csc.get_shortcut_id(updated_copy_title_name)
        check_with_cdm_on_ews_quick_sets_copy(qs, updated_copy_title_name, updated_expected_settings_cdm)
        copy_job_from_fp_menu_copy(spice, net, job, short_cut_id, configuration)
    finally:
        logging.info("Close the current browser")
        ews.close_browser()
        logging.info("Clean up quickset when finish test")
        qs = ews.quick_sets_app
        qs.csc.shortcuts_init(updated_copy_title_name)
        tray.reset_trays()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:copy created copy quickset job from menu quicksets
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_clone_start_from_landingapp_copyjob_from_menu_quicksets
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_clone_start_from_landingapp_copyjob_from_menu_quicksets
        +guid:0e7dd95b-9d0a-45d0-9cbc-b047db330a6f
        +dut:
            +type:Simulator
            +configuration: DeviceFunction=Copy & FlatbedMediaSize=A3 & EWS=Quicksets
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_clone_start_from_landingapp_copyjob_from_menu_quicksets(spice, net, job, ews):
    try:
        updated_expected_settings_cdm = expected_cdm_for_copy_default_from_actual_cdm(ews)

        # Create copy quick set with default settings
        verify_create_copy_quick_set_from_ews(
            ews=ews,
            expected_settings_cdm=updated_expected_settings_cdm,
            title=copy_title_name,
            description=copy_description,
            start_option=QuickSetStartOption.start_automatically,
            copy_options=None
        )
        logging.info("Close the current browser")
        ews.close_browser()
        # Reopen browser to copy the quickset
        qs = ews.quick_sets_app
        qs.start_to_copy_quick_set_by_title(copy_title_name)
        # Modify form content
        updated_copy_title_name = f"{copy_title_name}_{get_local_time()}"
        qs.complete_copy_quick_sets_from_setup_page(
            title=updated_copy_title_name,
            description=copy_description,
            start_option=QuickSetStartOption.user_presses_start,
            copy_options=copy_option_combi1
        )

        logging.info("Check quickset in EWS")
        qs_index = qs.find_quick_set_by_title(updated_copy_title_name)
        assert qs_index != -1, "Expected quickset is not found"
        # Check in cdm
        updated_expected_settings_cdm = copy.deepcopy(expected_cdm_copy_combi1)
        updated_expected_settings_cdm ["summary_info"]["title"] = updated_copy_title_name
        updated_expected_settings_cdm["settings_info"]["src"]["scan"]["pagesFlipUpEnabled"] = "true"
        updated_expected_settings_cdm["settings_info"]["src"]["scan"]["plexMode"] = "duplex"
        updated_expected_settings_cdm["settings_info"]["dest"]["print"]["duplexBinding"] = "twoSidedShortEdge"
        updated_expected_settings_cdm ["summary_info"]["action"] = "open"
        check_with_cdm_on_ews_quick_sets_copy(qs, updated_copy_title_name, updated_expected_settings_cdm)
        copy_job_from_fp_menu_quickset(spice, net, job, copy_title_name, start_option=QuickSetStartOption.start_automatically)
    finally:
        logging.info("Close the current browser")
        ews.close_browser()
        logging.info("Clean up quickset when finish test")
        qs = ews.quick_sets_app
        qs.csc.shortcuts_init(updated_copy_title_name)
        qs.csc.shortcuts_init(copy_title_name)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:copy created copy quickset job from copy app
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_clone_start_from_landingapp_copyjob_from_copyapp
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_clone_start_from_landingapp_copyjob_from_copyapp
        +guid:2dec50a1-00ef-4c10-8d09-709a1273501b
        +dut:
            +type:Simulator
            +configuration: DeviceFunction=Copy & FlatbedMediaSize=A3 & EWS=Quicksets
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_clone_start_from_landingapp_copyjob_from_copyapp(spice, net, job, ews, tray, configuration):
    try:
        updated_expected_settings_cdm = expected_cdm_for_copy_default_from_actual_cdm(ews)
        # Create copy quick set with default settings
        verify_create_copy_quick_set_from_ews(
            ews=ews,
            expected_settings_cdm=updated_expected_settings_cdm,
            title=copy_title_name,
            description=copy_description,
            start_option=QuickSetStartOption.start_automatically,
            copy_options=None
        )
        logging.info("Close the current browser")
        ews.close_browser()
        # Reopen browser to copy the quickset
        qs = ews.quick_sets_app
        qs.start_to_copy_quick_set_by_title(copy_title_name)
        # Modify form content
        updated_copy_title_name = f"{copy_title_name}_{get_local_time()}"
        qs.complete_copy_quick_sets_from_setup_page(
            title=updated_copy_title_name,
            description=copy_description,
            start_option=QuickSetStartOption.user_presses_start,
            copy_options=copy_option_combi1
        )

        logging.info("Check quickset in EWS")
        qs_index = qs.find_quick_set_by_title(updated_copy_title_name)
        assert qs_index != -1, "Expected quickset is not found"
        # Check in cdm
        updated_expected_settings_cdm = copy.deepcopy(expected_cdm_copy_combi1)
        updated_expected_settings_cdm["summary_info"]["title"] = updated_copy_title_name
        updated_expected_settings_cdm["summary_info"]["action"] = "open"
        updated_expected_settings_cdm["settings_info"]["src"]["scan"]["pagesFlipUpEnabled"] = "true"
        updated_expected_settings_cdm["settings_info"]["src"]["scan"]["plexMode"] = "duplex"
        updated_expected_settings_cdm["settings_info"]["dest"]["print"]["duplexBinding"] = "twoSidedShortEdge"
        check_with_cdm_on_ews_quick_sets_copy(qs, updated_copy_title_name, updated_expected_settings_cdm)
        tray.configure_tray('tray-2', 'iso_a4_210x297mm', 'stationery')
        short_cut_id = qs.csc.get_shortcut_id(copy_title_name)
        copy_job_from_fp_copy_app(spice, net, job, short_cut_id, configuration)
    finally:
        logging.info("Close the current browser")
        ews.close_browser()
        logging.info("Clean up quickset when finish test")
        qs = ews.quick_sets_app
        qs.csc.shortcuts_init(updated_copy_title_name)
        qs.csc.shortcuts_init(copy_title_name)
        tray.reset_trays()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:copy created copy quickset job from menu copy app
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_clone_start_from_landingapp_copyjob_from_menu_copy
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_clone_start_from_landingapp_copyjob_from_menu_copy
        +guid:f93d5c6a-f2b6-497a-bd2f-dec7cbdae85f
        +dut:
            +type:Simulator
            +configuration: DeviceFunction=Copy & FlatbedMediaSize=A3 & EWS=Quicksets
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_clone_start_from_landingapp_copyjob_from_menu_copy(spice, net, job, ews, tray, configuration):
    try:
        updated_expected_settings_cdm = expected_cdm_for_copy_default_from_actual_cdm(ews)
        # Create copy quick set with default settings
        verify_create_copy_quick_set_from_ews(
            ews=ews,
            expected_settings_cdm=updated_expected_settings_cdm,
            title=copy_title_name,
            description=copy_description,
            start_option=QuickSetStartOption.start_automatically,
            copy_options=None
        )

        logging.info("Close the current browser")
        ews.close_browser()
        # Reopen browser to copy the quickset
        qs = ews.quick_sets_app
        qs.start_to_copy_quick_set_by_title(copy_title_name)
        # Modify form content
        updated_copy_title_name = f"{copy_title_name}_{get_local_time()}"
        qs.complete_copy_quick_sets_from_setup_page(
            title=updated_copy_title_name,
            description=copy_description,
            start_option=QuickSetStartOption.user_presses_start,
            copy_options=copy_option_combi1
        )

        logging.info("Check quickset in EWS")
        qs_index = qs.find_quick_set_by_title(updated_copy_title_name)
        assert qs_index != -1, "Expected quickset is not found"
        # Check in cdm
        updated_expected_settings_cdm = copy.deepcopy(expected_cdm_copy_combi1)
        updated_expected_settings_cdm["summary_info"]["title"] = updated_copy_title_name
        updated_expected_settings_cdm["settings_info"]["src"]["scan"]["pagesFlipUpEnabled"] = "true"
        updated_expected_settings_cdm["settings_info"]["src"]["scan"]["plexMode"] = "duplex"
        updated_expected_settings_cdm["settings_info"]["dest"]["print"]["duplexBinding"] = "twoSidedShortEdge"
        updated_expected_settings_cdm ["summary_info"]["action"] = "open"
        check_with_cdm_on_ews_quick_sets_copy(qs, updated_copy_title_name, updated_expected_settings_cdm)
        tray.configure_tray('tray-2', 'iso_a4_210x297mm', 'stationery')
        short_cut_id = qs.csc.get_shortcut_id(copy_title_name)
        copy_job_from_fp_menu_copy(spice, net, job, short_cut_id, configuration)
    finally:
        logging.info("Close the current browser")
        ews.close_browser()
        logging.info("Clean up quickset when finish test")
        qs = ews.quick_sets_app
        qs.csc.shortcuts_init(updated_copy_title_name)
        qs.csc.shortcuts_init(copy_title_name)
        tray.reset_trays()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:create copy quickset and check user created quickset icon
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-144001
    +timeout:240
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_user_created_icon_from_copy_app
    +test:
        +title:test_copy_quickset_user_created_icon_from_copy_app
        +guid:3459aeed-e43e-4cbf-a642-db308e6292a8
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & EngineFirmwareFamily=Maia
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_user_created_icon_from_copy_app(spice, net, job, ews):
    qs_copy_color_lines = "34cc69d4-194f-11ed-89dc-4be3ffadc2eb"
    qs_copy_mixed_content = "61b72f38-1945-11ed-bf29-87d40f139a32"
    qs_copy_image = "dba2ec94-250a-11ed-b62b-eb3183c3f17f"
    qs_copy_blueprint = "eba1f540-239d-11ed-83d5-0b139473ea60"
    try:
        updated_expected_settings_cdm = expected_cdm_for_copy_default_from_actual_cdm(ews)
        verify_create_copy_quick_set_from_ews(
            ews=ews,
            expected_settings_cdm=updated_expected_settings_cdm,
            title=copy_title_name,
            description=copy_description,
            start_option=QuickSetStartOption.start_automatically,
            copy_options=None
        )
    # Auto_Test_Quick_Set_Copy
    finally:
        logging.info("Close the current browser")
        ews.close_browser()
        logging.info("Goto copy app")
        spice.copy_ui().goto_copy_from_copyapp_at_home_screen()
        logging.info("wait for Quickset")
        spice.wait_for("#copyLandingView")
        spice.wait_for("#copyLandingView #qsScroll")
        # Auto_Test_Quick_Set_Copy
        objectName = ews.quicksets_app.csc.get_shortcut_id(copy_title_name)
        user_qs = spice.wait_for("#copyLandingView #qsScroll #"+objectName)
        logging.info("validate user created icon")
        qs_icon = user_qs["icon"]
        ucqs_path = "qrc:/images/Graphics/UserCreatedQuickset.json"
        assert qs_icon == ucqs_path
        factory_qs = spice.wait_for("#copyLandingView #qsScroll #"+qs_copy_color_lines)
        qs_icon = factory_qs["icon"]
        assert qs_icon != ucqs_path
        factory_qs = spice.wait_for("#copyLandingView #qsScroll #"+qs_copy_mixed_content)
        qs_icon = factory_qs["icon"]
        assert qs_icon != ucqs_path
        factory_qs = spice.wait_for("#copyLandingView #qsScroll #"+qs_copy_image)
        qs_icon = factory_qs["icon"]
        assert qs_icon != ucqs_path
        factory_qs = spice.wait_for("#copyLandingView #qsScroll #"+qs_copy_blueprint)
        qs_icon = factory_qs["icon"]
        assert qs_icon != ucqs_path
        spice.goto_homescreen()
        assert spice.is_HomeScreen()
        ews.quicksets_app.csc.delete_all_shortcuts()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:create copy quickset and check user created quickset icon in quicksets app
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-144001
    +timeout:240
    +asset:LFP
    +delivery_team:LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_user_created_icon_from_qs_app
    +test:
        +title:test_copy_quickset_user_created_icon_from_qs_app
        +guid:756bc621-01bb-437f-acfb-af4a7449ff6f
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & EngineFirmwareFamily=Maia
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_user_created_icon_from_qs_app(spice, net, job, ews):
    try:
        updated_expected_settings_cdm = expected_cdm_for_copy_default_from_actual_cdm(ews)
        verify_create_copy_quick_set_from_ews(
            ews=ews,
            expected_settings_cdm=updated_expected_settings_cdm,
            title=copy_title_name,
            description=copy_description,
            start_option=QuickSetStartOption.start_automatically,
            copy_options=None
        )
    finally:
        logging.info("Goto qs app copy section")
        spice.quickset_ui.goto_quicksetapp_landing_view("copy")
        logging.info("wait for Quickset")
        spice.wait_for("#secondaryPanelList #secondaryPanelHeader #secondaryPanelListGrid")
        # Auto_Test_Quick_Set_Copy
        objectName = copy_title_name
        user_qs = spice.wait_for("#secondaryPanelList #secondaryPanelHeader #secondaryPanelListGrid #"+objectName+" #launcherButton #mainIcon")
        logging.info("validate user created icon")
        qs_icon = user_qs["source"]
        ucqs_path = "qrc:/images/Graphics/UserCreatedQuickset.json"
        logging.info("validate user created icon:"+qs_icon)
        assert qs_icon == ucqs_path

        factory_qs = spice.wait_for("#secondaryPanelList #secondaryPanelHeader #secondaryPanelListGrid #Image #launcherButton #mainIcon")
        qs_icon = factory_qs["source"]
        assert qs_icon != ucqs_path
        factory_qs = spice.wait_for("#secondaryPanelList #secondaryPanelHeader #secondaryPanelListGrid #Blueprint #launcherButton #mainIcon")
        qs_icon = factory_qs["source"]
        assert qs_icon != ucqs_path

        spice.goto_homescreen_back_button()
        ews.quicksets_app.csc.delete_all_shortcuts()
        logging.info("Close the current browser")
        ews.close_browser()

"""
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose: We change quickset many times as fast as posible to check there is no crash
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid: DUNE-147265
        +timeout:60
        +asset:LFP
        +delivery_team: LFP
        +feature_team: LFP_ScannerWorkflows
        +test_framework:TUF
        +name:test_copy_ui_change_quickset_in_quick_succesion
        +test:
            +title:test_copy_ui_change_quickset_in_quick_succesion
            +guid: 5ecd7710-bc7b-4f33-ac45-58d5262237a9
            +dut:
                +type:Simulator,Emulator
                +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & EngineFirmwareFamily=Maia
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_change_quickset_in_quick_succesion(spice, udw, net):
    # HomeScreen
    home = spice.main_app.get_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)

    spice.main_app.goto_copy_app()

    # CopyApp
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    quickset_id_array = [CopyAppWorkflowObjectIds.blueprint_quicksetId,CopyAppWorkflowObjectIds.mixed_content_quicksetId,
                         CopyAppWorkflowObjectIds.color_quicksetId,CopyAppWorkflowObjectIds.greyscale_quicksetId,
                         CopyAppWorkflowObjectIds.image_quicksetId,CopyAppWorkflowObjectIds.blueprint_red_stamp_quicksetId]

    # Selected quickset as fast as posible
    spice.copy_ui().copy_quickset_wait_enable_and_select_array(quickset_id_array)

    # Back To Home to set initial state again
    spice.copy_app.goto_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:UI should not crash
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-141772
    +timeout:1200
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_verify_no_crash_in_quickset
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Negative
    +test:
        +title:test_copy_ui_verify_no_crash_in_quickset
        +guid:f53fefd4-4687-47e3-89ae-79b0f8d9b5ba
        +dut:
            +type:Simulator
            +configuration: DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ADFMediaSize=A4
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_verify_no_crash_in_quickset(spice, udw, net, ews, job):
    try:
        #DUNE-208786 Setting Load media back to default (ADF) as duplex prompt is being raised 
        #in IQ because of some previous tests execution
        udw.mainApp.ScanMedia.loadMedia("ADF")
        qs = ews.quick_sets_app
        logging.info("Delete all quicksets firstly")
        qs.csc.delete_all_shortcuts()
        #Create quicksets
        copy_settings = copy.deepcopy(copy_option_combi3)
        copy_settings[CopyOptionsKey.original_size] = CopyOptions.OriginalSize.A4_210x297_mm
        copy_settings[CopyOptionsKey.paper_size] = CopyOptions.CopyPaperSize.A4_210x297mm
        for i in range(0,3):
            qs.create_copy_quick_sets(
                title=copy_quicksets_name_list[i],
                description=copy_description,
                start_option=QuickSetStartOption.user_presses_start,
                copy_options=copy_settings
            )
        logging.info("Close the current browser")
        ews.close_browser()
        home = spice.main_app.get_home()
        copy_job_app = spice.copy_ui()
        copy_job_app.goto_copy()
        for i in range(0,3):
            spice.quickset_ui.goto_viewall_menu_from_app_landing_view(quickset_type = "copy")
            job.bookmark_jobs()
            short_cut_id = qs.csc.get_shortcut_id(copy_quicksets_name_list[i])
            #logging.info('short_cut_id is ', short_cut_id)
            time.sleep(2)
            copy_job_app.select_copy_quickset("#" + short_cut_id)
            spice.quickset_ui.start_quickset_job(quickset_type="copy")
            job.wait_for_no_active_jobs()
            job.check_job_log_by_status_and_type_cdm([{"type": "copy", "status": "success"}])
            job.clear_joblog()

        # Back To Home to set initial state again
        spice.goto_homescreen()
        spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
        spice.validate_app(home, False)
    finally:
        logging.info("delete all quicksets")
        qs.delete_all_quicksets()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Validate One Touch Quickset When image preview configuration is disabled
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-186110
    +timeout:200
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_validate_onetouch_quickset_when_image_preview_configuration_disabled
    +test:
        +title:test_copy_ui_validate_onetouch_quickset_when_image_preview_configuration_disabled
        +guid:3384e86a-aa81-46b3-98d4-7e4df7326ce7
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & MediaAlerts=JamAutoNav
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator 
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_validate_onetouch_quickset_when_image_preview_configuration_disabled(cdm, spice, udw, net, job, scan_emulation):
    scan_emulation.media.unload_media("ADF")
    job_ids = job.get_recent_job_ids()
    last_job_id = job_ids[len(job_ids) - 1]
    job_ids.clear()

    # HomeScreen
    home = spice.main_app.get_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)
    try:
        ticket_default_body = Copy(cdm, udw).get_copy_default_ticket(cdm)
        default_job_ticket = copy.deepcopy(ticket_default_body)
        ticket_default_body["pipelineOptions"]["manualUserOperations"]["imagePreviewConfiguration"] = "disable"
        Copy(cdm, udw).patch_operation_on_default_copy_job_ticket(cdm, default_job_ticket)

        csc = CDMShortcuts(cdm, net)

        # delete previously added shortcut and start from fresh if needed
        csc.shortcuts_init("MyCopy")
        shortcut_id = str(uuid.uuid4())

        # Create shortcut : provide shortcutName,shortcutId,source,destinations,action,copyAllowed,isFactory: bool
        csc.create_custom_shortcut("MyCopy1", shortcut_id, "scan", ["print"], "execute", "true", False, csc.JobTicketType.COPY)
        job.bookmark_jobs()
        menu_app = spice.homeMenuUI()
        menu_app.goto_menu_quickSets_and_check_loading_screen(spice, net, quickset_type="copy")
        menu_app.select_onetouch_quickset_from_menu_quickset(spice, "#MyCopy1")
        job.wait_for_no_active_jobs()

        # wait for toast message dismiss
        # Get job details of the copy
        job_ids = job.get_recent_job_ids()
        copy_job_id = job_ids[len(job_ids) - 1]
        assert copy_job_id != last_job_id, "Copy job is missing"

        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")
    finally:
        # Go back to home screen
        spice.goto_homescreen()
        csc.delete_shortcut(shortcut_id)
        Copy(cdm, udw).patch_operation_on_default_copy_job_ticket(cdm, default_job_ticket)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Validate One Touch Quickset When image preview configuration is enabled
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-186110
    +timeout:180
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_validate_onetouch_quickset_when_image_preview_configuration_enabled
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_validate_onetouch_quickset_when_image_preview_configuration_enabled
        +guid:993d754f-1c67-48c5-bab1-e79e1cc82a42
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & MediaAlerts=JamAutoNav
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_validate_onetouch_quickset_when_image_preview_configuration_enabled(cdm, spice, udw, net, job, setup_teardown_quickset):
    # check jobId
    udw.mainApp.ScanMedia.unloadMedia("ADF")
    job_ids = job.get_recent_job_ids()
    last_job_id = job_ids[len(job_ids) - 1]
    job_ids.clear()

    # HomeScreen
    home = spice.main_app.get_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)
    try:
        # enable image preview configuration
        ticket_default_body = Copy(cdm, udw).get_copy_default_ticket(cdm)
        default_job_ticket = copy.deepcopy(ticket_default_body)
        ticket_default_body["pipelineOptions"]["manualUserOperations"]["imagePreviewConfiguration"] = "enable"
        Copy(cdm, udw).patch_operation_on_default_copy_job_ticket(cdm, default_job_ticket)

        csc = CDMShortcuts(cdm, net)

        # delete previously added shortcut and start from fresh if needed
        csc.shortcuts_init("MyCopy")
        shortcut_id = str(uuid.uuid4())

        # Create shortcut : provide shortcutName,shortcutId,source,destinations,action,copyAllowed,isFactory: bool
        csc.create_custom_shortcut("MyCopy1", shortcut_id, "scan", ["print"], "execute", "true", False, csc.JobTicketType.COPY)
        job.bookmark_jobs()
        menu_app = spice.homeMenuUI()
        menu_app.goto_menu_quickSets_and_check_loading_screen(spice, net, quickset_type="copy")
        menu_app.select_onetouch_quickset_from_menu_quickset(spice, "#MyCopy1")

        # Wait and check Copy app is expanded
        spice.copy_ui().wait_for_copy_landing_view_from_widget_or_one_touch_quickset()

        # Sometime preview screen takes time to load hence adding sleep so the click is done once preview is loaded
        time.sleep(3)
        spice.scan_settings.wait_for_preview_n(1)
        #spice.copy_ui().start_copy_after_preview()
        spice.copy_ui().start_copy_from_secondary_panel()
        menu_app.wait_for_menu_quickSets_screen(spice)
        job.wait_for_no_active_jobs()

        # wait for toast message dismiss
        # Get job details of the copy
        job_ids = job.get_recent_job_ids()
        copy_job_id = job_ids[len(job_ids) - 1]
        assert copy_job_id != last_job_id, "Copy job is missing"

        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")
    finally:
        # Go back to home screen
        spice.goto_homescreen()
        Copy(cdm, udw).patch_operation_on_default_copy_job_ticket(cdm, default_job_ticket)