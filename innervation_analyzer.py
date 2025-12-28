import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# --- PAGE CONFIG ---
st.set_page_config(page_title="Innervation Analysis", layout="wide")

# Set font style for publication-quality plots
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']

# --- TITLE & INTRO ---
st.title("Innervation Analysis Project")
st.markdown("""
This tool analyzes nociceptor innervation patterns under different conditions (Control, CFA, Carrageenan).
It accepts raw data (Text files) or summary datasets (CSV/Excel), performs statistical analysis (ANOVA + Tukey),
and generates publication-ready figures.
""")

# --- FUNCTIONS ---

def process_text_files(uploaded_files):
    """Parses raw text files where each line ends with a data value."""
    values = []
    if uploaded_files:
        for file in uploaded_files:
            try:
                # Decode and split by lines
                content = file.getvalue().decode("utf-8")
                lines = content.split('\n')
                for line in lines:
                    parts = line.strip().split()
                    if parts:
                        try:
                            # We assume the last column is the number
                            val = float(parts[-1])
                            values.append(val)
                        except ValueError:
                            continue
            except Exception as e:
                st.error(f"Error reading {file.name}: {e}")
    # Group by file (mouse) mean or take all values? 
    # Usually we treat each file as a biological replicate (mouse).
    # Here we take the mean of each file to represent one data point (n=1 mouse).
    # If the text file contains multiple slices for ONE mouse, we average them.
    if values: 
        # Note: This logic assumes 1 file = 1 mouse. 
        # If multiple files = 1 mouse, the user should combine them. 
        # For simplicity in this assignment, we take the mean of the file content.
        return np.mean(values) 
    return None

def process_excel_csv(uploaded_file):
    """Reads a CSV or Excel file using Pandas."""
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        return df
    except Exception as e:
        st.error(f"Error reading file: {e}")
        return None

# --- SIDEBAR: DATA INPUT ---
st.sidebar.header("Data Import")
input_method = st.sidebar.radio("Select Input Method:", ["Upload Text Files (Raw)", "Upload Excel/CSV (Summary)"])

data_groups = {"Control": [], "CFA": [], "Carrageenan": []}
data_loaded = False

if input_method == "Upload Text Files (Raw)":
    st.sidebar.info("Upload .txt files. Each file represents one mouse/sample.")
    
    # 3 File Uploaders for the 3 Groups
    files_ctrl = st.sidebar.file_uploader("Control Files", accept_multiple_files=True, type=['txt'])
    files_cfa = st.sidebar.file_uploader("CFA Files", accept_multiple_files=True, type=['txt'])
    files_carr = st.sidebar.file_uploader("Carrageenan Files", accept_multiple_files=True, type=['txt'])
    
    # Process files
    if files_ctrl and files_cfa and files_carr:
        # For text files, we iterate through the list of uploaded files
        # Each file is processed to get one single number (the mean of that mouse)
        data_groups["Control"] = [res for f in files_ctrl if (res := process_text_files([f])) is not None]
        data_groups["CFA"] = [res for f in files_cfa if (res := process_text_files([f])) is not None]
        data_groups["Carrageenan"] = [res for f in files_carr if (res := process_text_files([f])) is not None]
        
        if all(len(v) > 0 for v in data_groups.values()):
            data_loaded = True

elif input_method == "Upload Excel/CSV (Summary)":
    st.sidebar.info("Upload a file with columns: 'Control', 'CFA', 'Carrageenan'.")
    uploaded_file = st.sidebar.file_uploader("Upload File", type=['csv', 'xlsx'])
    
    if uploaded_file:
        df = process_excel_csv(uploaded_file)
        if df is not None:
            # Check for required columns
            required_cols = ["Control", "CFA", "Carrageenan"]
            # Case insensitive check
            df.columns = [c.strip() for c in df.columns] 
            
            # Simple matching (flexible)
            col_map = {}
            for req in required_cols:
                match = next((c for c in df.columns if req.lower() in c.lower()), None)
                col_map[req] = match
            
            if all(col_map.values()):
                # Extract non-null values for each group
                data_groups["Control"] = df[col_map["Control"]].dropna().tolist()
                data_groups["CFA"] = df[col_map["CFA"]].dropna().tolist()
                data_groups["Carrageenan"] = df[col_map["Carrageenan"]].dropna().tolist()
                data_loaded = True
            else:
                st.sidebar.error(f"Columns not found. Expected: {required_cols}")

# --- MAIN ANALYSIS ---

