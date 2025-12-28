# 🐭 Innervation Ratio Analyzer

A web-based tool for analyzing and visualizing nociceptor innervation patterns in mouse footpads. This application calculates the ratio of innervation between injured (Left) and control (Right) paws, compares experimental groups (CFA vs. Carrageenan), and generates publication-quality figures with statistical analysis.

🔗 [Live Demo](https://shellygil.github.io/innervation_analyzer/)
## 🎯 Features

* **Browser-Based:** Runs entirely in your web browser using PyScript (no Python installation required).
* **Ratio Analysis:** Automatically calculates the  $Ratio = \frac{\text{Left Index (Injected)}}{\text{Right Index (Control)}}$  for each animal to normalize baseline variability.
* **Batch Processing:** Upload multiple raw text files at once for CFA and Carrageenan groups.
* **Statistical Analysis:** Performs an **Unpaired T-Test** between groups and reports the P-value.
* **Scientific Visualization:**
    * Generates Bar Charts with overlaid individual data points (scatter).
    * Includes Standard Error of Mean (SEM) error bars.
    * Automatically draws **Significance Brackets** with stars (*, **, ***) if $p < 0.05$.
    * "GraphPad Prism" style aesthetics (Floating axes, clean background).
* **Customization:** Edit graph titles and axis labels directly from the dashboard.

## 🚀 How to Use
1. **Open the App:** Navigate to the website URL.
2. **Load CFA Data:**
  * Upload all Left Paw text files for the CFA group. Click + Add Left.
  * Upload all Right Paw text files for the CFA group. Click + Add Right.
  * Note: Ensure the order of files matches (the 1st Left file belongs to the same mouse as the 1st Right file).
3. **Load Carrageenan Data:**
  * Repeat the process for the Carrageenan Left and Right groups.
4. **Generate:** Click the CALCULATE RATIOS button.
5. **Analyze:**
  * View the generated graph on the right.
  * Check the "Statistics" box below the graph for the T-Test results.
  * Right-click the graph to save the image.


## 🛠️ Technologies Used

* HTML5 / CSS3: For the responsive Dashboard layout.
* PyScript: To run Python code inside the browser.
* Pandas: Data manipulation.
* SciPy: Statistical testing (T-Test).
* Matplotlib: Figure generation.

## 📦 Local Development

If you want to run this locally without GitHub Pages:
1. Clone this repository.
2. You cannot open index.html directly (due to browser security policies regarding local file access).
3. Use a simple local server:

```
python -m http.server
```
4. Open http://localhost:8000 in your browser.

## 📝 Development History (Prompt Summary)
This application was developed through an iterative process using a Large Language Model (Gemini). Below is a summary of the prompts and logic used to build it:
1. **Initial Concept:** The user asked for help presenting footpad nociceptor innervation results (Control vs. CFA vs. Carrageenan) based on max intensity TIF files.
2. **Data Processing:** We moved from image processing concepts to data analysis. The user provided an Excel file structure, and we wrote Python scripts to calculate averages and standard errors (SEM).
3. **Statistical Integration:** The user requested statistical significance calculations. We implemented One-Way ANOVA and Tukey's HSD post-hoc tests.
4. **GUI Creation:** The user requested a desktop GUI so they wouldn't have to edit code. We built a Tkinter app that accepted text files as inputs.
5. **Web Conversion:** To make it shareable and accessible, we ported the logic to Streamlit, and finally to PyScript (HTML/JS) to allow it to run as a static website on GitHub Pages.
6. **Design Refinement:** We iterated on the design multiple times:
   * Moving from a vertical layout to a "Dashboard" layout (Sidebar inputs, Right-side graph).
   * Fixing "Silent Crashes" by improving how JavaScript buttons trigger Python functions.
   * Implementing a specific color palette (Light Blue & Grey).
7. **Logic Pivot (Ratio Analysis):** The user changed the analytical approach from comparing raw indexes to comparing Left/Right Ratios. The code was rewritten to pair Left/Right files, calculate individual ratios, and perform an Unpaired T-Test.
8. **Final Polish:** Added automatic "Significance Brackets" that draw physically on the graph if $p < 0.05$, ensuring the figure is publication-ready.
   
## 📂 Input Data Format

The app accepts **.txt files**. It is designed to be robust and can handle various outputs from image analysis software (like FIJI/ImageJ).

* **File Structure:** The app looks for the **last number** on every line of the text file.
* **Recommendation:** Use one text file per paw, or one text file containing measurements for one specific side of one mouse.

**Example content of a `.txt` file:**
```text
MAX_Image_01.tif    5.43
MAX_Image_02.tif    4.22
MAX_Image_03.tif    6.10

