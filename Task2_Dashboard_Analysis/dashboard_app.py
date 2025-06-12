import dash
from dash import dcc, html, Input, Output, State, dash_table, callback, ctx
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import joblib
import numpy as np
from datetime import datetime, timedelta
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeChangerAIO, template_from_url
import warnings
warnings.filterwarnings('ignore')

# Load data & model (with error handling)
try:
    df = pd.read_csv('data/sales_data_sample.csv', encoding='latin1')
    model = joblib.load('model/sales_model.pkl')
    le_product = joblib.load('model/le_product.pkl')
    le_country = joblib.load('model/le_country.pkl')
except:
    # Fallback sample data if files don't exist
    np.random.seed(42)
    dates = pd.date_range('2020-01-01', '2024-12-31', freq='D')
    df = pd.DataFrame({
        'ORDERNUMBER': range(1, 1001),
        'ORDERDATE': np.random.choice(dates, 1000),
        'COUNTRY': np.random.choice(['USA', 'UK', 'France', 'Germany', 'Japan', 'Australia'], 1000),
        'PRODUCTLINE': np.random.choice(['Motorcycles', 'Classic Cars', 'Trucks', 'Vintage Cars', 'Planes', 'Ships'], 1000),
        'QUANTITYORDERED': np.random.randint(10, 100, 1000),
        'PRICEEACH': np.random.uniform(20, 200, 1000),
        'MSRP': np.random.uniform(25, 250, 1000),
        'SALES': np.random.uniform(1000, 50000, 1000)
    })

# Advanced data preprocessing
df['ORDERDATE'] = pd.to_datetime(df['ORDERDATE'])
df['Month'] = df['ORDERDATE'].dt.month
df['Year'] = df['ORDERDATE'].dt.year
df['Month-Year'] = df['ORDERDATE'].dt.strftime('%b-%Y')
df['Quarter'] = df['ORDERDATE'].dt.quarter
df['Quarter-Year'] = 'Q' + df['Quarter'].astype(str) + '-' + df['Year'].astype(str)
df['Week'] = df['ORDERDATE'].dt.isocalendar().week
df['Weekday'] = df['ORDERDATE'].dt.day_name()
df['Month_Name'] = df['ORDERDATE'].dt.strftime('%B')

# Advanced calculated metrics
df['PROFIT'] = (df['PRICEEACH'] - df['MSRP'] * 0.6) * df['QUANTITYORDERED']
df['PROFIT_MARGIN'] = (df['PROFIT'] / df['SALES']) * 100
df['DISCOUNT'] = df['MSRP'] - df['PRICEEACH']
df['DISCOUNT_RATE'] = (df['DISCOUNT'] / df['MSRP']) * 100
df['REVENUE_PER_UNIT'] = df['SALES'] / df['QUANTITYORDERED']
df['CUSTOMER_SEGMENT'] = pd.cut(df['SALES'], bins=[0, 1000, 5000, 20000, float('inf')], 
                               labels=['Low Value', 'Medium Value', 'High Value', 'Premium'])

# Performance metrics
df_current = df[df['ORDERDATE'] >= (df['ORDERDATE'].max() - timedelta(days=30))]
df_previous = df[(df['ORDERDATE'] >= (df['ORDERDATE'].max() - timedelta(days=60))) & 
                 (df['ORDERDATE'] < (df['ORDERDATE'].max() - timedelta(days=30)))]

# Modern color scheme
colors = {
    'primary': '#2E86AB',      # Professional blue
    'secondary': '#A23B72',    # Accent purple
    'success': '#F18F01',      # Warm orange
    'warning': '#C73E1D',      # Alert red
    'background': '#0F1419',   # Dark background
    'surface': '#1A1F26',      # Card background
    'text': '#FFFFFF',         # Primary text
    'text_secondary': '#94A3B8', # Secondary text
    'border': '#334155',       # Border color
    'gradient_start': '#2E86AB',
    'gradient_end': '#A23B72'
}

# Initialize app with custom theme
app = dash.Dash(__name__, 
                external_stylesheets=[
                    dbc.themes.BOOTSTRAP,
                    "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap",
                    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
                ])

app.title = "Enterprise Sales Analytics Suite"

