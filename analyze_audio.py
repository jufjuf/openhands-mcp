import sys
import json

def main():
    input_data = sys.stdin.read()
    # Simulate audio analysis
    result = {
        "transcript": "Hello, this is a test transcription.",
        "summary": "Test audio about AI."
    }
    print(json.dumps(result))

if __name__ == "__main__":
    main()
