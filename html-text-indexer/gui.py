"""
HTML Text Indexer - Graphical User Interface
A modern GUI for the HTML text processing and indexing system
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
from pathlib import Path
import threading
import sys
import io
from datetime import datetime
import importlib.util

# Import the activities from main.py
spec = importlib.util.spec_from_file_location("main", Path(__file__).parent / "main.py")
main_module = importlib.util.module_from_spec(spec)
sys.modules["main_activities"] = main_module
spec.loader.exec_module(main_module)


class TextRedirector(io.StringIO):
    """Redirect stdout/stderr to a text widget"""
    def __init__(self, widget, tag="stdout"):
        super().__init__()
        self.widget = widget
        self.tag = tag

    def write(self, str_text):
        self.widget.config(state='normal')
        self.widget.insert(tk.END, str_text, (self.tag,))
        self.widget.see(tk.END)
        self.widget.config(state='disabled')
        self.widget.update_idletasks()
    
    def flush(self):
        pass


class HTMLTextIndexerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("HTML Text Indexer - Professional Edition")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 600)
        
        # Modern color scheme
        self.colors = {
            'bg_primary': '#f5f7fa',
            'bg_secondary': '#ffffff',
            'bg_dark': '#2c3e50',
            'bg_console': '#1a1a1a',
            'accent': '#4a90e2',
            'accent_hover': '#357abd',
            'success': '#2ecc71',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'text_primary': '#2c3e50',
            'text_secondary': '#6c757d',
            'text_light': '#ffffff',
            'border': '#e1e8ed',
            'card_shadow': '#e8ecf0',
        }
        
        # Set background color
        self.root.configure(bg=self.colors['bg_primary'])
        
        # Get script directory for default paths
        self.script_dir = Path(__file__).parent
        self.html_sources_path = self.script_dir / "data" / "html_sources"
        self.results_path = self.script_dir / "results"
        self.stoplist_path = self.script_dir / "stoplist.txt"
        
        # Track running status
        self.is_running = False
        
        # Configure style
        self.setup_style()
        
        # Create UI
        self.create_widgets()
        
    def setup_style(self):
        """Configure the UI style with modern design"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure modern colors and fonts
        style.configure('Title.TLabel', 
                       font=('Segoe UI', 20, 'bold'), 
                       foreground=self.colors['text_primary'],
                       background=self.colors['bg_primary'])
        
        style.configure('Header.TLabel', 
                       font=('Segoe UI', 11, 'bold'), 
                       foreground=self.colors['text_primary'],
                       background=self.colors['bg_primary'])
        
        style.configure('Info.TLabel', 
                       font=('Segoe UI', 9), 
                       foreground=self.colors['text_secondary'],
                       background=self.colors['bg_primary'])
        
        style.configure('Run.TButton', 
                       font=('Segoe UI', 10, 'bold'),
                       padding=(15, 8))
        
        # Modern button styles
        style.configure('TButton',
                       font=('Segoe UI', 10),
                       padding=(12, 8),
                       relief='flat',
                       borderwidth=0)
        
        style.map('TButton',
                 background=[('active', self.colors['accent']),
                           ('!active', self.colors['bg_secondary'])],
                 foreground=[('active', self.colors['text_light']),
                            ('!active', self.colors['text_primary'])],
                 bordercolor=[('active', self.colors['accent']),
                            ('!active', self.colors['border'])],
                 focuscolor=[('!focus', 'none')])
        
        style.map('Run.TButton',
                 background=[('active', self.colors['accent_hover']),
                           ('!active', self.colors['accent'])],
                 foreground=[('active', self.colors['text_light']),
                            ('!active', self.colors['text_light'])],
                 bordercolor=[('active', self.colors['accent_hover']),
                            ('!active', self.colors['accent'])],
                 focuscolor=[('!focus', 'none')])
        
        # Notebook style
        style.configure('TNotebook',
                       background=self.colors['bg_primary'],
                       borderwidth=0)
        
        style.configure('TNotebook.Tab',
                       font=('Segoe UI', 11),
                       padding=(24, 12),
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['text_primary'],
                       borderwidth=0)
        
        style.map('TNotebook.Tab',
                 background=[('selected', self.colors['accent']),
                           ('!selected', self.colors['bg_secondary'])],
                 foreground=[('selected', self.colors['text_light']),
                           ('!selected', self.colors['text_primary'])],
                 expand=[('selected', [1, 1, 1, 0])])
        
        # LabelFrame style
        style.configure('TLabelframe',
                       background=self.colors['bg_secondary'],
                       borderwidth=1,
                       relief='solid',
                       bordercolor=self.colors['border'])
        
        style.configure('TLabelframe.Label',
                       font=('Segoe UI', 10, 'bold'),
                       foreground=self.colors['accent'],
                       background=self.colors['bg_secondary'])
        
        # Entry style
        style.configure('TEntry',
                       fieldbackground=self.colors['bg_secondary'],
                       borderwidth=1,
                       relief='solid',
                       bordercolor=self.colors['border'],
                       padding=5)
        
        # Scrollbar style
        style.configure('TScrollbar',
                       background=self.colors['bg_secondary'],
                       troughcolor=self.colors['bg_primary'],
                       borderwidth=0,
                       arrowcolor=self.colors['text_secondary'],
                       darkcolor=self.colors['border'],
                       lightcolor=self.colors['border'])
        
    def create_widgets(self):
        """Create all UI widgets with modern design"""
        # Header frame with modern design
        header_frame = tk.Frame(self.root, bg=self.colors['accent'], height=90)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Title in header
        title_label = tk.Label(
            header_frame, 
            text="HTML Text Indexer", 
            font=('Segoe UI', 24, 'bold'),
            bg=self.colors['accent'],
            fg=self.colors['text_light'],
            pady=20
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame,
            text="Professional Text Processing & Indexing System",
            font=('Segoe UI', 11),
            bg=self.colors['accent'],
            fg=self.colors['text_light']
        )
        subtitle_label.pack(pady=(0, 20))
        
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        main_frame.rowconfigure(0, weight=1)
        
        # Tab 1: Activities
        self.activities_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(self.activities_frame, text="Activities")
        self.create_activities_tab()
        
        # Tab 2: Configuration
        self.config_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(self.config_frame, text="Configuration")
        self.create_config_tab()
        
        # Tab 3: Batch Processing
        self.batch_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(self.batch_frame, text="Batch Processing")
        self.create_batch_tab()
        
        # Tab 4: Search (Activity 12)
        self.search_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(self.search_frame, text="Search (Activity 12)")
        self.create_search_tab()
        
        # Console/Log area with modern styling
        console_container = tk.Frame(main_frame, bg=self.colors['bg_primary'])
        console_container.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        console_container.columnconfigure(0, weight=1)
        console_container.rowconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=2)
        
        console_header = tk.Frame(console_container, bg=self.colors['accent'], height=40)
        console_header.grid(row=0, column=0, sticky=(tk.W, tk.E))
        console_header.pack_propagate(False)
        
        console_label = tk.Label(
            console_header,
            text="Console Output",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['accent'],
            fg=self.colors['text_light'],
            padx=10
        )
        console_label.pack(side=tk.LEFT, pady=7)
        
        # Create console with modern dark theme
        console_frame = tk.Frame(console_container, bg=self.colors['bg_console'])
        console_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        console_frame.columnconfigure(0, weight=1)
        console_frame.rowconfigure(0, weight=1)
        
        self.console = scrolledtext.ScrolledText(
            console_frame, 
            height=12, 
            state='disabled',
            bg=self.colors['bg_console'],
            fg='#e0e0e0',
            font=('Consolas', 10),
            wrap=tk.WORD,
            insertbackground='#ffffff',
            selectbackground=self.colors['accent'],
            selectforeground='#ffffff',
            borderwidth=0,
            highlightthickness=0,
            padx=12,
            pady=12
        )
        self.console.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure text tags for colored output
        self.console.tag_config("stdout", foreground='#e0e0e0')
        self.console.tag_config("stderr", foreground='#ff6b6b')
        self.console.tag_config("success", foreground='#51cf66')
        self.console.tag_config("error", foreground='#ff6b6b')
        
        # Redirect stdout to console
        sys.stdout = TextRedirector(self.console, "stdout")
        sys.stderr = TextRedirector(self.console, "stderr")
        
        # Control buttons at bottom with modern styling
        control_frame = tk.Frame(main_frame, bg=self.colors['bg_primary'])
        control_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))
        
        # Left side buttons
        left_buttons = tk.Frame(control_frame, bg=self.colors['bg_primary'])
        left_buttons.pack(side=tk.LEFT)
        
        self.clear_btn = ttk.Button(left_buttons, text="Clear Console", command=self.clear_console)
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        self.run_all_btn = ttk.Button(left_buttons, text="Run All (1-11)", command=self.run_all_activities, style='Run.TButton')
        self.run_all_btn.pack(side=tk.LEFT, padx=5)
        
        self.clean_btn = ttk.Button(left_buttons, text="Clean Folders", command=self.run_clean_folders)
        self.clean_btn.pack(side=tk.LEFT, padx=5)
        
        # Right side status
        right_status = tk.Frame(control_frame, bg=self.colors['bg_primary'])
        right_status.pack(side=tk.RIGHT)
        
        self.status_indicator = tk.Frame(right_status, bg=self.colors['success'], width=12, height=12, relief='flat')
        self.status_indicator.pack(side=tk.LEFT, padx=(0, 8), pady=3)
        
        self.status_label = tk.Label(
            right_status,
            text="Ready",
            font=('Segoe UI', 9, 'bold'),
            bg=self.colors['bg_primary'],
            fg=self.colors['success']
        )
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        # Welcome message with styling
        self.console.config(state='normal')
        self.console.insert(tk.END, "=" * 70 + "\n", "stdout")
        self.console.insert(tk.END, " " * 20 + "Welcome to HTML Text Indexer!" + " " * 20 + "\n", "success")
        self.console.insert(tk.END, "=" * 70 + "\n", "stdout")
        self.console.insert(tk.END, f"Project directory: {self.script_dir}\n", "stdout")
        self.console.insert(tk.END, "Select an activity from the tabs above to begin.\n\n", "stdout")
        self.console.config(state='disabled')
        
    def create_activities_tab(self):
        """Create the activities tab with individual activity buttons"""
        activities = [
            ("Activity 1: Open HTML Files", "Open and read HTML files, measure loading times", self.run_activity1),
            ("Activity 2: Clean HTML", "Remove HTML tags and extract clean text", self.run_activity2),
            ("Activity 3: Process Words", "Extract and sort words from cleaned text", self.run_activity3),
            ("Activity 4: Consolidate Words", "Create consolidated sorted word list", self.run_activity4),
            ("Activity 5: Tokenize", "Tokenize text files for indexing", self.run_activity5),
            ("Activity 6: Build Dictionary", "Create dictionary with document frequency", self.run_activity6),
            ("Activity 7: Dictionary & Posting", "Generate dictionary and posting lists", self.run_activity7),
            ("Activity 8: Hash Table Dictionary", "Build hash table-based dictionary", self.run_activity8),
            ("Activity 9: Refine Dictionary", "Remove stop words and filter tokens", self.run_activity9),
            ("Activity 10: Weight Tokens", "Calculate TF.IDF weights for tokens", self.run_activity10),
            ("Activity 11: Document Index", "Create document index with unique IDs", self.run_activity11),
            ("Activity 12: Search Dictionary", "Search for words in dictionary and posting files", self.run_activity12),
        ]
        
        # Create a canvas with scrollbar for activities
        canvas = tk.Canvas(self.activities_frame, highlightthickness=0, bg=self.colors['bg_primary'])
        scrollbar = ttk.Scrollbar(self.activities_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg_primary'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set, bg=self.colors['bg_primary'])
        
        # Add activities with modern card design
        for i, (title, description, command) in enumerate(activities):
            # Create card frame with modern shadow effect
            card_frame = tk.Frame(
                scrollable_frame,
                bg=self.colors['bg_secondary'],
                relief='flat',
                borderwidth=0,
                highlightbackground=self.colors['card_shadow'],
                highlightthickness=1
            )
            card_frame.grid(row=i, column=0, sticky=(tk.W, tk.E), pady=6, padx=8)
            card_frame.columnconfigure(1, weight=1)
            
            # Activity number badge with modern design
            badge = tk.Label(
                card_frame,
                text=str(i+1),
                font=('Segoe UI', 13, 'bold'),
                bg=self.colors['accent'],
                fg=self.colors['text_light'],
                width=3,
                height=1,
                padx=8,
                relief='flat'
            )
            badge.grid(row=0, column=0, rowspan=2, padx=18, pady=18, sticky='n')
            
            # Title and description
            content_frame = tk.Frame(card_frame, bg=self.colors['bg_secondary'])
            content_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 15), pady=15)
            content_frame.columnconfigure(0, weight=1)
            
            title_label = tk.Label(
                content_frame,
                text=title,
                font=('Segoe UI', 12, 'bold'),
                bg=self.colors['bg_secondary'],
                fg=self.colors['text_primary'],
                anchor='w'
            )
            title_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 6))
            
            desc_label = tk.Label(
                content_frame,
                text=description,
                font=('Segoe UI', 10),
                bg=self.colors['bg_secondary'],
                fg=self.colors['text_secondary'],
                anchor='w',
                wraplength=600
            )
            desc_label.grid(row=1, column=0, sticky=tk.W)
            
            # Run button
            btn = ttk.Button(
                card_frame,
                text="Run",
                command=command,
                style='Run.TButton'
            )
            btn.grid(row=0, column=2, rowspan=2, padx=15, pady=15, sticky='e')
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_config_tab(self):
        """Create the configuration tab"""
        # HTML Sources path
        ttk.Label(self.config_frame, text="HTML Sources Directory:", style='Header.TLabel').grid(
            row=0, column=0, sticky=tk.W, pady=(0, 5)
        )
        
        html_frame = ttk.Frame(self.config_frame)
        html_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        html_frame.columnconfigure(0, weight=1)
        
        self.html_path_var = tk.StringVar(value=str(self.html_sources_path))
        html_entry = ttk.Entry(html_frame, textvariable=self.html_path_var, width=60)
        html_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        html_browse = ttk.Button(html_frame, text="Browse...", command=self.browse_html_dir)
        html_browse.grid(row=0, column=1)
        
        # Results path
        ttk.Label(self.config_frame, text="Results Directory:", style='Header.TLabel').grid(
            row=2, column=0, sticky=tk.W, pady=(0, 5)
        )
        
        results_frame = ttk.Frame(self.config_frame)
        results_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        results_frame.columnconfigure(0, weight=1)
        
        self.results_path_var = tk.StringVar(value=str(self.results_path))
        results_entry = ttk.Entry(results_frame, textvariable=self.results_path_var, width=60)
        results_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        results_browse = ttk.Button(results_frame, text="Browse...", command=self.browse_results_dir)
        results_browse.grid(row=0, column=1)
        
        # Stoplist path
        ttk.Label(self.config_frame, text="Stoplist File:", style='Header.TLabel').grid(
            row=4, column=0, sticky=tk.W, pady=(0, 5)
        )
        
        stoplist_frame = ttk.Frame(self.config_frame)
        stoplist_frame.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        stoplist_frame.columnconfigure(0, weight=1)
        
        self.stoplist_path_var = tk.StringVar(value=str(self.stoplist_path))
        stoplist_entry = ttk.Entry(stoplist_frame, textvariable=self.stoplist_path_var, width=60)
        stoplist_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        stoplist_browse = ttk.Button(stoplist_frame, text="Browse...", command=self.browse_stoplist)
        stoplist_browse.grid(row=0, column=1)
        
        # Info
        info_text = """
Configuration Notes:
• HTML Sources: Directory containing the HTML files to process
• Results: Directory where all output files and reports will be saved
• Stoplist: Text file containing stop words (one per line) for filtering

Changes will be applied when you run activities.
        """
        info_label = ttk.Label(self.config_frame, text=info_text, style='Info.TLabel', justify=tk.LEFT)
        info_label.grid(row=6, column=0, sticky=tk.W, pady=(10, 0))
        
    def create_batch_tab(self):
        """Create the batch processing tab"""
        ttk.Label(
            self.batch_frame, 
            text="Run Multiple Activities", 
            style='Header.TLabel'
        ).grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        info_label = ttk.Label(
            self.batch_frame,
            text="Select which activities to run in sequence:",
            style='Info.TLabel'
        )
        info_label.grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
        
        # Checkboxes for activities
        self.batch_vars = []
        batch_activities = [
            "Activity 1: Open HTML Files",
            "Activity 2: Clean HTML",
            "Activity 3: Process Words",
            "Activity 4: Consolidate Words",
            "Activity 5: Tokenize",
            "Activity 6: Build Dictionary",
            "Activity 7: Dictionary & Posting",
            "Activity 8: Hash Table Dictionary",
            "Activity 9: Refine Dictionary",
            "Activity 10: Weight Tokens",
            "Activity 11: Document Index",
            "Activity 12: Search Dictionary",
        ]
        
        checkbox_frame = ttk.Frame(self.batch_frame)
        checkbox_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        for i, activity in enumerate(batch_activities):
            var = tk.BooleanVar(value=False)
            self.batch_vars.append(var)
            cb = ttk.Checkbutton(checkbox_frame, text=activity, variable=var)
            cb.grid(row=i, column=0, sticky=tk.W, pady=2)
        
        # Preset buttons
        preset_frame = ttk.Frame(self.batch_frame)
        preset_frame.grid(row=3, column=0, sticky=tk.W, pady=(0, 15))
        
        ttk.Button(preset_frame, text="Select All", command=self.select_all_activities).pack(side=tk.LEFT, padx=5)
        ttk.Button(preset_frame, text="Deselect All", command=self.deselect_all_activities).pack(side=tk.LEFT, padx=5)
        ttk.Button(preset_frame, text="Basic (1-4)", command=self.select_basic_activities).pack(side=tk.LEFT, padx=5)
        ttk.Button(preset_frame, text="Advanced (5-9)", command=self.select_advanced_activities).pack(side=tk.LEFT, padx=5)
        
        # Run button
        self.run_batch_btn = ttk.Button(
            self.batch_frame,
            text="Run Selected Activities",
            command=self.run_batch_activities,
            style='Run.TButton'
        )
        self.run_batch_btn.grid(row=4, column=0, pady=10)
        
    def browse_html_dir(self):
        """Browse for HTML sources directory"""
        directory = filedialog.askdirectory(initialdir=self.html_sources_path)
        if directory:
            self.html_path_var.set(directory)
            self.html_sources_path = Path(directory)
            
    def browse_results_dir(self):
        """Browse for results directory"""
        directory = filedialog.askdirectory(initialdir=self.results_path)
        if directory:
            self.results_path_var.set(directory)
            self.results_path = Path(directory)
            
    def browse_stoplist(self):
        """Browse for stoplist file"""
        filename = filedialog.askopenfilename(
            initialdir=self.stoplist_path.parent,
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.stoplist_path_var.set(filename)
            self.stoplist_path = Path(filename)
    
    def select_all_activities(self):
        for var in self.batch_vars:
            var.set(True)
    
    def deselect_all_activities(self):
        for var in self.batch_vars:
            var.set(False)
    
    def select_basic_activities(self):
        for i, var in enumerate(self.batch_vars):
            var.set(i < 4)
    
    def select_advanced_activities(self):
        for i, var in enumerate(self.batch_vars):
            var.set(i >= 4)
    
    def log_message(self, message, tag="stdout"):
        """Add a message to the console with optional tag for styling"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.console.config(state='normal')
        self.console.insert(tk.END, f"[{timestamp}] ", "stdout")
        self.console.insert(tk.END, f"{message}\n", tag)
        self.console.see(tk.END)
        self.console.config(state='disabled')
        
    def clear_console(self):
        """Clear the console"""
        self.console.config(state='normal')
        self.console.delete(1.0, tk.END)
        self.console.config(state='disabled')
        
    def set_running(self, running):
        """Update UI based on running state"""
        self.is_running = running
        if running:
            self.status_indicator.config(bg=self.colors['warning'])
            self.status_label.config(text="Running...", foreground=self.colors['warning'])
        else:
            self.status_indicator.config(bg=self.colors['success'])
            self.status_label.config(text="Ready", foreground=self.colors['success'])
    
    def run_in_thread(self, func, *args):
        """Run a function in a separate thread"""
        if self.is_running:
            messagebox.showwarning("Already Running", "An activity is already running. Please wait for it to complete.")
            return
        
        def wrapper():
            try:
                self.set_running(True)
                func(*args)
                self.log_message("Activity completed successfully!", "success")
            except Exception as e:
                self.log_message(f"Error: {str(e)}", "error")
                messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
            finally:
                self.set_running(False)
        
        thread = threading.Thread(target=wrapper, daemon=True)
        thread.start()
    
    # Activity runners
    def run_activity1(self):
        self.log_message("=== Starting Activity 1 ===")
        self.run_in_thread(main_module.actividad1)
    
    def run_activity2(self):
        self.log_message("=== Starting Activity 2 ===")
        self.run_in_thread(main_module.actividad2)
    
    def run_activity3(self):
        self.log_message("=== Starting Activity 3 ===")
        self.run_in_thread(main_module.actividad3)
    
    def run_activity4(self):
        self.log_message("=== Starting Activity 4 ===")
        self.run_in_thread(main_module.actividad4)
    
    def run_activity5(self):
        self.log_message("=== Starting Activity 5 ===")
        self.run_in_thread(main_module.actividad5, str(self.html_sources_path), str(self.results_path))
    
    def run_activity6(self):
        self.log_message("=== Starting Activity 6 ===")
        self.run_in_thread(main_module.actividad6, str(self.html_sources_path), str(self.results_path))
    
    def run_activity7(self):
        self.log_message("=== Starting Activity 7 ===")
        self.run_in_thread(main_module.actividad7, str(self.results_path))
    
    def run_activity8(self):
        self.log_message("=== Starting Activity 8 ===")
        self.run_in_thread(main_module.actividad8, str(self.results_path))
    
    def run_activity9(self):
        self.log_message("=== Starting Activity 9 ===")
        self.run_in_thread(main_module.actividad9, str(self.results_path), str(self.stoplist_path))
    
    def run_activity10(self):
        self.log_message("=== Starting Activity 10 ===")
        self.run_in_thread(main_module.actividad10, str(self.results_path))
    
    def run_activity11(self):
        self.log_message("=== Starting Activity 11 ===")
        self.run_in_thread(main_module.actividad11, str(self.results_path))
    
    def run_clean_folders(self):
        self.log_message("=== Cleaning Folders ===")
        self.run_in_thread(main_module.cleanFolders, True, True)
    
    def run_all_activities(self):
        """Run all activities sequentially (1-11)"""
        if self.is_running:
            messagebox.showwarning("Already Running", "An activity is already running. Please wait for it to complete.")
            return
        
        def all_activities_runner():
            try:
                self.set_running(True)
                self.log_message("=== Starting All Activities (1-11) ===\n")
                
                activity_funcs = [
                    lambda: main_module.actividad1(),
                    lambda: main_module.actividad2(),
                    lambda: main_module.actividad3(),
                    lambda: main_module.actividad4(),
                    lambda: main_module.actividad5(str(self.html_sources_path), str(self.results_path)),
                    lambda: main_module.actividad6(str(self.html_sources_path), str(self.results_path)),
                    lambda: main_module.actividad7(str(self.results_path)),
                    lambda: main_module.actividad8(str(self.results_path)),
                    lambda: main_module.actividad9(str(self.results_path), str(self.stoplist_path)),
                    lambda: main_module.actividad10(str(self.results_path)),
                    lambda: main_module.actividad11(str(self.results_path)),
                ]
                
                for i, activity_func in enumerate(activity_funcs, 1):
                    self.log_message(f"\n{'='*60}")
                    self.log_message(f"Running Activity {i}...")
                    self.log_message(f"{'='*60}\n")
                    activity_func()
                
                self.log_message("\n" + "="*60, "stdout")
                self.log_message("All activities (1-11) completed successfully!", "success")
                self.log_message("="*60 + "\n", "stdout")
                
            except Exception as e:
                self.log_message(f"\nError running all activities: {str(e)}", "error")
                messagebox.showerror("Error", f"Error running all activities:\n{str(e)}")
            finally:
                self.set_running(False)
        
        thread = threading.Thread(target=all_activities_runner, daemon=True)
        thread.start()
    
    def run_batch_activities(self):
        """Run selected activities in batch"""
        selected = [i for i, var in enumerate(self.batch_vars) if var.get()]
        
        if not selected:
            messagebox.showwarning("No Selection", "Please select at least one activity to run.")
            return
        
        def batch_runner():
            try:
                self.set_running(True)
                self.log_message(f"=== Starting Batch Processing ({len(selected)} activities) ===\n")
                
                activity_funcs = [
                    lambda: main_module.actividad1(),
                    lambda: main_module.actividad2(),
                    lambda: main_module.actividad3(),
                    lambda: main_module.actividad4(),
                    lambda: main_module.actividad5(str(self.html_sources_path), str(self.results_path)),
                    lambda: main_module.actividad6(str(self.html_sources_path), str(self.results_path)),
                    lambda: main_module.actividad7(str(self.results_path)),
                    lambda: main_module.actividad8(str(self.results_path)),
                    lambda: main_module.actividad9(str(self.results_path), str(self.stoplist_path)),
                    lambda: main_module.actividad10(str(self.results_path)),
                    lambda: main_module.actividad11(str(self.results_path)),
                ]
                
                for i in selected:
                    self.log_message(f"\n{'='*60}")
                    self.log_message(f"Running Activity {i+1}...")
                    self.log_message(f"{'='*60}\n")
                    activity_funcs[i]()
                
                self.log_message("\n" + "="*60, "stdout")
                self.log_message("All selected activities completed successfully!", "success")
                self.log_message("="*60 + "\n", "stdout")
                
            except Exception as e:
                self.log_message(f"\nBatch processing failed: {str(e)}", "error")
                messagebox.showerror("Batch Error", f"Batch processing failed:\n{str(e)}")
            finally:
                self.set_running(False)
        
        thread = threading.Thread(target=batch_runner, daemon=True)
        thread.start()
    
    def create_search_tab(self):
        """Create the search tab for Activity 12"""
        # Header
        header_label = ttk.Label(
            self.search_frame,
            text="Search in Dictionary (Activity 12)",
            style='Header.TLabel',
            font=('Segoe UI', 14, 'bold')
        )
        header_label.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        # Description
        desc_label = ttk.Label(
            self.search_frame,
            text="Enter a word to search in the dictionary and posting files. The word will be converted to lowercase to match the dictionary format.",
            style='Info.TLabel',
            wraplength=700
        )
        desc_label.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(0, 20))
        
        # Search options frame
        options_frame = ttk.LabelFrame(self.search_frame, text="Search Options", padding="15")
        options_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Dictionary version selection
        self.dict_version_var = tk.StringVar(value="no_stoplist")
        ttk.Radiobutton(
            options_frame,
            text="Full dictionary (without stoplist - Activity 8)",
            variable=self.dict_version_var,
            value="no_stoplist"
        ).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        ttk.Radiobutton(
            options_frame,
            text="Filtered dictionary (with stoplist - Activity 9)",
            variable=self.dict_version_var,
            value="with_stoplist"
        ).grid(row=1, column=0, sticky=tk.W, pady=5)
        
        # Search input frame
        search_input_frame = ttk.LabelFrame(self.search_frame, text="Search", padding="15")
        search_input_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        search_input_frame.columnconfigure(1, weight=1)
        
        ttk.Label(search_input_frame, text="Word to search:", style='Header.TLabel').grid(
            row=0, column=0, sticky=tk.W, padx=(0, 10)
        )
        
        self.search_entry = ttk.Entry(search_input_frame, width=40, font=('Segoe UI', 11))
        self.search_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        self.search_entry.bind('<Return>', lambda e: self.perform_search())
        
        self.search_btn = ttk.Button(
            search_input_frame,
            text="Search",
            command=self.perform_search,
            style='Run.TButton'
        )
        self.search_btn.grid(row=0, column=2)
        
        # Results frame
        results_frame = ttk.LabelFrame(self.search_frame, text="Search Results", padding="15")
        results_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(1, weight=1)
        self.search_frame.rowconfigure(4, weight=1)
        self.search_frame.columnconfigure(0, weight=1)
        
        # Results header
        self.results_header = ttk.Label(
            results_frame,
            text="Enter a word and click 'Search' to find documents",
            style='Info.TLabel'
        )
        self.results_header.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        # Results listbox with scrollbar
        listbox_frame = tk.Frame(results_frame, bg=self.colors['bg_secondary'])
        listbox_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        listbox_frame.columnconfigure(0, weight=1)
        listbox_frame.rowconfigure(0, weight=1)
        
        scrollbar_results = ttk.Scrollbar(listbox_frame)
        scrollbar_results.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        self.results_listbox = tk.Listbox(
            listbox_frame,
            font=('Consolas', 11),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            selectbackground=self.colors['accent'],
            selectforeground=self.colors['text_light'],
            yscrollcommand=scrollbar_results.set,
            borderwidth=1,
            relief='solid',
            highlightthickness=0
        )
        self.results_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar_results.config(command=self.results_listbox.yview)
    
    def perform_search(self):
        """Perform the search and display results"""
        word = self.search_entry.get().strip()
        
        if not word:
            messagebox.showwarning("Empty Search", "Please enter a word to search.")
            return
        
        # Determine which dictionary to use
        use_stoplist = (self.dict_version_var.get() == "with_stoplist")
        
        # Perform search
        try:
            documents = main_module.search_word(word, str(self.results_path), use_stoplist)
            
            # Clear previous results
            self.results_listbox.delete(0, tk.END)
            
            if documents:
                # Update header
                dict_type = "filtered (with stoplist)" if use_stoplist else "full (without stoplist)"
                self.results_header.config(
                    text=f"Found '{word}' in {len(documents)} document(s) using {dict_type} dictionary:"
                )
                
                # Add results
                for i, doc in enumerate(documents, 1):
                    self.results_listbox.insert(tk.END, f"{i}. {doc}")
                
                self.log_message(f"Search for '{word}': Found in {len(documents)} document(s)", "success")
            else:
                self.results_header.config(
                    text=f"Word '{word}' not found in the dictionary"
                )
                self.log_message(f"Search for '{word}': Not found", "stdout")
                
        except Exception as e:
            error_msg = f"Error during search: {str(e)}"
            self.log_message(error_msg, "error")
            messagebox.showerror("Search Error", error_msg)
    
    def run_activity12(self):
        """Open the search tab"""
        self.notebook.select(3)  # Switch to search tab (index 3)
        self.search_entry.focus()


def main():
    """Launch the GUI"""
    root = tk.Tk()
    app = HTMLTextIndexerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

