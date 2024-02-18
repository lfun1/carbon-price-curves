"""The home page of the app."""
import plotly.graph_objects as go
from carbon_price_curves import styles
from carbon_price_curves.templates import template
from typing import List
import reflex as rx
from functools import partial

# Added for graph
import plotly.express as px
import pandas as pd

options_1: List[str] = ["Technology", "Manufacturing", "Retail", "Finance", "Oil/Gas", "Other"]
# options_2: List[str] = ["2_Option 1", "2_Option 2", "2_Option 3"]
# options_3: List[str] = ["3_Option 1", "3_Option 2", "3_Option 3"]
# options_4: List[str] = ["4_Option 1", "4_Option 2", "4_Option 3"]

# Added for graph
df_test = pd.read_csv('assets/cdr_data_test.csv')
df_supply_2024 = pd.read_csv('assets/default_supply.csv')
df_demand_market = pd.read_csv('assets/demand_market_2024_v2.csv')

fig_test = px.line(
    df_test,
    x="CDR Purchases",
    y="Total Sales",
    title="Global total carbon dioxide removal sales 2020-2023",
)

fig_supply_2024 = px.line(
    df_supply_2024,
    x="Quantiy",
    y="Price",
    title="Carbon Credits Market 2024",
)

fig_demand_market = px.line(
    df_demand_market,
    x="Quantiy",
    y="Price",
)

combined_fig = go.Figure()

# Add traces from fig_supply_2024 to the new figure
for trace in fig_supply_2024.data:
    combined_fig.add_trace(trace)

# Add traces from fig_demand_market to the new figure
for trace in fig_demand_market.data:
    combined_fig.add_trace(trace)

# Update layout from fig_supply_2024
combined_fig.update_layout(fig_supply_2024.layout)

#Custom x-axis limit.
combined_fig.update_layout(xaxis=dict(range=[0, 3000000000]))

graph_market_2024 : rx.Component = rx.chakra.vstack(
    rx.chakra.heading("Carbon Credits Market 2024"),
    rx.plotly(data=combined_fig, height="400px"),
)

class FormState(rx.State):
    form_data: dict = {}
    goal_year: int = 2035,
    goal_reduction: int = 50,
    percentage_change: int = 0,
    model_length: int = 15,

    def set_end(self, goal_year: int):
        self.goal_year = goal_year

    def set_red(self, goal_reduction: int):
        self.goal_reduction = goal_reduction

    def set_change(self, percentage_change: int):
        self.percentage_change = percentage_change

    def setModelLength(self, model_length: int):
        self.model_length = model_length

    def handleSubmit(self, form_data: dict):
        self.form_data = form_data

