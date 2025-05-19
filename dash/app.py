import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import requests
import pandas as pd

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.H1("Product Tracking System Dashboard"),
    
    # Dashboard
    html.Div(id='dashboard'),
    dcc.Interval(id='interval-component', interval=5*1000, n_intervals=0),
    
    # Forms
    html.H2("Manage Data"),
    
    # POST Form
    html.Div([
        html.H3("Add Product"),
        dbc.Input(id='post-name', placeholder='Enter product name', type='text'),
        dbc.Input(id='post-type', placeholder='Enter product type', type='text'),
        dbc.Input(id='post-age-group', placeholder='Enter age group', type='text'),
        dbc.Input(id='post-gender', placeholder='Enter gender', type='text'),
        dbc.Input(id='post-year', placeholder='Enter year', type='number'),
        dbc.Input(id='post-retail-price', placeholder='Enter retail price', type='number'),
        dbc.Input(id='post-factory-cost', placeholder='Enter factory cost', type='number'),
        dbc.Input(id='post-target-cost', placeholder='Enter target cost', type='number'),
        dbc.Input(id='post-sold', placeholder='Enter sold', type='number'),
        dbc.Button('Add', id='post-button', n_clicks=0),
        html.Div(id='post-response')
    ]),
    
    # PUT Form
    html.Div([
        html.H3("Update Product"),
        dbc.Input(id='put-id', placeholder='Enter product ID', type='number'),
        dbc.Input(id='put-name', placeholder='Enter new product name', type='text'),
        dbc.Input(id='put-type', placeholder='Enter new product type', type='text'),
        dbc.Input(id='put-age-group', placeholder='Enter new age group', type='text'),
        dbc.Input(id='put-gender', placeholder='Enter new gender', type='text'),
        dbc.Input(id='put-year', placeholder='Enter new year', type='number'),
        dbc.Input(id='put-retail-price', placeholder='Enter new retail price', type='number'),
        dbc.Input(id='put-factory-cost', placeholder='Enter new factory cost', type='number'),
        dbc.Input(id='put-target-cost', placeholder='Enter new target cost', type='number'),
        dbc.Input(id='put-sold', placeholder='Enter new sold', type='number'),
        dbc.Button('Update', id='put-button', n_clicks=0),
        html.Div(id='put-response')
    ]),
    
    # DELETE Form
    html.Div([
        html.H3("Delete Product"),
        dbc.Input(id='delete-id', placeholder='Enter product ID', type='number'),
        dbc.Button('Delete', id='delete-button', n_clicks=0),
        html.Div(id='delete-response')
    ])
])

@app.callback(
    Output('dashboard', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_dashboard(n):
    response = requests.get('http://localhost:5000/get_shoes')
    if response.status_code == 200:
        shoes = response.json()
        df = pd.DataFrame(shoes)
        
        line_chart = dcc.Graph(
            figure={
                'data': [
                    {'x': df['year'], 'y': df['sold'], 'type': 'line', 'name': 'Sold'},
                    {'x': df['year'], 'y': df['retail_price'], 'type': 'line', 'name': 'Retail Price'}
                ],
                'layout': {
                    'title': 'Yearly Sales and Retail Price'
                }
            }
        )
        
        pie_chart = dcc.Graph(
            figure={
                'data': [
                    {'values': df['sold'], 'labels': df['type'], 'type': 'pie'}
                ],
                'layout': {
                    'title': 'Sales Distribution by Product Type'
                }
            }
        )
        
        return html.Div([
            line_chart,
            pie_chart,
            dbc.Table.from_dataframe(
                df,
                striped=True,
                bordered=True,
                hover=True
            )
        ])
    return "Error fetching data"

@app.callback(
    Output('post-response', 'children'),
    Input('post-button', 'n_clicks'),
    State('post-name', 'value'),
    State('post-type', 'value'),
    State('post-age-group', 'value'),
    State('post-gender', 'value'),
    State('post-year', 'value'),
    State('post-retail-price', 'value'),
    State('post-factory-cost', 'value'),
    State('post-target-cost', 'value'),
    State('post-sold', 'value')
)
def add_product(n_clicks, name, type, age_group, gender, year, retail_price, factory_cost, target_cost, sold):
    if n_clicks > 0:
        response = requests.post('http://api.example.com/products', json={
            'name': name,
            'type': type,
            'age_group': age_group,
            'gender': gender,
            'year': year,
            'retail_price': retail_price,
            'factory_cost': factory_cost,
            'target_cost': target_cost,
            'sold': sold
        })
        if response.status_code == 201:
            return "Product added successfully"
        return "Error adding product"
    return ""

@app.callback(
    Output('put-response', 'children'),
    Input('put-button', 'n_clicks'),
    State('put-id', 'value'),
    State('put-name', 'value'),
    State('put-type', 'value'),
    State('put-age-group', 'value'),
    State('put-gender', 'value'),
    State('put-year', 'value'),
    State('put-retail-price', 'value'),
    State('put-factory-cost', 'value'),
    State('put-target-cost', 'value'),
    State('put-sold', 'value')
)
def update_product(n_clicks, id, name, type, age_group, gender, year, retail_price, factory_cost, target_cost, sold):
    if n_clicks > 0:
        response = requests.put(f'http://api.example.com/products/{id}', json={
            'name': name,
            'type': type,
            'age_group': age_group,
            'gender': gender,
            'year': year,
            'retail_price': retail_price,
            'factory_cost': factory_cost,
            'target_cost': target_cost,
            'sold': sold
        })
        if response.status_code == 200:
            return "Product updated successfully"
        return "Error updating product"
    return ""

@app.callback(
    Output('delete-response', 'children'),
    Input('delete-button', 'n_clicks'),
    State('delete-id', 'value')
)
def delete_product(n_clicks, id):
    if n_clicks > 0:
        response = requests.delete(f'http://api.example.com/products/{id}')
        if response.status_code == 200:
            return "Product deleted successfully"
        return "Error deleting product"
    return ""

if __name__ == '__main__':
    app.run_server(debug=True)