from dunetuf.ews.CopyEws import *

job_copy_settings_default= {}

job_copy_option_default = {
    CopyEwsOptionsKey.number_of_copies: 1,
    CopyEwsOptionsKey.two_sided: TwoSided.one_to_one_sided,
    CopyEwsOptionsKey.color_mode: ColorMode.color,
    CopyEwsOptionsKey.pages_per_sheet: PagesPerSheet.one,
    CopyEwsOptionsKey.two_sided_pages_flip_up: False,
    CopyEwsOptionsKey.original_size: OriginalSize.Letter_8_5x11_in_,
    CopyEwsOptionsKey.output_scale: OutputScale.none,
    CopyEwsOptionsKey.select_tray: PaperTray.auto,
    # CopyEwsOptionsKey.quality: Quality.standard,
    CopyEwsOptionsKey.lighter_darker: LighterDarker.five,
    CopyEwsOptionsKey.content_type: ContentType.mixed,
    CopyEwsOptionsKey.collate: True
}

job_copy_option_combi_random = {
    CopyEwsOptionsKey.number_of_copies: 2,
    CopyEwsOptionsKey.two_sided: TwoSided.one_to_two_sided,
    CopyEwsOptionsKey.pages_per_sheet: PagesPerSheet.two,
    CopyEwsOptionsKey.two_sided_pages_flip_up: True,
    CopyEwsOptionsKey.original_size: OriginalSize.A4_210x297_mm,
    # No output scale when pagesPerSheet is 2
    # CopyEwsOptionsKey.output_scale: OutputScale.none,
    CopyEwsOptionsKey.select_tray: PaperTray.tray1,
    # CopyEwsOptionsKey.quality: Quality.best,
    CopyEwsOptionsKey.lighter_darker: LighterDarker.three,
    CopyEwsOptionsKey.content_type: ContentType.text,
    CopyEwsOptionsKey.collate: False
}

job_copy_option_combi_reboot = {
    CopyEwsOptionsKey.number_of_copies: 17,
    CopyEwsOptionsKey.two_sided: TwoSided.two_to_one_sided,
    CopyEwsOptionsKey.pages_per_sheet: PagesPerSheet.one,
    CopyEwsOptionsKey.two_sided_pages_flip_up: False,
    CopyEwsOptionsKey.original_size: OriginalSize.A4_210x297_mm,
    CopyEwsOptionsKey.output_scale: OutputScale.custom,
    CopyEwsOptionsKey.precise_scaling_amount: 50,
    CopyEwsOptionsKey.select_tray: PaperTray.tray3,
    # CopyEwsOptionsKey.quality: Quality.best,
    CopyEwsOptionsKey.lighter_darker: LighterDarker.six,
    CopyEwsOptionsKey.content_type: ContentType.text,
    CopyEwsOptionsKey.collate: False
}

job_copy_option_combi_outputscale_custom_min = {
    CopyEwsOptionsKey.output_scale: OutputScale.custom,
    CopyEwsOptionsKey.precise_scaling_amount: 20
}

job_copy_option_combi_outputscale_custom_max = {
    CopyEwsOptionsKey.output_scale: OutputScale.custom,
    CopyEwsOptionsKey.precise_scaling_amount: 500
}

job_copy_option_combi_outputscale_custom_min_normal = {
    CopyEwsOptionsKey.output_scale: OutputScale.custom,
    CopyEwsOptionsKey.precise_scaling_amount: 25
}

job_copy_option_combi_outputscale_custom_max_normal = {
    CopyEwsOptionsKey.output_scale: OutputScale.custom,
    CopyEwsOptionsKey.precise_scaling_amount: 400
}

#Original Size
job_copy_option_combi_original_size_A4 = {
CopyEwsOptionsKey.original_size: OriginalSize.A4_210x297_mm
}

job_copy_option_combi_original_size_SEF_A4 = {
CopyEwsOptionsKey.original_size: OriginalSize.SEF_A4_210x297_mm
}

job_copy_option_combi_original_size_A5 = {
CopyEwsOptionsKey.original_size: OriginalSize.A5_148x210_mm
}

job_copy_option_combi_original_size_SEF_A5 = {
CopyEwsOptionsKey.original_size: OriginalSize.SEF_A5_148x210_mm
}

job_copy_option_combi_original_size_A6 = {
CopyEwsOptionsKey.original_size: OriginalSize.A6_105x148_mm
}

