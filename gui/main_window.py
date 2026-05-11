"""
Главное окно настольного приложения A/B тестирования.
Реализовано в процедурном стиле без использования классов.

Все ссылки на виджеты и состояние GUI хранятся в модульном словаре UI,
который инициализируется функцией build_app().
"""

import os
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analysis import ab_test_analyzer, data_processor
from utils import translator
from visualization import plot_manager


UI: dict = {}


def build_app():
    """Создать и сконфигурировать главное окно приложения."""
    root = tk.Tk()
    UI['root'] = root

    update_window_title()
    root.geometry("1200x800")

    setup_menu()
    setup_main_frame()
    setup_status_bar()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.bind('<Control-o>', lambda e: load_data())

    return root


def run():
    """Запустить главный цикл приложения."""
    if 'root' not in UI:
        build_app()
    UI['root'].mainloop()


def setup_menu():
    """Создать строку меню приложения."""
    root = UI['root']
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label=translator.t('menu_file'), menu=file_menu)
    file_menu.add_command(label=translator.t('menu_load_data'), command=load_data, accelerator="Ctrl+O")
    file_menu.add_command(label=translator.t('menu_load_country_data'), command=load_country_data)
    file_menu.add_separator()
    file_menu.add_command(label=translator.t('menu_export_results'), command=export_to_csv)
    file_menu.add_separator()
    file_menu.add_command(label=translator.t('menu_exit'), command=on_closing)

    analysis_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label=translator.t('menu_analysis'), menu=analysis_menu)
    analysis_menu.add_command(label=translator.t('menu_clean_data'), command=clean_data)
    analysis_menu.add_command(label=translator.t('menu_run_ab_test'), command=run_ab_test)
    analysis_menu.add_command(label=translator.t('menu_generate_report'), command=generate_report)

    language_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label=translator.t('menu_language'), menu=language_menu)
    language_menu.add_command(label=translator.t('menu_switch_to_russian'), command=lambda: switch_language('ru'))
    language_menu.add_command(label=translator.t('menu_switch_to_english'), command=lambda: switch_language('en'))

    help_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label=translator.t('menu_help'), menu=help_menu)
    help_menu.add_command(label=translator.t('menu_about'), command=show_about)

    UI['menubar'] = menubar
    UI['file_menu'] = file_menu
    UI['analysis_menu'] = analysis_menu
    UI['language_menu'] = language_menu
    UI['help_menu'] = help_menu


def setup_main_frame():
    """Создать главный фрейм с вкладками."""
    root = UI['root']
    main_frame = ttk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    notebook = ttk.Notebook(main_frame)
    notebook.pack(fill=tk.BOTH, expand=True)
    UI['notebook'] = notebook

    create_data_tab()
    create_probability_tab()
    create_ab_test_tab()
    create_visualization_tab()
    create_results_tab()


def switch_language(language):
    """Сменить язык приложения и обновить все элементы UI."""
    if translator.switch_language(language):
        update_window_title()
        update_menu_texts()
        update_tab_texts()
        refresh_all_text_content()
        update_status(translator.t('status_ready'))


def refresh_all_text_content():
    """Обновить весь текстовый контент при смене языка."""
    if data_processor.has_raw_data():
        update_data_info()

    if data_processor.has_clean_data():
        if UI['prob_stats_text'].get(1.0, tk.END).strip():
            calculate_probability_stats()

    sim_results = ab_test_analyzer.get_simulation_results()
    z_results = ab_test_analyzer.get_z_test_results()

    if sim_results is not None:
        display_simulation_results(sim_results)
    if z_results is not None:
        display_z_test_results(z_results)

    if plot_manager.FIGURES:
        if 'simulation' in plot_manager.FIGURES and sim_results:
            show_simulation_plot()
        elif 'comparison' in plot_manager.FIGURES and data_processor.has_clean_data():
            show_comparison_plot()

    if UI['results_text'].get(1.0, tk.END).strip():
        generate_report()


def update_window_title():
    UI['root'].title(translator.t('window_title'))


def update_menu_texts():
    """Полностью пересоздать меню с новым языком."""
    setup_menu()


def update_tab_texts():
    """Обновить тексты вкладок и их содержимое."""
    notebook = UI['notebook']
    tabs = [
        (UI['data_frame'], 'tab_data'),
        (UI['prob_frame'], 'tab_probability'),
        (UI['ab_test_frame'], 'tab_ab_test'),
        (UI['viz_frame'], 'tab_visualizations'),
        (UI['results_frame'], 'tab_results'),
    ]
    for i, (_tab, key) in enumerate(tabs):
        notebook.tab(i, text=translator.t(key))

    update_data_tab_content()


