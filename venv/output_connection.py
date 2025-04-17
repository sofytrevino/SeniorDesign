from flask import Flask, render_template
app = Flask(__name__)
@app.route('/form', methods=['GET'])
def show_form():
    #need to update this with html files as form; html files should be in a template
    form = MyForm()
    return render_template('form.html', form=form)