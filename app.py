from pathlib import Path

import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Visual Similarity Study",
    page_icon="📊",
    layout="wide",
)

# Reduce this value if the question page is too tall for the screen.
IMAGE_HEIGHT_PX = 185

# Reuse the diagram generated for the previous study.
EXAMPLE_DIAGRAM_PATH = "images/example/wasserstein_example.png"

st.markdown(
    f"""
    <style>
        #MainMenu, header, footer {{
            visibility: hidden;
        }}

        .block-container {{
            max-width: 900px;
            padding-top: 0.4rem;
            padding-bottom: 0.4rem;
        }}

        h1 {{
            font-size: 1.8rem;
            margin-top: 0.2rem;
            margin-bottom: 0.5rem;
        }}

        h2 {{
            font-size: 1.35rem;
            margin-top: 0.2rem;
            margin-bottom: 0.5rem;
        }}

        h3 {{
            font-size: 1.05rem;
            margin-top: 0.5rem;
            margin-bottom: 0.2rem;
        }}

        p {{
            margin-bottom: 0.35rem;
        }}

        /*
        Quiz images keep a consistent displayed height.
        */
        .quiz-image [data-testid="stImage"] {{
            margin-bottom: -0.35rem;
        }}

        .quiz-image [data-testid="stImage"] img {{
            height: {IMAGE_HEIGHT_PX}px !important;
            width: 100% !important;
            object-fit: contain !important;
            border: 2px solid transparent;
            border-radius: 8px;
            transition: border-color 0.15s ease;
        }}

        .quiz-image [data-testid="stImage"] img:hover {{
            border-color: #1f77b4;
            cursor: pointer;
        }}

        /*
        The instructional example preserves its own natural size.
        */
        .example-diagram [data-testid="stImage"] {{
            margin-bottom: 0.3rem;
        }}

        .example-diagram [data-testid="stImage"] img {{
            height: auto !important;
            max-height: none !important;
            width: 100% !important;
            object-fit: contain !important;
            border: none !important;
            border-radius: 0 !important;
            cursor: default !important;
        }}

        div[data-testid="stButton"] > button {{
            min-height: 42px;
            margin-top: 0.15rem;
            margin-bottom: 0.15rem;
        }}

        [data-testid="stProgress"] {{
            margin-top: 0;
            margin-bottom: 0.1rem;
        }}

        .diagram-placeholder {{
            border: 2px dashed #8c8c8c;
            border-radius: 10px;
            padding: 3rem 1rem;
            margin: 1rem 0;
            text-align: center;
            color: #555555;
            background-color: #f7f7f7;
        }}

        .slide-note {{
            border-left: 4px solid #1f77b4;
            border-radius: 4px;
            padding: 0.7rem 0.9rem;
            margin-top: 0.8rem;
            background-color: #f0f6fc;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)


QUESTION_TEXT = "Which option appears more similar to the given distribution?"

NUM_QUESTIONS = 20

QUESTIONS = [
    {
        "target_image": f"images/Q{i}/t.png",
        "option_a_image": f"images/Q{i}/a.png",
        "option_b_image": f"images/Q{i}/b.png",
    }
    for i in range(1, NUM_QUESTIONS + 1)
]


def initialize_state():
    if "screen" not in st.session_state:
        st.session_state.screen = "study"

    if "question_index" not in st.session_state:
        st.session_state.question_index = 0

    if "answers" not in st.session_state:
        st.session_state.answers = []

    if "selected_option" not in st.session_state:
        st.session_state.selected_option = None

    if "quiz_finished" not in st.session_state:
        st.session_state.quiz_finished = False


def go_to_instructions():
    st.session_state.screen = "instructions"


def start_quiz():
    st.session_state.screen = "quiz"


def go_back_to_study():
    st.session_state.screen = "study"


def choose_option(option):
    """
    Store only the participant's selected option.
    No correctness, score, or distance data are calculated or shown.
    """
    if st.session_state.selected_option is not None:
        return

    question_index = st.session_state.question_index

    st.session_state.selected_option = option

    st.session_state.answers.append(
        {
            "question": question_index + 1,
            "selected_option": option,
        }
    )


def next_question():
    st.session_state.question_index += 1
    st.session_state.selected_option = None

    if st.session_state.question_index >= len(QUESTIONS):
        st.session_state.quiz_finished = True


def finish_study():
    st.session_state.quiz_finished = True


def restart_study():
    st.session_state.screen = "study"
    st.session_state.question_index = 0
    st.session_state.answers = []
    st.session_state.selected_option = None
    st.session_state.quiz_finished = False


def show_image(image_path):
    """Show a fixed-height image for a quiz question."""
    if Path(image_path).exists():
        with st.container():
            st.markdown(
                '<div class="quiz-image">',
                unsafe_allow_html=True,
            )

            st.image(
                image_path,
                width="stretch",
            )

            st.markdown(
                "</div>",
                unsafe_allow_html=True,
            )
    else:
        st.error(f"Image not found: `{image_path}`")


def show_example_image(image_path):
    """Show the reusable introductory example diagram."""
    if Path(image_path).exists():
        with st.container():
            st.markdown(
                '<div class="example-diagram">',
                unsafe_allow_html=True,
            )

            st.image(
                image_path,
                width="stretch",
            )

            st.markdown(
                "</div>",
                unsafe_allow_html=True,
            )
    else:
        st.error(f"Example diagram not found: `{image_path}`")


def show_question_label(question_number):
    st.markdown(
        f"""
        <div style="
            height: {IMAGE_HEIGHT_PX}px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.25rem;
            font-weight: 700;
        ">
            Q{question_number}
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_option_button(option, question_index):
    return st.button(
        option,
        key=f"choose_{option.lower()}_{question_index}",
        width="stretch",
        disabled=st.session_state.selected_option is not None,
    )


def show_study_slide():
    st.title("Visual Similarity of Distributions")

    st.write(
        """
        This study investigates how people visually compare data
        distributions shown as scatter plots.
        """
    )

    st.write(
        """
        In many situations, people perceive distributions as similar when
        they have comparable overall visual patterns.
        """
    )

    st.subheader("Visual similarity")

    st.write(
        """
        When comparing distributions, people often look at how the points
        are positioned and how the overall pattern appears.
        """
    )

    left_column, right_column = st.columns(2)

    with left_column:
        st.info(
            """
            **Distributions may appear similar when they have:**

            - Comparable location
            - Similar shape or pattern
            - Similar spread or concentration
            """
        )

    with right_column:
        st.warning(
            """
            **Distributions may appear different when they have:**

            - Clearly different locations
            - Different spread or overall range
            - Different clusters or isolated points
            """
        )

    st.subheader("Example")

    if Path(EXAMPLE_DIAGRAM_PATH).exists():
        show_example_image(EXAMPLE_DIAGRAM_PATH)

        st.markdown(
            """
            <div class="slide-note">
                Most people would likely consider <strong>Option A</strong>
                and <strong>Reference Q</strong> more similar because both
                have compact point patterns in a similar location.
                <strong>Option B</strong> is wider and positioned differently,
                so it may appear less similar to the reference distribution Q.
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:
        st.markdown(
            """
            <div class="diagram-placeholder">
                <strong>Diagram placeholder</strong><br><br>
                Add the reusable example diagram here:<br>
                <code>images/example/wasserstein_example.png</code>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="slide-note">
            There is no single visual rule that you must follow.
            Please use your own visual impression when deciding which
            option looks more similar to the reference distribution.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.button(
        "Next",
        type="primary",
        width="stretch",
        on_click=go_to_instructions,
    )


def show_instructions_slide():
    st.title("Instructions")

    st.write(f"The study contains **{NUM_QUESTIONS} questions**.")

    st.write(
        """
        Each question contains three scatter plots arranged vertically:
        """
    )

    st.markdown(
        """
        ```text
        [A]  Option A distribution

        [Q]  Reference distribution

        [B]  Option B distribution
        ```
        """
    )

    st.subheader("Your task")

    st.write(
        """
        For each question, choose the option, **A** or **B**, that appears
        more similar to the reference distribution **Q**.
        """
    )

    st.subheader("What you may consider")

    st.markdown(
        """
        - Overall position or location
        - Shape and orientation
        - Spread or concentration
        - Clusters or separated groups
        - Outliers
        """
    )

    st.subheader("After selecting an answer")

    st.markdown(
        """
        1. Select either A or B.
        2. The Next Question button will become available.
        3. Click Next Question to continue.
        """
    )

    st.markdown(
        """
        <div class="slide-note">
            Please choose the option that appears more similar to Q
            according to your own visual impression.
        </div>
        """,
        unsafe_allow_html=True,
    )

    back_column, start_column = st.columns(2)

    with back_column:
        st.button(
            "Back",
            width="stretch",
            on_click=go_back_to_study,
        )

    with start_column:
        st.button(
            "Start Study",
            type="primary",
            width="stretch",
            on_click=start_quiz,
        )


def show_quiz():
    index = st.session_state.question_index
    question = QUESTIONS[index]

    st.progress((index + 1) / len(QUESTIONS))
    st.subheader(f"Question {index + 1} of {len(QUESTIONS)}")
    st.write(QUESTION_TEXT)

    # Row 1: Option A
    option_a_button, option_a_image = st.columns(
        [1, 8],
        vertical_alignment="center",
    )

    with option_a_button:
        option_a_selected = show_option_button("A", index)

    with option_a_image:
        show_image(question["option_a_image"])

    if option_a_selected:
        choose_option("A")
        st.rerun()

    # Row 2: Reference distribution Q
    target_label, target_image = st.columns(
        [1, 8],
        vertical_alignment="center",
    )

    with target_label:
        show_question_label(index + 1)

    with target_image:
        show_image(question["target_image"])

    # Row 3: Option B
    option_b_button, option_b_image = st.columns(
        [1, 8],
        vertical_alignment="center",
    )

    with option_b_button:
        option_b_selected = show_option_button("B", index)

    with option_b_image:
        show_image(question["option_b_image"])

    if option_b_selected:
        choose_option("B")
        st.rerun()

    # No correctness or distance feedback is shown in this study.
    is_last_question = index == len(QUESTIONS) - 1
    next_button_text = "Finish Study" if is_last_question else "Next Question"

    if st.button(
        next_button_text,
        type="primary",
        width="stretch",
        disabled=st.session_state.selected_option is None,
    ):
        if is_last_question:
            finish_study()
        else:
            next_question()

        st.rerun()


def show_results():
    st.header("Study Complete")

    st.write(
        """
        Thank you for completing the study.
        """
    )

    results_rows = [
        {
            "Question": f"Q{answer['question']}",
            "Your Answer": f"Option {answer['selected_option']}",
        }
        for answer in st.session_state.answers
    ]

    results_df = pd.DataFrame(results_rows)

    st.subheader("Your Responses")

    st.dataframe(
        results_df,
        width="stretch",
        hide_index=True,
        column_config={
            "Question": st.column_config.TextColumn(
                "Question",
                width="medium",
            ),
            "Your Answer": st.column_config.TextColumn(
                "Your Answer",
                width="medium",
            ),
        },
    )

    csv_data = results_df.to_csv(
        index=False,
    ).encode("utf-8")

    st.download_button(
        label="Download Results",
        data=csv_data,
        file_name="visual_similarity_results.csv",
        mime="text/csv",
        type="primary",
        width="stretch",
    )

    st.button(
        "Restart Study",
        width="stretch",
        on_click=restart_study,
    )
initialize_state()

if st.session_state.screen == "study":
    show_study_slide()

elif st.session_state.screen == "instructions":
    show_instructions_slide()

elif st.session_state.quiz_finished:
    show_results()

else:
    show_quiz()