"""The dashboard page."""
from carbon_price_curves.templates import template

import reflex as rx
import plotly.express as px

@template(route="/dashboard", title="Dashboard")
def dashboard() -> rx.Component:
    """The dashboard page.

    Returns:
        The UI for the dashboard page.
    """

    df = px.data.gapminder().query("country=='Canada'")

    fig = px.line(
        df,
        x="year",
        y="lifeExp",
        labels={
            "year": "Year",
            "lifeExp": "Life Expectancy (years)",
        },
        title="Life expectancy in Canada",
    )

    graph : rx.Component = rx.chakra.vstack(
        rx.chakra.text("Graph"),
        rx.plotly(data=fig, height="400px"),
    )

    year_slider : rx.Component = slider_year_on_change()

    return rx.chakra.vstack(
        rx.chakra.heading("Carbon Credits Forecast", font_size="3em"),
        year_slider,
        graph,
    )

class SliderYearState(rx.State):
    year: int = 2024

    def set_year(self, yr: int):
        self.year = yr

def slider_year_on_change() -> rx.Component:
    return rx.vstack(
        rx.heading("Year: ", SliderYearState.year),
        rx.slider(
            default_value = 2030,
            min=2024,
            max=2050,
            step=1,
            on_change=SliderYearState.set_year,
            width="100%",
        ),
    )