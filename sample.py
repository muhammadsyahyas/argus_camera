import cv2

from argus_camera import ArgusCamera


def main():
    camera = ArgusCamera(
        stream_resolution=(1640, 1232),
        video_converter_resolution=(640, 400))
    if not camera.isOpened():
        raise RuntimeError("Failed initializing camera! (code: %d)" % camera.camera_error_code)
    print("MaxAeRegions:", camera.getMaxAeRegions())
    print("MinAeRegionSize:", camera.getMinAeRegionSize())

    while True:
        ret, image = camera.read()
        if not ret:
            print("Failed reading frame from camera! (code: %d)" % camera.read_error_code)
            continue
        bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        cv2.imshow("camera", bgr)
        k = cv2.waitKey(1)
        if k & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            print("Exiting...")
            break


if __name__ == "__main__":
    main()
