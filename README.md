# tutor-evaluation-data-analysis
This repository contains the analysis code and data used in the article titled "Evaluation Scores Analysis from Disciplinary Perspective." The analysis focuses on mentor evaluation scores across different academic disciplines, covering key metrics such as "average score," "Teacher-Student Relationship," "Student Prospects," "Student Allowance," "Supervisor's Professional Ability," "Supervisor's Project Attitude," and "Supervisor's Lifestyle."

## Table of Contents

- [Introduction](#introduction)
- [Data](#data)
- [Requirements](#requirements)
- [Usage](#usage)
- [Analysis Breakdown](#analysis-breakdown)
- [Figures](#figures)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This repository is developed to conduct and document the evaluation of mentors in Chinese higher education institutions. The study analyzes mentor evaluations across multiple academic disciplines and provides insights into the impact of mentorship on student satisfaction and future prospects.

## Data

The analysis uses the dataset `proceed_comments_data_en_v4.json`, which contains anonymous evaluations of mentors across various universities in China. Each record in the dataset includes information about the mentor's major, evaluation score, and other qualitative aspects.

## Requirements

The code in this repository relies on the following Python libraries:

- `pandas`: for data manipulation and analysis
- `matplotlib`: for plotting and visualizations
- `seaborn`: for enhanced visualizations
- `json`: for working with the JSON data

To install the necessary libraries, use the following command:

```bash
pip install pandas matplotlib seaborn
```

## Usage

### Running the Analysis

1. **Load the dataset**: The dataset `proceed_comments_data_en_v4.json` should be placed in the same directory as the analysis script.
   
2. **Run the script**: The script processes the data, filters out invalid major names (containing non-alphabetic characters or marked as "Unknown"), and generates bar charts for each of the seven evaluation metrics.

3. **Generated Figures**: After running the script, seven figures will be saved in the `figures/` directory, corresponding to the seven analyzed metrics.

### Example Command

```bash
python analysis_script.py
```

## Analysis Breakdown

The following metrics are analyzed in this study:

1. **Average Score**: A general measure of student satisfaction with mentors. It aggregates student evaluations across various aspects, providing an overall score that reflects how mentors are perceived by students.
   
2. **Teacher-Student Relationship**: This metric evaluates the quality of the interpersonal relationship between students and mentors. A higher score indicates a stronger, more supportive relationship, which is often critical for a positive academic experience.

3. **Student Prospects**: This metric reflects how students view their future career and academic opportunities under their mentor’s guidance. Fields with higher scores tend to provide better networking, career advice, and academic development support.

4. **Student Allowance**: This metric analyzes the financial support mentors provide to their students. Adequate financial support can positively impact students' academic success and overall satisfaction.

5. **Supervisor's Professional Ability**: This metric evaluates the mentor's competence and expertise in their field. Higher scores reflect students' trust in their mentors' ability to provide valuable academic and research guidance.

6. **Supervisor's Project Attitude**: This metric assesses how well mentors align project work with students' academic goals. High scores indicate that mentors are perceived as guiding students through relevant and beneficial research projects, while lower scores may suggest excessive focus on unrelated projects.

7. **Supervisor's Lifestyle**: This metric reflects the mentor's work-life balance and its impact on students. Mentors who maintain a balanced lifestyle tend to be more approachable and supportive, contributing to a healthier academic environment.

## Figures

The generated figures, corresponding to the seven metrics, are saved with the following filenames:

- `metric_1_average_score_colored.png`
- `metric_2_Teacher-Student_Relationship_colored.png`
- `metric_3_Student_Prospects_colored.png`
- `metric_4_Student_Allowance_colored.png`
- `metric_5_Supervisor's_Professional_Ability_colored.png`
- `metric_6_Supervisor's_Project_Attitude_colored.png`
- `metric_7_Supervisor's_Lifestyle_colored.png`

Each figure illustrates the average score for each major in the corresponding metric.

## Contributing

Contributions are welcome! Please feel free to open an issue or submit a pull request with improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
