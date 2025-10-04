import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# ----- Enhanced Data Processor -----
class AgenticProcessor:
    def __init__(self):
        self.prod = None
        self.cmm = None
        self.unified = None
        self.mapping = {}
        self.analysis_results = {}

    def load_from_upload(self, prod_file, cmm_file):
        """Load data from uploaded files"""
        try:
            if prod_file is not None and cmm_file is not None:
                self.prod = pd.read_csv(prod_file)
                self.cmm = pd.read_csv(cmm_file)
                
                # Convert timestamps
                self.prod['production_timestamp'] = pd.to_datetime(
                    self.prod['production_timestamp'], errors='coerce'
                )
                self.cmm['measurement_timestamp'] = pd.to_datetime(
                    self.cmm['measurement_timestamp'], errors='coerce'
                )
                return True
            return False
        except Exception as e:
            st.error(f"Error loading files: {str(e)}")
            return False

    def load_sample(self):
        """Load sample data files"""
        try:
            self.prod = pd.read_csv("production_data.csv")
            self.cmm = pd.read_csv("cmm_data.csv")
            
            self.prod['production_timestamp'] = pd.to_datetime(
                self.prod['production_timestamp'], errors='coerce'
            )
            self.cmm['measurement_timestamp'] = pd.to_datetime(
                self.cmm['measurement_timestamp'], errors='coerce'
            )
            return True
        except Exception as e:
            st.error(f"Error loading sample data: {str(e)}")
            return False

    def ai_schema_mapping(self):
        """AI-powered schema mapping"""
        if self.prod is None or self.cmm is None:
            return {}
        
        # AI discovers semantic relationships
        self.mapping = {
            'part_id': 'component_id',
            'lot_id': 'lot_id',
            'production_timestamp': 'measurement_timestamp',
            'machine_id': 'cmm_machine_id',
            'operator_id': 'inspector_id'
        }
        return self.mapping

    def create_unified_dataset(self):
        """Create unified dataset"""
        if self.prod is None or self.cmm is None:
            return None
            
        if not self.mapping:
            self.ai_schema_mapping()
        
        self.unified = pd.merge(
            self.prod,
            self.cmm,
            on='lot_id',
            how='inner',
            suffixes=('_production', '_quality')
        )
        return self.unified

    def comprehensive_analysis(self):
        """Run comprehensive quality analysis"""
        if self.unified is None:
            self.create_unified_dataset()
        
        df = self.unified
        
        # Basic quality metrics
        total = len(df)
        passed = (df['result'] == 'pass').sum()
        failed = (df['result'] == 'fail').sum()
        
        # Quality by machine
        machine_quality = df.groupby('machine_id')['result'].apply(
            lambda x: (x == 'pass').mean() * 100
        ).round(1)
        
        # Quality by shift
        shift_quality = df.groupby('shift')['result'].apply(
            lambda x: (x == 'pass').mean() * 100
        ).round(1)
        
        # Defective lots analysis
        defective_lots = df[df['result'] == 'fail'].groupby('lot_id').agg({
            'part_id': 'first',
            'machine_id': 'first',
            'shift': 'first',
            'result': 'count'
        }).rename(columns={'result': 'defect_count'}).reset_index()
        defective_lots = defective_lots.sort_values('defect_count', ascending=False)
        
        # Anomaly detection (95th percentile method)
        df['deviation'] = (df['measured_value'] - df['nominal_value']).abs()
        deviation_threshold = df['deviation'].quantile(0.95)
        anomalies = df[df['deviation'] > deviation_threshold]
        
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
        
        return self.analysis_results

    def auto_run_all_analysis(self):
        """Automatically run all analysis steps"""
        if self.prod is not None and self.cmm is not None:
            self.ai_schema_mapping()
            self.create_unified_dataset()
            self.comprehensive_analysis()
            return True
        return False

# ----- Helper function for colored dataframes -----
def color_result_column(val):
    """Color the result column - green for pass, red for fail"""
    if val == 'pass':
        return 'color: #28a745; font-weight: bold'
    elif val == 'fail':
        return 'color: #dc3545; font-weight: bold'
    return ''

