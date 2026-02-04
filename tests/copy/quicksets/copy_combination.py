from dunetuf.ews.pom.quick_sets.quicksets_enum import *

copy_title_name = "Auto_Test_Quick_Set_Copy"
copy_description = "Just For Auto Test"
valid_255_characters = "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcda" \
                       "bcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdab" \
                       "cdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabc" \
                       "dabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd" \
                       "abcdabcdabcdabcdabcdabcdhjcuhdbfjikxdsvnlop"
valid_special_characters = "!@#$%^&{:>"
valid_one_characters = "a"

copy_quicksets_name_list = [
    'Auto_Test_Quick_Set_Copy1',
    'Auto_Test_Quick_Set_Copy2',
    'Auto_Test_Quick_Set_Copy3',
    'Auto_Test_Quick_Set_Copy4',
    'Auto_Test_Quick_Set_Copy5',
    'Auto_Test_Quick_Set_Email1',
    'Auto_Test_Quick_Set_Email2',
    'Auto_Test_Quick_Set_Usb1',
    'Auto_Test_Quick_Set_Usb2',
    'Auto_Test_Quick_Set_Network_Folder1',
]

quicksets_name_list = ['a','b','c','d','e','f','g','h','i','j']

# Remove CopyOptionsKey.two_sided_pages_flip_up setting when CopySides sets to 1-1 sided, as this setting is not supported for 1-1 sided.
# Delete color and original. The default values (color<->Autodetect / letter<->Any) for Homepro(selene) and Enterprsie(hpMfp) models are different.
# Delete papar size. The default values (letter <-> any(=Match Original size)) for Homepro(selene) and Enterprsie(hpMfp) models are different.
# Copy option settings for default
copy_option_default = {
    CopyOptionsKey.sides: CopyOptions.CopySides.one_to_one_sided,
    CopyOptionsKey.number_of_copies: 1,
    CopyOptionsKey.output_scale: CopyOptions.CopyOutputScale.none,
    CopyOptionsKey.paper_type: CopyOptions.CopyPaperType.plain,
    CopyOptionsKey.paper_tray: CopyOptions.CopyPaperTray.auto,
    CopyOptionsKey.lighter_darker: CopyOptions.CopyLighterDarker.five,
    CopyOptionsKey.content_type: CopyOptions.CopyContentType.mixed,
    CopyOptionsKey.pages_per_sheet: CopyOptions.CopyPagesperSheet.one,
    CopyOptionsKey.collate: True
}

copy_option_quality_standard = {
    CopyOptionsKey.sides: CopyOptions.CopySides.one_to_one_sided,
    CopyOptionsKey.number_of_copies: 1,
    CopyOptionsKey.output_scale: CopyOptions.CopyOutputScale.none,
    CopyOptionsKey.paper_type: CopyOptions.CopyPaperType.plain,
    CopyOptionsKey.paper_tray: CopyOptions.CopyPaperTray.auto,
    CopyOptionsKey.lighter_darker: CopyOptions.CopyLighterDarker.five,
    CopyOptionsKey.content_type: CopyOptions.CopyContentType.mixed,
    CopyOptionsKey.pages_per_sheet: CopyOptions.CopyPagesperSheet.one,
    CopyOptionsKey.collate: True,
    CopyOptionsKey.quality: CopyOptions.CopyQuality.standard
}

copy_option_quality_best = {
    CopyOptionsKey.sides: CopyOptions.CopySides.one_to_one_sided,
    CopyOptionsKey.number_of_copies: 1,
    CopyOptionsKey.output_scale: CopyOptions.CopyOutputScale.none,
    CopyOptionsKey.paper_type: CopyOptions.CopyPaperType.plain,
    CopyOptionsKey.paper_tray: CopyOptions.CopyPaperTray.auto,
    CopyOptionsKey.lighter_darker: CopyOptions.CopyLighterDarker.five,
    CopyOptionsKey.content_type: CopyOptions.CopyContentType.mixed,
    CopyOptionsKey.pages_per_sheet: CopyOptions.CopyPagesperSheet.one,
    CopyOptionsKey.collate: True,
    CopyOptionsKey.quality: CopyOptions.CopyQuality.best
}

copy_option_quality_draft = {
    CopyOptionsKey.sides: CopyOptions.CopySides.one_to_one_sided,
    CopyOptionsKey.number_of_copies: 1,
    CopyOptionsKey.output_scale: CopyOptions.CopyOutputScale.none,
    CopyOptionsKey.paper_type: CopyOptions.CopyPaperType.plain,
    CopyOptionsKey.paper_tray: CopyOptions.CopyPaperTray.auto,
    CopyOptionsKey.lighter_darker: CopyOptions.CopyLighterDarker.five,
    CopyOptionsKey.content_type: CopyOptions.CopyContentType.mixed,
    CopyOptionsKey.pages_per_sheet: CopyOptions.CopyPagesperSheet.one,
    CopyOptionsKey.collate: True,
    CopyOptionsKey.quality: CopyOptions.CopyQuality.draft
}

# Copy option settings for combi1
#DUNE-223694 PageFlipUp option only available for duplex hence changing sides to two to two sided
copy_option_combi1 = {
    CopyOptionsKey.sides: CopyOptions.CopySides.two_to_two_sided,
    CopyOptionsKey.two_sided_pages_flip_up: True,
    CopyOptionsKey.color: CopyOptions.Color.automatic,
    CopyOptionsKey.original_size: CopyOptions.CopyOriginalSize.A3_297x420_mm,
    CopyOptionsKey.number_of_copies: 1,
    CopyOptionsKey.output_scale: CopyOptions.CopyOutputScale.none,
    CopyOptionsKey.paper_size: CopyOptions.CopyPaperSize.A4_210x297mm,
    CopyOptionsKey.paper_type: CopyOptions.CopyPaperType.any_type,
    CopyOptionsKey.paper_tray: CopyOptions.CopyPaperTray.auto,
    CopyOptionsKey.lighter_darker: CopyOptions.CopyLighterDarker.six,
    CopyOptionsKey.content_type: CopyOptions.CopyContentType.mixed,
    CopyOptionsKey.pages_per_sheet: CopyOptions.CopyPagesperSheet.one,
    CopyOptionsKey.collate: True
}

# Copy option settings for combi2
copy_option_combi2 = {
    CopyOptionsKey.sides: CopyOptions.CopySides.two_to_one_sided,
    CopyOptionsKey.two_sided_pages_flip_up: False,
    CopyOptionsKey.original_size: CopyOptions.CopyOriginalSize.Any_size,
    CopyOptionsKey.number_of_copies: 5,
    CopyOptionsKey.output_scale: CopyOptions.CopyOutputScale.fit_to_page,
    CopyOptionsKey.paper_size: CopyOptions.CopyPaperSize.custom,
    CopyOptionsKey.paper_type: CopyOptions.CopyPaperType.plain,
    CopyOptionsKey.paper_tray: CopyOptions.CopyPaperTray.auto,
    CopyOptionsKey.lighter_darker: CopyOptions.CopyLighterDarker.nine,
    CopyOptionsKey.content_type: CopyOptions.CopyContentType.photograph,
    CopyOptionsKey.pages_per_sheet: CopyOptions.CopyPagesperSheet.one,
    CopyOptionsKey.collate: False
}

