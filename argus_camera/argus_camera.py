from typing import Optional, Tuple

import numpy as np

from .cpp import *


class ArgusCamera:
    """
    Argus Camera Python wrapper.
    """

    def __init__(
            self,
            device_id=0,
            stream_resolution=(640, 480),
            video_converter_resolution=(640, 480),
            frame_duration_range=(int(1e9//30), int(1e9//30)),
            exposure_time_range=(int(0), int(999999999)),
            source_clip_rect=(0.0, 0.0, 1.0, 1.0),
            gain_range=(0., 300.),
            ae_regions=None,
            sensor_mode=0):

        self.device_id = device_id

        self.video_converter_resolution = video_converter_resolution

        self.config = DEFAULT_DEVKIT_CONFIG()
        self.config.setDeviceId(device_id)
        self.config.setStreamResolution(stream_resolution)
        self.config.setVideoConverterResolution(video_converter_resolution)
        self.config.setFrameDurationRange(frame_duration_range)
        self.config.setExposureTimeRange(exposure_time_range)
        self.config.setGainRange(gain_range)
        self.config.setSourceClipRect(source_clip_rect)
        self.config.setExposureCompensation(0)
        self.config.setAeLock(False)
        self.config.setSensorMode(sensor_mode)
        if ae_regions is not None:
            aer_arr = np.asarray(ae_regions, dtype=np.float32)
            aer_s = aer_arr.shape
            if not (len(aer_s) == 2 and aer_s[0] and aer_s[1] == 5):
                raise ValueError("ae_regions value error")
            self.config.setAeRegions(aer_arr.tolist())
        self.channels = 4

        ret = IArgusCamera_createArgusCamera(self.config)
        if isinstance(ret, tuple):
            self.camera, self.camera_error_code = ret
        elif isinstance(ret, int):
            self.camera = None
            self.camera_error_code = ret
        else:
            raise NotImplementedError

        self.read_error_code = -1

    def isOpened(self) -> bool:
        """
        Return the initialization status of the camera.

        RETURN
        ------
        bool
            If true, the camera successfully initialized.
        """
        return not self.camera_error_code

    def read(self) -> Tuple[bool, Optional[np.ndarray]]:
        """
        Read frame from camera.

        RETURN
        -------
        Tuple[bool, Optional[np.ndarray]]
            bool
                Status of the result of read call.
                If failed, the error code could be obtained
                from ``read_error_code`` attribute.
            Optional[np.ndarray]
                If read call success, return Numpy array
                containing the frame from camera.
                Otherwise, return None.
        """
        image = np.empty(
            list(self.video_converter_resolution)[::-1] + [self.channels],
            np.uint8)
        self.read_error_code = self.camera.read(image.ctypes.data)
        if not self.read_error_code:
            return True, image[:, :, :3]
        return False, None

    def getMaxAeRegions(self) -> int:
        """
        RETURN
        ------
        int
            Returns the maximum number of regions of interest
            supported by AE. A value of 0 means that the entire
            image is the only supported region of interest.
        """
        return self.camera.getMaxAeRegions()

    def getMinAeRegionSize(self) -> Tuple[int, int]:
        """
        RETURN
        ------
        Tuple[int, int]
            Returns the minimum size (width, height) of resultant
            region required by AE.
        """
        return self.camera.getMinAeRegionSize()
