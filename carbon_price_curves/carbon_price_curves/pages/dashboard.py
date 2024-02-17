"""The dashboard page."""
from carbon_price_curves.templates import template

import reflex as rx
import plotly.express as px
import pandas as pd

@template(route="/dashboard", title="Dashboard")
def dashboard() -> rx.Component:
    """The dashboard page.

    Returns:
        The UI for the dashboard page.
    """

    # df = px.data.gapminder().query("country=='Canada'")
    df = pd.read_csv('assets/cdr_data_test.csv')

    fig = px.line(
        df,
        x="CDR Purchases",
        y="Total Sales",
        title="Global total carbon dioxide removal sales 2020-2023",
    )

    graph : rx.Component = rx.chakra.vstack(
        rx.chakra.text("Global total carbon dioxide removal sales 2020-2023"),
        rx.plotly(data=fig, height="400px"),
    )

    year_slider : rx.Component = slider_year_on_change()

    return rx.chakra.vstack(
        rx.chakra.heading("Carbon Credits Forecast", font_size="3em", padding="25px",),
        rx.box(
            year_slider,
            width="100%",
            padding="25px",
        ),
        rx.box(
            graph,
            width="60%",
        ),
        width="100%",
    )

# Year Slider
class SliderYearState(rx.State):
    year: int = 2024

    def set_year(self, yr: int):
        self.year = yr

def slider_year_on_change() -> rx.Component:
    return rx.vstack(
        rx.heading("Year: ", SliderYearState.year, align="center"),
        rx.slider(
            default_value = 2030,
            min=2024,
            max=2050,
            step=1,
            on_change=SliderYearState.set_year,
            width="100%",
        ),
        width="100%",
    )