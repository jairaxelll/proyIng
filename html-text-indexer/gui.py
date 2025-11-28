"""
HTML Text Indexer - Graphical User Interface
A modern GUI for the HTML text processing and indexing system
Using CustomTkinter for a beautiful, modern interface
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
from pathlib import Path
import threading
import sys
import io
from datetime import datetime
import importlib.util

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")  # "light" or "dark"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"

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
        self.widget.configure(state='normal')
        self.widget.insert("end", str_text)
        self.widget.see("end")
        self.widget.configure(state='disabled')
        self.widget.update_idletasks()
    
    def flush(self):
        pass


class HTMLTextIndexerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("HTML Text Indexer - Professional Edition")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 700)
        
        # Get script directory for default paths
        self.script_dir = Path(__file__).parent
        self.html_sources_path = self.script_dir / "data" / "html_sources"
        self.results_path = self.script_dir / "results"
        self.stoplist_path = self.script_dir / "stoplist.txt"
        
        # Track running status
        self.is_running = False
        
        # Create UI
        self.create_widgets()
        
    def create_widgets(self):
        """Create all UI widgets with modern CustomTkinter design"""
        # Main container
        main_container = ctk.CTkFrame(self.root, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header frame
        header_frame = ctk.CTkFrame(main_container, height=100, corner_radius=15)
        header_frame.pack(fill="x", pady=(0, 15))
        header_frame.pack_propagate(False)
        
        # Title in header
        title_label = ctk.CTkLabel(
            header_frame, 
            text="HTML Text Indexer",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title_label.pack(pady=(15, 5))
        
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Professional Text Processing & Indexing System",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        subtitle_label.pack(pady=(0, 15))
        
        # Create tabview for tabs
        self.tabview = ctk.CTkTabview(main_container, corner_radius=15)
        self.tabview.pack(fill="both", expand=True, pady=(0, 15))
        
        # Tab 1: Activities
        self.tabview.add("Activities")
        self.create_activities_tab()
        
        # Tab 2: Configuration
        self.tabview.add("Configuration")
        self.create_config_tab()
        
        # Tab 3: Batch Processing
        self.tabview.add("Batch Processing")
        self.create_batch_tab()
        
        # Tab 4: Search (Activity 12)
        self.tabview.add("Search (Activity 12)")
        self.create_search_tab()
        
        # Console/Log area
        console_frame = ctk.CTkFrame(main_container, corner_radius=15)
        console_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Console header
        console_header = ctk.CTkFrame(console_frame, height=40, corner_radius=0, fg_color=("gray70", "gray30"))
        console_header.pack(fill="x", pady=(0, 0))
        
        console_label = ctk.CTkLabel(
            console_header,
            text="Console Output",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        console_label.pack(side="left", padx=15, pady=10)
        
        # Console textbox
        self.console = ctk.CTkTextbox(
            console_frame,
            font=ctk.CTkFont(family="Consolas", size=11),
            corner_radius=0,
            fg_color=("gray90", "gray17")
        )
        self.console.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Configure text tags for colored output (CTkTextbox uses different approach)
        # We'll use text color changes via insert with tags
        
        # Redirect stdout to console
        sys.stdout = TextRedirector(self.console, "stdout")
        sys.stderr = TextRedirector(self.console, "stderr")
        
        # Control buttons at bottom
        control_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        control_frame.pack(fill="x", pady=(0, 0))
        
        # Left side buttons
        left_buttons = ctk.CTkFrame(control_frame, fg_color="transparent")
        left_buttons.pack(side="left")
        
        self.clear_btn = ctk.CTkButton(
            left_buttons, 
            text="Clear Console", 
            command=self.clear_console,
            width=120,
            corner_radius=8
        )
        self.clear_btn.pack(side="left", padx=5)
        
        self.run_all_btn = ctk.CTkButton(
            left_buttons, 
            text="Run All (1-11)", 
            command=self.run_all_activities,
            width=140,
            corner_radius=8,
            fg_color=("gray75", "gray25"),
            hover_color=("gray70", "gray30")
        )
        self.run_all_btn.pack(side="left", padx=5)
        
        self.clean_btn = ctk.CTkButton(
            left_buttons, 
            text="Clean Folders", 
            command=self.run_clean_folders,
            width=120,
            corner_radius=8
        )
        self.clean_btn.pack(side="left", padx=5)
        
        # Right side status
        right_status = ctk.CTkFrame(control_frame, fg_color="transparent")
        right_status.pack(side="right")
        
        self.status_indicator = ctk.CTkFrame(
            right_status, 
            width=12, 
            height=12, 
            corner_radius=6,
            fg_color="#2ecc71"
        )
        self.status_indicator.pack(side="left", padx=(0, 8), pady=3)
        
        self.status_label = ctk.CTkLabel(
            right_status,
            text="Ready",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#2ecc71"
        )
        self.status_label.pack(side="left", padx=5)
        
        # Welcome message
        self.console.configure(state='normal')
        self.console.insert("end", "=" * 70 + "\n")
        self.console.insert("end", " " * 20 + "Welcome to HTML Text Indexer!" + " " * 20 + "\n")
        self.console.insert("end", "=" * 70 + "\n")
        self.console.insert("end", f"Project directory: {self.script_dir}\n")
        self.console.insert("end", "Select an activity from the tabs above to begin.\n\n")
        self.console.configure(state='disabled')
        
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
        
        # Scrollable frame for activities
        scrollable_frame = ctk.CTkScrollableFrame(self.tabview.tab("Activities"), corner_radius=0)
        scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add activities with modern card design
        for i, (title, description, command) in enumerate(activities):
            # Create card frame
            card_frame = ctk.CTkFrame(
                scrollable_frame,
                corner_radius=12,
                border_width=1,
                border_color=("gray80", "gray30")
            )
            card_frame.pack(fill="x", pady=8, padx=5)
            
            # Inner frame for content
            content_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
            content_frame.pack(fill="both", expand=True, padx=15, pady=15)
            
            # Activity number badge
            badge_frame = ctk.CTkFrame(
                content_frame,
                width=50,
                height=50,
                corner_radius=25,
                fg_color=("#3B82F6", "#1E40AF")
            )
            badge_frame.pack(side="left", padx=(0, 15))
            badge_frame.pack_propagate(False)
            
            badge_label = ctk.CTkLabel(
                badge_frame,
                text=str(i+1),
                font=ctk.CTkFont(size=18, weight="bold")
            )
            badge_label.pack(expand=True)
            
            # Title and description
            text_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
            text_frame.pack(side="left", fill="both", expand=True, padx=(0, 15))
            
            title_label = ctk.CTkLabel(
                text_frame,
                text=title,
                font=ctk.CTkFont(size=16, weight="bold"),
                anchor="w"
            )
            title_label.pack(anchor="w", pady=(0, 5))
            
            desc_label = ctk.CTkLabel(
                text_frame,
                text=description,
                font=ctk.CTkFont(size=13),
                text_color="gray",
                anchor="w",
                justify="left"
            )
            desc_label.pack(anchor="w")
            
            # Run button
            btn = ctk.CTkButton(
                content_frame,
                text="Run",
                command=command,
                width=100,
                height=35,
                corner_radius=8,
                fg_color=("#3B82F6", "#1E40AF"),
                hover_color=("#2563EB", "#1E3A8A")
            )
            btn.pack(side="right", padx=(10, 0))
        
    def create_config_tab(self):
        """Create the configuration tab"""
        config_scroll = ctk.CTkScrollableFrame(self.tabview.tab("Configuration"), corner_radius=0)
        config_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        # HTML Sources path
        ctk.CTkLabel(
            config_scroll, 
            text="HTML Sources Directory:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", pady=(10, 5))
        
        html_frame = ctk.CTkFrame(config_scroll, fg_color="transparent")
        html_frame.pack(fill="x", pady=(0, 15))
        
        self.html_path_var = ctk.StringVar(value=str(self.html_sources_path))
        html_entry = ctk.CTkEntry(
            html_frame, 
            textvariable=self.html_path_var, 
            width=500,
            height=35,
            corner_radius=8
        )
        html_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        html_browse = ctk.CTkButton(
            html_frame, 
            text="Browse...", 
            command=self.browse_html_dir,
            width=100,
            corner_radius=8
        )
        html_browse.pack(side="right")
        
        # Results path
        ctk.CTkLabel(
            config_scroll, 
            text="Results Directory:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", pady=(10, 5))
        
        results_frame = ctk.CTkFrame(config_scroll, fg_color="transparent")
        results_frame.pack(fill="x", pady=(0, 15))
        
        self.results_path_var = ctk.StringVar(value=str(self.results_path))
        results_entry = ctk.CTkEntry(
            results_frame, 
            textvariable=self.results_path_var, 
            width=500,
            height=35,
            corner_radius=8
        )
        results_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        results_browse = ctk.CTkButton(
            results_frame, 
            text="Browse...", 
            command=self.browse_results_dir,
            width=100,
            corner_radius=8
        )
        results_browse.pack(side="right")
        
        # Stoplist path
        ctk.CTkLabel(
            config_scroll, 
            text="Stoplist File:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", pady=(10, 5))
        
        stoplist_frame = ctk.CTkFrame(config_scroll, fg_color="transparent")
        stoplist_frame.pack(fill="x", pady=(0, 15))
        
        self.stoplist_path_var = ctk.StringVar(value=str(self.stoplist_path))
        stoplist_entry = ctk.CTkEntry(
            stoplist_frame, 
            textvariable=self.stoplist_path_var, 
            width=500,
            height=35,
            corner_radius=8
        )
        stoplist_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        stoplist_browse = ctk.CTkButton(
            stoplist_frame, 
            text="Browse...", 
            command=self.browse_stoplist,
            width=100,
            corner_radius=8
        )
        stoplist_browse.pack(side="right")
        
        # Info
        info_text = """Configuration Notes:
• HTML Sources: Directory containing the HTML files to process
• Results: Directory where all output files and reports will be saved
• Stoplist: Text file containing stop words (one per line) for filtering

Changes will be applied when you run activities."""
        
        info_label = ctk.CTkLabel(
            config_scroll, 
            text=info_text, 
            font=ctk.CTkFont(size=12),
            text_color="gray",
            justify="left",
            anchor="w"
        )
        info_label.pack(anchor="w", pady=(20, 10))
        
    def create_batch_tab(self):
        """Create the batch processing tab"""
        batch_scroll = ctk.CTkScrollableFrame(self.tabview.tab("Batch Processing"), corner_radius=0)
        batch_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(
            batch_scroll, 
            text="Run Multiple Activities",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(anchor="w", pady=(10, 5))
        
        ctk.CTkLabel(
            batch_scroll,
            text="Select which activities to run in sequence:",
            font=ctk.CTkFont(size=13),
            text_color="gray"
        ).pack(anchor="w", pady=(0, 15))
        
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
        
        checkbox_frame = ctk.CTkFrame(batch_scroll, fg_color="transparent")
        checkbox_frame.pack(fill="x", pady=(0, 15))
        
        for i, activity in enumerate(batch_activities):
            var = ctk.BooleanVar(value=False)
            self.batch_vars.append(var)
            cb = ctk.CTkCheckBox(
                checkbox_frame, 
                text=activity, 
                variable=var,
                font=ctk.CTkFont(size=13)
            )
            cb.pack(anchor="w", pady=5)
        
        # Preset buttons
        preset_frame = ctk.CTkFrame(batch_scroll, fg_color="transparent")
        preset_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkButton(
            preset_frame, 
            text="Select All", 
            command=self.select_all_activities,
            width=120,
            corner_radius=8
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            preset_frame, 
            text="Deselect All", 
            command=self.deselect_all_activities,
            width=120,
            corner_radius=8
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            preset_frame, 
            text="Basic (1-4)", 
            command=self.select_basic_activities,
            width=120,
            corner_radius=8
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            preset_frame, 
            text="Advanced (5-9)", 
            command=self.select_advanced_activities,
            width=120,
            corner_radius=8
        ).pack(side="left", padx=5)
        
        # Run button
        self.run_batch_btn = ctk.CTkButton(
            batch_scroll,
            text="Run Selected Activities",
            command=self.run_batch_activities,
            width=200,
            height=40,
            corner_radius=8,
            fg_color=("#3B82F6", "#1E40AF"),
            hover_color=("#2563EB", "#1E3A8A"),
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.run_batch_btn.pack(pady=20)
        
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
        self.console.configure(state='normal')
        self.console.insert("end", f"[{timestamp}] {message}\n")
        self.console.see("end")
        self.console.configure(state='disabled')
        
    def clear_console(self):
        """Clear the console"""
        self.console.configure(state='normal')
        self.console.delete("1.0", "end")
        self.console.configure(state='disabled')
        
    def set_running(self, running):
        """Update UI based on running state"""
        self.is_running = running
        if running:
            self.status_indicator.configure(fg_color="#f39c12")
            self.status_label.configure(text="Running...", text_color="#f39c12")
        else:
            self.status_indicator.configure(fg_color="#2ecc71")
            self.status_label.configure(text="Ready", text_color="#2ecc71")
    
    def run_in_thread(self, func, *args):
        """Run a function in a separate thread"""
        if self.is_running:
            messagebox.showwarning("Already Running", "An activity is already running. Please wait for it to complete.")
            return
        
        def wrapper():
            try:
                self.set_running(True)
                func(*args)
                self.log_message("Activity completed successfully!")
            except Exception as e:
                self.log_message(f"Error: {str(e)}")
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
                
                self.log_message("\n" + "="*60)
                self.log_message("All activities (1-11) completed successfully!")
                self.log_message("="*60 + "\n")
                
            except Exception as e:
                self.log_message(f"\nError running all activities: {str(e)}")
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
                
                self.log_message("\n" + "="*60)
                self.log_message("All selected activities completed successfully!")
                self.log_message("="*60 + "\n")
                
            except Exception as e:
                self.log_message(f"\nBatch processing failed: {str(e)}")
                messagebox.showerror("Batch Error", f"Batch processing failed:\n{str(e)}")
            finally:
                self.set_running(False)
        
        thread = threading.Thread(target=batch_runner, daemon=True)
        thread.start()
    
    def create_search_tab(self):
        """Create the search tab for Activity 12"""
        search_scroll = ctk.CTkScrollableFrame(self.tabview.tab("Search (Activity 12)"), corner_radius=0)
        search_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header
        header_label = ctk.CTkLabel(
            search_scroll,
            text="Search in Dictionary (Activity 12)",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        header_label.pack(anchor="w", pady=(10, 10))
        
        # Description
        desc_label = ctk.CTkLabel(
            search_scroll,
            text="Enter a word to search in the dictionary and posting files. The word will be converted to lowercase to match the dictionary format.",
            font=ctk.CTkFont(size=13),
            text_color="gray",
            justify="left",
            anchor="w",
            wraplength=800
        )
        desc_label.pack(anchor="w", pady=(0, 20))
        
        # Search options frame
        options_frame = ctk.CTkFrame(search_scroll, corner_radius=12)
        options_frame.pack(fill="x", pady=(0, 15), padx=5)
        
        ctk.CTkLabel(
            options_frame,
            text="Search Options",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=15, pady=(15, 10))
        
        # Dictionary version selection
        self.dict_version_var = ctk.StringVar(value="no_stoplist")
        
        radio_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
        radio_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        ctk.CTkRadioButton(
            radio_frame,
            text="Full dictionary (without stoplist - Activity 8)",
            variable=self.dict_version_var,
            value="no_stoplist",
            font=ctk.CTkFont(size=13)
        ).pack(anchor="w", pady=5)
        
        ctk.CTkRadioButton(
            radio_frame,
            text="Filtered dictionary (with stoplist - Activity 9)",
            variable=self.dict_version_var,
            value="with_stoplist",
            font=ctk.CTkFont(size=13)
        ).pack(anchor="w", pady=5)
        
        # Results limit selection
        limit_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
        limit_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        ctk.CTkLabel(
            limit_frame,
            text="Results limit:",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(side="left", padx=(0, 10))
        
        self.results_limit_var = ctk.StringVar(value="20")
        
        limit_options_frame = ctk.CTkFrame(limit_frame, fg_color="transparent")
        limit_options_frame.pack(side="left")
        
        ctk.CTkRadioButton(
            limit_options_frame,
            text="5",
            variable=self.results_limit_var,
            value="5",
            font=ctk.CTkFont(size=13)
        ).pack(side="left", padx=(0, 15))
        
        ctk.CTkRadioButton(
            limit_options_frame,
            text="10",
            variable=self.results_limit_var,
            value="10",
            font=ctk.CTkFont(size=13)
        ).pack(side="left", padx=(0, 15))
        
        ctk.CTkRadioButton(
            limit_options_frame,
            text="20",
            variable=self.results_limit_var,
            value="20",
            font=ctk.CTkFont(size=13)
        ).pack(side="left")
        
        # Search input frame
        search_input_frame = ctk.CTkFrame(search_scroll, corner_radius=12)
        search_input_frame.pack(fill="x", pady=(0, 15), padx=5)
        
        ctk.CTkLabel(
            search_input_frame,
            text="Search",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=15, pady=(15, 10))
        
        input_inner_frame = ctk.CTkFrame(search_input_frame, fg_color="transparent")
        input_inner_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        ctk.CTkLabel(
            input_inner_frame, 
            text="Word to search:",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(side="left", padx=(0, 10))
        
        self.search_entry = ctk.CTkEntry(
            input_inner_frame, 
            width=400,
            height=35,
            corner_radius=8,
            font=ctk.CTkFont(size=13)
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.search_entry.bind('<Return>', lambda e: self.perform_search())
        
        self.search_btn = ctk.CTkButton(
            input_inner_frame,
            text="Search",
            command=self.perform_search,
            width=120,
            height=35,
            corner_radius=8,
            fg_color=("#3B82F6", "#1E40AF"),
            hover_color=("#2563EB", "#1E3A8A"),
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.search_btn.pack(side="right")
        
        # Results frame
        results_frame = ctk.CTkFrame(search_scroll, corner_radius=12)
        results_frame.pack(fill="both", expand=True, pady=(0, 10), padx=5)
        
        ctk.CTkLabel(
            results_frame,
            text="Search Results",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=15, pady=(15, 10))
        
        # Results header
        self.results_header = ctk.CTkLabel(
            results_frame,
            text="Enter a word and click 'Search' to find documents",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.results_header.pack(anchor="w", padx=15, pady=(0, 10))
        
        # Results textbox (scrollable)
        self.results_textbox = ctk.CTkTextbox(
            results_frame,
            font=ctk.CTkFont(family="Consolas", size=14),
            corner_radius=8,
            height=400,
            fg_color=("gray90", "gray20")
        )
        self.results_textbox.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        self.results_textbox.configure(state='disabled')  # Start disabled
    
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
            
            # Get the results limit
            limit = int(self.results_limit_var.get())
            
            # Apply limit to results
            total_documents = len(documents)
            limited_documents = documents[:limit]
            
            # Clear previous results
            self.results_textbox.configure(state='normal')
            self.results_textbox.delete("1.0", "end")
            
            if documents:
                # Update header
                dict_type = "filtered (with stoplist)" if use_stoplist else "full (without stoplist)"
                if total_documents > limit:
                    self.results_header.configure(
                        text=f"Found '{word}' in {total_documents} document(s) using {dict_type} dictionary (showing first {limit}):"
                    )
                else:
                    self.results_header.configure(
                        text=f"Found '{word}' in {total_documents} document(s) using {dict_type} dictionary:"
                    )
                
                # Add results with better formatting
                results_text = ""
                for i, doc in enumerate(limited_documents, 1):
                    results_text += f"{i}. {doc}\n"
                
                # Add note if results were limited
                if total_documents > limit:
                    results_text += f"\n... and {total_documents - limit} more document(s) (limit: {limit} results)\n"
                
                # Insert results
                self.results_textbox.insert("1.0", results_text)
                self.results_textbox.see("1.0")  # Scroll to top
                self.results_textbox.update_idletasks()  # Force update
                
                # Also log the documents found in console
                self.log_message(f"Search for '{word}': Found in {total_documents} document(s) (showing {len(limited_documents)})")
                self.log_message("Documents found:")
                for i, doc in enumerate(limited_documents, 1):
                    self.log_message(f"  {i}. {doc}")
                if total_documents > limit:
                    self.log_message(f"  ... and {total_documents - limit} more document(s) (limit: {limit} results)")
            else:
                self.results_header.configure(
                    text=f"Word '{word}' not found in the dictionary"
                )
                # Show message in textbox too
                self.results_textbox.insert("1.0", f"No documents found containing '{word}'.\n\nPlease try:\n- Checking the spelling\n- Using a different dictionary (with/without stoplist)\n- Searching for a different word")
                self.log_message(f"Search for '{word}': Not found")
            
            # Ensure textbox is updated and visible
            self.results_textbox.configure(state='disabled')
            self.results_textbox.update_idletasks()
            self.root.update_idletasks()
                
        except Exception as e:
            error_msg = f"Error during search: {str(e)}"
            self.log_message(error_msg)
            import traceback
            self.log_message(traceback.format_exc())
            messagebox.showerror("Search Error", error_msg)
    
    def run_activity12(self):
        """Open the search tab"""
        self.tabview.set("Search (Activity 12)")
        self.search_entry.focus()


def main():
    """Launch the GUI"""
    root = ctk.CTk()
    app = HTMLTextIndexerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