job_copy_option_combi_original_size_envelop_b5 = {
CopyEwsOptionsKey.original_size: OriginalSize.Envelope_B5_176x250_mm
}

job_copy_option_combi_original_size_B6_Jis = {
CopyEwsOptionsKey.original_size: OriginalSize.B6_JIS_128x182_mm
}

job_copy_option_combi_original_size_envelop_c5 = {
CopyEwsOptionsKey.original_size: OriginalSize.Envelope_C5_162x229_mm
}

job_copy_option_combi_original_size_double_postcard_jis={
CopyEwsOptionsKey.original_size: OriginalSize.Double_Postcard_JIS
}

job_copy_option_combi_original_size_executive={
CopyEwsOptionsKey.original_size: OriginalSize.Executive_7_25x10_5_in_
}

#original size don`t contains 3x5_in
job_copy_option_combi_original_size_three_multiply_five={
CopyEwsOptionsKey.original_size: OriginalSize.Executive_7_25x10_5_in_
}

job_copy_option_combi_original_size_four_multiply_six={
CopyEwsOptionsKey.original_size: OriginalSize.s_4x6_in_
}

job_copy_option_combi_original_size_five_multiply_seven={
CopyEwsOptionsKey.original_size: OriginalSize.s_5x7_in_
}

job_copy_option_combi_original_size_five_multiply_eight={
CopyEwsOptionsKey.original_size: OriginalSize.s_5x8_in_
}

job_copy_option_combi_original_size_letter={
CopyEwsOptionsKey.original_size: OriginalSize.Letter_8_5x11_in_
}

job_copy_option_combi_original_size_SEF_letter={
CopyEwsOptionsKey.original_size: OriginalSize.SEF_Letter_8_5x11_in_
}

job_copy_option_combi_original_size_16K_195_270={
CopyEwsOptionsKey.original_size: OriginalSize.s_16K_195x270_mm
}

job_copy_option_combi_original_size_16K_197_273={
CopyEwsOptionsKey.original_size: OriginalSize.s_16K_197x273_mm
}

job_copy_option_combi_original_size_statement={
CopyEwsOptionsKey.original_size: OriginalSize.Statement_8_5x5_5_in_
}

job_copy_option_combi_original_size_envelop_c6={
CopyEwsOptionsKey.original_size: OriginalSize.Envelope_C6_114x162_mm
}

job_copy_option_combi_original_size_envelop_dl={
CopyEwsOptionsKey.original_size: OriginalSize.Envelope_DL_110x220_mm
}

job_copy_option_combi_original_size_b5_jis={
CopyEwsOptionsKey.original_size: OriginalSize.B5_JIS
}

job_copy_option_combi_original_size_SEF_b5_jis={
CopyEwsOptionsKey.original_size: OriginalSize.SEF_B5_JIS
}

job_copy_option_combi_original_size_japanese_envelop={
CopyEwsOptionsKey.original_size: OriginalSize.Japanese_Envelope_Chou_3_120x235_mm
}

#no Postcard_JIS
job_copy_option_combi_original_size_postcard_jis={
CopyEwsOptionsKey.original_size: OriginalSize.jpn_hagaki_100x148mm
}

#no 3.9*7.5
job_copy_option_combi_original_envelop_monarch={
CopyEwsOptionsKey.original_size: OriginalSize.na_monarch_3_87x7_5in
}
job_copy_option_combi_original_envelop_10={
CopyEwsOptionsKey.original_size: OriginalSize.Envelope_10_4_1x9_5_in_
}
job_copy_option_combi_original_na_personal_3_625x6_5in={
CopyEwsOptionsKey.original_size:  OriginalSize.na_personal_3_625x6_5in
}
job_copy_option_combi_original_oe_photo_l_3_5x5in={
CopyEwsOptionsKey.original_size: OriginalSize.oe_photo_l_3_5x5in
}
job_copy_option_combi_original_10x15={
CopyEwsOptionsKey.original_size:  OriginalSize.om_small_photo_100x150mm
}
job_copy_option_combi_original_oe_square_photo_5x5in={
CopyEwsOptionsKey.original_size:  OriginalSize.oe_square_photo_5x5in
}
job_copy_option_combi_original_16K_184x260={
CopyEwsOptionsKey.original_size: OriginalSize.s_16K_184x260_mm
}
job_copy_option_combi_original_3x5_in={
CopyEwsOptionsKey.original_size: OriginalSize.na_index_3x5_3x5in
}

