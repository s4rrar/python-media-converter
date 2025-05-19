# 🎬 Python Media Converter

**Python Media Converter** is a terminal-based utility that allows users to convert media files (video, audio, and image formats) from one format to another using a simple and interactive menu-driven interface. Built on top of `ffmpeg`, this tool streamlines batch media conversions with ease.

---

## ✨ Features

- Convert media files (video/audio/images) using `ffmpeg`
- Menu-driven user interface in the terminal
- Batch processing support
- Detects media files in the current directory
- Supports custom and common output formats
- Interactive file selection and format conversion
- Cross-platform (Windows, macOS, Linux)

---

## 🛠️ Requirements

- Python 3.6+
- [ffmpeg](https://ffmpeg.org/) must be installed and accessible via the command line

### Install Python dependencies:
```bash
pip install ffmpeg-python
````

---

## 🚀 Usage

1. Place the script (`pmc.py`) in a directory containing media files.
2. Run the script:

```bash
python pmc.py
```

3. Follow the interactive prompts to:

   * Select input format
   * Choose output format
   * Select files to convert
   * Provide an optional output directory

---

## 🧾 Supported Formats

**Input & Output (common):**

* **Video**: mp4, avi, mkv, mov, webm, m4v
* **Audio**: mp3, wav, flac, aac, ogg, m4a
* **Images**: jpg, png, gif, webp

**Other input formats supported:**

* ts, 3gp, vob, mpg, mpeg, mxf, divx, m2ts, etc.

---

## 📁 Directory Structure

```
your-folder/
├── pmc.py
├── example.mp4
├── song.wav
└── ...
```

---

## 👤 Author

Created by **@s4rrar**

---

## 📝 Notes

* Conversion failures are handled gracefully with error messages.
* Press `Ctrl+C` at any time to cancel a running operation.
* The tool does not overwrite original files unless you direct output to the same location.