# Copy option settings with scan mode and standard document add pages
copy_option_combi_standard_doc_add_pages = {
    CopyOptionsKey.sides: CopyOptions.CopySides.two_to_one_sided,
    CopyOptionsKey.two_sided_pages_flip_up: False,
    CopyOptionsKey.original_size: CopyOptions.CopyOriginalSize.Any_size,
    CopyOptionsKey.number_of_copies: 5,
    CopyOptionsKey.output_scale: CopyOptions.CopyOutputScale.fit_to_page,
    CopyOptionsKey.paper_size: CopyOptions.CopyPaperSize.custom,
    CopyOptionsKey.paper_type: CopyOptions.CopyPaperType.plain,
    CopyOptionsKey.paper_tray: CopyOptions.CopyPaperTray.auto,
    CopyOptionsKey.lighter_darker: CopyOptions.CopyLighterDarker.nine,
    CopyOptionsKey.content_type: CopyOptions.CopyContentType.photograph,
    CopyOptionsKey.pages_per_sheet: CopyOptions.CopyPagesperSheet.one,
    CopyOptionsKey.collate: False,
    CopyOptionsKey.scan_mode: CopyOptions.CopyScanMode.standardDocumentAddPages
}

# Copy option settings for combi3
copy_option_combi3 = {
    CopyOptionsKey.sides: CopyOptions.CopySides.two_to_two_sided,
    CopyOptionsKey.two_sided_pages_flip_up: False,
    CopyOptionsKey.original_size: CopyOptions.CopyOriginalSize.Letter_8_5x11_in_,
    CopyOptionsKey.number_of_copies: 99,
    CopyOptionsKey.output_scale: CopyOptions.CopyOutputScale.none,
    CopyOptionsKey.paper_size: CopyOptions.CopyPaperSize.letter_8_5x11in,
    CopyOptionsKey.paper_type: CopyOptions.CopyPaperType.plain,
    CopyOptionsKey.paper_tray: CopyOptions.CopyPaperTray.tray1,
    CopyOptionsKey.lighter_darker: CopyOptions.CopyLighterDarker.three,
    CopyOptionsKey.content_type: CopyOptions.CopyContentType.text,
    CopyOptionsKey.collate: False
}

# Copy option settings for combi4
copy_option_combi4 = {
    CopyOptionsKey.sides: CopyOptions.CopySides.one_to_one_sided,
    CopyOptionsKey.color: CopyOptions.Color.black_only,
    CopyOptionsKey.original_size: CopyOptions.OriginalSize.A4_210x297_mm,
    CopyOptionsKey.number_of_copies: 10,
    CopyOptionsKey.output_scale: CopyOptions.CopyOutputScale.fit_to_page,
    CopyOptionsKey.paper_size: CopyOptions.CopyPaperSize.A4_210x297mm,
    CopyOptionsKey.paper_type: CopyOptions.CopyPaperType.plain,
    CopyOptionsKey.paper_tray: CopyOptions.CopyPaperTray.tray3,
    CopyOptionsKey.lighter_darker: CopyOptions.CopyLighterDarker.one,
    CopyOptionsKey.content_type: CopyOptions.CopyContentType.text,
    CopyOptionsKey.pages_per_sheet: CopyOptions.CopyPagesperSheet.one,
    CopyOptionsKey.collate: True
}

# Copy option settings for combi5
copy_option_combi5 = {
    CopyOptionsKey.sides: CopyOptions.CopySides.one_to_one_sided,
    CopyOptionsKey.color: CopyOptions.Color.automatic,
    CopyOptionsKey.original_size: CopyOptions.OriginalSize.A5_148x210_mm,
    CopyOptionsKey.number_of_copies: 1,
    CopyOptionsKey.output_scale: CopyOptions.CopyOutputScale.full_page_A4_to_letter,
    CopyOptionsKey.paper_size: CopyOptions.CopyPaperSize.A5_148x210mm,
    CopyOptionsKey.paper_type: CopyOptions.CopyPaperType.HP_matte_120g,
    CopyOptionsKey.paper_tray: CopyOptions.CopyPaperTray.tray1,
    CopyOptionsKey.lighter_darker: CopyOptions.CopyLighterDarker.five,
    CopyOptionsKey.content_type: CopyOptions.CopyContentType.image,
    CopyOptionsKey.pages_per_sheet: CopyOptions.CopyPagesperSheet.one,
    CopyOptionsKey.collate: True
}

# Copy option settings for combi6
copy_option_combi6 = {
    CopyOptionsKey.sides: CopyOptions.CopySides.one_to_one_sided,
    CopyOptionsKey.color: CopyOptions.Color.automatic,
    CopyOptionsKey.original_size: CopyOptions.OriginalSize.s_4x6_in_,
    CopyOptionsKey.number_of_copies: 1,
    CopyOptionsKey.output_scale: CopyOptions.CopyOutputScale.letter_to_A4,
    CopyOptionsKey.paper_size: CopyOptions.CopyPaperSize.s_4x6in,
    CopyOptionsKey.paper_type: CopyOptions.CopyPaperType.HP_matte_150g,
    CopyOptionsKey.paper_tray: CopyOptions.CopyPaperTray.auto,
    CopyOptionsKey.lighter_darker: CopyOptions.CopyLighterDarker.five,
    CopyOptionsKey.content_type: CopyOptions.CopyContentType.glossy,
    CopyOptionsKey.pages_per_sheet: CopyOptions.CopyPagesperSheet.one,
    CopyOptionsKey.collate: True
}

# Copy option settings for combi7
copy_option_combi7 = {
    CopyOptionsKey.sides: CopyOptions.CopySides.one_to_one_sided,
    CopyOptionsKey.color: CopyOptions.Color.automatic,
    CopyOptionsKey.original_size: CopyOptions.OriginalSize.s_5x8_in_,
    CopyOptionsKey.number_of_copies: 1,
    CopyOptionsKey.output_scale: CopyOptions.CopyOutputScale.full_page_A4_to_letter,
    CopyOptionsKey.paper_size: CopyOptions.CopyPaperSize.s_5x8in,
    CopyOptionsKey.paper_type: CopyOptions.CopyPaperType.HP_matte_200g,
    CopyOptionsKey.paper_tray: CopyOptions.CopyPaperTray.auto,
    CopyOptionsKey.lighter_darker: CopyOptions.CopyLighterDarker.five,
    CopyOptionsKey.content_type: CopyOptions.CopyContentType.automatic,
    CopyOptionsKey.pages_per_sheet: CopyOptions.CopyPagesperSheet.one,
    CopyOptionsKey.collate: True
}

