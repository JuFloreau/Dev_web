from flask import Flask 
from flask import abort, request, make_response, flash
from flask import render_template, redirect, url_for
from werkzeug.utils import secure_filename
import os
import json
import pygal
import re


from data import MATTERS,TEACHERS,CLASS

UPLOAD_FOLDER = 'static\class'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask (__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Test fonctionnement du serveur flask
@app.route('/hello_world')
def hello_world(name=None):
	if name :
		return '<h1>Hello {}!</h1>'.format(name)
	else :
		return '<h1>Hello!</h1>'


@app.route('/')
def index():
	matter_name=[]
	number_class=[]
	if(len(MATTERS)>=1):
		if(len(CLASS)>=1):
			for matter in MATTERS:
				j=0
				for classes in CLASS :
					if classes.get('id_matter')==matter.get('id'):
						j=j+1
				number_class.append(j)
				matter_name.append(matter.get('matter'))

		else:
			bar_chart.title = 'Nombre de cours pas matière'
			for matter in MATTERS:
				number_class.append(0)
				matter_name.append(matter.get('matter'))
	else:
		matter_name.append("Pas de matière et de cours ajoutés")
		number_class.append(0)
	bar_chart = pygal.Bar()
	bar_chart.title = 'Nombre de cours par matière'
	bar_chart.x_labels = matter_name
	bar_chart.add('Cours',number_class)
	graph_data=bar_chart.render_data_uri()

	pie_chart = pygal.Pie()
	pie_chart.title = 'Nombre de cours par matière'
	for i in range(len(matter_name)):
		pie_chart.add(matter_name[i],number_class[i])
	pie_data=pie_chart.render_data_uri()

	return render_template("index.html",graph_data=graph_data, pie_data=pie_data)

#------------------------ ADD FUNCTIONS--------------------------------

@app.route('/add_matter/')
@app.route('/add_matter/', methods=['POST'])
def add_matter():
	if(request.method=='POST'):
		name = request.form.get('name_matter','')
		if(len(MATTERS)>=1):
			new_id=MATTERS[-1].get('id')+1
		else:
			new_id=0
		new_matter={"id":new_id,"matter": name}
		MATTERS.append(new_matter)
		(filepath, filename) = os.path.split('data\data_matter_tmp.json')
		matter_file=open(os.path.join(filepath,filename), "w")
		matter_file.write('{\n  \"MATTERS\": [\n')
		i=0
		for matter in MATTERS:
			matter_file.write("    {\"id\": "+ str(matter.get("id")) + ", \"matter\": \""+ str(matter.get("matter")) +"\"}")
			i=i+1
			if(i!=len(MATTERS)):
				matter_file.write(',\n')
		matter_file.write('\n]\n}')
		matter_file.close()
		filename_to_remove="data_matter.json"
		os.remove(os.path.join(filepath,filename_to_remove))
		os.rename(os.path.join(filepath,filename),os.path.join(filepath,filename_to_remove))
	return render_template('add_matter.html', matter_name=MATTERS)

@app.route('/add_teacher/')
@app.route('/add_teacher/', methods=['POST'])
def add_teacher():
	if(request.method=='POST'):
		name = request.form.get('name_teacher','')
		if(len(TEACHERS)>=1):
			new_id=TEACHERS[-1].get('id')+1
		else:
			new_id=0
		new_teacher={"id":new_id+1,"teacher": name}
		TEACHERS.append(new_teacher)
		(filepath, filename) = os.path.split('data\data_teacher_tmp.json')
		teacher_file=open(os.path.join(filepath,filename), "w")
		teacher_file.write('{\n  \"TEACHERS\": [\n')
		i=0
		for teacher in TEACHERS:
			teacher_file.write("    {\"id\": "+ str(teacher.get("id")) + ", \"teacher\": \""+ str(teacher.get("teacher")) +"\"}")
			i=i+1
			if(i!=len(TEACHERS)):
				teacher_file.write(',\n')
		teacher_file.write('\n]\n}')
		teacher_file.close()
		filename_to_remove="data_teacher.json"
		os.remove(os.path.join(filepath,filename_to_remove))
		os.rename(os.path.join(filepath,filename),os.path.join(filepath,filename_to_remove))
	return render_template('add_teacher.html', teacher_name=TEACHERS)

def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/add_class')
@app.route('/add_class', methods=['POST'])
def add_class():
	if(request.method=='POST'):
		name_class = request.form.get('name_class','')
		matter = request.form.get('matter_name','')
		teacher = request.form.get('teacher_name','')
		myfilename=""
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		# if user does not select file, browser also
		# submit an empty part without filename
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			myfilename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], myfilename))
		id_matter=None
		id_teacher=None
		for item in MATTERS:
			if item.get('matter')==matter:
				id_matter=item.get('id')
				break;	
		for item in TEACHERS:
			if item.get('teacher')==teacher:
				id_teacher=item.get('id')
				break;
		if(len(CLASS)>=1):
			new_id=CLASS[-1].get('id')+1
		else:
			new_id=0
		new_class={"id": new_id, "class_name": name_class, "id_matter": id_matter, "id_teacher": id_teacher, "file_name":myfilename}
		CLASS.append(new_class)
		(filepath, filename) = os.path.split('data\data_class_tmp.json')
		class_file=open(os.path.join(filepath,filename), "w")
		class_file.write('{\n  \"CLASS\": [\n')
		i=0
		for classes in CLASS:
			class_file.write("{\"id\": "+ str(classes.get("id")) + ", \"class_name\": \""+str(classes.get("class_name"))+"\", \"id_matter\": "+str(classes.get("id_matter"))+", \"id_teacher\": "+ str(classes.get("id_teacher")) +", \"file_name\": \""+str(classes.get("file_name"))+"\"}")
			i=i+1
			if(i!=len(CLASS)):
				class_file.write(',\n')
		class_file.write('\n]\n}')
		class_file.close()
		filename_to_remove="data_class.json"
		os.remove(os.path.join(filepath,filename_to_remove))
		os.rename(os.path.join(filepath,filename),os.path.join(filepath,filename_to_remove))
		return render_template('class_list.html', name_class=CLASS, name_matter=MATTERS, name_teacher=TEACHERS)
	return render_template('add_class.html', class_name=CLASS, MATTER=MATTERS, TEACHER=TEACHERS)