#Paper Size
job_copy_option_combi_paper_size_match_original = {
CopyEwsOptionsKey.paper_size: PaperSize.Match_Original
}

job_copy_option_combi_paper_size_custom = {
CopyEwsOptionsKey.paper_size: PaperSize.custom
}

job_copy_option_combi_unit_millimeters = {
CopyEwsOptionsKey.unit_of_measurement: UnitOfMeasure.millimeters
}

job_copy_option_combi_unit_inches = {
	CopyEwsOptionsKey.unit_of_measurement: UnitOfMeasure.inches
}

job_copy_option_combi_paper_size_A4 = {
CopyEwsOptionsKey.paper_size: PaperSize.A4_210x297_mm
}

job_copy_option_combi_paper_size_SEF_A4 = {
CopyEwsOptionsKey.paper_size: PaperSize.SEF_A4_210x297_mm
}

job_copy_option_combi_paper_size_A5 = {
CopyEwsOptionsKey.paper_size: PaperSize.A5_148x210_mm
}

job_copy_option_combi_paper_size_SEF_A5 = {
CopyEwsOptionsKey.paper_size: PaperSize.SEF_A5_148x210_mm
}

job_copy_option_combi_paper_size_A6 = {
CopyEwsOptionsKey.paper_size: PaperSize.A6_105x148_mm
}

job_copy_option_combi_paper_size_envelop_b5 = {
CopyEwsOptionsKey.paper_size: PaperSize.Envelope_B5_176x250_mm
}

job_copy_option_combi_paper_size_B6_Jis = {
CopyEwsOptionsKey.paper_size: PaperSize.B6_JIS_128x182_mm
}

job_copy_option_combi_paper_size_envelop_c5 = {
CopyEwsOptionsKey.paper_size: PaperSize.Envelope_C5_162x229_mm
}

job_copy_option_combi_paper_size_double_postcard_jis={
CopyEwsOptionsKey.paper_size: PaperSize.Double_Postcard_JIS
}

job_copy_option_combi_paper_size_executive={
CopyEwsOptionsKey.paper_size: PaperSize.Executive_7_25x10_5_in_
}

#original size don`t contains 3x5_in
job_copy_option_combi_paper_size_three_multiply_five={
CopyEwsOptionsKey.paper_size: PaperSize.Executive_7_25x10_5_in_
}

job_copy_option_combi_paper_size_four_multiply_six={
CopyEwsOptionsKey.paper_size: PaperSize.s_4x6_in_
}

job_copy_option_combi_paper_size_five_multiply_seven={
CopyEwsOptionsKey.paper_size: PaperSize.s_5x7_in_
}

job_copy_option_combi_paper_size_five_multiply_eight={
CopyEwsOptionsKey.paper_size: PaperSize.s_5x8_in_
}

job_copy_option_combi_paper_size_letter={
CopyEwsOptionsKey.paper_size: PaperSize.Letter_8_5x11_in_
}

job_copy_option_combi_paper_size_SEF_letter={
CopyEwsOptionsKey.paper_size: PaperSize.SEF_Letter_8_5x11_in_
}

job_copy_option_combi_paper_size_16K_195_270={
CopyEwsOptionsKey.paper_size: PaperSize.s_16K_195x270_mm
}

job_copy_option_combi_paper_size_16K_197_273={
CopyEwsOptionsKey.paper_size: PaperSize.s_16K_197x273_mm
}

job_copy_option_combi_paper_size_statement={
CopyEwsOptionsKey.paper_size: PaperSize.Statement_8_5x5_5_in_
}

job_copy_option_combi_paper_size_envelop_c6={
CopyEwsOptionsKey.paper_size: PaperSize.Envelope_C6_114x162_mm
}

job_copy_option_combi_paper_size_envelop_dl={
CopyEwsOptionsKey.paper_size: PaperSize.Envelope_DL_110x220_mm
}

job_copy_option_combi_paper_size_b5_jis={
CopyEwsOptionsKey.paper_size: PaperSize.B5_JIS
}

job_copy_option_combi_paper_size_SEF_b5_jis={
CopyEwsOptionsKey.paper_size: PaperSize.SEF_B5_JIS
}

job_copy_option_combi_paper_size_japanese_envelop={
CopyEwsOptionsKey.paper_size: PaperSize.Japanese_Envelope_Chou_3_120x235_mm
}

#no Postcard_JIS
job_copy_option_combi_paper_size_postcard_jis={
CopyEwsOptionsKey.paper_size: PaperSize.jpn_hagaki_100x148mm
}

