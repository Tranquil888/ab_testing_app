import pandas as pd
import numpy as np
from typing import Tuple, Optional
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.column_mapper import ColumnMapper

class DataProcessor:
    """Handles data loading, cleaning, and validation for A/B testing analysis."""
    
    def __init__(self):
        self.df = None
        self.df_clean = None
        self.validation_errors = []
        self.column_mapper = ColumnMapper()
        self.dataset_format = None
    
    def load_data(self, file_path: str) -> bool:
        """Load CSV data and validate required columns."""
        try:
            self.df = pd.read_csv(file_path)
            
            # Detect format and create column mapping
            self.dataset_format = self.column_mapper.detect_format(self.df)
            self.column_mapper.create_mapping(self.df, self.dataset_format)
            
            return self._validate_data()
        except Exception as e:
            self.validation_errors.append(f"Error loading file: {str(e)}")
            return False
    
    def load_country_data(self, file_path: str) -> bool:
        """Load country data and merge with main dataset."""
        try:
            if self.df_clean is None:
                self.validation_errors.append("Please load and clean main data first")
                return False
            
            country_df = pd.read_csv(file_path)
            self.df_clean = pd.merge(self.df_clean, country_df, on=['user_id'])
            return True
        except Exception as e:
            self.validation_errors.append(f"Error loading country data: {str(e)}")
            return False
    
    def _validate_data(self) -> bool:
        """Validate required columns are present using column mapping."""
        self.validation_errors.clear()
        
        # Validate using column mapper
        is_valid, errors = self.column_mapper.validate_mapping(self.df)
        self.validation_errors.extend(errors)
        
        return is_valid
    
    def get_data_info(self) -> dict:
        """Get basic information about the dataset."""
        if self.df is None:
            return {}
        
        return {
            'shape': self.df.shape,
            'columns': list(self.df.columns),
            'missing_values': self.df.isnull().sum().to_dict(),
            'unique_users': self.df['user_id'].nunique() if 'user_id' in self.df.columns else 0,
            'detected_format': self.dataset_format,
            'column_mapping': self.column_mapper.column_mapping
        }
    
    def count_misaligned(self) -> int:
        """Count misaligned rows where treatment doesn't match new_page."""
        if self.df is None:
            return 0
        
        try:
            # Normalize column names first
            df_normalized = self.column_mapper.normalize_dataframe(self.df)
            
            misaligned = ((df_normalized['group'] == 'treatment') & (df_normalized['landing_page'] == 'old_page')) | \
                        ((df_normalized['group'] == 'control') & (df_normalized['landing_page'] == 'new_page'))
            return misaligned.sum()
        except:
            return 0
    
    def clean_data(self) -> Tuple[bool, str]:
        """Clean data by removing misaligned rows and duplicates."""
        if self.df is None:
            return False, "No data loaded"
        
        try:
            # Normalize column names first
            df_normalized = self.column_mapper.normalize_dataframe(self.df)
            
            # Remove misaligned rows
            misaligned = ((df_normalized['group'] == 'treatment') & (df_normalized['landing_page'] == 'old_page')) | \
                        ((df_normalized['group'] == 'control') & (df_normalized['landing_page'] == 'new_page'))
            self.df_clean = df_normalized[~misaligned].copy()
            
            # Remove duplicate user_ids
            duplicate_mask = self.df_clean['user_id'].duplicated(keep=False)
            if duplicate_mask.any():
                # Keep first occurrence of each duplicate
                self.df_clean = self.df_clean[~duplicate_mask | 
                                              (~self.df_clean['user_id'].duplicated(keep='first'))]
            
            return True, f"Data cleaned successfully. Shape: {self.df_clean.shape}"
        except Exception as e:
            return False, f"Error cleaning data: {str(e)}"
    
    def get_probability_stats(self) -> dict:
        """Calculate basic probability statistics."""
        if self.df_clean is None:
            return {}
        
        stats = {}
        
        # Overall conversion rate
        stats['overall_conversion'] = (self.df_clean['converted'] == 1).mean()
        
        # Conversion by group
        if 'group' in self.df_clean.columns:
            control_mask = self.df_clean['group'] == 'control'
            treatment_mask = self.df_clean['group'] == 'treatment'
            
            stats['control_conversion'] = (self.df_clean.loc[control_mask, 'converted'] == 1).mean()
            stats['treatment_conversion'] = (self.df_clean.loc[treatment_mask, 'converted'] == 1).mean()
        
        # Page distribution
        if 'landing_page' in self.df_clean.columns:
            stats['new_page_prob'] = (self.df_clean['landing_page'] == 'new_page').mean()
        
        return stats
    
    def get_sample_sizes(self) -> dict:
        """Get sample sizes for analysis."""
        if self.df_clean is None:
            return {}
        
        sizes = {}
        if 'landing_page' in self.df_clean.columns:
            sizes['n_new'] = (self.df_clean['landing_page'] == 'new_page').sum()
            sizes['n_old'] = (self.df_clean['landing_page'] == 'old_page').sum()
        
        if 'group' in self.df_clean.columns:
            sizes['n_control'] = (self.df_clean['group'] == 'control').sum()
            sizes['n_treatment'] = (self.df_clean['group'] == 'treatment').sum()
        
        return sizes
    
    def get_conversion_counts(self) -> dict:
        """Get conversion counts for statistical tests."""
        if self.df_clean is None:
            return {}
        
        counts = {}
        if 'landing_page' in self.df_clean.columns:
            old_mask = self.df_clean['landing_page'] == 'old_page'
            new_mask = self.df_clean['landing_page'] == 'new_page'
            
            counts['convert_old'] = (self.df_clean.loc[old_mask, 'converted'] == 1).sum()
            counts['convert_new'] = (self.df_clean.loc[new_mask, 'converted'] == 1).sum()
        
        return counts
    
    def get_format_info(self) -> dict:
        """Get detailed information about the detected dataset format."""
        if self.df is None:
            return {}
        
        return self.column_mapper.get_format_info()
    
    def get_manual_mapping_suggestions(self) -> dict:
        """Get suggestions for manual column mapping."""
        if self.df is None:
            return {}
        
        return self.column_mapper.suggest_manual_mapping(self.df)