# Custom CSS - Fixed approach
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                font-family: 'Inter', sans-serif;
                background: linear-gradient(135deg, #0F1419 0%, #1A1F26 100%);
                margin: 0;
                padding: 0;
            }

            .main-container {
                background: transparent;
                min-height: 100vh;
            }

            .header-section {
                background: linear-gradient(135deg, #2E86AB 0%, #A23B72 100%);
                border-radius: 12px;
                padding: 24px;
                margin-bottom: 24px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            }

            .kpi-card {
                background: rgba(26, 31, 38, 0.95);
                border: 1px solid #334155;
                border-radius: 12px;
                padding: 20px;
                margin-bottom: 16px;
                transition: all 0.3s ease;
                backdrop-filter: blur(10px);
            }

            .kpi-card:hover {
                transform: translateY(-4px);
                box-shadow: 0 12px 48px rgba(46, 134, 171, 0.15);
                border-color: #2E86AB;
            }

            .chart-container {
                background: rgba(26, 31, 38, 0.95);
                border: 1px solid #334155;
                border-radius: 12px;
                padding: 20px;
                margin-bottom: 20px;
                backdrop-filter: blur(10px);
            }

            .filter-panel {
                background: rgba(26, 31, 38, 0.95);
                border: 1px solid #334155;
                border-radius: 12px;
                padding: 24px;
                backdrop-filter: blur(10px);
                position: sticky;
                top: 20px;
                height: fit-content;
            }

            .metric-icon {
                width: 48px;
                height: 48px;
                border-radius: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 24px;
                margin-bottom: 12px;
            }

            .trend-indicator {
                font-size: 12px;
                font-weight: 600;
                padding: 4px 8px;
                border-radius: 16px;
                margin-top: 8px;
            }

            .trend-up {
                background: rgba(241, 143, 1, 0.1);
                color: #F18F01;
            }

            .trend-down {
                background: rgba(199, 62, 29, 0.1);
                color: #C73E1D;
            }

            .prediction-panel {
                background: linear-gradient(135deg, rgba(46, 134, 171, 0.1) 0%, rgba(162, 59, 114, 0.1) 100%);
                border: 1px solid #2E86AB;
                border-radius: 12px;
                padding: 24px;
            }

            .section-header {
                font-size: 24px;
                font-weight: 700;
                color: #FFFFFF;
                margin-bottom: 16px;
                display: flex;
                align-items: center;
                gap: 12px;
            }

            .section-header::before {
                content: '';
                width: 4px;
                height: 24px;
                background: linear-gradient(135deg, #2E86AB 0%, #A23B72 100%);
                border-radius: 2px;
            }

            .alert-card {
                background: rgba(241, 143, 1, 0.1);
                border-left: 4px solid #F18F01;
                border-radius: 8px;
                padding: 16px;
                margin-bottom: 16px;
            }

            .notification-badge {
                position: absolute;
                top: -8px;
                right: -8px;
                background: #C73E1D;
                color: white;
                border-radius: 50%;
                width: 20px;
                height: 20px;
                font-size: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Advanced KPI card component
def create_advanced_kpi_card(title, value, change, icon, color, prefix="", suffix=""):
    change_color = colors['success'] if change >= 0 else colors['warning']
    change_icon = "fa-arrow-up" if change >= 0 else "fa-arrow-down"
    
    return html.Div([
        html.Div([
            html.Div([
                html.I(className=f"fas {icon}", style={'color': color})
            ], className="metric-icon", style={'background': f'{color}20'}),
            html.Div([
                html.H6(title, style={'color': colors['text_secondary'], 'margin': '0', 'font-size': '14px'}),
                html.H3(f"{prefix}{value:,.0f}{suffix}", 
                        style={'color': colors['text'], 'margin': '8px 0', 'font-weight': '700'}),
                html.Div([
                    html.I(className=f"fas {change_icon}", style={'color': change_color, 'margin-right': '8px'}),
                    html.Span(f"{abs(change):.1f}%", style={'color': change_color, 'font-weight': '600'}),
                    html.Span(" vs last period", style={'color': colors['text_secondary'], 'margin-left': '4px'})
                ], className="trend-indicator")
            ], style={'flex': '1'})
        ], style={'display': 'flex', 'align-items': 'flex-start', 'gap': '16px'})
    ], className="kpi-card")

# Alert system component
def create_alert_system():
    alerts = [
        {"type": "warning", "message": "Sales in Q4 are 15% below target", "icon": "fa-exclamation-triangle"},
        {"type": "success", "message": "Motorcycles segment exceeded expectations", "icon": "fa-check-circle"},
        {"type": "info", "message": "New market opportunity identified in Asia", "icon": "fa-info-circle"}
    ]
    
    return html.Div([
        html.H6("🚨 Business Alerts", style={'color': colors['text'], 'margin-bottom': '16px', 'font-weight': '600'}),
        html.Div([
            html.Div([
                html.I(className=f"fas {alert['icon']}", style={'margin-right': '12px', 'color': colors['warning']}),
                html.Span(alert['message'], style={'color': colors['text_secondary'], 'font-size': '14px'})
            ], className="alert-card", style={'margin-bottom': '8px'}) for alert in alerts
        ])
    ])

# Real-time metrics simulator
def get_real_time_metrics():
    total_sales = df['SALES'].sum()
    total_orders = len(df)
    avg_order_value = total_sales / total_orders
    total_profit = df['PROFIT'].sum()
    
    # Simulate growth rates
    sales_growth = np.random.uniform(5, 25)
    orders_growth = np.random.uniform(-2, 15)
    aov_growth = np.random.uniform(2, 12)
    profit_growth = np.random.uniform(8, 30)
    
    return {
        'total_sales': total_sales,
        'total_orders': total_orders,
        'avg_order_value': avg_order_value,
        'total_profit': total_profit,
        'sales_growth': sales_growth,
        'orders_growth': orders_growth,
        'aov_growth': aov_growth,
        'profit_growth': profit_growth
    }

# Layout with advanced components
app.layout = html.Div([
    # Header Section
    html.Div([
        html.Div([
            html.Div([
                html.I(className="fas fa-chart-line", style={'font-size': '32px', 'margin-right': '16px'}),
                html.Div([
                    html.H1("Enterprise Sales Analytics Suite", 
                           style={'margin': '0', 'font-weight': '700', 'font-size': '28px'}),
                    html.P("Real-time Business Intelligence & Predictive Analytics", 
                           style={'margin': '4px 0 0 0', 'opacity': '0.9', 'font-size': '16px'})
                ])
            ], style={'display': 'flex', 'align-items': 'center'}),
            
            html.Div([
                html.Div([
                    html.I(className="fas fa-bell", style={'font-size': '18px'}),
                    html.Div("3", className="notification-badge")
                ], style={'position': 'relative', 'margin-right': '20px', 'cursor': 'pointer'}),
                html.Div(id="live-time", style={'font-size': '14px', 'opacity': '0.8'})
            ], style={'display': 'flex', 'align-items': 'center'})
        ], style={'display': 'flex', 'justify-content': 'space-between', 'align-items': 'center'})
    ], className="header-section"),
    
    # Main Content
    dbc.Container([
        dbc.Row([
            # Left Sidebar - Filters & Alerts
            dbc.Col([
                html.Div([
                    html.H5("📊 Analytics Controls", style={'color': colors['text'], 'margin-bottom': '20px'}),
                    
                    # Time Period Filter
                    html.Div([
                        html.Label("Time Aggregation", style={'color': colors['text_secondary'], 'font-weight': '500'}),
                        dcc.Dropdown(
                            id='time-filter',
                            options=[
                                {'label': '📅 Daily', 'value': 'daily'},
                                {'label': '📊 Weekly', 'value': 'weekly'},
                                {'label': '📈 Monthly', 'value': 'monthly'},
                                {'label': '📋 Quarterly', 'value': 'quarterly'},
                                {'label': '📰 Yearly', 'value': 'yearly'}
                            ],
                            value='monthly',
                            clearable=False,
                            style={'margin-bottom': '16px'}
                        )
                    ]),
                    
                    # Date Range
                    html.Div([
                        html.Label("Date Range", style={'color': colors['text_secondary'], 'font-weight': '500'}),
                        dcc.DatePickerRange(
                            id='date-range',
                            start_date=df['ORDERDATE'].min(),
                            end_date=df['ORDERDATE'].max(),
                            display_format='YYYY-MM-DD',
                            style={'margin-bottom': '16px', 'width': '100%'}
                        )
                    ]),
                    
                    # Multi-select filters
                    html.Div([
                        html.Label("Product Lines", style={'color': colors['text_secondary'], 'font-weight': '500'}),
                        dcc.Dropdown(
                            id='product-filter',
                            options=[{'label': f"🚗 {pl}", 'value': pl} for pl in sorted(df['PRODUCTLINE'].unique())],
                            value=list(df['PRODUCTLINE'].unique()),
                            multi=True,
                            style={'margin-bottom': '16px'}
                        )
                    ]),
                    
                    html.Div([
                        html.Label("Markets", style={'color': colors['text_secondary'], 'font-weight': '500'}),
                        dcc.Dropdown(
                            id='country-filter',
                            options=[{'label': f"🌍 {c}", 'value': c} for c in sorted(df['COUNTRY'].unique())],
                            value=list(df['COUNTRY'].unique()),
                            multi=True,
                            style={'margin-bottom': '16px'}
                        )
                    ]),
                    
                    html.Div([
                        html.Label("Customer Segment", style={'color': colors['text_secondary'], 'font-weight': '500'}),
                        dcc.Dropdown(
                            id='segment-filter',
                            options=[{'label': seg, 'value': seg} for seg in df['CUSTOMER_SEGMENT'].unique()],
                            value=list(df['CUSTOMER_SEGMENT'].unique()),
                            multi=True,
                            style={'margin-bottom': '20px'}
                        )
                    ]),
                    
                    dbc.Button("🔄 Refresh Analytics", id='apply-filters', color="primary", 
                              className="w-100 mb-4", style={'font-weight': '600'}),
                    
                    html.Hr(style={'border-color': colors['border']}),
                    
                    # Alerts Section
                    create_alert_system()
                    
                ], className="filter-panel")
            ], width=3),
            
            # Main Dashboard
            dbc.Col([
                # KPI Cards Row
                dbc.Row([
                    dbc.Col([
                        html.Div(id='kpi-cards-container')
                    ], width=12)
                ], className="mb-4"),
                
                # Main Charts Row
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.H5("📈 Revenue & Profit Trends", className="section-header"),
                            dcc.Graph(id='main-trend-chart', style={'height': '400px'})
                        ], className="chart-container")
                    ], width=8),
                    
                    dbc.Col([
                        html.Div([
                            html.H5("🎯 Performance Metrics", className="section-header"),
                            dcc.Graph(id='performance-gauge', style={'height': '400px'})
                        ], className="chart-container")
                    ], width=4)
                ], className="mb-4"),
                
                # Secondary Charts Row
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.H5("🏪 Product Performance", className="section-header"),
                            dcc.Graph(id='product-analysis', style={'height': '350px'})
                        ], className="chart-container")
                    ], width=6),
                    
                    dbc.Col([
                        html.Div([
                            html.H5("🌍 Geographic Distribution", className="section-header"),
                            dcc.Graph(id='geographic-chart', style={'height': '350px'})
                        ], className="chart-container")
                    ], width=6)
                ], className="mb-4"),
                
                # Advanced Analytics Row
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.H5("🕒 Temporal Patterns", className="section-header"),
                            dcc.Graph(id='temporal-analysis', style={'height': '300px'})
                        ], className="chart-container")
                    ], width=8),
                    
                    dbc.Col([
                        html.Div([
                            html.H5("🔮 AI Sales Predictor", className="section-header"),
                            html.Div([
                                # Prediction inputs
                                dbc.Row([
                                    dbc.Col([
                                        html.Label("Quantity", style={'color': colors['text_secondary']}),
                                        dbc.Input(id='pred-qty', type='number', value=25, min=1, max=1000)
                                    ], width=6),
                                    dbc.Col([
                                        html.Label("Price", style={'color': colors['text_secondary']}),
                                        dbc.Input(id='pred-price', type='number', value=100, step=0.01)
                                    ], width=6)
                                ], className="mb-3"),
                                
                                dbc.Row([
                                    dbc.Col([
                                        html.Label("MSRP", style={'color': colors['text_secondary']}),
                                        dbc.Input(id='pred-msrp', type='number', value=120, step=0.01)
                                    ], width=12)
                                ], className="mb-3"),
                                
                                dbc.Row([
                                    dbc.Col([
                                        html.Label("Market", style={'color': colors['text_secondary']}),
                                        dcc.Dropdown(
                                            id='pred-country',
                                            options=[{'label': c, 'value': c} for c in sorted(df['COUNTRY'].unique())],
                                            value='USA'
                                        )
                                    ], width=6),
                                    dbc.Col([
                                        html.Label("Product", style={'color': colors['text_secondary']}),
                                        dcc.Dropdown(
                                            id='pred-product',
                                            options=[{'label': p, 'value': p} for p in sorted(df['PRODUCTLINE'].unique())],
                                            value='Motorcycles'
                                        )
                                    ], width=6)
                                ], className="mb-3"),
                                
                                dbc.Button("🚀 Generate Prediction", id='predict-btn', 
                                          color="primary", className="w-100 mb-3"),
                                
                                html.Div(id='prediction-output', style={'text-align': 'center'})
                            ])
                        ], className="prediction-panel")
                    ], width=4)
                ])
            ], width=9)
        ]),
        
        # Data Table Section
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H5("📋 Detailed Transaction Records", className="section-header"),
                    dash_table.DataTable(
                        id='data-table',
                        columns=[
                            {"name": "Order #", "id": "ORDERNUMBER", "type": "numeric"},
                            {"name": "Date", "id": "ORDERDATE", "type": "datetime"},
                            {"name": "Country", "id": "COUNTRY", "type": "text"},
                            {"name": "Product Line", "id": "PRODUCTLINE", "type": "text"},
                            {"name": "Quantity", "id": "QUANTITYORDERED", "type": "numeric"},
                            {"name": "Sales", "id": "SALES", "type": "numeric", "format": {"specifier": "$,.0f"}},
                            {"name": "Profit", "id": "PROFIT", "type": "numeric", "format": {"specifier": "$,.0f"}},
                            {"name": "Margin %", "id": "PROFIT_MARGIN", "type": "numeric", "format": {"specifier": ".1f"}}
                        ],
                        data=[],
                        page_size=15,
                        sort_action="native",
                        filter_action="native",
                        style_table={'overflowX': 'auto'},
                        style_cell={
                            'textAlign': 'left',
                            'padding': '12px',
                            'backgroundColor': colors['surface'],
                            'color': colors['text'],
                            'border': f'1px solid {colors["border"]}',
                            'font-family': 'Inter, sans-serif'
                        },
                        style_header={
                            'backgroundColor': colors['primary'],
                            'color': 'white',
                            'fontWeight': '600',
                            'textAlign': 'center'
                        },
                        style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': f'{colors["primary"]}10'
                            },
                            {
                                'if': {'filter_query': '{PROFIT_MARGIN} > 20'},
                                'backgroundColor': f'{colors["success"]}20',
                                'color': colors['success']
                            }
                        ]
                    )
                ], className="chart-container")
            ], width=12)
        ], className="mt-4")
    ], fluid=True, className="main-container"),
    
    # Interval component for real-time updates
    dcc.Interval(id='interval-component', interval=30*1000, n_intervals=0),
    
    # Store components for data
    dcc.Store(id='filtered-data-store'),
    html.Div(id='dummy-trigger', style={'display': 'none'})
], style={'background': colors['background'], 'min-height': '100vh', 'padding': '20px'})

