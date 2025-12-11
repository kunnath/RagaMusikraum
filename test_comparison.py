#!/usr/bin/env python3
"""
Test the song comparison feature
"""

import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.song_comparator import SongComparator

def create_test_data():
    """Create sample test data for comparison"""
    
    # Original song
    original = {
        'notes': [
            {'time': 0.0, 'note': 'C', 'octave': 4, 'full_note': 'C4', 'frequency': 261.63, 'cents_deviation': 0},
            {'time': 0.5, 'note': 'D', 'octave': 4, 'full_note': 'D4', 'frequency': 293.66, 'cents_deviation': 0},
            {'time': 1.0, 'note': 'E', 'octave': 4, 'full_note': 'E4', 'frequency': 329.63, 'cents_deviation': 0},
            {'time': 1.5, 'note': 'F', 'octave': 4, 'full_note': 'F4', 'frequency': 349.23, 'cents_deviation': 0},
            {'time': 2.0, 'note': 'G', 'octave': 4, 'full_note': 'G4', 'frequency': 392.00, 'cents_deviation': 0},
            {'time': 2.5, 'note': 'A', 'octave': 4, 'full_note': 'A4', 'frequency': 440.00, 'cents_deviation': 0},
            {'time': 3.0, 'note': 'B', 'octave': 4, 'full_note': 'B4', 'frequency': 493.88, 'cents_deviation': 0},
            {'time': 3.5, 'note': 'C', 'octave': 5, 'full_note': 'C5', 'frequency': 523.25, 'cents_deviation': 0},
        ]
    }
    
    # Comparison song (similar but with some differences)
    comparison = {
        'notes': [
            {'time': 0.05, 'note': 'C', 'octave': 4, 'full_note': 'C4', 'frequency': 262.00, 'cents_deviation': 2},
            {'time': 0.55, 'note': 'D', 'octave': 4, 'full_note': 'D4', 'frequency': 294.00, 'cents_deviation': 1},
            # Missing E4
            {'time': 1.48, 'note': 'F', 'octave': 4, 'full_note': 'F4', 'frequency': 350.00, 'cents_deviation': 3},
            {'time': 2.10, 'note': 'G', 'octave': 4, 'full_note': 'G4', 'frequency': 391.00, 'cents_deviation': -2},
            {'time': 2.45, 'note': 'A', 'octave': 4, 'full_note': 'A4', 'frequency': 440.50, 'cents_deviation': 1},
            {'time': 3.05, 'note': 'B', 'octave': 4, 'full_note': 'B4', 'frequency': 494.00, 'cents_deviation': 0},
            # Extra note
            {'time': 3.25, 'note': 'A#', 'octave': 4, 'full_note': 'A#4', 'frequency': 466.16, 'cents_deviation': 0},
            {'time': 3.55, 'note': 'C', 'octave': 5, 'full_note': 'C5', 'frequency': 523.00, 'cents_deviation': -1},
        ]
    }
    
    return original, comparison


def main():
    print("=" * 80)
    print("Testing Song Comparison Feature")
    print("=" * 80)
    print()
    
    # Create test data
    print("Creating test data...")
    original, comparison = create_test_data()
    
    # Save to temp files
    os.makedirs('temp', exist_ok=True)
    
    original_path = 'temp/test_original.json'
    comparison_path = 'temp/test_comparison.json'
    
    with open(original_path, 'w') as f:
        json.dump(original, f, indent=2)
    
    with open(comparison_path, 'w') as f:
        json.dump(comparison, f, indent=2)
    
    print(f"✅ Test files created:")
    print(f"   Original: {original_path} ({len(original['notes'])} notes)")
    print(f"   Comparison: {comparison_path} ({len(comparison['notes'])} notes)")
    print()
    
    # Test comparison
    print("Running comparison...")
    print()
    
    comparator = SongComparator(time_tolerance=0.5)
    
    try:
        results = comparator.compare_songs(original_path, comparison_path)
        
        # Generate and display report
        report = comparator.generate_comparison_report(results)
        print(report)
        
        # Save report
        report_path = 'temp/test_comparison_report.txt'
        with open(report_path, 'w') as f:
            f.write(report)
        
        print(f"\n✅ Report saved to: {report_path}")
        
        # Display key metrics
        print("\n" + "=" * 80)
        print("KEY METRICS")
        print("=" * 80)
        score = results['overall_score']
        print(f"Overall Score: {score['overall_similarity_score']}%")
        print(f"Grade: {score['grade']}")
        print(f"Note Matching: {score['note_matching_score']}%")
        print(f"Timing Accuracy: {score['timing_accuracy_score']}%")
        print()
        
        match = results['note_matching']
        print(f"Matched Notes: {match['matching_notes_count']} / {len(original['notes'])}")
        print(f"Missing Notes: {match['unmatched_original_count']}")
        print(f"Extra Notes: {match['unmatched_comparison_count']}")
        print()
        
        print("✅ Test completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
