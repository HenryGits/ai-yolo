import os
from os.path import splitext, basename, join

import numpy as np
from json2yolo import ds_dir

class DivideImages():

    def __init__(self, imagePath, outputDir):
        self.imageDir = imagePath
        self.listPathFile = outputDir + "/imagesPathAll.txt"
        self.outputDir = outputDir + "/"
        self.makeAllImagesPath(self.imageDir)
        self.DivideImagePath()

    def makeAllImagesPath(self, ImageDir):
        imagesList = os.listdir(ImageDir)
        imagesList = [x for x in imagesList if self.IsImage(x)]
        id2Name = [(splitext(x)[0], x) for x in imagesList]
        res = dict(id2Name)
        lines = list(res.values())
        with open(self.listPathFile, 'w') as f:
            for x in lines:
                # y = x.strip() + "\n"
                y = join(self.imageDir, x) + "\n"
                f.write(y)

    def IsImage(self, fileName):
        """ whether filename is an image or not """
        imgType = ['.bmp', '.jpg', '.jpeg', '.png', '.tif']
        baseName = basename(fileName)
        basenameExt = splitext(baseName)[-1]
        return (basenameExt in imgType) and (not baseName.startswith("."))

    def DivideImagePath(self):
        pathList = np.asarray(self.readImgPathFromfile(self.listPathFile))
        imgSum = len(pathList)
        np.random.seed(7)
        np.random.shuffle(pathList)

        numTest = int(imgSum * 0.15)
        numTrain = imgSum - numTest

        testList = pathList[:numTest]
        trainList = pathList[numTest:]

        with open(join(self.outputDir, "test.txt"), 'w') as f:
            for x in testList:
                y = x.strip() + "\n"
                f.write(y)

        with open(join(self.outputDir, "train.txt"), 'w') as f:
            for x in trainList:
                y = x.strip() + "\n"
                f.write(y)

    def readImgPathFromfile(self, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()
        lines = [x.strip() for x in lines]
        return lines


if __name__ == '__main__':
    # 参数1：收集的图片文件，参数2：生成训练集和测试集文件的路径
    divide = DivideImages(join(ds_dir, 'images'), ds_dir)
