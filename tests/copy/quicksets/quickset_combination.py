
quickset_common_combi1 = lambda: {
    "color_mode": "black_only", # value from key of scan_color_mode_option_dict
    "original_size": "a4_210x297_mm", # value from key of scan_original_size_option_dict
    "resolution": "75_dpi", # value from key of scan_resolution_option_dict
    "lighter&darker": 1, # int [1-9]
    "file_type": "pdf_a", # value from key of scan_file_type_option_dict
    "file_type_user_editable": True, # True/False
    "file_size": "small", # value from key of scan_file_size_option_dict
    "orientation": "portrait", # value from key of scan_orientation_option_dict
}

quickset_common_combi2 = lambda: {
    "color_mode": "color", # value from key of scan_color_mode_option_dict
    "original_size": "letter_8.5x11in", # value from key of scan_original_size_option_dict
    "resolution": "150_dpi", # value from key of scan_resolution_option_dict
    "lighter&darker": 5, # int [1-9]
    "file_type_user_editable": False, # True/False
    "file_size": "medium", # value from key of scan_file_size_option_dict
    "orientation": "landscape", # value from key of scan_orientation_option_dict
}

quickset_common_combi2_enterprise = lambda: {
    "color_mode": "color", # value from key of scan_color_mode_option_dict
    "original_size": "letter_8.5x11in", # value from key of scan_original_size_option_dict
    "resolution": "150_dpi", # value from key of scan_resolution_option_dict
    "lighter&darker": 5, # int [1-9]
    "file_type": "pdf", # value from key of scan_file_type_option_dict
    "file_type_user_editable": False, # True/False
    "file_size": "medium", # value from key of scan_file_size_option_dict
    "orientation": "landscape", # value from key of scan_orientation_option_dict
    "split_job_into_multi_page_files": True,  #True/False
    "max_images_per_attachment": 5,  # int [1 - 9999]
    "file_name_prefix": "date_device_date_ddmmyyyy", # value from key of scan_file_name_prefix_option_dict
    "file_name_suffix": "date_device_date_yyyymmdd", # value from key of scan_file_name_suffix_option_dict
    "file_numbering_format": "xy", # value from key of scan_file_numbering_format_option_dict
    "add_numbering_job_has_just_one_file": False # True/False
}

quickset_common_combi2_book_mode_enterprise = lambda: {
    "scan_capture_mode": "bookMode"
}

quickset_common_combi3 = lambda: {
    "color_mode": "grayscale", # value from key of scan_color_mode_option_dict
    "original_size": "legal_8.5x14in", # value from key of scan_original_size_option_dict
    "resolution": "200_dpi", # value from key of scan_resolution_option_dict
    "lighter&darker": 9, # int [1-9]
    "file_type": "jpeg", # value from key of scan_file_type_option_dict
    "file_size": "large", # value from key of scan_file_size_option_dict
}


quickset_common_combi4 = lambda: {
    "original_size": "a5_148x210_mm", # value from key of scan_original_size_option_dict
    "resolution": "200_dpi", # value from key of scan_resolution_option_dict
    "lighter&darker": 8, # int [1-9]
    "file_type": "pdf", # value from key of scan_file_type_option_dict
}

quickset_common_combi5 = lambda: {
    "original_size": "executive_7_25x10_5in", # value from key of scan_original_size_option_dict
    "resolution": "300_dpi", # value from key of scan_resolution_option_dict
    "lighter&darker": 6, # int [1-9]
    "file_type": "pdf", # value from key of scan_file_type_option_dict
    "pdf_encryption": True, # True/False
}

quickset_common_combi6 = lambda: {
    "original_size": "5x8in", # value from key of scan_original_size_option_dict
    "content_type": "photograph", # value from key of scan_content_type_option_dict
    "resolution": "400_dpi", # value from key of scan_resolution_option_dict
    "file_type": "tiff", # value from key of scan_file_type_option_dict
    "tiff_compression": "tiff_6_0", # value from key of scan_tiff_compression_option_dict
}

quickset_common_combi7 =lambda:  {
    "original_size": "oficio_8_5x13in", # value from key of scan_original_size_option_dict
    "content_type": "mixed", # value from key of scan_content_type_option_dict
    "resolution": "600_dpi", # value from key of scan_resolution_option_dict
    "file_type": "tiff", # value from key of scan_file_type_option_dict
    "tiff_compression": "tiff_post_6_0", # value from key of scan_tiff_compression_option_dict
}