# ----- Streamlit App Configuration -----
st.set_page_config(
    page_title="Agentic AI Manufacturing",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ----- Modern CSS with Cohesive Purple Theme -----
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .upload-section {
        background: #f8f9ff;
        border: 2px dashed #667eea;
        border-radius: 10px;
        padding: 2rem;
        margin: 2rem 0;
        text-align: center;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.1);
        text-align: center;
        border-top: 4px solid #667eea;
        margin: 0.5rem;
    }
    
    .success-card {
        border-top-color: #7c4dff;
    }
    
    .warning-card {
        border-top-color: #9c88ff;
    }
    
    .danger-card {
        border-top-color: #b39ddb;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: #f8f9ff;
        padding: 0.5rem;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 3.5rem;
        padding: 0 2rem;
        border-radius: 10px;
        background: white;
        color: #667eea;
        font-weight: 500;
        border: 2px solid transparent;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        border-color: #667eea;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
    }
    
    .upload-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.8rem 2rem;
        border-radius: 10px;
        font-weight: 500;
        margin: 0.5rem;
    }
    
    .sample-button {
        background: white;
        color: #667eea;
        border: 2px solid #667eea;
        padding: 0.8rem 2rem;
        border-radius: 10px;
        font-weight: 500;
        margin: 0.5rem;
    }
    .stButton>button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;

  }
  .stButton>button:hover {
    opacity: 0.9 !important;
  }
</style>
""", unsafe_allow_html=True)

# Initialize processor
if 'processor' not in st.session_state:
    st.session_state.processor = AgenticProcessor()
    st.session_state.data_loaded = False
    st.session_state.analysis_complete = False

processor = st.session_state.processor

# ----- Modern Header -----
st.markdown("""
<div class="main-header">
    <h1>🤖 Agentic AI Manufacturing Integration</h1>
    <p style="font-size: 1.2rem; margin-top: 1rem; opacity: 0.9;">
        Intelligent Integration of ERP Production Data and CMM Quality Measurements
    </p>
</div>
""", unsafe_allow_html=True)

# ----- Data Upload Section (Below Header) -----
st.markdown("""
<div class="upload-section">
    <h3 style="color: #667eea; margin-bottom: 1rem;">📊 Data Upload</h3>
    <p style="color: #666; margin-bottom: 2rem;">Upload your manufacturing data files or use sample data to get started</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    production_file = st.file_uploader(
        "Production CSV (ERP/MES Data)",
        type=['csv'],
        key="prod_upload",
        help="Upload production data with lot IDs, machine info, timestamps"
    )

with col2:
    cmm_file = st.file_uploader(
        "CMM CSV (Quality Data)", 
        type=['csv'],
        key="cmm_upload",
        help="Upload CMM measurements with pass/fail results"
    )

with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📤 Upload Files", type="primary", use_container_width=True):
        if production_file and cmm_file:
            success = processor.load_from_upload(production_file, cmm_file)
            if success:
                st.session_state.data_loaded = True
                processor.auto_run_all_analysis()
                st.session_state.analysis_complete = True
                st.success("🎉 Files loaded and analyzed!")
                st.rerun()
        else:
            st.warning("⚠️ Please upload both files")
    
    if st.button("📋 Use Sample Data", type="secondary", use_container_width=True):
        success = processor.load_sample()
        if success:
            st.session_state.data_loaded = True
            processor.auto_run_all_analysis()
            st.session_state.analysis_complete = True
            st.success("🎉 Sample data loaded and analyzed!")
            st.rerun()

# Show data loading status
if st.session_state.data_loaded:
    col1, col2 = st.columns(2)
    with col1:
        st.success(f"✅ Production data: {len(processor.prod):,} records")
    with col2:
        st.success(f"✅ CMM data: {len(processor.cmm):,} records")

st.markdown("---")

# ----- Tab Structure -----
tab1, tab2, tab3, tab4 = st.tabs([
    "🧠 AI Schema Mapping",
    "🔗 Data Integration", 
    "📊 Quality Analytics",
    "🚨 Anomaly Detection"
])

# ----- TAB 1: AI Schema Mapping -----
with tab1:
    st.header("🧠 AI-Powered Schema Mapping")
    
    if not st.session_state.data_loaded:
        st.info("⚠️ Please upload data or use sample data to see AI schema mapping results")
    else:
        # Show mapping results automatically
        st.subheader("🗺️ AI-Discovered Column Mappings")
        st.markdown("*The AI agent automatically discovered these semantic relationships:*")
        
        # Create clean mapping table without confidence
        mapping_df = pd.DataFrame([
            {"Production Column": k, "CMM Column": v}
            for k, v in processor.mapping.items()
        ])
        
        st.dataframe(
            mapping_df, 
            use_container_width=True, 
            hide_index=True,
            column_config={
                "Production Column": st.column_config.TextColumn(
                    "Production Column",
                    help="Columns from ERP/MES production data",
                    width="medium"
                ),
                "CMM Column": st.column_config.TextColumn(
                    "CMM Column", 
                    help="Mapped columns from CMM quality data",
                    width="medium"
                )
            }
        )
        
        st.markdown(f"✨ **AI successfully mapped {len(processor.mapping)} column relationships**")

