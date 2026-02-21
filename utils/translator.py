"""
Translation module for A/B Testing Desktop Application
Supports English and Russian languages
"""

class Translator:
    """Translation manager for the application."""
    
    def __init__(self):
        self.current_language = 'en'
        self.translations = {
            'en': {
                # Window and Menu
                'window_title': 'A/B Testing Analysis Tool',
                'menu_file': 'File',
                'menu_analysis': 'Analysis',
                'menu_help': 'Help',
                'menu_language': 'Language',
                'menu_load_data': 'Load Data...',
                'menu_load_country_data': 'Load Country Data...',
                'menu_export_results': 'Export Results...',
                'menu_exit': 'Exit',
                'menu_clean_data': 'Clean Data',
                'menu_run_ab_test': 'Run A/B Test',
                'menu_generate_report': 'Generate Report',
                'menu_about': 'About',
                'menu_switch_to_russian': 'Switch to Russian',
                'menu_switch_to_english': 'Switch to English',
                
                # Tab names
                'tab_data': 'Data',
                'tab_probability': 'Probability',
                'tab_ab_test': 'A/B Test',
                'tab_visualizations': 'Visualizations',
                'tab_results': 'Results',
                
                # Data tab
                'data_information': 'Data Information',
                'controls': 'Controls',
                'btn_load_data': 'Load Data',
                'btn_load_country_data': 'Load Country Data',
                'btn_clean_data': 'Clean Data',
                'btn_show_preview': 'Show Preview',
                'current_file': 'Current File:',
                'no_file_loaded': 'No file loaded',
                
                # Probability tab
                'probability_statistics': 'Probability Statistics',
                'btn_calculate_statistics': 'Calculate Statistics',
                
                # A/B Test tab
                'test_controls': 'Test Controls',
                'simulation_iterations': 'Simulation Iterations:',
                'btn_run_simulation': 'Run Simulation',
                'btn_run_z_test': 'Run Z-Test',
                'test_results': 'Test Results',
                
                # Visualization tab
                'btn_simulation_histogram': 'Simulation Histogram',
                'btn_conversion_comparison': 'Conversion Comparison',
                'btn_save_plot': 'Save Plot',
                
                # Results tab
                'analysis_summary': 'Analysis Summary',
                'btn_generate_report': 'Generate Report',
                'btn_export_to_csv': 'Export to CSV',
                'btn_clear_results': 'Clear Results',
                
                # Status bar
                'status_ready': 'Ready',
                'status_loading_data': 'Loading data...',
                'status_data_loaded': 'Data loaded: {} rows',
                'status_cleaning_data': 'Cleaning data...',
                'status_data_cleaned': 'Data cleaned',
                'status_calculating_stats': 'Calculating statistics...',
                'status_stats_calculated': 'Statistics calculated',
                'status_running_simulation': 'Running simulation...',
                'status_simulation_complete': 'Simulation complete',
                'status_running_ztest': 'Running z-test...',
                'status_ztest_complete': 'Z-test complete',
                'status_generating_report': 'Generating report...',
                'status_report_generated': 'Report generated',
                'status_results_cleared': 'Results cleared',
                
                # Dialog titles
                'load_ab_test_data': 'Load A/B Test Data',
                'load_country_data': 'Load Country Data',
                'save_plot': 'Save Plot',
                'export_results': 'Export Results',
                
                # Messages
                'msg_data_loaded': 'Data loaded successfully',
                'msg_country_data_loaded': 'Country data loaded successfully',
                'msg_data_cleaned': 'Data cleaned successfully',
                'msg_no_data_loaded': 'No data loaded. Please load data first.',
                'msg_export_success': 'Results exported to {}',
                'msg_export_failed': 'Export failed: {}',
                'msg_plot_saved': 'Plot saved to {}',
                'msg_about': 'A/B Testing Analysis Tool\nVersion 1.0\n\nA comprehensive tool for analyzing A/B test results using statistical methods and interactive visualizations.',
                
                # File types
                'csv_files': 'CSV files',
                'all_files': 'All files',
                'png_files': 'PNG files',
                'pdf_files': 'PDF files',
                
                # Error messages
                'error': 'Error',
                'success': 'Success',
                'info': 'Information',
                'warning': 'Warning',
                
                # Data information text
                'data_info_total_rows': 'Total rows: {}',
                'data_info_clean_rows': 'Clean rows: {}',
                'data_info_duplicates': 'Duplicates removed: {}',
                'data_info_misaligned': 'Misaligned rows removed: {}',
                'data_info_columns': 'Columns: {}',
                'data_info_control_group': 'Control group: {} users',
                'data_info_treatment_group': 'Treatment group: {} users',
                'data_info_old_page': 'Old page: {} users',
                'data_info_new_page': 'New page: {} users',
                'data_info_converted': 'Converted: {} users ({:.2%})',
                'data_info_not_converted': 'Not converted: {} users ({:.2%})',
                
                # Results page specific labels
                'results_total_users': 'Total Users: {}',
                'results_unique_users': 'Unique Users: {}',
                'results_new_page_sample': 'New Page Sample Size: {}',
                'results_old_page_sample': 'Old Page Sample Size: {}',
                'results_overall_conversion': 'Overall Conversion Rate: {}',
                'results_control_conversion': 'Control Conversion Rate: {}',
                'results_treatment_conversion': 'Treatment Conversion Rate: {}',
                'results_conversion_difference': 'Conversion Difference: {}',
                'results_p_value': 'P-value: {}',
                'results_actual_difference': 'Actual Difference: {}',
                'results_z_score': 'Z-score: {}',
                'results_conversions': 'Conversions:',
                'results_new_page_conversions': 'New Page: {}',
                'results_old_page_conversions': 'Old Page: {}',
                
                # Probability statistics text
                'prob_stats_title': 'Probability Analysis Results',
                'prob_stats_overall': 'Overall Conversion Rate',
                'prob_stats_control': 'Control Group Conversion Rate',
                'prob_stats_treatment': 'Treatment Group Conversion Rate',
                'prob_stats_difference': 'Difference (Treatment - Control)',
                'prob_stats_control_users': 'Control Group Users',
                'prob_stats_treatment_users': 'Treatment Group Users',
                'prob_stats_control_conversions': 'Control Group Conversions',
                'prob_stats_treatment_conversions': 'Treatment Group Conversions',
                
                # A/B test results text
                'ab_test_simulation_results': 'Monte Carlo Simulation Results',
                'ab_test_iterations': 'Simulation Iterations: {}',
                'ab_test_null_hypothesis': 'Null Hypothesis: p_treatment - p_control ≤ 0',
                'ab_test_alternative_hypothesis': 'Alternative Hypothesis: p_treatment - p_control > 0',
                'ab_test_observed_diff': 'Observed Difference: {:.6f}',
                'ab_test_p_value': 'P-value: {:.6f}',
                'ab_test_conclusion_significant': 'Conclusion: Reject null hypothesis. Result is statistically significant.',
                'ab_test_conclusion_not_significant': 'Conclusion: Fail to reject null hypothesis. Result is not statistically significant.',
                'ab_test_z_test_results': 'Z-Test Results',
                'ab_test_z_score': 'Z-score: {:.6f}',
                'ab_test_confidence_interval': '95% Confidence Interval: [{:.6f}, {:.6f}]',
                
                # Report text
                'report_title': 'A/B Test Analysis Report',
                'report_executive_summary': 'Executive Summary',
                'report_data_overview': 'Data Overview',
                'report_statistical_analysis': 'Statistical Analysis',
                'report_recommendations': 'Recommendations',
                'report_recommendation_significant': 'The treatment shows statistically significant improvement. Consider implementing the new page.',
                'report_recommendation_not_significant': 'No statistically significant difference found. Further testing may be needed.',
                'report_business_impact': 'Business Impact',
                'report_potential_lift': 'Potential conversion lift: {:.2%}',
                'report_next_steps': 'Next Steps',
                
                # Warning messages
                'msg_load_data_first': 'Please load data first',
                'msg_load_and_clean_data_first': 'Please load and clean data first',
                'msg_no_plot_to_save': 'No plot to save',
                'msg_failed_to_load_data': 'Failed to load data:\n{}',
                'msg_error_loading_data': 'Error loading data',
                
                # Plot elements and visualization
                'plot_simulation_title': 'Distribution of Simulated Differences Under Null Hypothesis',
                'plot_simulation_xlabel': 'Difference in Conversion Rates (p_new - p_old)',
                'plot_simulation_ylabel': 'Frequency',
                'plot_simulation_actual_diff': 'Actual Difference: {:.6f}',
                'plot_simulation_null_hypothesis': 'Null Hypothesis (0)',
                'plot_simulation_p_value': 'P-value: {:.4f}',
                
                'plot_comparison_title': 'Conversion Rate Comparison: Control vs Treatment',
                'plot_comparison_ylabel': 'Conversion Rate',
                'plot_comparison_control': 'Control\n(Old Page)',
                'plot_comparison_treatment': 'Treatment\n(New Page)',
                
                'plot_time_series_title1': 'Conversion Rates Over Time',
                'plot_time_series_xlabel': 'Day of Month',
                'plot_time_series_ylabel': 'Conversion Rate',
                'plot_time_series_old_page': 'Old Page',
                'plot_time_series_new_page': 'New Page',
                'plot_time_series_title2': 'Conversion Rate Difference Over Time',
                'plot_time_series_diff_ylabel': 'Difference (New - Old)',
                
                'plot_day_of_week_title': 'Conversion Rates by Day of Week',
                'plot_day_of_week_ylabel': 'Conversion Rate',
                
                # Data preview window
                'preview_title': 'Data Preview',
                'preview_close': 'Close',
                
                # Additional status messages
                'status_running_simulation': 'Running simulation...',
                'status_simulation_complete': 'Simulation complete',
                'status_running_ztest': 'Running z-test...',
                'status_ztest_complete': 'Z-test complete',
                'status_calculating_stats': 'Calculating statistics...',
                'status_stats_calculated': 'Statistics calculated',
                'status_cleaning_data': 'Cleaning data...',
                'status_data_cleaned': 'Data cleaned'
            },
            'ru': {
                # Window and Menu
                'window_title': 'Инструмент анализа A/B тестирования',
                'menu_file': 'Файл',
                'menu_analysis': 'Анализ',
                'menu_help': 'Справка',
                'menu_language': 'Язык',
                'menu_load_data': 'Загрузить данные...',
                'menu_load_country_data': 'Загрузить данные о странах...',
                'menu_export_results': 'Экспортировать результаты...',
                'menu_exit': 'Выход',
                'menu_clean_data': 'Очистить данные',
                'menu_run_ab_test': 'Запустить A/B тест',
                'menu_generate_report': 'Создать отчет',
                'menu_about': 'О программе',
                'menu_switch_to_russian': 'Переключить на русский',
                'menu_switch_to_english': 'Переключить на английский',
                
                # Tab names
                'tab_data': 'Данные',
                'tab_probability': 'Вероятности',
                'tab_ab_test': 'A/B тест',
                'tab_visualizations': 'Визуализации',
                'tab_results': 'Результаты',
                
                # Data tab
                'data_information': 'Информация о данных',
                'controls': 'Управление',
                'btn_load_data': 'Загрузить данные',
                'btn_load_country_data': 'Загрузить страны',
                'btn_clean_data': 'Очистить данные',
                'btn_show_preview': 'Показать предпросмотр',
                'current_file': 'Текущий файл:',
                'no_file_loaded': 'Файл не загружен',
                
                # Probability tab
                'probability_statistics': 'Статистика вероятностей',
                'btn_calculate_statistics': 'Рассчитать статистику',
                
                # A/B Test tab
                'test_controls': 'Управление тестом',
                'simulation_iterations': 'Итерации симуляции:',
                'btn_run_simulation': 'Запустить симуляцию',
                'btn_run_z_test': 'Запустить Z-тест',
                'test_results': 'Результаты теста',
                
                # Visualization tab
                'btn_simulation_histogram': 'Гистограмма симуляции',
                'btn_conversion_comparison': 'Сравнение конверсии',
                'btn_save_plot': 'Сохранить график',
                
                # Results tab
                'analysis_summary': 'Сводка анализа',
                'btn_generate_report': 'Создать отчет',
                'btn_export_to_csv': 'Экспортировать в CSV',
                'btn_clear_results': 'Очистить результаты',
                
                # Status bar
                'status_ready': 'Готов',
                'status_loading_data': 'Загрузка данных...',
                'status_data_loaded': 'Данные загружены: {} строк',
                'status_cleaning_data': 'Очистка данных...',
                'status_data_cleaned': 'Данные очищены',
                'status_calculating_stats': 'Расчет статистики...',
                'status_stats_calculated': 'Статистика рассчитана',
                'status_running_simulation': 'Запуск симуляции...',
                'status_simulation_complete': 'Симуляция завершена',
                'status_running_ztest': 'Запуск Z-теста...',
                'status_ztest_complete': 'Z-тест завершен',
                'status_generating_report': 'Создание отчета...',
                'status_report_generated': 'Отчет создан',
                'status_results_cleared': 'Результаты очищены',
                
                # Dialog titles
                'load_ab_test_data': 'Загрузить данные A/B теста',
                'load_country_data': 'Загрузить данные о странах',
                'save_plot': 'Сохранить график',
                'export_results': 'Экспортировать результаты',
                
                # Messages
                'msg_data_loaded': 'Данные успешно загружены',
                'msg_country_data_loaded': 'Данные о странах успешно загружены',
                'msg_data_cleaned': 'Данные успешно очищены',
                'msg_no_data_loaded': 'Данные не загружены. Пожалуйста, сначала загрузите данные.',
                'msg_export_success': 'Результаты экспортированы в {}',
                'msg_export_failed': 'Экспорт не удался: {}',
                'msg_plot_saved': 'График сохранен в {}',
                'msg_about': 'Инструмент анализа A/B тестирования\nВерсия 1.0\n\nКомплексный инструмент для анализа результатов A/B тестирования с использованием статистических методов и интерактивных визуализаций.',
                
                # File types
                'csv_files': 'CSV файлы',
                'all_files': 'Все файлы',
                'png_files': 'PNG файлы',
                'pdf_files': 'PDF файлы',
                
                # Error messages
                'error': 'Ошибка',
                'success': 'Успех',
                'info': 'Информация',
                'warning': 'Предупреждение',
                
                # Data information text
                'data_info_total_rows': 'Всего строк: {}',
                'data_info_clean_rows': 'Чистых строк: {}',
                'data_info_duplicates': 'Удалено дубликатов: {}',
                'data_info_misaligned': 'Удалено несовместимых строк: {}',
                'data_info_columns': 'Столбцы: {}',
                'data_info_control_group': 'Контрольная группа: {} пользователей',
                'data_info_treatment_group': 'Тестовая группа: {} пользователей',
                'data_info_old_page': 'Старая страница: {} пользователей',
                'data_info_new_page': 'Новая страница: {} пользователей',
                'data_info_converted': 'Сконвертировано: {} пользователей ({:.2%})',
                'data_info_not_converted': 'Не сконвертировано: {} пользователей ({:.2%})',
                
                # Results page specific labels
                'results_total_users': 'Всего пользователей: {}',
                'results_unique_users': 'Уникальных пользователей: {}',
                'results_new_page_sample': 'Размер выборки новой страницы: {}',
                'results_old_page_sample': 'Размер выборки старой страницы: {}',
                'results_overall_conversion': 'Общая конверсия: {}',
                'results_control_conversion': 'Конверсия контрольной группы: {}',
                'results_treatment_conversion': 'Конверсия тестовой группы: {}',
                'results_conversion_difference': 'Разница конверсии: {}',
                'results_p_value': 'P-значение: {}',
                'results_actual_difference': 'Фактическая разница: {}',
                'results_z_score': 'Z-оценка: {}',
                'results_conversions': 'Конверсии:',
                'results_new_page_conversions': 'Новая страница: {}',
                'results_old_page_conversions': 'Старая страница: {}',
                
                # A/B Test page - Comparison of One-sided vs Two-sided Tests
                'comparison_title': 'СРАВНЕНИЕ ОДНОСТОРОННИХ И ДВУСТОРОННИХ ТЕСТОВ',
                'one_sided_tests_title': 'ОДНОСТОРОННИЕ ТЕСТЫ (новый > старый)',
                'two_sided_tests_title': 'ДВУСТОРОННИЕ ТЕСТЫ (любая разница)',
                'simulation_p_value': 'P-значение симуляции: {}',
                'z_test_p_value': 'P-значение Z-теста: {}',
                'z_score': 'Z-показатель: {}',
                'success_message': '🎯 УСПЕХ: Двусторонние тесты достигли p-значения < {}!',
                'statistically_significant_difference': 'Это показывает статистически значимую разницу между старой и новой страницами при проверке любой разницы.',
                
                # A/B Test page - Interpretation
                'interpretation_title': 'ИНТЕРПРЕТАЦИЯ:',
                'interpretation_one_sided_check': '• Односторонние тесты проверяют, ЛУЧШЕ ли новая страница старой',
                'interpretation_two_sided_check': '• Двусторонние тесты проверяют наличие ЛЮБОЙ разницы между страницами',
                'interpretation_two_sided_more_likely': '• Двусторонние тесты с большей вероятностью обнаружат значимые различия',
                'interpretation_one_sided_prove_improvement': '• Используйте односторонний тест, когда вы специально хотите доказать улучшение',
                'interpretation_two_sided_detect_difference': '• Используйте двусторонний тест, когда вы хотите обнаружить любую разницу',
                
                # Probability statistics text
                'prob_stats_title': 'Результаты вероятностного анализа',
                'prob_stats_overall': 'Общая конверсия',
                'prob_stats_control': 'Конверсия контрольной группы',
                'prob_stats_treatment': 'Конверсия тестовой группы',
                'prob_stats_difference': 'Разница (Тестовая - Контрольная)',
                'prob_stats_control_users': 'Пользователи контрольной группы',
                'prob_stats_treatment_users': 'Пользователи тестовой группы',
                'prob_stats_control_conversions': 'Конверсии контрольной группы',
                'prob_stats_treatment_conversions': 'Конверсии тестовой группы',
                
                # A/B test results text
                'ab_test_simulation_results': 'Результаты симуляции Монте-Карло',
                'ab_test_iterations': 'Итерации симуляции: {}',
                'ab_test_null_hypothesis': 'Нулевая гипотеза: p_тестовая - p_контрольная ≤ 0',
                'ab_test_alternative_hypothesis': 'Альтернативная гипотеза: p_тестовая - p_контрольная > 0',
                'ab_test_observed_diff': 'Наблюдаемая разница: {:.6f}',
                'ab_test_p_value': 'P-значение: {:.6f}',
                'ab_test_conclusion_significant': 'Вывод: Отвергаем нулевую гипотезу. Результат статистически значим.',
                'ab_test_conclusion_not_significant': 'Вывод: Не отвергаем нулевую гипотезу. Результат не является статистически значимым.',
                'ab_test_z_test_results': 'Результаты Z-теста',
                'ab_test_z_score': 'Z-оценка: {:.6f}',
                'ab_test_confidence_interval': '95% доверительный интервал: [{:.6f}, {:.6f}]',
                
                # Report text
                'report_title': 'Отчет анализа A/B теста',
                'report_executive_summary': 'Краткое резюме',
                'report_data_overview': 'Обзор данных',
                'report_statistical_analysis': 'Статистический анализ',
                'report_recommendations': 'Рекомендации',
                'report_recommendation_significant': 'Тест показывает статистически значимое улучшение. Рассмотрите внедрение новой страницы.',
                'report_recommendation_not_significant': 'Статистически значимых различий не найдено. Может потребоваться дополнительное тестирование.',
                'report_business_impact': 'Влияние на бизнес',
                'report_potential_lift': 'Потенциальный рост конверсии: {:.2%}',
                'report_next_steps': 'Следующие шаги',
                
                # Warning messages
                'msg_load_data_first': 'Пожалуйста, сначала загрузите данные',
                'msg_load_and_clean_data_first': 'Пожалуйста, загрузите и очистите данные сначала',
                'msg_no_plot_to_save': 'Нет графика для сохранения',
                'msg_failed_to_load_data': 'Не удалось загрузить данные:\n{}',
                'msg_error_loading_data': 'Ошибка загрузки данных',
                
                # Plot elements and visualization
                'plot_simulation_title': 'Распределение симулированных различий при нулевой гипотезе',
                'plot_simulation_xlabel': 'Разница в конверсии (p_новая - p_старая)',
                'plot_simulation_ylabel': 'Частота',
                'plot_simulation_actual_diff': 'Фактическая разница: {:.6f}',
                'plot_simulation_null_hypothesis': 'Нулевая гипотеза (0)',
                'plot_simulation_p_value': 'P-значение: {:.4f}',
                
                'plot_comparison_title': 'Сравнение конверсии: Контрольная vs Тестовая',
                'plot_comparison_ylabel': 'Конверсия',
                'plot_comparison_control': 'Контрольная\n(Старая страница)',
                'plot_comparison_treatment': 'Тестовая\n(Новая страница)',
                
                'plot_time_series_title1': 'Конверсия во времени',
                'plot_time_series_xlabel': 'День месяца',
                'plot_time_series_ylabel': 'Конверсия',
                'plot_time_series_old_page': 'Старая страница',
                'plot_time_series_new_page': 'Новая страница',
                'plot_time_series_title2': 'Разница конверсии во времени',
                'plot_time_series_diff_ylabel': 'Разница (Новая - Старая)',
                
                'plot_day_of_week_title': 'Конверсия по дням недели',
                'plot_day_of_week_ylabel': 'Конверсия',
                
                # Data preview window
                'preview_title': 'Предпросмотр данных',
                'preview_close': 'Закрыть',
                
                # Additional status messages
                'status_running_simulation': 'Запуск симуляции...',
                'status_simulation_complete': 'Симуляция завершена',
                'status_running_ztest': 'Запуск Z-теста...',
                'status_ztest_complete': 'Z-тест завершен',
                'status_calculating_stats': 'Расчет статистики...',
                'status_stats_calculated': 'Статистика рассчитана',
                'status_cleaning_data': 'Очистка данных...',
                'status_data_cleaned': 'Данные очищены'
            }
        }
    
    def t(self, key, *args):
        """Get translation for a key with optional formatting."""
        if key in self.translations[self.current_language]:
            text = self.translations[self.current_language][key]
            if args:
                return text.format(*args)
            return text
        return key  # Return key if translation not found
    
    def switch_language(self, language):
        """Switch application language."""
        if language in self.translations:
            self.current_language = language
            return True
        return False
    
    def get_current_language(self):
        """Get current language code."""
        return self.current_language
