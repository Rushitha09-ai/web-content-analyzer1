"""
Test script to verify Milestone 1 functionality
"""
from backend.app import WebContentAnalyzer

def main():
    # Initialize the analyzer
    analyzer = WebContentAnalyzer()
    
    # Test URLs - one normal website and one that should fail security check
    test_urls = [
        "https://www.python.org",  # Should work
        "http://192.168.1.1"       # Should fail security check
    ]
    
    print("Testing Web Content Analyzer - Milestone 1\n")
    
    # Test single URL analysis
    print("Testing single URL analysis:")
    result = analyzer.analyze_url(test_urls[0])
    print(f"\nAnalyzing: {test_urls[0]}")
    print("Status:", result["status"])
    if result["status"] == "success":
        print("\nExtracted Content:")
        print("Title:", result["content"]["title"])
        print("\nMeta Description:", result["content"]["meta_description"])
        print("\nNumber of links found:", len(result["content"]["links"]))
        print("\nFirst 200 chars of main content:", result["content"]["main_content"][:200], "...")
    else:
        print("Error:", result.get("error"))
    
    # Test security check with private IP
    print("\nTesting security check with private IP:")
    result = analyzer.analyze_url(test_urls[1])
    print(f"\nAnalyzing: {test_urls[1]}")
    print("Status:", result["status"])
    print("Result:", result.get("error", "No error"))

if __name__ == "__main__":
    main()
