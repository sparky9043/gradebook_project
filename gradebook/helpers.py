from bokeh.plotting import figure
from bokeh.embed import components
from math import pi
import pandas as pd
from bokeh.palettes import Category10
from bokeh.transform import cumsum


def get_pie_graph(user_data: dict):
    data = (
        pd.Series(user_data)
        .reset_index(name="value")
        .rename(columns={"index": "grades"})
    )
    data["angle"] = data["value"] / data["value"].sum() * 2 * pi
    data["color"] = Category10[len(user_data)]

    p = figure(
        height=400,
        title="Student Grades",
        toolbar_location=None,
        tools="hover",
        tooltips="@grades: @value",
        x_range=(-0.5, 1.0),
    )

    p.wedge(
        x=0,
        y=1,
        radius=0.4,
        start_angle=cumsum("angle", include_zero=True),
        end_angle=cumsum("angle"),
        line_color="white",
        fill_color="color",
        legend_field="grades",
        source=data,
    )

    p.axis.axis_label = None
    p.axis.visible = False
    p.grid.grid_line_color = None

    return components(p)


def get_bar_graph(user_data: list[tuple]):
    x_data = [data[0] for data in user_data]
    y_data = [data[1] for data in user_data]

    p = figure(
        x_range=x_data,
        height=350,
        title="",
        toolbar_location=None,
        tools="",
    )

    p.vbar(x=x_data, top=y_data, width=0.9)

    p.xgrid.grid_line_color = None
    p.y_range.start = 0

    return components(p)


def convert_number_to_letter(number: int) -> str:
    if 0 <= number < 1:
        return "F"
    elif number < 2:
        return "D"
    elif number < 3:
        return "C"
    elif number < 4:
        return "B"
    elif number == 4:
        return "A"
    else:
        raise ValueError("Grade points must be between 0 to 4")


def convert_letter_to_number(letter: str) -> int:
    if letter == "A":
        return 4
    elif letter == "B":
        return 3
    elif letter == "C":
        return 2
    elif letter == "D":
        return 1
    elif letter == "F":
        return 0
    else:
        raise ValueError("Grades should only be A,B,C,D or F")


def calculate_gpa(grades: dict[str, int]):

    total_points = 0
    total_count = 0
    for letter_grade, count in grades.items():
        number_grade = convert_letter_to_number(letter_grade)
        total_points += number_grade * count
        total_count += count
    if total_count != 0:
        return total_points / total_count
    else:
        return 0
