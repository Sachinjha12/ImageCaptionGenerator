import logging
import time
import json
from dunetuf.ews.pom.quick_sets.Locators import Locators
from dunetuf.ews.pom.quick_sets.quicksets_enum import *
from tests.copy.quicksets.copy_combination import *


def copy_job_from_fp_menu_quickset(spice, net, job, copy_name, start_option=QuickSetStartOption.start_automatically):
    """

    @param spice:
    @param net:
    @param job:
    @param copy_name:
    @param start_option:
    @return:
    """
    job.bookmark_jobs()
    menu_app = spice.homeMenuUI()
    logging.info("Perform quickset job from FP of menu app")
    menu_app.goto_menu_quickSets_and_check_loading_screen(spice, net, quickset_type="copy")
    menu_app.select_copy_quickset_from_menu_quickset(spice, f"#{copy_name}", start_option)

    if start_option == QuickSetStartOption.user_presses_start:
        spice.copy_ui().start_copy()

    wait_for_copy_complete_successfully(spice)
    check_job_log_from_cdm(job)

    # go to homescreen
    spice.goto_homescreen()


def copy_job_from_fp_menu_copy(spice, net, job, copy_name, configuration):
    """

    @param spice:
    @param net:
    @param job:
    @param copy_name:
    @return:
    """
    job.bookmark_jobs()
    logging.info("Perform quickset job from FP of menu app")
    menu_app = spice.homeMenuUI()
    if configuration.familyname == "enterprise":
        menu_app.goto_menu(spice)
    else:
        menu_app.goto_menu_copy(spice)
        spice.copy_ui().check_copy_home_screen_under_menu_app(spice, net)
    menu_app.goto_document(spice)
    spice.copy_ui().check_copy_default_screen(spice, net)
    spice.copy_ui().goto_copy_quickset_view()
    spice.copy_ui().select_copy_quickset(f"#{copy_name}")
    spice.copy_ui().start_copy()
    logging.info("check the ui status after copy")
    spice.copy_ui().wait_for_copy_job_status_toast_or_modal(net, configuration, timeout=450)
    wait_for_copy_complete_successfully(spice)
    check_job_log_from_cdm(job)
    # go to homescreen
    spice.goto_homescreen()


def copy_job_from_fp_copy_app(spice, net, job, copy_name, configuration):
    """

    @param spice:
    @param job:
    @param sharepoint_name:
    @return:
    """
    job.bookmark_jobs()
    copy_app = spice.copy_ui()

    logging.info("Perform quickset job from FP of copy app")
    copy_app.goto_copy_from_copyapp_at_home_screen()
    copy_app.check_copy_default_screen(spice, net)
    copy_app.goto_copy_quickset_view()
    copy_app.select_copy_quickset(f"#{copy_name}")
    copy_app.start_copy()
    copy_app.wait_for_copy_job_status_toast_or_modal(net, configuration,timeout = 450)
    logging.info("check the ui status after copy")

    wait_for_copy_complete_successfully(spice)
    check_job_log_from_cdm(job)

    # go to homescreen
    spice.goto_homescreen()


def verify_create_copy_quick_set_from_ews(ews, expected_settings_cdm, title, description=None,
                                          start_option: QuickSetStartOption = None, copy_options: dict = None):
    """
    Delete the identical quick set and create quick set with specific setting
    For checking point of copy setting of expected_settings, please refer to info at bottom 'Sample for expected_settings for function "check_with_cdm_on_ews_quick_sets_copy"'
    @param ews:
    @param expected_settings_cdm: refer to info at bottom 'Sample for expected_settings for function "check_with_cdm_on_ews_quick_sets_copy"'
    @param title: quickset name
    @param description:
    @param start_option:
    @param copy_options: scan options for quickset
    @return:
    """
    qs = ews.quick_sets_app
    logging.info("before create, check it already created or not. if yes, delete it.")
    qs.csc.delete_all_shortcuts()
    logging.info("Create quick set with corresponding settings")
    qs.create_copy_quick_sets(
        title=title,
        description=description,
        start_option=start_option,
        copy_options=copy_options
    )

    logging.info("Verify if quick set is listed in EWS")
    qs_index = qs.find_quick_set_by_title(title)
    assert qs_index != -1, f"Failed to create "

    logging.info("Validate newly added quick set from CDM")
    check_with_cdm_on_ews_quick_sets_copy(qs, title, expected_settings_cdm)

