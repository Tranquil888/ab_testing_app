"""
Сопоставление столбцов для различных форматов наборов данных A/B тестов.
Реализовано в процедурном стиле без использования классов.
"""

import pandas as pd
from typing import Dict, List, Optional, Tuple


COLUMN_MAPPINGS = {
    'standard': {
        'user_id': ['user_id'],
        'group': ['group'],
        'landing_page': ['landing_page'],
        'converted': ['converted'],
    },
    'alternative': {
        'user_id': ['id'],
        'group': ['con_treat'],
        'landing_page': ['page'],
        'converted': ['converted'],
    },
    'generic': {
        'user_id': ['user_id', 'id', 'user', 'customer_id', 'participant_id'],
        'group': ['group', 'con_treat', 'treatment', 'variant', 'test_group', 'experiment_group'],
        'landing_page': ['landing_page', 'page', 'version', 'variant_page', 'test_page'],
        'converted': ['converted', 'conversion', 'success', 'clicked', 'purchased', 'action'],
    },
}

REQUIRED_COLUMNS = ['user_id', 'group', 'landing_page', 'converted']


def detect_format(df: pd.DataFrame) -> str:
    """Определить формат набора данных по именам столбцов."""
    columns = [col.lower().strip() for col in df.columns]

    if 'user_id' in columns and 'group' in columns and 'landing_page' in columns:
        return 'standard'
    elif 'id' in columns and 'con_treat' in columns and 'page' in columns:
        return 'alternative'

    return 'generic'


def create_mapping(df: pd.DataFrame, format_type: Optional[str] = None) -> Tuple[Dict[str, str], List[str]]:
    """
    Создать сопоставление столбцов для набора данных.
    Возвращает кортеж (mapping, errors).
    """
    if format_type is None:
        format_type = detect_format(df)

    columns_lower = [col.lower().strip() for col in df.columns]
    mapping = {}
    errors = []

    format_mappings = COLUMN_MAPPINGS[format_type]

    for standard_col, possible_names in format_mappings.items():
        found_col = None
        for possible_name in possible_names:
            if possible_name in columns_lower:
                found_col = df.columns[columns_lower.index(possible_name)]
                break
            for col in columns_lower:
                if possible_name.lower() in col.lower():
                    found_col = df.columns[columns_lower.index(col)]
                    break
            if found_col:
                break

        if found_col:
            mapping[standard_col] = found_col
        else:
            errors.append(f"Не удалось найти столбец для {standard_col}")

    return mapping, errors


def validate_mapping(df: pd.DataFrame, mapping: Dict[str, str]) -> Tuple[bool, List[str]]:
    """Проверить, что сопоставление покрывает все обязательные столбцы."""
    errors = []

    for col in REQUIRED_COLUMNS:
        if col not in mapping:
            errors.append(f"Отсутствует обязательный столбец: {col}")
        elif mapping[col] not in df.columns:
            errors.append(f"Сопоставленный столбец '{mapping[col]}' не найден в наборе данных")

    return len(errors) == 0, errors


def normalize_dataframe(df: pd.DataFrame, mapping: Dict[str, str]) -> pd.DataFrame:
    """Нормализовать имена столбцов согласно сопоставлению."""
    if not mapping:
        raise ValueError("Сопоставление столбцов отсутствует. Сначала вызовите create_mapping().")

    df_normalized = df.copy()
    reverse_mapping = {v: k for k, v in mapping.items()}
    df_normalized = df_normalized.rename(columns=reverse_mapping)

    return df_normalized


def get_format_info(detected_format: Optional[str], mapping: Dict[str, str], errors: List[str]) -> Dict[str, object]:
    """Получить информацию об обнаруженном формате."""
    return {
        'detected_format': detected_format,
        'column_mapping': mapping,
        'validation_errors': errors,
        'is_valid': len(errors) == 0,
    }


def suggest_manual_mapping(df: pd.DataFrame) -> Dict[str, List[str]]:
    """Предложить варианты ручного сопоставления столбцов."""
    columns_lower = [col.lower().strip() for col in df.columns]
    suggestions = {}

    for standard_col, possible_names in COLUMN_MAPPINGS['generic'].items():
        matching_cols = []
        for col in columns_lower:
            for possible_name in possible_names:
                if possible_name.lower() in col.lower():
                    matching_cols.append(df.columns[columns_lower.index(col)])
                    break
        suggestions[standard_col] = matching_cols

    return suggestions