#no 3.9*7.5
job_copy_option_combi_original_envelop_monarch={
CopyEwsOptionsKey.paper_size: PaperSize.na_monarch_3_87x7_5in
}
job_copy_option_combi_original_envelop_10={
CopyEwsOptionsKey.paper_size: PaperSize.Envelope_10_4_1x9_5_in_
}
job_copy_option_combi_original_na_personal_3_625x6_5in={
CopyEwsOptionsKey.paper_size:  PaperSize.na_personal_3_625x6_5in
}
job_copy_option_combi_original_oe_photo_l_3_5x5in={
CopyEwsOptionsKey.paper_size: PaperSize.oe_photo_l_3_5x5in
}
job_copy_option_combi_original_10x15={
CopyEwsOptionsKey.paper_size:  PaperSize.om_small_photo_100x150mm
}
job_copy_option_combi_original_oe_square_photo_5x5in={
CopyEwsOptionsKey.paper_size:  PaperSize.oe_square_photo_5x5in
}
job_copy_option_combi_original_16K_184x260={
CopyEwsOptionsKey.paper_size: PaperSize.s_16K_184x260_mm
}
job_copy_option_combi_original_3x5_in={
CopyEwsOptionsKey.paper_size: PaperSize.na_index_3x5_3x5in
}

job_copy_option_combi_colorMode_automatic={
CopyEwsOptionsKey.color_mode: ColorMode.automatic
}
job_copy_applying_pages_per_sheet_two = {
    CopyEwsOptionsKey.pages_per_sheet: PagesPerSheet.two
}

job_copy_option_combi_auto_tone_level_5={
CopyEwsOptionsKey.auto_tone: True,
CopyEwsOptionsKey.auto_tone_level: AutoToneLevel.five
}

job_copy_option_combi_auto_paper_color_level_5={
CopyEwsOptionsKey.auto_paper_color_removal: True,
CopyEwsOptionsKey.auto_paper_color_removal_level: AutoPaperColorRemovalLevel.five
}

job_copy_option_combi_colorMode_color={
CopyEwsOptionsKey.color_mode: ColorMode.color
}

job_copy_option_combi_colorMode_grayscale={
CopyEwsOptionsKey.color_mode: ColorMode.grayscale
}

#Paper Tray
job_copy_option_combi_paper_tray_manual={
CopyEwsOptionsKey.select_tray: PaperTray.manual_feed
}

job_copy_applying_with_different_combinations_one= {
    CopyEwsOptionsKey.number_of_copies: 99,
    CopyEwsOptionsKey.two_sided: TwoSided.one_to_two_sided,
    CopyEwsOptionsKey.color_mode: ColorMode.grayscale,
    CopyEwsOptionsKey.pages_per_sheet: PagesPerSheet.two,
    CopyEwsOptionsKey.two_sided_pages_flip_up: False,
    CopyEwsOptionsKey.original_size: OriginalSize.Legal_8_5x14_in_,
    # No scaling while pagesPerSheet is 2
    # CopyEwsOptionsKey.output_scale: OutputScale.letter_to_A4,
    CopyEwsOptionsKey.select_tray: PaperTray.tray2,
    # CopyEwsOptionsKey.quality: Quality.draft,
    CopyEwsOptionsKey.lighter_darker: LighterDarker.one,
    CopyEwsOptionsKey.content_type: ContentType.mixed,
    CopyEwsOptionsKey.collate: True
}

job_copy_applying_with_different_combinations_two= {
    CopyEwsOptionsKey.number_of_copies: 50,
    CopyEwsOptionsKey.two_sided: TwoSided.two_to_one_sided,
    CopyEwsOptionsKey.pages_per_sheet: PagesPerSheet.one,
    CopyEwsOptionsKey.two_sided_pages_flip_up: True,
    CopyEwsOptionsKey.original_size: OriginalSize.A5_148x210_mm,
    CopyEwsOptionsKey.output_scale: OutputScale.letter_to_A4,
    CopyEwsOptionsKey.select_tray: PaperTray.tray3,
    # CopyEwsOptionsKey.quality: Quality.best,
    CopyEwsOptionsKey.lighter_darker: LighterDarker.nine,
    CopyEwsOptionsKey.content_type: ContentType.photograph,
    CopyEwsOptionsKey.collate: False
}
# no color_mode  Automatic
job_copy_applying_with_different_combinations_three= {
    CopyEwsOptionsKey.number_of_copies: 1,
    CopyEwsOptionsKey.two_sided: TwoSided.two_to_two_sided,
    #no color_mode  Automatic
    CopyEwsOptionsKey.color_mode: ColorMode.automatic,
    CopyEwsOptionsKey.pages_per_sheet: PagesPerSheet.two,
    CopyEwsOptionsKey.two_sided_pages_flip_up: True,
    CopyEwsOptionsKey.original_size: OriginalSize.A4_210x297_mm,
    # No scaling while pagesPerSheet is 2
    # CopyEwsOptionsKey.output_scale: OutputScale.legal_to_letter,
    CopyEwsOptionsKey.select_tray: PaperTray.auto,
    # CopyEwsOptionsKey.quality: Quality.standard,
    CopyEwsOptionsKey.lighter_darker: LighterDarker.three,
    CopyEwsOptionsKey.content_type: ContentType.text,
    CopyEwsOptionsKey.collate: True
}