def verify_copy_quality_options(quick_set_app, expected_setting):
    actual_settings = quick_set_app.csc.get_quicksets_created_capabilities_by_title(copy_title_name)
    printQualitySetting = actual_settings["settings_info"]["dest"]["print"]["printQuality"]

    assert printQualitySetting == expected_setting, "Print Quality setting was not set correctly."

def verify_create_copy_quick_set_from_ews_standard_doc_add_pages(ews, expected_settings_cdm, title, description=None,
                                          start_option: QuickSetStartOption = None, copy_options: dict = None):
    """
    Delete the identical quick set and create quick set with specific setting
    For checking point of copy setting of expected_settings, please refer to info at bottom 'Sample for expected_settings for function "check_with_cdm_on_ews_quick_sets_copy"'
    @param ews:
    @param expected_settings_cdm: refer to info at bottom 'Sample for expected_settings for function "check_with_cdm_on_ews_quick_sets_copy"'
    @param title: quickset name
    @param description:
    @param start_option:
    @param copy_options: scan options for quickset
    @return:
    """
    qs = ews.quick_sets_app
    logging.info("before create, check it already created or not. if yes, delete it.")
    qs.csc.delete_all_shortcuts()
    logging.info("Create quick set with corresponding settings")
    qs.create_copy_quick_sets(
        title=title,
        description=description,
        start_option=start_option,
        copy_options=copy_options
    )

    logging.info("Verify if quick set is listed in EWS")
    qs_index = qs.find_quick_set_by_title(title)
    assert qs_index != -1, f"Failed to create "

    logging.info("Validate newly added quick set from CDM")
    check_with_cdm_on_ews_quick_sets_copy_standard_doc_add_pages(qs, title, expected_settings_cdm)


def check_with_cdm_on_ews_quick_sets_copy(quick_set_app, quick_set_title, expected_settings: dict):
    """
    Check with cmd for configuration of quick set
    For checking point of copy setting of expected_settings, please refer to info at bottom 'Sample for expected_settings for function "check_with_cdm_on_ews_quick_sets_copy"'
    @param quick_set_app:
    @param quick_set_title: quickset name
    @param expected_settings: refer to info at bottom 'Sample for expected_settings for function "check_with_cdm_on_ews_quick_sets_copy"'
    @return:
    """
    actual_settings = quick_set_app.csc.get_quicksets_created_capabilities_by_title(quick_set_title)
    # pick up the paramters that need to be validate
    scan_setting = actual_settings["settings_info"]["src"]["scan"]
    scaling_setting = actual_settings["settings_info"]["pipelineOptions"]["scaling"]
    print_setting = actual_settings["settings_info"]["dest"]["print"]

    validated_settings = {
        "summary_info": actual_settings["summary_info"],
        "settings_info": {
            "src": {
                "scan": {
                    "colorMode": scan_setting["colorMode"],
                    "mediaSource": scan_setting["mediaSource"],
                    "mediaSize": scan_setting["mediaSize"],
                    "plexMode": scan_setting["plexMode"],
                    "contentType": scan_setting["contentType"],
                    "contentOrientation": scan_setting["contentOrientation"],
                    "pagesFlipUpEnabled": scan_setting["pagesFlipUpEnabled"]
                }
            },
            "pipelineOptions": {
                "imageModifications": {
                    "exposure" : actual_settings["settings_info"]["pipelineOptions"]["imageModifications"]["exposure"]
                },
                "scaling": {
                    "scaleToFitEnabled": scaling_setting["scaleToFitEnabled"],
                    "xScalePercent": scaling_setting["xScalePercent"],
                    "yScalePercent": scaling_setting["yScalePercent"],
                    "scaleSelection": scaling_setting["scaleSelection"]
                }
            },
            "dest": {
                "print":{
                    "collate": print_setting["collate"],
                    "copies": print_setting["copies"], 
                    "mediaSource": print_setting["mediaSource"], 
                    "mediaSize": print_setting["mediaSize"], 
                    "mediaType": print_setting["mediaType"],
                    "plexMode": print_setting["plexMode"],
                    "duplexBinding": print_setting["duplexBinding"],
                    "printQuality": print_setting["printQuality"]
                }
            }
        }
    }

    logging.info(f"Need to validated setting is: <{validated_settings}>")
    check_json(expected_settings, validated_settings)

