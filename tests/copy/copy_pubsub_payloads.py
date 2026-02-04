import json
from dunetuf.cdm.CdmEndpoints import CdmEndpoints
 
custom_copy_configuration_payload = {
  "version": "1.1.0-alpha.6",
  "ticketId": "840e9486-7565-4b4c-bd27-58a7c00c9eee",
  "links": [
    {
      "href": CdmEndpoints.JOB_TICKET_COPY,
      "rel": "self"
    },
    {
      "href": CdmEndpoints.JOB_TICKET_COPY_CONSTRAINTS,
      "rel": "constraints"
    }
  ],
  "src": {
    "scan": {
      "colorMode": "color",
      "mediaSource": "adf",
      "mediaSize": "na_legal_8.5x14in",
      "xOffset": 0,
      "yOffset": 0,
      "plexMode": "simplex",
      "resolution": "e300Dpi",
      "contentType": "mixed",
      "contentOrientation": "portrait",
      "pagesFlipUpEnabled": "true",
      "autoColorDetect": "detectOnly",
      "blackBackground": "false",
      "mediaType": "whitePaper",
      "autoExposure": "false",
      "gamma": 1,
      "highlight": 1,
      "colorSensitivity": 0,
      "colorRange": 0,
      "ccdChannel": "grayCcdEmulated",
      "binaryRendering": "halftone",
      "descreen": "false",
      "feederPickStop": "false",
      "shadow": 1,
      "compressionFactor": 0,
      "threshold": 0,
      "scanCaptureMode": "standard",
      "scanAcquisitionsSpeed": "auto",
      "autoDeskew": "false"
    }
  },
  "pipelineOptions": {
    "imageModifications": {
      "sharpness": 2,
      "backgroundCleanup": 2,
      "exposure": 5,
      "contrast": 1,
      "blankPageSuppressionEnabled": "false",
      "pagesPerSheet": "oneUp"
    },
    "manualUserOperations": {
      "imagePreviewConfiguration": "disable",
      "autoRelease": "false"
    },
    "scaling": {
      "scaleToFitEnabled": "false",
      "xScalePercent": 100,
      "yScalePercent": 100,
      "scaleSelection": "fitToPage"
    },
    "generatePreview": "false"
  },
  "dest": {
    "print": {
      "collate": "collated",
      "copies": 1,
      "mediaSource": "auto",
      "mediaSize": "na_legal_8.5x14in",
      "mediaType": "stationery",
      "plexMode": "duplex",
      "duplexBinding": "twoSidedLongEdge",
      "printQuality": "normal"
    }
  }
}
