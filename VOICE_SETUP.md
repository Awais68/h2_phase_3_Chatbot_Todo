# Voice Commands Setup Guide

## Current Status

✅ **SpeechRecognition** - Installed
✅ **PyAudio** - Installed
⚠️ **System Audio Libraries** - May need installation

---

## PyAudio System Dependencies

PyAudio requires system-level audio libraries. Install based on your OS:

### Ubuntu/Debian (Your System):
```bash
sudo apt-get update
sudo apt-get install portaudio19-dev python3-pyaudio
```

Then reinstall PyAudio:
```bash
cd "/media/data/hackathon series/hackathon-2/hackathon-2/sp-1"
source .venv/bin/activate
pip install --force-reinstall PyAudio
```

### macOS:
```bash
brew install portaudio
pip install PyAudio
```

### Windows:
```bash
# Download precompiled wheel from:
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
pip install PyAudio‑0.2.11‑cp313‑cp313‑win_amd64.whl
```

---

## Alternative: Voice Commands WITHOUT Microphone

If you can't install PyAudio or don't have a microphone, the app **still works perfectly**!

Voice commands are **completely optional**. All features are fully accessible via keyboard:

- ✅ Add tasks
- ✅ View/filter/search tasks
- ✅ Update/delete tasks
- ✅ Sort and organize
- ✅ All functionality available

**The voice feature is a bonus**, not required!

---

## Test Voice Setup

After installing system libraries, test if PyAudio works:

```bash
cd "/media/data/hackathon series/hackathon-2/hackathon-2/sp-1"
source .venv/bin/activate
python -c "import pyaudio; print('✓ PyAudio working!')"
```

If successful, voice commands will work in the app!

---

## Using Voice Commands

Once PyAudio is working:

1. Run the app: `python phase1_complete_cli.py`
2. Choose option **8** (🎤 Voice Commands)
3. Speak clearly:
   - "Add task buy milk high priority tomorrow tags personal shopping"
   - "List tasks"
   - "Filter by status completed"
   - "Search meeting"

The app will transcribe and execute your command!

---

## Recommendation

**For now**, use the app without voice commands. It has all the core features working:

```bash
python phase1_complete_cli.py
```

Voice is a nice-to-have extra. Everything else works great! 🎉