def check_with_cdm_on_ews_quick_sets_copy_standard_doc_add_pages(quick_set_app, quick_set_title, expected_settings: dict):
    """
    Check with cmd for configuration of quick set
    For checking point of copy setting of expected_settings, please refer to info at bottom 'Sample for expected_settings for function "check_with_cdm_on_ews_quick_sets_copy"'
    @param quick_set_app:
    @param quick_set_title: quickset name
    @param expected_settings: refer to info at bottom 'Sample for expected_settings for function "check_with_cdm_on_ews_quick_sets_copy"'
    @return:
    """
    actual_settings = quick_set_app.csc.get_quicksets_created_capabilities_by_title(quick_set_title)
    # pick up the paramters that need to be validate
    scan_setting = actual_settings["settings_info"]["src"]["scan"]
    scaling_setting = actual_settings["settings_info"]["pipelineOptions"]["scaling"]
    print_setting = actual_settings["settings_info"]["dest"]["print"]

    validated_settings = {
        "summary_info": actual_settings["summary_info"],
        "settings_info": {
            "src": {
                "scan": {
                    "colorMode": scan_setting["colorMode"],
                    "mediaSource": scan_setting["mediaSource"],
                    "mediaSize": scan_setting["mediaSize"],
                    "plexMode": scan_setting["plexMode"],
                    "contentType": scan_setting["contentType"],
                    "contentOrientation": scan_setting["contentOrientation"],
                    "pagesFlipUpEnabled": scan_setting["pagesFlipUpEnabled"],
                    "scanCaptureMode": scan_setting["scanCaptureMode"]
                }
            },
            "pipelineOptions": {
                "imageModifications": {
                    "exposure" : actual_settings["settings_info"]["pipelineOptions"]["imageModifications"]["exposure"]
                },
                "scaling": {
                    "scaleToFitEnabled": scaling_setting["scaleToFitEnabled"],
                    "xScalePercent": scaling_setting["xScalePercent"],
                    "yScalePercent": scaling_setting["yScalePercent"],
                    "scaleSelection": scaling_setting["scaleSelection"]
                },
                "promptForAdditionalPages": actual_settings["settings_info"]["pipelineOptions"]["promptForAdditionalPages"]
            },
            "dest": {
                "print":{
                    "collate": print_setting["collate"],
                    "copies": print_setting["copies"],
                    "mediaSource": print_setting["mediaSource"],
                    "mediaSize": print_setting["mediaSize"],
                    "mediaType": print_setting["mediaType"],
                    "plexMode": print_setting["plexMode"],
                    "duplexBinding": print_setting["duplexBinding"],
                    "printQuality": print_setting["printQuality"]
                }
            }
        }
    }

    logging.info(f"Need to validated setting is: <{validated_settings}>")
    check_json(expected_settings, validated_settings)