job_copy_applying_with_different_combinations_four= {
    CopyEwsOptionsKey.number_of_copies: 90,
    CopyEwsOptionsKey.two_sided: TwoSided.one_to_one_sided,
    CopyEwsOptionsKey.pages_per_sheet: PagesPerSheet.one,
    # No pagesFlipUp when two-sided is 1-to-1
    # CopyEwsOptionsKey.two_sided_pages_flip_up: False,
    CopyEwsOptionsKey.original_size: OriginalSize.Letter_8_5x11_in_,
    CopyEwsOptionsKey.output_scale: OutputScale.custom,
    CopyEwsOptionsKey.select_tray: PaperTray.tray1,
    # CopyEwsOptionsKey.quality: Quality.best,
    CopyEwsOptionsKey.lighter_darker: LighterDarker.seven,
    CopyEwsOptionsKey.content_type: ContentType.mixed,
    CopyEwsOptionsKey.collate: True
}

job_copy_applying_with_different_combinations_five= {
    CopyEwsOptionsKey.number_of_copies: 3,
    CopyEwsOptionsKey.two_sided: TwoSided.one_to_one_sided,
    CopyEwsOptionsKey.color_mode: ColorMode.grayscale,
    CopyEwsOptionsKey.pages_per_sheet: PagesPerSheet.one,
    # No pagesFlipUp when two-sided is 1-to-1
    # CopyEwsOptionsKey.two_sided_pages_flip_up: False,
    CopyEwsOptionsKey.original_size: OriginalSize.Letter_8_5x11_in_,
    CopyEwsOptionsKey.select_tray: PaperTray.auto,
    CopyEwsOptionsKey.lighter_darker: LighterDarker.four,
    CopyEwsOptionsKey.content_type: ContentType.mixed,
    CopyEwsOptionsKey.collate: True
}

expected_default_settings = {	
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
			"scaleToFitEnabled": "false",
			"xScalePercent": 100,
			"yScalePercent": 100,
			"scaleSelection": "none"
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
			"duplexBinding": "oneSided"
		}
	}
}

expected_default_original_settings = {	
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
			"scaleToFitEnabled": "false",
			"xScalePercent": 100,
			"yScalePercent": 100,
			"scaleSelection": "none"
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
			"duplexBinding": "oneSided"
		}
	}
}

excepted_reboot_settings = {
	"src": {
		"scan": {
			"colorMode": "color",
			"mediaSource": "adf",
			"mediaSize": "iso_a4_210x297mm",
			"plexMode": "duplex",
			"contentType": "text",
			"contentOrientation": "portrait",
			"pagesFlipUpEnabled": "false"
		}
	},
	"pipelineOptions": {
		"imageModifications": {
			"exposure": 6,
      		"blankPageSuppressionEnabled": "false"
		},	
		"scaling": {
			"scaleToFitEnabled": "false",
			"xScalePercent": 50,
			"yScalePercent": 50,
			"scaleSelection": "custom"
		}
	},
	"dest": {
		"print": {
			"collate": "uncollated",
			"copies": 17,
			"mediaSource": "tray-3",
			"mediaSize": "na_letter_8.5x11in",
			"mediaType": "stationery",
			"plexMode": "simplex",
			"duplexBinding": "oneSided"
		}
	}
}

expected_custom_value_settings = {	
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
			"scaleToFitEnabled": "false",
			"xScalePercent": 25,
			"yScalePercent": 25,
			"scaleSelection": "custom"
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
			"duplexBinding": "oneSided"
		}
	}
}

