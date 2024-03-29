import cv2
import mediapipe as mp
import pyautogui

class CursorController:
    def __init__(self):
        self.true=1
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
        self.screen_w, self.screen_h = pyautogui.size()
        self.cam = cv2.VideoCapture(0)
        self.timer = Timer()

    def control_cursor(self):
        # Read frame from webcam
        while self.true:
            ret, frame = self.cam.read()
            if not ret:
                break

            # Flip the frame horizontally
            frame = cv2.flip(frame, 1)

            # Convert frame to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process frame with face mesh model
            output = self.face_mesh.process(rgb_frame)

            # Get landmark points from output
            landmark_points = output.multi_face_landmarks
            frame_h, frame_w, _ = frame.shape

            # Check if there are any landmark points detected
            if landmark_points:
                # Get landmarks of the first face
                landmarks = landmark_points[0].landmark

                # Control cursor based on specific landmark points
                for id, landmark in enumerate(landmarks[474:478]):
                    x = int(landmark.x * frame_w)
                    y = int(landmark.y * frame_h)
                    cv2.circle(frame, (x, y), 3, (0, 255, 0))

                    if id == 1:
                        screen_x = self.screen_w / frame_w * x
                        screen_y = self.screen_h / frame_h * y
                        pyautogui.moveTo(screen_x, screen_y)

                # Check if left eye is closed
                left = [landmarks[145], landmarks[159]]
                for landmark in left:
                    x = int(landmark.x * frame_w)
                    y = int(landmark.y * frame_h)
                    cv2.circle(frame, (x, y), 3, (0, 255, 255))

                if (left[0].y - left[1].y) < 0.003:
                    pyautogui.doubleClick()
                    pyautogui.sleep(0.5)

                # Check if the cursor has been on the same place for more than 5 seconds
                if self.timer.last_x == screen_x and self.timer.last_y == screen_y:
                    self.timer.time += 1
                    if self.timer.time >= 1:
                        pyautogui.click()
                        self.timer.time = 0

                # Update the timer
                self.timer.last_x = screen_x
                self.timer.last_y = screen_y

            # Display frame with annotations
            #cv2.imshow('Eye Controlled Mouse', frame)

            # Check for key press to break the loop
            if cv2.waitKey(1) == 27:
                break

    def release(self):
        self.cam.release()
        cv2.destroyAllWindows()

class Timer:
    def __init__(self):
        self.time = 0
        self.last_x = 0
        self.last_y = 0

if __name__ == '__main__':
    cursor_controller = CursorController()
    cursor_controller.control_cursor()
    cursor_controller.release()