def update_data_tab_content():
    """Обновить тексты в вкладке данных с учётом текущего языка."""
    data_frame = UI['data_frame']
    for widget in data_frame.winfo_children():
        if isinstance(widget, ttk.LabelFrame):
            current_text = widget.cget('text')
            if 'Data Information' in current_text or 'Информация о данных' in current_text:
                widget.configure(text=translator.t('data_information'))
            elif 'Controls' in current_text or 'Управление' in current_text:
                widget.configure(text=translator.t('controls'))

    for widget in data_frame.winfo_children():
        if isinstance(widget, ttk.LabelFrame):
            for child in widget.winfo_children():
                if isinstance(child, ttk.Button):
                    text = child.cget('text')
                    if 'Load Data' in text or 'Загрузить данные' in text:
                        child.configure(text=translator.t('btn_load_data'))
                    elif 'Load Country Data' in text or 'Загрузить страны' in text or 'Загрузить данные о странах' in text:
                        child.configure(text=translator.t('btn_load_country_data'))
                    elif 'Clean Data' in text or 'Очистить данные' in text:
                        child.configure(text=translator.t('btn_clean_data'))
                    elif 'Show Preview' in text or 'Показать' in text:
                        child.configure(text=translator.t('btn_show_preview'))
                elif isinstance(child, ttk.Label):
                    text = child.cget('text')
                    if 'Current File' in text or 'Текущий файл' in text:
                        child.configure(text=translator.t('current_file'))
                    elif 'No file loaded' in text or 'Файл не загружен' in text:
                        child.configure(text=translator.t('no_file_loaded'))


def create_data_tab():
    """Создать вкладку управления данными."""
    notebook = UI['notebook']
    data_frame = ttk.Frame(notebook)
    notebook.add(data_frame, text=translator.t('tab_data'))
    UI['data_frame'] = data_frame

    left_frame = ttk.LabelFrame(data_frame, text=translator.t('data_information'), padding=10)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

    data_info_text = tk.Text(left_frame, height=15, width=50, wrap=tk.WORD)
    data_scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=data_info_text.yview)
    data_info_text.configure(yscrollcommand=data_scrollbar.set)
    data_info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    data_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    UI['data_info_text'] = data_info_text

    right_frame = ttk.LabelFrame(data_frame, text=translator.t('controls'), padding=10)
    right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)

    ttk.Button(right_frame, text=translator.t('btn_load_data'), command=load_data).pack(pady=5, fill=tk.X)
    ttk.Button(right_frame, text=translator.t('btn_load_country_data'), command=load_country_data).pack(pady=5, fill=tk.X)
    ttk.Button(right_frame, text=translator.t('btn_clean_data'), command=clean_data).pack(pady=5, fill=tk.X)
    ttk.Button(right_frame, text=translator.t('btn_show_preview'), command=show_data_preview).pack(pady=5, fill=tk.X)

    ttk.Label(right_frame, text=translator.t('current_file')).pack(pady=(20, 5))
    file_path_label = ttk.Label(right_frame, text=translator.t('no_file_loaded'), wraplength=200)
    file_path_label.pack(pady=5)
    UI['file_path_label'] = file_path_label


