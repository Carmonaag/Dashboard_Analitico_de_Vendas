
from dash import html
import dash_bootstrap_components as dbc

def create_kpi_card(title, value, formatter=lambda x: f"R$ {x:,.2f}"):
    """Cria um card de KPI."""
    return dbc.Col(
        dbc.Card(
            dbc.CardBody([
                html.H4(title, className="card-title"),
                html.P(formatter(value), className="card-text")
            ])
        ),
        md=4
    )
