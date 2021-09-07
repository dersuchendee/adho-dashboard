import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from layouts import example_graph1, example_graph2, example_graph3, example_graph4, example_graph5, example_graph6, example_graph9
from app import app

@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "active_tab"),
)
def render_tab_content(active_tab):
    """
    This callback takes the 'active_tab' property as input, and 
    renders the associated graph with the tab name on page 1.
    """
    if active_tab is not None:
        if active_tab == "graph1":
            return dcc.Graph(figure=example_graph1, id='graph')
        elif active_tab == "graph2":
            return dcc.Graph(figure=example_graph2, id='graph')
        elif active_tab == "graph3":
            return dcc.Graph(figure=example_graph3, id='graph')
        elif active_tab == "graph4":
            return dcc.Graph(figure=example_graph4, id='graph')
        elif active_tab == "graph5":
            return dcc.Graph(figure=example_graph5, id='graph')
        elif active_tab == "graph6":
            return dcc.Graph(figure=example_graph6, id='graph')
        elif active_tab == "graph9":
            return dcc.Graph(figure=example_graph9, id='graph')
    return "No tab selected"

@app.callback(
    Output("graph-text","children"),
    Input("graph","clickData"),
)
def graph_click(clickData):
    """
    This callback identifies if the clicked upon graph is a scatter plot 
    or a historgram and displays data clicked on
    """
    if 'pointIndex' in clickData['points'][0]:
        return html.P(f"Date: {clickData['points'][0]['x']}\nTweets: {clickData['points'][0]['y']}") #ok non funzia
    elif 'binNumber' in clickData['points'][0]:
        return html.P(f"Hashtag: {clickData['points'][0]['x']}\nCount: {clickData['points'][0]['y']}")

@app.callback(
    Output("selected-button","children"),
    Input("page2-buttons","value")
)
def button_choice(value):
    """
    This callback takes in page2-buttons selected value and returns content to display
    in selected-button
    """
    return 'You have selected "{}"'.format(value)

@app.callback(
    Output("selected-dropdown","children"),
    Input("page2-dropdown","value")
)
def dropdown_choice(value):
    """
    This callback takes in page2-dropdown's selected value and returns content to display
    in selected-button
    """
    return 'You have selected "{}"'.format(value)