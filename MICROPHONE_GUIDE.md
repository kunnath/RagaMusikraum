# 🎤 Live Microphone Input Feature

## 🎯 Overview

Record your voice directly and see your musical notes in **real-time**! Perfect for:
- 🎵 **Vocal practice** - See which notes you're singing
- 🎓 **Learning to sing** - Check if you're hitting the right pitch
- 🎼 **Music transcription** - Record melodies by humming
- 📊 **Pitch accuracy** - Improve your vocal control

## ✨ Features

### 1. **Direct Microphone Recording**
- 🎙️ Record from any connected microphone
- ⏱️ Flexible recording duration (5-60 seconds)
- 🔊 Built-in microphone test
- 📊 Real-time audio level monitoring

### 2. **Instant Note Analysis**
- 🎵 Detects musical notes from your voice
- 📈 Shows pitch accuracy over time
- 📊 Note distribution visualization
- 🎹 Generates MIDI from your singing

### 3. **Visual Feedback**
- 📉 Pitch contour graph
- 🎼 Notes over time visualization
- 📊 Note frequency distribution
- 🎯 Most common notes display

### 4. **Export Options**
- 💾 Save raw recording
- 🎹 Export to MIDI file
- 📄 Export analysis as JSON
- 🖼️ Save visualizations

## 🚀 How to Use

### Step 1: Select Microphone
```
1. Open the app
2. Go to "🎤 Live Mic" tab
3. Select your microphone from dropdown
4. Click "🔊 Test Microphone" to verify it works
```

### Step 2: Configure Settings
```
⏱️ Recording Duration: 5-60 seconds
🎵 Pitch Detection: CREPE (best for vocals)
✨ Options: Enable smoothing and outlier removal
```

### Step 3: Record Your Voice
```
1. Click "🔴 Start Recording"
2. Sing or speak clearly
3. Watch the countdown timer
4. Recording automatically stops
```

### Step 4: Analyze
```
1. Check audio level (should be > 0.01)
2. Click "🎵 Analyze Recording"
3. View your notes and pitch accuracy
4. Download MIDI or JSON if needed
```

## 🎓 Usage Examples

### Example 1: Vocal Practice
```
Goal: Check if you can sing a C major scale

1. Record: 10 seconds
2. Sing: C - D - E - F - G - A - B - C
3. Analyze: See if you hit all the right notes
4. Compare: Check pitch accuracy graph
```

### Example 2: Pitch Training
```
Goal: Improve pitch accuracy

1. Record: 15 seconds
2. Hold: One sustained note (e.g., "Aahhh" on A4)
3. Analyze: Check if pitch is stable
4. Review: Look at pitch contour for wobble
```

### Example 3: Song Learning
```
Goal: Learn melody of a song

1. Record: 30 seconds
2. Hum/Sing: The melody you're practicing
3. Analyze: Compare notes to sheet music
4. Export: Download MIDI to verify in DAW
```

## 📋 Requirements

### Hardware:
- 🎤 **Microphone** (built-in or USB)
- 🔊 **Quiet environment** for best results

### Software:
- ✅ Microphone permissions granted to browser/app
- ✅ `sounddevice` library installed
- ✅ Audio drivers working properly

## ⚙️ Settings Guide

### **Recording Duration**
- **5-10s**: Quick note checks
- **15-30s**: Practicing scales/phrases
- **30-60s**: Full melodies

### **Pitch Detection Method**
- **CREPE**: Best for vocals (most accurate)
- **Librosa**: Faster, good enough for practice
- **Aubio**: Alternative option

### **Post-Processing**
- **Smooth pitch**: ✅ Recommended (removes jitter)
- **Remove outliers**: ✅ Recommended (removes errors)

## 📊 Understanding Results

### **Audio Level**
```
> 0.1:  Loud (might be too loud)
0.01-0.1: Good (ideal range)
< 0.01: Quiet (speak/sing louder)
```

### **Note Accuracy**
- Check if detected notes match what you sang
- Look at pitch contour for stability
- Compare note distribution to expectations

### **Visualizations**

#### **Notes Over Time**
Shows which notes you sang and when
- X-axis: Time in seconds
- Y-axis: Musical notes
- Points: Each detected note instance

#### **Pitch Contour**
Shows your pitch accuracy
- Blue dots: Detected pitch
- Smooth line: Your vocal contour
- Deviations: Pitch wobble or inaccuracy

#### **Note Distribution**
Shows how often you hit each note
- Bars: Each unique note
- Height: Frequency of occurrence
- Helps identify your vocal range

## 💡 Tips for Best Results

### 🎤 **Microphone Setup**
1. Position mic 6-12 inches from mouth
2. Speak/sing directly toward mic
3. Avoid touching or bumping mic
4. Use pop filter if available

### 🔇 **Environment**
1. Record in quiet room
2. Close windows (reduce outside noise)
3. Turn off fans/AC if possible
4. Avoid echo-heavy rooms

### 🎵 **Vocal Technique**
1. Sing clearly and steadily
2. Start with simple scales
3. Hold notes for at least 1 second
4. Avoid sliding between notes (unless practicing)
5. Breathe quietly between phrases