# Copy option settings for combi8
copy_option_combi8 = {
    CopyOptionsKey.sides: CopyOptions.CopySides.one_to_one_sided,
    CopyOptionsKey.color: CopyOptions.Color.automatic,
    CopyOptionsKey.original_size: CopyOptions.OriginalSize.Legal_8_5x14_in_,
    CopyOptionsKey.number_of_copies: 1,
    CopyOptionsKey.output_scale: CopyOptions.CopyOutputScale.full_page_A4_to_letter,
    CopyOptionsKey.paper_size: CopyOptions.CopyPaperSize.legal_8_5x14in,
    CopyOptionsKey.paper_type: CopyOptions.CopyPaperType.labels,
    CopyOptionsKey.paper_tray: CopyOptions.CopyPaperTray.auto,
    CopyOptionsKey.lighter_darker: CopyOptions.CopyLighterDarker.five,
    CopyOptionsKey.content_type: CopyOptions.CopyContentType.best,
    CopyOptionsKey.pages_per_sheet: CopyOptions.CopyPagesperSheet.one,
    CopyOptionsKey.collate: True
}

# Copy option settings for combi9
copy_option_combi9 = {
    CopyOptionsKey.sides: CopyOptions.CopySides.one_to_one_sided,
    CopyOptionsKey.color: CopyOptions.Color.automatic,
    CopyOptionsKey.original_size: CopyOptions.OriginalSize.A2_420x594_mm,
    CopyOptionsKey.number_of_copies: 1,
    CopyOptionsKey.output_scale: CopyOptions.CopyOutputScale.custom,
    CopyOptionsKey.precise_scaling_amount: 90,
    CopyOptionsKey.paper_size: CopyOptions.CopyPaperSize.A2_420x594mm,
    CopyOptionsKey.paper_type: CopyOptions.CopyPaperType.letterhead,
    CopyOptionsKey.paper_tray: CopyOptions.CopyPaperTray.auto,
    CopyOptionsKey.lighter_darker: CopyOptions.CopyLighterDarker.five,
    CopyOptionsKey.content_type: CopyOptions.CopyContentType.automatic,
    CopyOptionsKey.pages_per_sheet: CopyOptions.CopyPagesperSheet.one,
    CopyOptionsKey.collate: True
}

# Copy option settings for combi10
copy_option_combi10 = {
    CopyOptionsKey.sides: CopyOptions.CopySides.one_to_one_sided,
    CopyOptionsKey.color: CopyOptions.Color.automatic,
    CopyOptionsKey.original_size: CopyOptions.OriginalSize.Oficio_8_5x13_in_,
    CopyOptionsKey.number_of_copies: 1,
    CopyOptionsKey.output_scale: CopyOptions.CopyOutputScale.fit_to_page,
    CopyOptionsKey.paper_size: CopyOptions.CopyPaperSize.oficio_8_5x13in,
    CopyOptionsKey.paper_type: CopyOptions.CopyPaperType.envelop,
    CopyOptionsKey.paper_tray: CopyOptions.CopyPaperTray.auto,
    CopyOptionsKey.lighter_darker: CopyOptions.CopyLighterDarker.five,
    CopyOptionsKey.content_type: CopyOptions.CopyContentType.automatic,
    CopyOptionsKey.pages_per_sheet: CopyOptions.CopyPagesperSheet.one,
    CopyOptionsKey.collate: True
}

# Copy option settings for combi11
copy_option_combi11 = {
    CopyOptionsKey.sides: CopyOptions.CopySides.one_to_one_sided,
    CopyOptionsKey.color: CopyOptions.Color.automatic,
    CopyOptionsKey.original_size: CopyOptions.OriginalSize.Oficio_216x340_mm,
    CopyOptionsKey.number_of_copies: 1,
    CopyOptionsKey.output_scale: CopyOptions.CopyOutputScale.fit_to_page,
    CopyOptionsKey.paper_size: CopyOptions.CopyPaperSize.oficio_216x340mm,
    CopyOptionsKey.paper_type: CopyOptions.CopyPaperType.heavy_envelop,
    CopyOptionsKey.paper_tray: CopyOptions.CopyPaperTray.auto,
    CopyOptionsKey.lighter_darker: CopyOptions.CopyLighterDarker.five,
    CopyOptionsKey.content_type: CopyOptions.CopyContentType.automatic,
    CopyOptionsKey.pages_per_sheet: CopyOptions.CopyPagesperSheet.one,
    CopyOptionsKey.collate: True
}

# Copy option settings for combi12
copy_option_combi12 = {
    CopyOptionsKey.sides: CopyOptions.CopySides.one_to_one_sided,
    CopyOptionsKey.color: CopyOptions.Color.automatic,
    CopyOptionsKey.original_size: CopyOptions.OriginalSize.s_16K_195x270_mm,
    CopyOptionsKey.number_of_copies: 1,
    CopyOptionsKey.output_scale: CopyOptions.CopyOutputScale.fit_to_page,
    CopyOptionsKey.paper_size: CopyOptions.CopyPaperSize.s_16k_195x270mm,
    CopyOptionsKey.paper_type: CopyOptions.CopyPaperType.prepunched,
    CopyOptionsKey.paper_tray: CopyOptions.CopyPaperTray.auto,
    CopyOptionsKey.lighter_darker: CopyOptions.CopyLighterDarker.five,
    CopyOptionsKey.content_type: CopyOptions.CopyContentType.automatic,
    CopyOptionsKey.pages_per_sheet: CopyOptions.CopyPagesperSheet.one,
    CopyOptionsKey.collate: True
}

# Copy option settings for combi13
copy_option_combi13 = {
    CopyOptionsKey.sides: CopyOptions.CopySides.one_to_one_sided,
    CopyOptionsKey.color: CopyOptions.Color.automatic,
    CopyOptionsKey.original_size: CopyOptions.OriginalSize.s_16K_184x260_mm,
    CopyOptionsKey.number_of_copies: 1,
    CopyOptionsKey.output_scale: CopyOptions.CopyOutputScale.fit_to_page,
    CopyOptionsKey.paper_size: CopyOptions.CopyPaperSize.s_16k_184x260mm,
    CopyOptionsKey.paper_type: CopyOptions.CopyPaperType.colored,
    CopyOptionsKey.paper_tray: CopyOptions.CopyPaperTray.auto,
    CopyOptionsKey.lighter_darker: CopyOptions.CopyLighterDarker.five,
    CopyOptionsKey.content_type: CopyOptions.CopyContentType.automatic,
    CopyOptionsKey.pages_per_sheet: CopyOptions.CopyPagesperSheet.one,
    CopyOptionsKey.collate: True
}

