import base64
import html
import json
import logging
import tempfile
import traceback
from pathlib import Path

import pandas as pd
import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="CortexDS — Autonomous Multi-Agent Data Science Intelligence System",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

ASSET_DIRS = [
    BASE_DIR / "assets",
    BASE_DIR / "static",
    BASE_DIR / "images",
]

BACKGROUND_NAMES = [
    "background.png",
    "background.jpg",
    "background.jpeg",
    "bg.png",
    "bg.jpg",
    "dashboard_background.png",
]

LOGO_NAMES = [
    "logo.png",
    "cortexds_logo.png",
    "CortexDS.png",
    "cortexds.png",
]


# ============================================================
# HELPERS
# ============================================================

def find_asset(names):
    for folder in ASSET_DIRS:
        for name in names:
            path = folder / name
            if path.is_file():
                return path

    for name in names:
        path = BASE_DIR / name
        if path.is_file():
            return path

    return None


def file_to_data_uri(path):
    if not path or not path.is_file():
        return ""

    suffix = path.suffix.lower()

    mime = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
        ".gif": "image/gif",
    }.get(suffix, "image/png")

    try:
        encoded = base64.b64encode(path.read_bytes()).decode("utf-8")
        return f"data:{mime};base64,{encoded}"
    except Exception:
        return ""


def safe(value):
    return html.escape(str(value))


def render_html(markup):
    """
    IMPORTANT:
    All custom HTML/CSS goes through st.html().
    Do NOT use st.markdown() for HTML in this application.
    This prevents HTML/CSS source from appearing as visible text.
    """
    if hasattr(st, "html"):
        st.html(markup)
    else:
        # Compatibility fallback for older Streamlit.
        st.markdown(markup, unsafe_allow_html=True)


def load_dataset(path):
    suffix = Path(path).suffix.lower()

    if suffix == ".csv":
        # utf-8-sig handles CSV files containing a BOM.
        return pd.read_csv(path, encoding="utf-8-sig")

    if suffix == ".xlsx":
        return pd.read_excel(path, engine="openpyxl")

    if suffix == ".xls":
        return pd.read_excel(path)

    raise ValueError(
        f"Unsupported file format: {suffix}. "
        "Supported formats are CSV, XLSX and XLS."
    )


def numeric_metric(result, keys, default=0.0):
    for key in keys:
        value = result.get(key)

        if value is not None:
            try:
                return float(value)
            except (TypeError, ValueError):
                pass

    return default


def get_problem_type(result):
    return str(
        result.get("problem_type")
        or result.get("problem")
        or ""
    ).strip().lower()


def get_best_model(result):
    name = result.get("model_name")

    if name:
        return str(name)

    name = result.get("best_model_name")

    if name:
        return str(name)

    manager = result.get("manager_decision")

    if isinstance(manager, dict):
        name = (
            manager.get("model_name")
            or manager.get("best_model")
            or manager.get("selected_model")
        )

        if name:
            return str(name)

    return "Not selected"


def get_primary_score(result, problem_type):
    metrics = result.get("metrics")

    if not isinstance(metrics, dict):
        metrics = {}

    if problem_type == "classification":
        return numeric_metric(
            metrics,
            [
                "accuracy",
                "Accuracy",
                "optimized_score",
                "score",
            ],
        )

    if problem_type == "regression":
        return numeric_metric(
            metrics,
            [
                "r2_score",
                "R²",
                "r2",
                "optimized_score",
                "score",
            ],
        )

    return numeric_metric(
        result,
        [
            "optimized_score",
            "score",
        ],
    )


def get_leaderboard(result):
    board = result.get("leaderboard", [])

    if isinstance(board, list):
        return board

    return []


# ============================================================
# ASSETS
# ============================================================

BACKGROUND_PATH = find_asset(BACKGROUND_NAMES)
LOGO_PATH = find_asset(LOGO_NAMES)

BACKGROUND_URI = file_to_data_uri(BACKGROUND_PATH)
LOGO_URI = file_to_data_uri(LOGO_PATH)


# ============================================================
# PIPELINE SERVICE
# ============================================================

PipelineService = None
PIPELINE_IMPORT_ERROR = None

try:
    from services.pipeline_service import PipelineService
except Exception as exc:
    PIPELINE_IMPORT_ERROR = str(exc)


# ============================================================
# SESSION STATE
# ============================================================

if "pipeline_result" not in st.session_state:
    st.session_state.pipeline_result = None

if "uploaded_path" not in st.session_state:
    st.session_state.uploaded_path = None

if "uploaded_name" not in st.session_state:
    st.session_state.uploaded_name = None

if "preview_df" not in st.session_state:
    st.session_state.preview_df = None


# ============================================================
# GLOBAL STYLE
# ============================================================

background_rule = ""

if BACKGROUND_URI:
    background_rule = f"""
        background-image:
            linear-gradient(
                rgba(2, 5, 35, 0.38),
                rgba(2, 5, 35, 0.56)
            ),
            url("{BACKGROUND_URI}");
        background-size: cover;
        background-position: center center;
        background-attachment: fixed;
    """
else:
    background_rule = """
        background:
            radial-gradient(
                circle at 85% 10%,
                rgba(34, 103, 255, 0.35),
                transparent 34%
            ),
            radial-gradient(
                circle at 10% 85%,
                rgba(128, 44, 255, 0.32),
                transparent 35%
            ),
            linear-gradient(
                135deg,
                #02052d 0%,
                #07114c 50%,
                #03072f 100%
            );
    """


