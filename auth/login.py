import streamlit as st
from database.db_manager import verify_user

def show_login_page():
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%) !important;
            color: #0f172a !important;
        }
        [data-testid="stHeader"] { background: transparent !important; }
        
        .portal-wrapper {
            max-width: 1100px;
            margin: 0 auto;
            padding: 30px 20px;
        }
        .hero-title {
            font-family: 'Inter', system-ui, sans-serif;
            font-size: 42px;
            font-weight: 800;
            color: #1e293b;
            letter-spacing: -1px;
            margin-bottom: 8px;
            text-align: center;
        }
        .hero-subtitle {
            font-size: 16px;
            color: #64748b;
            text-align: center;
            margin-bottom: 40px;
        }
        
        .form-side {
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.6);
            padding: 35px;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.05);
        }
        
        .feature-card {
            background: #ffffff;
            border-radius: 14px;
            padding: 20px;
            margin-bottom: 16px;
            border: 1px solid #e2e8f0;
        }
        .feature-title {
            font-size: 16px;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 4px;
        }
        .feature-desc {
            font-size: 13px;
            color: #64748b;
            line-height: 1.5;
        }
        
        .founder-header-badge {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #ffffff !important;
            padding: 15px;
            border-radius: 12px;
            text-align: center;
            margin-bottom: 25px;
            box-shadow: 0 4px 12px rgba(15, 23, 42, 0.15);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="portal-wrapper">', unsafe_allow_html=True)
    st.markdown('<h1 class="hero-title">🧬 NextGen DNA Analyzer Suite</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Advanced Cloud-Native Computational Genomics Platform</p>', unsafe_allow_html=True)
    
    # Swapped column weight order to bring login forms to the left array
    col_left, col_right = st.columns([0.9, 1.2])
    
    # LEFT COLUMN: Login Gate & Founder Card (First target on mobiles)
    with col_left:
        st.markdown('<div class="form-side">', unsafe_allow_html=True)
        
        st.markdown("""
            <div class="founder-header-badge">
                <div style="font-size:10px; color:#38bdf8; font-weight:700; letter-spacing:1.5px; margin-bottom:2px;">FOUNDER & CHIEF ARCHITECT</div>
                <div style="font-size:18px; font-weight:800; color:#ffffff; letter-spacing:0.5px;">ARJUNAN G</div>
                <div style="font-size:12px; color:#94a3b8; margin-top:2px;">Lead Systems Engineer • V2.0 Stable</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<h4 style='color:#1e293b; margin-bottom:15px; font-weight:700;'>Secure Gateway Sign-In</h4>", unsafe_allow_html=True)
        
        email = st.text_input("Research Email ID", placeholder="operator@genomics.org", key="login_email")
        password = st.text_input("Security Access Passphrase", type="password", placeholder="••••••••••••", key="login_pwd")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Authenticate Space Entry", use_container_width=True):
            if email and password:
                user = verify_user(email, password)
                if user:
                    st.session_state['logged_in'] = True
                    st.session_state['user_name'] = "ARJUNAN G"
                    st.success("Access verified!")
                    st.rerun()
                else:
                    st.error("Access Denied! Invalid credentials.")
            else:
                st.warning("Please verify all fields.")
                
        st.markdown("<div style='text-align:center; margin: 12px 0; color:#94a3b8; font-size:11px;'>OR DEMO PRESENTATION</div>", unsafe_allow_html=True)
        
        if st.button("🔓 Quick Bypass / Developer Mode", use_container_width=True, type="primary"):
            st.session_state['logged_in'] = True
            st.session_state['user_name'] = "ARJUNAN G"
            st.success("Welcome Leader!")
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)
        
    # RIGHT COLUMN: Feature Information Cards
    with col_right:
        st.markdown('<div class="info-side" style="padding-left: 10px;">', unsafe_allow_html=True)
        st.markdown("<h3 style='color:#334155; margin-bottom:20px; font-weight:700;'>🎯 Core Structural Platform Engines</h3>", unsafe_allow_html=True)
        st.markdown("""
            <div class="feature-card">
                <div class="feature-title">⚡ High-Volume Sequence Uplink Engine</div>
                <div class="feature-desc">Integrated buffer framework optimized for massive data sequencing files. Secure streaming pipeline architectures support up to <b>200MB multi-FASTA / TXT entries</b>.</div>
            </div>
            <div class="feature-card">
                <div class="feature-title">🗺️ Interactive 2D Variant Hotspot Mapper</div>
                <div class="feature-desc">Translates nucleotide locations into clinical models while highlighting pathogenic point variant hazards via neon indicators.</div>
            </div>
            <div class="feature-card">
                <div class="feature-title">🌍 Cross-Species Homology Core Tracker</div>
                <div class="feature-desc">Executes real-time evolutionary taxonomy matching algorithms against standard global reference frameworks.</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)