# Copy option settings for combi14
copy_option_combi14 = {
    CopyOptionsKey.sides: CopyOptions.CopySides.one_to_one_sided,
    CopyOptionsKey.color: CopyOptions.Color.automatic,
    CopyOptionsKey.original_size: CopyOptions.OriginalSize.Double_Postcard_JIS,
    CopyOptionsKey.number_of_copies: 1,
    CopyOptionsKey.output_scale: CopyOptions.CopyOutputScale.fit_to_page,
    CopyOptionsKey.paper_size: CopyOptions.CopyPaperSize.double_postcard_JIS,
    CopyOptionsKey.paper_type: CopyOptions.CopyPaperType.bond,
    CopyOptionsKey.paper_tray: CopyOptions.CopyPaperTray.auto,
    CopyOptionsKey.lighter_darker: CopyOptions.CopyLighterDarker.five,
    CopyOptionsKey.content_type: CopyOptions.CopyContentType.automatic,
    CopyOptionsKey.pages_per_sheet: CopyOptions.CopyPagesperSheet.one,
    CopyOptionsKey.collate: True
}

# Copy option settings for combi15
copy_option_combi15 = {
    CopyOptionsKey.sides: CopyOptions.CopySides.one_to_one_sided,
    CopyOptionsKey.color: CopyOptions.Color.automatic,
    CopyOptionsKey.original_size: CopyOptions.OriginalSize.Envelope_10_4_1x9_5_in_,
    CopyOptionsKey.number_of_copies: 1,
    CopyOptionsKey.output_scale: CopyOptions.CopyOutputScale.fit_to_page,
    CopyOptionsKey.paper_size: CopyOptions.CopyPaperSize.envelope_10_4_1x9_5in,
    CopyOptionsKey.paper_type: CopyOptions.CopyPaperType.recycled,
    CopyOptionsKey.paper_tray: CopyOptions.CopyPaperTray.auto,
    CopyOptionsKey.lighter_darker: CopyOptions.CopyLighterDarker.five,
    CopyOptionsKey.content_type: CopyOptions.CopyContentType.automatic,
    CopyOptionsKey.pages_per_sheet: CopyOptions.CopyPagesperSheet.one,
    CopyOptionsKey.collate: True
}

# Copy option settings for combi16
copy_option_combi16 = {
    CopyOptionsKey.sides: CopyOptions.CopySides.one_to_one_sided,
    CopyOptionsKey.color: CopyOptions.Color.automatic,
    CopyOptionsKey.original_size: CopyOptions.OriginalSize.Envelop_Monarch,
    CopyOptionsKey.number_of_copies: 1,
    CopyOptionsKey.output_scale: CopyOptions.CopyOutputScale.fit_to_page,
    CopyOptionsKey.paper_size: CopyOptions.CopyPaperSize.envelop_monarch,
    CopyOptionsKey.paper_type: CopyOptions.CopyPaperType.HP_glossy_150g,
    CopyOptionsKey.paper_tray: CopyOptions.CopyPaperTray.auto,
    CopyOptionsKey.lighter_darker: CopyOptions.CopyLighterDarker.five,
    CopyOptionsKey.content_type: CopyOptions.CopyContentType.automatic,
    CopyOptionsKey.pages_per_sheet: CopyOptions.CopyPagesperSheet.one,
    CopyOptionsKey.collate: True
}

# Copy option settings for combi17
copy_option_combi17 = {
    CopyOptionsKey.sides: CopyOptions.CopySides.one_to_one_sided,
    CopyOptionsKey.color: CopyOptions.Color.automatic,
    CopyOptionsKey.original_size: CopyOptions.OriginalSize.Envelope_B5_176x250_mm,
    CopyOptionsKey.number_of_copies: 1,
    CopyOptionsKey.output_scale: CopyOptions.CopyOutputScale.fit_to_page,
    CopyOptionsKey.paper_size: CopyOptions.CopyPaperSize.envelop_B5,
    CopyOptionsKey.paper_type: CopyOptions.CopyPaperType.HP_trifold_glossy,
    CopyOptionsKey.paper_tray: CopyOptions.CopyPaperTray.auto,
    CopyOptionsKey.lighter_darker: CopyOptions.CopyLighterDarker.five,
    CopyOptionsKey.content_type: CopyOptions.CopyContentType.automatic,
    CopyOptionsKey.pages_per_sheet: CopyOptions.CopyPagesperSheet.one,
    CopyOptionsKey.collate: True
}

# Copy option settings for combi18
copy_option_combi18 = {
    CopyOptionsKey.sides: CopyOptions.CopySides.one_to_one_sided,
    CopyOptionsKey.color: CopyOptions.Color.automatic,
    CopyOptionsKey.original_size: CopyOptions.OriginalSize.Executive_7_25x10_5_in_,
    CopyOptionsKey.number_of_copies: 1,
    CopyOptionsKey.output_scale: CopyOptions.CopyOutputScale.fit_to_page,
    CopyOptionsKey.paper_size: CopyOptions.CopyPaperSize.executive_7_25x10_5in,
    CopyOptionsKey.paper_type: CopyOptions.CopyPaperType.HP_glossy_200g,
    CopyOptionsKey.paper_tray: CopyOptions.CopyPaperTray.auto,
    CopyOptionsKey.lighter_darker: CopyOptions.CopyLighterDarker.five,
    CopyOptionsKey.content_type: CopyOptions.CopyContentType.automatic,
    CopyOptionsKey.pages_per_sheet: CopyOptions.CopyPagesperSheet.one,
    CopyOptionsKey.collate: True
}

# Copy option settings for combi19
copy_option_combi19 = {
    CopyOptionsKey.sides: CopyOptions.CopySides.one_to_one_sided,
    CopyOptionsKey.color: CopyOptions.Color.automatic,
    CopyOptionsKey.original_size: CopyOptions.OriginalSize.Postcard_JIS,
    CopyOptionsKey.number_of_copies: 1,
    CopyOptionsKey.output_scale: CopyOptions.CopyOutputScale.fit_to_page,
    CopyOptionsKey.paper_size: CopyOptions.CopyPaperSize.postcard_JIS_100x148,
    CopyOptionsKey.paper_type: CopyOptions.CopyPaperType.light,
    CopyOptionsKey.paper_tray: CopyOptions.CopyPaperTray.auto,
    CopyOptionsKey.lighter_darker: CopyOptions.CopyLighterDarker.five,
    CopyOptionsKey.content_type: CopyOptions.CopyContentType.automatic,
    CopyOptionsKey.pages_per_sheet: CopyOptions.CopyPagesperSheet.one,
    CopyOptionsKey.collate: True
}

