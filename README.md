# 🐭 Innervation Analysis Dashboard

A comprehensive web-based tool for analyzing nociceptor innervation patterns. This application offers a complete workflow: parsing raw data files, normalizing data via Left/Right ratios, performing statistical tests, and generating two types of publication-quality figures (Summary Ratios and Raw Data).

🔗 **[Live Demo](https://shellygil.github.io/innervation_analyzer/)**

## 🎯 Key Features

### 1. Dual Visualization Modes
* **📊 Ratio Comparison (Summary):** Calculates the $Ratio = \frac{\text{Left (Injured)}}{\text{Right (Control)}}$ for every mouse, averages them per group, and runs an **Unpaired T-Test**. Best for seeing the overall effect size.
* **📈 Individual Paws (Raw Data):** A "Long Graph" that displays the raw innervation index for **every single paw** side-by-side. Best for quality control and spotting outliers.

### 2. Smart Automation
* **Auto-Labeling:** The app reads your filenames (e.g., `223L_data.txt`) and automatically extracts the Mouse ID (`223L`) to label the X-axis.
* **Significance Testing:** Automatically calculates P-values and draws scientific "bracket" lines with stars (*, **, ***) if results are significant ($p < 0.05$).

### 3. Publication-Ready Customization
* **Appearance Control:** Adjust font sizes individually for the Main Title, Axis Labels, Tick Numbers, and the Legend.
* **Dynamic Legend:** Automatically adds a color-coded legend (Red=CFA, Blue=Carrageenan, Grey=Control).
* **Export:** Download high-resolution PNGs directly from the dashboard.

## 📂 Input Data & Naming Convention

The app accepts **.txt files** where the last number on each line is the measurement.

**💡 Pro Tip for Automatic Labeling:**
To get the best axis labels in the "Raw Data" graph, name your files starting with the Mouse ID followed by an underscore or dot.
* **Good:** `235L_innervation.txt` → Label on Graph: **235L**
* **Good:** `Mouse4_Right.txt` → Label on Graph: **Mouse4 (R)**

## 🚀 How to Use

1.  **Open the App:** Navigate to the website URL.
2.  **Upload Data:**
    * **CFA Group:** Upload Left (Injected) and Right (Control) files.
    * **Carrageenan Group:** Upload Left (Injected) and Right (Control) files.
    * *Note: Ensure files are uploaded in matching order (1st Left pairs with 1st Right).*
3.  **Choose Graph Mode:**
    * Select **"Ratio Comparison"** for the summary statistics.
    * Select **"Individual Paws"** to see the raw data distribution.
4.  **Customize:**
    * Edit the Graph Title and Y-Axis Label.
    * Use the **Appearance** row to tweak font sizes until it looks perfect.
5.  **Generate & Download:** Click **GENERATE GRAPH** to view, then click **⬇ PNG** to save the figure.

## 🛠️ Technologies Used

* **[PyScript](https://pyscript.net/):** Python runtime in the browser.
* **Pandas & NumPy:** Data handling and math.
* **Matplotlib:** Scientific plotting.
* **SciPy:** Statistical analysis (T-Tests).

## 📦 Local Development

To run this locally:
1.  Clone the repository.
2.  Start a local server (browsers block local file access for security):
    ```bash
    python -m http.server
    ```
3.  Open `http://localhost:8000` in your browser.

---

## 📝 Development History (Prompt Summary)

This tool was built through an iterative collaboration with Gemini. Below is the summary of the development stages:

1.  **Initial Logic:** Started with Python scripts to parse text files and calculate means/SEMs for innervation indexes.
2.  **Web Conversion:** Ported the logic to **PyScript** to create a shareable, zero-install web tool hosted on GitHub Pages.
3.  **UI Evolution:** Moved from a vertical layout to a "Dashboard" style with a sidebar for inputs and a main stage for results.
4.  **Ratio Analysis Pivot:** Shifted the analytical focus from raw means to **Left/Right Ratios** to normalize baseline variability between mice.
5.  **Publication Polish:**
    * Added automatic **Significance Brackets** that physically draw on the plot.
    * Added a **Raw Data Mode** to visualize every mouse side-by-side.
    * Implemented **Smart Filename Parsing** so graph labels match the uploaded filenames.
    * Added granular **Font Size Controls** to ensure the figures meet specific publication standards.
