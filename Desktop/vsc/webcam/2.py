import threading
import time
import cv2

class JarvisEyes:
    def __init__(self, camera_index=0):
        # Initialize the camera connection
        self.cap = cv2.VideoCapture(camera_index)
        self.current_frame = None
        self.is_running = True
        self.lock = threading.Lock()  # Prevents thread collisions over the frame data
        
        if not self.cap.isOpened():
            print("Error: Could not open webcam.")
            self.is_running = False

    def start(self):
        """Spawns the background thread to handle camera frame grabbing."""
        if self.is_running:
            # target=self._update runs the loop in the background
            # daemon=True ensures the thread closes automatically when the main script ends
            threading.Thread(target=self._update, daemon=True).start()
            print("Jarvis Eyes: Background camera thread started.")

    def _update(self):
        """The infinite background loop that continuously pulls images from hardware."""
        while self.is_running:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Failed to grab frame from webcam.")
                continue
            
            # Safely update the frame inside a thread lock
            with self.lock:
                self.current_frame = frame
                
            # A microscopic sleep prevents the thread from consuming 100% CPU resource
            time.sleep(0.01)

    def get_latest_frame(self):
        """Allows other threads to safely request a snapshot copy of the current frame."""
        with self.lock:
            if self.current_frame is None:
                return None
            # Return a copy so the main thread doesn't accidentally mutate the live buffer
            return self.current_frame.copy()

    def stop(self):
        """Gracefully releases resources."""
        self.is_running = False
        self.cap.release()
        cv2.destroyAllWindows()
        print("Jarvis Eyes: Camera released.")


def main_voice_loop(eyes):
    """Placeholder for your main Jarvis loop (The Ears & Brain)."""
    print("Jarvis Ears: Listening loop online...")
    
    try:
        while True:
            # 1. Simulating the hotword trigger or text input trigger
            user_input = input("\nPress [Enter] to simulate saying 'Jarvis, what is this?' (or type 'exit' to quit): ")
            if user_input.strip().lower() == 'exit':
                break
                
            print("Jarvis: Checking my visual feed...")
            
            # 2. Instantly pull the frame sitting in RAM at this exact millisecond
            snapshot = eyes.get_latest_frame()
            
            if snapshot is not None:
                print(f"Jarvis: Frame grabbed successfully! Dimensions: {snapshot.shape[1]}x{snapshot.shape[0]}")
                
                # --- FUTURE PIPELINE STEPS GO HERE ---
                # Step A: Convert snapshot to base64
                # Step B: Send snapshot + transcribed text to your vision AI API
                # Step C: Send AI text response to Text-To-Speech library
                # --------------------------------------
                
                # Optional: Pop open a small window to visually show you what snapshot was passed to the AI
                cv2.imshow("Jarvis Visual Memory Snapshot", snapshot)
                cv2.waitKey(1000)  # Show the snapshot window for 1 second
                cv2.destroyWindow("Jarvis Visual Memory Snapshot")
            else:
                print("Jarvis: I'm currently blind. Check camera connections.")
                
    finally:
        eyes.stop()

if __name__ == "__main__":
    # 1. Spin up the background camera thread
    jarvis_eyes = JarvisEyes(camera_index=0)
    jarvis_eyes.start()
    
    # 2. Keep the main execution path on the Voice Loop
    main_voice_loop(jarvis_eyes)
    