def create_probability_tab():
    """Создать вкладку вероятностного анализа."""
    notebook = UI['notebook']
    prob_frame = ttk.Frame(notebook)
    notebook.add(prob_frame, text=translator.t('tab_probability'))
    UI['prob_frame'] = prob_frame

    canvas = tk.Canvas(prob_frame)
    scrollbar = ttk.Scrollbar(prob_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    stats_frame = ttk.LabelFrame(scrollable_frame, text=translator.t('probability_statistics'), padding=10)
    stats_frame.pack(fill=tk.X, padx=10, pady=5)

    prob_stats_text = tk.Text(stats_frame, height=20, width=80, wrap=tk.WORD)
    prob_scrollbar = ttk.Scrollbar(stats_frame, orient=tk.VERTICAL, command=prob_stats_text.yview)
    prob_stats_text.configure(yscrollcommand=prob_scrollbar.set)
    prob_stats_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    prob_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    UI['prob_stats_text'] = prob_stats_text

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    ttk.Button(
        scrollable_frame,
        text=translator.t('btn_calculate_statistics'),
        command=calculate_probability_stats,
    ).pack(pady=10)


def create_ab_test_tab():
    """Создать вкладку A/B тестирования."""
    notebook = UI['notebook']
    ab_test_frame = ttk.Frame(notebook)
    notebook.add(ab_test_frame, text=translator.t('tab_ab_test'))
    UI['ab_test_frame'] = ab_test_frame

    control_frame = ttk.LabelFrame(ab_test_frame, text=translator.t('test_controls'), padding=10)
    control_frame.pack(fill=tk.X, padx=10, pady=5)

    test_type_frame = ttk.Frame(control_frame)
    test_type_frame.grid(row=0, column=0, columnspan=4, sticky=tk.W, padx=5, pady=5)

    ttk.Label(test_type_frame, text=translator.t('label_test_type')).pack(side=tk.LEFT, padx=(0, 10))
    test_type_var = tk.StringVar(value="one-sided")
    UI['test_type_var'] = test_type_var
    ttk.Radiobutton(
        test_type_frame, text=translator.t('radio_one_sided'), variable=test_type_var, value="one-sided"
    ).pack(side=tk.LEFT, padx=5)
    ttk.Radiobutton(
        test_type_frame, text=translator.t('radio_two_sided'), variable=test_type_var, value="two-sided"
    ).pack(side=tk.LEFT, padx=5)
    ttk.Button(test_type_frame, text=translator.t('btn_compare_both'), command=run_both_tests_threaded).pack(
        side=tk.LEFT, padx=20
    )

    ttk.Label(control_frame, text=translator.t('simulation_iterations')).grid(row=1, column=0, sticky=tk.W, padx=5)
    iterations_var = tk.StringVar(value="10000")
    UI['iterations_var'] = iterations_var
    ttk.Entry(control_frame, textvariable=iterations_var, width=10).grid(row=1, column=1, padx=5)

    ttk.Button(control_frame, text=translator.t('btn_run_simulation'), command=run_simulation_threaded).grid(
        row=1, column=2, padx=20
    )
    ttk.Button(control_frame, text=translator.t('btn_run_z_test'), command=run_z_test_threaded).grid(
        row=1, column=3, padx=5
    )

    progress_var = tk.DoubleVar()
    UI['progress_var'] = progress_var
    progress_bar = ttk.Progressbar(control_frame, variable=progress_var, maximum=100, length=300)
    progress_bar.grid(row=2, column=0, columnspan=4, pady=10, sticky=tk.EW)
    UI['progress_bar'] = progress_bar

    results_frame = ttk.LabelFrame(ab_test_frame, text=translator.t('test_results'), padding=10)
    results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    ab_results_text = tk.Text(results_frame, height=15, wrap=tk.WORD)
    ab_scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=ab_results_text.yview)
    ab_results_text.configure(yscrollcommand=ab_scrollbar.set)
    ab_results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    ab_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    UI['ab_results_text'] = ab_results_text


def create_visualization_tab():
    """Создать вкладку визуализации."""
    notebook = UI['notebook']
    viz_frame = ttk.Frame(notebook)
    notebook.add(viz_frame, text=translator.t('tab_visualizations'))
    UI['viz_frame'] = viz_frame

    control_frame = ttk.Frame(viz_frame)
    control_frame.pack(fill=tk.X, padx=10, pady=5)

    ttk.Button(
        control_frame, text=translator.t('btn_simulation_histogram'), command=show_simulation_plot
    ).pack(side=tk.LEFT, padx=5)
    ttk.Button(
        control_frame, text=translator.t('btn_conversion_comparison'), command=show_comparison_plot
    ).pack(side=tk.LEFT, padx=5)
    ttk.Button(control_frame, text=translator.t('btn_save_plot'), command=save_current_plot).pack(side=tk.LEFT, padx=5)

    plot_frame = ttk.Frame(viz_frame)
    plot_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    UI['plot_frame'] = plot_frame


def create_results_tab():
    """Создать вкладку результатов."""
    notebook = UI['notebook']
    results_frame = ttk.Frame(notebook)
    notebook.add(results_frame, text=translator.t('tab_results'))
    UI['results_frame'] = results_frame

    results_text_frame = ttk.LabelFrame(results_frame, text=translator.t('analysis_summary'), padding=10)
    results_text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    results_text = tk.Text(results_text_frame, height=25, wrap=tk.WORD)
    results_scrollbar = ttk.Scrollbar(results_text_frame, orient=tk.VERTICAL, command=results_text.yview)
    results_text.configure(yscrollcommand=results_scrollbar.set)
    results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    results_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    UI['results_text'] = results_text

    button_frame = ttk.Frame(results_frame)
    button_frame.pack(fill=tk.X, padx=10, pady=5)

    ttk.Button(button_frame, text=translator.t('btn_generate_report'), command=generate_report).pack(
        side=tk.LEFT, padx=5
    )
    ttk.Button(button_frame, text=translator.t('btn_export_to_csv'), command=export_to_csv).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text=translator.t('btn_clear_results'), command=clear_results).pack(side=tk.LEFT, padx=5)


