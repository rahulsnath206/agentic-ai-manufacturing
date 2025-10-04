"""
Agentic AI Manufacturing Data Integration System
Core data processing and AI-powered schema mapping module
"""

import pandas as pd
import numpy as np
from datetime import datetime
import json
import logging
from typing import Dict, List, Tuple, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataProcessor:
    """
    Core data processing class for manufacturing data integration
    """
    
    def __init__(self):
        self.production_data = None
        self.cmm_data = None
        self.unified_data = None
        self.schema_mapping = {}
        
    def load_data(self, production_file: str, cmm_file: str) -> bool:
        """
        Load production and CMM data from CSV files
        
        Args:
            production_file: Path to production data CSV
            cmm_file: Path to CMM data CSV
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            logger.info("Loading production data...")
            self.production_data = pd.read_csv(production_file)
            
            logger.info("Loading CMM data...")
            self.cmm_data = pd.read_csv(cmm_file)
            
            # Clean and standardize timestamps
            self.production_data['production_timestamp'] = pd.to_datetime(
                self.production_data['production_timestamp']
            )
            self.cmm_data['measurement_timestamp'] = pd.to_datetime(
                self.cmm_data['measurement_timestamp']
            )
            
            logger.info(f"Production data loaded: {self.production_data.shape}")
            logger.info(f"CMM data loaded: {self.cmm_data.shape}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            return False
    
    def analyze_data_structure(self) -> Dict[str, Any]:
        """
        Analyze the structure of both datasets
        
        Returns:
            Dict containing analysis results
        """
        if self.production_data is None or self.cmm_data is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        analysis = {
            'production_data': {
                'shape': self.production_data.shape,
                'columns': list(self.production_data.columns),
                'dtypes': self.production_data.dtypes.to_dict(),
                'null_counts': self.production_data.isnull().sum().to_dict(),
                'unique_counts': {col: self.production_data[col].nunique() 
                                for col in self.production_data.columns}
            },
            'cmm_data': {
                'shape': self.cmm_data.shape,
                'columns': list(self.cmm_data.columns),
                'dtypes': self.cmm_data.dtypes.to_dict(),
                'null_counts': self.cmm_data.isnull().sum().to_dict(),
                'unique_counts': {col: self.cmm_data[col].nunique() 
                                for col in self.cmm_data.columns}
            }
        }
        
        return analysis
    
    def ai_powered_schema_mapping(self) -> Dict[str, str]:
        """
        Use AI-like techniques to map schema between datasets
        This simulates what an LLM would do - finding semantic similarities
        
        Returns:
            Dict mapping production columns to CMM columns
        """
        logger.info("Performing AI-powered schema mapping...")
        
        # Get column names and create descriptions
        prod_cols = list(self.production_data.columns)
        cmm_cols = list(self.cmm_data.columns)
        
        # Create semantic descriptions for columns
        column_descriptions = {
            # Production columns
            'production_order_id': 'production order identifier number',
            'part_id': 'part component identifier number',
            'lot_id': 'manufacturing lot batch identifier',
            'production_timestamp': 'production manufacturing date time',
            'quantity': 'quantity amount number produced',
            'machine_id': 'machine equipment identifier',
            'operator_id': 'operator worker identifier',
            'shift': 'work shift time period',
            'plant_code': 'plant facility location code',
            'status': 'production status state',
            
            # CMM columns  
            'measurement_id': 'measurement test identifier number',
            'component_id': 'component part identifier number',
            'lot_id': 'manufacturing lot batch identifier',
            'feature_name': 'measured feature characteristic name',
            'nominal_value': 'target nominal specification value',
            'upper_tolerance': 'upper tolerance limit specification',
            'lower_tolerance': 'lower tolerance limit specification', 
            'measured_value': 'actual measured test value',
            'measurement_timestamp': 'measurement test date time',
            'cmm_machine_id': 'cmm measurement machine identifier',
            'inspector_id': 'quality inspector identifier',
            'result': 'test measurement result outcome'
        }
        
        # Use TF-IDF similarity to find matches
        vectorizer = TfidfVectorizer()
        
        # Get descriptions for each dataset
        prod_descriptions = [column_descriptions.get(col, col) for col in prod_cols]
        cmm_descriptions = [column_descriptions.get(col, col) for col in cmm_cols]
        
        # Combine all descriptions for vectorization
        all_descriptions = prod_descriptions + cmm_descriptions
        tfidf_matrix = vectorizer.fit_transform(all_descriptions)
        
        # Calculate similarity matrix
        similarity_matrix = cosine_similarity(
            tfidf_matrix[:len(prod_cols)], 
            tfidf_matrix[len(prod_cols):]
        )
        
        # Find best matches
        mappings = {}
        for i, prod_col in enumerate(prod_cols):
            similarities = similarity_matrix[i]
            best_match_idx = np.argmax(similarities)
            best_score = similarities[best_match_idx]
            
            if best_score > 0.3:  # Threshold for meaningful similarity
                mappings[prod_col] = cmm_cols[best_match_idx]
        
        # Add obvious direct mappings that AI would definitely catch
        obvious_mappings = {
            'part_id': 'component_id',  # These are clearly the same
            'lot_id': 'lot_id'  # Exact match
        }
        
        mappings.update(obvious_mappings)
        self.schema_mapping = mappings
        
        logger.info(f"Schema mapping completed: {mappings}")
        return mappings
    
    def create_unified_dataset(self) -> pd.DataFrame:
        """
        Create unified dataset by merging production and CMM data
        
        Returns:
            pd.DataFrame: Unified dataset
        """
        logger.info("Creating unified dataset...")
        
        if not self.schema_mapping:
            self.ai_powered_schema_mapping()
        
        # Perform the merge based on mapped columns
        # Primary merge on lot_id (which exists in both)
        unified = pd.merge(
            self.production_data,
            self.cmm_data,
            on='lot_id',
            how='inner',
            suffixes=('_prod', '_cmm')
        )
        
        # Additional merge validation on part_id/component_id if available
        if 'part_id' in self.schema_mapping and self.schema_mapping['part_id'] in self.cmm_data.columns:
            # Verify that part_id matches component_id
            part_matches = unified['part_id'] == unified[self.schema_mapping['part_id']]
            logger.info(f"Part ID consistency: {part_matches.sum()}/{len(unified)} records match")
        
        self.unified_data = unified
        logger.info(f"Unified dataset created with {unified.shape[0]} records")
        
        return unified
    
    def calculate_quality_metrics(self) -> Dict[str, Any]:
        """
        Calculate key quality and production metrics
        
        Returns:
            Dict containing calculated metrics
        """
        if self.unified_data is None:
            self.create_unified_dataset()
        
        # Basic quality metrics
        total_measurements = len(self.unified_data)
        passed_measurements = len(self.unified_data[self.unified_data['result'] == 'pass'])
        failed_measurements = len(self.unified_data[self.unified_data['result'] == 'fail'])
        
        pass_rate = (passed_measurements / total_measurements) * 100 if total_measurements > 0 else 0
        fail_rate = (failed_measurements / total_measurements) * 100 if total_measurements > 0 else 0
        
        # Defect traceability by production lot
        defect_by_lot = self.unified_data[self.unified_data['result'] == 'fail'].groupby('lot_id').size()
        
        # Quality by machine
        quality_by_machine = self.unified_data.groupby('machine_id')['result'].apply(
            lambda x: (x == 'pass').sum() / len(x) * 100
        ).to_dict()
        
        # Quality by shift
        quality_by_shift = self.unified_data.groupby('shift')['result'].apply(
            lambda x: (x == 'pass').sum() / len(x) * 100
        ).to_dict()
        
        # Quality by plant
        quality_by_plant = self.unified_data.groupby('plant_code')['result'].apply(
            lambda x: (x == 'pass').sum() / len(x) * 100
        ).to_dict()
        
        metrics = {
            'overall_quality': {
                'total_measurements': total_measurements,
                'passed_measurements': passed_measurements,
                'failed_measurements': failed_measurements,
                'pass_rate_percent': round(pass_rate, 2),
                'fail_rate_percent': round(fail_rate, 2)
            },
            'defect_traceability': {
                'lots_with_defects': len(defect_by_lot),
                'total_lots': self.unified_data['lot_id'].nunique(),
                'worst_lots': defect_by_lot.nlargest(10).to_dict()
            },
            'quality_by_machine': quality_by_machine,
            'quality_by_shift': quality_by_shift,
            'quality_by_plant': quality_by_plant
        }
        
        return metrics
    
    def detect_anomalies(self) -> Dict[str, Any]:
        """
        Detect anomalies in measurement data using statistical methods
        
        Returns:
            Dict containing anomaly detection results
        """
        if self.unified_data is None:
            self.create_unified_dataset()
        
        # Calculate measurement deviations from nominal
        self.unified_data['deviation'] = abs(
            self.unified_data['measured_value'] - self.unified_data['nominal_value']
        )
        
        # Statistical anomaly detection using IQR method
        Q1 = self.unified_data['deviation'].quantile(0.25)
        Q3 = self.unified_data['deviation'].quantile(0.75)
        IQR = Q3 - Q1
        
        # Define outliers
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        anomalies = self.unified_data[
            (self.unified_data['deviation'] < lower_bound) | 
            (self.unified_data['deviation'] > upper_bound)
        ]
        
        # Anomalies by machine
        anomalies_by_machine = anomalies.groupby('machine_id').size().to_dict()
        
        # Anomalies by feature
        anomalies_by_feature = anomalies.groupby('feature_name').size().to_dict()
        
        anomaly_results = {
            'total_anomalies': len(anomalies),
            'anomaly_percentage': round((len(anomalies) / len(self.unified_data)) * 100, 2),
            'deviation_statistics': {
                'mean': round(self.unified_data['deviation'].mean(), 4),
                'std': round(self.unified_data['deviation'].std(), 4),
                'q1': round(Q1, 4),
                'q3': round(Q3, 4),
                'iqr': round(IQR, 4)
            },
            'anomalies_by_machine': anomalies_by_machine,
            'anomalies_by_feature': anomalies_by_feature,
            'top_anomalous_measurements': anomalies.nlargest(10, 'deviation')[
                ['measurement_id', 'part_id', 'lot_id', 'feature_name', 'deviation', 'result']
            ].to_dict('records')
        }
        
        return anomaly_results
    
    def generate_analysis_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive analysis report
        
        Returns:
            Dict containing complete analysis
        """
        logger.info("Generating comprehensive analysis report...")
        
        # Ensure we have unified data
        if self.unified_data is None:
            self.create_unified_dataset()
        
        # Get all metrics
        quality_metrics = self.calculate_quality_metrics()
        anomaly_results = self.detect_anomalies()
        data_analysis = self.analyze_data_structure()
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'data_summary': {
                'production_records': len(self.production_data),
                'cmm_measurements': len(self.cmm_data),
                'unified_records': len(self.unified_data),
                'schema_mapping': self.schema_mapping
            },
            'quality_metrics': quality_metrics,
            'anomaly_detection': anomaly_results,
            'data_structure': data_analysis
        }
        
        logger.info("Analysis report generated successfully")
        return report