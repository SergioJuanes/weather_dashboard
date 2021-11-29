
def create_card_forecast():
    return html.Div([
                dbc.Card(
                    [
                            html.Div(id = 'icon_day_one', className="forecast-card-icon"),
                        dbc.CardBody(
                            html.Div([
                                html.P(id = 'temp_day_one'),
                                html.P(id = 'forecast_day_one'),
                            ], className="forecast-card-text")
                            
                        ),
                    ],
                    style={"width": "18rem"},
                )
            ]),