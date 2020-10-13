from argus_camera import ArgusCamera

def get_camera():
    return ArgusCamera(
        device_id=0,
        stream_resolution=(1640, 1232),
        video_converter_resolution=(1280, 800),
        frame_duration_range=(int(1e9//15), int(1e9//15)),
        exposure_time_range=(0, 9999999999999),
        source_clip_rect=(0., 0., 1., 1.),
        gain_range=(0., 300.),
        ae_regions=[[0, 0, 300, 300, 1.0]],
        sensor_mode=0
    )

def main():
    camera = get_camera()
    if not camera.isOpened():
        raise RuntimeError(
            "Failed initializing camera! (code: %d)" % camera.camera_error_code)

    while True:
        ret, image = camera.read()
        if not ret:
            print(
                "Failed reading frame from camera! (code: %d)" %
                camera.read_error_code)
            continue
        print(image.shape)


if __name__ == "__main__":
    main()