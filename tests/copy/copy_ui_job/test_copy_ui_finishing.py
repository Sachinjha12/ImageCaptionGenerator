import logging
import time
import uuid
from dunetuf.cdm.CdmShortcuts import CDMShortcuts
from dunetuf.job.job import Job
from dunetuf.copy.copy import Copy
import json
import pprint
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test for staple option of Copy default option
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-142400
    +timeout:300
    +asset:Copy
    +delivery_team:A3
    +feature_team:CopySendPK
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_default_option_staple
    +test:
        +title:test_copy_ui_default_option_staple
        +guid:a7064c85-22eb-4fab-ac6e-05eb78b769e8
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ProductSpecSupported=Finisher & FinisherSettings=Staple
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_default_option_staple(spice, job, udw, net, cdm):    
    try:
        # set copy options
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().verify_copy_settings_selected_option(net, "finisher_staple", "none")
        spice.copy_ui().back_to_landing_view()

    finally:
        spice.goto_homescreen()
        spice.wait_ready()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test for staple option of Copy option
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-142400
    +timeout:300
    +asset:Copy
    +delivery_team:A3
    +feature_team:CopySendPK
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_option_staple
    +test:
        +title:test_copy_ui_option_staple
        +guid:50bf3c2c-2f6c-4440-9378-cbb33609daaa
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ProductSpecSupported=Finisher & FinisherSettings=Staple
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_option_staple(spice, job, udw, net, cdm):    
    try:
        # set copy options
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().select_staple_option("leftTwoPoints")   
        spice.copy_ui().back_to_landing_view()

    finally:
        spice.goto_homescreen()
        spice.wait_ready()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test for staple option of Copy option
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-142400
    +timeout:300
    +asset:Copy
    +delivery_team:A3
    +feature_team:CopySendPK
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_option_staple_job
    +test:
        +title:test_copy_ui_option_staple_job
        +guid:50682312-b49c-4399-b56e-351db6ebfd1a
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ProductSpecSupported=Finisher & FinisherSettings=Staple
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_option_staple_job(spice, job, udw, net, cdm):
    # check jobId
    job_ids = job.get_recent_job_ids()
    last_job_id = job_ids[len(job_ids) - 1]
    job_ids.clear()    
    
    try:
        # set copy options
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().select_staple_option("topLeftOnePointAny")   
        spice.copy_ui().back_to_landing_view()

        
        # Verify ticket values
        spice.copy_ui().start_copy()
        Copy(cdm, udw).validate_settings_used_in_copy(finisher_staple="topLeftOnePointAny")
        time.sleep(5)
        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)

        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")

    finally:
        spice.goto_homescreen()
        spice.wait_ready()
                
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test for punch option of Copy default option
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-142400
    +timeout:300
    +asset:Copy
    +delivery_team:A3
    +feature_team:CopySendPK
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_default_option_punch
    +test:
        +title:test_copy_ui_default_option_punch
        +guid:e4d54bcb-e9a2-4fac-a3e3-f983bc9d7d36
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ProductSpecSupported=Finisher & FinisherSettings=HolePunch
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_default_option_punch(spice, job, udw, net, cdm):    
    try:
        # set copy options
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        logging.info("Verify the value displayed for blank page suppression")
        spice.copy_ui().verify_copy_settings_selected_option(net, "finisher_punch", "none")
        spice.copy_ui().back_to_landing_view()

    finally:
        spice.goto_homescreen()
        spice.wait_ready()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test for punch option of Copy option
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-142400
    +timeout:300
    +asset:Copy
    +delivery_team:A3
    +feature_team:CopySendPK
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_option_punch
    +test:
        +title:test_copy_ui_option_punch
        +guid:e7b97b68-be3f-4dd0-862c-cc1ef8ba9784
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ProductSpecSupported=Finisher & FinisherSettings=HolePunch
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_option_punch(spice, job, udw, net, cdm):    
    try:
        # set copy options
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().select_punch_option("leftTwoPointDin")
    
        spice.copy_ui().back_to_landing_view()

    finally:
        spice.goto_homescreen()
        spice.wait_ready()    

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test for punch option of Copy option
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-142400
    +timeout:300
    +asset:Copy
    +delivery_team:A3
    +feature_team:CopySendPK
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_option_punch_job
    +test:
        +title:test_copy_ui_option_punch_job
        +guid:b27c7a20-42af-4b4f-a2e2-0cac3b1880df
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ProductSpecSupported=Finisher & FinisherSettings=HolePunch
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_option_punch_job(spice, job, udw, net, cdm):
    # check jobId
    job_ids = job.get_recent_job_ids()
    last_job_id = job_ids[len(job_ids) - 1]
    job_ids.clear()    
    
    try:
        # set copy options
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().select_punch_option("rightTwoPointDin")   
        spice.copy_ui().back_to_landing_view()

        
        # Verify ticket values
        spice.copy_ui().start_copy()
        Copy(cdm, udw).validate_settings_used_in_copy(finisher_punch= "rightTwoPointDin")
        time.sleep(5)
        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)

        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")

    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test for fold option of Copy default option
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-184313
    +timeout:300
    +asset:Copy
    +delivery_team:A3
    +feature_team:CopySendPK
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_default_option_fold
    +test:
        +title:test_copy_ui_default_option_fold
        +guid:fd9dbd21-4eec-436b-ac41-b4a11763627b
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ProductSpecSupported=Finisher & FinisherSettings=BookletMaker
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_default_option_fold(spice, job, udw, net, cdm):    
    try:
        # set copy options
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().verify_copy_settings_selected_option(net, "finisher_fold", "none")
        spice.copy_ui().back_to_landing_view()

    finally:
        spice.goto_homescreen()
        spice.wait_ready()     
 

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test for Vfold option of Copy option
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-184313
    +timeout:300
    +asset:Copy
    +delivery_team:A3
    +feature_team:CopySendPK
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_option_Vfold_job
    +test:
        +title:test_copy_ui_option_Vfold_job
        +guid:32acbb64-1760-4755-9299-62884000c5d7
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ProductSpecSupported=Finisher & FinisherSettings=BookletMaker
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_option_Vfold_job(spice, job, udw, net, cdm):
    # check jobId
    job_ids = job.get_recent_job_ids()
    last_job_id = job_ids[len(job_ids) - 1]
    job_ids.clear()    
    
    try:
        # set copy options
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().select_fold_option("V-fold")   
        spice.copy_ui().back_to_landing_view()
        
        # Verify ticket values
        spice.copy_ui().start_copy()
        Copy(cdm, udw).validate_settings_used_in_copy(finisher_fold= "vInwardTop")
        time.sleep(5)
        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)

        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")

    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test for Vfold option of Copy option
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-184313
    +timeout:300
    +asset:Copy
    +delivery_team:A3
    +feature_team:CopySendPK
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_option_Cfold_job
    +test:
        +title:test_copy_ui_option_Cfold_job
        +guid:f0669ac6-de61-417a-96cf-72367db45ec5
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ProductSpecSupported=Finisher & FinisherSettings=BookletMaker
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_option_Cfold_job(spice, job, udw, net, cdm):
    # check jobId
    job_ids = job.get_recent_job_ids()
    last_job_id = job_ids[len(job_ids) - 1]
    job_ids.clear()    
    
    try:
        # set copy options
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().select_fold_option("C-fold")   
        spice.copy_ui().back_to_landing_view()
        
        # Verify ticket values
        spice.copy_ui().start_copy()
        Copy(cdm, udw).validate_settings_used_in_copy(finisher_fold= "cInwardTop")
        time.sleep(5)
        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)

        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")

    finally:
        spice.goto_homescreen()
        spice.wait_ready()
            
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test for bookletMaker option of Copy default option
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-208846
    +timeout:300
    +asset:Copy
    +delivery_team:A3
    +feature_team:CopySendPK
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_default_option_booklet_maker
    +test:
        +title:test_copy_ui_default_option_booklet_maker
        +guid:e73193f4-f5f6-4c76-b0d1-9be3a0a39763
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ProductSpecSupported=Finisher & FinisherSettings=BookletMaker
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_default_option_booklet_maker(spice, job, udw, net, cdm):    
    try:
        # set copy options
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().verify_copy_settings_selected_option(net, "finisher_booklet", "off")
        spice.copy_ui().back_to_landing_view()

    finally:
        spice.goto_homescreen()
        spice.wait_ready() 

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test for foldAndStitch option of Copy option
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-208846
    +timeout:300
    +asset:Copy
    +delivery_team:A3
    +feature_team:CopySendPK
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_option_booklet_maker_job
    +test:
        +title:test_copy_ui_option_booklet_maker_job
        +guid:9f564e8d-b79d-4d53-8673-5329d4cbc152
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ProductSpecSupported=Finisher & FinisherSettings=BookletMaker
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_option_booklet_maker_job(spice, job, udw, net, cdm):
    # check jobId
    job_ids = job.get_recent_job_ids()
    last_job_id = job_ids[len(job_ids) - 1]
    job_ids.clear()    
    
    try:
        # set copy options
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().select_booklet_option('foldAndStitch')   
        spice.copy_ui().back_to_landing_view()
        
        # Verify ticket values
        spice.copy_ui().start_copy()
        Copy(cdm, udw).validate_settings_used_in_copy(finisher_booklet = "saddleStitch")
        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)

        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")

    finally:
        spice.goto_homescreen()
        spice.wait_ready()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test for foldAndStitch option of Copy option
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-208846
    +timeout:300
    +asset:Copy
    +delivery_team:A3
    +feature_team:CopySendPK
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_option_booklet_maker_custom_job
    +test:
        +title:test_copy_ui_option_booklet_maker_custom_job
        +guid:47b82b2a-3ab2-4963-8fec-1a7bdce6e4d8
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ProductSpecSupported=Finisher & FinisherSettings=BookletMaker
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_option_booklet_maker_custom_job(spice, job, udw, net, cdm):
    # check jobId
    job_ids = job.get_recent_job_ids()
    last_job_id = job_ids[len(job_ids) - 1]
    job_ids.clear()    
    
    try:
        # set copy options
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().select_booklet_option('foldAndStitch')
        time.sleep(10)
        spice.copy_ui().select_booklet_option('foldAndStitch_Custom')   
        spice.copy_ui().back_to_landing_view()
        
        # Verify ticket values
        spice.copy_ui().start_copy()
        Copy(cdm, udw).validate_settings_used_in_copy(finisher_booklet = "saddleStitch")
        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)

        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")

    finally:
        spice.goto_homescreen()
        spice.wait_ready()

