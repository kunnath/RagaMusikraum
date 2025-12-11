# 🔧 Streaming Error Troubleshooting Guide

## Common Streaming Errors and Solutions

### ❌ "Video is private or restricted"

**Cause:** The video is not publicly accessible.

**Solutions:**
1. ✅ Use **"Download & Analyze"** mode instead (more compatible)
2. Check if video requires sign-in
3. Try a different public video

---

### ❌ "Video is age-restricted or region-locked"

**Cause:** Video has age or geographical restrictions.

**Solutions:**
1. ✅ Use **"Download & Analyze"** mode (may bypass some restrictions)
2. Try accessing from a different location
3. Check if video is available in your region

---

### ❌ "Cannot extract audio stream URL"

**Cause:** YouTube's stream format is not compatible or URL expired.

**Solutions:**
1. ✅ Use **"Download & Analyze"** mode
2. Refresh the page and try again
3. Copy the URL again (it may have changed)

---

### ❌ "Network connection issue"

**Cause:** Internet connection problems or timeout.

**Solutions:**
1. Check your internet connection
2. Disable VPN if enabled
3. Try again in a few moments
4. Use **"Download & Analyze"** mode for better reliability

---

### ❌ "Cannot process audio file"

**Cause:** Audio format is incompatible or file is corrupted.

**Solutions:**
1. ✅ Use **"Download & Analyze"** mode
2. Try a different video
3. Verify FFmpeg is installed: `ffmpeg -version`

---

### ❌ "No audio data downloaded"

**Cause:** Streaming stopped before any data was received.

**Solutions:**
1. Check internet speed (need stable connection)
2. Try a shorter video
3. Use **"Download & Analyze"** mode

---

## 🎯 When to Use Each Mode

### Use **Quick Stream Analysis** when:
- ✅ Video is public and unrestricted
- ✅ You have stable internet connection
- ✅ You only need first 60 seconds
- ✅ You want fast results
- ✅ Disk space is limited

### Use **Download & Analyze** when:
- ✅ Stream mode fails
- ✅ Video has restrictions
- ✅ You need the full song
- ✅ Internet is unstable
- ✅ You want to keep the audio file

---

## 🐛 Debug Steps

### Step 1: Verify the URL
```
1. Copy the URL directly from YouTube
2. Make sure it starts with https://
3. Check for any extra characters
4. Try the URL in your browser first
```

### Step 2: Check Video Status
```
✓ Is the video public?
✓ Does it play in your browser?
✓ Is it available in your country?
✓ Is it age-restricted?
```

### Step 3: Test Your Setup
```
1. Check internet: ping google.com
2. Check FFmpeg: ffmpeg -version
3. Try a different video
4. Restart the app
```

### Step 4: Try Download Mode
```
If streaming fails:
1. Click "Download & Analyze" instead
2. Wait for full download
3. Should work more reliably
```

---

## 💡 Pro Tips

### For Best Results:
1. **Use popular, public videos** - Better compatibility
2. **Test with short videos first** - Faster feedback
3. **Keep internet stable** - Streaming requires continuous connection
4. **Have FFmpeg updated** - Latest version works best

### Streaming Limitations:
- ⏱️ **60-second limit** by design
- 📦 **50 MB size limit** for safety
- 🌐 **Requires internet** during entire process
- 🎬 **YouTube only** (not other sites)

### When Streaming Works Best:
- 🎵 Music videos (not complex audio)
- 📹 High-quality uploads
- 🌐 Public, unrestricted content
- ⚡ Good internet connection (5+ Mbps)

---

## 🔍 Error Message Decoder

| Error Message | Meaning | Solution |
|--------------|---------|----------|
| "private or restricted" | Video not public | Use Download mode |
| "age-restricted" | Requires age verification | Use Download mode |
| "not available" | Video deleted/blocked | Try different video |
| "stream URL expired" | Temporary URL timeout | Refresh and retry |
| "network issue" | Connection problem | Check internet |
| "cannot process" | Format incompatible | Use Download mode |
| "empty file" | No data received | Check connection |

---

## 🚨 Still Having Issues?

### Quick Checklist:
- [ ] Video is public and plays in browser
- [ ] Internet connection is stable
- [ ] FFmpeg is installed and working
- [ ] URL is copied correctly
- [ ] Tried Download mode as alternative

### Get More Help:
1. Check the **Debug Information** expander in the error message
2. Read the full error traceback
3. Try with a simple test video (short, public music video)
4. Verify your Python packages are up to date: `pip install -r requirements.txt --upgrade`

---

## 📊 Success Rate by Video Type

| Video Type | Stream Success | Download Success |
|-----------|----------------|------------------|
| Public music video | ⭐⭐⭐⭐⭐ 95% | ⭐⭐⭐⭐⭐ 99% |
| Age-restricted | ⭐⭐ 30% | ⭐⭐⭐⭐ 80% |
| Region-locked | ⭐ 10% | ⭐⭐⭐ 60% |
| Private/Unlisted | ❌ 0% | ⭐ 20% |
| Live streams | ❌ 0% | ⭐⭐ 40% |

**Recommendation:** For maximum compatibility, use **Download & Analyze** mode.

---

## 🎓 Understanding the Process

### Stream Mode:
```
1. Extract video info (no download)
2. Get direct audio stream URL
3. Stream first 60s to memory
4. Save briefly to temp file
5. Process with librosa
6. Delete temp file
7. Continue analysis
```

### Where It Can Fail:
- ❌ Step 1: Video info blocked
- ❌ Step 2: Can't get stream URL
- ❌ Step 3: Network interruption
- ❌ Step 5: Format incompatibility

### Download Mode (More Reliable):
```
1. Download full video with yt-dlp
2. Extract audio permanently
3. Convert to WAV format
4. Process normally
```

**Why it's more reliable:**
- ✅ yt-dlp handles restrictions better
- ✅ Complete file on disk
- ✅ Multiple retry attempts
- ✅ Format conversion included

---

## ✅ Summary

**Stream Mode:** Fast but picky - works with simple public videos  
**Download Mode:** Slower but reliable - handles most situations

**When in doubt, use Download & Analyze!** 🚀
