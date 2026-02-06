import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import os
import sys
import pandas as pd
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analysis.data_processor import DataProcessor
from analysis.ab_test_analyzer import ABTestAnalyzer
from visualization.plot_manager import PlotManager

class MainWindow:
    """Main application window for A/B Testing Desktop App."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("A/B Testing Analysis Tool")
        self.root.geometry("1200x800")
        
        # Initialize components
        self.data_processor = DataProcessor()
        self.ab_analyzer = ABTestAnalyzer(self.data_processor)
        self.plot_manager = PlotManager()
        
        # Setup UI
        self.setup_menu()
        self.setup_main_frame()
        self.setup_status_bar()
        
        # Bind close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_menu(self):
        """Create application menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Load Data...", command=self.load_data, accelerator="Ctrl+O")
        file_menu.add_command(label="Load Country Data...", command=self.load_country_data)
        file_menu.add_separator()
        file_menu.add_command(label="Export Results...", command=self.export_to_csv)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)
        
        # Analysis menu
        analysis_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Analysis", menu=analysis_menu)
        analysis_menu.add_command(label="Clean Data", command=self.clean_data)
        analysis_menu.add_command(label="Run A/B Test", command=self.run_ab_test)
        analysis_menu.add_command(label="Generate Report", command=self.generate_report)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
        # Keyboard shortcuts
        self.root.bind('<Control-o>', lambda e: self.load_data())
    
    def setup_main_frame(self):
        """Create main frame with notebook for tabs."""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_data_tab()
        self.create_probability_tab()
        self.create_ab_test_tab()
        self.create_visualization_tab()
        self.create_results_tab()
    
    def create_data_tab(self):
        """Create data management tab."""
        self.data_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.data_frame, text="Data")
        
        # Left panel - Data info
        left_frame = ttk.LabelFrame(self.data_frame, text="Data Information", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Data info text
        self.data_info_text = tk.Text(left_frame, height=15, width=50, wrap=tk.WORD)
        data_scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.data_info_text.yview)
        self.data_info_text.configure(yscrollcommand=data_scrollbar.set)
        
        self.data_info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        data_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Right panel - Controls
        right_frame = ttk.LabelFrame(self.data_frame, text="Controls", padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        
        ttk.Button(right_frame, text="Load Data", command=self.load_data).pack(pady=5, fill=tk.X)
        ttk.Button(right_frame, text="Load Country Data", command=self.load_country_data).pack(pady=5, fill=tk.X)
        ttk.Button(right_frame, text="Clean Data", command=self.clean_data).pack(pady=5, fill=tk.X)
        ttk.Button(right_frame, text="Show Preview", command=self.show_data_preview).pack(pady=5, fill=tk.X)
        
        # File path label
        ttk.Label(right_frame, text="Current File:").pack(pady=(20, 5))
        self.file_path_label = ttk.Label(right_frame, text="No file loaded", wraplength=200)
        self.file_path_label.pack(pady=5)
    
    def create_probability_tab(self):
        """Create probability analysis tab."""
        self.prob_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.prob_frame, text="Probability")
        
        # Create scrollable frame
        canvas = tk.Canvas(self.prob_frame)
        scrollbar = ttk.Scrollbar(self.prob_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Probability stats
        stats_frame = ttk.LabelFrame(scrollable_frame, text="Probability Statistics", padding=10)
        stats_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.prob_stats_text = tk.Text(stats_frame, height=20, width=80, wrap=tk.WORD)
        prob_scrollbar = ttk.Scrollbar(stats_frame, orient=tk.VERTICAL, command=self.prob_stats_text.yview)
        self.prob_stats_text.configure(yscrollcommand=prob_scrollbar.set)
        
        self.prob_stats_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        prob_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        ttk.Button(scrollable_frame, text="Calculate Statistics", 
                  command=self.calculate_probability_stats).pack(pady=10)
    
    def create_ab_test_tab(self):
        """Create A/B testing tab."""
        self.ab_test_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.ab_test_frame, text="A/B Test")
        
        # Top frame - Controls
        control_frame = ttk.LabelFrame(self.ab_test_frame, text="Test Controls", padding=10)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Simulation iterations
        ttk.Label(control_frame, text="Simulation Iterations:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.iterations_var = tk.StringVar(value="10000")
        ttk.Entry(control_frame, textvariable=self.iterations_var, width=10).grid(row=0, column=1, padx=5)
        
        ttk.Button(control_frame, text="Run Simulation", 
                  command=self.run_simulation_threaded).grid(row=0, column=2, padx=20)
        ttk.Button(control_frame, text="Run Z-Test", 
                  command=self.run_z_test_threaded).grid(row=0, column=3, padx=5)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(control_frame, variable=self.progress_var, 
                                          maximum=100, length=300)
        self.progress_bar.grid(row=1, column=0, columnspan=4, pady=10, sticky=tk.EW)
        
        # Middle frame - Results
        results_frame = ttk.LabelFrame(self.ab_test_frame, text="Test Results", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.ab_results_text = tk.Text(results_frame, height=15, wrap=tk.WORD)
        ab_scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.ab_results_text.yview)
        self.ab_results_text.configure(yscrollcommand=ab_scrollbar.set)
        
        self.ab_results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        ab_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_visualization_tab(self):
        """Create visualization tab."""
        self.viz_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.viz_frame, text="Visualizations")
        
        # Plot selection
        control_frame = ttk.Frame(self.viz_frame)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(control_frame, text="Simulation Histogram", 
                  command=self.show_simulation_plot).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Conversion Comparison", 
                  command=self.show_comparison_plot).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Save Plot", 
                  command=self.save_current_plot).pack(side=tk.LEFT, padx=5)
        
        # Plot display area
        self.plot_frame = ttk.Frame(self.viz_frame)
        self.plot_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    def create_results_tab(self):
        """Create results summary tab."""
        self.results_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.results_frame, text="Results")
        
        # Results text area
        results_text_frame = ttk.LabelFrame(self.results_frame, text="Analysis Summary", padding=10)
        results_text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.results_text = tk.Text(results_text_frame, height=25, wrap=tk.WORD)
        results_scrollbar = ttk.Scrollbar(results_text_frame, orient=tk.VERTICAL, 
                                         command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=results_scrollbar.set)
        
        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        results_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Export buttons
        button_frame = ttk.Frame(self.results_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="Generate Report", 
                  command=self.generate_report).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Export to CSV", 
                  command=self.export_to_csv).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Results", 
                  command=self.clear_results).pack(side=tk.LEFT, padx=5)
    
    def setup_status_bar(self):
        """Create status bar."""
        self.status_bar = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def load_data(self):
        """Load main data file."""
        filename = filedialog.askopenfilename(
            title="Load A/B Test Data",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if filename:
            self.update_status("Loading data...")
            if self.data_processor.load_data(filename):
                self.file_path_label.config(text=os.path.basename(filename))
                self.update_data_info()
                self.update_status(f"Data loaded: {len(self.data_processor.df)} rows")
            else:
                messagebox.showerror("Error", "Failed to load data:\n" + 
                                   "\n".join(self.data_processor.validation_errors))
                self.update_status("Error loading data")
    
    def load_country_data(self):
        """Load country data file."""
        filename = filedialog.askopenfilename(
            title="Load Country Data",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if filename:
            if self.data_processor.load_country_data(filename):
                self.update_status("Country data loaded successfully")
                messagebox.showinfo("Success", "Country data loaded and merged")
            else:
                messagebox.showerror("Error", "Failed to load country data:\n" + 
                                   "\n".join(self.data_processor.validation_errors))
    
    def clean_data(self):
        """Clean the loaded data."""
        if self.data_processor.df is None:
            messagebox.showwarning("Warning", "Please load data first")
            return
        
        success, message = self.data_processor.clean_data()
        if success:
            self.update_data_info()
            self.update_status("Data cleaned successfully")
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)
    
    def update_data_info(self):
        """Update data information display."""
        self.data_info_text.delete(1.0, tk.END)
        
        if self.data_processor.df is not None:
            info = self.data_processor.get_data_info()
            text = f"Dataset Shape: {info['shape']}\n"
            text += f"Unique Users: {info['unique_users']}\n"
            text += f"Columns: {', '.join(info['columns'])}\n\n"
            
            if self.data_processor.df is not None:
                misaligned = self.data_processor.get_misaligned_count()
                text += f"Misaligned Rows: {misaligned}\n\n"
            
            if self.data_processor.df_clean is not None:
                text += f"Cleaned Shape: {self.data_processor.df_clean.shape}\n"
                text += f"Cleaned Unique Users: {self.data_processor.df_clean['user_id'].nunique()}\n"
            
            self.data_info_text.insert(tk.END, text)
    
    def calculate_probability_stats(self):
        """Calculate and display probability statistics."""
        if self.data_processor.df_clean is None:
            messagebox.showwarning("Warning", "Please load and clean data first")
            return
        
        stats = self.data_processor.get_probability_stats()
        sizes = self.data_processor.get_sample_sizes()
        
        text = "PROBABILITY ANALYSIS RESULTS\n"
        text += "=" * 50 + "\n\n"
        
        text += f"Overall Conversion Rate: {stats['overall_conversion']:.6f}\n"
        text += f"Control Group Conversion Rate: {stats['control_conversion']:.6f}\n"
        text += f"Treatment Group Conversion Rate: {stats['treatment_conversion']:.6f}\n"
        text += f"Probability of New Page: {stats['new_page_prob']:.6f}\n\n"
        
        text += f"Sample Sizes:\n"
        text += f"  New Page: {sizes.get('n_new', 0)}\n"
        text += f"  Old Page: {sizes.get('n_old', 0)}\n"
        text += f"  Control: {sizes.get('n_control', 0)}\n"
        text += f"  Treatment: {sizes.get('n_treatment', 0)}\n\n"
        
        conversion_diff = stats['treatment_conversion'] - stats['control_conversion']
        text += f"Conversion Difference (Treatment - Control): {conversion_diff:.6f}\n\n"
        
        if abs(conversion_diff) < 0.001:
            text += "Observation: The difference between conversion rates is very small.\n"
            text += "Statistical testing is needed to determine significance."
        
        self.prob_stats_text.delete(1.0, tk.END)
        self.prob_stats_text.insert(tk.END, text)
    
    def run_simulation_threaded(self):
        """Run simulation in background thread."""
        if self.data_processor.df_clean is None:
            messagebox.showwarning("Warning", "Please load and clean data first")
            return
        
        try:
            iterations = int(self.iterations_var.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid number of iterations")
            return
        
        self.progress_var.set(0)
        self.update_status("Running simulation...")
        
        def run_simulation():
            try:
                results = self.ab_analyzer.run_simulation(iterations)
                self.root.after(0, self.display_simulation_results, results)
            except Exception as e:
                self.root.after(0, messagebox.showerror, "Error", f"Simulation failed: {str(e)}")
            finally:
                self.root.after(0, self.progress_var.set, 100)
                self.root.after(0, self.update_status, "Simulation complete")
        
        threading.Thread(target=run_simulation, daemon=True).start()
    
    def run_z_test_threaded(self):
        """Run z-test in background thread."""
        if self.data_processor.df_clean is None:
            messagebox.showwarning("Warning", "Please load and clean data first")
            return
        
        self.update_status("Running z-test...")
        
        def run_test():
            try:
                results = self.ab_analyzer.run_z_test()
                self.root.after(0, self.display_z_test_results, results)
            except Exception as e:
                self.root.after(0, messagebox.showerror, "Error", f"Z-test failed: {str(e)}")
            finally:
                self.root.after(0, self.update_status, "Z-test complete")
        
        threading.Thread(target=run_test, daemon=True).start()
    
    def display_simulation_results(self, results):
        """Display simulation results."""
        if 'error' in results:
            messagebox.showerror("Error", results['error'])
            return
        
        text = "SIMULATION RESULTS\n"
        text += "=" * 50 + "\n\n"
        text += f"Iterations: {results['n_iterations']:,}\n"
        text += f"Actual Difference: {results['actual_diff']:.6f}\n"
        text += f"P-value: {results['p_value']:.6f}\n\n"
        
        interpretation = self.ab_analyzer.get_interpretation()
        text += interpretation
        
        self.ab_results_text.delete(1.0, tk.END)
        self.ab_results_text.insert(tk.END, text)
    
    def display_z_test_results(self, results):
        """Display z-test results."""
        if 'error' in results:
            messagebox.showerror("Error", results['error'])
            return
        
        text = "Z-TEST RESULTS\n"
        text += "=" * 50 + "\n\n"
        text += f"Z-score: {results['z_score']:.6f}\n"
        text += f"P-value: {results['p_value']:.6f}\n"
        text += f"Critical Value: {results['critical_value']:.6f}\n"
        text += f"Z-significance: {results['z_significance']:.6f}\n\n"
        
        text += f"Conversions:\n"
        text += f"  New Page: {results['convert_new']:,} / {results['n_new']:,}\n"
        text += f"  Old Page: {results['convert_old']:,} / {results['n_old']:,}\n\n"
        
        interpretation = self.ab_analyzer.get_interpretation()
        text += interpretation
        
        self.ab_results_text.delete(1.0, tk.END)
        self.ab_results_text.insert(tk.END, text)
    
    def show_simulation_plot(self):
        """Show simulation histogram plot."""
        if self.ab_analyzer.simulation_results is None:
            messagebox.showwarning("Warning", "Please run simulation first")
            return
        
        # Clear previous plots
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        
        canvas = self.plot_manager.create_simulation_histogram(
            self.plot_frame, self.ab_analyzer.simulation_results)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def show_comparison_plot(self):
        """Show conversion comparison plot."""
        if self.data_processor.df_clean is None:
            messagebox.showwarning("Warning", "Please load and clean data first")
            return
        
        # Clear previous plots
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        
        stats = self.data_processor.get_probability_stats()
        canvas = self.plot_manager.create_conversion_comparison_chart(
            self.plot_frame, stats)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def save_current_plot(self):
        """Save current plot to file."""
        filename = filedialog.asksaveasfilename(
            title="Save Plot",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if filename:
            # Try to save the most recent plot
            if 'simulation' in self.plot_manager.figures:
                self.plot_manager.save_plot('simulation', filename)
                messagebox.showinfo("Success", f"Plot saved to {filename}")
            else:
                messagebox.showwarning("Warning", "No plot to save")
    
    def generate_report(self):
        """Generate comprehensive analysis report."""
        if self.data_processor.df_clean is None:
            messagebox.showwarning("Warning", "Please load and clean data first")
            return
        
        summary = self.ab_analyzer.get_summary_stats()
        
        text = "A/B TESTING ANALYSIS REPORT\n"
        text += "=" * 60 + "\n\n"
        
        text += "DATASET SUMMARY\n"
        text += "-" * 30 + "\n"
        text += f"Total Users: {summary['total_users']:,}\n"
        text += f"Unique Users: {summary['unique_users']:,}\n"
        text += f"New Page Sample Size: {summary['new_page_sample_size']:,}\n"
        text += f"Old Page Sample Size: {summary['old_page_sample_size']:,}\n\n"
        
        text += "CONVERSION ANALYSIS\n"
        text += "-" * 30 + "\n"
        text += f"Overall Conversion Rate: {summary['overall_conversion_rate']:.4f}\n"
        text += f"Control Conversion Rate: {summary['control_conversion_rate']:.4f}\n"
        text += f"Treatment Conversion Rate: {summary['treatment_conversion_rate']:.4f}\n"
        text += f"Conversion Difference: {summary['conversion_difference']:.6f}\n\n"
        
        if self.ab_analyzer.simulation_results:
            text += "SIMULATION RESULTS\n"
            text += "-" * 30 + "\n"
            text += f"P-value: {self.ab_analyzer.simulation_results['p_value']:.6f}\n"
            text += f"Actual Difference: {self.ab_analyzer.simulation_results['actual_diff']:.6f}\n\n"
        
        if self.ab_analyzer.z_test_results:
            text += "Z-TEST RESULTS\n"
            text += "-" * 30 + "\n"
            text += f"Z-score: {self.ab_analyzer.z_test_results['z_score']:.6f}\n"
            text += f"P-value: {self.ab_analyzer.z_test_results['p_value']:.6f}\n\n"
        
        text += "RECOMMENDATIONS\n"
        text += "-" * 30 + "\n"
        
        # Generate recommendation based on results
        if self.ab_analyzer.simulation_results:
            p_val = self.ab_analyzer.simulation_results['p_value']
            if p_val > 0.05:
                text += "• FAIL TO REJECT null hypothesis\n"
                text += "• New page does NOT show statistically significant improvement\n"
                text += "• RECOMMENDATION: Keep the old page\n"
            else:
                text += "• REJECT null hypothesis\n"
                text += "• New page shows statistically significant improvement\n"
                text += "• RECOMMENDATION: Implement the new page\n"
        else:
            text += "• Run statistical tests to get recommendations\n"
        
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, text)
        
        # Switch to results tab
        self.notebook.select(self.results_frame)
        self.update_status("Report generated")
    
    def export_to_csv(self):
        """Export results to CSV."""
        filename = filedialog.asksaveasfilename(
            title="Export Results",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                # Create summary dataframe
                summary = self.ab_analyzer.get_summary_stats()
                df = pd.DataFrame([summary])
                df.to_csv(filename, index=False)
                messagebox.showinfo("Success", f"Results exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Export failed: {str(e)}")
    
    def clear_results(self):
        """Clear all results."""
        self.results_text.delete(1.0, tk.END)
        self.ab_results_text.delete(1.0, tk.END)
        self.prob_stats_text.delete(1.0, tk.END)
        self.plot_manager.clear_all_plots()
        self.update_status("Results cleared")
    
    def show_data_preview(self):
        """Show preview of loaded data."""
        if self.data_processor.df is None:
            messagebox.showwarning("Warning", "Please load data first")
            return
        
        # Create preview window
        preview_window = tk.Toplevel(self.root)
        preview_window.title("Data Preview")
        preview_window.geometry("800x600")
        
        # Create treeview for data display
        tree_frame = ttk.Frame(preview_window)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Show first 100 rows
        preview_data = self.data_processor.df.head(100)
        
        # Create treeview
        tree = ttk.Treeview(tree_frame)
        
        # Configure columns
        tree["columns"] = list(preview_data.columns)
        for col in preview_data.columns:
            tree.column(col, width=100, anchor=tk.CENTER)
            tree.heading(col, text=col)
        
        # Add data
        for i, row in preview_data.iterrows():
            tree.insert("", tk.END, values=list(row))
        
        # Add scrollbars
        y_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        x_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=tree.xview)
        tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def run_ab_test(self):
        """Run A/B test (shortcut to simulation)."""
        self.run_simulation_threaded()
    
    def show_about(self):
        about_text = """A/B Testing Analysis Tool
        
Version 1.0

A comprehensive desktop application for analyzing A/B test results
using statistical methods and data visualization.

Features:
• Data loading and cleaning
• Probability analysis
• A/B testing with simulation
• Statistical hypothesis testing
• Interactive visualizations
• Comprehensive reporting

Built with Python, Tkinter, Pandas, and Matplotlib."""
        
        messagebox.showinfo("About", about_text)
    
    def update_status(self, message):
        """Update status bar."""
        self.status_bar.config(text=message)
        self.root.update_idletasks()
    
    def on_closing(self):
        """Handle application closing."""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.plot_manager.clear_all_plots()
            self.root.destroy()
    
    def run(self):
        """Start the application."""
        self.root.mainloop()

if __name__ == "__main__":
    app = MainWindow()
    app.run()