def setup_status_bar():
    """Создать строку статуса."""
    status_bar = ttk.Label(
        UI['root'], text=translator.t('status_ready'), relief=tk.SUNKEN, anchor=tk.W
    )
    status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    UI['status_bar'] = status_bar


def load_data():
    """Загрузить основной файл данных."""
    filename = filedialog.askopenfilename(
        title=translator.t('load_ab_test_data'),
        filetypes=[(translator.t('csv_files'), "*.csv"), (translator.t('all_files'), "*.*")],
    )

    if filename:
        update_status(translator.t('status_loading_data'))
        if data_processor.load_data(filename):
            UI['file_path_label'].config(text=os.path.basename(filename))
            update_data_info()
            update_status(translator.t('status_data_loaded', len(data_processor.get_df())))
        else:
            messagebox.showerror(
                translator.t('error'),
                translator.t('msg_failed_to_load_data', "\n".join(data_processor.get_validation_errors())),
            )
            update_status(translator.t('status_error_loading_data'))


def load_country_data():
    """Загрузить файл данных о странах."""
    filename = filedialog.askopenfilename(
        title=translator.t('load_country_data'),
        filetypes=[(translator.t('csv_files'), "*.csv"), (translator.t('all_files'), "*.*")],
    )

    if filename:
        if data_processor.load_country_data(filename):
            update_status(translator.t('status_country_data_loaded'))
            messagebox.showinfo(translator.t('success'), translator.t('msg_country_data_merged'))
        else:
            messagebox.showerror(
                translator.t('error'),
                translator.t('msg_failed_load_country_data', "\n".join(data_processor.get_validation_errors())),
            )


def clean_data():
    """Очистить загруженные данные."""
    if not data_processor.has_raw_data():
        messagebox.showwarning(translator.t('warning'), translator.t('msg_load_data_first'))
        return

    success, message = data_processor.clean_data()
    if success:
        update_data_info()
        update_status(translator.t('status_data_cleaned_successfully'))
        messagebox.showinfo(translator.t('success'), message)
    else:
        messagebox.showerror(translator.t('error'), message)


def update_data_info():
    """Обновить отображение информации о данных."""
    data_info_text = UI['data_info_text']
    data_info_text.delete(1.0, tk.END)

    if not data_processor.has_raw_data():
        return

    info = data_processor.get_data_info()
    text = f"{translator.t('data_info_total_rows', info['shape'][0])}\n"
    text += f"{translator.t('data_info_columns', ', '.join(info['columns']))}\n\n"

    if info.get('detected_format'):
        text += f"{translator.t('data_info_format', info['detected_format'].upper())}\n"
        if info.get('column_mapping'):
            text += f"{translator.t('data_info_column_mapping_header')}\n"
            for standard_col, actual_col in info['column_mapping'].items():
                text += f"  {standard_col} -> {actual_col}\n"
        text += "\n"

    misaligned = data_processor.count_misaligned()
    text += f"{translator.t('data_info_misaligned', misaligned)}\n\n"

    df_clean = data_processor.get_df_clean()
    if df_clean is not None:
        text += f"{translator.t('data_info_clean_rows', df_clean.shape[0])}\n"

        control_count = len(df_clean[df_clean['group'] == 'control'])
        treatment_count = len(df_clean[df_clean['group'] == 'treatment'])
        text += f"{translator.t('data_info_control_group', control_count)}\n"
        text += f"{translator.t('data_info_treatment_group', treatment_count)}\n"

        converted_count = df_clean['converted'].sum()
        total_count = len(df_clean)
        not_converted_count = total_count - converted_count
        conversion_rate = converted_count / total_count

        text += f"{translator.t('data_info_converted', converted_count, conversion_rate)}\n"
        text += f"{translator.t('data_info_not_converted', not_converted_count, 1 - conversion_rate)}\n"

    data_info_text.insert(tk.END, text)


