import os
import subprocess

# Set your input and output folders here
import os

user = os.getenv("USERPROFILE")
input_dir = os.path.join(user, "Music", "iTunes", "iTunes Media", "Music")
output_dir = os.path.join(user, "Music", "ConvertedMP3")


# Create output folder if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

failures = []

print(f"Scanning '{input_dir}' for .m4a files...")

for root, dirs, files in os.walk(input_dir):
    for file in files:
        if file.lower().endswith(".m4a"):
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, input_dir)
            rel_path_mp3 = os.path.splitext(rel_path)[0] + ".mp3"
            dest_path = os.path.join(output_dir, rel_path_mp3)

            # Create target folder
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)

            if not os.path.exists(dest_path):
                print(f"Converting: {rel_path}")
                try:
                    result = subprocess.run([
                        "ffmpeg", "-v", "error",
                        "-i", full_path,
                        "-codec:a", "libmp3lame",
                        "-qscale:a", "2",
                        dest_path
                    ], check=True)
                except subprocess.CalledProcessError:
                    print(f"[!] Failed to convert: {rel_path}")
                    failures.append(rel_path)
            else:
                print(f"Skipping (already exists): {rel_path}")

print("\n✅ Done!")

if failures:
    print(f"\n❌ {len(failures)} files failed to convert:")
    for f in failures:
        print(" -", f)