quickset_common_combi8 = lambda: {
    "original_sides": "1-sided", # value from key of scan_sides_option_dict
    "original_size": "statement_8.5x5.5in", # value from key of scan_original_size_option_dict
    "content_type": "text", # value from key of scan_content_type_option_dict
}

quickset_common_combi9 = lambda: {
    "original_size": "b5_jis", # value from key of scan_original_size_option_dict
    "resolution": "1200_dpi", # value from key of scan_resolution_option_dict
}

quickset_common_combi10 = lambda: {
    "original_sides": "2-sided", # value from key of scan_sides_option_dict
    "original_size": "5x7in", # value from key of scan_original_size_option_dict
}

quickset_common_combi11 = lambda: {
    "original_size": "16k_184x260_mm", # value from key of scan_original_size_option_dict
}

quickset_common_combi12 = lambda: {
    "original_size": "oficio_216x340_mm", # value from key of scan_original_size_option_dict
}

quickset_common_combi13 = lambda: {
    "original_size": "envelop_monarch", # value from key of scan_original_size_option_dict
}

quickset_common_combi14 = lambda: {
    "original_size": "b6_jis_128x182_mm", # value from key of scan_original_size_option_dict
}

quickset_common_combi15 = lambda: {
    "original_size": "b5_176x250_mm", # value from key of scan_original_size_option_dict
}

quickset_common_combi16 = lambda: {
    "original_size": "16k_195x270_mm", # value from key of scan_original_size_option_dict
}

quickset_common_combi17 = lambda: {
    "original_size": "envelope_10_4.1x9.5in", # value from key of scan_original_size_option_dict
}

quickset_common_combi18 = lambda: {
    "original_size": "5x8in", # value from key of scan_original_size_option_dict
}

quickset_common_combi19 = lambda: {
    "original_size": "8x10in", # value from key of scan_original_size_option_dict
}

quickset_common_combi20 = lambda: {
    "original_size": "5x5in", # value from key of scan_original_size_option_dict
}

quickset_common_combi21 = lambda: {
    "original_size": "16k_197x273_mm", # value from key of scan_original_size_option_dict
}

quickset_common_combi22 = lambda: {
    "original_size": "statement_8.5x5.5in", # value from key of scan_original_size_option_dict
}

quickset_common_combi23 = lambda: {
    "original_size": "envelope_b5_176x250_mm", # value from key of scan_original_size_option_dict
}

quickset_common_combi24 = lambda: {
    "original_size": "envelope_c5_162x229_mm", # value from key of scan_original_size_option_dict
}

quickset_common_combi25 = lambda: {
    "original_size": "5x8in", # value from key of scan_original_size_option_dict
}

quickset_common_combi26 = lambda: {
    "original_size": "double_postcard_jis", # value from key of scan_original_size_option_dict
}

quickset_common_combi27 = lambda: {
    "original_size": "postcard_jis", # value from key of scan_original_size_option_dict
}

quickset_common_combi28 = lambda: {
    "original_size": "hagaki_ofuku", # value from key of scan_original_size_option_dict
}

quickset_common_combi29 = lambda: {
    "original_size": "100x150mm", # value from key of scan_original_size_option_dict
}

quickset_common_combi30 = lambda: {
    "original_size": "2l_127x178_mm", # value from key of scan_original_size_option_dict
}

quickset_common_combi1_manual_feeder = lambda: {
    "background_noise_removal": False, #True/False
    "original_paper_type" : "white", # value from key of scan_original_paper_type_option_dict
    "color_mode": "color", # value from key of scan_color_mode_option_dict
    "long_original": False, #True/False
}

quickset_common_combi2_manual_feeder = lambda: {
    "edge_to_edge_output": True, #True/False
    "color_mode": "black_only", # value from key of scan_color_mode_option_dict
    "file_type": "tiff", # value from key of scan_file_type_option_dict
    "resolution": "200_dpi", # value from key of scan_resolution_option_dict
}

quickset_common_combi3_manual_feeder = lambda: {
    "edge_to_edge_output": False, #True/False
    "original_paper_type" : "blueprint", # value from key of scan_original_paper_type_option_dict
    "background_color_removal": False, #True/False
    "file_size": "small", # value from key of scan_file_size_option_dict
}

quickset_common_combi4_manual_feeder = lambda: {
    "background_noise_removal": True, #True/False
    "long_original": True, #True/False
    "file_type": "pdf", # value from key of scan_file_type_option_dict
    "file_size": "medium", # value from key of scan_file_size_option_dict
}