def calculate_probability_stats():
    """Рассчитать и отобразить вероятностную статистику."""
    if not data_processor.has_clean_data():
        messagebox.showwarning(translator.t('warning'), translator.t('msg_load_and_clean_data_first'))
        return

    try:
        stats = data_processor.get_probability_stats()
        sizes = data_processor.get_sample_sizes()

        text = f"{translator.t('prob_stats_title')}\n"
        text += "=" * 50 + "\n\n"

        text += f"{translator.t('prob_stats_overall')}: {stats['overall_conversion']:.6f}\n"
        text += f"{translator.t('prob_stats_control')}: {stats['control_conversion']:.6f}\n"
        text += f"{translator.t('prob_stats_treatment')}: {stats['treatment_conversion']:.6f}\n\n"

        text += f"{translator.t('prob_stats_control_users')}: {sizes.get('n_control', 0)}\n"
        text += f"{translator.t('prob_stats_treatment_users')}: {sizes.get('n_treatment', 0)}\n"
        text += f"{translator.t('prob_stats_control_conversions')}: {int(sizes.get('n_control', 0) * stats['control_conversion'])}\n"
        text += f"{translator.t('prob_stats_treatment_conversions')}: {int(sizes.get('n_treatment', 0) * stats['treatment_conversion'])}\n\n"

        conversion_diff = stats['treatment_conversion'] - stats['control_conversion']
        text += f"{translator.t('prob_stats_difference')}: {conversion_diff:.6f}\n\n"

        if abs(conversion_diff) < 0.001:
            text += f"{translator.t('prob_observation_small_diff')}\n"
            text += translator.t('prob_observation_need_test')

        UI['prob_stats_text'].delete(1.0, tk.END)
        UI['prob_stats_text'].insert(tk.END, text)

    except KeyError as e:
        messagebox.showerror(translator.t('error'), translator.t('msg_data_structure_error', str(e)))
        update_status(translator.t('status_invalid_data_structure'))
    except Exception as e:
        messagebox.showerror(translator.t('error'), translator.t('msg_calc_stats_error', str(e)))
        update_status(translator.t('status_error_calc_stats'))


def run_simulation_threaded():
    """Запустить симуляцию в фоновом потоке."""
    if not data_processor.has_clean_data():
        messagebox.showwarning(translator.t('warning'), translator.t('msg_load_and_clean_data_first'))
        return

    try:
        iterations = int(UI['iterations_var'].get())
    except ValueError:
        messagebox.showerror(translator.t('error'), translator.t('msg_invalid_iterations'))
        return

    UI['progress_var'].set(0)
    update_status(translator.t('status_running_simulation'))
    root = UI['root']

    def worker():
        try:
            test_type = UI['test_type_var'].get()
            results = ab_test_analyzer.run_simulation(iterations, test_type)
            root.after(0, display_simulation_results, results)
        except KeyError as e:
            error_msg = translator.t('msg_data_structure_error', str(e))
            root.after(0, messagebox.showerror, translator.t('error'), error_msg)
            root.after(0, update_status, translator.t('status_invalid_data_structure'))
        except Exception as e:
            error_msg = translator.t('msg_simulation_failed', str(e))
            root.after(0, messagebox.showerror, translator.t('error'), error_msg)
            root.after(0, update_status, translator.t('status_error_during_simulation'))
        finally:
            root.after(0, UI['progress_var'].set, 100)
            root.after(0, update_status, translator.t('status_simulation_complete'))

    threading.Thread(target=worker, daemon=True).start()


def run_z_test_threaded():
    """Запустить z-тест в фоновом потоке."""
    if not data_processor.has_clean_data():
        messagebox.showwarning(translator.t('warning'), translator.t('msg_load_and_clean_data_first'))
        return

    update_status(translator.t('status_running_ztest'))
    root = UI['root']

    def worker():
        try:
            test_type = UI['test_type_var'].get()
            results = ab_test_analyzer.run_z_test(test_type)
            root.after(0, display_z_test_results, results)
        except KeyError as e:
            error_msg = translator.t('msg_data_structure_error', str(e))
            root.after(0, messagebox.showerror, translator.t('error'), error_msg)
            root.after(0, update_status, translator.t('status_invalid_data_structure'))
        except Exception as e:
            error_msg = translator.t('msg_ztest_failed', str(e))
            root.after(0, messagebox.showerror, translator.t('error'), error_msg)
            root.after(0, update_status, translator.t('status_error_during_ztest'))
        finally:
            root.after(0, update_status, translator.t('status_ztest_complete'))

    threading.Thread(target=worker, daemon=True).start()


