"""
Анализ A/B тестирования: симуляция Монте-Карло и z-тест для пропорций.
Реализован в процедурном стиле без использования классов.

Последние полученные результаты хранятся в модульном словаре STATE,
чтобы GUI и отчёты могли их переиспользовать без передачи аргументов.
"""

import math
import os
import sys
from typing import Any, Dict

import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from analysis import data_processor


STATE = {
    'simulation_results': None,
    'z_test_results': None,
}


def reset_state():
    """Сбросить сохранённые результаты тестов."""
    STATE['simulation_results'] = None
    STATE['z_test_results'] = None


def normal_cdf(x: float) -> float:
    """Функция распределения стандартного нормального распределения."""
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def proportions_ztest(count, nobs, value=None, alternative='two-sided'):
    """
    Z-тест для пропорций.

    Args:
        count: пара количества успехов в группах
        nobs: пара размеров выборок
        value: значение нулевой гипотезы (по умолчанию 0 для разности пропорций)
        alternative: 'two-sided', 'larger' или 'smaller'

    Returns:
        (z_stat, p_value)
    """
    if value is None:
        value = 0

    count1, count2 = count
    n1, n2 = nobs

    p1 = count1 / n1
    p2 = count2 / n2

    if value == 0:
        p_pooled = (count1 + count2) / (n1 + n2)
        var_pooled = p_pooled * (1 - p_pooled) * (1 / n1 + 1 / n2)
    else:
        var_pooled = p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2

    diff = p1 - p2 - value
    z_stat = diff / math.sqrt(var_pooled)

    if alternative == 'two-sided':
        p_value = 2 * (1 - normal_cdf(abs(z_stat)))
    elif alternative == 'larger':
        p_value = 1 - normal_cdf(z_stat)
    elif alternative == 'smaller':
        p_value = normal_cdf(z_stat)
    else:
        raise ValueError("alternative must be 'two-sided', 'larger', or 'smaller'")

    return z_stat, p_value


def run_simulation(n_iterations: int = 10000, test_type: str = 'one-sided') -> Dict[str, Any]:
    """Запустить симуляцию Монте-Карло при нулевой гипотезе."""
    if not data_processor.has_clean_data():
        return {'error': 'Данные недоступны'}

    stats = data_processor.get_probability_stats()
    sizes = data_processor.get_sample_sizes()

    p_null = stats.get('overall_conversion', 0)
    n_new = sizes.get('n_new', 0)
    n_old = sizes.get('n_old', 0)

    if n_new == 0 or n_old == 0:
        return {'error': 'Некорректные размеры выборок'}

    np.random.seed(42)
    p_diffs = (
        np.random.binomial(n_new, p_null, n_iterations) / n_new
        - np.random.binomial(n_old, p_null, n_iterations) / n_old
    )

    actual_diff = stats['treatment_conversion'] - stats['control_conversion']

    if test_type == 'two-sided':
        p_value = (np.abs(p_diffs) > np.abs(actual_diff)).mean()
    else:
        p_value = (p_diffs > actual_diff).mean()

    results = {
        'p_diffs': p_diffs,
        'actual_diff': actual_diff,
        'p_value': p_value,
        'p_null': p_null,
        'n_iterations': n_iterations,
        'test_type': test_type,
    }
    STATE['simulation_results'] = results
    return results


def run_z_test(test_type: str = 'one-sided') -> Dict[str, Any]:
    """Запустить z-тест для пропорций."""
    if not data_processor.has_clean_data():
        return {'error': 'Данные недоступны'}

    counts = data_processor.get_conversion_counts()
    sizes = data_processor.get_sample_sizes()

    convert_new = counts.get('convert_new', 0)
    convert_old = counts.get('convert_old', 0)
    n_new = sizes.get('n_new', 0)
    n_old = sizes.get('n_old', 0)

    if n_new == 0 or n_old == 0:
        return {'error': 'Некорректные размеры выборок'}

    alternative = 'two-sided' if test_type == 'two-sided' else 'larger'
    z_score, p_value = proportions_ztest(
        [convert_new, convert_old], [n_new, n_old], alternative=alternative
    )

    critical_value = 1.6448536269514722
    z_significance = normal_cdf(z_score)

    results = {
        'z_score': z_score,
        'p_value': p_value,
        'critical_value': critical_value,
        'z_significance': z_significance,
        'convert_new': convert_new,
        'convert_old': convert_old,
        'n_new': n_new,
        'n_old': n_old,
        'test_type': test_type,
        'alternative': alternative,
    }
    STATE['z_test_results'] = results
    return results


