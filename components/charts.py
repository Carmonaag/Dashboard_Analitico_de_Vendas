
import plotly.express as px
import plotly.graph_objects as go

def create_sales_evolution_chart(sales_evolution):
    """Cria o gráfico de evolução de vendas."""
    fig = px.line(sales_evolution, x='data', y='receita', title='Evolução de Vendas', labels={'data': 'Mês', 'receita': 'Receita'})
    fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))
    return fig

def create_category_sales_chart(category_sales):
    """Cria o gráfico de vendas por categoria."""
    fig = px.pie(category_sales, names='categoria', values='receita', title='Vendas por Categoria')
    fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))
    return fig

def create_top_products_chart(top_products):
    """Cria o gráfico de top 10 produtos."""
    fig = px.bar(top_products, x='receita', y='produto', orientation='h', title='Top 10 Produtos por Receita')
    fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))
    return fig

def create_region_heatmap(region_heatmap_data):
    """Cria o mapa de calor de vendas por região."""
    fig = px.imshow(region_heatmap_data, title='Mapa de Calor: Receita por Região e Categoria', labels=dict(x="Categoria", y="Região", color="Receita"))
    fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))
    return fig

def create_trend_analysis_chart(daily_sales, trend_line):
    """Cria o gráfico de análise de tendência."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=daily_sales['dias_desde_inicio'], y=daily_sales['receita'], mode='markers', name='Vendas Diárias'))
    if trend_line is not None:
        fig.add_trace(go.Scatter(x=daily_sales['dias_desde_inicio'], y=trend_line, mode='lines', name='Linha de Tendência', line=dict(color='red')))
    fig.update_layout(title='Análise de Tendência de Vendas', xaxis_title='Dias desde o Início do Período', yaxis_title='Receita')
    fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))
    return fig

def create_sales_forecast_chart(daily_sales, trend_line, future_days, future_sales):
    """Cria o gráfico de previsão de vendas."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=daily_sales['dias_desde_inicio'], y=daily_sales['receita'], mode='markers', name='Vendas Diárias'))
    if trend_line is not None:
        fig.add_trace(go.Scatter(x=daily_sales['dias_desde_inicio'], y=trend_line, mode='lines', name='Linha de Tendência', line=dict(color='red')))
    if future_days is not None:
        fig.add_trace(go.Scatter(x=future_days.flatten(), y=future_sales, mode='lines', name='Previsão (30 dias)', line=dict(color='green', dash='dash')))
    fig.update_layout(title='Previsão de Vendas (Próximos 30 dias)', xaxis_title='Dias desde o Início do Período', yaxis_title='Receita')
    fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))
    return fig
