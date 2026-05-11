"""
Модуль для загрузки, очистки и валидации данных A/B тестирования.
Реализован в процедурном стиле без использования классов.

Состояние хранится в модульном словаре STATE, который содержит исходный
DataFrame, очищенный DataFrame, ошибки валидации и информацию о
сопоставлении столбцов.
"""

import os
import sys
from typing import Tuple

import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import column_mapper


STATE = {
    'df': None,
    'df_clean': None,
    'validation_errors': [],
    'column_mapping': {},
    'dataset_format': None,
}


def reset_state():
    """Сбросить модульное состояние к начальному виду."""
    STATE['df'] = None
    STATE['df_clean'] = None
    STATE['validation_errors'] = []
    STATE['column_mapping'] = {}
    STATE['dataset_format'] = None


def load_data(file_path: str) -> bool:
    """Загрузить CSV-данные и проверить обязательные столбцы."""
    try:
        df = pd.read_csv(file_path)
        STATE['df'] = df

        dataset_format = column_mapper.detect_format(df)
        mapping, mapping_errors = column_mapper.create_mapping(df, dataset_format)

        STATE['dataset_format'] = dataset_format
        STATE['column_mapping'] = mapping
        STATE['validation_errors'] = list(mapping_errors)

        return _validate_data()
    except Exception as e:
        STATE['validation_errors'].append(f"Ошибка загрузки файла: {str(e)}")
        return False


def load_country_data(file_path: str) -> bool:
    """Загрузить данные о странах и объединить с основным набором данных."""
    try:
        if STATE['df_clean'] is None:
            STATE['validation_errors'].append("Сначала загрузите и очистите основные данные")
            return False

        country_df = pd.read_csv(file_path)
        STATE['df_clean'] = pd.merge(STATE['df_clean'], country_df, on=['user_id'])
        return True
    except Exception as e:
        STATE['validation_errors'].append(f"Ошибка загрузки данных о странах: {str(e)}")
        return False


def _validate_data() -> bool:
    """Проверить наличие обязательных столбцов через сопоставление."""
    if STATE['df'] is None:
        return False

    is_valid, errors = column_mapper.validate_mapping(STATE['df'], STATE['column_mapping'])
    STATE['validation_errors'] = errors
    return is_valid


def get_data_info() -> dict:
    """Получить базовую информацию о наборе данных."""
    df = STATE['df']
    if df is None:
        return {}

    return {
        'shape': df.shape,
        'columns': list(df.columns),
        'missing_values': df.isnull().sum().to_dict(),
        'unique_users': df['user_id'].nunique() if 'user_id' in df.columns else 0,
        'detected_format': STATE['dataset_format'],
        'column_mapping': STATE['column_mapping'],
    }


def count_misaligned() -> int:
    """Подсчитать несоответствующие строки (treatment не совпадает с new_page)."""
    df = STATE['df']
    if df is None:
        return 0

    try:
        df_normalized = column_mapper.normalize_dataframe(df, STATE['column_mapping'])
        misaligned = (
            ((df_normalized['group'] == 'treatment') & (df_normalized['landing_page'] == 'old_page'))
            | ((df_normalized['group'] == 'control') & (df_normalized['landing_page'] == 'new_page'))
        )
        return int(misaligned.sum())
    except Exception:
        return 0


def clean_data() -> Tuple[bool, str]:
    """Очистить данные: удалить несоответствия и дубликаты."""
    df = STATE['df']
    if df is None:
        return False, "Данные не загружены"

    try:
        df_normalized = column_mapper.normalize_dataframe(df, STATE['column_mapping'])

        misaligned = (
            ((df_normalized['group'] == 'treatment') & (df_normalized['landing_page'] == 'old_page'))
            | ((df_normalized['group'] == 'control') & (df_normalized['landing_page'] == 'new_page'))
        )
        df_clean = df_normalized[~misaligned].copy()

        duplicate_mask = df_clean['user_id'].duplicated(keep=False)
        if duplicate_mask.any():
            df_clean = df_clean[~duplicate_mask | (~df_clean['user_id'].duplicated(keep='first'))]

        STATE['df_clean'] = df_clean
        return True, f"Данные успешно очищены. Размерность: {df_clean.shape}"
    except Exception as e:
        return False, f"Ошибка очистки данных: {str(e)}"


def get_probability_stats() -> dict:
    """Рассчитать базовую статистику вероятностей."""
    df_clean = STATE['df_clean']
    if df_clean is None:
        return {}

    stats = {'overall_conversion': (df_clean['converted'] == 1).mean()}

    if 'group' in df_clean.columns:
        control_mask = df_clean['group'] == 'control'
        treatment_mask = df_clean['group'] == 'treatment'
        stats['control_conversion'] = (df_clean.loc[control_mask, 'converted'] == 1).mean()
        stats['treatment_conversion'] = (df_clean.loc[treatment_mask, 'converted'] == 1).mean()

    if 'landing_page' in df_clean.columns:
        stats['new_page_prob'] = (df_clean['landing_page'] == 'new_page').mean()

    return stats


def get_sample_sizes() -> dict:
    """Получить размеры выборок для анализа."""
    df_clean = STATE['df_clean']
    if df_clean is None:
        return {}

    sizes = {}
    if 'landing_page' in df_clean.columns:
        sizes['n_new'] = int((df_clean['landing_page'] == 'new_page').sum())
        sizes['n_old'] = int((df_clean['landing_page'] == 'old_page').sum())

    if 'group' in df_clean.columns:
        sizes['n_control'] = int((df_clean['group'] == 'control').sum())
        sizes['n_treatment'] = int((df_clean['group'] == 'treatment').sum())

    return sizes


def get_conversion_counts() -> dict:
    """Получить количество конверсий для статистических тестов."""
    df_clean = STATE['df_clean']
    if df_clean is None:
        return {}

    counts = {}
    if 'landing_page' in df_clean.columns:
        old_mask = df_clean['landing_page'] == 'old_page'
        new_mask = df_clean['landing_page'] == 'new_page'
        counts['convert_old'] = int((df_clean.loc[old_mask, 'converted'] == 1).sum())
        counts['convert_new'] = int((df_clean.loc[new_mask, 'converted'] == 1).sum())

    return counts


def get_format_info() -> dict:
    """Получить подробную информацию об обнаруженном формате."""
    if STATE['df'] is None:
        return {}
    return column_mapper.get_format_info(
        STATE['dataset_format'], STATE['column_mapping'], STATE['validation_errors']
    )


def get_manual_mapping_suggestions() -> dict:
    """Получить предложения для ручного сопоставления столбцов."""
    if STATE['df'] is None:
        return {}
    return column_mapper.suggest_manual_mapping(STATE['df'])


def get_validation_errors() -> list:
    """Получить список ошибок валидации."""
    return list(STATE['validation_errors'])


def has_raw_data() -> bool:
    return STATE['df'] is not None


def has_clean_data() -> bool:
    return STATE['df_clean'] is not None


def get_df() -> pd.DataFrame:
    return STATE['df']


def get_df_clean() -> pd.DataFrame:
    return STATE['df_clean']