applying_with_different_combinations_one_expected_settings={
	"src": {
		"scan": {
			"colorMode": "grayscale",
			"mediaSource": "adf",
			"mediaSize": "na_legal_8.5x14in",
			"plexMode": "simplex",
			"contentType": "mixed",
			"contentOrientation": "portrait",
			"pagesFlipUpEnabled": "false"
		}
	},
	"pipelineOptions": {
		"imageModifications": {
			"exposure": 1
		},
		"scaling": {
			"scaleToFitEnabled": "false",
			"xScalePercent": 100,
			"yScalePercent": 100,
			"scaleSelection": "none"
		}
	},
	"dest": {
		"print": {
			"collate": "collated",
			"copies": 99,
			"mediaSource": "tray-2",
			"mediaSize": "na_letter_8.5x11in",
			"mediaType": "stationery",
			"plexMode": "duplex",
			"duplexBinding": "twoSidedLongEdge"
		}
	}
}

applying_with_different_combinations_two_expected_settings={
	"src": {
		"scan": {
			"colorMode": "color",
			"mediaSource": "adf",
			"mediaSize": "iso_a5_148x210mm",
			"plexMode": "duplex",
			"contentType": "photo",
			"contentOrientation": "portrait",
			"pagesFlipUpEnabled": "true"
		}
	},
	"pipelineOptions": {
		"imageModifications": {
			"exposure": 9
		},
		"scaling": {
			"scaleToFitEnabled": "false",
			"xScalePercent": 94,
			"yScalePercent": 94,
			"scaleSelection": "letterToA4"
		}
	},
	"dest": {
		"print": {
			"collate": "uncollated",
			"copies": 50,
			"mediaSource": "tray-3",
			"mediaSize": "na_letter_8.5x11in",
			"mediaType": "stationery",
			"plexMode": "simplex",
			"duplexBinding": "oneSided"
		}
	}
}
# no color_mode  Automatic
applying_with_different_combinations_three_expected_settings={}


applying_with_different_combinations_four_expected_settings={
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
			"exposure": 7
		},
		"scaling": {
			"scaleToFitEnabled": "false",
			"xScalePercent": 100,
			"yScalePercent": 100,
			"scaleSelection": "custom"
		}
	},
	"dest": {
		"print": {
			"collate": "collated",
			"copies": 90,
			"mediaSource": "tray-1",
			"mediaSize": "na_letter_8.5x11in",
			"mediaType": "stationery",
			"plexMode": "simplex",
			"duplexBinding": "oneSided"
		}
	}
}

applying_with_different_combinations_five_expected_settings={
	"src": {
		"scan": {
			"colorMode": "grayscale",
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
			"exposure": 4
		},
		"scaling": {
			"scaleToFitEnabled": "false",
			"xScalePercent": 100,
			"yScalePercent": 100,
			"scaleSelection": "none"
		}
	},
	"dest": {
		"print": {
			"collate": "collated",
			"copies": 3,
			"mediaSource": "auto",
			"mediaSize": "na_letter_8.5x11in",
			"mediaType": "stationery",
			"plexMode": "simplex",
			"duplexBinding": "oneSided"
		}
	}
}

def applying_with_different_combinations_one_expected_settings_from_actual_cdm(ews):
    """
    Check data configuration with cdm
    @param: actual_settings ->  for checking field, please refer to bottom sample data
    @return:
    """
    # pick up the paramters that need to be validate
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()

    scan_setting = default_value["src"]["scan"]
    scaling_setting = default_value["pipelineOptions"]["scaling"]
    print_setting = default_value["dest"]["print"]
    validated_settings = {
		"src": {
			"scan": {
				"colorMode":"grayscale",
				"mediaSource": scan_setting["mediaSource"],
				"mediaSize": "na_legal_8.5x14in",
				"plexMode": scan_setting["plexMode"],
				"contentType": scan_setting["contentType"],
				"contentOrientation": scan_setting["contentOrientation"],
				"pagesFlipUpEnabled": scan_setting["pagesFlipUpEnabled"]
			}
		},
		"pipelineOptions": {
			"imageModifications": {
				"exposure": 1
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
				"copies": 99,
				"mediaSource": "tray-2",
				"mediaSize": print_setting["mediaSize"],
				"mediaType": print_setting["mediaType"],
				"plexMode": "duplex",
				"duplexBinding": "twoSidedLongEdge"
			}
		}
    }

    return validated_settings
