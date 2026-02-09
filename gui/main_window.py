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
from utils.translator import Translator

class MainWindow:
    """Main application window for A/B Testing Desktop App."""
    
    def __init__(self):
        self.root = tk.Tk()
        
        # Initialize translator first
        self.translator = Translator()
        
        # Setup window title (will be updated when language changes)
        self.update_window_title()
        self.root.geometry("1200x800")
        
        # Initialize components
        self.data_processor = DataProcessor()
        self.ab_analyzer = ABTestAnalyzer(self.data_processor)
        self.plot_manager = PlotManager(self.translator)
        
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
        menubar.add_cascade(label=self.translator.t('menu_file'), menu=file_menu)
        file_menu.add_command(label=self.translator.t('menu_load_data'), command=self.load_data, accelerator="Ctrl+O")
        file_menu.add_command(label=self.translator.t('menu_load_country_data'), command=self.load_country_data)
        file_menu.add_separator()
        file_menu.add_command(label=self.translator.t('menu_export_results'), command=self.export_to_csv)
        file_menu.add_separator()
        file_menu.add_command(label=self.translator.t('menu_exit'), command=self.on_closing)
        
        # Analysis menu
        analysis_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.translator.t('menu_analysis'), menu=analysis_menu)
        analysis_menu.add_command(label=self.translator.t('menu_clean_data'), command=self.clean_data)
        analysis_menu.add_command(label=self.translator.t('menu_run_ab_test'), command=self.run_ab_test)
        analysis_menu.add_command(label=self.translator.t('menu_generate_report'), command=self.generate_report)
        
        # Language menu
        language_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.translator.t('menu_language'), menu=language_menu)
        language_menu.add_command(label=self.translator.t('menu_switch_to_russian'), command=lambda: self.switch_language('ru'))
        language_menu.add_command(label=self.translator.t('menu_switch_to_english'), command=lambda: self.switch_language('en'))
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.translator.t('menu_help'), menu=help_menu)
        help_menu.add_command(label=self.translator.t('menu_about'), command=self.show_about)
        
        # Store menu references for language switching
        self.menubar = menubar
        self.file_menu = file_menu
        self.analysis_menu = analysis_menu
        self.language_menu = language_menu
        self.help_menu = help_menu
        
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
        
        # Store notebook reference for language switching
        self.notebook_ref = self.notebook
    
    def switch_language(self, language):
        """Switch application language and update all UI elements."""
        if self.translator.switch_language(language):
            self.update_window_title()
            self.update_menu_texts()
            self.update_tab_texts()
            self.refresh_all_text_content()
            self.update_status(self.translator.t('status_ready'))
    
    def refresh_all_text_content(self):
        """Refresh all text content when language changes."""
        # Refresh data info if data is loaded
        if self.data_processor.df is not None:
            self.update_data_info()
        
        # Refresh probability stats if calculated
        if self.data_processor.df_clean is not None:
            # Check if probability stats have been calculated
            if self.prob_stats_text.get(1.0, tk.END).strip():
                self.calculate_probability_stats()
        
        # Refresh A/B test results if available
        if self.ab_analyzer.simulation_results is not None:
            self.display_simulation_results(self.ab_analyzer.simulation_results)
        
        if self.ab_analyzer.z_test_results is not None:
            self.display_z_test_results(self.ab_analyzer.z_test_results)
        
        # Refresh plots if they exist
        if hasattr(self.plot_manager, 'figures') and self.plot_manager.figures:
            # Recreate plots with new language
            if 'simulation' in self.plot_manager.figures and self.ab_analyzer.simulation_results:
                self.show_simulation_plot()
            elif 'comparison' in self.plot_manager.figures and self.data_processor.df_clean is not None:
                stats = self.data_processor.get_probability_stats()
                self.show_comparison_plot()
        
        # Refresh report if generated
        if self.results_text.get(1.0, tk.END).strip():
            self.generate_report()
    
    def update_window_title(self):
        """Update window title with current language."""
        self.root.title(self.translator.t('window_title'))
    
    def update_menu_texts(self):
        """Update all menu texts with current language."""
        # Clear and recreate menus
        self.setup_menu()
    
    def update_tab_texts(self):
        """Update all tab texts with current language."""
        # Update tab texts
        tabs = [
            (self.data_frame, 'tab_data'),
            (self.prob_frame, 'tab_probability'),
            (self.ab_test_frame, 'tab_ab_test'),
            (self.viz_frame, 'tab_visualizations'),
            (self.results_frame, 'tab_results')
        ]
        
        for i, (tab, key) in enumerate(tabs):
            self.notebook_ref.tab(i, text=self.translator.t(key))
        
        # Update tab content
        self.update_data_tab_content()
        self.update_probability_tab_content()
        self.update_ab_test_tab_content()
        self.update_visualization_tab_content()
        self.update_results_tab_content()
    
    def update_data_tab_content(self):
        """Update data tab content with current language."""
        # Update LabelFrame texts
        for widget in self.data_frame.winfo_children():
            if isinstance(widget, ttk.LabelFrame):
                # Get the current text to identify which frame this is
                current_text = widget.cget('text')
                if 'Data Information' in current_text or 'Информация о данных' in current_text:
                    widget.configure(text=self.translator.t('data_information'))
                elif 'Controls' in current_text or 'Управление' in current_text:
                    widget.configure(text=self.translator.t('controls'))
        
        # Update button texts and labels
        for widget in self.data_frame.winfo_children():
            if isinstance(widget, ttk.LabelFrame):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Button):
                        text = child.cget('text')
                        if 'Load Data' in text or 'Загрузить данные' in text:
                            child.configure(text=self.translator.t('btn_load_data'))
                        elif 'Load Country Data' in text or 'Загрузить страны' in text or 'Загрузить данные о странах' in text:
                            child.configure(text=self.translator.t('btn_load_country_data'))
                        elif 'Clean Data' in text or 'Очистить данные' in text:
                            child.configure(text=self.translator.t('btn_clean_data'))
                        elif 'Show Preview' in text or 'Показать' in text:
                            child.configure(text=self.translator.t('btn_show_preview'))
                    elif isinstance(child, ttk.Label):
                        text = child.cget('text')
                        if 'Current File' in text or 'Текущий файл' in text:
                            child.configure(text=self.translator.t('current_file'))
                        elif 'No file loaded' in text or 'Файл не загружен' in text:
                            child.configure(text=self.translator.t('no_file_loaded'))
    
    def update_probability_tab_content(self):
        """Update probability tab content with current language."""
        # Similar implementation for probability tab
        pass
    
    def update_ab_test_tab_content(self):
        """Update A/B test tab content with current language."""
        # Similar implementation for A/B test tab
        pass
    
    def update_visualization_tab_content(self):
        """Update visualization tab content with current language."""
        # Similar implementation for visualization tab
        pass
    
    def update_results_tab_content(self):
        """Update results tab content with current language."""
        # Similar implementation for results tab
        pass
    
    def create_data_tab(self):
        """Create data management tab."""
        self.data_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.data_frame, text=self.translator.t('tab_data'))
        
        # Left panel - Data info
        left_frame = ttk.LabelFrame(self.data_frame, text=self.translator.t('data_information'), padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Data info text
        self.data_info_text = tk.Text(left_frame, height=15, width=50, wrap=tk.WORD)
        data_scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.data_info_text.yview)
        self.data_info_text.configure(yscrollcommand=data_scrollbar.set)
        
        self.data_info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        data_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Right panel - Controls
        right_frame = ttk.LabelFrame(self.data_frame, text=self.translator.t('controls'), padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        
        ttk.Button(right_frame, text=self.translator.t('btn_load_data'), command=self.load_data).pack(pady=5, fill=tk.X)
        ttk.Button(right_frame, text=self.translator.t('btn_load_country_data'), command=self.load_country_data).pack(pady=5, fill=tk.X)
        ttk.Button(right_frame, text=self.translator.t('btn_clean_data'), command=self.clean_data).pack(pady=5, fill=tk.X)
        ttk.Button(right_frame, text=self.translator.t('btn_show_preview'), command=self.show_data_preview).pack(pady=5, fill=tk.X)
        
        # File path label
        ttk.Label(right_frame, text=self.translator.t('current_file')).pack(pady=(20, 5))
        self.file_path_label = ttk.Label(right_frame, text=self.translator.t('no_file_loaded'), wraplength=200)
        self.file_path_label.pack(pady=5)
    
    def create_probability_tab(self):
        """Create probability analysis tab."""
        self.prob_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.prob_frame, text=self.translator.t('tab_probability'))
        
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
        stats_frame = ttk.LabelFrame(scrollable_frame, text=self.translator.t('probability_statistics'), padding=10)
        stats_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.prob_stats_text = tk.Text(stats_frame, height=20, width=80, wrap=tk.WORD)
        prob_scrollbar = ttk.Scrollbar(stats_frame, orient=tk.VERTICAL, command=self.prob_stats_text.yview)
        self.prob_stats_text.configure(yscrollcommand=prob_scrollbar.set)
        
        self.prob_stats_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        prob_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        ttk.Button(scrollable_frame, text=self.translator.t('btn_calculate_statistics'), 
                  command=self.calculate_probability_stats).pack(pady=10)
    
    def create_ab_test_tab(self):
        """Create A/B testing tab."""
        self.ab_test_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.ab_test_frame, text=self.translator.t('tab_ab_test'))
        
        # Top frame - Controls
        control_frame = ttk.LabelFrame(self.ab_test_frame, text=self.translator.t('test_controls'), padding=10)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Simulation iterations
        ttk.Label(control_frame, text=self.translator.t('simulation_iterations')).grid(row=0, column=0, sticky=tk.W, padx=5)
        self.iterations_var = tk.StringVar(value="10000")
        ttk.Entry(control_frame, textvariable=self.iterations_var, width=10).grid(row=0, column=1, padx=5)
        
        ttk.Button(control_frame, text=self.translator.t('btn_run_simulation'), 
                  command=self.run_simulation_threaded).grid(row=0, column=2, padx=20)
        ttk.Button(control_frame, text=self.translator.t('btn_run_z_test'), 
                  command=self.run_z_test_threaded).grid(row=0, column=3, padx=5)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(control_frame, variable=self.progress_var, 
                                          maximum=100, length=300)
        self.progress_bar.grid(row=1, column=0, columnspan=4, pady=10, sticky=tk.EW)
        
        # Middle frame - Results
        results_frame = ttk.LabelFrame(self.ab_test_frame, text=self.translator.t('test_results'), padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.ab_results_text = tk.Text(results_frame, height=15, wrap=tk.WORD)
        ab_scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.ab_results_text.yview)
        self.ab_results_text.configure(yscrollcommand=ab_scrollbar.set)
        
        self.ab_results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        ab_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_visualization_tab(self):
        """Create visualization tab."""
        self.viz_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.viz_frame, text=self.translator.t('tab_visualizations'))
        
        # Plot selection
        control_frame = ttk.Frame(self.viz_frame)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(control_frame, text=self.translator.t('btn_simulation_histogram'), 
                  command=self.show_simulation_plot).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text=self.translator.t('btn_conversion_comparison'), 
                  command=self.show_comparison_plot).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text=self.translator.t('btn_save_plot'), 
                  command=self.save_current_plot).pack(side=tk.LEFT, padx=5)
        
        # Plot display area
        self.plot_frame = ttk.Frame(self.viz_frame)
        self.plot_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    def create_results_tab(self):
        """Create results summary tab."""
        self.results_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.results_frame, text=self.translator.t('tab_results'))
        
        # Results text area
        results_text_frame = ttk.LabelFrame(self.results_frame, text=self.translator.t('analysis_summary'), padding=10)
        results_text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.results_text = tk.Text(results_text_frame, height=25, wrap=tk.WORD)
        results_scrollbar = ttk.Scrollbar(results_text_frame, orient=tk.VERTICAL, command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=results_scrollbar.set)
        
        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        results_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Export buttons
        button_frame = ttk.Frame(self.results_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text=self.translator.t('btn_generate_report'), 
                  command=self.generate_report).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=self.translator.t('btn_export_to_csv'), 
                  command=self.export_to_csv).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=self.translator.t('btn_clear_results'), 
                  command=self.clear_results).pack(side=tk.LEFT, padx=5)
    
    def setup_status_bar(self):
        """Create status bar."""
        self.status_bar = ttk.Label(self.root, text=self.translator.t('status_ready'), relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def load_data(self):
        """Load main data file."""
        filename = filedialog.askopenfilename(
            title=self.translator.t('load_ab_test_data'),
            filetypes=[(self.translator.t('csv_files'), "*.csv"), (self.translator.t('all_files'), "*.*")]
        )
        
        if filename:
            self.update_status(self.translator.t('status_loading_data'))
            if self.data_processor.load_data(filename):
                self.file_path_label.config(text=os.path.basename(filename))
                self.update_data_info()
                self.update_status(self.translator.t('status_data_loaded', len(self.data_processor.df)))
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
            text = f"{self.translator.t('data_info_total_rows', info['shape'][0])}\n"
            text += f"{self.translator.t('data_info_columns', ', '.join(info['columns']))}\n\n"
            
            if self.data_processor.df is not None:
                misaligned = self.data_processor.get_misaligned_count()
                text += f"{self.translator.t('data_info_misaligned', misaligned)}\n\n"
            
            if self.data_processor.df_clean is not None:
                text += f"{self.translator.t('data_info_clean_rows', self.data_processor.df_clean.shape[0])}\n"
                
                # Add group statistics
                control_count = len(self.data_processor.df_clean[self.data_processor.df_clean['group'] == 'control'])
                treatment_count = len(self.data_processor.df_clean[self.data_processor.df_clean['group'] == 'treatment'])
                text += f"{self.translator.t('data_info_control_group', control_count)}\n"
                text += f"{self.translator.t('data_info_treatment_group', treatment_count)}\n"
                
                # Add conversion statistics
                converted_count = self.data_processor.df_clean['converted'].sum()
                total_count = len(self.data_processor.df_clean)
                not_converted_count = total_count - converted_count
                conversion_rate = converted_count / total_count
                
                text += f"{self.translator.t('data_info_converted', converted_count, conversion_rate)}\n"
                text += f"{self.translator.t('data_info_not_converted', not_converted_count, 1-conversion_rate)}\n"
            
            self.data_info_text.insert(tk.END, text)
    
    def calculate_probability_stats(self):
        """Calculate and display probability statistics."""
        if self.data_processor.df_clean is None:
            messagebox.showwarning(self.translator.t('warning'), self.translator.t('msg_load_and_clean_data_first'))
            return
        
        try:
            stats = self.data_processor.get_probability_stats()
            sizes = self.data_processor.get_sample_sizes()
            
            text = f"{self.translator.t('prob_stats_title')}\n"
            text += "=" * 50 + "\n\n"
            
            text += f"{self.translator.t('prob_stats_overall')}: {stats['overall_conversion']:.6f}\n"
            text += f"{self.translator.t('prob_stats_control')}: {stats['control_conversion']:.6f}\n"
            text += f"{self.translator.t('prob_stats_treatment')}: {stats['treatment_conversion']:.6f}\n\n"
            
            text += f"{self.translator.t('prob_stats_control_users')}: {sizes.get('n_control', 0)}\n"
            text += f"{self.translator.t('prob_stats_treatment_users')}: {sizes.get('n_treatment', 0)}\n"
            text += f"{self.translator.t('prob_stats_control_conversions')}: {int(sizes.get('n_control', 0) * stats['control_conversion'])}\n"
            text += f"{self.translator.t('prob_stats_treatment_conversions')}: {int(sizes.get('n_treatment', 0) * stats['treatment_conversion'])}\n\n"
            
            conversion_diff = stats['treatment_conversion'] - stats['control_conversion']
            text += f"{self.translator.t('prob_stats_difference')}: {conversion_diff:.6f}\n\n"
            
            if abs(conversion_diff) < 0.001:
                text += "Observation: The difference between conversion rates is very small.\n"
                text += "Statistical testing is needed to determine significance."
            
            self.prob_stats_text.delete(1.0, tk.END)
            self.prob_stats_text.insert(tk.END, text)
            
        except KeyError as e:
            error_msg = f"Data structure error: Missing required column {str(e)}. Please check your data format."
            messagebox.showerror(self.translator.t('error'), error_msg)
            self.update_status("Error: Invalid data structure")
        except Exception as e:
            error_msg = f"Error calculating statistics: {str(e)}"
            messagebox.showerror(self.translator.t('error'), error_msg)
            self.update_status("Error calculating statistics")
    
    def run_simulation_threaded(self):
        """Run simulation in background thread."""
        if self.data_processor.df_clean is None:
            messagebox.showwarning(self.translator.t('warning'), self.translator.t('msg_load_and_clean_data_first'))
            return
        
        try:
            iterations = int(self.iterations_var.get())
        except ValueError:
            messagebox.showerror(self.translator.t('error'), "Invalid number of iterations")
            return
        
        self.progress_var.set(0)
        self.update_status(self.translator.t('status_running_simulation'))
        
        def run_simulation():
            try:
                results = self.ab_analyzer.run_simulation(iterations)
                self.root.after(0, self.display_simulation_results, results)
            except KeyError as e:
                error_msg = f"Data structure error: Missing required column {str(e)}. Please check your data format."
                self.root.after(0, messagebox.showerror, self.translator.t('error'), error_msg)
                self.root.after(0, self.update_status, "Error: Invalid data structure")
            except Exception as e:
                error_msg = f"Simulation failed: {str(e)}"
                self.root.after(0, messagebox.showerror, self.translator.t('error'), error_msg)
                self.root.after(0, self.update_status, "Error during simulation")
            finally:
                self.root.after(0, self.progress_var.set, 100)
                self.root.after(0, self.update_status, self.translator.t('status_simulation_complete'))
        
        threading.Thread(target=run_simulation, daemon=True).start()
    
    def run_z_test_threaded(self):
        """Run z-test in background thread."""
        if self.data_processor.df_clean is None:
            messagebox.showwarning(self.translator.t('warning'), self.translator.t('msg_load_and_clean_data_first'))
            return
        
        self.update_status(self.translator.t('status_running_ztest'))
        
        def run_test():
            try:
                results = self.ab_analyzer.run_z_test()
                self.root.after(0, self.display_z_test_results, results)
            except KeyError as e:
                error_msg = f"Data structure error: Missing required column {str(e)}. Please check your data format."
                self.root.after(0, messagebox.showerror, self.translator.t('error'), error_msg)
                self.root.after(0, self.update_status, "Error: Invalid data structure")
            except Exception as e:
                error_msg = f"Z-test failed: {str(e)}"
                self.root.after(0, messagebox.showerror, self.translator.t('error'), error_msg)
                self.root.after(0, self.update_status, "Error during Z-test")
            finally:
                self.root.after(0, self.update_status, self.translator.t('status_ztest_complete'))
        
        threading.Thread(target=run_test, daemon=True).start()
    
    def display_simulation_results(self, results):
        """Display simulation results."""
        if 'error' in results:
            messagebox.showerror(self.translator.t('error'), results['error'])
            return
        
        text = f"{self.translator.t('ab_test_simulation_results')}\n"
        text += "=" * 50 + "\n\n"
        text += f"{self.translator.t('ab_test_iterations', results['n_iterations'])}\n"
        text += f"{self.translator.t('ab_test_null_hypothesis')}\n"
        text += f"{self.translator.t('ab_test_alternative_hypothesis')}\n\n"
        text += f"{self.translator.t('ab_test_observed_diff', results['actual_diff'])}\n"
        text += f"{self.translator.t('ab_test_p_value', results['p_value'])}\n\n"
        
        if results['p_value'] < 0.05:
            text += f"{self.translator.t('ab_test_conclusion_significant')}\n"
        else:
            text += f"{self.translator.t('ab_test_conclusion_not_significant')}\n"
        
        self.ab_results_text.delete(1.0, tk.END)
        self.ab_results_text.insert(tk.END, text)
    
    def display_z_test_results(self, results):
        """Display z-test results."""
        if 'error' in results:
            messagebox.showerror(self.translator.t('error'), results['error'])
            return
        
        text = f"{self.translator.t('ab_test_z_test_results')}\n"
        text += "=" * 50 + "\n\n"
        text += f"{self.translator.t('ab_test_z_score', results['z_score'])}\n"
        text += f"{self.translator.t('ab_test_p_value', results['p_value'])}\n\n"
        
        text += f"Conversions:\n"
        text += f"  New Page: {results['convert_new']:,} / {results['n_new']:,}\n"
        text += f"  Old Page: {results['convert_old']:,} / {results['n_old']:,}\n\n"
        
        if results['p_value'] < 0.05:
            text += f"{self.translator.t('ab_test_conclusion_significant')}\n"
        else:
            text += f"{self.translator.t('ab_test_conclusion_not_significant')}\n"
        
        self.ab_results_text.delete(1.0, tk.END)
        self.ab_results_text.insert(tk.END, text)
    
    def show_simulation_plot(self):
        """Show simulation histogram plot."""
        if self.ab_analyzer.simulation_results is None:
            messagebox.showwarning(self.translator.t('warning'), "Please run simulation first")
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
            messagebox.showwarning(self.translator.t('warning'), self.translator.t('msg_load_and_clean_data_first'))
            return
        
        try:
            # Clear previous plots
            for widget in self.plot_frame.winfo_children():
                widget.destroy()
            
            stats = self.data_processor.get_probability_stats()
            canvas = self.plot_manager.create_conversion_comparison_chart(
                self.plot_frame, stats)
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        except KeyError as e:
            error_msg = f"Data structure error: Missing required column {str(e)}. Please check your data format."
            messagebox.showerror(self.translator.t('error'), error_msg)
            self.update_status("Error: Invalid data structure")
        except Exception as e:
            error_msg = f"Error creating comparison plot: {str(e)}"
            messagebox.showerror(self.translator.t('error'), error_msg)
            self.update_status("Error creating plot")
    
    def save_current_plot(self):
        """Save current plot to file."""
        filename = filedialog.asksaveasfilename(
            title=self.translator.t('save_plot'),
            defaultextension=".png",
            filetypes=[(self.translator.t('png_files'), "*.png"), (self.translator.t('pdf_files'), "*.pdf"), (self.translator.t('all_files'), "*.*")]
        )
        
        if filename:
            # Try to save the most recent plot
            if 'simulation' in self.plot_manager.figures:
                self.plot_manager.save_plot('simulation', filename)
                messagebox.showinfo(self.translator.t('success'), f"Plot saved to {filename}")
            else:
                messagebox.showwarning(self.translator.t('warning'), self.translator.t('msg_no_plot_to_save'))
    
    def generate_report(self):
        """Generate comprehensive analysis report."""
        if self.data_processor.df_clean is None:
            messagebox.showwarning(self.translator.t('warning'), self.translator.t('msg_load_and_clean_data_first'))
            return
        
        summary = self.ab_analyzer.get_summary_stats()
        
        text = f"{self.translator.t('report_title')}\n"
        text += "=" * 60 + "\n\n"
        
        text += f"{self.translator.t('report_data_overview')}\n"
        text += "-" * 30 + "\n"
        text += f"Total Users: {summary['total_users']:,}\n"
        text += f"Unique Users: {summary['unique_users']:,}\n"
        text += f"New Page Sample Size: {summary['new_page_sample_size']:,}\n"
        text += f"Old Page Sample Size: {summary['old_page_sample_size']:,}\n\n"
        
        text += f"{self.translator.t('report_statistical_analysis')}\n"
        text += "-" * 30 + "\n"
        text += f"Overall Conversion Rate: {summary['overall_conversion_rate']:.4f}\n"
        text += f"Control Conversion Rate: {summary['control_conversion_rate']:.4f}\n"
        text += f"Treatment Conversion Rate: {summary['treatment_conversion_rate']:.4f}\n"
        text += f"Conversion Difference: {summary['conversion_difference']:.6f}\n\n"
        
        if self.ab_analyzer.simulation_results:
            text += f"{self.translator.t('ab_test_simulation_results')}\n"
            text += "-" * 30 + "\n"
            text += f"P-value: {self.ab_analyzer.simulation_results['p_value']:.6f}\n"
            text += f"Actual Difference: {self.ab_analyzer.simulation_results['actual_diff']:.6f}\n\n"
        
        if self.ab_analyzer.z_test_results:
            text += f"{self.translator.t('ab_test_z_test_results')}\n"
            text += "-" * 30 + "\n"
            text += f"Z-score: {self.ab_analyzer.z_test_results['z_score']:.6f}\n"
            text += f"P-value: {self.ab_analyzer.z_test_results['p_value']:.6f}\n\n"
        
        text += f"{self.translator.t('report_recommendations')}\n"
        text += "-" * 30 + "\n"
        
        # Generate recommendation based on results
        if self.ab_analyzer.simulation_results:
            p_val = self.ab_analyzer.simulation_results['p_value']
            if p_val > 0.05:
                text += f"• {self.translator.t('ab_test_conclusion_not_significant')}\n"
                text += f"• {self.translator.t('report_recommendation_not_significant')}\n"
            else:
                text += f"• {self.translator.t('ab_test_conclusion_significant')}\n"
                text += f"• {self.translator.t('report_recommendation_significant')}\n"
                
                # Calculate potential lift
                control_rate = summary['control_conversion_rate']
                treatment_rate = summary['treatment_conversion_rate']
                lift = (treatment_rate - control_rate) / control_rate
                text += f"• {self.translator.t('report_potential_lift', lift)}\n"
        else:
            text += "• Run statistical tests to get recommendations\n"
        
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, text)
        
        # Switch to results tab
        self.notebook.select(self.results_frame)
        self.update_status(self.translator.t('status_report_generated'))
    
    def export_to_csv(self):
        """Export results to CSV."""
        filename = filedialog.asksaveasfilename(
            title=self.translator.t('export_results'),
            defaultextension=".csv",
            filetypes=[(self.translator.t('csv_files'), "*.csv"), (self.translator.t('all_files'), "*.*")]
        )
        
        if filename:
            try:
                # Create summary dataframe
                summary = self.ab_analyzer.get_summary_stats()
                df = pd.DataFrame([summary])
                df.to_csv(filename, index=False)
                messagebox.showinfo(self.translator.t('success'), self.translator.t('msg_export_success', filename))
            except Exception as e:
                messagebox.showerror(self.translator.t('error'), self.translator.t('msg_export_failed', str(e)))
    
    def clear_results(self):
        """Clear all results."""
        self.results_text.delete(1.0, tk.END)
        self.ab_results_text.delete(1.0, tk.END)
        self.prob_stats_text.delete(1.0, tk.END)
        self.plot_manager.clear_all_plots()
        self.update_status(self.translator.t('status_results_cleared'))
    
    def show_data_preview(self):
        """Show preview of loaded data."""
        if self.data_processor.df is None:
            messagebox.showwarning(self.translator.t('warning'), self.translator.t('msg_load_data_first'))
            return
        
        # Create preview window
        preview_window = tk.Toplevel(self.root)
        preview_window.title(self.translator.t('preview_title'))
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
        about_text = self.translator.t('msg_about')
        messagebox.showinfo(self.translator.t('menu_about'), about_text)
    
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