# Copy option settings for combi20
copy_option_combi20 = {
    CopyOptionsKey.sides: CopyOptions.CopySides.one_to_one_sided,
    CopyOptionsKey.color: CopyOptions.Color.automatic,
    CopyOptionsKey.original_size: CopyOptions.OriginalSize.Double_Postcard_JIS,
    CopyOptionsKey.number_of_copies: 1,
    CopyOptionsKey.output_scale: CopyOptions.CopyOutputScale.fit_to_page,
    CopyOptionsKey.paper_size: CopyOptions.CopyPaperSize.double_postcard_JIS,
    CopyOptionsKey.paper_type: CopyOptions.CopyPaperType.intermediate,
    CopyOptionsKey.paper_tray: CopyOptions.CopyPaperTray.auto,
    CopyOptionsKey.lighter_darker: CopyOptions.CopyLighterDarker.five,
    CopyOptionsKey.content_type: CopyOptions.CopyContentType.automatic,
    CopyOptionsKey.pages_per_sheet: CopyOptions.CopyPagesperSheet.one,
    CopyOptionsKey.collate: True
}

# Copy option settings for combi21
copy_option_combi21 = {
    CopyOptionsKey.sides: CopyOptions.CopySides.one_to_one_sided,
    CopyOptionsKey.color: CopyOptions.Color.automatic,
    CopyOptionsKey.original_size: CopyOptions.OriginalSize.Envelope_10_4_1x9_5_in_,
    CopyOptionsKey.number_of_copies: 1,
    CopyOptionsKey.output_scale: CopyOptions.CopyOutputScale.fit_to_page,
    CopyOptionsKey.paper_size: CopyOptions.CopyPaperSize.envelope_10_4_1x9_5in,
    CopyOptionsKey.paper_type: CopyOptions.CopyPaperType.midweight,
    CopyOptionsKey.paper_tray: CopyOptions.CopyPaperTray.auto,
    CopyOptionsKey.lighter_darker: CopyOptions.CopyLighterDarker.five,
    CopyOptionsKey.content_type: CopyOptions.CopyContentType.automatic,
    CopyOptionsKey.pages_per_sheet: CopyOptions.CopyPagesperSheet.one,
    CopyOptionsKey.collate: True
}

# Copy option settings for combi22
copy_option_combi22 = {
    CopyOptionsKey.sides: CopyOptions.CopySides.one_to_one_sided,
    CopyOptionsKey.color: CopyOptions.Color.automatic,
    CopyOptionsKey.original_size: CopyOptions.OriginalSize.A3_297x420_mm,
    CopyOptionsKey.number_of_copies: 1,
    CopyOptionsKey.output_scale: CopyOptions.CopyOutputScale.fit_to_page,
    CopyOptionsKey.paper_size: CopyOptions.CopyPaperSize.A3_297x420mm,
    CopyOptionsKey.paper_type: CopyOptions.CopyPaperType.extra_heavy,
    CopyOptionsKey.paper_tray: CopyOptions.CopyPaperTray.auto,
    CopyOptionsKey.lighter_darker: CopyOptions.CopyLighterDarker.five,
    CopyOptionsKey.content_type: CopyOptions.CopyContentType.automatic,
    CopyOptionsKey.pages_per_sheet: CopyOptions.CopyPagesperSheet.one,
    CopyOptionsKey.collate: True
}

# Copy option settings for combi23
copy_option_combi23 = {
    CopyOptionsKey.sides: CopyOptions.CopySides.one_to_one_sided,
    CopyOptionsKey.color: CopyOptions.Color.automatic,
    CopyOptionsKey.original_size: CopyOptions.OriginalSize.Letter_8_5x11_in_,
    CopyOptionsKey.number_of_copies: 1,
    CopyOptionsKey.output_scale: CopyOptions.CopyOutputScale.fit_to_page,
    CopyOptionsKey.paper_size: CopyOptions.CopyPaperSize.letter_8_5x11in,
    CopyOptionsKey.paper_type: CopyOptions.CopyPaperType.cardstock,
    CopyOptionsKey.paper_tray: CopyOptions.CopyPaperTray.auto,
    CopyOptionsKey.lighter_darker: CopyOptions.CopyLighterDarker.five,
    CopyOptionsKey.content_type: CopyOptions.CopyContentType.automatic,
    CopyOptionsKey.pages_per_sheet: CopyOptions.CopyPagesperSheet.one,
    CopyOptionsKey.collate: True
}

# Copy option settings for combi24
copy_option_combi24 = {
    CopyOptionsKey.sides: CopyOptions.CopySides.one_to_one_sided,
    CopyOptionsKey.color: CopyOptions.Color.automatic,
    CopyOptionsKey.original_size: CopyOptions.OriginalSize.A4_210x297_mm,
    CopyOptionsKey.number_of_copies: 1,
    CopyOptionsKey.output_scale: CopyOptions.CopyOutputScale.fit_to_page,
    CopyOptionsKey.paper_size: CopyOptions.CopyPaperSize.A4_210x297mm,
    CopyOptionsKey.paper_type: CopyOptions.CopyPaperType.heavy_glossy,
    CopyOptionsKey.paper_tray: CopyOptions.CopyPaperTray.auto,
    CopyOptionsKey.lighter_darker: CopyOptions.CopyLighterDarker.five,
    CopyOptionsKey.content_type: CopyOptions.CopyContentType.automatic,
    CopyOptionsKey.pages_per_sheet: CopyOptions.CopyPagesperSheet.one,
    CopyOptionsKey.collate: True
}

#Copy option settings for combi25
copy_option_combi25 = {
    CopyOptionsKey.sides: CopyOptions.CopySides.one_to_one_sided,
    CopyOptionsKey.color: CopyOptions.Color.color,
    CopyOptionsKey.original_size: CopyOptions.OriginalSize.SEF_A4_210x297_mm,
    CopyOptionsKey.number_of_copies: 1,
    CopyOptionsKey.output_scale: CopyOptions.CopyOutputScale.none,
    CopyOptionsKey.paper_size: CopyOptions.CopyPaperSize.SEF_A4_210x297_mm,
    CopyOptionsKey.paper_type: CopyOptions.CopyPaperType.plain,
    CopyOptionsKey.lighter_darker: CopyOptions.CopyLighterDarker.five,
    CopyOptionsKey.content_type: CopyOptions.CopyContentType.mixed,
    CopyOptionsKey.pages_per_sheet: CopyOptions.CopyPagesperSheet.one,
    CopyOptionsKey.collate: True,
    CopyOptionsKey.blank_page_suppression: True
}

