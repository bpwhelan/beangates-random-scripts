#!/usr/bin/env python3
"""
SRT Characters Per Hour Calculator for Japanese Text

This script analyzes SRT subtitle files to calculate the reading speed
in Japanese characters per hour, filtering out punctuation and non-Japanese text.
"""

import re
import sys
import argparse
from datetime import datetime, timedelta
from typing import List, Tuple


def parse_srt_time(time_str: str) -> timedelta:
    """Parse SRT timestamp format (HH:MM:SS,mmm) to timedelta."""
    # Replace comma with dot for milliseconds
    time_str = time_str.replace(',', '.')
    
    # Parse the time string
    time_obj = datetime.strptime(time_str, '%H:%M:%S.%f')
    
    # Convert to timedelta
    return timedelta(
        hours=time_obj.hour,
        minutes=time_obj.minute,
        seconds=time_obj.second,
        microseconds=time_obj.microsecond
    )


def filter_japanese_text(text: str) -> str:
    """
    Filter text to keep only Japanese characters (Hiragana, Katakana, Kanji).
    Removes punctuation, numbers, Latin characters, text in parentheses, and other non-Japanese text.
    """
    # First, remove text inside parentheses (including the parentheses themselves)
    # This removes sound effects, speaker names, etc.
    text = re.sub(r'\([^)]*\)', '', text)
    
    # Japanese character ranges:
    # Hiragana: U+3040-U+309F
    # Katakana: U+30A0-U+30FF
    # CJK Unified Ideographs (Kanji): U+4E00-U+9FAF
    # CJK Extension A: U+3400-U+4DBF
    # Additional common Japanese punctuation that we want to keep for context but not count
    
    japanese_pattern = re.compile(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF\u3400-\u4DBF]')
    
    # Extract only Japanese characters
    japanese_chars = japanese_pattern.findall(text)
    
    return ''.join(japanese_chars)


def parse_srt_file(filepath: str) -> List[Tuple[timedelta, timedelta, str]]:
    """
    Parse SRT file and return list of (start_time, end_time, text) tuples.
    """
    subtitles = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
    except UnicodeDecodeError:
        # Try with different encodings if UTF-8 fails
        try:
            with open(filepath, 'r', encoding='shift_jis') as file:
                content = file.read()
        except UnicodeDecodeError:
            with open(filepath, 'r', encoding='cp932') as file:
                content = file.read()
    
    # Split into subtitle blocks
    blocks = content.strip().split('\n\n')
    
    for block in blocks:
        lines = block.strip().split('\n')
        
        if len(lines) < 3:
            continue
            
        # Skip the subtitle number (first line)
        # Parse timing (second line)
        timing_line = lines[1]
        
        # Extract start and end times
        time_match = re.match(r'(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})', timing_line)
        
        if not time_match:
            continue
            
        start_time = parse_srt_time(time_match.group(1))
        end_time = parse_srt_time(time_match.group(2))
        
        # Combine all text lines (third line onwards)
        text = ' '.join(lines[2:])
        
        # Remove HTML tags if present
        text = re.sub(r'<[^>]+>', '', text)
        
        subtitles.append((start_time, end_time, text))
    
    return subtitles


def calculate_chars_per_hour(subtitles: List[Tuple[timedelta, timedelta, str]]) -> dict:
    """
    Calculate characters per hour from parsed subtitles.
    Returns a dictionary with statistics.
    """
    total_japanese_chars = 0
    total_duration = timedelta()
    subtitle_count = 0
    
    for start_time, end_time, text in subtitles:
        # Filter to Japanese characters only
        japanese_text = filter_japanese_text(text)
        char_count = len(japanese_text)
        
        # Calculate duration for this subtitle
        duration = end_time - start_time
        
        total_japanese_chars += char_count
        total_duration += duration
        subtitle_count += 1
        
        if char_count > 0:  # Only print non-empty subtitles for debugging
            print(f"Subtitle: '{text}' -> '{japanese_text}' ({char_count} chars, {duration.total_seconds():.1f}s)")
    
    # Calculate characters per hour
    total_hours = total_duration.total_seconds() / 3600
    
    if total_hours == 0:
        chars_per_hour = 0
    else:
        chars_per_hour = total_japanese_chars / total_hours
    
    # Calculate video duration (from first to last subtitle)
    if subtitles:
        video_start = subtitles[0][0]
        video_end = max(end_time for _, end_time, _ in subtitles)
        video_duration = video_end - video_start
        video_hours = video_duration.total_seconds() / 3600
        chars_per_video_hour = total_japanese_chars / video_hours if video_hours > 0 else 0
    else:
        video_duration = timedelta()
        video_hours = 0
        chars_per_video_hour = 0
    
    return {
        'total_japanese_chars': total_japanese_chars,
        'total_subtitle_duration': total_duration,
        'total_subtitle_hours': total_hours,
        'video_duration': video_duration,
        'video_hours': video_hours,
        'subtitle_count': subtitle_count,
        'chars_per_hour_subtitle_time': chars_per_hour,
        'chars_per_hour_video_time': chars_per_video_hour
    }


def main():
    parser = argparse.ArgumentParser(description='Calculate Japanese characters per hour from SRT files')
    parser.add_argument('srt_file', help='Path to the SRT file')
    parser.add_argument('-v', '--verbose', action='store_true', help='Show detailed output')
    
    args = parser.parse_args()
    
    try:
        # Parse the SRT file
        print(f"Parsing SRT file: {args.srt_file}")
        subtitles = parse_srt_file(args.srt_file)
        
        if not subtitles:
            print("No subtitles found in the file!")
            return
        
        print(f"Found {len(subtitles)} subtitles")
        
        # Calculate statistics
        stats = calculate_chars_per_hour(subtitles)
        
        # Display results
        print("\n" + "="*50)
        print("JAPANESE CHARACTERS PER HOUR ANALYSIS")
        print("="*50)
        print(f"Total Japanese characters: {stats['total_japanese_chars']:,}")
        print(f"Number of subtitles: {stats['subtitle_count']:,}")
        print(f"Total subtitle duration: {str(stats['total_subtitle_duration']).split('.')[0]}")
        print(f"Video duration: {str(stats['video_duration']).split('.')[0]}")
        print()
        print(f"Characters per hour (subtitle time): {stats['chars_per_hour_subtitle_time']:.0f}")
        print(f"Characters per hour (video time): {stats['chars_per_hour_video_time']:.0f}")
        print()
        
        # Additional metrics
        if stats['total_japanese_chars'] > 0:
            avg_chars_per_subtitle = stats['total_japanese_chars'] / stats['subtitle_count']
            print(f"Average characters per subtitle: {avg_chars_per_subtitle:.1f}")
            
        if stats['total_subtitle_hours'] > 0:
            reading_speed_per_min = stats['chars_per_hour_subtitle_time'] / 60
            print(f"Reading speed: {reading_speed_per_min:.0f} characters per minute")
        
    except FileNotFoundError:
        print(f"Error: File '{args.srt_file}' not found!")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing file: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()