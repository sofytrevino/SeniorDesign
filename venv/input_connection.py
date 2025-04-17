from flask import Flask, render_template, request
#import sys
#import os
import subprocess

'''
Request method that enables calling phiSearch functions from within here
# Get the absolute path to the directory containing the script to be called
script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "C:/Users/ogmor/Documents/Spring 25/CS Project/SeniorDesign/SeniorDesign-1"))
# Add the directory to Python's search path
sys.path.append(script_dir)  
# Import the script
import phiSearch
'''

#Subprocess method
app = Flask(__name__)
@app.route('/')
@app.route('/submit', methods=['POST'])
def get_started():
    return render_template('index.html')

def submit_form():
    #get file names from HTML
    fileinput = request.form.get('fileinput')
    medicalfile = request.form.get('medicalfile')
    script_to_run = "C:/Users/ogmor/Documents/Spring 25/CS Project/SeniorDesign/SeniorDesign-1/phiSearch.py"
    arguments = [script_to_run, fileinput, medicalfile] #NOTE: this method requires user providing path for files

    result = run_phiSearch(script_to_run, *arguments)

    if result.returncode == 0:
        print("Script executed successfully.")
        print("Output:", result.stdout)
    else:
        print("Script failed with error code:", result.returncode)
        print("Error message:", result.stderr)
    return "Successfully executed."

def run_phiSearch(script_path, *args):
    # Process form data here
    command = ['python', script_path, *args]
    result = subprocess.run(command, capture_output=True, text=True)
    return result  

   # return 'Form submitted successfully!'
if __name__ == '__main__':
    app.run()