#------------------------ DELETE FUNCTIONS--------------------------------
def delete_matters(id):

	liste_class_del=[]
	for classes in CLASS:
		if(classes.get('id_matter')==id):
			liste_class_del.append(classes.get('id'))
	for index in liste_class_del:
		delete_classes(index)
	j=0
	for matter in MATTERS:
		if matter.get('id')==id:
			del MATTERS[j]
		j=j+1
	(filepath, filename) = os.path.split('data\data_matter_tmp.json')
	matter_file=open(os.path.join(filepath,filename), "w")
	matter_file.write('{\n  \"MATTERS\": [\n')
	i=0
	for matter in MATTERS:
		matter_file.write("    {\"id\": "+ str(matter.get("id")) + ", \"matter\": \""+ str(matter.get("matter")) +"\"}")
		i=i+1
		if(i!=len(MATTERS)):
			matter_file.write(',\n')
	matter_file.write('\n]\n}')
	matter_file.close()
	filename_to_remove="data_matter.json"
	os.remove(os.path.join(filepath,filename_to_remove))
	os.rename(os.path.join(filepath,filename),os.path.join(filepath,filename_to_remove))

def delete_teachers(id):
	liste_class_del=[]
	for classes in CLASS:
		if(classes.get('id_teacher')==id):
			liste_class_del.append(classes.get('id'))
	for index in liste_class_del:
		delete_classes(index)
	j=0
	for teacher in TEACHERS:
		if teacher.get('id')==id:
			del TEACHERS[j]
		j=j+1

	(filepath, filename) = os.path.split('data\data_teacher_tmp.json')
	teacher_file=open(os.path.join(filepath,filename), "w")
	teacher_file.write('{\n  \"TEACHERS\": [\n')
	i=0
	for teacher in TEACHERS:
		teacher_file.write("    {\"id\": "+ str(teacher.get("id")) + ", \"teacher\": \""+ str(teacher.get("teacher")) +"\"}")
		i=i+1
		if(i!=len(TEACHERS)):
			teacher_file.write(',\n')
	teacher_file.write('\n]\n}')
	teacher_file.close()
	filename_to_remove="data_teacher.json"
	os.remove(os.path.join(filepath,filename_to_remove))
	os.rename(os.path.join(filepath,filename),os.path.join(filepath,filename_to_remove))
	return render_template('add_teacher.html', teacher_name=TEACHERS)

