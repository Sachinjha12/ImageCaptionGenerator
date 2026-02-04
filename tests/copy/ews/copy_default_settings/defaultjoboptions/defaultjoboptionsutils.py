#########################################################################################
# @file      defaultjoboptionsutils.py
# @author    Mike Burton (michael.burton1@hp.com)
#            heavily leveraged from Bikas K B (bikas.kb@hp.com)
# @date      6-11-2021
# @brief     Operations required for EWS verification of Default Job Options
# (c) Copyright HP Inc. 2020. All rights reserved.
###########################################################################################
import logging
import time
from enum import Enum
from dunetuf.cdm import CDM

class JobType(Enum):
    """ Def JobType type names used in EWS """
    COPY = 'copy'
    SCAN_EMAIL = 'scanEmail'
    SCAN_NETWORK_FOLDER = 'scanNetworkFolder'
    SCAN_USB = 'scanUsb'
    SCAN_SHAREPOINT = 'scanSharePoint'

class DefaultJobOptionsUtils:
    media_size_dict = {
        'any':'Any Size',
        'iso_b2_500x707mm':'B2',
        'iso_b3_353x500mm':'B3',
        'iso_b4_250x353mm':'B4',
        'iso_b6_125x176mm':'B5',
        'iso_a0_841x1189mm':'A0',
        'iso_a1_594x841mm':'A1',
        'iso_a2_420x594mm':'A2',
        'iso_a3_297x420mm':'A3 (297x420 mm)',
        'iso_a4_210x297mm':'A4 (210x297 mm)',
        'com.hp.ext.mediaSize.iso_a4_210x297mm.rotated':'A4 ▭ (210x297 mm)',
        'iso_a5_148x210mm':'A5 (148x210 mm)',
        'com.hp.ext.mediaSize.iso_a5_148x210mm.rotated':'A5 ▭ (148x210 mm)',
        'iso_a6_105x148mm':'A6 (105x148 mm)',
        'iso_c6_114x162mm':'C6',
        'na_letter_8.5x11in':'Letter (8.5x11 in.)',
        'com.hp.ext.mediaSize.na_letter_8.5x11in.rotated' : 'Letter ▭ (8.5x11 in.)',
        'na_govt-letter_8x10in':'Letter (8inx10in)',
        'na_legal_8.5x14in':'Legal (8.5x14 in.)',
        'na_ledger_11x17in':'Ledger',
        'custom':'Custom',
        'ANY_CUSTOM':'Any Size',
        'na_executive_7.25x10.5in':'Executive (7.25x10.5 in.)',
        'na_foolscap_8.5x13in':'Oficio (8.5x13 in.)',
        'na_index-4x6_4x6in':'4x6 in.',
        'na_5x7_5x7in':'5x7 in.',
        'na_index-5x8_5x8in':'5x8 in.',
        'jis_b5_182x257mm':'B5 (JIS) (182x257 mm)',
        'jis_b6_128x182mm':'B6 (JIS) (128x182 mm)',
        'na_oficio_8.5x13.4in':'Oficio (216x340 mm)',
        'om_16k_195x270mm':'16K (195x270 mm)',
        'om_16k_184x260mm':'16K (184x260 mm)',
        'roc_16k_7.75x10.75in':'16K (197x273 mm)',
        'jpn_hagaki_100x148mm':'Postcard (JIS) (100x148 mm)',
        'jpn_oufuku_148x200mm':'Double Postcard (JIS) (148x200 mm)',
        'na_personal_3.625x6.5in':'Personal (3.625inx6.5in)',
        'na_number-10_4.125x9.5in':'Envelope #10 (4.1x9.5 in.)',
        'na_monarch_3.875x7.5in':'Envelope Monarch (3.9x7.5 in.)',
        'iso_c5_162x229mm':'Envelope C5 (162x229 mm)',
        'iso_dl_110x220mm':'Envelope DL (110x220 mm)',
        'iso_b5_176x250mm':'Envelope B5 (176x250 mm)',
        'na_a2_4.375x5.75in':'Envelope A2',
        'om_small-photo_100x150mm':'10x15cm',
        'photo4x11':'Photo (4inx11in)',
        'photo5x5':'Photo (5inx5in)',
        'photo5x11':'Photo (5inx11in)',
        'photo8x8':'Photo (8inx8in)',
        'jpn_chou3_120x235mm':'Chou 3 Envelope',
        'oe_photo-l_3.5x5in':'Oe Photo (3.5inx5in)',
        'na_invoice_5.5x8.5in':'Statement (8.5x5.5 in.)',
        'na_index-3x5_3x5in':'3x5 in.',
        'iso_b1_707x1000mm':'iso_b1_707x1000mm',
        'iso_c0_917x1297mm':'iso_c0_917x1297mm',
        'iso_c1_648x917mm':'iso_c1_648x917mm',
        'iso_c2_458x648mm':'iso_c2_458x648mm',
        'iso_c3_324x458mm':'iso_c3_324x458mm',
        'iso_c4_229x324mm':'iso_c4_229x324mm',
        'jis_b1_728x1030mm':'jis_b1_728x1030mm',
        'jis_b2_515x728mm':'jis_b2_515x728mm',
        'jis_b3_364x515mm':'jis_b3_364x515mm',
        'jis_b4_257x364mm':'jis_b4_257x364mm',
        'na_arch-a_9x12in':'na_arch-a_9x12in',
        'na_arch-b_12x18in':'na_arch-b_12x18in',
        'na_arch-c_18x24in':'na_arch-c_18x24in',
        'na_arch-d_24x36in':'na_arch-d_24x36in',
        'na_arch-e_36x48in':'na_arch-e_36x48in',
        'na_c_17x22in':'na_c_17x22in',
        'na_d_22x34in':'na_d_22x34in',
        'na_e_34x44in':'na_e_34x44in',
        'na_edp_11x14in':'na_edp_11x14in',
        'na_super-b_13x19in':'na_super-b_13x19in',
        'na_wide-format_30x42in':'na_wide-format_30x42in',
        'na_arch-e2_26x38in':'na_arch-e2_26x38in',
        'na_arch-e3_27x39in':'na_arch-e3_27x39in',
        'com.hp.ext.mediaSize.iso_a4_210x297mm.rotated':'A4 ▭ (210x297 mm)',
        'com.hp.ext.mediaSize.na_letter_8.5x11in.rotated':'Letter ▭ (8.5x11 in.)',
        'com.hp.ext.mediaSize.iso_a5_148x210mm.rotated':'A5 ▭ (148x210 mm)',
        'com.hp.ext.mediaSize.jis_b5_182x257mm.rotated':'B5 (JIS) ▭ (182x257 mm)'
    }
    original_sides_dict = {
        'simplex':'1',
        'duplex':'2'
    }
    resolution_dict = {
        'e75Dpi':'75 dpi',
        'e100Dpi':'100 dpi',
        'e150Dpi':'150 dpi',
        'e200Dpi':'200 dpi',
        'e240Dpi':'240 dpi',
        'e300Dpi':'300 dpi',
        'e400Dpi':'400 dpi',
        'e500Dpi':'500 dpi',
        'e600Dpi':'600 dpi',
        'e1200Dpi':'1200 dpi'
    }
    content_type_dict = {
        'mixed':'Mixed',
        'image':'Image',
        'photograph':'Photograph',
        'text':'Text' 
    }
    
    color_dict = {
        'color':'Color',
        'monochrome':'Black Only',
        'grayscale':'Grayscale',
        'autoDetect':'Automatic'
    }
    lighter_darker_dict = {
        1:'1- (Lighter)',
        2:'2',
        3:'3',
        4:'4',
        5:'5',
        6:'6',
        7:'7',
        8:'8',
        9:'9 - (Darker)'
    }

    bool_conv_dict = {
        'true':'on',
        'false':'off'
    }

    file_size_dict = {
        'low':'Small',
        'medium': 'Medium',
        'high': 'Large',
    }

    orientation_dict = {
        'landscape':'Landscape',
        'portrait':'Portrait'
    }

    tray_dic = {
        'auto' : 'Automatic',
        'tray-1':'Tray 1',
        'tray-2':'Tray 2',
        'tray-3':'Tray 3'
    }
    
    exposure_dict = {
        1: 'cNumeral1',
        2: 'cNumeral2',
        3: 'cNumeral3',
        4: 'cNumeral4',
        5: 'cOption5Normal',
        6: 'cNumeral6',
        7: 'cNumeral7',
        8: 'cNumeral8',
        9: 'cNumeral9'
    }

    def_job_options_select_ids_list = ['mediaSize', 'colorMode', 'exposure']

    @staticmethod
    def get_default_job_options_job_ticket_url(cdm, defjobtype):
        """
        Method to get default job options from CDM

        Args:
            defjobtype: Default Job Type
        Returns:
            def_job_options dictionalry
        """
        return cdm.JOB_TICKET_CONFIGURATION_DEFAULTS + '/' + defjobtype.value

    @staticmethod
    def get_def_job_options_strval_by_key(web_element_id, key):
        """
        Method to get string value of SELECT or dropdown job options

        Args:
            web_element_id : id
            key : cdm value
        Returns:
            string value of job options
        """
        if(web_element_id == 'mediaSize'):
            return DefaultJobOptionsUtils.media_size_dict[key]
        elif(web_element_id == 'plexMode'):
            return DefaultJobOptionsUtils.original_sides_dict[key]
        elif(web_element_id == 'resolution'):
            return DefaultJobOptionsUtils.resolution_dict[key]
        elif(web_element_id == 'colorMode'):
            return DefaultJobOptionsUtils.color_dict[key]
        elif(web_element_id == 'exposure'):
            return DefaultJobOptionsUtils.lighter_darker_dict[key]
        elif(web_element_id == 'fileType'):
            return DefaultJobOptionsUtils.file_type_dict[key]
        elif(web_element_id == 'qualityAndFileSize'):
            return DefaultJobOptionsUtils.file_size_dict[key]
        elif(web_element_id == 'contentOrientation'):
            return DefaultJobOptionsUtils.orientation_dict[key]
        elif(web_element_id == 'colorGrayScaleTiffCompression'):
            return DefaultJobOptionsUtils.color_gray_scale_tiff_compression_dict[key]
        elif(web_element_id == 'mediaSourcePrompt'):
            return DefaultJobOptionsUtils.tray_dic[key]
        else:
            logging.error('Invalid web_element_id', web_element_id)
            return ''

    @staticmethod
    def get_default_job_options(cdm, defjobtype):
        """
        Method to get default job options from CDM

        Args:
            defjobtype: Default Job Type
        Returns:
            def_job_options dictionalry
        """
        # Get the def job options from response
        def_job_options = {}

        def_job_ticket = cdm.get(DefaultJobOptionsUtils.get_default_job_options_job_ticket_url(cdm, defjobtype))

        def_job_src = def_job_ticket["src"]
        def_job_scan = def_job_src["scan"]
        def_job_pipelineOptions = def_job_ticket["pipelineOptions"]
        def_job_imagemodifications = def_job_pipelineOptions["imageModifications"]
        if cdm.device_feature_cdm.is_color_supported():
            def_job_options.update({"colorMode": def_job_scan["colorMode"]})
        else:
            def_job_options.update({"contentType": def_job_scan["contentType"]})

        return def_job_options

    @staticmethod
    def get_default_job_options_strvalue_by_id(djo_data, def_job_options_payload):
        """
        Method to prepare payload job options string values, cdm values

        Args:
            djo_data : def job options from cdm
            def_job_options_payload: job options payload to apply
        Returns:
            def_job_options_cdm_strvalue : cdm values of payload
            def_job_options_id_strvalue : string values of payload
        """
        def_job_options_cdm_strvalue = {}
        def_job_options_id_strvalue = {}
        for id, strval in def_job_options_payload.items():
            if id in DefaultJobOptionsUtils.def_job_options_select_ids_list:
                def_job_options_cdm_strvalue.update({id: DefaultJobOptionsUtils.get_def_job_options_strval_by_key(id, djo_data[id])})
                def_job_options_id_strvalue.update({id: DefaultJobOptionsUtils.get_def_job_options_strval_by_key(id, strval)})

        return def_job_options_cdm_strvalue, def_job_options_id_strvalue

    @staticmethod
    def select_default_job_options_strvalue(ews, helper, def_job_options_payload, def_job_options_cdm_strvalue, def_job_options_id_strvalue):
        """
        Method to select payload job options

        Args:
            ews: ews driver
            helper : helper for util functions
            def_job_options_payload: job options payload to apply
            def_job_options_cdm_strvalue : cdm values of payload
            def_job_options_id_strvalue : string values of payload
        Returns:
            None
        """
        for id in def_job_options_payload.keys():
 #           print(id)
            if(id in DefaultJobOptionsUtils.def_job_options_select_ids_list):
                time.sleep(3)
                helper.assert_field_text(id, def_job_options_cdm_strvalue[id])
                helper.select_from_dropdown(id, def_job_options_id_strvalue[id])
#                print('setting ' + str(id) +  ' to ' + str(def_job_options_id_strvalue[id]) )
                time.sleep(1)

    @staticmethod
    def verify_default_job_options_strvalue_by_id(ews, helper, def_job_options_payload, def_job_options_id_strvalue):
        """
        Method to verify payload job options values are applied or not

        Args:
            ews : ews
            def_job_options_payload: job options payload to apply
            def_job_options_id_strvalue : string values of payload
        Returns:
            None
        """
        for id in def_job_options_payload.items():
            if id in DefaultJobOptionsUtils.def_job_options_select_ids_list:
                helper.assert_field_text(id, DefaultJobOptionsUtils.get_def_job_options_strval_by_key(id, def_job_options_id_strvalue[id]))
