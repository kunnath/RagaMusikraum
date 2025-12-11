"""
Song Comparison Module
Compares two songs to analyze similarity in notes, timing, and overall structure.
"""

import json
import numpy as np
from collections import Counter
from typing import Dict, List, Tuple, Any
import logging

logger = logging.getLogger(__name__)


class SongComparator:
    """Compare two songs and analyze their similarities and differences."""
    
    def __init__(self, time_tolerance: float = 0.5):
        """
        Initialize the song comparator.
        
        Args:
            time_tolerance: Time window (in seconds) to consider notes as "matching" in time
        """
        self.time_tolerance = time_tolerance
    
    def load_song_data(self, json_path: str) -> Dict[str, Any]:
        """
        Load song analysis data from JSON file.
        
        Args:
            json_path: Path to the JSON file containing song analysis
            
        Returns:
            Dictionary containing song data
        """
        try:
            with open(json_path, 'r') as f:
                data = json.load(f)
            logger.info(f"Loaded song data from {json_path}")
            return data
        except Exception as e:
            logger.error(f"Error loading song data: {str(e)}")
            raise
    
    def extract_notes(self, song_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract notes list from song data.
        
        Args:
            song_data: Song analysis data dictionary
            
        Returns:
            List of note dictionaries
        """
        return song_data.get('notes', [])
    
    def compare_note_distributions(self, notes1: List[Dict], notes2: List[Dict]) -> Dict[str, Any]:
        """
        Compare the overall note distributions between two songs.
        
        Args:
            notes1: Notes from first song
            notes2: Notes from second song
            
        Returns:
            Dictionary with comparison statistics
        """
        # Get note counters
        notes1_counter = Counter(n['full_note'] for n in notes1)
        notes2_counter = Counter(n['full_note'] for n in notes2)
        
        # Get all unique notes
        all_notes = set(notes1_counter.keys()) | set(notes2_counter.keys())
        
        # Calculate statistics
        total_notes1 = sum(notes1_counter.values())
        total_notes2 = sum(notes2_counter.values())
        
        # Common notes
        common_notes = set(notes1_counter.keys()) & set(notes2_counter.keys())
        notes_only_in_1 = set(notes1_counter.keys()) - set(notes2_counter.keys())
        notes_only_in_2 = set(notes2_counter.keys()) - set(notes1_counter.keys())
        
        # Calculate similarity percentage
        if total_notes1 == 0 or total_notes2 == 0:
            similarity = 0.0
        else:
            # Use Jaccard similarity for note sets
            jaccard_similarity = len(common_notes) / len(all_notes) if all_notes else 0
            
            # Calculate frequency similarity for common notes
            freq_similarity = 0.0
            if common_notes:
                for note in common_notes:
                    freq1 = notes1_counter[note] / total_notes1
                    freq2 = notes2_counter[note] / total_notes2
                    freq_similarity += 1 - abs(freq1 - freq2)
                freq_similarity /= len(common_notes)
            
            # Combined similarity (weighted average)
            similarity = (jaccard_similarity * 0.4 + freq_similarity * 0.6) * 100
        
        return {
            'similarity_percentage': round(similarity, 2),
            'total_notes_original': total_notes1,
            'total_notes_comparison': total_notes2,
            'common_notes': sorted(list(common_notes)),
            'common_notes_count': len(common_notes),
            'notes_only_in_original': sorted(list(notes_only_in_1)),
            'notes_only_in_comparison': sorted(list(notes_only_in_2)),
            'note_distribution_original': dict(notes1_counter.most_common()),
            'note_distribution_comparison': dict(notes2_counter.most_common())
        }
    
    def find_matching_notes(self, notes1: List[Dict], notes2: List[Dict]) -> Dict[str, Any]:
        """
        Find notes that match in both time and pitch between two songs.
        
        Args:
            notes1: Notes from original song
            notes2: Notes from comparison song
            
        Returns:
            Dictionary with matching and non-matching notes
        """
        matches = []
        unmatched_original = []
        unmatched_comparison = list(notes2)  # Start with all notes2
        
        for note1 in notes1:
            best_match = None
            best_match_idx = None
            min_time_diff = float('inf')
            
            # Find the closest matching note in time window
            for idx, note2 in enumerate(unmatched_comparison):
                time_diff = abs(note1['time'] - note2['time'])
                
                # Check if within time tolerance and same note
                if (time_diff <= self.time_tolerance and 
                    note1['full_note'] == note2['full_note'] and
                    time_diff < min_time_diff):
                    best_match = note2
                    best_match_idx = idx
                    min_time_diff = time_diff
            
            if best_match:
                matches.append({
                    'note': note1['full_note'],
                    'original_time': note1['time'],
                    'comparison_time': best_match['time'],
                    'time_difference': round(min_time_diff, 3),
                    'original_frequency': note1['frequency'],
                    'comparison_frequency': best_match['frequency'],
                    'frequency_difference_hz': round(abs(note1['frequency'] - best_match['frequency']), 2)
                })
                unmatched_comparison.pop(best_match_idx)
            else:
                unmatched_original.append({
                    'note': note1['full_note'],
                    'time': note1['time'],
                    'frequency': note1['frequency']
                })
        
        match_percentage = (len(matches) / len(notes1) * 100) if notes1 else 0
        
        return {
            'matching_notes': matches,
            'matching_notes_count': len(matches),
            'match_percentage': round(match_percentage, 2),
            'unmatched_in_original': unmatched_original,
            'unmatched_in_comparison': unmatched_comparison,
            'unmatched_original_count': len(unmatched_original),
            'unmatched_comparison_count': len(unmatched_comparison)
        }
    
    def analyze_timing_differences(self, matches: List[Dict]) -> Dict[str, Any]:
        """
        Analyze timing differences for matched notes.
        
        Args:
            matches: List of matched notes from find_matching_notes
            
        Returns:
            Statistics about timing differences
        """
        if not matches:
            return {
                'average_time_difference': 0.0,
                'max_time_difference': 0.0,
                'min_time_difference': 0.0,
                'std_time_difference': 0.0,
                'timing_accuracy_percentage': 0.0
            }
        
        time_diffs = [m['time_difference'] for m in matches]
        
        avg_diff = np.mean(time_diffs)
        max_diff = np.max(time_diffs)
        min_diff = np.min(time_diffs)
        std_diff = np.std(time_diffs)
        
        # Calculate timing accuracy (inverse of normalized difference)
        timing_accuracy = (1 - (avg_diff / self.time_tolerance)) * 100
        timing_accuracy = max(0, min(100, timing_accuracy))  # Clamp between 0-100
        
        return {
            'average_time_difference': round(avg_diff, 3),
            'max_time_difference': round(max_diff, 3),
            'min_time_difference': round(min_diff, 3),
            'std_time_difference': round(std_diff, 3),
            'timing_accuracy_percentage': round(timing_accuracy, 2)
        }
    
    def calculate_overall_score(self, comparison_results: Dict[str, Any]) -> Dict[str, float]:
        """
        Calculate an overall similarity score based on multiple factors.
        
        Args:
            comparison_results: Complete comparison results
            
        Returns:
            Dictionary with score breakdown
        """
        note_similarity = comparison_results['note_distribution']['similarity_percentage']
        match_percentage = comparison_results['note_matching']['match_percentage']
        timing_accuracy = comparison_results['timing_analysis']['timing_accuracy_percentage']
        
        # Weighted average (you can adjust weights)
        weights = {
            'note_similarity': 0.4,    # How similar are the notes used
            'match_percentage': 0.4,   # How many notes match in time
            'timing_accuracy': 0.2     # How accurate is the timing
        }
        
        overall_score = (
            note_similarity * weights['note_similarity'] +
            match_percentage * weights['match_percentage'] +
            timing_accuracy * weights['timing_accuracy']
        )
        
        return {
            'overall_similarity_score': round(overall_score, 2),
            'note_similarity_score': round(note_similarity, 2),
            'note_matching_score': round(match_percentage, 2),
            'timing_accuracy_score': round(timing_accuracy, 2),
            'grade': self._get_grade(overall_score)
        }
    
    def _get_grade(self, score: float) -> str:
        """Convert score to letter grade."""
        if score >= 90:
            return 'A (Excellent)'
        elif score >= 80:
            return 'B (Very Good)'
        elif score >= 70:
            return 'C (Good)'
        elif score >= 60:
            return 'D (Fair)'
        else:
            return 'F (Needs Improvement)'
    
    def compare_songs(self, original_json: str, comparison_json: str) -> Dict[str, Any]:
        """
        Complete comparison of two songs.
        
        Args:
            original_json: Path to original song's JSON analysis file
            comparison_json: Path to comparison song's JSON analysis file
            
        Returns:
            Complete comparison report
        """
        logger.info(f"Comparing songs: {original_json} vs {comparison_json}")
        
        # Load both songs
        original_data = self.load_song_data(original_json)
        comparison_data = self.load_song_data(comparison_json)
        
        # Extract notes
        notes1 = self.extract_notes(original_data)
        notes2 = self.extract_notes(comparison_data)
        
        if not notes1 or not notes2:
            raise ValueError("One or both songs have no notes detected")
        
        # Perform comparisons
        note_distribution = self.compare_note_distributions(notes1, notes2)
        note_matching = self.find_matching_notes(notes1, notes2)
        timing_analysis = self.analyze_timing_differences(note_matching['matching_notes'])
        
        # Compile results
        results = {
            'original_file': original_json,
            'comparison_file': comparison_json,
            'note_distribution': note_distribution,
            'note_matching': note_matching,
            'timing_analysis': timing_analysis
        }
        
        # Calculate overall score
        results['overall_score'] = self.calculate_overall_score(results)
        
        logger.info(f"Comparison complete. Overall score: {results['overall_score']['overall_similarity_score']}%")
        
        return results
    
    def generate_comparison_report(self, results: Dict[str, Any], output_path: str = None) -> str:
        """
        Generate a human-readable comparison report.
        
        Args:
            results: Comparison results from compare_songs
            output_path: Optional path to save the report
            
        Returns:
            Formatted report string
        """
        report_lines = [
            "=" * 80,
            "SONG COMPARISON REPORT",
            "=" * 80,
            "",
            f"Original Song: {results['original_file']}",
            f"Your Song: {results['comparison_file']}",
            "",
            "=" * 80,
            "OVERALL SCORE",
            "=" * 80,
            f"Overall Similarity: {results['overall_score']['overall_similarity_score']}%",
            f"Grade: {results['overall_score']['grade']}",
            "",
            f"  • Note Similarity: {results['overall_score']['note_similarity_score']}%",
            f"  • Note Matching: {results['overall_score']['note_matching_score']}%",
            f"  • Timing Accuracy: {results['overall_score']['timing_accuracy_score']}%",
            "",
            "=" * 80,
            "NOTE DISTRIBUTION ANALYSIS",
            "=" * 80,
            f"Original Song Total Notes: {results['note_distribution']['total_notes_original']}",
            f"Your Song Total Notes: {results['note_distribution']['total_notes_comparison']}",
            f"Common Notes: {results['note_distribution']['common_notes_count']} notes",
            f"  {', '.join(results['note_distribution']['common_notes'][:20])}{'...' if len(results['note_distribution']['common_notes']) > 20 else ''}",
            ""
        ]
        
        if results['note_distribution']['notes_only_in_original']:
            report_lines.extend([
                f"Notes in Original but NOT in Your Song ({len(results['note_distribution']['notes_only_in_original'])}): ",
                f"  {', '.join(results['note_distribution']['notes_only_in_original'])}",
                ""
            ])
        
        if results['note_distribution']['notes_only_in_comparison']:
            report_lines.extend([
                f"Extra Notes in Your Song ({len(results['note_distribution']['notes_only_in_comparison'])}): ",
                f"  {', '.join(results['note_distribution']['notes_only_in_comparison'])}",
                ""
            ])
        
        report_lines.extend([
            "=" * 80,
            "NOTE MATCHING ANALYSIS",
            "=" * 80,
            f"Matched Notes: {results['note_matching']['matching_notes_count']} / {results['note_distribution']['total_notes_original']} ({results['note_matching']['match_percentage']}%)",
            f"Unmatched in Original: {results['note_matching']['unmatched_original_count']}",
            f"Unmatched in Your Song: {results['note_matching']['unmatched_comparison_count']}",
            "",
            "=" * 80,
            "TIMING ANALYSIS",
            "=" * 80,
            f"Average Timing Difference: {results['timing_analysis']['average_time_difference']}s",
            f"Timing Accuracy: {results['timing_analysis']['timing_accuracy_percentage']}%",
            f"Max Time Difference: {results['timing_analysis']['max_time_difference']}s",
            f"Min Time Difference: {results['timing_analysis']['min_time_difference']}s",
            "",
        ])
        
        # Show sample of matching notes
        if results['note_matching']['matching_notes']:
            report_lines.extend([
                "=" * 80,
                "SAMPLE MATCHING NOTES (First 10)",
                "=" * 80,
            ])
            for i, match in enumerate(results['note_matching']['matching_notes'][:10], 1):
                report_lines.append(
                    f"{i}. {match['note']} @ {match['original_time']:.2f}s -> {match['comparison_time']:.2f}s "
                    f"(Δ {match['time_difference']}s, Δ {match['frequency_difference_hz']}Hz)"
                )
            report_lines.append("")
        
        # Show sample of unmatched notes
        if results['note_matching']['unmatched_in_original']:
            report_lines.extend([
                "=" * 80,
                "SAMPLE MISSING NOTES (First 10)",
                "=" * 80,
            ])
            for i, note in enumerate(results['note_matching']['unmatched_in_original'][:10], 1):
                report_lines.append(
                    f"{i}. {note['note']} @ {note['time']:.2f}s (MISSING in your song)"
                )
            report_lines.append("")
        
        report_lines.append("=" * 80)
        
        report = "\n".join(report_lines)
        
        if output_path:
            with open(output_path, 'w') as f:
                f.write(report)
            logger.info(f"Report saved to {output_path}")
        
        return report
