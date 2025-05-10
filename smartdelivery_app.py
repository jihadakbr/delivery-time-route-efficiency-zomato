import streamlit as st

# Adjusting the page
st.set_page_config(
    page_title="SmartDelivery Analytics", 
    page_icon="🛵", 
    layout='wide'
)

def main():
    # Load external CSS
    def load_css():
        with open("assets/styles.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Load external JS
    def load_js(current_page):
        with open("assets/scripts.js") as f:
            js_code = f.read().replace("{{CURRENT_PAGE}}", current_page)
            st.markdown(f"<script>{js_code}</script>", unsafe_allow_html=True)

    # Initialize session state for page navigation
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "🏠 Home"

    # Navigation options
    nav_options = [
        "🏠 Home",
        "🔍 Overview",
        "📊 Dashboard",
        "🛵 Delivery Time",
        "📞 Contact"
    ]

    # Load CSS
    load_css()

    # Sidebar navigation
    with st.sidebar:
        st.markdown(
            '<div class="sidebar-title">🛵 SmartDelivery Analytics</div>', 
            unsafe_allow_html=True
        )
        
        for option in nav_options:
            if st.button(option, key=option):
                st.session_state.current_page = option
                st.rerun()
        
        st.markdown(
            '<div class="sidebar-footer">Made with ❤️ by Jihad Akbar</div>', 
            unsafe_allow_html=True
        )

    # Load JS with current page
    load_js(st.session_state.current_page)

    # Page display logic
    if st.session_state.current_page == "🏠 Home":
        from custom_pages.home import home_page
        home_page()

    elif st.session_state.current_page == "🔍 Overview":
        from custom_pages.overview import overview_page
        overview_page()

    elif st.session_state.current_page == "📊 Dashboard":
        from custom_pages.dashboard import dashboard_page
        dashboard_page()

    elif st.session_state.current_page == "🛵 Delivery Time":
        from app.delivery_time import delivery_time_page
        delivery_time_page()

    else:
        from custom_pages.contact import contact_page
        contact_page()

if __name__ == "__main__":
    main()