import streamlit as st
import plotly.express as px
import pandas as pd
from database.db_manager import init_db
from auth.login import show_login_page
from auth.register import show_register_page
import modules.dna_analyzer_logic as logic

init_db()
st.set_page_config(page_title="NextGen DNA Analyzer", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
        /* Force body and sidebar backgrounds to stay light white/clean */
        .stApp, section[data-testid="stSidebar"] {
            background-color: #f8fafc !important;
            background: #f8fafc !important;
        }
        
        /* Overrides both Light and Dark mode font colors globally to solid black */
        .stApp p, .stApp span, .stApp h1, .stApp h2, .stApp h3, .stApp label,
        section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span, 
        section[data-testid="stSidebar"] label, section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
        }
        
        /* FIX: Force All Input and Textarea box backgrounds to be clean white and text to be solid black */
        input, select, textarea, [data-testid="stTextInput"] div, [data-testid="stTextArea"] div, [data-testid="stWidgetLabel"] {
            background-color: #ffffff !important;
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
        }
        
        /* ULTRA FIX: Force ALL Streamlit Buttons to have solid dark background and bright white text */
        button, [data-testid^="baseButton"], .stButton button {
            background-color: #1e293b !important;
            color: #ffffff !important;
            border: 1px solid #1e293b !important;
        }
        
        /* Force button text inside paragraph/span tags to stay white */
        button p, button span, [data-testid^="baseButton"] p, [data-testid^="baseButton"] span {
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
        }
        
        /* FIX: Force Sidebar close/open arrow icon to be visible black */
        section[data-testid="stSidebarCollapsedControl"] button svg, 
        button[data-testid="collapsedControl"] svg,
        [data-testid="stSidebar"] button svg {
            fill: #000000 !important;
            color: #000000 !important;
        }
        
        /* Maintain your custom design cards but force black text inside them */
        .glass-card { 
            background: #ffffff; 
            border-radius: 12px; 
            border: 1px solid #e2e8f0; 
            padding: 25px; 
            margin-bottom: 15px;
            color: #000000 !important;
        }
        .metric-box { 
            background: #f0fdf4; 
            border: 1px solid #bbf7d0; 
            padding: 15px; 
            border-radius: 10px; 
            text-align: center;
            color: #000000 !important;
        }
        .metric-title { color: #334155 !important; font-size: 14px; font-weight: 500; }
        .metric-val { font-size: 26px; font-weight: bold; color: #16a34a !important; }
        
        .alignment-box { 
            font-family: monospace; 
            background-color: #0f172a; 
            color: #38bdf8 !important; 
            padding: 20px; 
            border-radius: 8px;
            -webkit-text-fill-color: #38bdf8 !important;
        }
        
        /* FIX: Top bar cards text to be solid crisp White */
        .system-top-bar p, .system-top-bar span, .system-top-bar h1, .system-top-bar h2, .system-top-bar h3, .system-top-bar div {
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
        }
        
        .system-top-bar {
            background: linear-gradient(90deg, #0f172a 0%, #1e293b 100%);
            padding: 15px 25px;
            border-radius: 12px;
            display: flex;
            justify-content: space-between;
        }
        
        h1, h2, h3 { color: #1e293b !important; }
    </style>
""", unsafe_allow_html=True)
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# Initialize Session State Variables
if 'analysis_triggered' not in st.session_state:
    st.session_state['analysis_triggered'] = False
if 'clean_seq_data' not in st.session_state:
    st.session_state['clean_seq_data'] = ""

if not st.session_state['logged_in']:
    auth_menu = st.radio("Access Terminal:", ["Sign-In Gateway Portal", "New Operator Account Registration"], horizontal=True, label_visibility="collapsed")
    st.markdown("<br>", unsafe_allow_html=True)
    if auth_menu == "Sign-In Gateway Portal":
        show_login_page()
    else:
        st.markdown('<div style="max-width:550px; margin: 40px auto;" class="glass-card">', unsafe_allow_html=True)
        show_register_page()
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown(f"""
        <div class="system-top-bar">
            <div style="color: #38bdf8; font-weight: 700; font-size: 14px; letter-spacing:0.5px;">
                ⚙️ GENOMIC OPERATIONAL KERNEL ACTIVE
            </div>
            <div style="color: #ffffff; font-size: 15px; font-weight: 600;">
                🚀 FOUNDER & CHIEF ARCHITECT: <span style="color: #a3e635; font-weight: 800; letter-spacing:0.5px;">ARJUNAN G</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.sidebar.success(f"Verified: {st.session_state.get('user_name', 'User')}")
    st.sidebar.markdown("---")
    st.sidebar.subheader("🎛️ Analysis Engine Mode")
    engine_mode = st.sidebar.radio("Select Tool Platform:", ["Single Sequence Engine", "Competitive Alignment Engine", "PCR Primer Designer"])
    
    if st.sidebar.button("Logout Server Session"):
        st.session_state['logged_in'] = False
        st.session_state['analysis_triggered'] = False
        st.rerun()
        
    # MODE 1: Single Genomic Sequence Suite
    if engine_mode == "Single Sequence Engine":
        st.title("🧬 NextGen DNA Analyzer")
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Data Input Hub Terminal")
        
        input_type = st.radio("Choose Sequence Feeding Methodology Panel:", ["Manual Character Text Input", "High-Volume FASTA/TXT File Load (Supports up to 200MB)"])
        
        seq_input = ""
        if input_type == "Manual Character Text Input":
            seq_input = st.text_area("Enter DNA sequence (e.g., ATCG...)", height=120)
        else:
            uploaded_fasta = st.file_uploader("Upload Biological Sequence Asset Dataset (.fasta, .txt):", type=["fasta", "txt"])
            if uploaded_fasta is not None:
                file_bytes = uploaded_fasta.read()
                seq_input = logic.parse_fasta_file(file_bytes)
                st.info(f"FASTA file parsing complete. Processed Vector Sequence Stream Length: {len(seq_input)} base pairs.")
        
        if st.button("Analyze Sequence"):
            if seq_input and logic.validate_dna_sequence(seq_input):
                st.session_state['analysis_triggered'] = True
                st.session_state['clean_seq_data'] = seq_input.upper().replace(" ", "").replace("\n", "").replace("\r", "")
            else:
                st.error("Invalid sequence framework or empty terminal field!")
                st.session_state['analysis_triggered'] = False
                
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Persistent UI Rendering Block
        if st.session_state['analysis_triggered']:
            clean_seq = st.session_state['clean_seq_data']
            metrics = logic.calculate_sequence_metrics(clean_seq)
            mutation_data = logic.detect_mutations_and_diseases(clean_seq)
            homology_list = logic.calculate_species_homology(clean_seq)
            
            # 📜 Certified Diagnostic PDF Exporter Button Area
            st.markdown('<div class="glass-card" style="border: 2px solid #3b82f6; background: #eff6ff;">', unsafe_allow_html=True)
            st.subheader("📄 Certified Molecular Diagnostics Data Exporter")
            st.write("Generate and download a high-precision corporate lab reference transcript file certified by Arjunan G:")
            
            # Lazy-loaded data logic integration to fix NameError
            try:
                pdf_report_data = logic.generate_high_detailed_report(clean_seq, metrics, mutation_data, homology_list)
                st.download_button(
                    label="📥 Download Certified Lab Diagnostic PDF Report",
                    data=pdf_report_data,
                    file_name="GENOMIC_DIAGNOSTIC_REPORT_ARJUNAN.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    type="primary"
                )
            except Exception as e:
                st.error(f"Error compiling PDF stream generation: {str(e)}")
                
            st.markdown('</div>', unsafe_allow_html=True)

            st.subheader("📊 Core Sequence Metrics")
            col1, col2, col3 = st.columns(3)
            with col1: st.markdown(f'<div class="metric-box"><span class="metric-title">Sequence Length</span><br><span class="metric-val">{metrics["length"]} bp</span></div>', unsafe_allow_html=True)
            with col2: st.markdown(f'<div class="metric-box"><span class="metric-title">GC Content</span><br><span class="metric-val">{metrics["gc_percentage"]}%</span></div>', unsafe_allow_html=True)
            with col3: st.markdown(f'<div class="metric-box"><span class="metric-title">AT Content</span><br><span class="metric-val">{metrics["at_percentage"]}%</span></div>', unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # 2D Map Blueprint
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("🗺️ Interactive 2D Genomic Mutation Map Blueprint")
            base_records = []
            mut_positions = {m["Position"]: m for m in mutation_data}
            for idx, base in enumerate(clean_seq):
                pos = idx + 1
                if pos in mut_positions:
                    base_records.append({"Position (bp)": pos, "Base": base, "Status": "Pathogenic Variant (Mutant)"})
                else:
                    base_records.append({"Position (bp)": pos, "Base": base, "Status": "Wild-Type (Normal)"})
            df_map = pd.DataFrame(base_records)
            fig_map = px.scatter(df_map, x="Position (bp)", y=[1] * len(df_map), color="Status",
                                 color_discrete_map={"Wild-Type (Normal)": "#3b82f6", "Pathogenic Variant (Mutant)": "#ef4444"},
                                 hover_data={"Position (bp)": True, "Base": True, "Status": True}, template="plotly_white")
            fig_map.update_layout(yaxis={'visible': False}, xaxis={'title': "Nucleotide Position Axis"}, height=180)
            st.plotly_chart(fig_map, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Clinical Table
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("🏥 Genomic Variant Mutation & Clinical Disease Table")
            st.dataframe(pd.DataFrame(mutation_data).drop(columns=["Position"], errors="ignore"), use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Species Tracker
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("🌍 Multi-Species Cross-Genetic Homology Tracker")
            df_homology = pd.DataFrame(homology_list)
            h_col1, h_col2 = st.columns([3, 2])
            with h_col1:
                fig_homology = px.bar(df_homology, x="Homology Match (%)", y="Species", color="Species",
                                      orientation="h", title="Species Match Percentage Matrix Mapping",
                                      template="plotly_white", text="Homology Match (%)")
                fig_homology.update_layout(showlegend=False, yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig_homology, use_container_width=True)
            with h_col2:
                st.write("<br><br>", unsafe_allow_html=True)
                st.dataframe(df_homology, use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Charts
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("📈 Nucleotide Frequency Visualization")
            df_freq = pd.DataFrame(list(metrics['frequencies'].items()), columns=['Nucleotide', 'Count'])
            chart_col1, chart_col2 = st.columns(2)
            with chart_col1: st.plotly_chart(px.bar(df_freq, x='Nucleotide', y='Count', color='Nucleotide', title="Nucleotide Composition", template="plotly_white"), use_container_width=True)
            with chart_col2: st.plotly_chart(px.pie(df_freq, names='Nucleotide', values='Count', title="Nucleotide Ratio", template="plotly_white", hole=0.4), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            utilities = logic.generate_molecular_utilities(clean_seq)
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("🧬 Downstream Molecular Biology Utilities Output")
            st.text_area("Calculated DNA Reverse Complement Strand:", utilities['reverse_complement'], height=70)
            st.text_area("Transcribed Messenger RNA (mRNA) Chain Variant:", utilities['mrna'], height=70)
            st.text_area("Translated Amino Acid Protein Structural String Vector:", utilities['protein'], height=70)
            st.markdown('</div>', unsafe_allow_html=True)

    # MODE 2: Competitive Sequence Alignment Engine
    elif engine_mode == "Competitive Alignment Engine":
        st.title("🔀 Competitive Sequence Alignment Suite")
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Input Comparative Targets")
        col_in1, col_in2 = st.columns(2)
        with col_in1: seq1_input = st.text_area("Reference Sequence (Wild-Type DNA / Normal Target)", "ATGCGATCGATCGATCGATC", height=120)
        with col_in2: seq2_input = st.text_area("Sample Sequence (Patient DNA / Variable Target)", "ATGGGATCGATCGCTCGATC", height=120)
        align_btn = st.button("Execute Cross-Alignment Analysis")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if align_btn:
            if logic.validate_dna_sequence(seq1_input) and logic.validate_dna_sequence(seq2_input):
                align_results = logic.perform_competitive_alignment(seq1_input, seq2_input)
                st.subheader("📊 Comparative Similarity Scores")
                c1, c2, c3 = st.columns(3)
                with c1: st.markdown(f'<div class="metric-box" style="background:#eff6ff; border-color:#bfdbfe;"><span class="metric-title" style="color:#1e40af;">Identity Match Ratio</span><br><span class="metric-val" style="color:#1d4ed8;">{align_results["similarity_percentage"]}%</span></div>', unsafe_allow_html=True)
                with c2: st.markdown(f'<div class="metric-box"><span class="metric-title">Conserved Homology Bases</span><br><span class="metric-val">{align_results["matched_bases"]} bp</span></div>', unsafe_allow_html=True)
                with c3: st.markdown(f'<div class="metric-box" style="background:#fef2f2; border-color:#fecaca;"><span class="metric-title" style="color:#991b1b;">Mutated Mismatches / Gaps</span><br><span class="metric-val" style="color:#b91c1c;">{align_results["mismatch_or_gaps"]} bp</span></div>', unsafe_allow_html=True)
                
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.subheader("🧬 Pairwise Alignment Map Blueprint")
                alignment_display = f"REF_STRAND:  {align_results['visual_1']}\n             {align_results['visual_match']}\nSMP_STRAND:  {align_results['visual_2']}"
                st.markdown(f'<div class="alignment-box">{alignment_display}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

    # MODE 3: PCR Primer Designer Suite
    elif engine_mode == "PCR Primer Designer":
        st.title("🧬 Industrial PCR Primer Designer Suite")
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Target Template Strand Initialization")
        pcr_seq_input = st.text_area("Enter Target DNA Oligonucleotide Sequence for amplification framework:", "ATGCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATC", height=120)
        p_len = st.slider("Select Custom Oligo Primer Length (Nucleotide Bases count):", min_value=15, max_value=50, value=20)
        pcr_btn = st.button("Generate Optimized Amplification Primers")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if pcr_btn:
            if logic.validate_dna_sequence(pcr_seq_input):
                primer_output = logic.design_pcr_primers(pcr_seq_input, p_len)
                if primer_output:
                    st.subheader("📊 Designed Core Amplification Oligos")
                    p_col1, p_col2 = st.columns(2)
                    with p_col1:
                        st.markdown('<div class="glass-card" style="border-left: 5px solid #2563eb;">', unsafe_allow_html=True)
                        st.markdown("### 🔵 Forward Primer (5' ➔ 3')")
                        st.code(primer_output["forward"]["seq"])
                        st.write(f"**Oligo Length:** {primer_output['forward']['length']} bp")
                        st.write(f"**GC Content:** {primer_output['forward']['gc']}%")
                        st.write(f"**Melting Temp ($T_m$):** {primer_output['forward']['tm']} °C")
                        st.markdown('</div>', unsafe_allow_html=True)
                    with p_col2:
                        st.markdown('<div class="glass-card" style="border-left: 5px solid #16a34a;">', unsafe_allow_html=True)
                        st.markdown("### 🟢 Reverse Primer (5' ➔ 3')")
                        st.code(primer_output["reverse"]["seq"])
                        st.write(f"**Oligo Length:** {primer_output['reverse']['length']} bp")
                        st.write(f"**GC Content:** {primer_output['reverse']['gc']}%")
                        st.write(f"**Melting Temp ($T_m$):** {primer_output['reverse']['tm']} °C")
                        st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.error("Template DNA Sequence length is too short to safely engineer dual flanking primers.")
            else:
                st.error("Invalid sequence!")