def delete_classes(id):
	j=0
	for classes in CLASS:
		if classes.get('id')==id:
			os.remove(os.path.join(UPLOAD_FOLDER,classes.get('file_name')))
			del CLASS[j]
		j=j+1
	(filepath, filename) = os.path.split('data\data_class_tmp.json')
	class_file=open(os.path.join(filepath,filename), "w")
	class_file.write('{\n  \"CLASS\": [\n')
	i=0
	for classes in CLASS:
		class_file.write("{\"id\": "+ str(classes.get("id")) + ", \"class_name\": \""+str(classes.get("class_name"))+"\", \"id_matter\": "+str(classes.get("id_matter"))+", \"id_teacher\": "+ str(classes.get("id_teacher")) +", \"file_name\": \""+str(classes.get("file_name"))+"\"}")
		i=i+1
		if(i!=len(CLASS)):
			class_file.write(',\n')
	class_file.write('\n]\n}')
	class_file.close()
	filename_to_remove="data_class.json"
	os.remove(os.path.join(filepath,filename_to_remove))
	os.rename(os.path.join(filepath,filename),os.path.join(filepath,filename_to_remove))

@app.route('/verification_matter/<int:id>')
def verification_matter(id=None):
	if (id!=None):
		for classes in CLASS:
			if(classes.get('id_matter')==id):
				return render_template('ask_verif.html', name="delete_matter",back="add_matter", id=id)
		delete_matters(id)
	return render_template('add_matter.html', matter_name=MATTERS)

@app.route('/verification_teacher/<int:id>')
def verification_teacher(id=None):
	if (id!=None):
		for classes in CLASS:
			if(classes.get('id_teacher')==id):
				return render_template('ask_verif.html', name="delete_teacher",back="add_teacher", id=id)
		delete_teachers(id)
	return render_template('add_teacher.html', teacher_name=TEACHERS)

@app.route('/delete_matter/<int:id>')
def delete_matter(id=None):
	if (id!=None):
		delete_matters(id)
	return render_template('add_matter.html', matter_name=MATTERS)

@app.route('/delete_class/<int:id>')
def delete_class(id=None):
	if (id!=None):
		delete_classes(id)
	return render_template('class_list.html', name_class=CLASS, name_matter=MATTERS, name_teacher=TEACHERS)

@app.route('/delete_teacher/<int:id>')
def delete_teacher(id=None):
	if (id!=None):
		delete_teachers(id)
	return render_template('add_matter.html', matter_name=MATTERS)


@app.route('/class_list')
def class_list():
	return render_template('class_list.html', name_class=CLASS, name_matter=MATTERS, name_teacher=TEACHERS)

@app.route('/search/', methods=['GET'])
def search():
	app.logger.debug(request.args)
	if (request.method=='GET'):
		searchword = request.args.get('pattern','')
		regexp = request.args.get('regexp','')
		res=[]
		if not regexp:
			if not searchword:
				return redirect('/')
			if searchword=='':
				return redirect('/')
			else:
				for classes in CLASS :
					for matter in MATTERS:
						if classes.get('id_matter')==matter.get('id'):
							if searchword.lower() in matter.get("matter").lower():
								res.append(classes)
							break;
					for teacher in TEACHERS:
						if classes.get('id_teacher')==teacher.get('id'):
							if searchword.lower() in teacher.get("teacher").lower():
								res.append(classes)
							break;
					if searchword.lower() in classes.get("class_name").lower():
						res.append(classes)
				return render_template('class_list.html', name_class=res, name_matter=MATTERS, name_teacher=TEACHERS)
		else :
			if not searchword:
				flash('No result found')
				return redirect('/')
			if searchword=='':
				flash('No result found')
				return redirect('/')
			else:
				for classes in CLASS :
					for matter in MATTERS:
						if classes.get('id_matter')==matter.get('id'):
							if re.match(searchword,matter.get("matter")):
								res.append(classes)
							break;
					for teacher in TEACHERS:
						if classes.get('id_teacher')==teacher.get('id'):
							if re.match(searchword,teacher.get("teacher")):
								if(classes not in res):
									res.append(classes)
							break;
					if re.match(searchword,classes.get("class_name")):
						if(classes not in res):
							res.append(classes)
				return render_template('class_list.html', name_class=res, name_matter=MATTERS, name_teacher=TEACHERS)
	return render_template('class_list.html', name_class=CLASS, name_matter=MATTERS, name_teacher=TEACHERS)
	abort(make_response('Not implemented yet ;)', 501))

# Script starts here
if __name__ == '__main__':
	from os import environ
	DEBUG = environ.get('DEBUG')
	app.run(port=8000, debug=DEBUG)


