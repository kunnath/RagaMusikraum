# Song Comparison Feature

Compare your song recordings with original songs to see how accurately you're performing!

## Features

### 📊 Comprehensive Analysis
- **Overall Similarity Score**: Get a percentage score (0-100%) with letter grade (A-F)
- **Note Distribution**: See which notes are common, missing, or extra
- **Note Matching**: Find out which notes match in timing and pitch
- **Timing Analysis**: Measure how accurate your timing is

### 🎯 Scoring System

The overall score is calculated from three components:

1. **Note Similarity (40%)**: How similar are the notes you used vs the original?
2. **Note Matching (40%)**: How many notes match in both pitch and timing?
3. **Timing Accuracy (20%)**: How close are your note timings?

**Grading Scale:**
- A (90-100%): Excellent
- B (80-89%): Very Good
- C (70-79%): Good
- D (60-69%): Fair
- F (0-59%): Needs Improvement

## Usage

### Option 1: Web Interface (Streamlit)

1. Start the app: `./run.sh` or `streamlit run app.py`
2. Go to the **"🔍 Compare Songs"** tab
3. Select or upload both songs (original and yours)
4. Adjust time tolerance if needed (default: 0.5 seconds)
5. Click **"Compare Songs"**
6. View detailed results and download reports

### Option 2: Command Line

```bash
# Basic comparison
python compare_songs.py original_analysis.json my_song_analysis.json

# With custom time tolerance
python compare_songs.py original.json my_song.json --tolerance 1.0

# Save reports
python compare_songs.py original.json my_song.json \
    --output report.txt \
    --json results.json
```

**Arguments:**
- `original`: Path to original song's JSON analysis file
- `comparison`: Path to your song's JSON analysis file
- `--tolerance`, `-t`: Time tolerance in seconds (default: 0.5)
- `--output`, `-o`: Save text report to file
- `--json`, `-j`: Save JSON results to file

## Understanding the Results

### Overall Score Tab
Shows your total similarity score, grade, and component scores.

### Note Distribution Tab
- **Common Notes**: Notes that appear in both songs
- **Missing Notes**: Notes in the original that you didn't hit
- **Extra Notes**: Notes you played that weren't in the original

### Note Matching Tab
- **Matched Notes**: Notes that match in both pitch and timing
- **Match Percentage**: Percentage of original notes you matched
- Shows detailed timing and frequency differences

### Timing Analysis Tab
- **Average Time Difference**: How far off your timing is on average
- **Timing Accuracy**: Percentage score for timing precision
- **Max/Min Differences**: Best and worst timing deviations

## Example Workflow

1. **Analyze the original song:**
   ```bash
   # In the Streamlit app, analyze the original song
   # This creates: outputs/original_song_20241210_123456_analysis.json
   ```

2. **Record and analyze your version:**
   ```bash
   # Analyze your recording
   # This creates: outputs/my_version_20241210_130000_analysis.json
   ```

3. **Compare them:**
   ```bash
   python compare_songs.py \
       outputs/original_song_20241210_123456_analysis.json \
       outputs/my_version_20241210_130000_analysis.json \
       --output comparison_report.txt
   ```

## Tips for Better Scores

### Improve Note Matching (40% weight)
- Practice hitting the right notes at the right time
- Use a metronome to improve timing
- Focus on notes you're missing

### Improve Note Similarity (40% weight)
- Learn all the notes in the original song
- Avoid adding extra notes or embellishments
- Match the pitch range of the original

### Improve Timing Accuracy (20% weight)
- Practice with backing tracks
- Record yourself and listen back
- Use the time tolerance setting to identify timing issues

## Time Tolerance Setting

The **time tolerance** determines how close in time two notes need to be to count as matching:

- **0.1-0.3s**: Strict (professional level)
- **0.5s**: Default (good for practice)
- **1.0s+**: Lenient (for beginners)

Lower tolerance = harder to match notes, but more accurate feedback.

## Report Formats

### Text Report
Human-readable format with:
- Overall score and grade
- Detailed statistics
- Sample matching/missing notes
- Timing analysis

### JSON Report
Machine-readable format containing:
- All raw comparison data
- Full lists of matches and mismatches
- Detailed statistics
- Can be used for further analysis

## Example Output

```
================================================================================
SONG COMPARISON REPORT
================================================================================

Original Song: outputs/original_song_analysis.json
Your Song: outputs/my_version_analysis.json

================================================================================
OVERALL SCORE
================================================================================
Overall Similarity: 78.45%
Grade: C (Good)

  • Note Similarity: 82.30%
  • Note Matching: 75.00%
  • Timing Accuracy: 78.50%

================================================================================
NOTE DISTRIBUTION ANALYSIS
================================================================================
Original Song Total Notes: 120
Your Song Total Notes: 115
Common Notes: 28 notes
  C4, C#4, D4, D#4, E4, F4, F#4, G4, G#4, A4, A#4, B4...

Notes in Original but NOT in Your Song (3): 
  B5, C6, D6

================================================================================
NOTE MATCHING ANALYSIS
================================================================================
Matched Notes: 90 / 120 (75.00%)
Unmatched in Original: 30
Unmatched in Your Song: 25

================================================================================
TIMING ANALYSIS
================================================================================
Average Timing Difference: 0.234s
Timing Accuracy: 78.50%
Max Time Difference: 0.487s
Min Time Difference: 0.012s
```

## Troubleshooting

### "No notes detected"
- Ensure both songs have been analyzed successfully
- Check that the JSON files contain note data

### Low similarity score
- Verify you're comparing the right songs
- Check the time tolerance setting
- Listen to both songs to identify differences

### "File not found"
- Use absolute paths or ensure you're in the correct directory
- Verify the JSON files exist in the outputs folder

## API Usage (for developers)

```python
from src.song_comparator import SongComparator

# Create comparator
comparator = SongComparator(time_tolerance=0.5)

# Compare songs
results = comparator.compare_songs(
    'original.json',
    'comparison.json'
)

# Generate report
report = comparator.generate_comparison_report(results)
print(report)

# Access specific metrics
print(f"Score: {results['overall_score']['overall_similarity_score']}%")
print(f"Matched: {results['note_matching']['match_percentage']}%")
```

## Future Enhancements

Potential features to add:
- Visual comparison graphs
- Note-by-note playback alignment
- Practice mode with real-time feedback
- Historical progress tracking
- Multiple song comparisons
