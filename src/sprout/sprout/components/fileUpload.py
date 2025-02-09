import reflex as rx

def fileUpload(uploadId: str, text: str, buttonText: str) -> rx.Component:
    return rx.upload(
            rx.vstack(
                rx.text(text),
                rx.button(buttonText),
                rx.cond(
                    rx.selected_files(uploadId),
                    rx.text(rx.selected_files(uploadId)),
                    rx.text("\u00A0"),
                ),
                align_items="center",
            ),
            id=uploadId,
            accept=".txt",
            max_files=1,
            padding="2em",
            multiple=False,
            width="100%",
            height="100%",
        )