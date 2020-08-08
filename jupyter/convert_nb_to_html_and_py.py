# Run all this in a Jupyter notebook cell.
%%javascript
IPython.notebook.save_notebook()
IPython.notebook.kernel.execute('nb_name = "' + IPython.notebook.notebook_name + '"')

!jupyter nbconvert --to script $nb_name
!jupyter nbconvert --to html $nb_name