# need to update output size function when DUNE-141523 fixed.
quickset_common_combi5_manual_feeder = lambda: {
    "original_paper_type": "translucent", # value from key of scan_original_paper_type_option_dict
    "reduce_scan_speed_to_enhance_quality": True, #True/False
    "background_color_removal": True, #True/False
    "file_size": "large", # value from key of scan_file_size_option_dict
    "output_size": "automatic", # value from key of scan_output_size_option_dict
}

quickset_common_combi6_manual_feeder = lambda: {
    "content_type": "image", # value from key of scan_content_type_option_dict
    "original_paper_type": "photo", # value from key of scan_original_paper_type_option_dict
    "resolution": "300_dpi", # value from key of scan_resolution_option_dict
    "output_size": "a0", # value from key of scan_output_size_option_dict
}

quickset_common_combi7_manual_feeder = lambda: {
    "content_type": "mixed", # value from key of scan_content_type_option_dict
    "auto_release_original": True, #True/False
    "resolution": "600_dpi", # value from key of scan_resolution_option_dict
    "file_type": "jpeg", # value from key of scan_file_type_option_dict
    "output_size": "a1", # value from key of scan_output_size_option_dict
}

quickset_common_combi8_manual_feeder = lambda: {
    "content_type": "lines", # value from key of scan_content_type_option_dict
    "auto_release_original": False, #True/False
    "color_mode": "grayscale", # value from key of scan_color_mode_option_dict
    "file_size": "largest", # value from key of scan_file_size_option_dict
    "output_size": "a2", # value from key of scan_output_size_option_dict
}

quickset_common_combi9_manual_feeder = lambda: {
    "original_paper_type": "blueprint", # value from key of scan_original_paper_type_option_dict
    "invert_blueprint": True, #True/False
    "detailed_background_removal": 6, # int [-6 - 6]
    "file_size": "smallest", # value from key of scan_file_size_option_dict
    "output_size": "a3", # value from key of scan_output_size_option_dict
}

quickset_common_combi10_manual_feeder = lambda: {
    "original_paper_type": "ammonia_blueprint", # value from key of scan_original_paper_type_option_dict
    "invert_blueprint": False, #True/False
    "detailed_background_removal": -6, # int [-6 - 6]
    "file_type": "pdf_a", # value from key of scan_file_type_option_dict
    "output_size": "a4", # value from key of scan_output_size_option_dict
}

quickset_common_combi11_manual_feeder = lambda: {
    "original_paper_type": "old", # value from key of scan_original_paper_type_option_dict
    "black_enhancement": 0, # int [0-255]
    "output_size": "b0_iso", # value from key of scan_output_size_option_dict
}

quickset_common_combi13_manual_feeder = lambda: {
    "output_size": "b2_iso", # value from key of scan_output_size_option_dict
    "black_enhancement": 100, # int [0-255]
    "position": "top_left", # value from key of scan_positioning_option_dict    
}

quickset_common_combi14_manual_feeder = lambda: {
    "output_size": "b3_iso", # value from key of scan_output_size_option_dict
    "black_enhancement": 255, # int [0-255]
    "position": "top_center", # value from key of scan_positioning_option_dict    
}

quickset_common_combi15_manual_feeder = lambda: {
    "output_size": "b4_iso", # value from key of scan_output_size_option_dict
    "position": "top_right", # value from key of scan_positioning_option_dict    
}

quickset_common_combi16_manual_feeder = lambda: {
    "output_size": "ansi_a", # value from key of scan_output_size_option_dict
    "position": "middle_left", # value from key of scan_positioning_option_dict    
}

quickset_common_combi17_manual_feeder = lambda: {
    "output_size": "ansi_b", # value from key of scan_output_size_option_dict
    "position": "middle_center", # value from key of scan_positioning_option_dict    
}

quickset_common_combi18_manual_feeder = lambda: {
    "output_size": "ansi_c", # value from key of scan_output_size_option_dict
    "position": "middle_right", # value from key of scan_positioning_option_dict
    "output_canvas_orientation": "portrait", # value from key of scan_output_canvas_orientation_option_dict
}

quickset_common_combi19_manual_feeder = lambda: {
    "output_size": "ansi_d", # value from key of scan_output_size_option_dict
    "position": "bottom_left", # value from key of scan_positioning_option_dict
    "output_canvas_orientation": "landscape", # value from key of scan_output_canvas_orientation_option_dict    
}