#Copy option settings for combi26
copy_option_combi26 = {
    CopyOptionsKey.sides: CopyOptions.CopySides.one_to_one_sided,
    CopyOptionsKey.color: CopyOptions.Color.color,
    CopyOptionsKey.original_size: CopyOptions.OriginalSize.A4_210x297_mm,
    CopyOptionsKey.number_of_copies: 1,
    CopyOptionsKey.output_scale: CopyOptions.CopyOutputScale.none,
    CopyOptionsKey.paper_size: CopyOptions.CopyPaperSize.A4_210x297mm,
    CopyOptionsKey.paper_type: CopyOptions.CopyPaperType.plain,
    CopyOptionsKey.lighter_darker: CopyOptions.CopyLighterDarker.five,
    CopyOptionsKey.content_type: CopyOptions.CopyContentType.mixed,
    CopyOptionsKey.pages_per_sheet: CopyOptions.CopyPagesperSheet.one,
    CopyOptionsKey.collate: True,
    CopyOptionsKey.blank_page_suppression: True
}

#Copy option settings for combi27
copy_option_combi27 = {
    CopyOptionsKey.sides: CopyOptions.CopySides.one_to_one_sided,
    CopyOptionsKey.color: CopyOptions.Color.color,
    CopyOptionsKey.original_size: CopyOptions.OriginalSize.A4_210x297_mm,
    CopyOptionsKey.number_of_copies: 1,
    CopyOptionsKey.output_scale: CopyOptions.CopyOutputScale.none,
    CopyOptionsKey.paper_size: CopyOptions.CopyPaperSize.A4_210x297mm,
    CopyOptionsKey.paper_type: CopyOptions.CopyPaperType.plain,
    CopyOptionsKey.lighter_darker: CopyOptions.CopyLighterDarker.five,
    CopyOptionsKey.content_type: CopyOptions.CopyContentType.mixed,
    CopyOptionsKey.pages_per_sheet: CopyOptions.CopyPagesperSheet.one,
    CopyOptionsKey.collate: True,
    CopyOptionsKey.blank_page_suppression: True,
    CopyOptionsKey.finisher_staple: CopyOptions.CopyStaple.topRightOnePointAngled
}

#Copy option settings for combi28
copy_option_combi28 = {
    CopyOptionsKey.sides: CopyOptions.CopySides.one_to_one_sided,
    CopyOptionsKey.color: CopyOptions.Color.color,
    CopyOptionsKey.original_size: CopyOptions.OriginalSize.A4_210x297_mm,
    CopyOptionsKey.number_of_copies: 1,
    CopyOptionsKey.output_scale: CopyOptions.CopyOutputScale.none,
    CopyOptionsKey.paper_size: CopyOptions.CopyPaperSize.A4_210x297mm,
    CopyOptionsKey.paper_type: CopyOptions.CopyPaperType.plain,
    CopyOptionsKey.lighter_darker: CopyOptions.CopyLighterDarker.five,
    CopyOptionsKey.content_type: CopyOptions.CopyContentType.mixed,
    CopyOptionsKey.pages_per_sheet: CopyOptions.CopyPagesperSheet.one,
    CopyOptionsKey.collate: True,
    CopyOptionsKey.blank_page_suppression: True,
    CopyOptionsKey.finisher_punch: CopyOptions.CopyPunch.rightTwoPointDin
}

copy_option_combi29 = {
    CopyOptionsKey.sides: CopyOptions.CopySides.one_to_one_sided,
    CopyOptionsKey.color: CopyOptions.Color.grayscale,
    CopyOptionsKey.original_size: CopyOptions.OriginalSize.Letter_8_5x11_in_,
    CopyOptionsKey.number_of_copies: 1,
    CopyOptionsKey.output_scale: CopyOptions.CopyOutputScale.none,
    CopyOptionsKey.paper_size: CopyOptions.CopyPaperSize.letter_8_5x11in,
    CopyOptionsKey.paper_type: CopyOptions.CopyPaperType.plain,
    CopyOptionsKey.paper_tray: CopyOptions.CopyPaperTray.auto,
    CopyOptionsKey.lighter_darker: CopyOptions.CopyLighterDarker.five,
    CopyOptionsKey.content_type: CopyOptions.CopyContentType.mixed,
    CopyOptionsKey.pages_per_sheet: CopyOptions.CopyPagesperSheet.one,
    CopyOptionsKey.collate: True
}

#Copy option settings for combi30
copy_option_combi30 = {
    CopyOptionsKey.sides: CopyOptions.CopySides.one_to_one_sided,
    CopyOptionsKey.color: CopyOptions.Color.automatic,
    CopyOptionsKey.original_size: CopyOptions.OriginalSize.A4_210x297_mm,
    CopyOptionsKey.number_of_copies: 1,
    CopyOptionsKey.output_scale: CopyOptions.CopyOutputScale.fit_to_page,
    CopyOptionsKey.paper_size: CopyOptions.CopyPaperSize.A4_210x297mm,
    CopyOptionsKey.paper_type: CopyOptions.CopyPaperType.plain,
    CopyOptionsKey.lighter_darker: CopyOptions.CopyLighterDarker.five,
    CopyOptionsKey.content_type: CopyOptions.CopyContentType.mixed,
    CopyOptionsKey.pages_per_sheet: CopyOptions.CopyPagesperSheet.four_right_then_down,
    CopyOptionsKey.add_page_border: False,
    CopyOptionsKey.collate: True,
    CopyOptionsKey.blank_page_suppression: False,
}

#Copy option settings for combi31
copy_option_combi31 = {
    CopyOptionsKey.sides: CopyOptions.CopySides.one_to_one_sided,
    CopyOptionsKey.color: CopyOptions.Color.automatic,
    CopyOptionsKey.original_size: CopyOptions.OriginalSize.A4_210x297_mm,
    CopyOptionsKey.number_of_copies: 1,
    CopyOptionsKey.output_scale: CopyOptions.CopyOutputScale.fit_to_page,
    CopyOptionsKey.paper_size: CopyOptions.CopyPaperSize.A4_210x297mm,
    CopyOptionsKey.paper_type: CopyOptions.CopyPaperType.plain,
    CopyOptionsKey.lighter_darker: CopyOptions.CopyLighterDarker.five,
    CopyOptionsKey.content_type: CopyOptions.CopyContentType.mixed,
    CopyOptionsKey.pages_per_sheet: CopyOptions.CopyPagesperSheet.four_down_then_right,
    CopyOptionsKey.add_page_border: False,
    CopyOptionsKey.collate: True,
    CopyOptionsKey.blank_page_suppression: False,
}

