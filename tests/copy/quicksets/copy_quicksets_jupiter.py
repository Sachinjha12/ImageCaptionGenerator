###############################################################################
#  @file   copy_quicksets_jupiter
#  @author Manuel Jimenez Vieites (manuel.jimenez.vieites@hp.com)
#  @date   31-08-2022
#  @brief  Python implementation of copyquicksets for jupiter.
#
#  (c) Copyright HP Inc. 2022. All rights reserved.
###############################################################################
from enum import Enum
from dunetuf.cdm.CdmEndpoints import CdmEndpoints


class COPYquicksets:
    """
    Class containing methods to manage current and 
    expected copy shortcuts and quickset data
    
    Args: no args
        
    """
    class Title(str, Enum):
        BLUEPRINT = 'Blueprint'
        BLUEPRINT_RED_STAMP = 'Blueprint With Red Stamp'
        MIXED = 'Mixed Content'
        COLOR = 'Color Lines'
        GRAYSCALE = 'Grayscale Lines'
        IMAGE = 'Image'

    class ColorMode(str, Enum):
        COLOR = 'color'
        GRAYSCALE = 'grayscale'

    class PrintQuality(str, Enum):
        BEST = 'best'
        STANDARD = 'normal'
        DRAFT = 'draft'
    
    class ContentType(str, Enum):
        LINEDRAWING = 'lineDrawing'
        MIXED = 'mixed'
        IMAGE = 'image'

    class MediaSource(str, Enum):
        AUTOMATIC = 'auto'
    
    class BackgroundColorRemoval(str, Enum):
        TRUE = 'true'
        FALSE = 'false'

    class Collate(str, Enum):
        COLLATED = 'collated'
        UNCOLLATED = 'uncollated'

    def build_relevant_ticket(self, id, colorMode, printQuality, contentType, mediaSource, backgroundColorRemoval, blackEnhancementLevel, copies, collate):
        """
        Build a dictionaty with relevant ticket data
        @params : Relevant data to build a ticket related to a shortcut
        @return : dictionary with the data ticket
        """
        ticket = { 
                    'id': id,
                    'colorMode': colorMode,
                    'printQuality' : printQuality,
                    'contentType': contentType,
                    'mediaSource' : mediaSource,
                    'backgroundColorRemoval' : backgroundColorRemoval,
                    'blackEnhancementLevel' : blackEnhancementLevel,
                    'copies' : copies,
                    'collate' : collate
                 }
        return ticket

    def add_shortcut(self, title, id, colorMode, printQuality, contentType, mediaSource, backgroundColorRemoval, collate, blackEnhancementLevel, copies):
        """
        Build a shortcut with title and ticket data and add  it to reference shortcuts dictionary (expected)
        @params : shortcut title and , relevant data to build a ticket
        """
        new_ticket_relevant_data = self.build_relevant_ticket(
            id,
            colorMode,
            printQuality,
            contentType,
            mediaSource,
            backgroundColorRemoval,
            blackEnhancementLevel,
            copies,
            collate
        )
        self.shortcuts_expected_data[title]= new_ticket_relevant_data

    def get_shortcut_ticket(self, cdm, net, shortcut):
        """
        Get ticket related to a shortcut
        @params : cdm, net fixtures
        @params : shortcut from where obtain the ticket (id)
        @return : ticket (raw data)
        """
        # Ticket endpoint link in ticket -> links (0) -> href
        endpoint_ticket_cdm = shortcut['links'][0]['href']
        # Remove chars '{' and '}' from endpoint
        endpoint_ticket_cdm_formated = endpoint_ticket_cdm.replace('{', '').replace('}', '')
        ticket_raw_data = cdm.get(endpoint_ticket_cdm_formated)
        return ticket_raw_data

    def extract_ticket_relevant_data(self, shortcut_id, ticket_full_data, cp_qsets):
        """
        Extract relevant data from ticket raw data
        @params : id of the shortcut, full ticket data (raw)
        @params : copy_quicksets instance
        @return : ticket relevant data only
        """
        # ticket -> src -> scan -> colorMode
        colorMode = ticket_full_data['src']['scan']['colorMode']
        
        # ticket -> dest -> print -> printQuality
        printQuality = ticket_full_data['dest']['print']['printQuality']
        
        # ticket -> src -> scan -> contentType
        contentType = ticket_full_data['src']['scan']['contentType']
        
        # ticket -> dest -> print -> mediaSource
        mediaSource = ticket_full_data['dest']['print']['mediaSource']
        
        # ticket -> pipelineOptions-> imageModifications -> backgroundColorRemoval
        backgroundColorRemoval = ticket_full_data['pipelineOptions']['imageModifications']['backgroundColorRemoval']
        
        # ticket -> pipelineOptions-> imageModifications -> blackEnhacementLevel
        backgroundColorRemovalLevel = str(ticket_full_data['pipelineOptions']['imageModifications']['blackEnhancementLevel'])
        
        # ticket -> dest -> print -> collate
        collate = ticket_full_data['dest']['print']['collate']
        
        # ticket -> dest -> print -> copies
        copies = str(ticket_full_data['dest']['print']['copies'])

        new_ticket_relevant_data = cp_qsets.build_relevant_ticket(
            shortcut_id,
            colorMode,
            printQuality,
            contentType,
            mediaSource,
            backgroundColorRemoval,
            backgroundColorRemovalLevel,
            copies,
            collate
        )
        return new_ticket_relevant_data
        
    def clone_ticket(self, cdm, ticketId):
        """
        Clone a ticket
        @params : ticket id to clone
        @params : id of the ticket
        @return : cloned ticket
        """
        uri = CdmEndpoints.JOB_TICKET_ENDPOINT
        reqPayload = {"ticketReference" : "user/ticket/" + ticketId}
        new_ticket_user_response = cdm.post_raw(uri, reqPayload)
        
        # Check that we cloned the ticket successfully
        assert new_ticket_user_response.status_code == 201
        return new_ticket_user_response.json()

    def __init__(self):
        # Build expected shortcuts dictionary (with expected ticket data)
        self.shortcuts_expected_data={}
        self.add_shortcut(
            self.Title.BLUEPRINT,
            "eba1f540-239d-11ed-83d5-0b139473ea60",
            self.ColorMode.GRAYSCALE,
            self.PrintQuality.DRAFT,
            self.ContentType.LINEDRAWING,
            self.MediaSource.AUTOMATIC,
            self.BackgroundColorRemoval.TRUE,
            self.Collate.COLLATED,
            blackEnhancementLevel="60",
            copies="1"
        )

        self.add_shortcut(
            self.Title.MIXED,
            "61b72f38-1945-11ed-bf29-87d40f139a32",
            self.ColorMode.COLOR,
            self.PrintQuality.DRAFT,
            self.ContentType.MIXED,
            self.MediaSource.AUTOMATIC,
            self.BackgroundColorRemoval.FALSE,
            self.Collate.COLLATED,
            blackEnhancementLevel="60",
            copies="1"
        )

        self.add_shortcut(
            self.Title.COLOR,
            "34cc69d4-194f-11ed-89dc-4be3ffadc2eb",
            self.ColorMode.COLOR,
            self.PrintQuality.DRAFT,
            self.ContentType.LINEDRAWING,
            self.MediaSource.AUTOMATIC,
            self.BackgroundColorRemoval.FALSE,
            self.Collate.COLLATED,
            blackEnhancementLevel="60",
            copies="1"
        )

        self.add_shortcut(
            self.Title.GRAYSCALE,
            "ccf3c448-250a-11ed-851e-d37653ac82ab",
            self.ColorMode.GRAYSCALE,
            self.PrintQuality.DRAFT,
            self.ContentType.LINEDRAWING,
            self.MediaSource.AUTOMATIC,
            self.BackgroundColorRemoval.TRUE,
            self.Collate.COLLATED,
            blackEnhancementLevel="60",
            copies="1"
        )

        self.add_shortcut(
            self.Title.IMAGE,
            "dba2ec94-250a-11ed-b62b-eb3183c3f17f",
            self.ColorMode.COLOR,
            self.PrintQuality.STANDARD,
            self.ContentType.IMAGE,
            self.MediaSource.AUTOMATIC,
            self.BackgroundColorRemoval.FALSE,
            self.Collate.COLLATED,
            blackEnhancementLevel="0",
            copies="1"
        )

        self.add_shortcut(
            self.Title.BLUEPRINT_RED_STAMP,
            "c2306e7e-c4b7-11ed-a0a1-8776890b7239",
            self.ColorMode.COLOR,
            self.PrintQuality.DRAFT,
            self.ContentType.LINEDRAWING,
            self.MediaSource.AUTOMATIC,
            self.BackgroundColorRemoval.TRUE,
            self.Collate.COLLATED,
            blackEnhancementLevel="60",
            copies="1"
        )

    def get_expected_copy_shortcuts_quicksets(self):
        """
        Return expected shortcut dictionary with ticket expected data inside
        @params : 
        @params : 
        @return : Expected shortcut dict with ticket expected data inside
        """
        return self.shortcuts_expected_data

        