quickset_common_combi20_manual_feeder = lambda: {
    "output_size": "ansi_e", # value from key of scan_output_size_option_dict
    "position": "bottom_center", # value from key of scan_positioning_option_dict    
}

quickset_common_combi21_manual_feeder = lambda: {
    "output_size": "arch_a", # value from key of scan_output_size_option_dict
    "position": "bottom_right", # value from key of scan_positioning_option_dict    
}

quickset_common_combi22_manual_feeder = lambda: {
    "output_size": "arch_b", # value from key of scan_output_size_option_dict 
}

quickset_common_combi23_manual_feeder = lambda: {
    "output_size": "arch_c", # value from key of scan_output_size_option_dict   
}

quickset_common_combi24_manual_feeder = lambda: {
    "output_size": "arch_d", # value from key of scan_output_size_option_dict
}

quickset_common_combi25_manual_feeder = lambda: {
    "output_size": "arch_e", # value from key of scan_output_size_option_dict
}

quickset_common_combi26_manual_feeder = lambda: {
    "output_size": "roll_1", # value from key of scan_output_size_option_dict
}

quickset_common_combi27_manual_feeder = lambda: {
    "output_size": "roll_2", # value from key of scan_output_size_option_dict
}

quickset_common_combi28_manual_feeder = lambda: {
    "output_size": "custom", # value from key of scan_output_size_option_dict
    "custom_output_size_width": 840, #int
}

quickset_common_combi29_manual_feeder = lambda: {
    "output_size": "custom", # value from key of scan_output_size_option_dict
    "custom_output_size_length": 1350, #int
}

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

quickset_copy_common_combi3 = lambda: {
    "content_type": "mixed", # value from key of copy_content_type_option_dict
    "number_of_copies" : 99, # int [1-999]
    "paper_size" : "a4_210x297_mm", # value from key of copy_paper_size_option_dict
    "quality" : "draft", # value from key of copy_file_quality_option_dict
    "sides" : "2_to_2_sided", # value from key of copy_sides_option_dict
    "two_sided_pages_flip_up" : True, # True/False
    "collate" : False # True/False
}

quickset_copy_common_combi4 = lambda: {
    "content_type": "text", # value from key of copy_content_type_option_dict
    "number_of_copies" : 10, # int [1-999]
    "paper_size" : "a4_210x297_mm", # value from key of copy_paper_size_option_dict
    "quality" : "draft", # value from key of copy_file_quality_option_dict
}

quickset_copy_common_combi5 = lambda: {
    "content_type": "image", # value from key of copy_content_type_option_dict
    "paper_size" : "a4_210x297_mm", # value from key of copy_paper_size_option_dict
    "quality" : "standard", # value from key of copy_file_quality_option_dict
}

quickset_copy_common_combi6 = lambda: {
    "content_type": "photograph", # value from key of copy_content_type_option_dict
    "paper_size" : "a4_210x297_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "hp_ecofficient", # value from key of copy_paper_type_option_dict
    #DUNE-226761 We don't have any quality option curerently implemented for copy.
    #Enable back once the quality option is implemented
    #"quality" : "best", # value from key of copy_file_quality_option_dict
}

quickset_copy_common_combi7 = lambda: {
    "color_mode": "color", # value from key of copy_color_mode_option_dict
    "paper_size" : "a4_210x297_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "hp_matte_90g", # value from key of copy_paper_type_option_dict
    "paper_tray" : "tray2", # value from key of copy_paper_tray_option_dict
}

quickset_copy_common_combi8 = lambda: {
    "color_mode": "grayscale", # value from key of copy_color_mode_option_dict
    "paper_size" : "a4_210x297_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "hp_matte_105g", # value from key of copy_paper_type_option_dict
    "paper_tray" : "tray1", # value from key of copy_paper_tray_option_dict
}

quickset_copy_common_combi9 = lambda: {
    #DUNE-DUNE-226761 Changing color_mode to grayscale as we don't have color mode option for black_only
    "color_mode": "grayscale", # value from key of copy_color_mode_option_dict
    "paper_size" : "a4_210x297_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "hp_matte_120g", # value from key of copy_paper_type_option_dict
    "paper_tray" : "tray3", # value from key of copy_paper_tray_option_dict
}

quickset_copy_common_combi10 = lambda: {
    "original_size": "legal_8.5x14in", # value from key of copy_original_size_option_dict
    "lighter_darker": 1, # int [1-9]
    "paper_size" : "a4_210x297_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "hp_matte_150g", # value from key of copy_paper_type_option_dict
    "paper_tray" : "tray1", # value from key of copy_paper_tray_option_dict
}

