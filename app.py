from dash import Dash, html, dcc, Input, Output
from utils import BSMEuropeanContinuousDiscounting, HeatMap
from plotly.express import imshow

app = Dash(__name__)

app.layout = html.Div(
    style={
        'backgroundColor': '#0E1117',
        'color': '#FAFAFA',
        'minHeight': '100vh',
        'display': 'flex',
        'fontFamily': 'Inter, sans-serif',
    },
    children=[
        # Sidebar
        html.Div(
            style={
                'width': '22%',
                'padding': '40px 25px',
                'backgroundColor': '#161A23',
                'display': 'flex',
                'flexDirection': 'column',
                'gap': '16px',
                'boxShadow': '2px 0 6px rgba(0,0,0,0.3)',
                'borderRight': '1px solid #222'
            },
            children=[
                html.H2("⚙️ Black–Scholes Inputs", style={'fontWeight': '600', 'marginBottom': '10px'}),

                html.Label("Stock Price (S)"),
                dcc.Input(id='S', type='number', value=100, step=1,
                        style={'backgroundColor': '#262B3C', 'color': 'white', 'borderRadius': '8px',
                                'border': 'none', 'padding': '8px'}),

                html.Label("Strike Price (K)"),
                dcc.Input(id='K', type='number', value=100, step=1,
                        style={'backgroundColor': '#262B3C', 'color': 'white', 'borderRadius': '8px',
                                'border': 'none', 'padding': '8px'}),

                html.Label("Time to Maturity (T, years)"),
                dcc.Input(id='T', type='number', value=1, step=0.1,
                        style={'backgroundColor': '#262B3C', 'color': 'white', 'borderRadius': '8px',
                                'border': 'none', 'padding': '8px'}),

                html.Label("Risk-free Rate (r)"),
                dcc.Input(id='r', type='number', value=0.05, step=0.01,
                        style={'backgroundColor': '#262B3C', 'color': 'white', 'borderRadius': '8px',
                                'border': 'none', 'padding': '8px'}),

                html.Label("Volatility (σ)"),
                dcc.Input(id='sigma', type='number', value=0.2, step=0.01,
                        style={'backgroundColor': '#262B3C', 'color': 'white', 'borderRadius': '8px',
                                'border': 'none', 'padding': '8px'}),

                # Heatmap Parameters section
                html.H3("📊 Heatmap Parameters", style={'marginTop': '30px', 'fontWeight': '600'}),

                html.Label("Your Call/Put Prices"),
                html.Div(
                    style={
                        'display': 'flex',
                        'gap': '10px',
                        'width': '100%'
                    },
                    children=[
                        html.Div([
                            html.Label("Call"),
                            dcc.Input(id='user_call_price', type='number', step=0.1,
                                    style={'backgroundColor': '#262B3C', 'color': 'white', 'borderRadius': '8px',
                                            'border': 'none', 'padding': '8px', 'width': '100%'})
                        ], style={'flex': 1}),
                        html.Div(style={
                            'width': '1px',
                            'height': '40px',
                            'backgroundColor': 'transparant'
                        }),
                        html.Div([
                            html.Label("Put"),
                            dcc.Input(id='user_put_price', type='number', step=0.1,
                                    style={'backgroundColor': '#262B3C', 'color': 'white', 'borderRadius': '8px',
                                            'border': 'none', 'padding': '8px', 'width': '100%'})
                        ], style={'flex': 1})
                    ]
                ),

                html.Label("Variance Range"),
                dcc.RangeSlider(
                    id='variance_slider',
                    min=0.05, max=0.9, step=0.01,
                    value=[0.1, 0.4],
                    marks=None,
                    tooltip={'placement': 'bottom', 'always_visible': True}
                ),

                html.Label("Spot Price Range"),
                dcc.RangeSlider(
                    id='spot_slider',
                    min=50, max=150, step=1,
                    value=[80, 120],
                    marks=None,
                    tooltip={'placement': 'bottom', 'always_visible': True}
                )
            ]
        ),

        # Main section
        html.Div(
            style={
                'flex': 1,
                'padding': '50px 60px',
                'display': 'flex',
                'flexDirection': 'column',
                'gap': '25px',
                'alignItems': 'center',
                'justifyContent': 'center',
                'textAlign': 'center',
                'margin': 'auto'
            },
            children=[
                html.H1("Option Pricing Dashboard", style={'fontWeight': '700'}),
                html.Div(id='option_prices', style={
                    'backgroundColor': '#161A23',
                    'padding': '20px',
                    'borderRadius': '10px',
                    'boxShadow': '0 2px 6px rgba(0,0,0,0.25)'
                }),
            ]
        )
    ]
)

