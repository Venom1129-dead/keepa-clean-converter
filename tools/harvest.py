#!/usr/bin/env python3
"""
Automated Research Harvester
Pulls transcripts from YouTube URLs and clean Markdown from web articles.
Outputs into: 01_Research/dumps/
"""

import sys
import os
import re
import urllib.request
from urllib.parse import urlparse, parse_qs
from datetime import datetime

DUMP_DIR = os.path.join(os.path.dirname(__file__), "..", "01_Research", "dumps")
INBOX_FILE = os.path.join(os.path.dirname(__file__), "..", "01_Research", "inbox_urls.txt")

os.makedirs(DUMP_DIR, exist_ok=True)

def extract_youtube_id(url):
    parsed = urlparse(url)
    if parsed.hostname in ('youtu.be', 'www.youtu.be'):
        return parsed.path[1:]
    if parsed.hostname in ('youtube.com', 'www.youtube.com'):
        if parsed.path == '/watch':
            return parse_qs(parsed.query).get('v', [None])[0]
        if parsed.path.startswith(('/embed/', '/v/')):
            return parsed.path.split('/')[2]
    return None

def harvest_youtube(video_id, url):
    print(f"[*] Processing YouTube Video ID: {video_id}")
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = " ".join([item['text'] for item in transcript_list])
        
        output_path = os.path.join(DUMP_DIR, f"yt_{video_id}.md")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"# YouTube Transcript: {video_id}\n")
            f.write(f"- Source URL: {url}\n")
            f.write(f"- Harvested At: {datetime.now().isoformat()}\n\n")
            f.write("## Full Transcript\n\n")
            f.write(full_text)
        print(f"[+] Successfully saved transcript to: {output_path}")
        return True
    except ImportError:
        print("[!] youtube_transcript_api not installed. Run: pip install youtube-transcript-api")
        return False
    except Exception as e:
        print(f"[-] Failed to fetch transcript for {video_id}: {e}")
        return False

def harvest_webpage(url):
    print(f"[*] Processing Webpage: {url}")
    try:
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8', errors='ignore')
            
        # Clean basic HTML tags to plain text
        clean_text = re.sub(r'<script.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
        clean_text = re.sub(r'<style.*?</style>', '', clean_text, flags=re.DOTALL | re.IGNORECASE)
        clean_text = re.sub(r'<[^>]+>', ' ', clean_text)
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        
        domain = urlparse(url).netloc.replace(':', '_')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(DUMP_DIR, f"web_{domain}_{timestamp}.md")
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"# Web Extract: {url}\n")
            f.write(f"- Harvested At: {datetime.now().isoformat()}\n\n")
            f.write("## Extracted Content\n\n")
            f.write(clean_text[:15000]) # First 15k chars
            
        print(f"[+] Successfully saved web extract to: {output_path}")
        return True
    except Exception as e:
        print(f"[-] Failed to fetch webpage {url}: {e}")
        return False

def main():
    if not os.path.exists(INBOX_FILE):
        print(f"[!] Inbox file not found: {INBOX_FILE}")
        return

    with open(INBOX_FILE, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    if not lines:
        print("[i] No URLs found in inbox_urls.txt. Add some links first!")
        return

    print(f"[*] Found {len(lines)} URLs to process...\n")
    for url in lines:
        video_id = extract_youtube_id(url)
        if video_id:
            harvest_youtube(video_id, url)
        else:
            harvest_webpage(url)

    print("\n[+] Harvest complete! Output files are located in 01_Research/dumps/")

if __name__ == "__main__":
    main()
