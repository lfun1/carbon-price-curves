"""Welcome to Reflex!."""

from carbon_price_curves import styles

# Import all the pages.
from carbon_price_curves.pages import *

import reflex as rx


class State(rx.State):
    """Define empty state to allow access to rx.State.router."""


# Create the app.
app = rx.App(style=styles.base_style)
