import cv2
import numpy as np
import pyautogui
import keyboard
import subprocess
import os

def record_screen_with_cursor(output_raw="raw_record.mp4", output_final="compressed_record.mp4", fps=20):
    screen_width, screen_height = pyautogui.size()
    out = cv2.VideoWriter(output_raw, cv2.VideoWriter_fourcc(*"mp4v"), fps, (screen_width, screen_height))

    print("📽️ Recording started (ESC to stop)...")

    try:
        while True:
            if keyboard.is_pressed("esc"):
                print("\n🛑 ESC pressed. Stopping recording...")
                break

            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Draw mouse cursor
            x, y = pyautogui.position()
            cv2.circle(frame, (x, y), 8, (0, 255, 0), 2)

            out.write(frame)

    finally:
        out.release()
        print(f"💾 Raw video saved: {output_raw}")

        # Compress with ffmpeg (CRF 23 = good quality & size, preset slow = better compression)
        print("🔄 Compressing video with ffmpeg...")
        try:
            subprocess.run([
                "ffmpeg", "-y", "-i", output_raw,
                "-vcodec", "libx264", "-crf", "23", "-preset", "slow",
                output_final
            ], check=True)
            print(f"✅ Compressed video saved: {output_final}")

            # Optional: delete raw video to save space
            os.remove(output_raw)
            print(f"🧹 Raw video deleted: {output_raw}")
        except Exception as e:
            print("❌ ffmpeg compression failed:", e)

# Start recording
record_screen_with_cursor()
