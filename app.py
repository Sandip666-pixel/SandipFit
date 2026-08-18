import streamlit as st
import numpy as np
from PIL import Image
import mediapipe as mp
import os
import math

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI FITNESS PRO",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# MEDIAPIPE SETUP
# ============================================================

MODEL_PATH = "pose_landmarker.task"

if not os.path.exists(MODEL_PATH):
    st.error("❌ `pose_landmarker.task` file not found!")

    st.info(
        "Project folder-এ terminal খুলে এই command চালাও:\n\n"
        "curl -L -o pose_landmarker.task "
        "https://storage.googleapis.com/mediapipe-models/"
        "pose_landmarker/pose_landmarker_heavy/float16/1/"
        "pose_landmarker_heavy.task"
    )

    st.stop()


BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode


options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=VisionRunningMode.IMAGE,
    num_poses=1,
    min_pose_detection_confidence=0.5,
    min_pose_presence_confidence=0.5,
    min_tracking_confidence=0.5
)


pose_landmarker = PoseLandmarker.create_from_options(options)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background: linear-gradient(
            135deg,
            #0f172a 0%,
            #111827 50%,
            #1e293b 100%
        );
        color: #f8fafc;
    }

    .main-title {
        text-align: center;
        font-size: 48px;
        font-weight: 900;
        background: linear-gradient(
            90deg,
            #ff2a5f,
            #00d2ff,
            #00e676
        );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 2px;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #cbd5e1;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 27px;
        font-weight: 800;
        color: #00d2ff;
        margin-top: 25px;
        margin-bottom: 15px;
        border-left: 5px solid #ff2a5f;
        padding-left: 12px;
    }

    .info-card {
        padding: 20px;
        border-radius: 18px;
        margin-bottom: 15px;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.12);
    }

    .blue-card {
        border: 2px solid #00d2ff;
        background: rgba(0,210,255,0.08);
        box-shadow: 0 8px 30px rgba(0,210,255,0.15);
    }

    .green-card {
        border: 2px solid #00e676;
        background: rgba(0,230,118,0.08);
        box-shadow: 0 8px 30px rgba(0,230,118,0.15);
    }

    .pink-card {
        border: 2px solid #ff2a5f;
        background: rgba(255,42,95,0.08);
        box-shadow: 0 8px 30px rgba(255,42,95,0.15);
    }

    .result-box {
        background: rgba(15,23,42,0.95);
        padding: 25px;
        border-radius: 20px;
        border: 2px solid #ff2a5f;
        box-shadow: 0 10px 40px rgba(255,42,95,0.20);
        margin-top: 20px;
    }

    .priority-high {
        color: #ff4d6d;
        font-weight: 800;
    }

    .priority-medium {
        color: #ffd166;
        font-weight: 800;
    }

    .priority-normal {
        color: #00e676;
        font-weight: 800;
    }

    .exercise-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 16px;
        padding: 18px;
        margin-bottom: 15px;
    }

    .footer {
        text-align: center;
        color: #94a3b8;
        margin-top: 60px;
        padding: 25px;
        font-weight: 600;
    }

    .stButton > button {
        background: linear-gradient(
            90deg,
            #ff2a5f,
            #ff6200
        ) !important;

        color: white !important;
        font-size: 20px !important;
        font-weight: 800 !important;
        border-radius: 15px !important;
        padding: 14px 25px !important;
        border: none !important;
        box-shadow: 0 5px 20px rgba(255,42,95,0.35) !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# EXERCISE DATABASE
# ============================================================
#
# IMPORTANT:
# Later you can replace:
#
# "gif": None
#
# with your own GIF/animation URL.
#
# Example:
#
# "gif": "https://yourwebsite.com/gifs/pushup.gif"
#
# ============================================================

EXERCISE_DATABASE = [

    # --------------------------------------------------------
    # CHEST
    # --------------------------------------------------------

    {
        "name": "Push-ups",
        "muscle": "Chest",
        "category": "Chest",
        "level": "Beginner",
        "sets": 3,
        "reps": 10,
        "gif": None
    },

    {
        "name": "Incline Push-ups",
        "muscle": "Upper Chest",
        "category": "Chest",
        "level": "Beginner",
        "sets": 3,
        "reps": 12,
        "gif": None
    },

    {
        "name": "Dumbbell Bench Press",
        "muscle": "Chest",
        "category": "Chest",
        "level": "Intermediate",
        "sets": 3,
        "reps": 10,
        "gif": None
    },

    {
        "name": "Dumbbell Fly",
        "muscle": "Chest",
        "category": "Chest",
        "level": "Intermediate",
        "sets": 3,
        "reps": 12,
        "gif": None
    },


    # --------------------------------------------------------
    # SHOULDERS
    # --------------------------------------------------------

    {
        "name": "Dumbbell Lateral Raise",
        "muscle": "Side Deltoid",
        "category": "Shoulders",
        "level": "Beginner",
        "sets": 3,
        "reps": 12,
        "gif": None
    },

    {
        "name": "Dumbbell Shoulder Press",
        "muscle": "Deltoids",
        "category": "Shoulders",
        "level": "Beginner",
        "sets": 3,
        "reps": 10,
        "gif": None
    },

    {
        "name": "Front Raise",
        "muscle": "Front Deltoid",
        "category": "Shoulders",
        "level": "Beginner",
        "sets": 3,
        "reps": 12,
        "gif": None
    },

    {
        "name": "Arnold Press",
        "muscle": "Deltoids",
        "category": "Shoulders",
        "level": "Intermediate",
        "sets": 3,
        "reps": 10,
        "gif": None
    },


    # --------------------------------------------------------
    # BACK
    # --------------------------------------------------------

    {
        "name": "Pull-ups",
        "muscle": "Latissimus Dorsi",
        "category": "Back",
        "level": "Intermediate",
        "sets": 3,
        "reps": 6,
        "gif": None
    },

    {
        "name": "Assisted Pull-ups",
        "muscle": "Latissimus Dorsi",
        "category": "Back",
        "level": "Beginner",
        "sets": 3,
        "reps": 8,
        "gif": None
    },

    {
        "name": "Dumbbell Row",
        "muscle": "Upper Back",
        "category": "Back",
        "level": "Beginner",
        "sets": 3,
        "reps": 10,
        "gif": None
    },

    {
        "name": "Lat Pulldown",
        "muscle": "Latissimus Dorsi",
        "category": "Back",
        "level": "Beginner",
        "sets": 3,
        "reps": 10,
        "gif": None
    },

    {
        "name": "Seated Cable Row",
        "muscle": "Middle Back",
        "category": "Back",
        "level": "Intermediate",
        "sets": 3,
        "reps": 10,
        "gif": None
    },


    # --------------------------------------------------------
    # BICEPS
    # --------------------------------------------------------

    {
        "name": "Dumbbell Bicep Curl",
        "muscle": "Biceps",
        "category": "Biceps",
        "level": "Beginner",
        "sets": 3,
        "reps": 12,
        "gif": None
    },

    {
        "name": "Hammer Curl",
        "muscle": "Biceps / Brachialis",
        "category": "Biceps",
        "level": "Beginner",
        "sets": 3,
        "reps": 12,
        "gif": None
    },

    {
        "name": "Concentration Curl",
        "muscle": "Biceps",
        "category": "Biceps",
        "level": "Intermediate",
        "sets": 3,
        "reps": 10,
        "gif": None
    },


    # --------------------------------------------------------
    # TRICEPS
    # --------------------------------------------------------

    {
        "name": "Bench Dips",
        "muscle": "Triceps",
        "category": "Triceps",
        "level": "Beginner",
        "sets": 3,
        "reps": 10,
        "gif": None
    },

    {
        "name": "Tricep Extension",
        "muscle": "Triceps",
        "category": "Triceps",
        "level": "Beginner",
        "sets": 3,
        "reps": 12,
        "gif": None
    },

    {
        "name": "Tricep Pushdown",
        "muscle": "Triceps",
        "category": "Triceps",
        "level": "Beginner",
        "sets": 3,
        "reps": 12,
        "gif": None
    },


    # --------------------------------------------------------
    # LEGS
    # --------------------------------------------------------

    {
        "name": "Bodyweight Squat",
        "muscle": "Quadriceps / Glutes",
        "category": "Legs",
        "level": "Beginner",
        "sets": 3,
        "reps": 15,
        "gif": None
    },

    {
        "name": "Reverse Lunges",
        "muscle": "Quadriceps / Glutes",
        "category": "Legs",
        "level": "Beginner",
        "sets": 3,
        "reps": 10,
        "gif": None
    },

    {
        "name": "Bulgarian Split Squat",
        "muscle": "Quads / Glutes",
        "category": "Legs",
        "level": "Intermediate",
        "sets": 3,
        "reps": 8,
        "gif": None
    },

    {
        "name": "Romanian Deadlift",
        "muscle": "Hamstrings / Glutes",
        "category": "Legs",
        "level": "Intermediate",
        "sets": 3,
        "reps": 10,
        "gif": None
    },

    {
        "name": "Glute Bridge",
        "muscle": "Glutes",
        "category": "Legs",
        "level": "Beginner",
        "sets": 3,
        "reps": 15,
        "gif": None
    },

    {
        "name": "Calf Raises",
        "muscle": "Calves",
        "category": "Legs",
        "level": "Beginner",
        "sets": 3,
        "reps": 15,
        "gif": None
    },


    # --------------------------------------------------------
    # CORE
    # --------------------------------------------------------

    {
        "name": "Plank",
        "muscle": "Core",
        "category": "Core",
        "level": "Beginner",
        "sets": 3,
        "reps": "30 sec",
        "gif": None
    },

    {
        "name": "Crunches",
        "muscle": "Abdominals",
        "category": "Core",
        "level": "Beginner",
        "sets": 3,
        "reps": 15,
        "gif": None
    },

    {
        "name": "Leg Raises",
        "muscle": "Lower Abs",
        "category": "Core",
        "level": "Beginner",
        "sets": 3,
        "reps": 10,
        "gif": None
    },

    {
        "name": "Mountain Climbers",
        "muscle": "Core / Conditioning",
        "category": "Core",
        "level": "Beginner",
        "sets": 3,
        "reps": 20,
        "gif": None
    },

    {
        "name": "Russian Twists",
        "muscle": "Obliques",
        "category": "Core",
        "level": "Intermediate",
        "sets": 3,
        "reps": 12,
        "gif": None
    }
]


# ============================================================
# BMI
# ============================================================

def calculate_bmi(weight_kg, height_cm):

    height_m = height_cm / 100

    if height_m <= 0:
        return 0, "Unknown"

    bmi = weight_kg / (height_m ** 2)

    if bmi < 18.5:
        category = "Underweight"

    elif bmi < 25:
        category = "Normal Weight"

    elif bmi < 30:
        category = "Overweight"

    else:
        category = "Obese"

    return round(bmi, 2), category


# ============================================================
# WATER
# ============================================================

def calculate_water_intake(weight_kg):

    liters = (weight_kg * 35) / 1000

    glasses = round(liters * 4)

    return round(liters, 2), glasses


# ============================================================
# BODY RATIO ANALYSIS
# ============================================================

def calculate_body_ratio(landmarks):

    left_shoulder = landmarks[11]
    right_shoulder = landmarks[12]

    left_hip = landmarks[23]
    right_hip = landmarks[24]

    shoulder_width = abs(
        left_shoulder.x - right_shoulder.x
    )

    hip_width = abs(
        left_hip.x - right_hip.x
    )

    if hip_width <= 0:
        ratio = 1.0
    else:
        ratio = shoulder_width / hip_width

    return (
        shoulder_width,
        hip_width,
        round(ratio, 2)
    )


# ============================================================
# BODY PRIORITY ENGINE
# ============================================================

def calculate_body_priorities(shoulder_width, hip_width, ratio):

    priorities = {
        "Shoulders": 1,
        "Back": 1,
        "Chest": 1,
        "Biceps": 1,
        "Triceps": 1,
        "Legs": 1,
        "Core": 1
    }

    reasons = []

    # --------------------------------------------------------
    # CASE 1: Relatively narrow shoulders
    # --------------------------------------------------------

    if ratio < 1.05:

        priorities["Shoulders"] = 3
        priorities["Back"] = 3
        priorities["Chest"] = 2

        reasons.append(
            "Shoulder-to-hip ratio is relatively low, "
            "so shoulder and back development receive higher priority."
        )

    elif ratio < 1.15:

        priorities["Shoulders"] = 2
        priorities["Back"] = 2

        reasons.append(
            "Upper-body width can receive moderate priority."
        )

    # --------------------------------------------------------
    # CASE 2: Wider shoulder structure
    # --------------------------------------------------------

    elif ratio >= 1.30:

        priorities["Shoulders"] = 1
        priorities["Back"] = 1
        priorities["Legs"] = 2

        reasons.append(
            "Upper-body width is already relatively prominent, "
            "so lower-body training receives additional priority "
            "for overall physique balance."
        )

    # --------------------------------------------------------
    # CASE 3: Balanced
    # --------------------------------------------------------

    else:

        priorities["Shoulders"] = 1
        priorities["Back"] = 1
        priorities["Chest"] = 1
        priorities["Legs"] = 1

        reasons.append(
            "The detected shoulder-to-hip proportion appears "
            "relatively balanced."
        )

    # --------------------------------------------------------
    # Always maintain core
    # --------------------------------------------------------

    priorities["Core"] = max(
        priorities["Core"],
        1
    )

    return priorities, reasons


# ============================================================
# PRIORITY LABEL
# ============================================================

def priority_label(score):

    if score >= 3:
        return "HIGH"

    elif score == 2:
        return "MEDIUM"

    return "NORMAL"


# ============================================================
# EXERCISE SELECTION ENGINE
# ============================================================

def generate_personalized_workout(priorities, fitness_level):

    selected = []

    category_limits = {
        "HIGH": 3,
        "MEDIUM": 2,
        "NORMAL": 1
    }

    categories = [
        "Shoulders",
        "Back",
        "Chest",
        "Legs",
        "Biceps",
        "Triceps",
        "Core"
    ]

    for category in categories:

        score = priorities.get(category, 1)

        label = priority_label(score)

        limit = category_limits[label]

        matching = [
            ex for ex in EXERCISE_DATABASE
            if ex["category"] == category
            and (
                fitness_level == "All Levels"
                or ex["level"] == fitness_level
                or (
                    fitness_level == "Intermediate"
                    and ex["level"] == "Beginner"
                )
            )
        ]

        if not matching:
            continue

        # High priority categories get more exercises.
        selected.extend(matching[:limit])

    return selected


# ============================================================
# DIET RECOMMENDATIONS
# ============================================================

def generate_diet(bmi_status):

    if bmi_status in ["Overweight", "Obese"]:

        return {
            "veg": (
                "Dal, paneer, tofu, soybeans, vegetables, "
                "oats and controlled portions of rice/roti."
            ),

            "nonveg": (
                "Chicken, fish, eggs, lean protein sources, "
                "vegetables and controlled portions of rice/roti."
            ),

            "eggetarian": (
                "Eggs, paneer, dal, oats, vegetables "
                "and other protein-rich foods."
            ),

            "avoid": (
                "Excessive sugary drinks, deep-fried foods, "
                "highly processed snacks and excessive calories."
            )
        }

    else:

        return {
            "veg": (
                "Paneer, tofu, dal, soybeans, nuts, "
                "whole grains and vegetables."
            ),

            "nonveg": (
                "Chicken, fish, eggs, lean meat, "
                "whole grains and vegetables."
            ),

            "eggetarian": (
                "Eggs, paneer, dal, oats, nuts "
                "and dairy products."
            ),

            "avoid": (
                "Excessive junk food, sugary drinks "
                "and highly processed snacks."
            )
        }


# ============================================================
# EXERCISE DISPLAY
# ============================================================

def display_exercise(exercise, priority):

    col1, col2 = st.columns([2, 1])

    with col1:

        st.markdown(
            f"""
            <div class="exercise-card">

            <h3>💪 {exercise["name"]}</h3>

            <p>
            <b>Target:</b>
            {exercise["muscle"]}
            </p>

            <p>
            <b>Level:</b>
            {exercise["level"]}
            </p>

            <p>
            <b>Priority:</b>
            {priority}
            </p>

            <p>
            <b>Recommended:</b>
            {exercise["sets"]} sets × {exercise["reps"]}
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        if exercise.get("gif"):

            try:
                st.image(
                    exercise["gif"],
                    caption=exercise["name"],
                    use_container_width=True
                )

            except Exception:

                st.info(
                    "GIF could not be loaded."
                )

        else:

            st.markdown(
                """
                <div class="info-card">
                🎞️ <b>Exercise Animation</b>

                <br><br>

                GIF not added yet.

                <br><br>

                Add the GIF URL in
                <code>EXERCISE_DATABASE</code>.
                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# HEADER
# ============================================================

header_left, header_center, header_right = st.columns(
    [1, 3, 1]
)

with header_left:

    if os.path.exists("image/male_charector.png"):

        st.image(
            "image/male_charector.png",
            width=160
        )


with header_center:

    st.markdown(
        '<div class="main-title">🔥 AI FITNESS PRO 🔥</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'AI Body Ratio • Personalized Workout • MediaPipe'
        '</div>',
        unsafe_allow_html=True
    )


with header_right:

    if os.path.exists("image/female_charector.png"):

        st.image(
            "image/female_charector.png",
            width=160
        )


st.divider()


# ============================================================
# SIDEBAR SETTINGS
# ============================================================

with st.sidebar:

    st.header("⚙️ Fitness Settings")

    fitness_level = st.selectbox(
        "Fitness Level",
        [
            "Beginner",
            "Intermediate",
            "All Levels"
        ]
    )

    st.divider()

    st.markdown(
        """
        ### 🧠 How AI Works

        **1.** Detect body landmarks

        **2.** Calculate body proportions

        **3.** Find training priorities

        **4.** Select relevant exercises

        **5.** Show personalized workout

        **6.** Attach GIF/animation
        """
    )


# ============================================================
# PERSONAL INFORMATION
# ============================================================

st.markdown(
    '<div class="section-title">'
    '👤 Personal Information'
    '</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:

    age = st.number_input(
        "Age",
        min_value=10,
        max_value=100,
        value=22
    )

    gender = st.selectbox(
        "Gender",
        ["Male", "Female"]
    )


with col2:

    height = st.number_input(
        "Height (cm)",
        min_value=100.0,
        max_value=250.0,
        value=170.0,
        step=0.5
    )

    weight = st.number_input(
        "Weight (kg)",
        min_value=20.0,
        max_value=250.0,
        value=70.0,
        step=0.5
    )


bmi_value, bmi_status = calculate_bmi(
    weight,
    height
)

water_liters, water_glasses = calculate_water_intake(
    weight
)


metric1, metric2 = st.columns(2)

with metric1:

    st.markdown(
        f"""
        <div class="info-card blue-card">

        <h3>🔵 BMI</h3>

        <h2>
        {bmi_value}
        </h2>

        <p>
        {bmi_status}
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


with metric2:

    st.markdown(
        f"""
        <div class="info-card green-card">

        <h3>🟢 Daily Water Goal</h3>

        <h2>
        {water_liters} L
        </h2>

        <p>
        Approximately {water_glasses} glasses
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


st.divider()


# ============================================================
# PHOTO UPLOAD
# ============================================================

st.markdown(
    '<div class="section-title">'
    '📸 Body Photos'
    '</div>',
    unsafe_allow_html=True
)

st.write(
    "For better body-proportion analysis, upload clear "
    "full-body front and side photos."
)


col1, col2 = st.columns(2)

with col1:

    st.subheader("🧍 Front View")

    front_photo = st.file_uploader(
        "Upload Front Photo",
        type=["jpg", "jpeg", "png"],
        key="front_photo"
    )


with col2:

    st.subheader("↔️ Side View")

    side_photo = st.file_uploader(
        "Upload Side Photo",
        type=["jpg", "jpeg", "png"],
        key="side_photo"
    )


st.divider()


# ============================================================
# ANALYZE BUTTON
# ============================================================

st.markdown(
    '<div class="section-title">'
    '🔍 AI Body Analysis'
    '</div>',
    unsafe_allow_html=True
)


analyze = st.button(
    "🚀 ANALYZE BODY & CREATE PERSONALIZED WORKOUT",
    use_container_width=True
)


# ============================================================
# ANALYSIS
# ============================================================

if analyze:

    if front_photo is None:

        st.error(
            "⚠️ Please upload a Front View photo."
        )

        st.stop()


    with st.spinner(
        "⚡ MediaPipe AI is analyzing body landmarks..."
    ):

        # ----------------------------------------------------
        # LOAD FRONT IMAGE
        # ----------------------------------------------------

        img = Image.open(
            front_photo
        ).convert("RGB")

        img_array = np.array(img)

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=img_array
        )


        # ----------------------------------------------------
        # DETECT FRONT POSE
        # ----------------------------------------------------

        detection_result = pose_landmarker.detect(
            mp_image
        )


    # ========================================================
    # RESULT CONTAINER
    # ========================================================

    st.markdown(
        '<div class="result-box">',
        unsafe_allow_html=True
    )

    st.markdown(
        "<h2>📊 AI Body Geometry Report</h2>",
        unsafe_allow_html=True
    )


    # ========================================================
    # LANDMARK CHECK
    # ========================================================

    if (
        detection_result.pose_landmarks
        and
        len(detection_result.pose_landmarks) > 0
    ):

        landmarks = detection_result.pose_landmarks[0]


        # ----------------------------------------------------
        # BODY RATIO
        # ----------------------------------------------------

        shoulder_width, hip_width, ratio = (
            calculate_body_ratio(landmarks)
        )


        # ----------------------------------------------------
        # PRIORITIES
        # ----------------------------------------------------

        priorities, reasons = (
            calculate_body_priorities(
                shoulder_width,
                hip_width,
                ratio
            )
        )


        # ====================================================
        # BODY RATIO METRICS
        # ====================================================

        c1, c2, c3 = st.columns(3)

        with c1:

            st.metric(
                "Shoulder Width",
                round(shoulder_width, 4)
            )

        with c2:

            st.metric(
                "Hip Width",
                round(hip_width, 4)
            )

        with c3:

            st.metric(
                "Shoulder / Hip",
                ratio
            )


        # ====================================================
        # RATIO INTERPRETATION
        # ====================================================

        if ratio < 1.05:

            ratio_message = (
                "Upper-body width is relatively narrow "
                "compared with the detected hip width."
            )

        elif ratio < 1.15:

            ratio_message = (
                "Upper and lower body proportions appear "
                "moderately balanced."
            )

        elif ratio < 1.30:

            ratio_message = (
                "Upper body appears wider than the hips."
            )

        else:

            ratio_message = (
                "Upper-body width is substantially wider "
                "than the detected hip width."
            )


        st.info(
            f"🧠 **AI Interpretation:** {ratio_message}"
        )


        # ====================================================
        # TRAINING PRIORITY
        # ====================================================

        st.markdown(
            "### 🎯 Personalized Training Priorities"
        )


        priority_cols = st.columns(4)

        category_order = [
            "Shoulders",
            "Back",
            "Chest",
            "Legs",
            "Biceps",
            "Triceps",
            "Core"
        ]


        for index, category in enumerate(category_order):

            score = priorities[category]

            label = priority_label(score)

            with priority_cols[index % 4]:

                if label == "HIGH":

                    st.error(
                        f"🔴 {category}\n\n"
                        f"**{label}**"
                    )

                elif label == "MEDIUM":

                    st.warning(
                        f"🟡 {category}\n\n"
                        f"**{label}**"
                    )

                else:

                    st.success(
                        f"🟢 {category}\n\n"
                        f"**{label}**"
                    )


        # ====================================================
        # WHY THIS PLAN?
        # ====================================================

        st.markdown(
            "### 🧠 Why AI Selected These Priorities"
        )

        for reason in reasons:

            st.write(
                f"• {reason}"
            )


        # ====================================================
        # IMPORTANT DISCLAIMER
        # ====================================================

        st.caption(
            "⚠️ Body-ratio analysis is an approximate visual "
            "fitness heuristic. It does not measure bone "
            "structure, body fat, or medical health."
        )


        # ====================================================
        # PERSONALIZED WORKOUT
        # ====================================================

        st.divider()

        st.markdown(
            "## 🏋️ Personalized Workout Plan"
        )

        workout = generate_personalized_workout(
            priorities,
            fitness_level
        )


        if not workout:

            st.warning(
                "No suitable exercises found for this level."
            )

        else:

            # ------------------------------------------------
            # GROUP BY CATEGORY
            # ------------------------------------------------

            grouped = {}

            for exercise in workout:

                category = exercise["category"]

                if category not in grouped:

                    grouped[category] = []

                grouped[category].append(
                    exercise
                )


            # ------------------------------------------------
            # DISPLAY
            # ------------------------------------------------

            for category in category_order:

                if category not in grouped:

                    continue


                score = priorities[category]

                label = priority_label(score)


                if label == "HIGH":

                    icon = "🔴"

                elif label == "MEDIUM":

                    icon = "🟡"

                else:

                    icon = "🟢"


                st.markdown(
                    f"### {icon} {category} — {label} Priority"
                )


                for exercise in grouped[category]:

                    display_exercise(
                        exercise,
                        label
                    )


        # ====================================================
        # FRONT PHOTO PREVIEW
        # ====================================================

        st.divider()

        st.markdown(
            "### 📸 Analyzed Front Photo"
        )

        st.image(
            img,
            use_container_width=True
        )


        # ====================================================
        # SIDE PHOTO
        # ====================================================

        if side_photo is not None:

            st.divider()

            st.markdown(
                "### ↔️ Side Photo Uploaded"
            )

            side_img = Image.open(
                side_photo
            ).convert("RGB")

            st.image(
                side_img,
                use_container_width=True
            )

            st.info(
                "Side-view image is currently stored for "
                "future posture and body-depth analysis. "
                "A separate side-view geometry model can "
                "be added later."
            )

        else:

            st.info(
                "💡 Uploading a side photo in future versions "
                "can improve posture, torso-depth and body-shape "
                "analysis."
            )


        # ====================================================
        # NUTRITION
        # ====================================================

        st.divider()

        st.markdown(
            "## 🥗 Personalized Nutrition Suggestions"
        )

        diet = generate_diet(
            bmi_status
        )


        tab1, tab2, tab3 = st.tabs(
            [
                "🥦 Vegetarian",
                "🍗 Non-Vegetarian",
                "🥚 Eggetarian"
            ]
        )


        with tab1:

            st.write(
                diet["veg"]
            )


        with tab2:

            st.write(
                diet["nonveg"]
            )


        with tab3:

            st.write(
                diet["eggetarian"]
            )


        st.warning(
            f"🚫 Foods to limit: {diet['avoid']}"
        )


    else:

        st.warning(
            "⚠️ MediaPipe could not detect a clear "
            "full-body pose."
        )

        st.write(
            "Try a clear full-body photo with the entire "
            "head, shoulders, hips and legs visible."
        )


    # ========================================================
    # CLOSE RESULT BOX
    # ========================================================

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">

    ⚡ AI FITNESS PRO
    <br>
    Powered by MediaPipe + Computer Vision + Personalized
    Exercise Recommendation Engine

    </div>
    """,
    unsafe_allow_html=True
)