import cv2
import numpy

CANS_PIC_PATH = "cans.jpeg"

def count_cans():
    # read image
    cans_image = cv2.imread(CANS_PIC_PATH)

    # convert to grayscale
    grayscale_cans_image = cv2.cvtColor(cans_image, cv2.COLOR_BGR2GRAY)

    # apply gaussian blur
    blurred_cans_image = cv2.GaussianBlur(grayscale_cans_image, (5, 5), 0)

    # detect cans
    cans = cv2.HoughCircles(
            blurred_cans_image,
            cv2.HOUGH_GRADIENT,
            dp=1,
            minDist=280,  # Minimum distance between circles
            param1=10,   # Upper threshold for edge detection
            param2=30,   # Threshold for center detection
            minRadius=280,  # Minimum radius of the circle
            maxRadius=290  # Maximum radius of the circle
        )

    if cans is not None:
        # count detected cans
        circles = numpy.uint16(numpy.around(cans))
        count = len(circles[0])

        # mark detected cans on image
        for i in circles[0, :]:
            cv2.circle(cans_image, (i[0], i[1]), i[2], (0, 255, 0), 2)
            cv2.circle(cans_image, (i[0], i[1]), 2, (0, 0, 255), 3)

        # save image with detected cans
        cv2.imwrite("detected_cans.jpeg", cans_image)

    else:
        count = -1

    # return result
    cv2.destroyAllWindows()
    return count




if __name__ == "__main__":
    cans_count = count_cans()
    if(cans_count == -1):
        cans_count = 'none'
    print(f"cans found: {cans_count}")