# Enhanced callback for KPI cards with real-time data
@app.callback(
    Output('kpi-cards-container', 'children'),
    Output('live-time', 'children'),
    [Input('interval-component', 'n_intervals'),
     Input('apply-filters', 'n_clicks')],
    [State('date-range', 'start_date'),
     State('date-range', 'end_date'),
     State('product-filter', 'value'),
     State('country-filter', 'value'),
     State('segment-filter', 'value')]
)
def update_kpi_cards(n_intervals, n_clicks, start_date, end_date, products, countries, segments):
    # Update live time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Filter data based on current selections
    filtered_df = df.copy()
    if start_date and end_date:
        filtered_df = filtered_df[
            (filtered_df['ORDERDATE'] >= pd.to_datetime(start_date)) &
            (filtered_df['ORDERDATE'] <= pd.to_datetime(end_date))
        ]
    if products:
        filtered_df = filtered_df[filtered_df['PRODUCTLINE'].isin(products)]
    if countries:
        filtered_df = filtered_df[filtered_df['COUNTRY'].isin(countries)]
    if segments:
        filtered_df = filtered_df[filtered_df['CUSTOMER_SEGMENT'].isin(segments)]
    
    # Calculate metrics
    total_sales = filtered_df['SALES'].sum()
    total_orders = len(filtered_df)
    avg_order_value = total_sales / total_orders if total_orders > 0 else 0
    total_profit = filtered_df['PROFIT'].sum()
    
    # Simulate growth rates with some randomness for demo
    base_growth = [12.5, 8.2, 4.3, 15.7]
    growth_rates = [base + np.random.uniform(-2, 2) for base in base_growth]
    
    kpi_cards = dbc.Row([
        dbc.Col([
            create_advanced_kpi_card(
                "Total Revenue", total_sales, growth_rates[0], 
                "fa-dollar-sign", colors['primary'], "$"
            )
        ], width=3),
        dbc.Col([
            create_advanced_kpi_card(
                "Total Orders", total_orders, growth_rates[1], 
                "fa-shopping-cart", colors['secondary']
            )
        ], width=3),
        dbc.Col([
            create_advanced_kpi_card(
                "Avg Order Value", avg_order_value, growth_rates[2], 
                "fa-chart-bar", colors['success'], "$"
            )
        ], width=3),
        dbc.Col([
            create_advanced_kpi_card(
                "Total Profit", total_profit, growth_rates[3], 
                "fa-coins", colors['warning'], "$"
            )
        ], width=3)
    ])
    
    return kpi_cards, f"🕒 Last updated: {current_time}"