#Copy option settings for combi32
copy_option_combi32 = {
    CopyOptionsKey.sides: CopyOptions.CopySides.one_to_one_sided,
    CopyOptionsKey.color: CopyOptions.Color.automatic,
    CopyOptionsKey.original_size: CopyOptions.OriginalSize.A4_210x297_mm,
    CopyOptionsKey.number_of_copies: 1,
    CopyOptionsKey.output_scale: CopyOptions.CopyOutputScale.fit_to_page,
    CopyOptionsKey.paper_size: CopyOptions.CopyPaperSize.A4_210x297mm,
    CopyOptionsKey.paper_type: CopyOptions.CopyPaperType.plain,
    CopyOptionsKey.lighter_darker: CopyOptions.CopyLighterDarker.five,
    CopyOptionsKey.content_type: CopyOptions.CopyContentType.mixed,
    CopyOptionsKey.pages_per_sheet: CopyOptions.CopyPagesperSheet.four_right_then_down,
    CopyOptionsKey.add_page_border: True,
    CopyOptionsKey.collate: True,
    CopyOptionsKey.blank_page_suppression: False,
}

#Copy option settings for combi33
copy_option_combi33 = {
    CopyOptionsKey.sides: CopyOptions.CopySides.one_to_one_sided,
    CopyOptionsKey.color: CopyOptions.Color.color,
    CopyOptionsKey.original_size: CopyOptions.OriginalSize.A4_210x297_mm,
    CopyOptionsKey.number_of_copies: 1,
    CopyOptionsKey.output_scale: CopyOptions.CopyOutputScale.fit_to_page,
    CopyOptionsKey.paper_type: CopyOptions.CopyPaperType.plain,
    CopyOptionsKey.lighter_darker: CopyOptions.CopyLighterDarker.five,
    CopyOptionsKey.content_type: CopyOptions.CopyContentType.mixed,
    CopyOptionsKey.pages_per_sheet: CopyOptions.CopyPagesperSheet.one,
    CopyOptionsKey.collate: True,
    CopyOptionsKey.finisher_fold: CopyOptions.CopyFold.vFold
}

#Copy option settings for combi34
copy_option_combi34 = {
    CopyOptionsKey.color: CopyOptions.Color.automatic,
    CopyOptionsKey.original_size: CopyOptions.OriginalSize.A4_210x297_mm,
    CopyOptionsKey.number_of_copies: 1,
    CopyOptionsKey.output_scale: CopyOptions.CopyOutputScale.fit_to_page,
    CopyOptionsKey.paper_size: CopyOptions.CopyPaperSize.A4_210x297mm,
    CopyOptionsKey.paper_type: CopyOptions.CopyPaperType.plain,
    CopyOptionsKey.lighter_darker: CopyOptions.CopyLighterDarker.five,
    CopyOptionsKey.content_type: CopyOptions.CopyContentType.mixed,
    CopyOptionsKey.booklet_format: True
}

#Copy option settings for combi35
copy_option_combi35 = {
    CopyOptionsKey.color: CopyOptions.Color.automatic,
    CopyOptionsKey.original_size: CopyOptions.OriginalSize.A4_210x297_mm,
    CopyOptionsKey.number_of_copies: 1,
    CopyOptionsKey.output_scale: CopyOptions.CopyOutputScale.fit_to_page,
    CopyOptionsKey.paper_size: CopyOptions.CopyPaperSize.A4_210x297mm,
    CopyOptionsKey.paper_type: CopyOptions.CopyPaperType.plain,
    CopyOptionsKey.lighter_darker: CopyOptions.CopyLighterDarker.five,
    CopyOptionsKey.content_type: CopyOptions.CopyContentType.mixed,
    CopyOptionsKey.booklet_format: True,
    CopyOptionsKey.borders_on_each_page: True
}

#Copy option settings for combi36
copy_option_combi36 = {
    CopyOptionsKey.sides: CopyOptions.CopySides.one_to_one_sided,
    CopyOptionsKey.original_size: CopyOptions.OriginalSize.A4_210x297_mm,
    CopyOptionsKey.number_of_copies: 1,
    CopyOptionsKey.paper_type: CopyOptions.CopyPaperType.plain,
    CopyOptionsKey.lighter_darker: CopyOptions.CopyLighterDarker.five,
    CopyOptionsKey.content_type: CopyOptions.CopyContentType.mixed,
    CopyOptionsKey.pages_per_sheet: CopyOptions.CopyPagesperSheet.one,
}

#Copy option settings for combi37
copy_option_combi37 = {
    CopyOptionsKey.sides: CopyOptions.CopySides.one_to_one_sided,
    CopyOptionsKey.original_size: CopyOptions.OriginalSize.Mixed_Letter_Ledger,
    CopyOptionsKey.number_of_copies: 1,
    CopyOptionsKey.paper_type: CopyOptions.CopyPaperType.plain,
    CopyOptionsKey.lighter_darker: CopyOptions.CopyLighterDarker.five,
    CopyOptionsKey.content_type: CopyOptions.CopyContentType.mixed,
    CopyOptionsKey.pages_per_sheet: CopyOptions.CopyPagesperSheet.one,
    CopyOptionsKey.blank_page_suppression: False,
}

#Copy option settings for combi38
copy_option_combi38 = {
    CopyOptionsKey.sides: CopyOptions.CopySides.one_to_one_sided,
    CopyOptionsKey.original_size: CopyOptions.OriginalSize.Mixed_Letter_Legal,
    CopyOptionsKey.number_of_copies: 1,
    CopyOptionsKey.paper_type: CopyOptions.CopyPaperType.plain,
    CopyOptionsKey.lighter_darker: CopyOptions.CopyLighterDarker.five,
    CopyOptionsKey.content_type: CopyOptions.CopyContentType.mixed,
    CopyOptionsKey.pages_per_sheet: CopyOptions.CopyPagesperSheet.one,
    CopyOptionsKey.blank_page_suppression: False,
}

#Copy option settings for combi39
copy_option_combi39 = {
    CopyOptionsKey.sides: CopyOptions.CopySides.one_to_one_sided,
    CopyOptionsKey.original_size: CopyOptions.OriginalSize.Mixed_A4_A3,
    CopyOptionsKey.number_of_copies: 1,
    CopyOptionsKey.paper_type: CopyOptions.CopyPaperType.plain,
    CopyOptionsKey.lighter_darker: CopyOptions.CopyLighterDarker.five,
    CopyOptionsKey.content_type: CopyOptions.CopyContentType.mixed,
    CopyOptionsKey.pages_per_sheet: CopyOptions.CopyPagesperSheet.one,
    CopyOptionsKey.blank_page_suppression: False,
}

copy_option_list = [
    copy_option_combi1,copy_option_combi2,copy_option_combi3,copy_option_combi4,copy_option_combi5,copy_option_combi6,\
    copy_option_combi7,copy_option_combi8,copy_option_combi9,copy_option_combi10,copy_option_combi11,copy_option_combi12,\
    copy_option_combi13,copy_option_combi14,copy_option_combi15,copy_option_combi16,copy_option_combi17,copy_option_combi18,\
    copy_option_combi19,copy_option_combi20,copy_option_combi21,copy_option_combi22,copy_option_combi23,copy_option_combi24, copy_option_combi25]

