import cv2
from bresenham import bresenham
import numpy as np
import matplotlib.pyplot as plt
import os


def analyze(filename, p1, p2, imageName=None, show=True):
    """
    Pass in a filename, and two tuples containing xy
    coordinates
    """
    outputDirName = "Output"
    if not os.path.exists(outputDirName):
        os.mkdir(outputDirName)

    if imageName is None:
        imageName = filename.split("/")[-1].split(".")[0]

    imageDirName = "./" + outputDirName + "/" + imageName + "/"

    if not os.path.exists(imageDirName):
        os.mkdir(imageDirName)

    image = cv2.imread(filename)
    saveAndPlotImageData(image, p1, p2, imageDirName)
    saveRGBChannelGreyscaleImages(image, p1, p2, imageDirName)


def saveAndPlotImageData(image, p1, p2, imageDirName, show=True):
    """
    Saves and plots the RGB channel outputs for the image.
    """
    # Get the points on the line
    points = bresenham(p1[0], p1[1], p2[0], p2[1])
    redPoints = []
    greenPoints = []
    bluePoints = []
    for x, y in points:
        blue, green, red = image[y][x]
        redPoints.append(red)
        bluePoints.append(blue)
        greenPoints.append(green)

    redPoints = np.array(redPoints)
    bluePoints = np.array(bluePoints)
    greenPoints = np.array(greenPoints)
    avgPoints = (redPoints + bluePoints + greenPoints)/3
    pixelDistances = np.arange(0, len(redPoints))

    # Save in to matriax. Serialize into CSV for later analysis
    combined = np.zeros((len(redPoints), 5))
    combined[:, 0] = pixelDistances
    combined[:, 1] = redPoints
    combined[:, 2] = greenPoints
    combined[:, 3] = bluePoints
    combined[:, 4] = avgPoints

    np.savetxt(imageDirName + 'RGB_Channels.csv',
               combined,
               delimiter=",")

    # Plot the data and analyse it
    fig1 = plt.figure(figsize=(9, 6.5))
    ax1 = fig1.add_subplot(221)
    ax2 = fig1.add_subplot(222)
    ax3 = fig1.add_subplot(223)
    ax4 = fig1.add_subplot(224)

    ax1.plot(pixelDistances, redPoints, 'r')
    ax1.set_xlabel("Distance [pixels]")
    ax1.set_ylabel("Red Channel Intensity")

    ax2.plot(pixelDistances, greenPoints, 'g')
    ax2.set_xlabel("Distance [pixels]")
    ax2.set_ylabel("Green Channel Intensity")

    ax3.plot(pixelDistances, bluePoints, 'b')
    ax3.set_xlabel("Distance [pixels]")
    ax3.set_ylabel("Blue Channel Intensity")

    ax4.plot(pixelDistances, avgPoints, 'black')
    ax4.set_xlabel("Distance [pixels]")
    ax4.set_ylabel("Average RGB Intensity Values")

    fig2 = plt.figure(figsize=(9, 6.5))
    ax1 = fig2.add_subplot(221)
    ax2 = fig2.add_subplot(222)
    ax3 = fig2.add_subplot(223)
    ax4 = fig2.add_subplot(224)

    bins = 128
    ax1.hist(redPoints, bins=bins, color='red')
    ax1.set_xlabel("Red Channel Intensity")
    ax1.set_ylabel("Counts")

    ax2.hist(greenPoints, bins=bins, color='green')
    ax2.set_xlabel("Green Channel Intensity")
    ax2.set_ylabel("Counts")

    ax3.hist(bluePoints, bins=bins, color='blue')
    ax3.set_xlabel("Blue Channel Intensity")
    ax3.set_ylabel("Counts")

    ax4.hist(avgPoints, bins=bins, color='black')
    ax4.set_xlabel("Average RGB Intensity")
    ax4.set_ylabel("Counts")

    if show:
        fig1.show()
        fig2.show()

    fig1.savefig(imageDirName + "plots.png")
    fig2.savefig(imageDirName + "histograms.png")


def saveRGBChannelGreyscaleImages(image, p1, p2, imageDirName, show=True):
    """
    Displays the line where the image was analyzed
    """
    thickness = 2
    shade = 255
    blueChannel, greenChannel, redChannel = cv2.split(image)

    cv2.line(image, p1, p2, shade, thickness)
    cv2.line(blueChannel, p1, p2, shade, thickness)
    cv2.line(greenChannel, p1, p2, shade, thickness)
    cv2.line(redChannel, p1, p2, shade, thickness)

    cv2.circle(image, p1, thickness + 5, shade, thickness=thickness)
    cv2.circle(blueChannel, p1, thickness + 5, shade, thickness=thickness)
    cv2.circle(greenChannel, p1, thickness + 5, shade, thickness=thickness)
    cv2.circle(redChannel, p1, thickness + 5, shade, thickness=thickness)

    cv2.imwrite(imageDirName + "originalImage.png", image)
    cv2.imwrite(imageDirName + "blueChannel.png", blueChannel)
    cv2.imwrite(imageDirName + "redChannel.png", redChannel)
    cv2.imwrite(imageDirName + "greenChannel.png", greenChannel)

    if show:
        cv2.namedWindow('Blue', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Blue', 600, 600)
        cv2.imshow('Blue', blueChannel)

        cv2.namedWindow('Green', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Green', 600, 600)
        cv2.imshow('Green', greenChannel)

        cv2.namedWindow('Red', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Red', 600, 600)
        cv2.imshow('Red', redChannel)

        cv2.namedWindow('Original', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Original', 600, 600)
        cv2.imshow('Original', image)

        cv2.waitKey(0)
        cv2.destroyAllWindows()


def main():
    # analyze("./Photos/300nm/DSL30008.TIF", (1160, 1345), (1241, 1308))
    analyze("./Photos/UnknownThickness/DSL30001-Unkown-Thickness.TIF",
            (1454, 627), (1548, 772))

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