def run_both_tests_threaded():
    """Запустить оба типа тестов в фоновом потоке для сравнения."""
    if not data_processor.has_clean_data():
        messagebox.showwarning(translator.t('warning'), translator.t('msg_load_and_clean_data_first'))
        return

    try:
        iterations = int(UI['iterations_var'].get())
    except ValueError:
        messagebox.showerror(translator.t('error'), translator.t('msg_invalid_iterations'))
        return

    UI['progress_var'].set(0)
    update_status(translator.t('status_running_both_tests'))
    root = UI['root']

    def worker():
        try:
            results = ab_test_analyzer.run_both_test_types(iterations)
            root.after(0, display_both_test_results, results)
        except KeyError as e:
            error_msg = translator.t('msg_data_structure_error', str(e))
            root.after(0, messagebox.showerror, translator.t('error'), error_msg)
            root.after(0, update_status, translator.t('status_invalid_data_structure'))
        except Exception as e:
            error_msg = translator.t('msg_comparison_failed', str(e))
            root.after(0, messagebox.showerror, translator.t('error'), error_msg)
            root.after(0, update_status, translator.t('status_error_during_comparison'))
        finally:
            root.after(0, UI['progress_var'].set, 100)
            root.after(0, update_status, translator.t('status_test_comparison_complete'))

    threading.Thread(target=worker, daemon=True).start()


def display_simulation_results(results):
    """Показать результаты симуляции."""
    if 'error' in results:
        messagebox.showerror(translator.t('error'), results['error'])
        return

    text = f"{translator.t('ab_test_simulation_results')}\n"
    text += "=" * 50 + "\n\n"
    text += f"{translator.t('ab_test_iterations', results['n_iterations'])}\n"
    text += f"{translator.t('ab_test_null_hypothesis')}\n"
    text += f"{translator.t('ab_test_alternative_hypothesis')}\n\n"
    text += f"{translator.t('ab_test_observed_diff', results['actual_diff'])}\n"
    text += f"{translator.t('ab_test_p_value', results['p_value'])}\n\n"

    if results['p_value'] < 0.05:
        text += f"{translator.t('ab_test_conclusion_significant')}\n"
    else:
        text += f"{translator.t('ab_test_conclusion_not_significant')}\n"

    UI['ab_results_text'].delete(1.0, tk.END)
    UI['ab_results_text'].insert(tk.END, text)


def display_z_test_results(results):
    """Показать результаты z-теста."""
    if 'error' in results:
        messagebox.showerror(translator.t('error'), results['error'])
        return

    text = f"{translator.t('ab_test_z_test_results')}\n"
    text += "=" * 50 + "\n\n"
    text += f"{translator.t('ab_test_z_score', results['z_score'])}\n"
    text += f"{translator.t('ab_test_p_value', results['p_value'])}\n\n"

    text += f"{translator.t('results_conversions')}\n"
    new_page_conv_str = f"{results['convert_new']:,} / {results['n_new']:,}"
    old_page_conv_str = f"{results['convert_old']:,} / {results['n_old']:,}"
    text += f"  {translator.t('results_new_page_conversions', new_page_conv_str)}\n"
    text += f"  {translator.t('results_old_page_conversions', old_page_conv_str)}\n\n"

    if results['p_value'] < 0.05:
        text += f"{translator.t('ab_test_conclusion_significant')}\n"
    else:
        text += f"{translator.t('ab_test_conclusion_not_significant')}\n"

    UI['ab_results_text'].delete(1.0, tk.END)
    UI['ab_results_text'].insert(tk.END, text)


def display_both_test_results(results):
    """Показать сравнение результатов обоих типов тестов."""
    if 'error' in results:
        messagebox.showerror(translator.t('error'), results['error'])
        return

    text = f"{translator.t('comparison_title')}\n"
    text += "=" * 60 + "\n\n"

    text += f"{translator.t('one_sided_tests_title')}\n"
    text += "-" * 40 + "\n"

    one_sim = results['one_sided_simulation']
    one_z = results['one_sided_ztest']

    text += f"{translator.t('simulation_p_value', one_sim['p_value'])}\n"
    text += f"{translator.t('z_test_p_value', one_z['p_value'])}\n"
    text += f"{translator.t('z_score', one_z['z_score'])}\n\n"

    text += f"{translator.t('two_sided_tests_title')}\n"
    text += "-" * 40 + "\n"

    two_sim = results['two_sided_simulation']
    two_z = results['two_sided_ztest']

    text += f"{translator.t('simulation_p_value', two_sim['p_value'])}\n"
    text += f"{translator.t('z_test_p_value', two_z['p_value'])}\n"
    text += f"{translator.t('z_score', two_z['z_score'])}\n\n"

    if two_sim['p_value'] < 0.25 or two_z['p_value'] < 0.25:
        text += f"{translator.t('success_message', '0.25')}\n"
        text += f"{translator.t('statistically_significant_difference')}\n\n"
    else:
        text += f"{translator.t('msg_two_sided_not_achieved')}\n\n"

    text += f"{translator.t('interpretation_title')}\n"
    text += "-" * 20 + "\n"
    text += f"{translator.t('interpretation_one_sided_check')}\n"
    text += f"{translator.t('interpretation_two_sided_check')}\n"
    text += f"{translator.t('interpretation_two_sided_more_likely')}\n"
    text += f"{translator.t('interpretation_one_sided_prove_improvement')}\n"
    text += f"{translator.t('interpretation_two_sided_detect_difference')}\n"

    UI['ab_results_text'].delete(1.0, tk.END)
    UI['ab_results_text'].insert(tk.END, text)