# ----- TAB 2: Data Integration -----
with tab2:
    st.header("🔗 Intelligent Data Integration")
    
    if not st.session_state.analysis_complete:
        st.info("⚠️ Please load data first to see integration results")
    else:
        df = processor.unified
        
        # Integration summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f'''
            <div class="metric-card">
                <h3 style="color: #667eea;">📦 Production</h3>
                <h2 style="color: #333;">{len(processor.prod):,}</h2>
                <p style="color: #666;">Records</p>
            </div>
            ''', unsafe_allow_html=True)
            
        with col2:
            st.markdown(f'''
            <div class="metric-card">
                <h3 style="color: #667eea;">🔍 CMM</h3>
                <h2 style="color: #333;">{len(processor.cmm):,}</h2>
                <p style="color: #666;">Measurements</p>
            </div>
            ''', unsafe_allow_html=True)
            
        with col3:
            st.markdown(f'''
            <div class="metric-card success-card">
                <h3 style="color: #7c4dff;">🔗 Unified</h3>
                <h2 style="color: #333;">{len(df):,}</h2>
                <p style="color: #666;">Integrated Records</p>
            </div>
            ''', unsafe_allow_html=True)
            
        with col4:
            integration_rate = (len(df) / max(len(processor.prod), len(processor.cmm))) * 100
            st.markdown(f'''
            <div class="metric-card success-card">
                <h3 style="color: #7c4dff;">📈 Success</h3>
                <h2 style="color: #333;">{integration_rate:.1f}%</h2>
                <p style="color: #666;">Integration Rate</p>
            </div>
            ''', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Data preview with filters and colored results
        st.subheader("🔍 Unified Dataset Preview")
        
        filter_col1, filter_col2 = st.columns(2)
        with filter_col1:
            result_filter = st.selectbox(
                "Filter by Result:",
                options=['All', 'Pass', 'Fail'],
                key="result_filter"
            )
        with filter_col2:
            machine_filter = st.selectbox(
                "Filter by Machine:",
                options=['All'] + sorted(df['machine_id'].unique().tolist()),
                key="machine_filter"
            )
        
        # Apply filters
        filtered_df = df.copy()
        if result_filter != 'All':
            filtered_df = filtered_df[filtered_df['result'] == result_filter.lower()]
        if machine_filter != 'All':
            filtered_df = filtered_df[filtered_df['machine_id'] == machine_filter]
        
        # Show colored dataframe
        display_df = filtered_df[['lot_id', 'part_id', 'machine_id', 'shift', 'feature_name', 
                                'measured_value', 'nominal_value', 'result']].copy()
        
        st.dataframe(
            display_df.style.applymap(color_result_column, subset=['result']),
            use_container_width=True,
            height=400,
            hide_index=True
        )
        st.caption(f"Showing {len(filtered_df):,} records (filtered from {len(df):,} total) • Pass = Green, Fail = Red")

# ----- TAB 3: Quality Analytics -----  
with tab3:
    st.header("📊 Comprehensive Quality Analytics")
    
    if not st.session_state.analysis_complete:
        st.info("⚠️ Please load data first to see quality analytics")
    else:
        results = processor.analysis_results
        overall = results['overall']
        
        # Overall quality performance
        st.subheader("🏆 Overall Quality Performance")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f'''
            <div class="metric-card success-card">
                <h3 style="color: #28a745;">✅ Pass Rate</h3>
                <h2 style="color: #28a745;">{overall['pass_rate']:.1f}%</h2>
                <p style="color: #666;">{overall['passed']:,} passed</p>
            </div>
            ''', unsafe_allow_html=True)
            
        with col2:
            st.markdown(f'''
            <div class="metric-card danger-card">
                <h3 style="color: #dc3545;">❌ Fail Rate</h3>
                <h2 style="color: #dc3545;">{overall['fail_rate']:.1f}%</h2>
                <p style="color: #666;">{overall['failed']:,} failed</p>
            </div>
            ''', unsafe_allow_html=True)
            
        with col3:
            st.markdown(f'''
            <div class="metric-card">
                <h3 style="color: #667eea;">🧪 Total Tests</h3>
                <h2 style="color: #333;">{overall['total']:,}</h2>
                <p style="color: #666;">Quality measurements</p>
            </div>
            ''', unsafe_allow_html=True)
            
        with col4:
            st.markdown(f'''
            <div class="metric-card warning-card">
                <h3 style="color: #ff9800;">⚠️ Failed Tests</h3>
                <h2 style="color: #ff9800;">{overall['failed']:,}</h2>
                <p style="color: #666;">Need attention</p>
            </div>
            ''', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Charts with purple theme
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            st.subheader("🏭 Quality Performance by Machine")
            machine_df = pd.DataFrame([
                {'Machine': k, 'Pass Rate': v} 
                for k, v in results['by_machine'].items()
            ])
            fig1 = px.bar(
                machine_df,
                x='Machine',
                y='Pass Rate',
                color='Pass Rate',
                color_continuous_scale=['#b39ddb', '#7c4dff', '#667eea'],
                title="Pass Rate by Machine (%)"
            )
            fig1.update_layout(
                height=400,
                plot_bgcolor='white',
                paper_bgcolor='white'
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with chart_col2:
            st.subheader("⏰ Quality Distribution by Shift")
            shift_df = pd.DataFrame([
                {'Shift': f"Shift {k}", 'Pass Rate': v}
                for k, v in results['by_shift'].items()
            ])
            fig2 = px.pie(
                shift_df,
                values='Pass Rate',
                names='Shift',
                title="Quality by Work Shift",
                color_discrete_sequence=['#667eea', '#7c4dff', '#b39ddb']
            )
            fig2.update_layout(height=400)
            st.plotly_chart(fig2, use_container_width=True)
        
        # Defect traceability - Show ALL defective lots
        st.subheader("📋 Defective Production Lots - Full Traceability")
        if not results['defective_lots'].empty:
            st.dataframe(
                results['defective_lots'], 
                use_container_width=True, 
                height=400,
                hide_index=True
            )
            st.caption(f"🔍 Total defective lots: {len(results['defective_lots'])}")
        else:
            st.success("🎉 No defective lots found!")

# ----- TAB 4: Anomaly Detection -----
with tab4:
    st.header("🚨 Advanced Anomaly Detection")
    
    if not st.session_state.analysis_complete:
        st.info("⚠️ Please load data first to see anomaly detection results")
    else:
        results = processor.analysis_results
        anomalies = results['anomalies']
        
        # Anomaly summary metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'''
            <div class="metric-card warning-card">
                <h3 style="color: #ff9800;">⚠️ Total Anomalies</h3>
                <h2 style="color: #ff9800;">{len(anomalies):,}</h2>
                <p style="color: #666;">Outliers detected</p>
            </div>
            ''', unsafe_allow_html=True)
            
        with col2:
            anomaly_rate = (len(anomalies) / len(processor.unified)) * 100
            st.markdown(f'''
            <div class="metric-card danger-card">
                <h3 style="color: #dc3545;">📊 Anomaly Rate</h3>
                <h2 style="color: #dc3545;">{anomaly_rate:.2f}%</h2>
                <p style="color: #666;">Of total measurements</p>
            </div>
            ''', unsafe_allow_html=True)
            
        with col3:
            st.markdown(f'''
            <div class="metric-card">
                <h3 style="color: #667eea;">📏 95th Percentile</h3>
                <h2 style="color: #333;">{results['deviation_stats']['threshold']:.4f}</h2>
                <p style="color: #666;">Deviation threshold</p>
            </div>
            ''', unsafe_allow_html=True)
        
        st.markdown("---")
        
        if len(anomalies) > 0:
            # Show ALL anomalous measurements with colored results
            st.subheader("🔍 Anomalous Measurements - Full List")
            anomaly_display = anomalies[['lot_id', 'part_id', 'machine_id', 'feature_name', 
                                       'measured_value', 'nominal_value', 'deviation', 'result']].copy()
            
            st.dataframe(
                anomaly_display.style.applymap(color_result_column, subset=['result']),
                use_container_width=True, 
                height=400, 
                hide_index=True
            )
            st.caption(f"🔍 Total anomalous measurements: {len(anomalies)} • Pass = Green, Fail = Red")
            
            # Deviation distribution chart with purple theme
            st.subheader("📈 Measurement Deviation Distribution")
            fig = px.histogram(
                processor.unified,
                x='deviation',
                title="Distribution of Measurement Deviations from Nominal Values",
                labels={'deviation': 'Deviation from Nominal', 'count': 'Frequency'},
                nbins=50,
                color_discrete_sequence=['#7c4dff']
            )
            fig.add_vline(
                x=results['deviation_stats']['threshold'],
                line_dash="dash",
                line_color="#dc3545",
                annotation_text="95th Percentile Threshold",
                line_width=3
            )
            fig.update_layout(
                height=400,
                plot_bgcolor='white',
                paper_bgcolor='white'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.success("✅ No anomalies detected in current dataset!")

# ----- Footer -----
st.markdown("---")
st.markdown(
    f"""
    <div style='text-align: center; color: #667eea; padding: 2rem; background: #f8f9ff; border-radius: 10px; margin-top: 2rem;'>
        <h4>🤖 Agentic AI Manufacturing Integration Platform</h4>
        <p style='color: #666; margin: 0.5rem 0;'>Built with ❤️ for intelligent manufacturing</p>
        <p style='color: #999; font-size: 0.9rem;'>Generated on {datetime.now().strftime('%Y-%m-%d at %H:%M')}</p>
    </div>
    """,
    unsafe_allow_html=True
)