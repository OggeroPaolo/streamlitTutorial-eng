import streamlit as st
from utils.utils import *
import pandas as pd

def create_products_tab(products_tab):
    col1, col2, col3 = products_tab.columns(3)
    payment_info = execute_query(st.session_state["connection"],
                                 "SELECT SUM(amount) AS 'Total Amount', MAX(amount) AS 'Max Payment', AVG(amount) AS 'Average Payment' FROM payments;")
    # create a suitable data structure from the query result
    payment_info_dict = [dict(zip(payment_info.keys(), result)) for result in payment_info]
    # add selected parameters as horizontal metrics
    col1.metric('Total Amount', f"$ {compact_format(payment_info_dict[0]['Total Amount'])}")
    col2.metric('Max Payment', f"$ {compact_format(payment_info_dict[0]['Max Payment'])}")
    col3.metric('Average Payment', f"$ {compact_format(payment_info_dict[0]['Average Payment'])}")

# each tab has a separate function

if __name__ == "__main__":
    st.title("📈 Analysis")

    # creation of separate tabs
    products_tab, staff_tab, customers_tab = st.tabs(["Products", "Staff", "Customers"])
    if check_connection():
        create_products_tab(products_tab=products_tab)
