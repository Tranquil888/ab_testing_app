import pandas as pd
from typing import Dict, List, Optional, Tuple

class ColumnMapper:
    """Handles column mapping for different A/B testing dataset formats."""
    
    # Predefined mappings for known dataset formats
    COLUMN_MAPPINGS = {
        'standard': {
            'user_id': ['user_id'],
            'group': ['group'],
            'landing_page': ['landing_page'],
            'converted': ['converted']
        },
        'alternative': {
            'user_id': ['id'],
            'group': ['con_treat'],
            'landing_page': ['page'],
            'converted': ['converted']
        },
        'generic': {
            'user_id': ['user_id', 'id', 'user', 'customer_id', 'participant_id'],
            'group': ['group', 'con_treat', 'treatment', 'variant', 'test_group', 'experiment_group'],
            'landing_page': ['landing_page', 'page', 'version', 'variant_page', 'test_page'],
            'converted': ['converted', 'conversion', 'success', 'clicked', 'purchased', 'action']
        }
    }
    
    def __init__(self):
        self.detected_format = None
        self.column_mapping = {}
        self.validation_errors = []
    
    def detect_format(self, df: pd.DataFrame) -> str:
        """Detect the dataset format based on column names."""
        columns = [col.lower().strip() for col in df.columns]
        
        # Check for exact matches first
        if 'user_id' in columns and 'group' in columns and 'landing_page' in columns:
            return 'standard'
        elif 'id' in columns and 'con_treat' in columns and 'page' in columns:
            return 'alternative'
        
        # Use generic mapping for other formats
        return 'generic'
    
    def create_mapping(self, df: pd.DataFrame, format_type: Optional[str] = None) -> Dict[str, str]:
        """Create column mapping for the dataset."""
        if format_type is None:
            format_type = self.detect_format(df)
        
        self.detected_format = format_type
        columns = [col.lower().strip() for col in df.columns]
        mapping = {}
        
        # Get the appropriate mapping dictionary
        format_mappings = self.COLUMN_MAPPINGS[format_type]
        
        for standard_col, possible_names in format_mappings.items():
            found_col = None
            for possible_name in possible_names:
                # Look for exact match first
                if possible_name in columns:
                    found_col = df.columns[columns.index(possible_name)]
                    break
                # Look for partial match (contains)
                for col in columns:
                    if possible_name.lower() in col.lower():
                        found_col = df.columns[columns.index(col)]
                        break
                if found_col:
                    break
            
            if found_col:
                mapping[standard_col] = found_col
            else:
                self.validation_errors.append(f"Could not find column for {standard_col}")
        
        self.column_mapping = mapping
        return mapping
    
    def validate_mapping(self, df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """Validate that the mapping covers all required columns."""
        required_columns = ['user_id', 'group', 'landing_page', 'converted']
        errors = []
        
        for col in required_columns:
            if col not in self.column_mapping:
                errors.append(f"Missing required column: {col}")
            elif self.column_mapping[col] not in df.columns:
                errors.append(f"Mapped column '{self.column_mapping[col]}' not found in dataset")
        
        self.validation_errors = errors
        return len(errors) == 0, errors
    
    def normalize_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normalize column names using the mapping."""
        if not self.column_mapping:
            raise ValueError("No column mapping available. Call create_mapping() first.")
        
        # Create a copy to avoid modifying original
        df_normalized = df.copy()
        
        # Rename columns according to mapping
        reverse_mapping = {v: k for k, v in self.column_mapping.items()}
        df_normalized = df_normalized.rename(columns=reverse_mapping)
        
        return df_normalized
    
    def get_format_info(self) -> Dict[str, any]:
        """Get information about the detected format."""
        return {
            'detected_format': self.detected_format,
            'column_mapping': self.column_mapping,
            'validation_errors': self.validation_errors,
            'is_valid': len(self.validation_errors) == 0
        }
    
    def suggest_manual_mapping(self, df: pd.DataFrame) -> Dict[str, List[str]]:
        """Suggest manual column mapping options."""
        columns = [col.lower().strip() for col in df.columns]
        suggestions = {}
        
        for standard_col, possible_names in self.COLUMN_MAPPINGS['generic'].items():
            matching_cols = []
            for col in columns:
                for possible_name in possible_names:
                    if possible_name.lower() in col.lower():
                        matching_cols.append(df.columns[columns.index(col)])
                        break
            suggestions[standard_col] = matching_cols
        
        return suggestions
