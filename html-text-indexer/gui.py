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
        self.root.title("HTML Text Indexer")
        self.root.geometry("1000x700")
        
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
        """Configure the UI style"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='#2c3e50')
        style.configure('Header.TLabel', font=('Arial', 11, 'bold'), foreground='#34495e')
        style.configure('Info.TLabel', font=('Arial', 9), foreground='#7f8c8d')
        style.configure('Run.TButton', font=('Arial', 10, 'bold'))
        
    def create_widgets(self):
        """Create all UI widgets"""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="HTML Text Indexer", style='Title.TLabel')
        title_label.grid(row=0, column=0, pady=(0, 10), sticky=tk.W)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Tab 1: Activities
        self.activities_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.activities_frame, text="Activities")
        self.create_activities_tab()
        
        # Tab 2: Configuration
        self.config_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.config_frame, text="Configuration")
        self.create_config_tab()
        
        # Tab 3: Batch Processing
        self.batch_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.batch_frame, text="Batch Processing")
        self.create_batch_tab()
        
        # Console/Log area
        console_label = ttk.Label(main_frame, text="Console Output:", style='Header.TLabel')
        console_label.grid(row=2, column=0, sticky=tk.W, pady=(10, 5))
        
        # Create console with scrollbar
        console_frame = ttk.Frame(main_frame)
        console_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        console_frame.columnconfigure(0, weight=1)
        console_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=2)
        
        self.console = scrolledtext.ScrolledText(
            console_frame, 
            height=15, 
            state='disabled',
            bg='#2c3e50',
            fg='#ecf0f1',
            font=('Consolas', 9),
            wrap=tk.WORD
        )
        self.console.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Redirect stdout to console
        sys.stdout = TextRedirector(self.console, "stdout")
        sys.stderr = TextRedirector(self.console, "stderr")
        
        # Control buttons at bottom
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=4, column=0, sticky=(tk.W, tk.E))
        
        self.clear_btn = ttk.Button(control_frame, text="Clear Console", command=self.clear_console)
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        self.run_all_btn = ttk.Button(control_frame, text="Run All Activities (1-11)", command=self.run_all_activities, style='Run.TButton')
        self.run_all_btn.pack(side=tk.LEFT, padx=5)
        
        self.clean_btn = ttk.Button(control_frame, text="Clean Folders", command=self.run_clean_folders)
        self.clean_btn.pack(side=tk.LEFT, padx=5)
        
        self.status_label = ttk.Label(control_frame, text="Ready", foreground='green')
        self.status_label.pack(side=tk.RIGHT, padx=5)
        
        # Welcome message
        self.log_message("Welcome to HTML Text Indexer!")
        self.log_message(f"Project directory: {self.script_dir}")
        self.log_message("Select an activity from the tabs above to begin.\n")
        
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
            ("Activity 9: Refine Dictionary", "Remove stop words and low-frequency terms", self.run_activity9),
            ("Activity 10: Weight Tokens", "Calculate TF.IDF weights for tokens", self.run_activity10),
            ("Activity 11: Document Index", "Create document index with unique IDs", self.run_activity11),
        ]
        
        # Create a canvas with scrollbar for activities
        canvas = tk.Canvas(self.activities_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.activities_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Add activities
        for i, (title, description, command) in enumerate(activities):
            frame = ttk.LabelFrame(scrollable_frame, text=title, padding="10")
            frame.grid(row=i, column=0, sticky=(tk.W, tk.E), pady=5, padx=5)
            
            desc_label = ttk.Label(frame, text=description, style='Info.TLabel')
            desc_label.pack(anchor=tk.W, pady=(0, 5))
            
            btn = ttk.Button(frame, text=f"Run Activity {i+1}", command=command, style='Run.TButton')
            btn.pack(anchor=tk.E)
        
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
    
    def log_message(self, message):
        """Add a message to the console"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.console.config(state='normal')
        self.console.insert(tk.END, f"[{timestamp}] {message}\n")
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
            self.status_label.config(text="Running...", foreground='orange')
        else:
            self.status_label.config(text="Ready", foreground='green')
    
    def run_in_thread(self, func, *args):
        """Run a function in a separate thread"""
        if self.is_running:
            messagebox.showwarning("Already Running", "An activity is already running. Please wait for it to complete.")
            return
        
        def wrapper():
            try:
                self.set_running(True)
                func(*args)
                self.log_message("✓ Activity completed successfully!\n")
            except Exception as e:
                self.log_message(f"✗ Error: {str(e)}\n")
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
                self.log_message("✓ All activities (1-11) completed successfully!")
                self.log_message("="*60 + "\n")
                
            except Exception as e:
                self.log_message(f"\n✗ Error running all activities: {str(e)}\n")
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
                self.log_message("✓ All selected activities completed successfully!")
                self.log_message("="*60 + "\n")
                
            except Exception as e:
                self.log_message(f"\n✗ Batch processing failed: {str(e)}\n")
                messagebox.showerror("Batch Error", f"Batch processing failed:\n{str(e)}")
            finally:
                self.set_running(False)
        
        thread = threading.Thread(target=batch_runner, daemon=True)
        thread.start()


def main():
    """Launch the GUI"""
    root = tk.Tk()
    app = HTMLTextIndexerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

