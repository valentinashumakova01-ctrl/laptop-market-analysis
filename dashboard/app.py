"""
Laptop Market Analysis Dashboard
Interactive dashboard for laptop data exploration
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.preprocessing import process_full_dataset

# page setup
st.set_page_config(
    page_title="Laptop Market Analysis",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("💻 Laptop Market Analysis Dashboard")
st.markdown("### Interactive Data Exploration Tool")

# Dataload
@st.cache_data
def load_data():
    """Load and cache the laptop dataset"""
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'laptops.csv')
    
    if os.path.exists(data_path):
        df_raw = pd.read_csv(data_path)
        st.info("Data loaded from local cache")
    else:
        st.error("Data file not found")
        st.stop()
    
    # Use preprocessing
    df_prepr = process_full_dataset(df_raw)
    df = fix_outliers(df_prepr)

    return df

with st.spinner("Loading data..."):
    try:
        df = load_data()
        st.success(f"Data loaded successfully! {len(df)} laptops found.")
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.stop()

df_rated = df[df['rating'] > 0].copy()

# Sidebar filters
st.sidebar.header("🔍 Filters")

# Brand filter
brands = ['All'] + sorted(df_rated['brand'].unique().tolist())
selected_brand = st.sidebar.selectbox("Select Brand", brands)

# Price range filter
min_price = int(df_rated['price(in Rs.)'].min())
max_price = int(df_rated['price(in Rs.)'].max())
price_range = st.sidebar.slider(
    "Price Range (₹)",
    min_price, max_price,
    (min_price, max_price)
)

# RAM filter
ram_options = ['All'] + sorted(df_rated['ram_gb'].unique().tolist())
selected_ram = st.sidebar.selectbox("RAM (GB)", ram_options)

# Rating filter
min_rating = st.sidebar.slider(
    "Minimum Rating",
    0.0, 5.0, 3.5, 0.1
)

# OS filter
os_options = ['All'] + sorted(df_rated['os'].unique().tolist())
selected_os = st.sidebar.selectbox("Operating System", os_options)

# Apply filters
filtered_df = df_rated.copy()

if selected_brand != 'All':
    filtered_df = filtered_df[filtered_df['brand'] == selected_brand]

filtered_df = filtered_df[
    (filtered_df['price(in Rs.)'] >= price_range[0]) & 
    (filtered_df['price(in Rs.)'] <= price_range[1])
]

if selected_ram != 'All':
    filtered_df = filtered_df[filtered_df['ram_gb'] == selected_ram]

filtered_df = filtered_df[filtered_df['rating'] >= min_rating]

if selected_os != 'All':
    filtered_df = filtered_df[filtered_df['os'] == selected_os]

# Display metrics
st.markdown("## Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Laptops", len(filtered_df))

with col2:
    st.metric("Average Price", f"₹{filtered_df['price(in Rs.)'].mean():,.0f}")

with col3:
    st.metric("Average Rating", f"{filtered_df['rating'].mean():.2f}")

with col4:
    st.metric("Top Brand", filtered_df['brand'].mode()[0] if len(filtered_df) > 0 else "N/A")

st.markdown("---")

# Main dashboard with tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Price Analysis", 
    "Rating Analysis", 
    "Technical Specs",
    "Brand Comparison",
    "Recommendations"
])

# Tab 1: Price Analysis
with tab1:
    
    st.subheader("Price Distribution by Brand")
    fig = px.box(filtered_df, x='brand', y='price(in Rs.)', color='brand',
                     title="Price Distribution by Brand")
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    

    st.subheader("Price vs Rating")
    fig = px.scatter(filtered_df, x='price(in Rs.)', y='rating', 
                        color='brand', size='no_of_ratings',
                        hover_data=['ram_gb', 'storage_gb', 'processor_brand'],
                        title="Price vs Rating Relationship")
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Price Distribution")
    fig = px.histogram(filtered_df, x='price(in Rs.)', nbins=50,
                       title="Price Distribution Histogram",
                       labels={'price(in Rs.)': 'Price (₹)', 'count': 'Number of Laptops'})
    st.plotly_chart(fig, use_container_width=True)

# Tab 2: Rating Analysis
with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Rating by Brand")
        rating_by_brand = filtered_df.groupby('brand')['rating'].mean().sort_values(ascending=False)
        fig = px.bar(x=rating_by_brand.index, y=rating_by_brand.values,
                     title="Average Rating by Brand",
                     labels={'x': 'Brand', 'y': 'Average Rating'})
        fig.add_hline(y=4.5, line_dash="dash", line_color="red", 
                      annotation_text="Premium Threshold (4.5)")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Rating by Processor Brand")
        rating_by_cpu = filtered_df.groupby('processor_brand')['rating'].mean().reset_index()
        fig = px.bar(rating_by_cpu, x='processor_brand', y='rating',
                     title="Average Rating by Processor Brand",
                     color='processor_brand')
        st.plotly_chart(fig, use_container_width=True)


    st.subheader("Rating by RAM")
    rating_by_ram = filtered_df.groupby('ram_gb')['rating'].mean().reset_index()
    fig = px.line(rating_by_ram, x='ram_gb', y='rating',
                      markers=True, title="Rating vs RAM Size")
    st.plotly_chart(fig, use_container_width=True)
        
    st.subheader("Rating Distribution")
    fig = px.histogram(filtered_df, x='rating', nbins=20,
                           title="Rating Distribution",
                           labels={'rating': 'Rating', 'count': 'Number of Laptops'})
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Average Rating by Display Size")
    display_rating = filtered_df.groupby('display_size')['rating'].agg(['mean', 'count']).reset_index()
    display_rating = display_rating.sort_values('display_size')
    fig = px.bar(display_rating, x='display_size', y='mean',
                     text='count',
                     title="Average Rating by Display Size",
                     labels={'display_size': 'Display Size (inches)', 'mean': 'Average Rating'},
                     color='mean',
                     color_continuous_scale='RdYlGn')
    fig.update_traces(textposition='outside')
    fig.add_hline(y=4.5, line_dash="dash", line_color="red")
    st.plotly_chart(fig, use_container_width=True)

# Tab 3: Technical Specs
with tab3:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("RAM Distribution")
        ram_counts = filtered_df['ram_gb'].value_counts().reset_index()
        ram_counts.columns = ['RAM (GB)', 'Count']
        fig = px.pie(ram_counts, values='Count', names='RAM (GB)',
                     title="RAM Distribution")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Storage Type Distribution")
        storage_counts = filtered_df['storage_type'].value_counts().reset_index()
        storage_counts.columns = ['Storage Type', 'Count']
        fig = px.bar(storage_counts, x='Storage Type', y='Count',
                     title="Storage Type Distribution",
                     color='Storage Type')
        st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Processor Brands")
        cpu_counts = filtered_df['processor_brand'].value_counts().reset_index()
        cpu_counts.columns = ['Processor', 'Count']
        fig = px.bar(cpu_counts, x='Processor', y='Count',
                     title="Processor Brand Distribution",
                     color='Processor')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("OS Distribution")
        os_counts = filtered_df['os'].value_counts().reset_index()
        os_counts.columns = ['OS', 'Count']
        fig = px.pie(os_counts, values='Count', names='OS',
                     title="Operating System Distribution")
        st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Processor Series Distribution")
        cpu_series_counts = filtered_df['processor_series'].value_counts().head(10).reset_index()
        cpu_series_counts.columns = ['Processor Series', 'Count']
        fig = px.bar(cpu_series_counts, x='Processor Series', y='Count',
                     title="Top 10 Processor Series")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Distribution of Display Sizes on the Market")
        fig = px.histogram(filtered_df, x='display_size', 
                           nbins=20,
                           title="Display Size Distribution",
                           labels={'display_size': 'Display Size (inches)', 
                                   'count': 'Number of Laptops'},
                           color_discrete_sequence=['skyblue'])
        fig.update_layout(bargap=0.1)
        st.plotly_chart(fig, use_container_width=True)

# Tab 4: Brand Comparison
with tab4:
    # Brand comparison metrics
    brand_metrics = filtered_df.groupby('brand').agg({
        'price(in Rs.)': 'mean',
        'rating': 'mean',
        'ram_gb': 'mean',
        'no_of_ratings': 'sum'
    }).round(2).reset_index()
    
    st.subheader("Brand Performance Comparison")
    
    fig = make_subplots(rows=1, cols=3, 
                        subplot_titles=('Average Price (₹)', 'Average Rating', 'Average RAM (GB)'))
    
    fig.add_trace(go.Bar(x=brand_metrics['brand'], y=brand_metrics['price(in Rs.)'],
                         name='Price', marker_color='lightblue'),
                  row=1, col=1)
    
    fig.add_trace(go.Bar(x=brand_metrics['brand'], y=brand_metrics['rating'],
                         name='Rating', marker_color='lightgreen'),
                  row=1, col=2)
    
    fig.add_trace(go.Bar(x=brand_metrics['brand'], y=brand_metrics['ram_gb'],
                         name='RAM', marker_color='lightcoral'),
                  row=1, col=3)
    
    fig.update_layout(height=500, showlegend=False,
                      title_text="Brand Comparison Dashboard")
    st.plotly_chart(fig, use_container_width=True)
    
    # Correlation heatmap
    st.subheader("Feature Correlation Heatmap")
    numeric_cols = ['price(in Rs.)', 'ram_gb', 'storage_gb', 'display_size', 'rating', 'no_of_ratings']
    available_cols = [c for c in numeric_cols if c in filtered_df.columns]
    if len(available_cols) > 1:
        corr_matrix = filtered_df[available_cols].corr()
        fig = px.imshow(corr_matrix.round(2), text_auto=True, aspect="auto",
                        title="Correlation Matrix of Numerical Features",
                        color_continuous_scale='RdBu_r', zmin=-1, zmax=1)
        st.plotly_chart(fig, use_container_width=True)

# Tab 5: Recommendations
with tab5:
    st.subheader("Smart Recommendations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("###Best Value for Money")
        st.info("""
        **Recommended Configuration:**
        - **RAM:** 16 GB
        - **Storage:** 512 GB SSD
        - **Processor:** Ryzen 5 / Intel i5
        - **OS:** Windows 11
        """)
        
        st.markdown("### Premium Choice")
        st.success("""
        **Top Performers:**
        - **Apple MacBooks** with M-series processors
        - **16-32 GB RAM**
        - **512 GB+ SSD**
        - **macOS**
        """)

# Footer
st.markdown("---")
st.markdown("### Key Insights")
st.info("""
- **SSD storage** has become the market standard for new laptops
- **16 GB RAM** offers the best balance of performance and customer satisfaction
- **AMD processors** demonstrate strong price-to-performance value
- **Premium ultrabooks** (Apple, high-end Dell XPS) consistently receive the highest ratings
- **Storage size** beyond 512 GB provides limited additional value for most users
""")

st.markdown("---")
st.caption("Laptop Market Analysis Dashboard | Data-driven insights for smart purchasing decisions")
