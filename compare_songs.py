#!/usr/bin/env python3
"""
Command-line tool for comparing two analyzed songs
"""

import sys
import os
import argparse
import json

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.song_comparator import SongComparator


def main():
    parser = argparse.ArgumentParser(
        description='Compare two analyzed songs to see how similar they are',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Compare two songs with default settings
  python compare_songs.py original.json my_song.json
  
  # Compare with custom time tolerance
  python compare_songs.py original.json my_song.json --tolerance 1.0
  
  # Save report to file
  python compare_songs.py original.json my_song.json --output report.txt
  
  # Save JSON results
  python compare_songs.py original.json my_song.json --json results.json
        """
    )
    
    parser.add_argument(
        'original',
        help='Path to original song JSON analysis file'
    )
    
    parser.add_argument(
        'comparison',
        help='Path to your song JSON analysis file'
    )
    
    parser.add_argument(
        '-t', '--tolerance',
        type=float,
        default=0.5,
        help='Time tolerance in seconds for matching notes (default: 0.5)'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Save text report to file'
    )
    
    parser.add_argument(
        '-j', '--json',
        help='Save JSON results to file'
    )
    
    args = parser.parse_args()
    
    # Validate files exist
    if not os.path.exists(args.original):
        print(f"❌ Error: Original file not found: {args.original}")
        sys.exit(1)
    
    if not os.path.exists(args.comparison):
        print(f"❌ Error: Comparison file not found: {args.comparison}")
        sys.exit(1)
    
    print("🔍 Starting song comparison...")
    print(f"   Original: {args.original}")
    print(f"   Your song: {args.comparison}")
    print(f"   Time tolerance: {args.tolerance}s")
    print()
    
    try:
        # Create comparator
        comparator = SongComparator(time_tolerance=args.tolerance)
        
        # Compare songs
        results = comparator.compare_songs(args.original, args.comparison)
        
        # Generate report
        report = comparator.generate_comparison_report(results)
        
        # Print report
        print(report)
        
        # Save to file if requested
        if args.output:
            with open(args.output, 'w') as f:
                f.write(report)
            print(f"\n✅ Text report saved to: {args.output}")
        
        # Save JSON if requested
        if args.json:
            with open(args.json, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"✅ JSON results saved to: {args.json}")
        
        # Exit with success
        sys.exit(0)
        
    except Exception as e:
        print(f"\n❌ Error during comparison: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