# start option set to start_automatically
expected_cdm_for_copy_default = {
	"summary_info": {
		"title": "Auto_Test_Quick_Set_Copy",
		"description": "Just For Auto Test",
		"action": "execute"
	},
	"settings_info": {
		"src": {
			"scan": {
				"colorMode": "autoDetect",
				"mediaSource": "adf",
				"mediaSize": "any",
				"plexMode": "simplex",
				# "resolution": "e300Dpi",
				"contentType": "mixed",
				"contentOrientation": "portrait",
                "pagesFlipUpEnabled": "false"
			}
		},
		"pipelineOptions": {
			"imageModifications": {	
				"exposure": 5,	
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
				"duplexBinding": "oneSided",
				"printQuality": "normal"
			}
		}
	}
}

# start option set to start_automatically
expected_cdm_copy_combi1 = {
    "summary_info": {
        "title": "Auto_Test_Quick_Set_Copy",
        "description": "Just For Auto Test",
        "action": "execute"
    },
    "settings_info": {
        "src": {
            "scan": {
                "colorMode": "autoDetect",
                "mediaSource": "adf",
                "mediaSize": "iso_a3_297x420mm",
                "plexMode": "simplex",
                # "resolution": "e300Dpi",
                "contentType": "mixed",
                "contentOrientation": "portrait",
                "pagesFlipUpEnabled": "false"
            }
        },
        "pipelineOptions": {
            "imageModifications": {
                "exposure": 6,
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
                "mediaSize": "iso_a4_210x297mm",
                "mediaType": "any",
                "plexMode": "duplex",
                "duplexBinding": "twoSidedLongEdge",
                "printQuality": "normal"
            }
        }
    }
}

# todo: Add expected cdm for combi2
expected_cdm_copy_combi2 = {
	"summary_info": {
		"title": "Auto_Test_Quick_Set_Copy",
		"description": "Just For Auto Test",
		"action": "open"
	},
	"settings_info": {
		"src": {
			"scan": {
				"colorMode": "grayscale",
				"mediaSource": "adf",
				"mediaSize": "any",
				"plexMode": "duplex",
				# "resolution": "e300Dpi",
				"contentType": "photo",
				"contentOrientation": "portrait",
                "pagesFlipUpEnabled": "false"
			}
		},
		"pipelineOptions": {
			"imageModifications": {
				"exposure": 9,
			},
			"scaling": {
				"scaleToFitEnabled": "true",
				"xScalePercent": 100,
				"yScalePercent": 100,
				"scaleSelection": "fitToPage"
			}
		},
		"dest": {
			"print": {
				"collate": "uncollated",
				"copies": 5,
				"mediaSource": "tray-2",
				"mediaSize": "custom",
				"mediaType": "stationery",
				"plexMode": "simplex",
				"duplexBinding": "oneSided",
				"printQuality": "normal"
			}
		}
	}
}

def expected_cdm_copy_combi2_from_actual_cdm(ews):
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
        "summary_info": {
            "title": "Auto_Test_Quick_Set_Copy",
            "description": "Just For Auto Test",
            "action": "open"
        },
        "settings_info": { 
            "src": {
                "scan": {
                    "colorMode": scan_setting["colorMode"],
				    "mediaSource": "adf",
				    "mediaSize": "any",
				    "plexMode": "duplex",
				    "contentType": "photo",
				    "contentOrientation": "portrait",
                    "pagesFlipUpEnabled": "false"
                }
            },
            "pipelineOptions": {
                "imageModifications": {
                    "exposure": 9
                },
                "scaling": {
				    "scaleToFitEnabled": "true",
				    "xScalePercent": 100,
				    "yScalePercent": 100,
				    "scaleSelection": "fitToPage"
                }
            },
            "dest": {
                "print": {
                    "collate": "uncollated",
				    "copies": 5,
				    "mediaSource": "auto",
				    "mediaSize": "custom",
				    "mediaType": "stationery",
				    "plexMode": "simplex",
				    "duplexBinding": "oneSided",
				    "printQuality": "normal"
                }
            }
        }
    }

    return validated_settings

def expected_cdm_copy_combi_standard_doc_add_pages_from_actual_cdm(ews):
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
        "summary_info": {
            "title": "Auto_Test_Quick_Set_Copy",
            "description": "Just For Auto Test",
            "action": "open"
        },
        "settings_info": {
            "src": {
                "scan": {
                    "colorMode": scan_setting["colorMode"],
				    "mediaSource": "adf",
				    "mediaSize": "any",
				    "plexMode": "duplex",
				    "contentType": "photo",
				    "contentOrientation": "portrait",
                    "pagesFlipUpEnabled": "false",
                    "scanCaptureMode": "standard"
                }
            },
            "pipelineOptions": {
                "imageModifications": {
                    "exposure": 9
                },
                "scaling": {
				    "scaleToFitEnabled": "true",
				    "xScalePercent": 100,
				    "yScalePercent": 100,
				    "scaleSelection": "fitToPage"
                },
                "promptForAdditionalPages": "true"
            },
            "dest": {
                "print": {
                    "collate": "uncollated",
				    "copies": 5,
				    "mediaSource": "auto",
				    "mediaSize": "custom",
				    "mediaType": "stationery",
				    "plexMode": "simplex",
				    "duplexBinding": "oneSided",
				    "printQuality": "normal"
                }
            }
        }
    }

    return validated_settings

expected_cdm_copy_combi3 = {
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
				"plexMode": "duplex",
				# "resolution": "e300Dpi",
				"contentType": "text",
				"contentOrientation": "portrait",
                "pagesFlipUpEnabled": "false"
			}
		},
		"pipelineOptions": {
			"imageModifications": {
				"exposure": 3,
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
				"copies": 99,
				"mediaSource": "tray-1",
				"mediaSize": "na_letter_8.5x11in",
				"mediaType": "stationery",
				"plexMode": "duplex",
				"duplexBinding": "twoSidedLongEdge",
				"printQuality": "normal"
			}
		}
	}
}


def expected_cdm_copy_combi3_from_actual_cdm(ews):
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
                    "mediaSize": "na_letter_8.5x11in",
                    "plexMode": "duplex",
                    # "resolution": scan_setting["resolution"],
                    "contentType": "text",
                    "contentOrientation": scan_setting["contentOrientation"],
                    "pagesFlipUpEnabled": scan_setting["pagesFlipUpEnabled"]
                }
            },
            "pipelineOptions": {
                "imageModifications": {
                    "exposure": 3
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
                    "collate": "uncollated",
                    "copies": 99,
                    "mediaSource": "tray-1",
                    "mediaSize": "na_letter_8.5x11in",
                    "mediaType": print_setting["mediaType"],
                    "plexMode": "duplex",
                    "duplexBinding": "twoSidedLongEdge",
                    "printQuality": "normal"
                }
            }
        }
    }

    return validated_settings