@template(route="/", title="Home", image="/github.svg")
def index() -> rx.Component:
    rx.heading(
                "Carbon Price Curves", size = "9",
        ),
    
    return rx.box(
        rx.box(
            rx.divider(),
            rx.heading("Selected variables"),
            rx.text(FormState.form_data.to_string()),
            elias = FormState.form_data.to_string(),
            margin_bottom="20px",
            text_size="3em",
        ),
        rx.box(
            rx.box(
                graph_market_2024,
                rx.text(
                    "Default graphs",
                ),
                background_color="white",
                border_radius="5px",
                width="80%",
                text_align="center",
                display="inline-block",
                margin_left=0,
                float="left",
            ),
            rx.box(
                rx.text(
                    "Model Variables",
                    padding_bottom="20px",
                    fontWeight="bold",
                ),
                rx.text(
                    "Model Length ",
                    FormState.model_length,
                    " years",
                    padding_bottom="10px",
                ),
                rx.slider(
                    default_value=15,
                    min=0,
                    max=30,
                    on_change=FormState.setModelLength,
                    step=1,
                    width="100%",
                    name="model_length",
                ),
                rx.text(
                    "Choose Scope that apply",
                    padding_top="10px",
                    padding_bottom="10px",
                ),
                rx.checkbox(
                    "Scope 1",
                    default_checked=False,
                    spacing="2",
                    name = "scope_1",
                ),
                rx.checkbox(
                    "Scope 2",
                    default_checked=False,
                    spacing="2",
                    name = "scope_2",
                ),
                rx.checkbox(
                    "Scope 3",
                    default_checked=False,
                    spacing="2",
                    name = "scope_3",
                ),
                rx.text(
                    "Company Variables",
                    padding_top="20px",
                    padding_bottom="20px",
                    fontWeight="bold",
                ),
                    rx.container(
                    rx.vstack(
                        rx.form(
                            rx.vstack(
                                rx.chakra.select(
                                    options_1,
                                    is_multi=True,
                                    placeholder="Select Industry",
                                    name = "industry"
                                    ),
                                    rx.text(
                                        "Goal Year ",
                                        FormState.goal_year,
                                    ),
                                rx.slider(
                                    default_value=2035,
                                    min=2024,
                                    max=2050,
                                    on_change=FormState.set_end,
                                    step=1,
                                    width="100%",
                                    name="goal_year",
                                ),
                                    rx.text(
                                        "Goal Reduction ",
                                        FormState.goal_reduction,
                                        "%",
                                    ),
                                rx.slider(
                                    default_value=50,
                                    min=0,
                                    max=100,
                                    on_change=FormState.set_red,
                                    step=1,
                                    width="100%",
                                    name="goal_red",
                                ),
                                    rx.text(
                                        "Reduction Path",
                                    ),
                                rx.checkbox(
                                    "CSS",
                                    default_checked=False,
                                    spacing="2",
                                    name = "css",
                                ),
                                rx.checkbox(
                                    "Bio Char",
                                    default_checked=False,
                                    spacing="2",
                                    name = "bio_char",
                                ),
                                rx.checkbox(
                                    "Mineralization",
                                    default_checked=False,
                                    spacing="2",
                                    name = "mineralization",
                                ),
                                rx.checkbox(
                                    "DAC",
                                    default_checked=False,
                                    spacing="2",
                                    name = "dac",
                                ),
                                rx.text(
                                        "Percentage Change ",
                                        FormState.percentage_change,
                                        "%",
                                    ),
                                rx.slider(
                                    default_value=0,
                                    min=-100,
                                    max=100,
                                    on_change=FormState.set_change,
                                    step=1,
                                    width="100%",
                                    name="goal_red",
                                ),
                                rx.text(
                                        "Current emissions",
                                    ),
                                rx.input(
                                    placeholder="Your current emissions",
                                    name = "cur_emission",
                                    width = "100%",
                                ),
                                    rx.text(
                                        "Current Market Price ($/ton C02)",
                                    ),
                                rx.input(
                                    placeholder="Current Market Price",
                                    name = "market_price",
                                    width = "100%",
                                ),
                                rx.text(
                                        "Willing to pay ($/ton C02)",
                                    ),
                                rx.input(
                                    placeholder="How much you wann pay?",
                                    name = "company_price",
                                    width = "100%",
                                ),
                                # rx.chakra.select(
                                #     options_2,
                                #     # is_multi=True,
                                #     placeholder="2. Select an example.",
                                #     name = "option_2"
                                #     ),
                                # rx.chakra.select(
                                #     options_3,
                                #     # is_multi=True,
                                #     placeholder="3. Select an example.",
                                #     name = "option_3"
                                #     ),
                                # rx.chakra.select(
                                #     options_4,
                                #     # is_multi=True,
                                #     placeholder="4. Select an example.",
                                #     name = "option_4"
                                #     ),
                                rx.button("Submit", type="submit"),
                            ),
                            on_submit=FormState.handleSubmit,
                            reset_on_submit=True,
                        ),
                    ),
                ),
                background_color="#CEFFEE",
                box_shadow="rgba(0, 0, 0, 0.15) 0px 2px 8px",
                border_radius="5px",
                width="20%",
                text_align="center",
                display="inline-block",
                margin_right=0,
                float="right",
                margin_left = "8px",
                padding="20px",
            ),
            display="flex",
            margin=0,
            padding=0,
            height="100%",
            box_shadow = "0px 0px 0px 1px rgba(84, 82, 95, 0.14)",
        )
    )