if data_loaded:
    st.success("Data successfully loaded!")
    
    # Prepare data for Statistics
    group_names = ["Control", "CFA", "Carrageenan"]
    data_arrays = [data_groups[n] for n in group_names]
    
    # Combine for Tukey
    all_values = np.concatenate(data_arrays)
    all_labels = np.concatenate([[n] * len(data_groups[n]) for n in group_names])
    
    # 1. STATISTICAL ANALYSIS (One-way ANOVA + Tukey)
    try:
        f_stat, p_anova = stats.f_oneway(*data_arrays)
        tukey = pairwise_tukeyhsd(endog=all_values, groups=all_labels, alpha=0.05)
        tukey_df = pd.DataFrame(data=tukey.summary().data[1:], columns=tukey.summary().data[0])
    except Exception as e:
        st.error("Not enough data points to run statistics (need variance).")
        st.stop()

    # Layout: Plot on Left, Stats on Right
    col_plot, col_stats = st.columns([1.5, 1])

    with col_plot:
        st.subheader("Innervation Results")
        
        # --- PLOTTING CODE (Matplotlib) ---
        fig, ax = plt.subplots(figsize=(6, 5))
        
        # Calculate Stats for Plotting
        means = [np.mean(d) for d in data_arrays]
        sems = [stats.sem(d) for d in data_arrays]
        
        # Styles
        colors = ['#E0E0E0', '#FFCDD2', '#BBDEFB'] # Grey, Red, Blue
        edges = ['#424242', '#D32F2F', '#1976D2']
        
        # Bars
        ax.bar(group_names, means, yerr=sems, capsize=0, 
               color=colors, edgecolor=edges, linewidth=2, width=0.6, alpha=0.9)
        
        # Error Bars (Custom thick lines)
        ax.errorbar(group_names, means, yerr=sems, fmt='none', ecolor='black', elinewidth=2, capsize=5)
        
        # Scatter (Individual Points)
        for i, data in enumerate(data_arrays):
            jitter = np.random.normal(0, 0.04, size=len(data))
            ax.scatter(np.full(len(data), i) + jitter, data, 
                       color='black', s=50, alpha=0.7, edgecolors='white', zorder=3)
        
        # Significance Brackets
        y_max = max(all_values)
        curr_y = y_max
        
        def get_pval(g1, g2):
            row = tukey_df[((tukey_df['group1'] == g1) & (tukey_df['group2'] == g2)) | 
                           ((tukey_df['group1'] == g2) & (tukey_df['group2'] == g1))]
            return row['p-adj'].values[0] if not row.empty else 1.0

        comparisons = [(0, 1, "Control", "CFA"), (0, 2, "Control", "Carrageenan"), (1, 2, "CFA", "Carrageenan")]
        
        for idx1, idx2, name1, name2 in comparisons:
            p_val = get_pval(name1, name2)
            if p_val < 0.05:
                h = y_max * 0.05
                y_top = curr_y + h * 1.5
                
                # Draw Bracket
                ax.plot([idx1, idx1, idx2, idx2], [y_top-h, y_top, y_top, y_top-h], lw=1.5, c='black')
                
                # Add Star
                sig_symbol = "***" if p_val < 0.001 else "**" if p_val < 0.01 else "*"
                ax.text((idx1 + idx2)/2, y_top, sig_symbol, ha='center', va='bottom', fontweight='bold', fontsize=12)
                
                curr_y = y_top # Update height for next bracket

        # Axis clean up (Prism Style)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_ylabel("Innervation Index", fontsize=12, fontweight='bold')
        ax.set_ylim(0, curr_y * 1.15)
        
        st.pyplot(fig)

    with col_stats:
        st.subheader("Statistical Report")
        
        # ANOVA Result
        st.markdown("#### One-Way ANOVA")
        st.metric(label="P-Value", value=f"{p_anova:.4f}")
        if p_anova < 0.05:
            st.success("Significant difference found!")
        else:
            st.warning("No significant difference detected.")
        
        st.divider()
        
        # Tukey Result Table
        st.markdown("#### Pairwise Comparisons (Tukey)")
        # Clean up dataframe for display
        display_df = tukey_df.rename(columns={'group1': 'Group A', 'group2': 'Group B', 'p-adj': 'P-Value', 'reject': 'Significant'})
        st.dataframe(display_df[['Group A', 'Group B', 'P-Value', 'Significant']], hide_index=True)
        
else:
    st.info("Please upload data using the sidebar to begin.")
