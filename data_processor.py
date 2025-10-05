"""
Agentic AI Manufacturing Data Integration System
Core data processing and AI-powered schema mapping module
"""

import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgenticProcessor:
    """
    Enhanced Data Processor for Manufacturing Data Integration
    Handles all data operations, AI schema mapping, and analysis
    """
    
    def __init__(self):
        """Initialize the processor with empty state"""
        self.prod = None
        self.cmm = None
        self.unified = None
        self.mapping = {}
        self.analysis_results = {}
        logger.info("AgenticProcessor initialized")

    def load_from_upload(self, prod_file, cmm_file):
        """
        Load data from uploaded Streamlit file objects
        
        Args:
            prod_file: Streamlit uploaded file object for production data
            cmm_file: Streamlit uploaded file object for CMM data
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if prod_file is not None and cmm_file is not None:
                logger.info("Loading data from uploaded files...")
                
                # Load CSV data from uploaded files
                self.prod = pd.read_csv(prod_file)
                self.cmm = pd.read_csv(cmm_file)
                
                # Convert timestamps to datetime
                self.prod['production_timestamp'] = pd.to_datetime(
                    self.prod['production_timestamp'], errors='coerce'
                )
                self.cmm['measurement_timestamp'] = pd.to_datetime(
                    self.cmm['measurement_timestamp'], errors='coerce'
                )
                
                logger.info(f"Production data loaded: {self.prod.shape}")
                logger.info(f"CMM data loaded: {self.cmm.shape}")
                return True
                
            return False
            
        except Exception as e:
            logger.error(f"Error loading uploaded files: {str(e)}")
            st.error(f"Error loading files: {str(e)}")
            return False

    def load_sample(self):
        """
        Load sample data files from disk
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            logger.info("Loading sample data files...")
            
            # Load sample CSV files
            self.prod = pd.read_csv("production_data.csv")
            self.cmm = pd.read_csv("cmm_data.csv")
            
            # Convert timestamps to datetime
            self.prod['production_timestamp'] = pd.to_datetime(
                self.prod['production_timestamp'], errors='coerce'
            )
            self.cmm['measurement_timestamp'] = pd.to_datetime(
                self.cmm['measurement_timestamp'], errors='coerce'
            )
            
            logger.info(f"Sample production data loaded: {self.prod.shape}")
            logger.info(f"Sample CMM data loaded: {self.cmm.shape}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading sample data: {str(e)}")
            st.error(f"Error loading sample data: {str(e)}")
            return False

    def ai_schema_mapping(self):
        """
        AI-powered schema mapping between production and CMM datasets
        Discovers semantic relationships between columns
        
        Returns:
            dict: Mapping of production columns to CMM columns
        """
        if self.prod is None or self.cmm is None:
            logger.warning("Data not loaded for schema mapping")
            return {}
        
        logger.info("Performing AI-powered schema mapping...")
        
        # AI discovers semantic relationships between datasets
        # This simulates what an AI agent would determine
        self.mapping = {
            'part_id': 'component_id',           # Product/component identifier
            'lot_id': 'lot_id',                  # Manufacturing batch identifier
            'production_timestamp': 'measurement_timestamp',  # Time correlation
            'machine_id': 'cmm_machine_id',      # Equipment relationship
            'operator_id': 'inspector_id'        # Personnel correlation
        }
        
        logger.info(f"Schema mapping completed: {len(self.mapping)} relationships found")
        return self.mapping

    def create_unified_dataset(self):
        """
        Create unified dataset by merging production and CMM data
        Uses AI-discovered schema mappings for integration
        
        Returns:
            pd.DataFrame: Unified dataset with merged production and quality data
        """
        if self.prod is None or self.cmm is None:
            logger.warning("Data not loaded for unification")
            return None
            
        if not self.mapping:
            self.ai_schema_mapping()
        
        logger.info("Creating unified dataset...")
        
        # Merge datasets on lot_id (primary key relationship)
        self.unified = pd.merge(
            self.prod,
            self.cmm,
            on='lot_id',
            how='inner',
            suffixes=('_production', '_quality')
        )
        
        logger.info(f"Unified dataset created with {len(self.unified)} records")
        return self.unified

    def comprehensive_analysis(self):
        """
        Run comprehensive quality and production analysis
        Calculates metrics, identifies defects, and detects anomalies
        
        Returns:
            dict: Complete analysis results with all metrics
        """
        if self.unified is None:
            self.create_unified_dataset()
        
        logger.info("Running comprehensive analysis...")
        df = self.unified
        
        # === OVERALL QUALITY METRICS ===
        total = len(df)
        passed = (df['result'] == 'pass').sum()
        failed = (df['result'] == 'fail').sum()
        
        # === QUALITY BY MACHINE ===
        machine_quality = df.groupby('machine_id')['result'].apply(
            lambda x: (x == 'pass').mean() * 100
        ).round(1)
        
        # === QUALITY BY SHIFT ===
        shift_quality = df.groupby('shift')['result'].apply(
            lambda x: (x == 'pass').mean() * 100
        ).round(1)
        
        # === DEFECTIVE LOTS ANALYSIS ===
        # Group failed measurements by lot for traceability
        defective_lots = df[df['result'] == 'fail'].groupby('lot_id').agg({
            'part_id': 'first',
            'machine_id': 'first', 
            'shift': 'first',
            'result': 'count'
        }).rename(columns={'result': 'defect_count'}).reset_index()
        defective_lots = defective_lots.sort_values('defect_count', ascending=False)
        
        # === ANOMALY DETECTION ===
        # Calculate measurement deviations from nominal values
        df['deviation'] = (df['measured_value'] - df['nominal_value']).abs()
        
        # Use 95th percentile as anomaly threshold (statistical method)
        deviation_threshold = df['deviation'].quantile(0.95)
        anomalies = df[df['deviation'] > deviation_threshold]
        
        # === COMPILE RESULTS ===
        self.analysis_results = {
            'overall': {
                'total': total,
                'passed': passed,
                'failed': failed,
                'pass_rate': (passed / total * 100) if total > 0 else 0,
                'fail_rate': (failed / total * 100) if total > 0 else 0
            },
            'by_machine': machine_quality.to_dict(),
            'by_shift': shift_quality.to_dict(),
            'defective_lots': defective_lots,
            'anomalies': anomalies,
            'deviation_stats': {
                'threshold': deviation_threshold
            }
        }
        
        logger.info("Comprehensive analysis completed")
        return self.analysis_results

    def auto_run_all_analysis(self):
        """
        Automatically run all analysis steps in sequence
        This is the main orchestration method
        
        Returns:
            bool: True if all analysis completed successfully
        """
        if self.prod is not None and self.cmm is not None:
            logger.info("Running full automated analysis pipeline...")
            
            # Step 1: AI Schema Mapping
            self.ai_schema_mapping()
            
            # Step 2: Data Integration
            self.create_unified_dataset()
            
            # Step 3: Comprehensive Analysis
            self.comprehensive_analysis()
            
            logger.info("Full analysis pipeline completed successfully")
            return True
            
        logger.warning("Cannot run analysis - data not loaded")
        return False

    def get_integration_stats(self):
        """
        Get statistics about data integration success
        
        Returns:
            dict: Integration statistics
        """
        if self.prod is None or self.cmm is None or self.unified is None:
            return {}
            
        return {
            'production_records': len(self.prod),
            'cmm_records': len(self.cmm),
            'unified_records': len(self.unified),
            'integration_rate': (len(self.unified) / max(len(self.prod), len(self.cmm))) * 100
        }