render_html(
    f"""
    <style>
        /* =====================================================
           MAIN BACKGROUND
        ===================================================== */

        html, body {{
            background: #02052d !important;
        }}

        [data-testid="stAppViewContainer"] {{
            {background_rule}
            min-height: 100vh;
        }}

        [data-testid="stHeader"] {{
            background: transparent !important;
        }}

        [data-testid="stToolbar"] {{
            background: transparent !important;
        }}

        [data-testid="stSidebar"] {{
            background:
                linear-gradient(
                    180deg,
                    rgba(3, 7, 43, 0.97),
                    rgba(4, 8, 45, 0.94)
                ) !important;
            border-right: 1px solid rgba(86, 128, 255, 0.35);
        }}

        [data-testid="stSidebarContent"] {{
            padding-top: 18px;
        }}

        #MainMenu {{
            visibility: hidden;
        }}

        footer {{
            visibility: hidden;
        }}

        /* =====================================================
           GLOBAL TEXT
        ===================================================== */

        [data-testid="stAppViewContainer"] * {{
            font-family:
                Inter,
                ui-sans-serif,
                system-ui,
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                sans-serif;
        }}

        h1, h2, h3, h4, h5, h6 {{
            color: #ffffff !important;
        }}

        /* =====================================================
           NATIVE STREAMLIT TEXT VISIBILITY
           (labels, markdown, alerts, code, expanders, status)
           These default to dark/near-black text in Streamlit's
           light theme, which becomes invisible on this dark
           background. Force a light, legible palette everywhere.
        ===================================================== */

        [data-testid="stAppViewContainer"] p,
        [data-testid="stAppViewContainer"] span,
        [data-testid="stAppViewContainer"] li,
        [data-testid="stAppViewContainer"] label,
        [data-testid="stMarkdownContainer"] {{
            color: #e6ecff !important;
        }}

        [data-testid="stWidgetLabel"] p,
        [data-testid="stWidgetLabel"] label {{
            color: #b9c8f7 !important;
            font-weight: 650 !important;
            font-size: 13.5px !important;
        }}

        [data-testid="stCaptionContainer"] {{
            color: #8ea3d9 !important;
        }}

        [data-testid="stAppViewContainer"] a {{
            color: #57e3ff !important;
        }}

        /* =====================================================
           FILE UPLOADER — HIGH CONTRAST
           Uploaded filename + size are BLACK.
        ===================================================== */

        [data-testid="stFileUploaderDropzone"] {{
            background: rgba(5, 16, 65, 0.82) !important;
            border: 1px dashed rgba(86, 155, 255, 0.75) !important;
            border-radius: 16px !important;
        }}

        [data-testid="stFileUploaderDropzone"] > div,
        [data-testid="stFileUploaderDropzone"] div,
        [data-testid="stFileUploaderDropzone"] span,
        [data-testid="stFileUploaderDropzone"] small {{
            opacity: 1 !important;
        }}

        [data-testid="stFileUploaderDropzone"] button {{
            background: linear-gradient(135deg, #5528ee, #087ff5) !important;
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            border: 1px solid rgba(255,255,255,0.45) !important;
            border-radius: 10px !important;
            font-weight: 800 !important;
        }}

        [data-testid="stFileUploaderFile"] {{
            background: #ffffff !important;
            border: 1px solid rgba(255,255,255,0.95) !important;
            border-radius: 12px !important;
            opacity: 1 !important;
        }}

        /* housing.csv */
        [data-testid="stFileUploaderFileName"],
        [data-testid="stFileUploaderFileName"] *,
        [data-testid="stFileUploaderFile"] [data-testid="stFileUploaderFileName"],
        [data-testid="stFileUploaderFile"] [data-testid="stFileUploaderFileName"] * {{
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
            opacity: 1 !important;
            font-weight: 700 !important;
        }}

        /* 1.1 MB */
        [data-testid="stFileUploaderFileSize"],
        [data-testid="stFileUploaderFileSize"] *,
        [data-testid="stFileUploaderFile"] [data-testid="stFileUploaderFileSize"],
        [data-testid="stFileUploaderFile"] [data-testid="stFileUploaderFileSize"] * {{
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
            opacity: 1 !important;
            font-weight: 600 !important;
        }}

        /* Streamlit version-independent fallback for file text */
        [data-testid="stFileUploaderFile"] span {{
            opacity: 1 !important;
        }}

        [data-testid="stFileUploaderFile"] svg {{
            opacity: 1 !important;
        }}

        /* Selectbox / dropdown */

        [data-baseweb="select"] * {{
            color: #ffffff !important;
        }}

        div[data-baseweb="popover"] li,
        div[data-baseweb="popover"] div {{
            color: #0c1230 !important;
        }}

        /* Alerts: info / success / warning / error */

        [data-testid="stAlert"] {{
            border-radius: 14px !important;
            border: 1px solid rgba(88, 130, 255, 0.30) !important;
        }}

        [data-testid="stAlert"] p,
        [data-testid="stAlert"] span,
        [data-testid="stAlert"] div {{
            color: #f2f5ff !important;
        }}

        [data-testid="stAlertContentInfo"] {{
            background: rgba(30, 110, 255, 0.16) !important;
        }}

        [data-testid="stAlertContentSuccess"] {{
            background: rgba(32, 231, 120, 0.14) !important;
        }}

        [data-testid="stAlertContentWarning"] {{
            background: rgba(255, 176, 32, 0.14) !important;
        }}

        [data-testid="stAlertContentError"] {{
            background: rgba(255, 70, 90, 0.16) !important;
        }}

        /* Code blocks */

        [data-testid="stAppViewContainer"] pre,
        [data-testid="stAppViewContainer"] code {{
            background: rgba(3, 9, 40, 0.85) !important;
            color: #7ef7c1 !important;
            border-radius: 10px !important;
            border: 1px solid rgba(88, 130, 255, 0.22);
        }}

        /* Expanders */

        [data-testid="stExpander"] {{
            background: rgba(7, 17, 65, 0.65) !important;
            border: 1px solid rgba(80, 123, 255, 0.28) !important;
            border-radius: 14px !important;
        }}

        [data-testid="stExpander"] summary {{
            color: #e6ecff !important;
        }}

        /* =====================================================
           PIPELINE STATUS
           Black title on a light header for maximum contrast.
        ===================================================== */

        .cds-pipeline-status {{
            margin: 18px 0 8px 0;
            border: 1px solid rgba(91, 130, 255, 0.55);
            border-radius: 16px;
            overflow: hidden;
            background: rgba(4, 12, 55, 0.84);
            box-shadow: 0 14px 40px rgba(0,0,0,0.28);
        }}

        .cds-pipeline-status-title {{
            background: #f4f6fb;
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
            font-size: 18px;
            font-weight: 850;
            padding: 15px 20px;
            border-bottom: 1px solid rgba(10,20,60,0.18);
        }}

        .cds-pipeline-status-title * {{
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
        }}

        .cds-pipeline-agent {{
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            font-size: 16px;
            font-weight: 650;
            padding: 13px 22px;
            line-height: 1.45;
        }}

        .cds-pipeline-agent strong {{
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
        }}

        .cds-pipeline-complete {{
            color: #19f28a !important;
            -webkit-text-fill-color: #19f28a !important;
            font-weight: 800;
            padding: 13px 22px 18px 22px;
        }}

        .cds-pipeline-error {{
            color: #ff5b6e !important;
            -webkit-text-fill-color: #ff5b6e !important;
            font-weight: 800;
            padding: 13px 22px 18px 22px;
        }}

        /* If Streamlit creates a native status widget elsewhere,
           keep its title readable as well. */
        [data-testid="stStatusWidget"] summary,
        [data-testid="stStatusWidget"] summary *,
        [data-testid="stStatusWidget"] p {{
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
            opacity: 1 !important;
        }}

        /* Dataframe container chrome (header row of the widget) */

        [data-testid="stDataFrame"] {{
            border: 1px solid rgba(80, 123, 255, 0.28);
        }}

        [data-testid="stElementToolbar"] {{
            background: rgba(7, 17, 65, 0.85) !important;
            border-radius: 8px;
        }}

        [data-testid="stElementToolbarButton"] svg {{
            fill: #cfdaff !important;
        }}

        /* =====================================================
           SIDEBAR
        ===================================================== */

        .cds-sidebar-logo {{
            text-align: center;
            padding: 8px 4px 20px 4px;
        }}

        .cds-sidebar-logo img {{
            width: 155px;
            max-width: 100%;
            height: auto;
            object-fit: contain;
            filter:
                drop-shadow(0 0 18px rgba(48, 226, 255, 0.30));
        }}

        .cds-sidebar-logo-fallback {{
            width: 90px;
            height: 90px;
            margin: auto;
            border-radius: 22px;
            display: flex;
            align-items: center;
            justify-content: center;
            background:
                linear-gradient(135deg, #602cff, #12dfff);
            font-size: 42px;
            box-shadow:
                0 0 30px rgba(41, 210, 255, 0.28);
        }}

        .cds-sidebar-name {{
            color: #ffffff;
            font-size: 24px;
            font-weight: 850;
            margin-top: 5px;
        }}

        .cds-sidebar-name span {{
            color: #36e5ff;
        }}

        .cds-sidebar-tag {{
            color: #8ea3d9;
            font-size: 9px;
            font-weight: 750;
            letter-spacing: 1px;
            line-height: 1.5;
        }}

        .cds-nav-title {{
            color: #8497cc;
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            margin: 25px 0 10px 4px;
        }}

        .cds-side-card {{
            padding: 12px 14px;
            margin: 7px 0;
            border-radius: 13px;
            color: #cdd7f7;
            font-weight: 650;
            font-size: 14px;
            background: rgba(14, 27, 84, 0.50);
            border: 1px solid rgba(84, 123, 255, 0.14);
            transition: all 0.18s ease;
        }}

        .cds-side-card:hover {{
            background: rgba(24, 45, 120, 0.65);
            border-color: rgba(122, 171, 255, 0.40);
            transform: translateX(3px);
            cursor: default;
        }}

        .cds-side-active {{
            color: #ffffff;
            background:
                linear-gradient(
                    90deg,
                    rgba(84, 38, 244, 0.90),
                    rgba(22, 116, 245, 0.88)
                );
            border: 1px solid rgba(122, 171, 255, 0.48);
            box-shadow:
                0 9px 26px rgba(48, 65, 245, 0.25);
        }}

        .cds-side-active:hover {{
            transform: translateX(0);
        }}

        .cds-system {{
            margin-top: 24px;
            padding: 14px;
            border-radius: 15px;
            background: rgba(7, 18, 66, 0.82);
            border: 1px solid rgba(76, 113, 255, 0.25);
        }}

        .cds-green-dot {{
            display: inline-block;
            width: 9px;
            height: 9px;
            border-radius: 50%;
            background: #20e778;
            box-shadow: 0 0 12px #20e778;
            margin-right: 8px;
            animation: cds-pulse 1.8s infinite;
        }}

        @keyframes cds-pulse {{
            0% {{ box-shadow: 0 0 0 0 rgba(32, 231, 120, 0.55); }}
            70% {{ box-shadow: 0 0 0 8px rgba(32, 231, 120, 0); }}
            100% {{ box-shadow: 0 0 0 0 rgba(32, 231, 120, 0); }}
        }}

        .cds-system-title {{
            color: #ffffff;
            font-size: 13px;
            font-weight: 750;
        }}

        .cds-system-status {{
            color: #46eb8a;
            font-size: 11px;
            margin-left: 18px;
        }}

        /* =====================================================
           HERO
        ===================================================== */

        .cds-hero {{
            padding: 34px 40px;
            margin: 6px 0 24px 0;
            border-radius: 25px;
            background:
                linear-gradient(
                    135deg,
                    rgba(4, 10, 56, 0.88),
                    rgba(7, 24, 93, 0.72)
                );
            border: 1px solid rgba(88, 130, 255, 0.40);
            box-shadow: 0 18px 60px rgba(0, 0, 0, 0.32);
            backdrop-filter: blur(7px);
            position: relative;
            overflow: hidden;
        }}

        .cds-hero::before {{
            content: "";
            position: absolute;
            top: -60%;
            right: -10%;
            width: 420px;
            height: 420px;
            background:
                radial-gradient(
                    circle,
                    rgba(70, 234, 255, 0.20),
                    transparent 70%
                );
            pointer-events: none;
        }}

        .cds-hero-title {{
            color: #ffffff;
            font-size: 42px;
            line-height: 1.15;
            font-weight: 900;
            margin-bottom: 10px;
        }}

        .cds-hero-title span {{
            background:
                linear-gradient(
                    90deg,
                    #ffffff,
                    #46eaff,
                    #9368ff
                );
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .cds-hero-subtitle {{
            color: #cddaff;
            font-size: 18px;
            font-weight: 650;
            margin-bottom: 18px;
        }}

        .cds-hero-description {{
            max-width: 950px;
            color: #eaf0ff;
            font-size: 15px;
            line-height: 1.75;
        }}

        .cds-ready {{
            display: inline-block;
            margin-top: 20px;
            padding: 9px 16px;
            border-radius: 30px;
            color: #70ffad;
            background: rgba(29, 222, 120, 0.10);
            border: 1px solid rgba(65, 239, 145, 0.34);
            font-size: 13px;
            font-weight: 800;
        }}

        /* =====================================================
           SECTION
        ===================================================== */

        .cds-section-title {{
            color: #ffffff;
            font-size: 23px;
            font-weight: 850;
            margin: 26px 0 12px 0;
            padding-left: 12px;
            border-left: 4px solid #46eaff;
        }}

        .cds-section-text {{
            color: #c7d2f5;
            font-size: 13px;
            line-height: 1.7;
        }}

        /* =====================================================
           METRIC CARDS
        ===================================================== */

        .cds-metric {{
            min-height: 118px;
            padding: 18px;
            border-radius: 18px;
            background:
                linear-gradient(
                    135deg,
                    rgba(7, 19, 73, 0.88),
                    rgba(8, 18, 64, 0.75)
                );
            border: 1px solid rgba(82, 125, 255, 0.30);
            box-shadow: 0 12px 34px rgba(0, 0, 0, 0.22);
            backdrop-filter: blur(7px);
            transition: transform 0.18s ease, box-shadow 0.18s ease;
        }}

        .cds-metric:hover {{
            transform: translateY(-3px);
            box-shadow: 0 16px 40px rgba(50, 90, 255, 0.28);
            border-color: rgba(120, 170, 255, 0.55);
        }}

        .cds-metric-label {{
            color: #a9b8e6;
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 800;
        }}

        .cds-metric-value {{
            color: #ffffff;
            font-size: 28px;
            font-weight: 900;
            margin-top: 8px;
        }}

        .cds-metric-note {{
            color: #93a4d6;
            font-size: 11px;
            margin-top: 5px;
        }}

        .cds-accent {{
            color: #42eaff !important;
        }}

        /* =====================================================
           GLASS CARDS
        ===================================================== */

        .cds-card {{
            padding: 21px;
            border-radius: 18px;
            background:
                linear-gradient(
                    135deg,
                    rgba(7, 20, 78, 0.88),
                    rgba(7, 17, 63, 0.76)
                );
            border: 1px solid rgba(80, 123, 255, 0.28);
            box-shadow: 0 12px 35px rgba(0, 0, 0, 0.23);
            backdrop-filter: blur(7px);
        }}

        .cds-card-title {{
            color: #ffffff;
            font-size: 18px;
            font-weight: 800;
            margin-bottom: 10px;
        }}

        .cds-card-text {{
            color: #d3ddfa;
            font-size: 13px;
            line-height: 1.7;
        }}

        .cds-best-model {{
            color: #49eaff;
            font-size: 28px;
            font-weight: 900;
        }}

        .cds-score {{
            color: #9db3ff;
            font-size: 14px;
            font-weight: 700;
        }}

        .cds-why {{
            padding: 22px;
            border-radius: 18px;
            background:
                linear-gradient(
                    135deg,
                    rgba(40, 29, 110, 0.70),
                    rgba(8, 35, 91, 0.78)
                );
            border: 1px solid rgba(113, 113, 255, 0.38);
            box-shadow: 0 14px 40px rgba(0, 0, 0, 0.22);
        }}

        .cds-why-title {{
            color: #ffffff;
            font-size: 17px;
            font-weight: 850;
        }}

        .cds-why-text {{
            color: #eef1ff;
            font-size: 14px;
            line-height: 1.75;
            margin-top: 12px;
        }}

        /* =====================================================
           PIPELINE
        ===================================================== */

        .cds-pipeline {{
            padding: 20px;
            border-radius: 20px;
            background: rgba(4, 14, 63, 0.76);
            border: 1px solid rgba(76, 123, 255, 0.28);
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.22);
        }}

        .cds-pipeline-grid {{
            display: grid;
            grid-template-columns: repeat(6, 1fr);
            gap: 9px;
        }}

        .cds-stage {{
            text-align: center;
            padding: 12px 5px;
            border-radius: 12px;
            transition: background 0.18s ease;
        }}

        .cds-stage:hover {{
            background: rgba(70, 234, 255, 0.08);
        }}

        .cds-stage-icon {{
            font-size: 24px;
        }}

        .cds-stage-name {{
            color: #e2e9ff;
            font-size: 11px;
            font-weight: 700;
            margin-top: 6px;
            line-height: 1.35;
        }}

        .cds-stage-ok {{
            color: #38ec82;
            font-size: 10px;
            margin-top: 4px;
        }}

        /* =====================================================
           BUTTONS / INPUTS
        ===================================================== */

        [data-testid="stFileUploader"] {{
            background: rgba(5, 16, 65, 0.72);
            border: 1px dashed rgba(76, 144, 255, 0.65);
            border-radius: 17px;
            padding: 10px;
        }}

        [data-baseweb="select"] > div {{
            background-color: rgba(7, 17, 65, 0.88) !important;
            color: #ffffff !important;
            border-color: rgba(72, 119, 255, 0.45) !important;
        }}

        [data-testid="stButton"] button {{
            border-radius: 12px;
            border: 1px solid rgba(98, 137, 255, 0.45);
            color: #ffffff;
            background:
                linear-gradient(
                    90deg,
                    #4f24e9,
                    #087af3
                );
            font-weight: 800;
            min-height: 45px;
            transition: all 0.18s ease;
        }}

        [data-testid="stButton"] button:hover {{
            border-color: #62eaff;
            box-shadow: 0 0 22px rgba(52, 185, 255, 0.35);
            transform: translateY(-1px);
        }}

        [data-testid="stButton"] button p {{
            color: #ffffff !important;
            font-weight: 800 !important;
        }}

        /* =====================================================
           DATAFRAME
        ===================================================== */

        [data-testid="stDataFrame"] {{
            border-radius: 15px;
            overflow: hidden;
        }}

        /* =====================================================
           RESPONSIVE
        ===================================================== */

        @media (max-width: 900px) {{
            .cds-hero-title {{
                font-size: 31px;
            }}

            .cds-pipeline-grid {{
                grid-template-columns: repeat(3, 1fr);
            }}
        }}
    </style>
    """
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    if LOGO_URI:
        render_html(
            f"""
            <div class="cds-sidebar-logo">
                <img src="{LOGO_URI}" alt="CortexDS Logo">
                <div class="cds-sidebar-name">
                    Cortex<span>DS</span>
                </div>
                <div class="cds-sidebar-tag">
                    AUTONOMOUS MULTI-AGENT
                    <br>
                    DATA SCIENCE INTELLIGENCE SYSTEM
                </div>
            </div>
            """
        )
    else:
        render_html(
            """
            <div class="cds-sidebar-logo">
                <div class="cds-sidebar-logo-fallback">🧠</div>
                <div class="cds-sidebar-name">
                    Cortex<span>DS</span>
                </div>
                <div class="cds-sidebar-tag">
                    AUTONOMOUS MULTI-AGENT
                    <br>
                    DATA SCIENCE INTELLIGENCE SYSTEM
                </div>
            </div>
            """
        )

    render_html(
        """
        <div class="cds-nav-title">Navigation</div>

        <div class="cds-side-card cds-side-active">
            ⚡ Pipeline
        </div>

        <div class="cds-side-card">
            📁 Dataset Analysis
        </div>

        <div class="cds-side-card">
            🔍 Data Quality
        </div>

        <div class="cds-side-card">
            🧹 Data Cleaning
        </div>

        <div class="cds-side-card">
            📊 EDA Explorer
        </div>

        <div class="cds-side-card">
            🧬 Feature Engineering
        </div>

        <div class="cds-side-card">
            🤖 Model Selection
        </div>

        <div class="cds-side-card">
            💬 Model Evaluation
        </div>

        <div class="cds-side-card">
            🏆 Best Model
        </div>

        <div class="cds-side-card">
            📈 Business Insights
        </div>

        <div class="cds-side-card">
            🧠 Memory
        </div>

        <div class="cds-system">
            <span class="cds-green-dot"></span>
            <span class="cds-system-title">System</span>
            <div class="cds-system-status">● Online</div>
        </div>
        """
    )


# ============================================================
# HERO
# ============================================================

render_html(
    """
    <div class="cds-hero">

        <div class="cds-hero-title">
            Welcome to <span>CortexDS</span> 👋
        </div>

        <div class="cds-hero-subtitle">
            Autonomous Multi-Agent Data Science Intelligence System
        </div>

        <div class="cds-hero-description">
            CortexDS transforms raw datasets into intelligent machine
            learning solutions through an autonomous multi-agent
            Data Science workflow.
            <br><br>
            The system analyzes the dataset, identifies the learning
            problem, prepares the data, performs feature engineering,
            evaluates suitable models, selects the strongest model,
            and generates explainable business insights.
        </div>

        <div class="cds-ready">
            ● System Ready — Upload a dataset to begin
        </div>

    </div>
    """
)


# ============================================================
# DATASET WORKSPACE
# ============================================================

render_html(
    """
    <div class="cds-section-title">
        📁 Dataset Workspace
    </div>

    <div class="cds-section-text">
        Upload a CSV, XLSX or XLS dataset. CortexDS will analyze the
        data and use the selected target column to execute the
        autonomous Data Science workflow.
        <br>
        <strong>Maximum file size: 200 MB.</strong>
    </div>
    """
)


uploaded_file = st.file_uploader(
    "Upload your dataset",
    type=["csv", "xlsx", "xls"],
    key="cortexds_dataset",
)


# ============================================================
# DATASET PROCESSING
# ============================================================

if uploaded_file is not None:

    suffix = Path(uploaded_file.name).suffix.lower()

    try:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as temp_file:

            temp_file.write(
                uploaded_file.getbuffer()
            )

            dataset_path = temp_file.name

        preview_df = load_dataset(dataset_path)

        st.session_state.uploaded_path = dataset_path
        st.session_state.uploaded_name = uploaded_file.name
        st.session_state.preview_df = preview_df

    except Exception as exc:

        st.error(
            "❌ CortexDS could not read this dataset."
        )

        st.exception(exc)

        preview_df = None

else:

    preview_df = st.session_state.preview_df
    dataset_path = st.session_state.uploaded_path


# ============================================================
# DATASET INFORMATION
# ============================================================

if preview_df is not None and not preview_df.empty:

    rows = len(preview_df)
    columns = len(preview_df.columns)

    numeric_count = len(
        preview_df.select_dtypes(
            include="number"
        ).columns
    )

    categorical_count = columns - numeric_count

    missing_cells = int(
        preview_df.isna().sum().sum()
    )

    total_cells = max(
        rows * columns,
        1,
    )

    missing_percent = (
        missing_cells / total_cells
    ) * 100

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        render_html(
            f"""
            <div class="cds-metric">
                <div class="cds-metric-label">Records</div>
                <div class="cds-metric-value">{rows:,}</div>
                <div class="cds-metric-note">Total Rows</div>
            </div>
            """
        )

    with c2:
        render_html(
            f"""
            <div class="cds-metric">
                <div class="cds-metric-label">Features</div>
                <div class="cds-metric-value">{columns:,}</div>
                <div class="cds-metric-note">Total Columns</div>
            </div>
            """
        )

    with c3:
        render_html(
            f"""
            <div class="cds-metric">
                <div class="cds-metric-label">Missing Values</div>
                <div class="cds-metric-value">{missing_percent:.2f}%</div>
                <div class="cds-metric-note">
                    {missing_cells:,} Missing Cells
                </div>
            </div>
            """
        )

    with c4:
        render_html(
            f"""
            <div class="cds-metric">
                <div class="cds-metric-label">Data Types</div>
                <div class="cds-metric-value cds-accent">
                    {numeric_count}/{categorical_count}
                </div>
                <div class="cds-metric-note">
                    Numerical / Categorical
                </div>
            </div>
            """
        )

    render_html(
        """
        <div class="cds-section-title">
            🎯 Target Selection
        </div>

        <div class="cds-section-text">
            Select the target column that CortexDS should predict.
            The pipeline will automatically determine whether the
            task is classification or regression.
        </div>
        """
    )

    target = st.selectbox(
        "Target column",
        options=list(preview_df.columns),
        key="cortexds_target",
    )

    render_html(
        """
        <div class="cds-section-title">
            👀 Dataset Preview
        </div>
        """
    )

    st.dataframe(
        preview_df.head(10),
        width="stretch",
        hide_index=True,
    )

    # ========================================================
    # RUN PIPELINE
    # ========================================================

    st.markdown("")

    run_pipeline = st.button(
        "🚀 Run CortexDS Autonomous Pipeline",
        width="stretch",
        type="primary",
    )

    if run_pipeline:

        if PipelineService is None:

            st.error(
                "❌ PipelineService could not be imported."
            )

            st.code(
                PIPELINE_IMPORT_ERROR
                or "Unknown import error"
            )

            st.info(
                "Expected file structure:"
            )

            st.code(
                "services/__init__.py\n"
                "services/pipeline_service.py"
            )

        else:

            # ----------------------------------------------------
            # CUSTOM PIPELINE STATUS CARD
            # ----------------------------------------------------
            # The native st.status() component can inherit a light
            # header from Streamlit's theme. We use a custom card
            # so the title is always BLACK on a light background.
            render_html(
                """
                <div class="cds-pipeline-status">
                    <div class="cds-pipeline-status-title">
                        🤖 CortexDS Autonomous Pipeline Running...
                    </div>
                </div>
                """
            )

            st.markdown(
                '<div class="cds-pipeline-agent">📥 '
                '<strong>Dataset Agent</strong> — Loading dataset</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                '<div class="cds-pipeline-agent">🔍 '
                '<strong>Data Quality Agent</strong> — Checking data quality</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                '<div class="cds-pipeline-agent">🧹 '
                '<strong>Cleaning Agent</strong> — Preparing dataset</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                '<div class="cds-pipeline-agent">📊 '
                '<strong>EDA Agent</strong> — Analyzing distributions</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                '<div class="cds-pipeline-agent">🧬 '
                '<strong>Feature Agent</strong> — Selecting useful features</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                '<div class="cds-pipeline-agent">🤖 '
                '<strong>Model Agent</strong> — Evaluating suitable models</div>',
                unsafe_allow_html=True,
            )

            try:

                result = PipelineService.execute(
                    dataset_path,
                    target,
                )

                st.session_state.pipeline_result = result

                st.markdown(
                    '<div class="cds-pipeline-agent">🏆 '
                    '<strong>Best Model Agent</strong> — Selecting strongest model</div>',
                    unsafe_allow_html=True,
                )

                st.markdown(
                    '<div class="cds-pipeline-agent">📈 '
                    '<strong>Business Agent</strong> — Generating business insights</div>',
                    unsafe_allow_html=True,
                )

                st.markdown(
                    '<div class="cds-pipeline-complete">'
                    '✅ CortexDS Autonomous Pipeline Completed'
                    '</div>',
                    unsafe_allow_html=True,
                )

            except Exception as exc:

                st.session_state.pipeline_result = None

                st.error(
                    "❌ CortexDS Pipeline Failed"
                )

                st.code(
                    f"{type(exc).__name__}: {exc}"
                )

                with st.expander(
                    "🔍 Technical Error Details"
                ):

                    st.code(
                        traceback.format_exc()
                    )


# ============================================================
# RESULTS
# ============================================================

result = st.session_state.pipeline_result

if isinstance(result, dict):

    render_html(
        """
        <div class="cds-section-title">
            🚀 AI Pipeline Results
        </div>
        """
    )

    problem_type = get_problem_type(result)
    best_model = get_best_model(result)
    score = get_primary_score(
        result,
        problem_type,
    )

    score_name = (
        "Accuracy"
        if problem_type == "classification"
        else "R² Score"
        if problem_type == "regression"
        else "Score"
    )

    # ========================================================
    # RESULT METRICS
    # ========================================================

    r1, r2, r3, r4 = st.columns(4)

    with r1:
        render_html(
            f"""
            <div class="cds-metric">
                <div class="cds-metric-label">Problem Type</div>
                <div class="cds-metric-value cds-accent">
                    {safe(problem_type.title() or "Unknown")}
                </div>
                <div class="cds-metric-note">Detected by CortexDS</div>
            </div>
            """
        )

    with r2:
        render_html(
            f"""
            <div class="cds-metric">
                <div class="cds-metric-label">Best Model</div>
                <div class="cds-metric-value cds-accent">
                    {safe(best_model)}
                </div>
                <div class="cds-metric-note">Selected Model</div>
            </div>
            """
        )

    with r3:
        render_html(
            f"""
            <div class="cds-metric">
                <div class="cds-metric-label">{safe(score_name)}</div>
                <div class="cds-metric-value">
                    {score:.4f}
                </div>
                <div class="cds-metric-note">Best Evaluated Score</div>
            </div>
            """
        )

    with r4:
        render_html(
            f"""
            <div class="cds-metric">
                <div class="cds-metric-label">Pipeline</div>
                <div class="cds-metric-value cds-accent">
                    Complete
                </div>
                <div class="cds-metric-note">
                    Autonomous Workflow
                </div>
            </div>
            """
        )

    # ========================================================
    # PIPELINE
    # ========================================================

    render_html(
        """
        <div class="cds-section-title">
            🔄 CortexDS Autonomous Workflow
        </div>

        <div class="cds-pipeline">

            <div class="cds-pipeline-grid">

                <div class="cds-stage">
                    <div class="cds-stage-icon">📥</div>
                    <div class="cds-stage-name">Dataset</div>
                    <div class="cds-stage-ok">● Complete</div>
                </div>

                <div class="cds-stage">
                    <div class="cds-stage-icon">🛡️</div>
                    <div class="cds-stage-name">Data Quality</div>
                    <div class="cds-stage-ok">● Complete</div>
                </div>

                <div class="cds-stage">
                    <div class="cds-stage-icon">🧹</div>
                    <div class="cds-stage-name">Cleaning</div>
                    <div class="cds-stage-ok">● Complete</div>
                </div>

                <div class="cds-stage">
                    <div class="cds-stage-icon">📊</div>
                    <div class="cds-stage-name">EDA</div>
                    <div class="cds-stage-ok">● Complete</div>
                </div>

                <div class="cds-stage">
                    <div class="cds-stage-icon">🧬</div>
                    <div class="cds-stage-name">Features</div>
                    <div class="cds-stage-ok">● Complete</div>
                </div>

                <div class="cds-stage">
                    <div class="cds-stage-icon">🤖</div>
                    <div class="cds-stage-name">Model</div>
                    <div class="cds-stage-ok">● Complete</div>
                </div>

            </div>

        </div>
        """
    )

    # ========================================================
    # MODEL SELECTION
    # ========================================================

    render_html(
        """
        <div class="cds-section-title">
            🏆 Best Model
        </div>
        """
    )

    render_html(
        f"""
        <div class="cds-card">

            <div class="cds-card-title">
                Selected Model
            </div>

            <div class="cds-best-model">
                {safe(best_model)}
            </div>

            <div class="cds-score">
                {safe(score_name)}: {score:.4f}
            </div>

        </div>
        """
    )

    # ========================================================
    # LEADERBOARD
    # ========================================================

    leaderboard = get_leaderboard(result)

    if leaderboard:

        render_html(
            """
            <div class="cds-section-title">
                📊 Model Performance Comparison
            </div>
            """
        )

        leaderboard_rows = []

        for item in leaderboard:

            if not isinstance(item, dict):
                continue

            name = (
                item.get("model_name")
                or item.get("name")
                or item.get("model")
                or "Unknown"
            )

            if problem_type == "classification":

                model_score = numeric_metric(
                    item,
                    [
                        "accuracy",
                        "Accuracy",
                        "score",
                    ],
                )

                metric = "Accuracy"

            else:

                model_score = numeric_metric(
                    item,
                    [
                        "r2_score",
                        "R²",
                        "r2",
                        "score",
                    ],
                )

                metric = "R² Score"

            leaderboard_rows.append(
                {
                    "Model": str(name),
                    metric: round(model_score, 4),
                }
            )

        if leaderboard_rows:

            leaderboard_df = pd.DataFrame(
                leaderboard_rows
            )

            leaderboard_df = (
                leaderboard_df
                .sort_values(
                    leaderboard_df.columns[1],
                    ascending=False,
                )
                .reset_index(drop=True)
            )

            st.dataframe(
                leaderboard_df,
                width="stretch",
                hide_index=True,
            )

    # ========================================================
    # WHY THIS IS THE BEST MODEL
    # ========================================================

    render_html(
        """
        <div class="cds-section-title">
            💡 Why This Is the Best Model
        </div>
        """
    )

    selection_reason = result.get(
        "model_selection_reason",
        "",
    )

    if not selection_reason:
        if problem_type == "classification":
            selection_reason = (
                f"{best_model} was selected because it achieved the highest "
                f"evaluated classification performance among the candidate "
                f"models. It achieved an Accuracy of {score:.4f} "
                f"({score * 100:.2f}%), making it the strongest evaluated "
                f"model for the current dataset and target."
            )
        elif problem_type == "regression":
            selection_reason = (
                f"{best_model} was selected because it achieved the strongest "
                f"evaluated regression performance among the candidate models. "
                f"It achieved an R² score of {score:.4f}, indicating that it "
                f"captures approximately {score * 100:.2f}% of the variation "
                f"in the target on the evaluation data."
            )
        else:
            selection_reason = (
                f"{best_model} was selected as the strongest model based on "
                f"the CortexDS evaluation results."
            )

    # Read model comparison information returned by the pipeline.
    comparison_lines = []
    if leaderboard:
        ranked_models = []

        for item in leaderboard:
            if not isinstance(item, dict):
                continue

            model_name = (
                item.get("model_name")
                or item.get("name")
                or item.get("model")
                or "Unknown"
            )

            if problem_type == "classification":
                model_score = numeric_metric(
                    item,
                    ["accuracy", "Accuracy", "score"],
                )
            else:
                model_score = numeric_metric(
                    item,
                    ["r2_score", "R²", "r2", "score"],
                )

            ranked_models.append(
                (str(model_name), model_score)
            )

        ranked_models.sort(
            key=lambda item: item[1],
            reverse=True,
        )

        for rank, (model_name, model_score) in enumerate(
            ranked_models[:5],
            start=1,
        ):
            comparison_lines.append(
                f"{rank}. {model_name} — {model_score:.4f}"
            )

    # Read optimized hyperparameters when the pipeline returns them.
    best_params = (
        result.get("best_params")
        or result.get("optimized_params")
        or result.get("hyperparameters")
        or {}
    )

    if not isinstance(best_params, dict):
        best_params = {}

    if not best_params:
        manager = result.get("manager_decision")

        if isinstance(manager, dict):
            candidate = (
                manager.get("best_params")
                or manager.get("optimized_params")
                or manager.get("hyperparameters")
            )

            if isinstance(candidate, dict):
                best_params = candidate

    render_html(
        f"""
        <div class="cds-why">
            <div class="cds-why-title">
                🏆 Model Selection Decision
            </div>

            <div class="cds-why-text">
                {safe(selection_reason)}
            </div>
        </div>
        """
    )

    # Detailed explanation cards
    explain_cols = st.columns(3)

    with explain_cols[0]:
        render_html(
            f"""
            <div class="cds-card">
                <div class="cds-card-title">
                    🎯 Predictive Performance
                </div>

                <div class="cds-card-text">
                    <strong>{safe(score_name)}:</strong>
                    {score:.4f}<br><br>

                    CortexDS evaluates candidate models using the same
                    evaluation workflow and compares their predictive
                    performance. The selected model is the model that
                    achieved the strongest score for the detected
                    problem type.
                </div>
            </div>
            """
        )

    with explain_cols[1]:
        if comparison_lines:
            comparison_html = "<br>".join(
                safe(line)
                for line in comparison_lines
            )
        else:
            comparison_html = (
                "The current pipeline result does not contain a model "
                "leaderboard. The selected model is therefore explained "
                "using its primary evaluation score."
            )

        render_html(
            f"""
            <div class="cds-card">
                <div class="cds-card-title">
                    📊 Candidate Comparison
                </div>

                <div class="cds-card-text">
                    {comparison_html}
                </div>
            </div>
            """
        )

    with explain_cols[2]:
        if best_params:
            params_html = "<br>".join(
                f"<strong>{safe(key)}:</strong> {safe(value)}"
                for key, value in best_params.items()
            )
        else:
            params_html = (
                "CortexDS completed model selection, but the current "
                "pipeline result did not return the optimized "
                "hyperparameters to the UI."
            )

        render_html(
            f"""
            <div class="cds-card">
                <div class="cds-card-title">
                    ⚙️ Optimization
                </div>

                <div class="cds-card-text">
                    {params_html}
                </div>
            </div>
            """
        )

    if problem_type == "regression":
        practical_explanation = (
            f"This is a regression problem, so CortexDS uses R² as the "
            f"primary comparison metric. The current R² score of "
            f"{score:.4f} means the selected model explains approximately "
            f"{score * 100:.2f}% of the variation in the target on the "
            f"evaluation data. Higher R² is preferred when the candidate "
            f"models are evaluated under the same conditions."
        )

    elif problem_type == "classification":
        practical_explanation = (
            f"This is a classification problem, so CortexDS uses Accuracy "
            f"as the primary comparison metric. {best_model} achieved "
            f"{score:.4f} ({score * 100:.2f}%), which was the strongest "
            f"evaluated result among the available candidate models."
        )

    else:
        practical_explanation = (
            f"CortexDS selected {best_model} because it produced the "
            f"strongest available evaluation score for this dataset."
        )

    render_html(
        f"""
        <div class="cds-why" style="margin-top:16px;">
            <div class="cds-why-title">
                🔎 How to Interpret the Decision
            </div>

            <div class="cds-why-text">
                {safe(practical_explanation)}
            </div>
        </div>
        """
    )

    # ========================================================
    # BUSINESS INSIGHTS
    # ========================================================

    render_html(
        """
        <div class="cds-section-title">
            📈 Business Insights
        </div>
        """
    )

    business_report = result.get(
        "business_report",
        {},
    )

    raw_insights = []

    if isinstance(business_report, dict):
        raw_insights = business_report.get(
            "insights",
            [],
        )

    if not isinstance(raw_insights, list):
        raw_insights = (
            [raw_insights]
            if raw_insights
            else []
        )

    # Display insights produced by the Business Intelligence Agent.
    if raw_insights:
        for index, insight in enumerate(
            raw_insights,
            start=1,
        ):
            render_html(
                f"""
                <div class="cds-card" style="margin-bottom:12px;">
                    <div class="cds-card-title">
                        💡 Business Insight {index}
                    </div>

                    <div class="cds-card-text">
                        {safe(insight)}
                    </div>
                </div>
                """
            )

    else:
        render_html(
            """
            <div class="cds-card">
                <div class="cds-card-title">
                    💡 Business Interpretation
                </div>

                <div class="cds-card-text">
                    The Business Intelligence Agent did not return a
                    separate insight list. The business interpretation
                    below is based on the actual model-selection result
                    returned by CortexDS.
                </div>
            </div>
            """
        )

    # Business-level interpretation based only on pipeline results.
    business_cols = st.columns(3)

    with business_cols[0]:
        render_html(
            f"""
            <div class="cds-card">
                <div class="cds-card-title">
                    🎯 Decision Support
                </div>

                <div class="cds-card-text">
                    The recommended model is
                    <strong>{safe(best_model)}</strong>.

                    Its current {safe(score_name)} is
                    <strong>{score:.4f}</strong>.

                    This gives stakeholders a measurable baseline for
                    prediction and decision-support workflows.
                </div>
            </div>
            """
        )

    with business_cols[1]:
        if problem_type == "regression":
            monitoring_text = (
                f"Because this is a regression problem, R² is the main "
                f"performance indicator shown by CortexDS. The current "
                f"baseline is {score:.4f}. Track this metric on new data "
                f"after deployment to identify performance degradation."
            )

        elif problem_type == "classification":
            monitoring_text = (
                f"Because this is a classification problem, Accuracy is "
                f"the main performance indicator shown by CortexDS. The "
                f"current baseline is {score:.4f}. Monitor performance on "
                f"new data to verify that model quality remains stable."
            )

        else:
            monitoring_text = (
                "The pipeline returned a general model score. Future "
                "production evaluations should compare new performance "
                "against this baseline."
            )

        render_html(
            f"""
            <div class="cds-card">
                <div class="cds-card-title">
                    📊 Performance Monitoring
                </div>

                <div class="cds-card-text">
                    {safe(monitoring_text)}
                </div>
            </div>
            """
        )

    with business_cols[2]:
        render_html(
            f"""
            <div class="cds-card">
                <div class="cds-card-title">
                    🚀 Recommended Next Step
                </div>

                <div class="cds-card-text">
                    Validate <strong>{safe(best_model)}</strong> on
                    new, unseen data before using its predictions for
                    important business decisions.

                    Continue monitoring prediction quality and retrain
                    the model when the underlying data distribution
                    changes significantly.
                </div>
            </div>
            """
        )


# ============================================================
# FOOTER
# ============================================================

render_html(
    """
    <div style="
        text-align:center;
        padding:40px 0 25px 0;
        color:#9db0e0;
        font-size:12px;
        line-height:1.7;
    ">
        <strong style="color:#c7d3fa;">
            CortexDS
        </strong>
        — Autonomous Multi-Agent Data Science Intelligence System
        <br>
        Dataset → Intelligence → Model → Insight
    </div>
    """
)