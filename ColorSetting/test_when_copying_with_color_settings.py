import logging
import sys
from dunetuf.emulation.scan import ScanEmulation
from tests.copy.copy_base import TestGivenEmptyQueueAndEmptyHistory
from tests.copy.copy_utils import create_and_start_copy_job


class TestWhenCopyingWithColorSettings(TestGivenEmptyQueueAndEmptyHistory):
    """
    Tests for copy functionality with different color mode settings (color, grayscale, autoDetect).
    
    Tests verify copy jobs from both ADF and flatbed with various color modes and duplex settings.
    """
    
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
        super().setup_class()
        scan_simulator_ip = sys.argv[sys.argv.index('scanSimulatorIP') + 1] if 'scanSimulatorIP' in sys.argv else None
        scan_simulator_ip = None if scan_simulator_ip == 'None' else scan_simulator_ip
        logging.info('Instantiating ScanEmulation with %s', scan_simulator_ip)
        cls.scan_emulation = ScanEmulation(cls.cdm, cls.udw, cls.tcl, scan_simulator_ip)

    @classmethod
    def teardown_class(cls):
        """Clean up shared test resources."""
        super().teardown_class()

    def setup_method(self):
        """Set up base payload for each test."""
        self.base_payload = {
            'src': {
                'scan': {
                    'colorMode': 'color',
                    'mediaSize': 'na_letter_8.5x11in',
                    'plexMode': 'simplex',
                    'resolution': 'e300Dpi',
                },
            },
            'dest': {
                'print': {
                    'copies': 1,
                    'mediaSize': 'na_letter_8.5x11in',
                    'plexMode': 'simplex',
                }
            }
        }

    def teardown_method(self):
        """Clean up resources after each test."""
        # Clear job queue
        self.job_queue.cancel_all_jobs()
        self.job_queue.wait_for_queue_empty()

        # Clear job history
        self.job_history.clear()
        self.job_history.wait_for_history_empty()

        # Restore default ticket
        response = self.update_default_ticket_if_required(self.default_ticket)
        assert response == 200

        # Reset scan pages to default
        self.udw.mainApp.ScanDeviceService.setNumScanPages(1)

    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose: color multiple page copy from ADF
        +test_tier: 1
        +is_manual: False
        +test_classification:System
        +reqid: DUNE-17182
        +timeout:120
        +asset: Copy
        +delivery_team:WalkupApps
        +feature_team:CopySolns
        +test_framework: TUF
        +name: TestWhenCopyingWithColorSettings::test_when_copying_color_from_adf_with_duplex_then_succeeds
        +categorization:
            +segment:Platform
            +area:Copy
            +feature:CopySettings
            +sub_feature:
            +interaction:Headless
            +test_type:Positive
        +test:
            +title: TestWhenCopyingWithColorSettings::test_when_copying_color_from_adf_with_duplex_then_succeeds
            +guid:d4a7f8b2-3c1e-4d9a-b5e6-7f8a9b0c1d2e
            +dut:
                +type: Simulator
                +configuration:DeviceClass=MFP & DeviceFunction=CopyColor & ScannerInput=AutomaticDocumentFeeder
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    # Original test: test_copy_color_adf_duplex_using_cdm (GUID: 99a86138-cc6c-493b-896b-75c7c575491e)
    def test_when_copying_color_from_adf_with_duplex_then_succeeds(self):
        """Test color copy from ADF with duplex output."""
        self.scan_emulation.media.load_media('ADF', 5)
        self.base_payload['dest']['print']['plexMode'] = 'duplex'
        
        job_id = create_and_start_copy_job(self.copy, self.base_payload)
        self.copy.wait_for_state(job_id, ["completed"])

    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose: grayscale single page copy from flatbed
        +test_tier: 1
        +is_manual: False
        +test_classification:System
        +reqid: DUNE-17182
        +timeout:200
        +asset: Copy
        +delivery_team:WalkupApps
        +feature_team:CopySolns
        +test_framework: TUF
        +name: TestWhenCopyingWithColorSettings::test_when_copying_grayscale_from_flatbed_with_simplex_then_succeeds
        +categorization:
            +segment:Platform
            +area:Copy
            +feature:CopySettings
            +sub_feature:
            +interaction:Headless
            +test_type:Positive
        +test:
            +title: TestWhenCopyingWithColorSettings::test_when_copying_grayscale_from_flatbed_with_simplex_then_succeeds
            +guid:3e9f2b5c-4d8a-4f1b-a6c7-8d9e0f1a2b3c
            +dut:
                +type: Simulator
                +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & Copy=GrayScale

        +overrides:
            +Enterprise:
                +is_manual:False
                +timeout:600
                +test:
                    +dut:
                        +type:Emulator
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    # Original test: test_copy_grayscale_flatbed_simplex_using_cdm (GUID: 804d0d6d-52f8-4f4a-a149-a3f78585327f)
    def test_when_copying_grayscale_from_flatbed_with_simplex_then_succeeds(self):
        """Test grayscale copy from flatbed with simplex output."""
        self.udw.mainApp.ScanDeviceService.setNumScanPages(1)
        self.base_payload['src']['scan']['colorMode'] = 'grayscale'
        self.base_payload['dest']['print']['plexMode'] = 'simplex'
        
        job_id = create_and_start_copy_job(self.copy, self.base_payload)
        self.copy.wait_for_state(job_id, ["completed"], timeout=90)

    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose: grayscale multiple page copy from ADF
        +test_tier: 1
        +is_manual: False
        +test_classification:System
        +reqid: DUNE-17182
        +timeout:120
        +asset: Copy
        +delivery_team:WalkupApps
        +feature_team:CopySolns
        +test_framework: TUF
        +name: TestWhenCopyingWithColorSettings::test_when_copying_grayscale_from_adf_with_duplex_then_succeeds
        +categorization:
            +segment:Platform
            +area:Copy
            +feature:CopySettings
            +sub_feature:
            +interaction:Headless
            +test_type:Positive
        +test:
            +title: TestWhenCopyingWithColorSettings::test_when_copying_grayscale_from_adf_with_duplex_then_succeeds
            +guid:5f1a3c6d-7e2b-4a8c-9d0e-1f2a3b4c5d6e
            +dut:
                +type: Simulator
                +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & Copy=GrayScale

        +overrides:
            +Enterprise:
                +is_manual:False
                +timeout:600
                +test:
                    +dut:
                        +type:Emulator
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    # Original test: test_copy_grayscale_adf_duplex_using_cdm (GUID: 9e7a95d6-cc88-4410-8f79-38218fcfadf6)
    def test_when_copying_grayscale_from_adf_with_duplex_then_succeeds(self):
        """Test grayscale copy from ADF with duplex output."""
        self.scan_emulation.media.load_media('ADF', 5)
        self.base_payload['src']['scan']['colorMode'] = 'grayscale'
        self.base_payload['dest']['print']['plexMode'] = 'duplex'
        
        job_id = create_and_start_copy_job(self.copy, self.base_payload)
        self.copy.wait_for_state(job_id, ["completed"])

    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose:Auto color mode single page copy from flatbed
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-99493
        +timeout:600
        +asset:Copy
        +delivery_team:WalkupApps
        +feature_team:CopySolns
        +test_framework:TUF
        +test_classification:System
        +name:TestWhenCopyingWithColorSettings::test_when_copying_autodetect_from_flatbed_with_simplex_then_succeeds
        +categorization:
            +segment:Platform
            +area:Copy
            +feature:CopySettings
            +sub_feature:
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:TestWhenCopyingWithColorSettings::test_when_copying_autodetect_from_flatbed_with_simplex_then_succeeds
            +guid:6a2b4d7e-8f3c-4b9d-a0e1-2f3a4b5c6d7e
            +dut:
                +type:Simulator
                +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScanColorMode=Automatic & Copy=Color
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    # Original test: test_copy_color_autodetect_flatbed_simplex_using_cdm (GUID: 4c6812a7-bee6-428f-ad6b-3fdeb777e6d8)
    def test_when_copying_autodetect_from_flatbed_with_simplex_then_succeeds(self):
        """Test auto color detection copy from flatbed with simplex output."""
        self.udw.mainApp.ScanDeviceService.setNumScanPages(1)
        if self.cdm.device_feature_cdm.is_color_supported():
            self.base_payload['src']['scan']['colorMode'] = 'autoDetect'
        self.base_payload['dest']['print']['plexMode'] = 'simplex'
        
        job_id = create_and_start_copy_job(self.copy, self.base_payload)
        self.copy.wait_for_state(job_id, ["completed"])

    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose:color mode autodetect multiple page copy from ADF
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-99493
        +timeout:600
        +asset:Copy
        +delivery_team:WalkupApps
        +feature_team:CopySolns
        +test_framework:TUF
        +test_classification:System
        +name:TestWhenCopyingWithColorSettings::test_when_copying_autodetect_from_adf_with_duplex_then_succeeds
        +categorization:
            +segment:Platform
            +area:Copy
            +feature:CopySettings
            +sub_feature:
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:TestWhenCopyingWithColorSettings::test_when_copying_autodetect_from_adf_with_duplex_then_succeeds
            +guid:7b3c5e8f-9g4d-4c0e-b1f2-3g4a5b6c7d8e
            +dut:
                +type:Simulator
                +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScanColorMode=Automatic & Copy=Color
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    # Original test: test_copy_color_autodetect_adf_duplex_using_cdm (GUID: 9b74f4ac-4739-4636-84c9-5918b493a0f4)
    def test_when_copying_autodetect_from_adf_with_duplex_then_succeeds(self):
        """Test auto color detection copy from ADF with duplex output."""
        self.scan_emulation.media.load_media('ADF', 3)
        if self.cdm.device_feature_cdm.is_color_supported():
            self.base_payload['src']['scan']['colorMode'] = 'autoDetect'
        self.base_payload['dest']['print']['plexMode'] = 'duplex'
        
        job_id = create_and_start_copy_job(self.copy, self.base_payload)
        self.copy.wait_for_state(job_id, ["completed"])

    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose: color single page copy from flatbed
        +test_tier: 1
        +is_manual: False
        +test_classification:System
        +reqid: DUNE-17182
        +timeout:120
        +asset: Copy
        +delivery_team:WalkupApps
        +feature_team:CopySolns
        +test_framework: TUF
        +name: TestWhenCopyingWithColorSettings::test_when_copying_color_from_flatbed_with_simplex_then_succeeds
        +categorization:
            +segment:Platform
            +area:Copy
            +feature:CopySettings
            +sub_feature:
            +interaction:Headless
            +test_type:Positive
        +test:
            +title: TestWhenCopyingWithColorSettings::test_when_copying_color_from_flatbed_with_simplex_then_succeeds
            +guid:8c4d6f9g-0h5e-4d1f-c2g3-4h5a6b7c8d9e
            +dut:
                +type: Simulator
                +configuration:DeviceClass=MFP & DeviceFunction=CopyColor & ScannerInput=Flatbed

        +overrides:
            +Enterprise:
                +is_manual:False
                +timeout:600
                +test:
                    +dut:
                        +type:Emulator
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    # Original test: test_copy_color_flatbed_simplex_using_cdm (GUID: eb6ccea8-d928-4b2d-a01a-0c9577ec6c83)
    def test_when_copying_color_from_flatbed_with_simplex_then_succeeds(self):
        """Test color copy from flatbed with simplex output."""
        job_id = self.copy.do_copy_job(adfLoaded=False, **self.base_payload)
        self.copy.wait_for_state(job_id, ["completed"])