def show_simulation_plot():
    """Показать гистограмму симуляции."""
    sim_results = ab_test_analyzer.get_simulation_results()
    if sim_results is None:
        messagebox.showwarning(translator.t('warning'), translator.t('msg_run_simulation_first'))
        return

    plot_frame = UI['plot_frame']
    for widget in plot_frame.winfo_children():
        widget.destroy()

    canvas = plot_manager.create_simulation_histogram(plot_frame, sim_results)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


def show_comparison_plot():
    """Показать график сравнения конверсий."""
    if not data_processor.has_clean_data():
        messagebox.showwarning(translator.t('warning'), translator.t('msg_load_and_clean_data_first'))
        return

    try:
        plot_frame = UI['plot_frame']
        for widget in plot_frame.winfo_children():
            widget.destroy()

        stats = data_processor.get_probability_stats()
        canvas = plot_manager.create_conversion_comparison_chart(plot_frame, stats)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    except KeyError as e:
        messagebox.showerror(translator.t('error'), translator.t('msg_data_structure_error', str(e)))
        update_status(translator.t('status_invalid_data_structure'))
    except Exception as e:
        messagebox.showerror(translator.t('error'), translator.t('msg_create_plot_error', str(e)))
        update_status(translator.t('status_error_creating_plot'))


def save_current_plot():
    """Сохранить текущий график в файл."""
    filename = filedialog.asksaveasfilename(
        title=translator.t('save_plot'),
        defaultextension=".png",
        filetypes=[
            (translator.t('png_files'), "*.png"),
            (translator.t('pdf_files'), "*.pdf"),
            (translator.t('all_files'), "*.*"),
        ],
    )

    if filename:
        if 'simulation' in plot_manager.FIGURES:
            plot_manager.save_plot('simulation', filename)
            messagebox.showinfo(translator.t('success'), translator.t('msg_plot_saved', filename))
        else:
            messagebox.showwarning(translator.t('warning'), translator.t('msg_no_plot_to_save'))


