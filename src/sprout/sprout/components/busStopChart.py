import reflex as rx

def busStopChart(title: str, data, max: int, numOfEntries: int, leftMargin) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading(title, size="4"),
            rx.recharts.bar_chart(
                rx.recharts.bar(
                    data_key="load",
                    fill=rx.color("accent", 8),
                ),
                rx.recharts.x_axis(type_="number", domain=[0, max]),
                rx.recharts.y_axis(data_key="name", type_="category"),
                data=data,
                width="100%",
                height=50*numOfEntries,
                layout="vertical",
                margin={
                    "top": 0,
                    "right": 0,
                    "left": leftMargin*7,
                    "bottom": 0,
                },
            ),
            rx.text("Naplnenosť vozidla"),
            align_items="center",
        ),
        size="3",
        width="100%",
    ),