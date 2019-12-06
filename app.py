import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
# Using bson objectId to convert the ID being passed from our template into a readable format for MongoDB.
from bson.objectid import ObjectId


app = Flask(__name__)


app.config["MONGO_DBNAME"] = 'task_manager'
app.config["MONGO_URI"] = 'mongodb+srv://root:r00tUser@newcluster-ldajm.mongodb.net/task_manager?retryWrites=true&w=majority'


mongo = PyMongo(app)


@app.route('/')


@app.route('/get_tasks')
def get_tasks():
    return render_template("tasks.html", tasks=mongo.db.tasks.find())


@app.route('/add_task')
def add_task():
    return render_template('addtask.html', categories=mongo.db.categories.find())


"""Form submission to take currently filled fields to create a new document in our tasks collection.
We convert the form to a dict so it can be easily understood by Mongo. In reality we would also add form validation here
and as part of html check."""
@app.route('/insert_task', methods=['POST'])
def insert_task():
    tasks = mongo.db.tasks
    tasks.insert_one(request.form.to_dict())
    return redirect(url_for('get_tasks'))
# Good practice to return the user to the task page once document is created in DB.


"""Create associated function that will react to the 'edit' button being clicked to edit the properties associated
with just that singular task. Fetch the task that matches the task ID using the mongo ID as parameter alongside the value
returned from our BSON objectID."""
@app.route('/edit_task/<task_id>')
def edit_task(task_id):
    the_task = mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
    # 2nd thing to do is to list the collections because we're going to use the task that's returned from MongoDB.
    # and all the categories to populate the form for editing, instead of showing a blank form like add_task....
    all_categories = mongo.db.categories.find()
    return render_template('edittask.html', task=the_task, categories=all_categories)


@app.route('/update_task/<task_id>', methods=['POST'])
def update_task(task_id):
    tasks = mongo.db.tasks
    tasks.update({'_id': ObjectId(task_id)},
     {
        'task_name': request.form.get('task_name'),
        'category_name': request.form.get('category_name'),
        'task_description': request.form.get('task_description'),
        'due_date': request.form.get('due_date'),
        'is_urgent': request.form.get('is_urgent')
     })
    return redirect(url_for('get_tasks'))


@app.route('/delete_task/<task_id>')
def delete_task(task_id):
    mongo.db.tasks.remove({'_id': ObjectId(task_id)})
    return redirect(url_for('get_tasks'))


@app.route('/get_categories')
def get_categories():
    return render_template('categories.html', categories=mongo.db.categories.find())


@app.route('/edit_category/<category_id>')
def edit_category(category_id):
    return render_template('editcategory.html', category=mongo.db.categories.find_one({'_id': ObjectId(category_id)}))


@app.route('/update_category/<category_id>', methods=['POST'])
def update_category(category_id):
    mongo.db.categories.update(
        {'_id': ObjectId(category_id)},
        {'category_name': request.form.get('category_name')})
    return redirect(url_for('get_categories'))


if __name__ == "__main__":
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=True)