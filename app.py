import os

server = app.server

os.system('python preprocess.py') #to make the preprocess of the data with the url provided

os.system('python dashapp.py')  #to make the dashboard with plotly Dash

if __name__ == "__main__":
    app.run_server(debug=False)
