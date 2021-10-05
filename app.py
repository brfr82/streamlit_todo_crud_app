import streamlit as st
import pandas as pd 
from db_fxns import * 
import streamlit.components.v1 as stc
import urllib.parse




# Data Viz Pkgs
import plotly.express as px 


HTML_BANNER = """
    <div style="background-color:#464e5f;padding:10px;border-radius:10px">
    <h1 style="color:white;text-align:center;">Lista de Compras para a minha Namorada</h1>
    <p style="color:white;text-align:center;">Built with Streamlit</p>
    </div>
    """


def main():
	stc.html(HTML_BANNER)
	
	menu = ["Listar","Criar","Actualizar","Apagar","sobre"]
	choice = st.sidebar.selectbox("Menu",menu)
	create_table()

	if choice == "Criar":
		st.subheader("Adicionar Item")
		col1,col2 = st.beta_columns(2)
		
		with col1:
			task = st.text_area("Compras a realizar")

		with col2:
			task_status = st.selectbox("Categoria",["Vestuario","Alimentar","Casa","Eletro"])
			task_due_date = st.date_input("Data")

		if st.button("Adicionar compra"):
			add_data(task,task_status,task_due_date)
			st.success("Adicionado ::{} ::To Task".format(task))


	elif choice == "Listar":
		# st.subheader("View Items")
		with st.beta_expander("Ver todas"):
			result = view_all_data()
			# st.write(result)
			clean_df = pd.DataFrame(result,columns=["Compra","Categoria","Data"])
			st.dataframe(clean_df)

		with st.beta_expander("Categoria da compra"):
			task_df = clean_df['Categoria'].value_counts().to_frame()
			# st.dataframe(task_df)
			task_df = task_df.reset_index()
			st.dataframe(task_df)

			p1 = px.pie(task_df,names='index',values='Categoria')
			st.plotly_chart(p1,use_container_width=True)
			
		html = clean_df.to_html()
		url="https://www.google.com/calendar/render?action=TEMPLATE&text=lista+de+compras&details="+urllib.parse.quote(html)+"&location=Lisboa&dates=20211005T155000Z%2F20211005T155000Z"

		link = '[Adicionar_GoogleCalendar]('+url+')'
		st.markdown(link, unsafe_allow_html=True)


	elif choice == "Actualizar":
		st.subheader("Editar Items")
		with st.beta_expander("Data Corrente"):
			result = view_all_data()
			# st.write(result)
			clean_df = pd.DataFrame(result,columns=["Compra","Categoria","Data"])
			st.dataframe(clean_df)

		list_of_tasks = [i[0] for i in view_all_task_names()]
		selected_task = st.selectbox("Compra",list_of_tasks)
		task_result = get_task(selected_task)
		# st.write(task_result)

		if task_result:
			task = task_result[0][0]
			task_status = task_result[0][1]
			task_due_date = task_result[0][2]

			col1,col2 = st.beta_columns(2)
			
			with col1:
				new_task = st.text_area("Compras a realizar",task)

			with col2:
				new_task_status = st.selectbox(task_status,["Vestuario","Alimentar","Casa","Eletro"])
				new_task_due_date = st.date_input(task_due_date)

			if st.button("Actualizar"):
				edit_task_data(new_task,new_task_status,new_task_due_date,task,task_status,task_due_date)
				st.success("Actualizado ::{} ::To {}".format(task,new_task))

			with st.beta_expander("Ver compras actualizadas"):
				result = view_all_data()
				# st.write(result)
				clean_df = pd.DataFrame(result,columns=["Compra","Categoria","Data da compra"])
				st.dataframe(clean_df)


	elif choice == "Apagar":
		st.subheader("Apagar")
		with st.beta_expander("Ver compras"):
			result = view_all_data()
			# st.write(result)
			clean_df = pd.DataFrame(result,columns=["Compra","Categoria","Data da compra"])
			st.dataframe(clean_df)

		unique_list = [i[0] for i in view_all_task_names()]
		delete_by_task_name =  st.selectbox("Seleccionar Compra",unique_list)
		if st.button("Apagar"):
			delete_data(delete_by_task_name)
			st.warning("Apagado: '{}'".format(delete_by_task_name))

		with st.beta_expander("Compras  actualizadas"):
			result = view_all_data()
			# st.write(result)
			clean_df = pd.DataFrame(result,columns=["Compra","Categoria","Data da compra"])
			st.dataframe(clean_df)

	else:
		st.subheader("Sobre: lista de compras")
		st.info("Built with Streamlit")
		st.info("Jesus Saves @JCharisTech")
		st.text("Edits: Bruno Ferreira")

	
		
		
if __name__ == '__main__':
	main()

