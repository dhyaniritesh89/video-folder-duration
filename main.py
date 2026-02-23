import os
import subprocess

VIDEO_EXTENSIONS = (".mp4", ".mkv", ".webm", ".avi", ".mov")


def get_video_duration(path):
    cmd = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        path
    ]

    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"ffprobe failed for {path}: {result.stderr}")

    return float(result.stdout.strip())


def seconds_to_hms(seconds):
    seconds = int(seconds)
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def main():
    folder_path = input("Enter folder path: ").strip()

    if not os.path.exists(folder_path):
        print("Path does not exist.")
        return

    if not os.path.isdir(folder_path):
        print("Path is not a directory.")
        return

    total_seconds = 0.0
    longest_file = None
    longest_duration = 0.0

    for name in os.listdir(folder_path):
        full_path = os.path.join(folder_path, name)

        if not os.path.isfile(full_path):
            continue

        if not name.lower().endswith(VIDEO_EXTENSIONS):
            continue

        try:
            duration = get_video_duration(full_path)
            total_seconds += duration

            if duration > longest_duration:
                longest_duration = duration
                longest_file = name

            print(f"{name} -> {duration:.2f} seconds")

        except Exception as e:
            print(f"Failed to read {name}: {e}")

    print("\n--- Summary ---")
    print(f"Total duration: {seconds_to_hms(total_seconds)}")
    if longest_file:
        print(f"Longest video: {longest_file} ({seconds_to_hms(longest_duration)})")
    else:
        print("No video files found.")


if __name__ == "__main__":
    main()