def check_with_cdm_on_ews_quick_sets_copy_custom(quick_set_app, quick_set_title, expected_settings: dict):
    """
    Check with cmd for configuration of quick set
    For checking point of copy setting of expected_settings, please refer to info at bottom 'Sample for expected_settings for function "check_with_cdm_on_ews_quick_sets_copy"'
    @param quick_set_app:
    @param quick_set_title: quickset name
    @param expected_settings: refer to info at bottom 'Sample for expected_settings for function "check_with_cdm_on_ews_quick_sets_copy"'
    @return:
    """
    actual_settings = quick_set_app.csc.get_quicksets_created_capabilities_by_title(quick_set_title)
    # pick up the paramters that need to be validate
    scan_setting = actual_settings["settings_info"]["src"]["scan"]
    scaling_setting = actual_settings["settings_info"]["pipelineOptions"]["scaling"]
    print_setting = actual_settings["settings_info"]["dest"]["print"]

    validated_settings = {
        "summary_info": actual_settings["summary_info"],
        "settings_info": {
            "src": {
                "scan": {
                    "colorMode": scan_setting["colorMode"],
                    "mediaSource": scan_setting["mediaSource"],
                    "mediaSize": scan_setting["mediaSize"],
                    "plexMode": scan_setting["plexMode"],
                    "contentType": scan_setting["contentType"],
                    "contentOrientation": scan_setting["contentOrientation"],
                    "pagesFlipUpEnabled": scan_setting["pagesFlipUpEnabled"]
                }
            },
            "pipelineOptions": {
                "imageModifications": {
                    "exposure" : actual_settings["settings_info"]["pipelineOptions"]["imageModifications"]["exposure"]
                },
                "scaling": {
                    "scaleToFitEnabled": scaling_setting["scaleToFitEnabled"],
                    "xScalePercent": scaling_setting["xScalePercent"],
                    "yScalePercent": scaling_setting["yScalePercent"],
                    "scaleSelection": scaling_setting["scaleSelection"]
                }
            },
            "dest": {
                "print":{
                    "collate": print_setting["collate"],
                    "copies": print_setting["copies"], 
                    "mediaSource": print_setting["mediaSource"], 
                    "mediaSize": print_setting["mediaSize"],
                    "customMediaXFeedDimension": print_setting["customMediaXFeedDimension"],
                    "customMediaYFeedDimension": print_setting["customMediaYFeedDimension"],
                    "mediaType": print_setting["mediaType"],
                    "plexMode": print_setting["plexMode"],
                    "duplexBinding": print_setting["duplexBinding"],
                    "printQuality": print_setting["printQuality"]
                }
            }
        }
    }

    logging.info(f"Need to validated setting is: <{validated_settings}>")
    check_json(expected_settings, validated_settings)

def check_json(expected_json: dict, actual_json: dict):
    """
    Compare two json
    @param expected_json:
    @param actual_json:
    @return:
    """
    logging.info(f"expected_data is <{json.dumps(expected_json, ensure_ascii=False)}>")
    logging.info(f"actual_data is <{json.dumps(actual_json, ensure_ascii=False)}>")

    expected_data = ordered(expected_json)
    actual_data = ordered(actual_json)

    result = expected_data == actual_data
    assert result, "Failed to check json"

    logging.info("Json result checking is pass")


def expected_cdm_for_copy_default_from_actual_cdm(ews):
    """
    Check data configuration with cdm
    @param: actual_settings ->  for checking field, please refer to bottom sample data
    @return:
    """
    # pick up the paramters that need to be validate
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()

    scan_setting = default_value["src"]["scan"]
    imageModifications_settings = default_value["pipelineOptions"]["imageModifications"]
    scaling_setting = default_value["pipelineOptions"]["scaling"]
    print_setting = default_value["dest"]["print"]
    validated_settings = {
        "summary_info": {
            "title": "Auto_Test_Quick_Set_Copy",
            "description": "Just For Auto Test",
            "action": "execute"
        },
        "settings_info": { 
            "src": {
                "scan": {
                    "colorMode": scan_setting["colorMode"],
                    "mediaSource": scan_setting["mediaSource"],
                    "mediaSize": scan_setting["mediaSize"],
                    "plexMode": scan_setting["plexMode"],
                    "contentType": scan_setting["contentType"],
                    "contentOrientation": scan_setting["contentOrientation"],
                    "pagesFlipUpEnabled": scan_setting["pagesFlipUpEnabled"]
                }
            },
            "pipelineOptions": {
                "imageModifications": {
                    "exposure": imageModifications_settings["exposure"]
                },
                "scaling": {
                    "scaleToFitEnabled": scaling_setting["scaleToFitEnabled"],
                    "xScalePercent": scaling_setting["xScalePercent"],
                    "yScalePercent": scaling_setting["yScalePercent"],
                    "scaleSelection": scaling_setting["scaleSelection"]
                }
            },
            "dest": {
                "print": {
                    "collate": print_setting["collate"],
                    "copies": print_setting["copies"],
                    "mediaSource": print_setting["mediaSource"],
                    "mediaSize": print_setting["mediaSize"],
                    "mediaType": print_setting["mediaType"],
                    "plexMode": print_setting["plexMode"],
                    "duplexBinding": print_setting["duplexBinding"],
                    "printQuality": print_setting["printQuality"]
                }
            }
        }
    }

    return validated_settings


def ordered(obj):
    """
    Order the obj
    @param obj:
    @return:
    """
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


