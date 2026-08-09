# 🧠 CortexDS

🚀 Autonomous Multi-Agent Data Science Intelligence System

CortexDS = The Intelligent Brain for Data Science

CortexDS is an autonomous multi-agent Data Science platform designed to transform raw datasets into complete, explainable machine learning solutions.

Instead of requiring the user to manually perform every stage of a Data Science workflow, CortexDS coordinates specialized agents that analyze the dataset, understand the learning problem, prepare the data, evaluate suitable machine learning models, select the strongest model, optimize it, and generate actionable insights.

## 🚀 Project Overview

Traditional machine learning projects often require a sequence of manual steps:

Data Loading → Data Quality → Cleaning → EDA → Feature Engineering → Model Selection → Evaluation → Optimization → Insights

CortexDS automates this workflow through an agent-based architecture.

The user uploads a dataset, selects the target column, and CortexDS executes the Data Science pipeline.

Core Workflow

                ┌─────────────────────┐
                │    Dataset Upload   │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │   Dataset Agent     │
                │ Data Understanding  │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Data Quality Agent  │
                │ Quality Assessment  │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │  Cleaning Agent     │
                │ Preprocessing       │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │     EDA Agent       │
                │ Exploratory Analysis│
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │  Feature Agent      │
                │ Feature Engineering │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │    Model Agent      │
                │ Model Evaluation    │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │  Debate Agent       │
                │ Model Comparison    │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Hyperparameter Agent│
                │ Model Optimization  │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Business Agent      │
                │ Intelligent Insights │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │    Final Result     │
                │ Best Model + Report │
                └─────────────────────┘

## ✨ Key Features

🤖 Autonomous Multi-Agent Workflow

CortexDS divides the Data Science workflow into specialized agents. Each agent has a specific responsibility and passes its results to the next stage.

📂 Dataset Support

The platform supports common tabular datasets:

CSV

XLSX

XLS

The application is designed to support datasets up to 200 MB per file.

🔍 Automatic Problem Understanding

CortexDS determines whether the machine learning task is:

Classification

Regression

Based on the target variable and dataset characteristics.

🧹 Data Quality Analysis

The Data Quality Agent checks for:

Missing values

Duplicate records

Constant columns

Low-variance features

High-cardinality columns

Outliers

Potential target leakage

Datetime columns

It also produces an overall data-quality assessment and recommendations.

🧼 Automated Data Cleaning

The Cleaning Agent prepares the dataset for machine learning by handling data-quality issues and preparing the data for downstream modeling.

📊 Exploratory Data Analysis

The EDA stage analyzes the structure and statistical characteristics of the dataset and produces an exploratory report.

🧬 Feature Engineering

The Feature Agent prepares model-ready features and handles numerical/categorical transformations required by the selected modeling workflow.

🤖 Automated Model Selection

For classification, CortexDS evaluates models such as:

["Logistic Regression","Random Forest Classifier","Gradient Boosting Classifier","XGBoost Classifier"]

For regression:

["Linear Regression","Random Forest Regressor","Gradient Boosting Regressor","XGBoost Regressor"]

The candidate models are evaluated and compared using appropriate performance metrics.

## 🏆 Best Model Selection

CortexDS selects the strongest candidate based on the model evaluation results.

The system provides a "Why This Is the Best Model" explanation that describes:

Model performance

Comparison with other candidates

Evaluation score

Optimization results

Practical interpretation of the selected model

## ⚙️ Hyperparameter Optimization

The Hyperparameter Agent optimizes the selected model using automated parameter search.

For example, Random Forest optimization can consider parameters such as:

n_estimators

max_depth

min_samples_split

The optimized model is evaluated again to determine its final performance.

## 💡 Business Intelligence

The Business Intelligence Agent converts model metrics into understandable insights.

For classification it can work with:

Accuracy

Precision

Recall

F1 Score

For regression:

R² Score

MAE

MSE

RMSE

The objective is to make the model result easier to understand from a practical decision-making perspective.

🧠 Memory

CortexDS includes a memory stage for storing information from completed experiments so the system can maintain knowledge about previous pipeline executions.

🔗 LangGraph Orchestration

The agents are coordinated through a graph-based workflow using LangGraph, allowing the pipeline stages to communicate through a shared state.

Folder names may vary depending on the final project version.

## 🛠️ Technology Stack

Programming Language

Python

Frontend / UI

Streamlit

Agent Orchestration

LangGraph

Data Processing

Pandas

NumPy

Machine Learning