# Main analytics callback
@app.callback(
    [Output('main-trend-chart', 'figure'),
     Output('performance-gauge', 'figure'),
     Output('product-analysis', 'figure'),
     Output('geographic-chart', 'figure'),
     Output('temporal-analysis', 'figure'),
     Output('data-table', 'data'),
     Output('filtered-data-store', 'data')],
    [Input('apply-filters', 'n_clicks'),
     Input('dummy-trigger', 'children')],
    [State('time-filter', 'value'),
     State('date-range', 'start_date'),
     State('date-range', 'end_date'),
     State('product-filter', 'value'),
     State('country-filter', 'value'),
     State('segment-filter', 'value')]
)
def update_all_charts(n_clicks, dummy, time_period, start_date, end_date, products, countries, segments):
    # Filter data
    filtered_df = df.copy()
    
    if start_date and end_date:
        filtered_df = filtered_df[
            (filtered_df['ORDERDATE'] >= pd.to_datetime(start_date)) &
            (filtered_df['ORDERDATE'] <= pd.to_datetime(end_date))
        ]
    
    if products:
        filtered_df = filtered_df[filtered_df['PRODUCTLINE'].isin(products)]
    if countries:
        filtered_df = filtered_df[filtered_df['COUNTRY'].isin(countries)]
    if segments:
        filtered_df = filtered_df[filtered_df['CUSTOMER_SEGMENT'].isin(segments)]
    
    # Main trend chart - Advanced multi-metric visualization
    time_mapping = {
        'daily': 'ORDERDATE',
        'weekly': 'Week',
        'monthly': 'Month-Year',
        'quarterly': 'Quarter-Year',
        'yearly': 'Year'
    }
    
    time_col = time_mapping.get(time_period, 'Month-Year')
    
    if time_period == 'daily':
        trend_data = filtered_df.groupby(filtered_df['ORDERDATE'].dt.date).agg({
            'SALES': 'sum',
            'PROFIT': 'sum',
            'QUANTITYORDERED': 'sum'
        }).reset_index()
        trend_data.columns = ['Date', 'SALES', 'PROFIT', 'QUANTITY']
        x_col = 'Date'
    else:
        trend_data = filtered_df.groupby(time_col).agg({
            'SALES': 'sum',
            'PROFIT': 'sum',
            'QUANTITYORDERED': 'sum'
        }).reset_index()
        trend_data.columns = [time_col, 'SALES', 'PROFIT', 'QUANTITY']
        x_col = time_col
    
    # Create main trend chart with subplots
    main_fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        subplot_titles=('Revenue & Profit Trends', 'Volume Analysis'),
        vertical_spacing=0.12,
        specs=[[{"secondary_y": True}], [{"secondary_y": False}]]
    )
    
    # Revenue line
    main_fig.add_trace(
        go.Scatter(
            x=trend_data[x_col],
            y=trend_data['SALES'],
            name='Revenue',
            line=dict(color=colors['primary'], width=3),
            mode='lines+markers',
            marker=dict(size=8),
            hovertemplate='<b>Revenue</b><br>%{y:$,.0f}<extra></extra>'
        ),
        row=1, col=1
    )
    
    # Profit bars
    main_fig.add_trace(
        go.Bar(
            x=trend_data[x_col],
            y=trend_data['PROFIT'],
            name='Profit',
            marker_color=colors['success'],
            opacity=0.7,
            hovertemplate='<b>Profit</b><br>%{y:$,.0f}<extra></extra>'
        ),
        row=1, col=1
    )
    
    # Volume bars
    main_fig.add_trace(
        go.Bar(
            x=trend_data[x_col],
            y=trend_data['QUANTITY'],
            name='Units Sold',
            marker_color=colors['secondary'],
            opacity=0.8,
            hovertemplate='<b>Units</b><br>%{y:,.0f}<extra></extra>'
        ),
        row=2, col=1
    )
    
    main_fig.update_layout(
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=colors['text'], family='Inter'),
        hovermode='x unified',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        ),
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    main_fig.update_xaxes(
        gridcolor='rgba(255,255,255,0.1)',
        showgrid=True,
        zeroline=False
    )
    main_fig.update_yaxes(
        gridcolor='rgba(255,255,255,0.1)',
        showgrid=True,
        zeroline=False
    )
    
    # Performance gauge chart
    total_sales = filtered_df['SALES'].sum()
    total_profit = filtered_df['PROFIT'].sum()
    profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
    
    gauge_fig = go.Figure()
    
    # Profit margin gauge
    gauge_fig.add_trace(go.Indicator(
        mode="gauge+number+delta",
        value=profit_margin,
        domain={'x': [0, 1], 'y': [0.5, 1]},
        title={'text': "Profit Margin %", 'font': {'color': colors['text']}},
        delta={'reference': 20, 'suffix': '%'},
        gauge={
            'axis': {'range': [None, 50], 'tickcolor': colors['text']},
            'bar': {'color': colors['primary']},
            'steps': [
                {'range': [0, 15], 'color': colors['warning']},
                {'range': [15, 25], 'color': colors['success']},
                {'range': [25, 50], 'color': colors['primary']}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 30
            }
        }
    ))
    
    # Order fulfillment rate (simulated metric)
    fulfillment_rate = np.random.uniform(85, 98)
    gauge_fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=fulfillment_rate,
        domain={'x': [0, 1], 'y': [0, 0.4]},
        title={'text': "Order Fulfillment %", 'font': {'color': colors['text']}},
        gauge={
            'axis': {'range': [None, 100], 'tickcolor': colors['text']},
            'bar': {'color': colors['secondary']},
            'steps': [
                {'range': [0, 70], 'color': colors['warning']},
                {'range': [70, 90], 'color': colors['success']},
                {'range': [90, 100], 'color': colors['primary']}
            ]
        }
    ))
    
    gauge_fig.update_layout(
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=colors['text'], family='Inter'),
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    # Product analysis - Enhanced treemap
    product_data = filtered_df.groupby('PRODUCTLINE').agg({
        'SALES': 'sum',
        'PROFIT': 'sum',
        'QUANTITYORDERED': 'sum'
    }).reset_index()
    product_data['PROFIT_MARGIN'] = (product_data['PROFIT'] / product_data['SALES'] * 100)
    
    product_fig = go.Figure(go.Treemap(
        labels=product_data['PRODUCTLINE'],
        values=product_data['SALES'],
        parents=[""] * len(product_data),
        textinfo="label+value+percent parent",
        texttemplate="<b>%{label}</b><br>$%{value:,.0f}<br>%{percentParent}",
        hovertemplate='<b>%{label}</b><br>Sales: $%{value:,.0f}<br>Share: %{percentParent}<extra></extra>',
        maxdepth=2,
        marker=dict(
            colorscale='Viridis',
            colorbar=dict(
                title=dict(
                    text="Sales Volume",
                    font=dict(color=colors['text'])  # Correct way to set title font
                )
            ),
            line=dict(width=2, color='white')
        )
    ))

    product_fig.update_layout(
        height=350,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=colors['text'], family='Inter'),
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    # Geographic distribution - Enhanced map
    geo_data = filtered_df.groupby('COUNTRY').agg({
        'SALES': 'sum',
        'PROFIT': 'sum',
        'QUANTITYORDERED': 'sum'
    }).reset_index()
    
    geo_fig = go.Figure(go.Choropleth(
    locations=geo_data['COUNTRY'],
    z=geo_data['SALES'],
    locationmode='country names',
    colorscale='Plasma',
    colorbar=dict(
        title=dict(
            text="Sales Volume",
            font=dict(color=colors['text'])  # Correct way to set title font
        ),
        tickfont=dict(color=colors['text'])
    ),
    hovertemplate='<b>%{locations}</b><br>Sales: $%{z:,.0f}<extra></extra>'
))

    geo_fig.update_layout(
        height=350,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=colors['text'], family='Inter'),
        geo=dict(
            bgcolor='rgba(0,0,0,0)',
            showframe=False,
            showcoastlines=True,
            coastlinecolor=colors['border'],
            projection_type='equirectangular'
        ),
        margin=dict(l=20, r=20, t=20, b=20)
    )
    # Temporal analysis - Heatmap by weekday and month
    temporal_data = filtered_df.copy()
    temporal_data['Weekday_Num'] = temporal_data['ORDERDATE'].dt.dayofweek
    temporal_data['Month_Num'] = temporal_data['ORDERDATE'].dt.month
    
    heatmap_data = temporal_data.groupby(['Weekday', 'Month_Name'])['SALES'].sum().unstack(fill_value=0)
    
    temporal_fig = go.Figure(go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale='Viridis',
        hovertemplate='<b>%{y}, %{x}</b><br>Sales: $%{z:,.0f}<extra></extra>',
        colorbar=dict(
            title=dict(
                text="Sales Volume",
                font=dict(color=colors['text'])
            ),
            tickfont=dict(color=colors['text'])
        )
    ))

    temporal_fig.update_layout(
        height=300,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=colors['text'], family='Inter'),
        xaxis=dict(
            title=dict(
                text='Month',
                font=dict(color=colors['text'])  # Correct way for axis title
            )
        ),
        yaxis=dict(
            title=dict(
                text='Day of Week',
                font=dict(color=colors['text'])  # Correct way for axis title
            )
        ),
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    # Prepare table data
    table_data = filtered_df.sort_values('ORDERDATE', ascending=False).head(50)
    table_data_formatted = table_data[[
        'ORDERNUMBER', 'ORDERDATE', 'COUNTRY', 'PRODUCTLINE', 
        'QUANTITYORDERED', 'SALES', 'PROFIT', 'PROFIT_MARGIN'
    ]].copy()
    table_data_formatted['ORDERDATE'] = table_data_formatted['ORDERDATE'].dt.strftime('%Y-%m-%d')
    
    return (main_fig, gauge_fig, product_fig, geo_fig, temporal_fig, 
            table_data_formatted.to_dict('records'), filtered_df.to_dict('records'))