def get_local_time():
    """
    Get local time str
    @return:
    """
    return time.strftime("%Y%m%d%H%M%S", time.localtime())


def wait_for_copy_complete_successfully(spice, time_out=300):
    """
    Wait for copy job complete
    @param time_out:
    @return:
    """
    # todo: need to update this function after Job Status Toast Messages implement, at present using self.get_current_job_status("usbPrint") to check job complete
    # self._spice.wait_for(self.print_done_view, time_out)
    # start_obj = "#ToastInfoText"
    # self._spice.wait_for(start_obj, 10)

    job_info_url = get_current_job_url(spice, "copy")

    if job_info_url:
        current_job_status = get_current_job_status(spice, job_info_url)

        while current_job_status != "completed" and time_out > 0:
            time_out = time_out - 1
            time.sleep(1)
            current_job_status = get_current_job_status(spice, job_info_url)

        assert current_job_status == "completed", f"Print job is not complete in time {time_out}"
        logging.info("print job finished")
    else:
        logging.warning("Failed to get job status from job queue, will check it with job history")


def get_current_job_url(spice, current_job_type="copy"):
    # todo: need to move this function into job.py since this function in other branch and wait for merge into default
    logging.info("To get the current active print job status from CDM")
    job_queue = spice.cdm.get(spice.cdm.JOB_QUEUE_ENDPOINT)
    job_list = job_queue.get("jobList")
    job_info_url = None

    get_job_queue_time_out = 20
    while len(job_list) == 0 and get_job_queue_time_out > 0:
        get_job_queue_time_out = get_job_queue_time_out - 1
        time.sleep(1)
        job_queue = spice.cdm.get(spice.cdm.JOB_QUEUE_ENDPOINT)
        job_list = job_queue.get("jobList")

    logging.info("job_queue is: " + str(job_queue))

    for job_item in job_list:
        if job_info_url:
            break

        job_type = job_item.get("jobType")

        if job_type == current_job_type:
            links = job_item.get("links")

            for link_item in links:
                rel = link_item.get("rel")
                if rel == "job":
                    job_info_url = link_item.get("href")
                    break

    if job_info_url:
        return job_info_url

    logging.warning(f"Failed to get job_info_url in job list: {job_list}")
    return None


def get_current_job_status(spice, job_info_url):
    current_job_info = spice.cdm.get(job_info_url)
    logging.info(f'Current job id is {current_job_info["jobId"]}, status is: {current_job_info["state"]}')
    return current_job_info["state"]


def check_job_log_from_cdm(job, completion_state_list=["success"], time_out=300):
    """
    Check the job from cdm
    make sure invoke function job.bookmark_jobs() before performing a job
    @param job:
    @param completion_state_list:[success, cancelled]
    @param time_out:
    @return:
    """
    logging.info("check the job log from cdm")
    while len(job.get_newjobs()) == 0 and time_out:
        time.sleep(1)
        time_out = time_out - 1

    assert len(job.get_newjobs()) == len(completion_state_list), "Failed to get all job log"

    for i, completion_state in enumerate(completion_state_list):
        logging.info(f"The index {i}，value is {completion_state}")
        actual_status = job.wait_for_job_completion_cdm(job.get_newjobs()[i]["jobId"])
        assert actual_status == completion_state, f"Job status is not correct, expected status should be <{completion_state}>, actual status is <{actual_status}>"

def check_quickset_order_by_quick_set_name(qs_app):
    """
    Check quickset sorted mode with quickset name
    @param qs_app:
    @return:
    """
    qs_app.load_self()

    # Click quick set name to order quickset
    qs_app.click_quickset_name_on_summary_table()
    qs_app.check_sorted_mode_with_quickset_name("ascending")
    order_brief_info = qs_app.get_all_quick_sets_brief_info()
    order_title_list = order_brief_info["title_list"]
    assert order_title_list == quicksets_name_list, "Failed to sort in ascending order by click quick set name"
    logging.info("Quickset list as per alphbetical order successful")

    qs_app.click_quickset_name_on_summary_table()
    qs_app.check_sorted_mode_with_quickset_name("descending")
    reverse_order_brief_info = qs_app.get_all_quick_sets_brief_info()
    reverse_order_title_list = reverse_order_brief_info["title_list"]
    assert reverse_order_title_list == quicksets_name_list[::-1], "Failed to order quick set name by click quick set name"
    logging.info("Quickset list as per reverse alphbetical order successful")

