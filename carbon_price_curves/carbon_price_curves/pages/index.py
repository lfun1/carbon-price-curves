"""The home page of the app."""

from carbon_price_curves import styles
from carbon_price_curves.templates import template
from typing import List
import reflex as rx
from functools import partial

options_1: List[str] = ["1_Option 1", "1_Option 2", "1_Option 3"]
options_2: List[str] = ["2_Option 1", "2_Option 2", "2_Option 3"]
options_3: List[str] = ["3_Option 1", "3_Option 2", "3_Option 3"]
options_4: List[str] = ["4_Option 1", "4_Option 2", "4_Option 3"]

class FormState(rx.State):
    form_data: dict = {}

    def handleSubmit(self, form_data: dict):
        """Handle the form submit."""
        self.form_data = form_data

@template(route="/", title="Home", image="/github.svg")
def index() -> rx.Component:
    """The home page.

    Returns:
        The UI for the home page.
    """            
    return rx.container(
        rx.heading(
            "Carbon Price Curves", size = "9",
        ),
        rx.vstack(
            rx.form(
                rx.vstack(
                    rx.chakra.select(
                        options_1,
                        is_multi=True,
                        placeholder="1. Select an example.",
                        name = "option_1"
                        ),
                    rx.chakra.select(
                        options_2,
                        # is_multi=True,
                        placeholder="2. Select an example.",
                        name = "option_2"
                        ),
                    rx.chakra.select(
                        options_3,
                        # is_multi=True,
                        placeholder="3. Select an example.",
                        name = "option_3"
                        ),
                    rx.chakra.select(
                        options_4,
                        # is_multi=True,
                        placeholder="4. Select an example.",
                        name = "option_4"
                        ),
                    rx.button("Submit", type="submit"),
                ),
                on_submit=FormState.handleSubmit,
                reset_on_submit=True,
            ),
            rx.divider(),
            rx.heading("Results"),
            rx.text(FormState.form_data.to_string()),
        ),
        rx.box(
            "A way to buid apps in pure Python!\n",
            text_align = "left",
        ),
    )