@app.callback(
    Output('option_prices', 'children'),
    Input('S', 'value'),
    Input('K', 'value'),
    Input('T', 'value'),
    Input('r', 'value'),
    Input('sigma', 'value'),
    Input('variance_slider', 'value'),
    Input('spot_slider', 'value')
)
def update_prices(S, K, T, r, sigma, var_range, spot_range):
    call_option, call_option_spot, call_option_volatility = BSMEuropeanContinuousDiscounting(
        underlying_spot=S, risk_free_rate=r, volatility=sigma,
        time_to_expiry=T, strike_price=K, type='call'
    )
    put_option, put_option_spot, put_option_volatility = BSMEuropeanContinuousDiscounting(
        underlying_spot=S, risk_free_rate=r, volatility=sigma,
        time_to_expiry=T, strike_price=K, type='put'
    )

    call_price = call_option.NPV()
    put_price = put_option.NPV()

    call_color = '#155724' if S >= K else '#721c24'
    put_color = '#155724' if S <= K else '#721c24'

    # Generate heatmaps
    call_fig = HeatMap(
        call_option,
        call_option_spot,
        call_option_volatility,
        var_range[0],
        var_range[1],
        spot_range[0],
        spot_range[1]
    )
    put_fig = HeatMap(
        put_option,
        put_option_spot,
        put_option_volatility,
        var_range[0],
        var_range[1],
        spot_range[0],
        spot_range[1],
        showscale=True
    )
    call_fig.update_layout(
        autosize=True,
        height=500,
        width=700,
        margin=dict(l=40, r=40, t=40, b=40)
    )
    put_fig.update_layout(
        autosize=True,
        height=500,
        width=700,
        margin=dict(l=40, r=40, t=40, b=40)
    )

    return html.Div(
        style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center', 'gap': '40px'},
        children=[
            html.Div(
                style={'display': 'flex', 'justifyContent': 'center', 'gap': '30px'},
                children=[
                    html.Div([
                        html.H3("Call Option", style={'marginBottom': '8px'}),
                        html.P(f"Price: {call_price:.4f}")
                    ], style={
                        'backgroundColor': call_color,
                        'padding': '20px',
                        'borderRadius': '10px',
                        'width': '200px',
                        'boxShadow': '0 2px 6px rgba(0,0,0,0.25)'
                    }),
                    html.Div([
                        html.H3("Put Option", style={'marginBottom': '8px'}),
                        html.P(f"Price: {put_price:.4f}")
                    ], style={
                        'backgroundColor': put_color,
                        'padding': '20px',
                        'borderRadius': '10px',
                        'width': '200px',
                        'boxShadow': '0 2px 6px rgba(0,0,0,0.25)'
                    })
                ]
            ),
            html.Div(
                style={
                    'display': 'flex',
                    'justifyContent': 'center',
                    'alignItems': 'flex-start',
                    'gap': '40px',
                    'width': '100%'
                },
                children=[
                    html.Div([
                        html.H4("Call Option Heatmap", style={'textAlign': 'center'}),
                        dcc.Graph(figure=call_fig, style={'width': '600px', 'height': '500px'})
                    ]),
                    html.Div([
                        html.H4("Put Option Heatmap", style={'textAlign': 'center'}),
                        dcc.Graph(figure=put_fig, style={'width': '600px', 'height': '500px'})
                    ])
                ]
            )

        ]
    )


if __name__ == "__main__":
    app.run_server(debug=True)
