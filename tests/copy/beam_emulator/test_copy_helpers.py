import pytest
import logging
import re
from typing import List
from time import sleep

from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.localization.LocalizationHelper import LocalizationHelper

def get_messages_on_screen(spice) -> List[str]:
    """
    In copy we have multiple views, all with the same ID. This will return the texts of
    all active views.
    :param spice:
    :return: All texts in screen with the ID print_done_status_message
    """
    current_index = 0
    found = []
    while True:
        candidate = None
        try:
            candidate = spice.query_item(MenuAppWorkflowObjectIds.print_done_status_message, query_index=current_index)
        except Exception:
            # item not found (exceeded max index?); exit
            return found

        try:
            if candidate["visible"] and candidate["enabled"]:
                # match
                found.append(candidate["text"])
        except:
            pass

        # continue searching until no more IDs
        current_index += 1
    # never reaches

def wait_for_print_menu_text(expected_final_msg_id: str, spice, net, locale: str = "en-US", *id_params_ids) -> str:
    """
    Waits for a certain menu message to show in the printing workflow.
    :param expected_final_msg_id: ID of the final message
    :param spice:
    :param net:
    :param locale: Printer language
    :param id_params_ids: List of IDs to be replaced in expected_final_msg_id
    :return: Got text
    """
    expected_screen_msg = str(LocalizationHelper.get_string_translation(net, expected_final_msg_id, locale))
    args_regex = re.compile(r'%\d+\$[ds]')
    for arg_id in id_params_ids:
        param_msg = str(LocalizationHelper.get_string_translation(net, arg_id, locale))
        logging.debug(f"Replacing param of '{expected_final_msg_id}' by '{param_msg}' (result of '{arg_id}')...")
        if not args_regex.search(expected_screen_msg):
            raise Exception("Couldn't replace string argument: no arguments left")

        expected_screen_msg = args_regex.sub(param_msg, expected_screen_msg, 1)
    logging.info(f"Waiting for '{expected_screen_msg}' in copy screen...")

    tries = 20 # 1s/try => 20s
    got_end_status_msgs = None
    while tries >= 0:
        got_end_status_msgs = get_messages_on_screen(spice)
        if expected_screen_msg in got_end_status_msgs:
            break # we're done

        # try again
        tries -= 1
        sleep(1)

    if got_end_status_msgs is None:
        raise TimeoutException(f"Couldn't find end message (id '{MenuAppWorkflowObjectIds.print_done_status_message}')")

    assert expected_screen_msg in got_end_status_msgs, \
            f"Expected copy status message to be '{expected_screen_msg}', but got a different message: '{got_end_status_msgs}'"

    return expected_screen_msg

def wait_for_print_to_complete(expected_final_msg_id: str, spice, net, locale: str = "en-US", *id_params_ids):
    """
    Waits for the 'done printing' screens and returns the
    button to close the screen and the info message.
    :param expected_final_msg_id: ID of the final message
    :param spice:
    :param net:
    :param locale: Printer language
    :param id_params_ids: List of IDs to be replaced in expected_final_msg_id
    :return: Tuple with the button to close the screen and the text reported
    """
    got_end_status_msg = wait_for_print_menu_text(expected_final_msg_id, spice, net, locale, *id_params_ids)
    finish_btn = spice.wait_for(MenuAppWorkflowObjectIds.ok_copy_button, timeout=1)

    return (finish_btn,got_end_status_msg)