quickset_copy_common_combi11 = lambda: {
    "original_size": "executive_7_25x10_5in",  # value from key of copy_original_size_option_dict
    "lighter_darker": 9, # int [1-9]
    "paper_size" : "a4_210x297_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "hp_matte_200g", # value from key of copy_paper_type_option_dict
    "pages_per_sheet" : "two", # value from key of copy_pagesper_sheet_option_dict
}

quickset_copy_common_combi12 = lambda: {
    "original_size": "oficio_8_5x13in", # value from key of copy_original_size_option_dict
    "lighter_darker": 6, # int [1-9]
    "paper_size" : "a4_210x297_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "hp_glossy_120g", # value from key of copy_paper_type_option_dict
    "output_scale" : "custom", # value from key of copy_output_scale_option_dict
}

quickset_copy_common_combi13 = lambda: {
    "original_size": "5x8in", # value from key of copy_original_size_option_dict
    "paper_size" : "a4_210x297_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "hp_glossy_150g", # value from key of copy_paper_type_option_dict
    "output_scale" : "custom", # value from key of copy_output_scale_option_dict
    "precise_scaling_amount": "25" # value for custom output_scale, string[25% - 400%]
}

quickset_copy_common_combi14 = lambda: {
    "original_size": "a4_210x297_mm", # value from key of copy_original_size_option_dict
    "paper_size" : "a4_210x297_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "hp_glossy_200g", # value from key of copy_paper_type_option_dict
    "output_scale" : "custom", # value from key of copy_output_scale_option_dict
    "precise_scaling_amount": "400" # value for custom output_scale, string[25% - 400%]
}

quickset_copy_common_combi15 = lambda: {
    "original_size": "a5_148x210_mm", # value from key of copy_original_size_option_dict
    "paper_size" : "a4_210x297_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "hp_trifold_glossy", # value from key of copy_paper_type_option_dict
    "output_scale" : "custom", # value from key of copy_output_scale_option_dict
}

quickset_copy_common_combi16 = lambda: {
    "original_size": "b5_jis", # value from key of copy_original_size_option_dict
    "paper_size" : "a4_210x297_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "light", # value from key of copy_paper_type_option_dict
    "output_scale" : "custom", # value from key of copy_output_scale_option_dict
}

quickset_copy_common_combi17 = lambda: {
    "original_size": "b6_jis_128x182_mm", # value from key of copy_original_size_option_dict
    "paper_size" : "a4_210x297_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "intermediate", # value from key of copy_paper_type_option_dict
    "output_scale" : "custom", # value from key of copy_output_scale_option_dict
}

quickset_copy_common_combi18 = lambda: {
    "original_size": "oficio_216x340_mm", # value from key of copy_original_size_option_dict
    "paper_size" : "a4_210x297_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "midweight", # value from key of copy_paper_type_option_dict
    "output_scale" : "custom", # value from key of copy_output_scale_option_dict
}

quickset_copy_common_combi19 = lambda: {
    "original_size": "16k_195x270_mm", # value from key of copy_original_size_option_dict
    "paper_size" : "a4_210x297_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "heavy", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi20 = lambda: {
    "original_size": "16k_184x260_mm", # value from key of copy_original_size_option_dict
    "paper_size" : "a4_210x297_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "extra_heavy", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi21 = lambda: {
    "original_size": "16k_197x273_mm", # value from key of copy_original_size_option_dict
    "paper_size" : "letter_8.5x11in", # value from key of copy_paper_size_option_dict
    "paper_type" : "heavy_glossy", # value from key of copy_paper_type_option_dict
}


