# Song Comparison Feature - Quick Reference

## ✅ What's New

A complete song comparison system that helps you measure how accurately you're performing songs compared to the original!

## 🎯 What It Does

### 1. Overall Similarity Score (0-100%)
- Combines note similarity, note matching, and timing accuracy
- Letter grade (A-F) for easy understanding
- Weighted scoring: Note Similarity (40%) + Note Matching (40%) + Timing (20%)

### 2. Note Distribution Analysis
- Shows which notes appear in both songs
- Identifies missing notes (in original but not in yours)
- Identifies extra notes (in yours but not in original)

### 3. Note Matching Analysis  
- Finds notes that match in both pitch AND timing
- Shows timing and frequency differences for each match
- Lists unmatched notes from both songs

### 4. Timing Analysis
- Average timing difference
- Timing accuracy percentage
- Min/max timing differences
- Standard deviation

## 🚀 Quick Start

### Method 1: Web Interface (Easiest)
```bash
./run.sh  # or: streamlit run app.py
```
1. Go to "Compare Songs" tab
2. Select original and your song JSON files
3. Click "Compare Songs"
4. View results and download reports!

### Method 2: Command Line
```bash
# Basic comparison
python compare_songs.py original.json my_song.json

# Save reports
python compare_songs.py original.json my_song.json \
    --output report.txt \
    --json results.json

# Adjust tolerance
python compare_songs.py original.json my_song.json --tolerance 1.0
```

## 📝 Example Workflow

1. **Analyze original song:**
   - Use the web app to analyze the original song
   - This creates: `outputs/original_song_TIMESTAMP_analysis.json`

2. **Record and analyze your version:**
   - Sing or play the song
   - Analyze it to create: `outputs/my_version_TIMESTAMP_analysis.json`

3. **Compare:**
   - Use web interface or command line
   - Get detailed comparison report!

## 📊 Understanding Scores

| Grade | Score | Meaning |
|-------|-------|---------|
| A | 90-100% | Excellent - Nearly perfect match! |
| B | 80-89% | Very Good - Strong performance |
| C | 70-79% | Good - On the right track |
| D | 60-69% | Fair - Needs more practice |
| F | 0-59% | Needs Improvement |

## 🎓 Tips to Improve

### To Improve Note Matching (40% weight):
- Practice hitting right notes at right times
- Use a metronome
- Record yourself and review

### To Improve Note Similarity (40% weight):
- Learn all notes in the original
- Avoid adding embellishments
- Match the pitch range

### To Improve Timing (20% weight):
- Practice with backing tracks
- Focus on rhythm
- Start slower, build speed

## ⚙️ Settings

**Time Tolerance:** How close in time notes need to be to match
- 0.1-0.3s: Professional level (strict)
- 0.5s: Default (good for practice)
- 1.0s+: Beginner-friendly (lenient)

## 📦 Files Created

### Analysis Phase:
- `outputs/SONG_NAME_TIMESTAMP_analysis.json` - Contains all note data

### Comparison Phase:
- Text Report: Human-readable summary
- JSON Report: Machine-readable data for further analysis

## 🐛 Troubleshooting

**"No notes detected"**
- Ensure songs are analyzed successfully
- Check that audio quality is good

**Low scores**
- Verify you're comparing the right songs
- Adjust time tolerance
- Check if original analysis is accurate

**File not found**
- Use absolute paths
- Check files exist in outputs folder

## 🔍 What Gets Compared

For each note, the system checks:
- ✅ **Pitch**: Is it the same note (C4, D#5, etc.)?
- ✅ **Timing**: Does it occur at the same time?
- ✅ **Frequency**: How close is the actual frequency?

## 📚 Files Added

- `src/song_comparator.py` - Main comparison logic
- `compare_songs.py` - CLI tool
- `test_comparison.py` - Test suite
- `COMPARISON_GUIDE.md` - Detailed documentation
- Updated `app.py` - Added comparison tab

## 🎵 Example Use Cases

1. **Practice Tool**: Compare your practice recordings to originals
2. **Progress Tracking**: Save comparisons to see improvement over time
3. **Teaching**: Show students exactly which notes they're missing
4. **Cover Songs**: Measure accuracy of your covers
5. **Transcription Verification**: Check if your transcription matches the original

## 💡 Pro Tips

1. Analyze in quiet environment for best results
2. Use same pitch detection method for both songs
3. Enable post-processing for cleaner results
4. Start with lenient time tolerance, reduce as you improve
5. Focus on one metric at a time when practicing

## 🚀 Next Steps

Try it out:
```bash
# Test with sample data
python test_comparison.py

# Use with your songs
python compare_songs.py outputs/original.json outputs/my_version.json
```

Happy practicing! 🎶
