"""
Simple test script to validate the Agentic AI Manufacturing Data Integration system
Run this to ensure everything is working correctly before the demo
"""

import sys
import os
from datetime import datetime

def test_imports():
    """Test if all required libraries can be imported"""
    print("🧪 Testing imports...")
    
    try:
        import pandas as pd
        import numpy as np
        import plotly.express as px
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        print("✅ All libraries imported successfully!")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_data_files():
    """Test if data files exist and are readable"""
    print("\n📁 Testing data files...")
    
    files_to_check = ['production_data.csv', 'cmm_data.csv']
    
    for file in files_to_check:
        if os.path.exists(file):
            try:
                import pandas as pd
                df = pd.read_csv(file)
                print(f"✅ {file}: {df.shape[0]} rows, {df.shape[1]} columns")
            except Exception as e:
                print(f"❌ Error reading {file}: {e}")
                return False
        else:
            print(f"❌ File not found: {file}")
            return False
    
    return True

def test_data_processor():
    """Test the core DataProcessor functionality"""
    print("\n🤖 Testing AI DataProcessor...")
    
    try:
        from data_processor import DataProcessor
        
        # Initialize processor
        processor = DataProcessor()
        print("✅ DataProcessor initialized")
        
        # Load data
        success = processor.load_data('production_data.csv', 'cmm_data.csv')
        if not success:
            print("❌ Failed to load data")
            return False
        print("✅ Data loaded successfully")
        
        # Test schema mapping
        mapping = processor.ai_powered_schema_mapping()
        print(f"✅ Schema mapping completed: {len(mapping)} mappings found")
        
        # Test unified dataset creation
        unified = processor.create_unified_dataset()
        print(f"✅ Unified dataset created: {len(unified)} records")
        
        # Test metrics calculation
        metrics = processor.calculate_quality_metrics()
        print(f"✅ Quality metrics calculated: {metrics['overall_quality']['pass_rate_percent']}% pass rate")
        
        # Test anomaly detection
        anomalies = processor.detect_anomalies()
        print(f"✅ Anomaly detection completed: {anomalies['total_anomalies']} anomalies found")
        
        return True
        
    except Exception as e:
        print(f"❌ DataProcessor test failed: {e}")
        return False

def test_streamlit_components():
    """Test if Streamlit app can be imported"""
    print("\n🎛️ Testing Streamlit components...")
    
    try:
        import streamlit as st
        print("✅ Streamlit imported successfully")
        
        # Try importing the app (but don't run it)
        sys.path.append('.')
        # We can't actually import the streamlit app without running it,
        # but we can check if the file exists and has the right structure
        if os.path.exists('streamlit_app.py'):
            with open('streamlit_app.py', 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                if 'def main()' in content and 'st.set_page_config' in content:
                    print("✅ Streamlit app structure validated")
                    return True
                else:
                    print("❌ Streamlit app missing required components")
                    return False
        else:
            print("❌ streamlit_app.py not found")
            return False
            
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False

def run_integration_test():
    """Run a complete integration test"""
    print("\n🔗 Running integration test...")
    
    try:
        from data_processor import DataProcessor
        
        processor = DataProcessor()
        
        # Load data
        processor.load_data('production_data.csv', 'cmm_data.csv')
        
        # Run complete analysis
        report = processor.generate_analysis_report()
        
        # Validate report structure
        required_keys = ['timestamp', 'data_summary', 'quality_metrics', 'anomaly_detection']
        for key in required_keys:
            if key not in report:
                print(f"❌ Missing key in report: {key}")
                return False
        
        print("✅ Integration test passed - full workflow functional")
        
        # Print summary
        print(f"\n📊 INTEGRATION TEST SUMMARY:")
        print(f"   Production records: {report['data_summary']['production_records']:,}")
        print(f"   CMM measurements: {report['data_summary']['cmm_measurements']:,}")
        print(f"   Unified records: {report['data_summary']['unified_records']:,}")
        print(f"   Pass rate: {report['quality_metrics']['overall_quality']['pass_rate_percent']}%")
        print(f"   Anomalies found: {report['anomaly_detection']['total_anomalies']:,}")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 AGENTIC AI MANUFACTURING INTEGRATION - SYSTEM TEST")
    print("=" * 60)
    print(f"⏰ Test started at: {datetime.now()}")
    
    tests = [
        ("Library Imports", test_imports),
        ("Data Files", test_data_files), 
        ("AI DataProcessor", test_data_processor),
        ("Streamlit Components", test_streamlit_components),
        ("Integration Test", run_integration_test)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print(f"\n{'='*60}")
    print("🎯 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<25} {status}")
        if result:
            passed += 1
    
    print(f"\n📊 Overall: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("\n🎉 ALL TESTS PASSED! System is ready for demo!")
        print("\n🚀 To run the application:")
        print("   1. Streamlit GUI: streamlit run streamlit_app.py")
        print("   2. Jupyter Notebook: jupyter notebook agentic-ai-prototype.ipynb")
        print("\n💡 You're ready to impress the interviewers!")
    else:
        print(f"\n⚠️ {len(tests) - passed} test(s) failed. Please fix issues before demo.")
    
    print(f"\n⏰ Test completed at: {datetime.now()}")

if __name__ == "__main__":
    main()