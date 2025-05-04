import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os

# Load data
df = pd.read_csv('data_employee.csv')

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=['https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap'])
server = app.server  # Expose Flask server for Gunicorn

# Layout
app.layout = html.Div([
    html.H1("Company XYZ Benefits Optimization Dashboard", style={'textAlign': 'center', 'fontFamily': 'Roboto', 'color': '#2c3e50'}),
    
    # Cards and Filters
    html.Div([
        # Cards for key metrics
        html.Div([
            html.Div([
                html.H3("Total Premium Cost", style={'fontFamily': 'Roboto'}),
                html.H4(id='total-premium-cost', style={'color': '#ffffff', 'fontFamily': 'Roboto'})
            ], style={'width': '22%', 'backgroundColor': '#008080', 'padding': '20px', 'margin': '1%', 'borderRadius': '10px', 'textAlign': 'center', 'boxShadow': '2px 2px 5px rgba(0,0,0,0.1)', 'color': '#ffffff'}),
            html.Div([
                html.H3("Total Employee Cost", style={'fontFamily': 'Roboto'}),
                html.H4(id='total-employee-cost', style={'color': '#ffffff', 'fontFamily': 'Roboto'})
            ], style={'width': '22%', 'backgroundColor': '#ff6f61', 'padding': '20px', 'margin': '1%', 'borderRadius': '10px', 'textAlign': 'center', 'boxShadow': '2px 2px 5px rgba(0,0,0,0.1)', 'color': '#ffffff'}),
            html.Div([
                html.H3("Total Employer Cost", style={'fontFamily': 'Roboto'}),
                html.H4(id='total-employer-cost', style={'color': '#ffffff', 'fontFamily': 'Roboto'})
            ], style={'width': '22%', 'backgroundColor': '#4b0082', 'padding': '20px', 'margin': '1%', 'borderRadius': '10px', 'textAlign': 'center', 'boxShadow': '2px 2px 5px rgba(0,0,0,0.1)', 'color': '#ffffff'}),
            html.Div([
                html.H3("Total Potential Savings", style={'fontFamily': 'Roboto'}),
                html.H4(id='total-potential-savings', style={'color': '#ffffff', 'fontFamily': 'Roboto'})
            ], style={'width': '22%', 'backgroundColor': '#228b22', 'padding': '20px', 'margin': '1%', 'borderRadius': '10px', 'textAlign': 'center', 'boxShadow': '2px 2px 5px rgba(0,0,0,0.1)', 'color': '#ffffff'})
        ], style={'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '20px'}),
        
        # Filters
        html.Div([
            html.Label("Select State:", style={'fontFamily': 'Roboto', 'marginBottom': '5px'}),
            dcc.Dropdown(
                id='state-filter',
                options=[{'label': 'All', 'value': 'All'}] + [{'label': state, 'value': state} for state in df['State'].unique()],
                value='All',
                style={'width': '100%', 'fontFamily': 'Roboto'}
            ),
            html.Label("Select Department:", style={'fontFamily': 'Roboto', 'marginBottom': '5px', 'marginTop': '10px'}),
            dcc.Dropdown(
                id='department-filter',
                options=[{'label': 'All', 'value': 'All'}] + [{'label': dept, 'value': dept} for dept in df['Department'].unique()],
                value='All',
                style={'width': '100%', 'fontFamily': 'Roboto'}
            )
        ], style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'space-between', 'marginBottom': '20px', 'gap': '20px'}),
        
        # Savings Calculator
        html.Div([
            html.Label("Enter Number of PPO Employees to Switch to HSA:", style={'fontFamily': 'Roboto'}),
            dcc.Input(id='ppo-switch-input', type='number', value=0, min=0, style={'width': '20%', 'fontFamily': 'Roboto'}),
            html.Div(id='savings-output', style={'marginTop': '10px', 'fontFamily': 'Roboto', 'color': '#2c3e50'})
        ], style={'marginBottom': '20px', 'backgroundColor': '#f8f9fa', 'padding': '15px', 'borderRadius': '5px'})
    ], style={'backgroundColor': '#f8f9fa', 'padding': '20px', 'borderRadius': '5px'}),
    
    # Cost Overview Section
    html.Div([
        html.H2("Cost Overview", style={'fontFamily': 'Roboto', 'color': '#2c3e50'}),
        dcc.Graph(id='cost-by-state-plan'),
        dcc.Graph(id='plan-by-state'),
        dcc.Graph(id='employer-employee-cost'),
        dcc.Graph(id='cost-breakdown-plan-state')
    ], style={'marginTop': '20px'}),
    
    # Savings Opportunities Section
    html.Div([
        html.H2("Savings Opportunities", style={'fontFamily': 'Roboto', 'color': '#2c3e50'}),
        dcc.Graph(id='savings-by-state'),
        dcc.Graph(id='savings-by-department'),
        dcc.Graph(id='cumulative-savings')
    ], style={'marginTop': '20px'}),
    
    # Detailed Analysis Section
    html.Div([
        html.H2("Detailed Analysis", style={'fontFamily': 'Roboto', 'color': '#2c3e50'}),
        dcc.Graph(id='cost-per-employee-heatmap'),
        dcc.Graph(id='cost-summary-table')
    ], style={'marginTop': '20px'})
], style={'backgroundColor': '#f1f3f5', 'padding': '20px', 'fontFamily': 'Roboto'})

# Callback for updating charts, cards, and savings calculator
@app.callback(
    [Output('cost-by-state-plan', 'figure'),
     Output('plan-by-state', 'figure'),
     Output('employer-employee-cost', 'figure'),
     Output('savings-by-state', 'figure'),
     Output('savings-by-department', 'figure'),
     Output('cost-breakdown-plan-state', 'figure'),
     Output('cumulative-savings', 'figure'),
     Output('cost-per-employee-heatmap', 'figure'),
     Output('cost-summary-table', 'figure'),
     Output('total-premium-cost', 'children'),
     Output('total-employee-cost', 'children'),
     Output('total-employer-cost', 'children'),
     Output('total-potential-savings', 'children'),
     Output('savings-output', 'children')],
    [Input('state-filter', 'value'),
     Input('department-filter', 'value'),
     Input('ppo-switch-input', 'value')]
)
def update_dashboard(selected_state, selected_department, ppo_switch):
    # Filter data based on state and department
    filtered_df = df
    if selected_state != 'All':
        filtered_df = filtered_df[filtered_df['State'] == selected_state]
    if selected_department != 'All':
        filtered_df = filtered_df[filtered_df['Department'] == selected_department]
    
    # Card calculations
    total_premium_cost = filtered_df['Premium Cost'].sum()
    total_employee_cost = filtered_df['Employee Cost'].sum()
    total_employer_cost = filtered_df['Employer Cost'].sum()
    
    # Calculate total potential savings (PPO to HSA)
    ppo_df = filtered_df[filtered_df['Medical Plan'] == 'PPO']
    hsa_df = filtered_df[filtered_df['Medical Plan'] == 'HSA']
    savings_by_state = ppo_df.groupby('State')[['Employer Cost', 'Employee Cost']].sum().reset_index()
    hsa_costs = hsa_df.groupby('State')[['Employer Cost', 'Employee Cost']].mean().reset_index()
    savings_by_state = savings_by_state.merge(hsa_costs, on='State', suffixes=('_PPO', '_HSA'), how='left')
    savings_by_state['Employer Savings'] = savings_by_state['Employer Cost_PPO'] - (savings_by_state['Employer Cost_HSA'] * ppo_df.groupby('State').size().reset_index(name='Count')['Count'])
    savings_by_state['Employee Savings'] = savings_by_state['Employee Cost_PPO'] - (savings_by_state['Employee Cost_HSA'] * ppo_df.groupby('State').size().reset_index(name='Count')['Count'])
    total_potential_savings = (savings_by_state['Employer Savings'].sum() + savings_by_state['Employee Savings'].sum()) if not savings_by_state.empty else 0
    
    # Savings Calculator
    avg_savings_per_employee = (total_potential_savings / len(ppo_df)) if len(ppo_df) > 0 else 0
    calculated_savings = ppo_switch * avg_savings_per_employee if ppo_switch is not None else 0
    
    # Bar Chart: Average Premium Cost by State and Plan
    cost_by_state_plan = filtered_df.groupby(['State', 'Medical Plan'])['Premium Cost'].mean().reset_index()
    fig1 = px.bar(
        cost_by_state_plan,
        x='State',
        y='Premium Cost',
        color='Medical Plan',
        barmode='group',
        title='Average Premium Cost by State and Plan Type',
        labels={'Premium Cost': 'Average Premium Cost ($)'},
        color_discrete_map={'PPO': '#ff6f61', 'HMO': '#008080', 'HSA': '#228b22'},
        hover_data={'Premium Cost': ':.2f'}
    )
    fig1.update_layout(font_family='Roboto', showlegend=True, plot_bgcolor='#ffffff', paper_bgcolor='#ffffff', yaxis_gridcolor='#e0e0e0')
    
    # Pie Chart: Plan Distribution for Selected State
    plan_by_state = filtered_df.groupby('Medical Plan').size().reset_index(name='Count')
    fig2 = px.pie(
        plan_by_state,
        names='Medical Plan',
        values='Count',
        title=f"Plan Distribution ({'All States' if selected_state == 'All' else selected_state}, {'All Departments' if selected_department == 'All' else selected_department})",
        color='Medical Plan',
        category_orders={'Medical Plan': ['PPO', 'HMO', 'HSA']},
        color_discrete_map={'PPO': '#ff6f61', 'HMO': '#008080', 'HSA': '#228b22'},
        hover_data=['Count']
    )
    fig2.update_layout(font_family='Roboto', showlegend=True, plot_bgcolor='#ffffff', paper_bgcolor='#ffffff')
    
    # Bar Chart: Employer vs Employee Cost by Plan
    cost_by_plan = filtered_df.groupby('Medical Plan')[['Employer Cost', 'Employee Cost']].mean().reset_index()
    fig3 = go.Figure(data=[
        go.Bar(name='Employer Cost', x=cost_by_plan['Medical Plan'], y=cost_by_plan['Employer Cost'], marker_color='#4b0082'),
        go.Bar(name='Employee Cost', x=cost_by_plan['Medical Plan'], y=cost_by_plan['Employee Cost'], marker_color='#ff6f61')
    ])
    fig3.update_layout(
        barmode='stack',
        title='Employer vs Employee Cost by Plan Type',
        xaxis_title='Medical Plan',
        yaxis_title='Average Cost ($)',
        legend=dict(x=0.8, y=1.1, orientation='h'),
        font_family='Roboto',
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        yaxis_gridcolor='#e0e0e0',
        hovermode='x unified'
    )
    
    # Bar Chart: Potential Savings by State (PPO to HSA)
    fig4 = go.Figure(data=[
        go.Bar(name='Employer Savings', x=savings_by_state['State'], y=savings_by_state['Employer Savings'], marker_color='#4b0082'),
        go.Bar(name='Employee Savings', x=savings_by_state['State'], y=savings_by_state['Employee Savings'], marker_color='#ff6f61')
    ])
    fig4.update_layout(
        barmode='group',
        title='Potential Savings by State (Switching PPO to HSA)',
        xaxis_title='State',
        yaxis_title='Total Savings ($)',
        legend=dict(x=0.8, y=1.1, orientation='h'),
        font_family='Roboto',
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        yaxis_gridcolor='#e0e0e0',
        hovermode='x unified'
    )
    
    # Bar Chart: Potential Savings by Department (PPO to HSA)
    savings_by_dept = ppo_df.groupby('Department')[['Employer Cost', 'Employee Cost']].sum().reset_index()
    hsa_costs_dept = hsa_df.groupby('Department')[['Employer Cost', 'Employee Cost']].mean().reset_index()
    savings_by_dept = savings_by_dept.merge(hsa_costs_dept, on='Department', suffixes=('_PPO', '_HSA'), how='left')
    savings_by_dept['Employer Savings'] = savings_by_dept['Employer Cost_PPO'] - (savings_by_dept['Employer Cost_HSA'] * ppo_df.groupby('Department').size().reset_index(name='Count')['Count'])
    savings_by_dept['Employee Savings'] = savings_by_dept['Employee Cost_PPO'] - (savings_by_dept['Employee Cost_HSA'] * ppo_df.groupby('Department').size().reset_index(name='Count')['Count'])
    fig5 = go.Figure(data=[
        go.Bar(name='Employer Savings', x=savings_by_dept['Department'], y=savings_by_dept['Employer Savings'], marker_color='#4b0082'),
        go.Bar(name='Employee Savings', x=savings_by_dept['Department'], y=savings_by_dept['Employee Savings'], marker_color='#ff6f61')
    ])
    fig5.update_layout(
        barmode='group',
        title='Potential Savings by Department (Switching PPO to HSA)',
        xaxis_title='Department',
        yaxis_title='Total Savings ($)',
        legend=dict(x=0.8, y=1.1, orientation='h'),
        font_family='Roboto',
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        yaxis_gridcolor='#e0e0e0',
        hovermode='x unified'
    )
    
    # Stacked Bar Chart: Cost Breakdown by Plan and State
    cost_breakdown = filtered_df.groupby(['State', 'Medical Plan'])[['Employer Cost', 'Employee Cost']].sum().reset_index()
    cost_breakdown_melted = cost_breakdown.melt(id_vars=['State', 'Medical Plan'], value_vars=['Employer Cost', 'Employee Cost'], var_name='Cost Type', value_name='Cost')
    fig6 = px.bar(
        cost_breakdown_melted,
        x='State',
        y='Cost',
        color='Cost Type',
        barmode='stack',
        facet_col='Medical Plan',
        title='Cost Breakdown by Plan and State',
        labels={'Cost': 'Total Cost ($)', 'Cost Type': 'Cost Type'},
        color_discrete_map={'Employer Cost': '#4b0082', 'Employee Cost': '#ff6f61'},
        hover_data={'Cost': ':.2f', 'State': True, 'Medical Plan': True}
    )
    fig6.update_layout(
        legend=dict(x=0.8, y=1.1, orientation='h'),
        facet_col_spacing=0.05,
        font_family='Roboto',
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        yaxis_gridcolor='#e0e0e0'
    )
    
    # Line Chart: Cumulative Savings Over Employees (PPO to HSA)
    if not ppo_df.empty and not hsa_df.empty:
        ppo_count = ppo_df.groupby('State').size().reset_index(name='PPO_Count')
        savings_per_employee = savings_by_state[['State', 'Employer Savings', 'Employee Savings']].copy()
        savings_per_employee['Total Savings Per Employee'] = (savings_per_employee['Employer Savings'] + savings_per_employee['Employee Savings']) / ppo_count['PPO_Count']
        savings_per_employee = savings_per_employee.merge(ppo_count, on='State')
        savings_per_employee['Cumulative Employees'] = savings_per_employee['PPO_Count'].cumsum()
        savings_per_employee['Cumulative Savings'] = (savings_per_employee['Total Savings Per Employee'] * savings_per_employee['PPO_Count']).cumsum()
        fig7 = px.line(
            savings_per_employee,
            x='Cumulative Employees',
            y='Cumulative Savings',
            title='Cumulative Savings by Number of Employees Switching to HSA',
            labels={'Cumulative Employees': 'Number of Employees Switching', 'Cumulative Savings': 'Total Savings ($)'},
            markers=True,
            hover_data={'Cumulative Employees': True, 'Cumulative Savings': ':.2f'}
        )
        fig7.update_layout(font_family='Roboto', plot_bgcolor='#ffffff', paper_bgcolor='#ffffff', yaxis_gridcolor='#e0e0e0')
    else:
        fig7 = go.Figure()
        fig7.update_layout(
            title='Cumulative Savings by Number of Employees Switching to HSA',
            xaxis_title='Number of Employees Switching',
            yaxis_title='Total Savings ($)',
            annotations=[dict(text="No PPO or HSA data available", x=0.5, y=0.5, showarrow=False)],
            font_family='Roboto',
            plot_bgcolor='#ffffff',
            paper_bgcolor='#ffffff'
        )
    
    # Heatmap: Cost per Employee by Department and Plan
    cost_per_employee = filtered_df.groupby(['Department', 'Medical Plan'])['Premium Cost'].mean().reset_index()
    cost_pivot = cost_per_employee.pivot(index='Department', columns='Medical Plan', values='Premium Cost').fillna(0)
    fig8 = go.Figure(data=go.Heatmap(
        z=cost_pivot.values,
        x=cost_pivot.columns,
        y=cost_pivot.index,
        colorscale='Viridis',
        text=cost_pivot.values.round(2),
        texttemplate='%{text}',
        textfont={'size': 12},
        hovertemplate='Department: %{y}<br>Plan: %{x}<br>Cost: $%{z:.2f}<extra></extra>'
    ))
    fig8.update_layout(
        title='Average Cost per Employee by Department and Plan',
        xaxis_title='Medical Plan',
        yaxis_title='Department',
        font_family='Roboto',
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff'
    )
    
    # Table: Cost Summary by State
    cost_summary = filtered_df.groupby('State')[['Premium Cost', 'Employer Cost', 'Employee Cost']].sum().reset_index()
    fig9 = go.Figure(data=[go.Table(
        header=dict(values=['State', 'Total Premium Cost ($)', 'Employer Cost ($)', 'Employee Cost ($)'],
                    fill_color='paleturquoise',
                    align='left',
                    font_family='Roboto'),
        cells=dict(values=[cost_summary['State'],
                           cost_summary['Premium Cost'].round(2),
                           cost_summary['Employer Cost'].round(2),
                           cost_summary['Employee Cost'].round(2)],
                   fill_color='lavender',
                   align='left',
                   font_family='Roboto'))
    ])
    fig9.update_layout(title='Cost Summary by State', font_family='Roboto', plot_bgcolor='#ffffff', paper_bgcolor='#ffffff')
    
    return (fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9,
            f"${total_premium_cost:,.2f}",
            f"${total_employee_cost:,.2f}",
            f"${total_employer_cost:,.2f}",
            f"${total_potential_savings:,.2f}",
            f"Estimated Savings for {ppo_switch or 0} PPO Employees Switching to HSA: ${calculated_savings:,.2f}")

# Run the app
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8050))
    app.run_server(host="0.0.0.0", port=port, debug=False)