quickset_copy_common_combi22 = lambda: {
    "original_size": "double_postcard_jis", # value from key of copy_original_size_option_dict
    "paper_size" : "legal_8.5x14in", # value from key of copy_paper_size_option_dict
    "paper_type" : "extra_heavy_glossy", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi23 = lambda: {
    "original_size": "statement_8.5x5.5in", # value from key of copy_original_size_option_dict
    "paper_size" : "executive_7_25x10_5in", # value from key of copy_paper_size_option_dict
    "paper_type" : "cardstock_glossy", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi24 = lambda: {
    "paper_size" : "oficio_8_5x13in", # value from key of copy_paper_size_option_dict
    "paper_type" : "letterhead", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi25 = lambda: {
    "paper_size" : "b5_jis", # value from key of copy_paper_size_option_dict
    "paper_type" : "preprinted", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi26 = lambda: {
    "paper_size" : "oficio_216x340_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "prepunched", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi27 = lambda: {
    "paper_size" : "16k_195x270_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "colored", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi28 = lambda: {
    "paper_size" : "16k_184x260_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "bond", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi29 = lambda: {
    "paper_size" : "16k_197x273_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "light", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi30 = lambda: {
    "paper_size" : "custom", # value from key of copy_paper_size_option_dict
    "paper_type" : "rough", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi31 = lambda: {
    "paper_size" : "16k_184x260_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "heavy_rough", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi32 = lambda: {
    "paper_size" : "a0_841x1189_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "plain", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi33 = lambda: {
    "paper_size" : "a1_594x841_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "hp_ecofficient", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi34 = lambda: {
    "paper_size" : "a2_420x594_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "hp_matte_90g", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi35 = lambda: {
    "paper_size" : "a3_297x420_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "hp_matte_105g", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi36 = lambda: {
    "paper_size" : "a4_210x297_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "hp_matte_120g", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi37 = lambda: {
    "paper_size" : "a5_148x210_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "hp_prem_matte", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi38 = lambda: {
    "paper_size" : "a6_105x148_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "hp_matte_150g", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi39 = lambda: {
    "paper_size" : "b0_1000x1414mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "comhpbrochurematter", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi40 = lambda: {
    "paper_size" : "b1_707x1000mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "hp_trifold_glossy", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi41 = lambda: {
    "paper_size" : "b2_500x707mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "hp_glossy_150g", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi42 = lambda: {
    "paper_size" : "b3_353x500mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "brochure_glossy", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi43 = lambda: {
    "paper_size" : "b4_250x353mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "hp_premium_plus_photo", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi44 = lambda: {
    "paper_size" : "envelope_b5_176x250_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "hp_advanced_photo", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi45 = lambda: {
    "paper_size" : "c0_917x1297mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "hp_everyday_photo", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi46 = lambda: {
    "paper_size" : "c1_648x917mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "hp_matte_200g", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi47 = lambda: {
    "paper_size" : "c2_458x648mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "hp_soft_gloss_120g", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi48 = lambda: {
    "paper_size" : "c3_324x458mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "hp_glossy_120g", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi49 = lambda: {
    "paper_size" : "c4_229x324mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "hp_glossy_200g", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi50 = lambda: {
    "paper_size" : "envelope_c5_162x229_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "light", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi51 = lambda: {
    "paper_size" : "envelope_c6_114x162_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "intermediate", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi52 = lambda: {
    "paper_size" : "envelope_dl_110x220_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "midweight", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi53 = lambda: {
    "paper_size" : "ra3_305x430mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "heavy", # value from key of copy_paper_type_option_dict
}
	
quickset_copy_common_combi54 = lambda: {
    "paper_size" : "ra4_215x305mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "extra_heavy", # value from key of copy_paper_type_option_dict
}	

quickset_copy_common_combi55 = lambda: {
    "paper_size" : "sra3_320x450mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "cardstock", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi56 = lambda: {
    "paper_size" : "sra4_225x320mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "hp_midweight_glossy", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi57 = lambda: {
    "paper_size" : "b0_jis_1030x1456mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "heavy_glossy", # value from key of copy_paper_type_option_dict
}
	
quickset_copy_common_combi58 = lambda: {
    "paper_size" : "b1_jis_728x1030mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "extra_heavy_glossy", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi59 = lambda: {
    "paper_size" : "b2_jis_515x728mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "cardstock_glossy", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi60 = lambda: {
    "paper_size" : "b3_jis_364x515mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "transparency", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi61 = lambda: {
    "paper_size" : "b4_jis_257x364mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "labels", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi62 = lambda: {
    "paper_size" : "b5_jis", # value from key of copy_paper_size_option_dict
    "paper_type" : "envelope", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi63 = lambda: {
    "paper_size" : "b6_jis_128x182_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "heavy_envelope", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi64 = lambda: {
    "paper_size" : "japanese_envelope_chou_3_120x235_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "letterhead", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi65 = lambda: {
    "paper_size" : "japanese_envelope_chou_4_90x205_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "preprinted", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi66 = lambda: {
    "paper_size" : "postcard_jis", # value from key of copy_paper_size_option_dict
    "paper_type" : "prepunched", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi67 = lambda: {
    "paper_size" : "double_postcard_jis", # value from key of copy_paper_size_option_dict
    "paper_type" : "colored", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi68 = lambda: {
    "paper_size" : "2l_127x178_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "lightbond", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi69 = lambda: {
    "paper_size" : "10x15in", # value from key of copy_paper_size_option_dict
    "paper_type" : "bond", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi70 = lambda: {
    "paper_size" : "5x7in", # value from key of copy_paper_size_option_dict
    "paper_type" : "recycled", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi71 = lambda: {
    "paper_size" : "a2_420x594_mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "paperboard", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi72 = lambda: {
    "paper_size" : "arch_a_229x305mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "heavy_paperboard", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi73 = lambda: {
    "paper_size" : "arch_b_305x457mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "light_paperboard", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi74 = lambda: {
    "paper_size" : "arch_c_457x610mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "rough", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi75 = lambda: {
    "paper_size" : "arch_d_610x914mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "light_rough", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi76 = lambda: {
    "paper_size" : "arch_e2_660x965mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "heavy_rough", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi77 = lambda: {
    "paper_size" : "arch_e3_686x991mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "stationery-fine", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi78 = lambda: {
    "paper_size" : "arch_e_914x1919mm", # value from key of copy_paper_size_option_dict
    "paper_type" : "tab_stock", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi79 = lambda: {
    "paper_size" : "ansi_c_17x22in", # value from key of copy_paper_size_option_dict
    "paper_type" : "hp_film_opaque", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi80 = lambda: {
    "paper_size" : "d_22x34in", # value from key of copy_paper_size_option_dict
    "paper_type" : "hp_photographic_glossy", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi81 = lambda: {
    "paper_size" : "e_34x44in", # value from key of copy_paper_size_option_dict
    "paper_type" : "hp_photographic_inkjet", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi82 = lambda: {
    "paper_size" : "11x14in", # value from key of copy_paper_size_option_dict
    "paper_type" : "hp_matte_brochure", # value from key of copy_paper_type_option_dict
}
	
quickset_copy_common_combi83 = lambda: {
    "paper_size" : "executive_7_25x10_5in", # value from key of copy_paper_size_option_dict
    "paper_type" : "hp_matte_presentation", # value from key of copy_paper_type_option_dict
}
	
quickset_copy_common_combi84 = lambda: {
    "paper_size" : "oficio_8_5x13in", # value from key of copy_paper_size_option_dict
    "paper_type" : "hp_matte_inkjet", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi85 = lambda: {
    "paper_size" : "8x10in", # value from key of copy_paper_size_option_dict
    "paper_type" : "hp_specialty_glossy", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi86 = lambda: {
    "paper_size" : "3x5in", # value from key of copy_paper_size_option_dict
    "paper_type" : "hp_specialty_glossy_inkjet", # value from key of copy_paper_type_option_dict
}
	
quickset_copy_common_combi87 = lambda: {
    "paper_size" : "4x6in", # value from key of copy_paper_size_option_dict
    "paper_type" : "hp_specialty_hagaki", # value from key of copy_paper_type_option_dict
}
	
quickset_copy_common_combi88 = lambda: {
    "paper_size" : "5x8in", # value from key of copy_paper_size_option_dict
    "paper_type" : "hp_trifold_brochure_glossy_180gsm", # value from key of copy_paper_type_option_dict
}

quickset_copy_common_combi89 = lambda: {
    "paper_size" : "statement_8.5x5.5in", # value from key of copy_paper_size_option_dict
    "paper_type" : "hp_matte_photo_duplex", # value from key of copy_paper_type_option_dict
}	

quickset_copy_common_combi90 = lambda: {
    "paper_size" : "ledger_11x17in", # value from key of copy_paper_size_option_dict
}

quickset_copy_common_combi91 = lambda: {
    "paper_size" : "legal_8.5x14in", # value from key of copy_paper_size_option_dict
}

quickset_copy_common_combi92 = lambda: {
    "paper_size" : "letter_8.5x11in", # value from key of copy_paper_size_option_dict
}

quickset_copy_common_combi93 = lambda: {
    "paper_size" : "envelop_monarch", # value from key of copy_paper_size_option_dict
}

quickset_copy_common_combi94 = lambda: {
    "paper_size" : "envelope_10_4.1x9.5in", # value from key of copy_paper_size_option_dict
}

quickset_copy_common_combi95 = lambda: {
    "paper_size" : "envelope_9", # value from key of copy_paper_size_option_dict
}

quickset_copy_common_combi96 = lambda: {
    "paper_size" : "oficio_216x340_mm", # value from key of copy_paper_size_option_dict
}

quickset_copy_common_combi97 = lambda: {
    "paper_size" : "envelope_6_three_quarter", # value from key of copy_paper_size_option_dict
}
	
quickset_copy_common_combi98 = lambda: {
    "paper_size" : "super_b_13x19in", # value from key of copy_paper_size_option_dict
}
	
quickset_copy_common_combi99 = lambda: {
    "paper_size" : "wide_format_30x42in", # value from key of copy_paper_size_option_dict
}

quickset_copy_common_combi100 = lambda: {
    "paper_size" : "photo_12x16in", # value from key of copy_paper_size_option_dict
}
	
quickset_copy_common_combi101 = lambda: {
    "paper_size" : "photo_14x17in", # value from key of copy_paper_size_option_dict
}
	
quickset_copy_common_combi102 = lambda: {
    "paper_size" : "photo_18x22in", # value from key of copy_paper_size_option_dict
}
	
quickset_copy_common_combi103 = lambda: {
    "paper_size" : "photo_10x12in", # value from key of copy_paper_size_option_dict
}	

quickset_copy_common_combi104 = lambda: {
    "paper_size" : "photo_14x18in", # value from key of copy_paper_size_option_dict
}
	
quickset_copy_common_combi105 = lambda: {
    "paper_size" : "photo_16x20in", # value from key of copy_paper_size_option_dict
}
	
quickset_copy_common_combi106 = lambda: {
    "paper_size" : "photo_20x24in", # value from key of copy_paper_size_option_dict
}	

quickset_copy_common_combi107 = lambda: {
    "paper_size" : "photo_22x28in", # value from key of copy_paper_size_option_dict
}
	
quickset_copy_common_combi108 = lambda: {
    "paper_size" : "photo_24x30in", # value from key of copy_paper_size_option_dict
}	

quickset_copy_common_combi109 = lambda: {
    "paper_size" : "l_3_5x5in", # value from key of copy_paper_size_option_dict
}	

quickset_copy_common_combi110 = lambda: {
    "paper_size" : "photo_4x12in", # value from key of copy_paper_size_option_dict
}
	
quickset_copy_common_combi111 = lambda: {
    "paper_size" : "photo_4x5in", # value from key of copy_paper_size_option_dict
}
	
quickset_copy_common_combi112 = lambda: {
    "paper_size" : "photo_5x5in", # value from key of copy_paper_size_option_dict
}

quickset_copy_common_combi113 = lambda: {
    "paper_size" : "16k_184x260_mm", # value from key of copy_paper_size_option_dict
}

quickset_copy_common_combi114 = lambda: {
    "paper_size" : "16k_195x270_mm", # value from key of copy_paper_size_option_dict
}

quickset_copy_common_combi115 = lambda: {
    "paper_size" : "8K_260x368mm", # value from key of copy_paper_size_option_dict
}
	
quickset_copy_common_combi116 = lambda: {
    "paper_size" : "8K_270x390mm", # value from key of copy_paper_size_option_dict
}
	
quickset_copy_common_combi117 = lambda: {
    "paper_size" : "photo_30x40cm", # value from key of copy_paper_size_option_dict
}
	
quickset_copy_common_combi118 = lambda: {
    "paper_size" : "photo_30x45cm", # value from key of copy_paper_size_option_dict
}	

quickset_copy_common_combi119 = lambda: {
    "paper_size" : "photo_35x46cm", # value from key of copy_paper_size_option_dict
}
	
quickset_copy_common_combi120 = lambda: {
    "paper_size" : "photo_40x60cm", # value from key of copy_paper_size_option_dict
}	

quickset_copy_common_combi121 = lambda: {
    "paper_size" : "photo_50x76cm", # value from key of copy_paper_size_option_dict
}	

quickset_copy_common_combi122 = lambda: {
    "paper_size" : "photo_60x90cm", # value from key of copy_paper_size_option_dict
}	

quickset_copy_common_combi123 = lambda: {
    "paper_size" : "100x150mm", # value from key of copy_paper_size_option_dict
}

quickset_copy_common_combi124 = lambda: {
    "paper_size" : "16k_197x273_mm", # value from key of copy_paper_size_option_dict
}

quickset_copy_common_combi125 = lambda: {
    "paper_size" : "8K_273x394mm", # value from key of copy_paper_size_option_dict
}	

quickset_copy_common_combi126 = lambda: {
    "paper_size" : "custom", # value from key of copy_paper_size_option_dict
}
