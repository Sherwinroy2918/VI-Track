import cv2
import mediapipe as mp
import pyautogui
import time
import speech_recognition as sr
class Timer:
    def __init__(self):
        self.time = 0
        self.last_x = 0
        self.last_y = 0
class Script:
    def __init__(self):
        self.true = 1
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
        self.screen_w, self.screen_h = pyautogui.size()
        self.cam = cv2.VideoCapture(0)
        self.timer = Timer()

    def control_cursor(self):
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
                    if self.timer.time >= 5:
                        pyautogui.click()
                        self.timer.time = 0

                # Update the timer
                self.timer.last_x = screen_x
                self.timer.last_y = screen_y

            # Display frame with annotations
            cv2.imshow('Eye Controlled Mouse', frame)

            # Check for key press to break the loop
            if cv2.waitKey(1) == 27:
                break
        self.cam.release()
        cv2.destroyAllWindows()

    def control_voice(self):
        print("Say 'start!' to control the cursor with voice commands and say 'end' to terminate")

        while self.true:
            rk = sr.Recognizer()
            with sr.Microphone() as source:
                print("Listening...")
                audio = rk.listen(source)

            try:
                command = rk.recognize_google(audio).lower()
                print("You said:", command)

                if command == "end":
                    print("Voice command terminated")
                    break

                if "open" in command:
                    if "browser" in command:
                        pyautogui.press("win")
                        pyautogui.typewrite("chrome")
                        pyautogui.press("enter")
                    elif "word" in command:
                        pyautogui.press("win")
                        pyautogui.typewrite("Word")
                        pyautogui.press("enter")
                    # Add more application opening logic here...

                elif "close" in command:
                    if "browser" in command:
                        pyautogui.hotkey("ctrl", "w")
                    # Add more application closing logic here...

                # Add more voice command logic here...

            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")

    def control_hand(self):
        pyautogui.FAILSAFE = False
        mp_hands = mp.solutions.hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5,
        )
        cap = cv2.VideoCapture(0)
        click_start_time = None

        while cap.isOpened() and self.true:
            ret, frame = cap.read()

            if not ret:
                break

            frame = cv2.flip(frame, 1)
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = mp_hands.process(image_rgb)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    index_finger_tip = hand_landmarks.landmark[8]
                    x, y = index_finger_tip.x, index_finger_tip.y
                    cursor_x = int(x * self.screen_w)
                    cursor_y = int(y * self.screen_h)
                    pyautogui.moveTo(cursor_x, cursor_y)

                    if click_start_time is None:
                        click_start_time = time.time()
                    elif time.time() - click_start_time > 4:
                        pyautogui.click()
                        click_start_time = None

            if cv2.waitKey(1) & 0xFF == 27:
                break

        cap.release()
        cv2.destroyAllWindows()
        mp_hands.close()

    def main(self):
        print("Please select a control method:")
        print("1. Voice Control")
        print("2. Retina Movement Control")
        print("3. Hands-free control for cursor movement")
        control_method = input()

        if control_method == "1":
            self.control_voice()
        elif control_method == "2":
            self.control_cursor()
        elif control_method == "3":
            self.control_hand()
        else:
            print("Invalid input, please try again.")

if __name__ == '__main__':
    script = Script()
    script.main()
