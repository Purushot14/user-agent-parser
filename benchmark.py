#!/usr/bin/env python3
"""
Simple benchmark to demonstrate performance improvements in user-agent-parser.
"""

import time
from user_agent_parser import Parser, parse

# Sample user agent strings
test_user_agents = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/92.0.4515.90 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-N9810) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/16.0 Chrome/92.0.4515.166 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Mobile/15E148 Safari/604.1",
]

def benchmark_original_parsing(iterations=1000):
    """Benchmark original parsing approach."""
    start_time = time.time()
    for _ in range(iterations):
        for ua in test_user_agents:
            parser = Parser(ua)
            result = parser()  # Parse each time
    end_time = time.time()
    return end_time - start_time

def benchmark_cached_parsing(iterations=1000):
    """Benchmark cached parsing approach."""
    start_time = time.time()
    for _ in range(iterations):
        for ua in test_user_agents:
            result = parse(ua)  # Use cached function
    end_time = time.time()
    return end_time - start_time

def benchmark_repeated_cached_parsing(iterations=1000):
    """Benchmark repeated parsing of same user agents (cache hit scenario)."""
    start_time = time.time()
    for _ in range(iterations):
        for ua in test_user_agents:
            result = parse(ua)  # Repeated parsing, cache hits
    end_time = time.time()
    return end_time - start_time

if __name__ == "__main__":
    print("User-Agent Parser Performance Benchmark")
    print("=" * 40)
    
    # Warm up
    for ua in test_user_agents[:2]:
        Parser(ua)()
        parse(ua)
    
    iterations = 1000
    print(f"Running benchmarks with {iterations} iterations...")
    
    # Benchmark original parsing
    original_time = benchmark_original_parsing(iterations)
    print(f"Original parsing: {original_time:.4f}s")
    
    # Benchmark cached parsing (first run - cache misses)
    cached_time_first = benchmark_cached_parsing(iterations)
    print(f"Cached parsing (cache misses): {cached_time_first:.4f}s")
    
    # Benchmark cached parsing (repeated - cache hits)
    cached_time_repeated = benchmark_repeated_cached_parsing(iterations)
    print(f"Cached parsing (cache hits): {cached_time_repeated:.4f}s")
    
    print("\nPerformance Improvements:")
    print(f"Cached vs Original: {original_time / cached_time_first:.2f}x faster")
    print(f"Cache hits vs Original: {original_time / cached_time_repeated:.2f}x faster")
    
    # Test correctness
    print("\nCorrectness verification:")
    test_ua = test_user_agents[0]
    original_result = Parser(test_ua)()
    cached_result = parse(test_ua)
    
    print(f"Original: {original_result}")
    print(f"Cached:   {cached_result}")
    print(f"Results match: {original_result == cached_result}")