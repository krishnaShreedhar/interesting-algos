from opencv_circle_detection.detectors import CircleDetector
import utils.files as uf


def circle_detection():
    cd = CircleDetector(hc_min_radius=100, hc_max_radius=500)
    list_file_paths = uf.get_all_files_glob("../data/examples_circle_detection/", ["jpg"])
    for index, file_path in enumerate(list_file_paths):
        cd.detect_circles(file_path)


def main():
    circle_detection()


if __name__ == '__main__':
    main()
