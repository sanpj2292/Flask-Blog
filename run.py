from flaskblog import app

# To run the server using python command rather than flask command
if __name__ == '__main__':
    # Debug True is set to make sure whenever there is change
    # then we don't need of stopping and restarting the server
    app.run(debug=True)