Scikit-learn

XGBoost

Hyperparameter Optimization

Optuna

Visualization / Analysis

Matplotlib

Plotly

AI / LLM Integration

Hugging Face inference/API integration where configured

📦 Installation

Clone the repository

git clone https://github.com/kanthulasanjay/CortexDS

Create a virtual environment

Windows

python -m venv .venv.venv\Scripts\activate

macOS / Linux

python3 -m venv .venvsource .venv/bin/activate

Install dependencies

pip install -r requirements.txt

🔐 Environment Variables

If your configuration uses Hugging Face or another external AI provider, create a .env file according to your local configuration.

Example:

HF_TOKEN=your_huggingface_token

Never commit API keys or tokens to GitHub.

Add .env to .gitignore:

.env.venv/pycache/*.pyc

▶️ Run CortexDS

Start the Streamlit application:

streamlit run app.py

🧪 Example Workflow

A typical execution looks like:

Upload Dataset↓

Select Target Column↓

Dataset Analysis↓

Data Quality Assessment↓

Data Cleaning↓

Exploratory Data Analysis↓

Feature Engineering↓

Problem Type Detection↓

Candidate Model Evaluation↓

Model Comparison↓

Best Model Selection↓

Hyperparameter Optimization↓

Model Explanation↓

Business Insights↓

Final Recommendation

📊 Example: Regression

For a housing dataset:

Dataset:California Housing Dataset

Target:median_house_value

CortexDS can identify the task as:

Problem Type: Regression

Candidate models:

Linear RegressionRandom Forest RegressorGradient Boosting RegressorXGBoost Regressor

Example output:

Best Model:Random Forest Regressor

R² Score:0.8313

The final result also includes optimization information and business-oriented interpretation.

💳 Example: Classification

For a credit-card default dataset:

Dataset:Credit Card Defaulter Prediction

Target:default

CortexDS identifies:

Problem Type:

Classification

It then evaluates classification candidates and selects the strongest model according to the evaluation results.

📈 Evaluation Metrics

Classification

Metric

Purpose

Accuracy

Overall prediction correctness

Precision

Correct positive predictions

Recall

Ability to identify actual positives

F1 Score

Balance between precision and recall

Regression

Metric

Purpose

R²

Explained variance

MAE

Average absolute prediction error

MSE

Squared prediction error

RMSE

Error in the target's scale

🧠 Why CortexDS?

CortexDS is designed to move beyond a simple prediction application.

A traditional ML application often looks like:

Dataset → Train Model → Predict

CortexDS aims to provide:

Dataset↓Understand↓Assess Quality↓Clean↓Explore↓Engineer Features↓Understand Problem↓Evaluate Multiple Models↓Compare Models↓Optimize↓Select Best Model↓Explain Result↓Generate Business Insights

This makes the project suitable as a demonstration of:

Agentic AI

Multi-agent systems

Data Science automation

Machine learning automation

Model selection

MLOps-oriented thinking

Explainable AI workflows

Business intelligence

## 🎯 Project Objectives

The major objectives of CortexDS are:

Automate repetitive Data Science tasks.

Reduce manual model-selection effort.

Provide a structured end-to-end ML workflow.

Compare multiple machine learning algorithms.

Automatically identify the strongest candidate.

Optimize the selected model.

Convert technical metrics into understandable insights.

Provide a unified interface for the complete workflow.

Demonstrate how multiple AI/ML agents can collaborate on a shared task.

## 🚀 Future Enhancements

Possible future improvements include:

Automated model deployment

REST API generation

Docker support

MLflow experiment tracking

Automated model monitoring

Drift detection

Feature importance visualization

SHAP-based explanations

Time-series forecasting agents

NLP-specific agents

Computer Vision agents

Automated report generation

Model registry

Cloud deployment

Multi-dataset comparison

Natural-language Data Science assistant

Human-in-the-loop model approval

📌 Current Project Status

🟢 Dataset Upload              Ready🟢 Data Quality                Ready🟢 Data Cleaning               Ready🟢 EDA                         Ready🟢 Feature Engineering         Ready🟢 Problem Detection           Ready🟢 Model Selection             Ready🟢 Model Comparison            Ready🟢 Hyperparameter Optimization Ready🟢 Business Insights           Ready🟢 Memory                      Ready

👨‍💻 Author

Sanjay

B.Tech — Computer Science(Data Science)

Interested in:

Data Science

Machine Learning

Artificial Intelligence

Generative AI

Agentic AI

Python

Analytics