### 📈 **Analysis**
1. Test mic before important recording
2. Check audio level after recording
3. Re-record if level is too low/high
4. Use smooth pitch for cleaner results
5. Compare to reference recordings

## 🐛 Troubleshooting

### ❌ **"No microphone devices found"**

**Solutions:**
1. Check mic is plugged in
2. Grant microphone permissions
3. Restart the app
4. Check system audio settings
5. Try different USB port (for USB mics)

---

### ❌ **"Very low audio level detected"**

**Solutions:**
1. Sing/speak louder
2. Move closer to mic
3. Increase mic volume in system settings
4. Check mic isn't muted
5. Select correct microphone device

---

### ❌ **"No clear notes detected"**

**Solutions:**
1. Sing more clearly (avoid mumbling)
2. Hold notes longer (at least 1 second)
3. Reduce background noise
4. Try CREPE pitch detection
5. Check mic is working (use test button)

---

### ❌ **"Recording failed"**

**Solutions:**
1. Grant microphone permissions
2. Close other apps using mic
3. Check mic isn't in use
4. Restart browser/app
5. Try different microphone device

---

### ❌ **"No audio detected after silence removal"**

**Solutions:**
1. Record with more volume
2. Speak/sing closer to mic
3. Check mic sensitivity
4. Disable silence removal temporarily
5. Test mic to verify it's working

## 🎯 Use Cases

### **1. Vocal Training**
- Practice scales
- Check pitch accuracy
- Improve vocal control
- Track progress over time

### **2. Song Learning**
- Learn melodies by ear
- Verify you're singing right notes
- Practice difficult passages
- Compare to original

### **3. Music Creation**
- Record melody ideas
- Hum compositions
- Export to MIDI for production
- Document musical thoughts

### **4. Pitch Practice**
- Train perfect pitch
- Improve relative pitch
- Practice intervals
- Develop muscle memory

### **5. Teaching**
- Show students their pitch
- Visual feedback for learning
- Record practice sessions
- Track student progress

## 📊 Example Workflow

### **Daily Vocal Practice Routine**

#### **Warm-up (5 min)**
```
1. Record: 10s humming scales
2. Analyze: Check if hitting notes cleanly
3. Repeat: Until pitch is stable
```

#### **Scale Practice (10 min)**
```
1. Record: 15s C major scale
2. Analyze: Verify all notes correct
3. Export: Save MIDI for reference
4. Record: Other scales (D, E, F, etc.)
```

#### **Song Practice (15 min)**
```
1. Record: 30s melody section
2. Analyze: Compare to original notes
3. Identify: Problem areas
4. Repeat: Until accurate
```

#### **Cool-down (5 min)**
```
1. Record: Gentle descending scales
2. Save: Best performances
3. Review: Progress vs yesterday
```

## 🎓 Learning Path

### **Beginner Level**
1. ✅ Test microphone setup
2. ✅ Record single sustained notes
3. ✅ Practice C major scale
4. ✅ Identify your vocal range
5. ✅ Learn to read pitch graphs

### **Intermediate Level**
1. ✅ Practice chromatic scales
2. ✅ Work on pitch stability
3. ✅ Try different keys
4. ✅ Record simple melodies
5. ✅ Compare to reference tracks

### **Advanced Level**
1. ✅ Practice complex melodies
2. ✅ Work on pitch precision
3. ✅ Record full songs
4. ✅ Analyze vibrato control
5. ✅ Export for production use

## 📈 Tracking Progress

### **What to Track**
- 📊 Pitch accuracy over time
- 🎵 Number of correct notes
- 📈 Consistency of pitch
- 🎼 Expansion of vocal range
- ⏱️ Duration you can hold notes

### **How to Track**
1. Save JSON exports with dates
2. Compare note distributions
3. Review pitch stability graphs
4. Keep MIDI files organized
5. Document improvements

## 🎉 Success Metrics

### **Good Session:**
- ✅ Audio level: 0.01-0.1
- ✅ 80%+ correct notes
- ✅ Stable pitch (minimal wobble)
- ✅ Clear note transitions
- ✅ Good note distribution

### **Needs Improvement:**
- ❌ Audio level < 0.01 or > 0.1
- ❌ < 70% correct notes
- ❌ Pitch wobbles significantly
- ❌ Unclear note boundaries
- ❌ Limited note range

## 🔗 Integration

### **Use with Other Features**

1. **Compare with Original:**
   - Record your version
   - Analyze original song
   - Use comparison feature
   - See differences

2. **MIDI Export:**
   - Record melody
   - Export to MIDI
   - Import to DAW
   - Produce full song

3. **Practice Tracking:**
   - Record daily
   - Save all sessions
   - Compare progress
   - Identify patterns

## 📝 Summary

The Live Microphone feature turns your computer into a real-time vocal analyzer!

**Perfect for:**
- 🎤 Singers improving technique
- 🎓 Music students learning pitch
- 🎵 Composers capturing ideas
- 👨‍🏫 Teachers providing visual feedback

**Key Benefits:**
- ⚡ Instant feedback
- 📊 Visual representations
- 💾 Exportable results
- 🎯 Accurate analysis

Start recording and see your musical notes come to life! 🎵✨
