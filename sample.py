import cv2
from argus_camera import ArgusCamera


def main():
    camera = ArgusCamera()

    while True:
        image = camera.read()
        bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        cv2.imshow("camera", bgr)
        k = cv2.waitKey(1)
        if k & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            print("Exiting...")
            break


if __name__ == "__main__":
    main()
