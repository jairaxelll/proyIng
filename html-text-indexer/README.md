# HTML Text Indexer

An HTML text processing and indexing system that extracts, cleans, tokenizes, and indexes text content from HTML files.

## Requirements

- Python 3.7 or higher
- tkinter (usually included with Python)
- No external dependencies required!

### Installing tkinter (if not already installed)

**Windows & macOS:** tkinter is usually included with Python

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install python3-tk
```

**Linux (Fedora):**
```bash
sudo dnf install python3-tkinter
```

## Quick Start

### Option 1: Web Application (CGI-BIN)

1. **Set up a web server** (Apache recommended)
2. **Configure CGI** (see `CGI_README.md` for detailed instructions)
3. **Access the web interface:**
   ```
   http://localhost/html-text-indexer/cgi-bin/index.cgi
   ```
4. **Run activities** through the web browser

See `CGI_README.md` for complete setup instructions.

### Option 2: Desktop GUI

1. **Clone or download the project**
2. **Launch the GUI:**
   - **Windows:** Double-click `launch_gui.bat`
   - **Linux/Mac:** Run `./launch_gui.sh` or `python3 gui.py`
   - **Any OS:** Run `python main.py --gui`
3. **Select an activity** from the Activities tab
4. **Click "Run Activity"** and watch the console output
5. **Check the results** in the `results/` folder

## Project Structure

```
html-text-indexer/
├── main.py                 # Main script with all activities
├── gui.py                  # Graphical user interface
├── launch_gui.bat          # Windows GUI launcher
├── launch_gui.sh           # Linux/Mac GUI launcher
├── README.md               # This file
├── CGI_README.md           # CGI web application setup guide
├── stoplist.txt            # Stop words for text filtering
├── cgi-bin/                # CGI web application scripts
│   ├── index.cgi          # Main web page
│   ├── activities.cgi      # Activities interface
│   ├── run_activity.cgi   # Activity runner
│   ├── search.cgi         # Search interface
│   └── config.cgi         # Configuration page
├── static/                 # Web application static files
│   ├── style.css          # Stylesheet
│   └── script.js          # JavaScript
├── data/                   # Input and processed data
│   ├── html_sources/       # Original HTML files (505 files)
│   ├── extracted_text/     # Cleaned text files
│   └── sorted_words/       # Word frequency files
└── results/                # Output files and reports
    ├── reports/            # Activity execution reports
    │   ├── activity_1_file_opening.txt
    │   ├── activity_2_html_cleaning.txt
    │   ├── activity_3_word_processing.txt
    │   ├── activity_4_sorting.txt
    │   ├── activity_5_consolidate.txt
    │   ├── activity_6_matricula.txt
    │   ├── activity_7_dictionary_posting.txt
    │   ├── activity_8_<matricula>.txt
    │   └── activity_9_<matricula>.txt
    ├── dictionary_posting/ # Dictionary and posting lists
    │   ├── Diccionario.txt
    │   └── Posting.txt
    ├── tokenized/          # Tokenized text files
    └── [various result files]
```

## Activities

The system performs 9 main activities:

1. **Activity 1**: Open and read HTML files
2. **Activity 2**: Remove HTML tags and clean text
3. **Activity 3**: Extract and process words
4. **Activity 4**: Create consolidated sorted word lists
5. **Activity 5**: Tokenize text files
6. **Activity 6**: Build dictionary with document frequency
7. **Activity 7**: Create dictionary and posting lists
8. **Activity 8**: Build hash table-based dictionary
9. **Activity 9**: Refine dictionary (remove stop words and low-frequency terms)

## Usage

### Web Application (CGI-BIN) - Recommended for Servers

Access the web interface through your browser:
```
http://localhost/html-text-indexer/cgi-bin/index.cgi
```

The web application provides:
- 🌐 Browser-based interface (no installation needed)
- ✨ Individual activity controls with descriptions
- 🔍 Search functionality for indexed documents
- 📊 Real-time activity execution and results
- 🎛️ Configuration management
- 📦 Batch processing (run multiple activities)
- 🎨 Modern, responsive design

See `CGI_README.md` for setup instructions.

### Desktop GUI

Launch the GUI for an easy-to-use desktop interface:
```bash
python main.py --gui
```

Or run the GUI directly:
```bash
python gui.py
```

The GUI provides:
- Individual activity controls with descriptions
- Real-time console output
- Configuration management (paths, settings)
- Batch processing (run multiple activities)
- Modern, intuitive interface

### Command Line Interface

Run all activities sequentially:
```bash
python main.py
```




Run specific activities:
```bash
python main.py --activity 1    # Run Activity 1
python main.py --activity 5    # Run Activity 5
# ... etc (1-9)
```

For tokenization and dictionary creation:
```bash
python main.py <input_dir> <output_dir> --mode actividad5
```

## Features

- Multi-encoding support (UTF-8, Latin-1, CP1252)
- Spanish text processing with accent support
- Hash table-based indexing
- Stop word filtering
- Frequency-based term filtering
- Comprehensive timing and performance reports

