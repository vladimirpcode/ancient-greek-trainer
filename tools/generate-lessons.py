import os

data_path = r"../db/lessons"
pages_path = r"../lessons"
pattern_path = r"../patterns"

def parse(data):
	c = ""
	i = 0
	
	def getnext():
		nonlocal c
		nonlocal i
		nonlocal data
		if i >= len(data):
			c = "EOT"
			return c
		c = data[i]
		i += 1
		return c
	
	def parse_key():
		nonlocal c
		key = ""
		while c != "EOT" and c != "{":
			if not c.isspace():
				key += c
			getnext()
		if c == "EOT":
			return "EOT"
		return key
		
	def parse_value():
		nonlocal c
		value=""
		getnext()
		while c != "EOT" and c != "}":
			value += c
			getnext()
		if c == "EOT":
			return "EOT"
		getnext()
		return value.strip()
		
	data = data.strip()
	getnext()
	keys = []
	values = []
	while c != "EOT":
		k = parse_key()
		v = parse_value()
		if k != "EOT" and v != "EOT":
			keys.append(k)
			values.append(v)
	
	return keys, values

def generate_main_index_html(lesson_numbers):
	f = open(r"../index.html", "w")
	f.write("<!DOCTYPE html><html><head><link rel='stylesheet' href='css/font-size.css'/><meta charset='utf-8'/></head><body>")
	for i in lesson_numbers:
		f.write("<a href='lessons/" + str(i) + "/index.html'>Урок " + str(i) + "</a><br><br>")
	f.write("</body></html>")
	f.close()


def pattern_choose_good_answer(filename, title, description, lesson, data, params):
	pre = """
	<!DOCTYPE html>
	<html>
	<head>
	  <meta http-equiv="CONTENT-TYPE" content="text/html; charset=UTF-8">
	  <link rel="stylesheet" href="../../patterns/choose-good-answer/style.css"/>
	  <title>2 склонение</title>
	</head>
	<body>
	  <select id="select_lang" onChange="changeLang()">
		<option selected id="select_ru">с русского</optin>
		<option id="select_gr">с древнегреческого</option>
	  </select>
	  <p id="counter">0/0</p>
	  <div id="box">
	   
	  </div>
	"""
	post = """
		</body>
		</html>
	"""

	def convert_to_arr(lines):
		ru = []
		gr = []
		i = 0
		while i < len(lines):
			lines[i] = lines[i].strip()
			if lines[i] != "" and not lines[i].startswith("#"):
				ru.append(lines[i])
				gr.append(lines[i + 1].strip())
				i += 2
			else:
				i += 1

		ru_str = "[ "
		gr_str = "[ "

		for i in range(len(ru)):
			ru_str += f'"{ru[i]}", '
			gr_str += f'"{gr[i]}", '
		ru_str = ru_str[:-2] + " ]"
		gr_str = gr_str[:-2] + " ]"
		return ru_str, gr_str

	# 1 - формируем data.js
	ru = "let ru = [ "
	gr = "let gr = [ "
	word_list = data.split("@")
	for i in word_list:
		ru_str, gr_str = convert_to_arr(i.split("\n"))
		ru += ru_str + ", "
		gr += gr_str + ", "
	ru = ru[:-2] + " ]"
	gr = gr[:-2] + " ]"
	result = ru + "\n" + gr + "\n"
	current_lesson_path = pages_path + r"/" + lesson
	if not os.path.exists(current_lesson_path):
		os.mkdir(current_lesson_path)
	f = open(current_lesson_path + r"/"+filename + ".js", "w")
	f.write(result)
	f.close()
	# формируем .html файл урока
	f = open(current_lesson_path + r"/" + filename + ".html", "w")
	f.write(pre)
	f.write("\t<script src='"+filename+".js'></script>")
	f.write("\t<script src='../../patterns/choose-good-answer/script.js'></script>")
	script = ""
	print(params)
	if "multiword" in params:
		script = "multiword = " + params["multiword"]
	else:
		script = "multiword = false"
	f.write("\t<script>"+script+"</script>")
	f.write(post)
	f.close()

		

		
		
title = ""
description = ""
lesson = ""
pattern = ""
params = {}
data = ""
files = os.listdir(data_path)
lesson_numbers = []
lesson_files = {}
for file in files:
	f = open(data_path+r"/" + file)
	data = f.read()
	f.close()
	keys, values = parse(data)
	for k,v in zip(keys, values):
		if k == "title": title = v
		elif k == "description": description = v
		elif k == "lesson": lesson = v
		elif k == "data": data = v
		elif k == "pattern": pattern = v
		elif k == "params":
			lines = v.split("\n")
			for l in lines:
				entry = l.split("=")
				if len(entry) == 2:
					params[entry[0].strip()] = entry[1].strip()
	if pattern == "choose-good-answer":
		pattern_choose_good_answer(file, title, description, lesson, data, params)
	if int(lesson) not in lesson_numbers:
		lesson_numbers.append(int(lesson))
	if lesson not in lesson_files:
		lesson_files[lesson] = []
	lesson_files[lesson].append(file + ".html")
	lesson_files[lesson].append(title)

print(lesson_files)
# формируем главный index.html
lesson_numbers.sort()
generate_main_index_html(lesson_numbers)

# формируем index.html в каждом уоке
for num in lesson_numbers:
	f = open(pages_path + r"/" + str(num) + "/index.html", "w")
	f.write("<!DOCTYPE html><html><head><link rel='stylesheet' href='../../css/font-size.css'/><meta charset='utf-8'/></head><body>")
	i = 0;
	while i < len(lesson_files[str(num)]):
		f.write("<a href='" + lesson_files[str(num)][i] + "'>" + lesson_files[str(num)][i+1] + "</a><br><br>")
		i += 2
	f.write("</body></html>")
	f.close()
	