def run_both_test_types(n_iterations: int = 10000) -> Dict[str, Any]:
    """Запустить и односторонние, и двусторонние тесты для сравнения."""
    original_sim = STATE['simulation_results']
    original_z = STATE['z_test_results']

    one_sided_sim = run_simulation(n_iterations, 'one-sided')
    one_sided_z = run_z_test('one-sided')

    two_sided_sim = run_simulation(n_iterations, 'two-sided')
    two_sided_z = run_z_test('two-sided')

    STATE['simulation_results'] = original_sim
    STATE['z_test_results'] = original_z

    return {
        'one_sided_simulation': one_sided_sim,
        'one_sided_ztest': one_sided_z,
        'two_sided_simulation': two_sided_sim,
        'two_sided_ztest': two_sided_z,
    }


def get_interpretation() -> str:
    """Получить интерпретацию результатов тестов."""
    sim = STATE['simulation_results']
    z_test = STATE['z_test_results']

    if sim is None and z_test is None:
        return "Результаты тестов отсутствуют. Сначала запустите анализ."

    interpretation = []

    if sim:
        p_val_sim = sim['p_value']
        test_type = sim.get('test_type', 'one-sided')
        interpretation.append(f"P-значение симуляции ({test_type}): {p_val_sim:.4f}")

        if test_type == 'two-sided':
            if p_val_sim < 0.25:
                interpretation.append("-> Достигнуто p-значение < 0.25 для двустороннего теста!")
                interpretation.append("-> Между страницами есть статистически значимая разница")
            else:
                interpretation.append("-> Статистически значимая разница не обнаружена")
        else:
            if p_val_sim > 0.05:
                interpretation.append("-> Не удаётся отвергнуть нулевую гипотезу")
                interpretation.append("-> Новая страница НЕ значимо лучше старой")
            else:
                interpretation.append("-> Отвергаем нулевую гипотезу")
                interpretation.append("-> Новая страница показывает значимое улучшение")

    if z_test:
        p_val_z = z_test['p_value']
        z_score = z_test['z_score']
        critical_value = z_test['critical_value']
        test_type = z_test.get('test_type', 'one-sided')

        interpretation.append(f"\nP-значение Z-теста ({test_type}): {p_val_z:.4f}")
        interpretation.append(f"Z-оценка: {z_score:.4f} (критическое: {critical_value:.4f})")

        if test_type == 'two-sided':
            if p_val_z < 0.25:
                interpretation.append("-> Достигнуто p-значение < 0.25 для двустороннего теста!")
                interpretation.append("-> Обнаружена статистически значимая разница")
            else:
                interpretation.append("-> Статистически значимая разница отсутствует")
        else:
            if z_score < critical_value and p_val_z > 0.05:
                interpretation.append("-> Не удаётся отвергнуть нулевую гипотезу")
                interpretation.append("-> Статистически значимая разница отсутствует")
            else:
                interpretation.append("-> Обнаружен статистически значимый результат")

    return "\n".join(interpretation)


def get_summary_stats() -> Dict[str, Any]:
    """Получить сводную статистику для отчётов."""
    if not data_processor.has_clean_data():
        return {}

    df_clean = data_processor.get_df_clean()
    stats = data_processor.get_probability_stats()
    sizes = data_processor.get_sample_sizes()

    return {
        'total_users': len(df_clean),
        'unique_users': df_clean['user_id'].nunique(),
        'overall_conversion_rate': stats['overall_conversion'],
        'control_conversion_rate': stats['control_conversion'],
        'treatment_conversion_rate': stats['treatment_conversion'],
        'conversion_difference': stats['treatment_conversion'] - stats['control_conversion'],
        'new_page_sample_size': sizes.get('n_new', 0),
        'old_page_sample_size': sizes.get('n_old', 0),
    }


def get_simulation_results() -> Dict[str, Any]:
    return STATE['simulation_results']


def get_z_test_results() -> Dict[str, Any]:
    return STATE['z_test_results']
