"""The home page of the app."""

from carbon_price_curves import styles
from carbon_price_curves.templates import template
from typing import List
import reflex as rx

options_1: List[str] = ["1_Option 1", "1_Option 2", "1_Option 3"]
options_2: List[str] = ["2_Option 1", "2_Option 2", "2_Option 3"]
options_3: List[str] = ["3_Option 1", "3_Option 2", "3_Option 3"]
options_4: List[str] = ["4_Option 1", "4_Option 2", "4_Option 3"]

@template(route="/", title="Home", image="/github.svg")
def index() -> rx.Component:
    """The home page.

    Returns:
        The UI for the home page.
    """
    # with open("README.md", encoding="utf-8") as readme:
    #     content = readme.read()
    # return rx.markdown(content, component_map=styles.markdown_style)
    class MultiSelectState_1(rx.State):
        option_1: List[str] = []
        option_2: List[str] = []
        option_3: List[str] = []
        option_4: List[str] = []

        def extract_options(self):
            options: List[str] = []
            options.append(options_1[len(options_1) - 1])
            options.append(options_2[len(options_2) - 1])
            options.append(options_3[len(options_3) - 1])
            options.append(options_4[len(options_4) - 1])
            return options
        
    return rx.container(
        rx.heading(
            "Carbon Price Curves",
        ),
        rx.chakra.vstack(
            rx.chakra.heading("Put in your details"),
            rx.chakra.select(
                options_1,
                is_multi=True,
                on_change=MultiSelectState_1.set_option_1,
                placeholder="Select an example.",
                variant="outline",
                ),
            rx.chakra.select(
                options_2,
                is_multi=True,
                on_change=MultiSelectState_1.set_option_2,
                placeholder="Select an example.",
                variant="outline",
                ),
            rx.chakra.select(
                options_3,
                is_multi=True,
                on_change=MultiSelectState_1.set_option_2,
                placeholder="Select an example.",
                variant="outline",
                ),
            rx.chakra.select(
                options_4,
                is_multi=True,
                on_change=MultiSelectState_1.set_option_2,
                placeholder="Select an example.",
                variant="outline",
                ),
        ),

        # rx.chakra.vstack(
        #     rx.chakra.heading(MultiSelectState.option_3),
        #     rx.chakra.select(
        #         options,
        #         is_multi=True,
        #         on_change=MultiSelectState.set_option_3,
        #         placeholder="Select an example.",
        #         variant="outline",
        #         ),
        # ),
        # rx.chakra.vstack(
        #     rx.chakra.heading(MultiSelectState.option_4),
        #     rx.chakra.select(
        #         options,
        #         is_multi=True,
        #         on_change=MultiSelectState.set_option_4,
        #         placeholder="Select an example.",
        #         variant="outline",
        #         ),
        # ),
        rx.box(
            "A way to buid apps in pure Python!",
            text_align = "left",
        ),
    )
