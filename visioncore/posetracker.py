import cv2
import mediapipe as mp
import numpy as np
class poseTracker():

    def __init__(self, mode=False,detectionCon=0.5,modelComplexity=1):
        self.mode = mode
        self.detectionCon = detectionCon
        self.modelComplex = modelComplexity
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(static_image_mode= False , model_complexity= self.modelComplex, enable_segmentation=True, min_detection_confidence= self.detectionCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.poseLandmarks = []
        self.rightHandPosition = None
        self.leftHandPosition = None
   
    def poseFinder(self,image):
        image_copy = image.copy()
        imageRGB = cv2.cvtColor(image_copy,cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imageRGB)

    def isFullPoseInImage(self):
        if self.results.pose_landmarks:
            landmarks = list(self.results.pose_landmarks.landmark)
            """cv2.imshow("thresh" , thresh)
            cv2.waitKey(1)"""
            nose = landmarks[0]
            nose_visibility = nose.visibility
            leftfoot = landmarks[32]
            leftfoot_visibilty = leftfoot.visibility
            rightfoot = landmarks[31]
            rightfoot_visibilty = rightfoot.visibility
            if nose_visibility > 0.999:
                return True
            if nose_visibility > 0.999 and leftfoot_visibilty > 0.5 and rightfoot_visibilty > 0.5:
                return True
            else :
                return False    
        else:
            return False
        

    def landmarksDetector(self,height,width):
        self.poseLandmarks = []
        if self.results.pose_landmarks:
            temp = []
            for lm in list(self.results.pose_landmarks.landmark):
                cx = int(lm.x * width)
                cy = int(lm.y * height)
                temp.append((cy,cx))
            self.poseLandmarks = temp
        
    
    """def interestedPointsDetectors(self):
        self.rightHandPosition = None
        self.leftHandPosition = None
        if len(self.poseLandmarks)> 0:
            self.rightHandPosition = self.poseLandmarks[16]
            self.leftHandPosition = self.poseLandmarks[15]
        else:
            self.leftHandPosition = None
            self.rightHandPosition = None"""
    
    def landmarkByItsIndex(self,index):
        if len(self.poseLandmarks) > 0:
            return self.poseLandmarks[index]
        else:
            return None
        
    def drawLandMarks(self,image):
        image_copy = image.copy()
        self.mpDraw.draw_landmarks(image_copy, self.results.pose_landmarks)
        return image_copy

    """def segmentationMask(self,image):
        image_copy = image.copy()
        condition = np.stack((self.results.segmentation_mask,) * 3, axis=-1) > 0.1
        bg_image = np.zeros(image_copy.shape, dtype=np.uint8)
        bg_image[:] = (255, 255, 255)
        image_copy = np.where(condition, image_copy, bg_image)
        return image_copy"""
    
    def posemask(self):
        _,thresh = cv2.threshold(self.results.segmentation_mask,0.1,1,cv2.THRESH_BINARY)
        #cv2.imshow("thresh" , thresh)
        #cv2.waitKey(1)
        return thresh
    
    def inverseBinaryPoseMask(self):
        _,thresh = cv2.threshold(self.results.segmentation_mask,0.1,1,cv2.THRESH_BINARY_INV)
        inverse = (thresh*255).round().astype(np.uint8)
        return inverse