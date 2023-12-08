from remi import start
from window import PDFReader

if __name__ == "__main__":
    start(PDFReader, debug=True, address='0.0.0.0', port=8081, start_browser=True, multiple_instance=True)