# AI Prediction callback
@app.callback(
    Output('prediction-output', 'children'),
    [Input('predict-btn', 'n_clicks')],
    [State('pred-qty', 'value'),
     State('pred-price', 'value'),
     State('pred-msrp', 'value'),
     State('pred-country', 'value'),
     State('pred-product', 'value')]
)
def make_prediction(n_clicks, qty, price, msrp, country, product):
    if not n_clicks:
        return html.Div([
            html.I(className="fas fa-robot", style={'font-size': '48px', 'color': colors['primary'], 'margin-bottom': '16px'}),
            html.P("Configure parameters and click predict to see AI-powered sales forecasting", 
                   style={'color': colors['text_secondary'], 'text-align': 'center'})
        ])
    
    # Simple prediction calculation (replace with actual model)
    base_prediction = qty * price
    
    # Apply country multiplier
    country_multipliers = {
        'USA': 1.2, 'UK': 1.1, 'France': 1.0, 'Germany': 1.15,
        'Japan': 1.3, 'Australia': 0.9
    }
    country_mult = country_multipliers.get(country, 1.0)
    
    # Apply product multiplier
    product_multipliers = {
        'Motorcycles': 1.3, 'Classic Cars': 1.5, 'Trucks': 1.1,
        'Vintage Cars': 1.8, 'Planes': 2.0, 'Ships': 1.4
    }
    product_mult = product_multipliers.get(product, 1.0)
    
    # Calculate final prediction
    prediction = base_prediction * country_mult * product_mult
    
    # Calculate confidence interval
    confidence_lower = prediction * 0.85
    confidence_upper = prediction * 1.15
    
    # Determine prediction quality
    margin = (price - msrp * 0.6) / price * 100 if price > 0 else 0
    if margin > 30:
        quality = "🟢 Excellent"
        quality_color = colors['success']
    elif margin > 15:
        quality = "🟡 Good"
        quality_color = colors['warning']
    else:
        quality = "🔴 Review"
        quality_color = colors['warning']
    
    return html.Div([
        html.Div([
            html.I(className="fas fa-chart-line", style={'font-size': '24px', 'margin-right': '12px'}),
            html.Span("AI Prediction Result", style={'font-size': '18px', 'font-weight': '600'})
        ], style={'display': 'flex', 'align-items': 'center', 'margin-bottom': '20px', 'color': colors['text']}),
        
        html.Div([
            html.H2(f"${prediction:,.0f}", style={
                'color': colors['primary'], 
                'font-weight': '700', 
                'margin': '0',
                'font-size': '32px'
            }),
            html.P("Predicted Sales Value", style={
                'color': colors['text_secondary'], 
                'margin': '4px 0 16px 0'
            })
        ], style={'text-align': 'center', 'margin-bottom': '20px'}),
        
        html.Div([
            html.Div([
                html.Span("Confidence Range", style={'color': colors['text_secondary'], 'font-size': '14px'}),
                html.Br(),
                html.Span(f"${confidence_lower:,.0f} - ${confidence_upper:,.0f}", 
                         style={'color': colors['text'], 'font-weight': '600'})
            ], style={'margin-bottom': '12px'}),
            
            html.Div([
                html.Span("Deal Quality", style={'color': colors['text_secondary'], 'font-size': '14px'}),
                html.Br(),
                html.Span(quality, style={'color': quality_color, 'font-weight': '600'})
            ], style={'margin-bottom': '12px'}),
            
            html.Div([
                html.Span("Profit Margin", style={'color': colors['text_secondary'], 'font-size': '14px'}),
                html.Br(),
                html.Span(f"{margin:.1f}%", style={'color': colors['text'], 'font-weight': '600'})
            ])
        ], style={
            'background': f'{colors["primary"]}10',
            'padding': '16px',
            'border-radius': '8px',
            'border-left': f'4px solid {colors["primary"]}'
        })
    ])

# Initialize dashboard on page load
@app.callback(
    Output('dummy-trigger', 'children'),
    Input('dummy-trigger', 'id')
)
def trigger_initial_load(_):
    return 'loaded'

if __name__ == '__main__':
    app.run(debug=True)