def check_quickset_order_by_quick_set_type(qs_app):
    """
    Check quickset sorted mode with quickset type
    @param qs_app:
    @return:
    """
    qs_app.load_self()
    brief_info = qs_app.get_all_quick_sets_brief_info()
    type_list = brief_info["quick_set_type_list"]
    type_list_ascending = sorted(type_list)
    type_list_descending = sorted(type_list, reverse=True)

    # Click quick set type to order quickset
    qs_app.click_quickset_type_on_summary_table()
    qs_app.check_sorted_mode_with_quickset_type("ascending")
    order_brief_info = qs_app.get_all_quick_sets_brief_info()
    order_type_list = order_brief_info["quick_set_type_list"]
    assert order_type_list == type_list_ascending, "Failed to order quick set type by click quick set type"
    logging.info("Quickset type as per alphbetical order successful")
    
    qs_app.click_quickset_type_on_summary_table()
    qs_app.check_sorted_mode_with_quickset_type("descending")
    reverse_order_brief_info = qs_app.get_all_quick_sets_brief_info()
    reverse_order_type_list = reverse_order_brief_info["quick_set_type_list"]
    assert reverse_order_type_list == type_list_descending, "Failed to order quick set type by click quick set type"
    logging.info("Quickset type as per reverse alphbetical order successful")

def check_quickset_order_by_start_option(qs_app):
    """
    Check quickset sorted mode with quickset start option
    @param qs_app:
    @return:
    """
    qs_app.load_self()    
    brief_info = qs_app.get_all_quick_sets_brief_info()
    title_list = brief_info["title_list"]
    start_immediately_title_list = []
    user_presses_start_title_list = []
    for title in title_list:
        icon_locator = qs_app._locators.start_immediately_icon_locator(title)
        is_icon_visible = qs_app._helper.is_element_visible(icon_locator)
        if is_icon_visible != False:
            start_immediately_title_list.append(title)
        else:
            user_presses_start_title_list.append(title)

    # Click start immediately to order quickset
    qs_app.click_start_immediately_on_summary_table()
    qs_app.check_sorted_mode_with_quickset_start_option("ascending")
    order_brief_info = qs_app.get_all_quick_sets_brief_info()
    order_title_list = order_brief_info["title_list"]
    assert order_title_list[0:len(start_immediately_title_list)] == start_immediately_title_list
    logging.info("Quickset list is sorted by start option in ascending order successful")

    qs_app.click_start_immediately_on_summary_table()
    qs_app.check_sorted_mode_with_quickset_start_option("descending")
    reverse_order_brief_info = qs_app.get_all_quick_sets_brief_info()
    reverse_order_title_list = reverse_order_brief_info["title_list"]
    assert reverse_order_title_list[0:len(user_presses_start_title_list)] == user_presses_start_title_list
    logging.info("Quickset list is sorted by start option in descending order successful")

"""
Sample for expected_settings for function "check_with_cdm_on_ews_quick_sets_copy"
{
	"summary_info": {
		"title": "Auto_Test_Quick_Set_Copy",
		"description": "Just For Auto Test",
		"action": "execute"
	},
	"settings_info": {
		"src": {
			"scan": {
				"colorMode": "color",
				"mediaSource": "adf",
				"mediaSize": "na_letter_8.5x11in",
				"plexMode": "simplex",
				"contentType": "mixed",
				"contentOrientation": "portrait",
				"pagesFlipUpEnabled": "false"
			}
		},
		"pipelineOptions": {
			"imageModifications": {
				"exposure": 5
			},
			"scaling": {
				"scaleToFitEnabled": "true",
				"xScalePercent": 100,
				"yScalePercent": 100,
				"scaleSelection": "none",
                "scaleToOutput": "tray_1",
				"scaleToSize": "na_letter_8.5x11in"
			}
		},
		"dest": {
			"print": {
				"collate": "collated",
				"copies": 1,
				"mediaSource": "auto",
				"mediaSize": "na_letter_8.5x11in",
				"mediaType": "stationery",
				"plexMode": "simplex",
				"duplexBinding": "oneSided",
				"printQuality": "normal"
			}
		}
	}
}
"""
