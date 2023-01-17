from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

# Create dash app instance
app = Dash(external_stylesheets=[dbc.themes.LUX])

# Dashboard Title
app.title = 'Dashboard Employee Promotion'

# Dashboard Component

## 1. NAVBAR
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Page 1", href="#")),
    ],
    brand="Employee Promotion Dashboard",
    brand_href="#",
    color="#000000",
    dark=True,
)

## 2. Load Data Set

promotion = pd.read_csv('promotion_clean.csv')
promotion[['department','region','education',
           'gender','recruitment_channel',
           'KPIs_met >80%','awards_won?',
           'is_promoted']] = promotion[['department','region',
                                        'education','gender',
                                        'recruitment_channel',
                                        'KPIs_met >80%','awards_won?',
                                        'is_promoted']].astype('category')

promotion[['date_of_birth','join_date']] = promotion[['date_of_birth','join_date']].astype('datetime64')

## 3. Card Content
#### Card Content 1
information_card = [
    dbc.CardHeader('Information'),
    dbc.CardBody([
        html.P('This is the information of employeed in our Start-Up. help to identify who is a potential candidate for promotion'),
    ])
]

#### Card Content 2
employee_card = [
    dbc.CardHeader('Total Employee'),
    dbc.CardBody([
        html.H1(promotion.shape[0])
    ]),
]

#### Card Content 3
promotion_card = [
    dbc.CardHeader('Number of employees promoted'),
    dbc.CardBody([
        html.H1(promotion[promotion['is_promoted']=='Yes'].shape[0], style={'color':'red'})
    ]),
]


### Barplot1
data_agg = promotion.groupby(['department','is_promoted']).count()[['employee_id']].reset_index()
data_agg = data_agg.sort_values(by = 'employee_id')
bar_plot1 = px.bar(
    data_agg,
    x = 'employee_id',
    y = 'department',
    color = 'is_promoted',
    color_discrete_sequence = ['#618685','#80ced6'],
    barmode = 'group',
    orientation='h',
    template = 'ggplot2',
    labels = {
        'department': 'Department',
        'employee_id': 'No of Employee',
        'is_promoted': 'Is Promoted?',
    },
    title = 'Number of employees in each department',
    height=700,
).update_layout(showlegend=False)

### Lineplot2
data_2020 = promotion[promotion['join_date'] >= '2020-01-01']
data_2020 = data_2020.groupby(['join_date']).count()['employee_id'].reset_index().tail(30)
line_plot2 = px.line(
    data_2020,
    x='join_date',
    y='employee_id',
    markers=True,
    color_discrete_sequence = ['#618685'],
    template = 'ggplot2',
    labels={
        'join_date':'Join date',
        'employee_id':'Number of employee'
    },
    title = 'Number of new hires in the last 30 days',
    height=700,
)

# User Interface
app.layout = html.Div([
    navbar,
    html.Br(),

    #### ----ROW1----
    dbc.Row([

        ## Row 1 Col 1
        dbc.Col(dbc.Card(information_card, color='#fefbd8'), width=6),

        ## Row 1 Col 2
        dbc.Col(dbc.Card(employee_card, color='#80ced6'), width=3),

        ## Row 1 Col 3
        dbc.Col(dbc.Card(promotion_card, color='#d5f4e6'), width=3),

    ]),

    html.Br(),

    ### ----ROW2----
    dbc.Row([

        ## Row 2 Col 1
        dbc.Col(dbc.Tabs([
            # Tab 1
            dbc.Tab(dcc.Graph(figure=bar_plot1),
            label='Each Department'),

            # Tab 2
            dbc.Tab(dcc.Graph(figure=line_plot2),
            label='New Hire'),
        ])),

        ## Row 2 Col 2
        dbc.Col([
            dcc.Dropdown(
                id='choose_dept',
                options=promotion['department'].unique(),
                value='Technology',
            ),
            dcc.Graph(id='plot3'),
        ]),

    ]),
])

@app.callback(
    Output(component_id='plot3', component_property='figure'),
    Input(component_id='choose_dept', component_property='value')
)

def update_plot(dept_name):
    data_agg = promotion[promotion['department'] == dept_name]
    hist_plot3 = px.histogram(
        data_agg,
        x = 'length_of_service',
        nbins = 20,
        color_discrete_sequence = ['#618685','#80ced6'],
        title = f'Length of Service Distribution in {dept_name} Department',
        template = 'ggplot2',
        labels={
            'length_of_service': 'Length of Service (years)',
        },
        marginal = 'box',
        height=700,
    )
    return hist_plot3

# Run app at local
if __name__ == '__main__':
    app.run_server(debug=True)