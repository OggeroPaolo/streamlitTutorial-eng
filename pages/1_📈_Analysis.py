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

    with products_tab.expander("Product Overview",True):
        prod_col1, prod_col2, prod_col3 = st.columns([3, 3, 4])
        sort_par = prod_col1.radio("sorted by: ", ["code", "name", "quantity", "price"])
        sort_choice = prod_col2.selectbox("Ordered by: ", ["ascending", "descending"])

        sort_dict ={"ascending": "ASC", "descending": "DESC"}

        if prod_col1.button("Sort", type="primary"):
            query1 = "SELECT productCode AS 'code', productName AS 'name', quantityInStock AS 'quantity', buyPrice AS 'price', MSRP FROM products"
            query2 = f"ORDER BY {sort_par} {sort_dict[sort_choice]}"
            products = execute_query(st.session_state["connection"], query1+ " " + query2 + ";")
            df_products = pd.DataFrame(products)
            st.dataframe(df_products, use_container_width=True)

# each tab has a separate function

if __name__ == "__main__":
    st.title("📈 Analysis")

    # creation of separate tabs
    products_tab, staff_tab, customers_tab = st.tabs(["Products", "Staff", "Customers"])
    if check_connection():
        create_products_tab(products_tab=products_tab)