def generate_report():
    """Сформировать комплексный отчёт анализа."""
    if not data_processor.has_clean_data():
        messagebox.showwarning(translator.t('warning'), translator.t('msg_load_and_clean_data_first'))
        return

    summary = ab_test_analyzer.get_summary_stats()

    text = f"{translator.t('report_title')}\n"
    text += "=" * 60 + "\n\n"

    text += f"{translator.t('report_data_overview')}\n"
    text += "-" * 30 + "\n"
    text += f"{translator.t('results_total_users', f'{summary['total_users']:,}')}\n"
    text += f"{translator.t('results_unique_users', f'{summary['unique_users']:,}')}\n"
    text += f"{translator.t('results_new_page_sample', f'{summary['new_page_sample_size']:,}')}\n"
    text += f"{translator.t('results_old_page_sample', f'{summary['old_page_sample_size']:,}')}\n\n"

    text += f"{translator.t('report_statistical_analysis')}\n"
    text += "-" * 30 + "\n"
    overall_conv_str = f"{summary['overall_conversion_rate']:.4f}"
    control_conv_str = f"{summary['control_conversion_rate']:.4f}"
    treatment_conv_str = f"{summary['treatment_conversion_rate']:.4f}"
    conv_diff_str = f"{summary['conversion_difference']:.6f}"
    text += f"{translator.t('results_overall_conversion', overall_conv_str)}\n"
    text += f"{translator.t('results_control_conversion', control_conv_str)}\n"
    text += f"{translator.t('results_treatment_conversion', treatment_conv_str)}\n"
    text += f"{translator.t('results_conversion_difference', conv_diff_str)}\n\n"

    sim_results = ab_test_analyzer.get_simulation_results()
    z_results = ab_test_analyzer.get_z_test_results()

    if sim_results:
        text += f"{translator.t('ab_test_simulation_results')}\n"
        text += "-" * 30 + "\n"
        p_val_str = f"{sim_results['p_value']:.6f}"
        diff_str = f"{sim_results['actual_diff']:.6f}"
        text += f"{translator.t('results_p_value', p_val_str)}\n"
        text += f"{translator.t('results_actual_difference', diff_str)}\n\n"

    if z_results:
        text += f"{translator.t('ab_test_z_test_results')}\n"
        text += "-" * 30 + "\n"
        z_score_str = f"{z_results['z_score']:.6f}"
        p_val_str2 = f"{z_results['p_value']:.6f}"
        text += f"{translator.t('results_z_score', z_score_str)}\n"
        text += f"{translator.t('results_p_value', p_val_str2)}\n\n"

    text += f"{translator.t('report_recommendations')}\n"
    text += "-" * 30 + "\n"

    if sim_results:
        p_val = sim_results['p_value']
        if p_val > 0.05:
            text += f"- {translator.t('ab_test_conclusion_not_significant')}\n"
            text += f"- {translator.t('report_recommendation_not_significant')}\n"
        else:
            text += f"- {translator.t('ab_test_conclusion_significant')}\n"
            text += f"- {translator.t('report_recommendation_significant')}\n"

            control_rate = summary['control_conversion_rate']
            treatment_rate = summary['treatment_conversion_rate']
            lift = (treatment_rate - control_rate) / control_rate
            text += f"- {translator.t('report_potential_lift', lift)}\n"
    else:
        text += f"- {translator.t('msg_run_tests_for_recommendations')}\n"

    UI['results_text'].delete(1.0, tk.END)
    UI['results_text'].insert(tk.END, text)

    UI['notebook'].select(UI['results_frame'])
    update_status(translator.t('status_report_generated'))


def export_to_csv():
    """Экспортировать результаты в CSV."""
    filename = filedialog.asksaveasfilename(
        title=translator.t('export_results'),
        defaultextension=".csv",
        filetypes=[(translator.t('csv_files'), "*.csv"), (translator.t('all_files'), "*.*")],
    )

    if filename:
        try:
            summary = ab_test_analyzer.get_summary_stats()
            df = pd.DataFrame([summary])
            df.to_csv(filename, index=False)
            messagebox.showinfo(translator.t('success'), translator.t('msg_export_success', filename))
        except Exception as e:
            messagebox.showerror(translator.t('error'), translator.t('msg_export_failed', str(e)))


def clear_results():
    """Очистить все результаты."""
    UI['results_text'].delete(1.0, tk.END)
    UI['ab_results_text'].delete(1.0, tk.END)
    UI['prob_stats_text'].delete(1.0, tk.END)
    plot_manager.clear_all_plots()
    update_status(translator.t('status_results_cleared'))


def show_data_preview():
    """Показать предпросмотр загруженных данных."""
    if not data_processor.has_raw_data():
        messagebox.showwarning(translator.t('warning'), translator.t('msg_load_data_first'))
        return

    preview_window = tk.Toplevel(UI['root'])
    preview_window.title(translator.t('preview_title'))
    preview_window.geometry("800x600")

    tree_frame = ttk.Frame(preview_window)
    tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    preview_data = data_processor.get_df().head(100)

    tree = ttk.Treeview(tree_frame)
    tree["columns"] = list(preview_data.columns)
    for col in preview_data.columns:
        tree.column(col, width=100, anchor=tk.CENTER)
        tree.heading(col, text=col)

    for _, row in preview_data.iterrows():
        tree.insert("", tk.END, values=list(row))

    y_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
    x_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=tree.xview)
    tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)


def run_ab_test():
    """Запустить A/B тест (быстрый вызов симуляции)."""
    run_simulation_threaded()


def show_about():
    """Показать диалог 'О программе'."""
    messagebox.showinfo(translator.t('menu_about'), translator.t('msg_about'))


def update_status(message):
    """Обновить строку состояния."""
    status_bar = UI.get('status_bar')
    if status_bar is None:
        return
    status_bar.config(text=message)
    UI['root'].update_idletasks()


def on_closing():
    """Обработать закрытие приложения."""
    if messagebox.askokcancel(translator.t('quit_title'), translator.t('quit_message')):
        plot_manager.clear_all_plots()
        UI['root'].destroy()


if __name__ == "__main__":
    build_app()
    run()
