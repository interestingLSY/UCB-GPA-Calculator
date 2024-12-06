import os, sys, dataclasses, re, math

raw_data = """

23-24学年度2学期
+	计算机图形学	Computer Graphics	任选	3	91	3.85
+	计算机组织与体系结构	Computer Architectures	专业必修	3	93	3.91
+	编译原理	Compiler Principles	专业必修	4	95	3.95
-	信息科学技术劳动实践	Labor Practice for Electronics Engineering and Computer Science	任选	2	合格	
+	计算机组织与体系结构实习	Lab on Computer Organization and Architecture	限选	2	100	4

23-24学年度1学期
+	软件工程	Software Engineering	专业必修	4	96	3.97
+	人工智能中的编程	Programming in Artificial Intelligence	任选	3	100	4
+	高层次芯片设计	Chip Design using High-level Programming Language	任选	3	99	4
-	游泳	Swimming	全校必修	1	90	3.81
+	计算机网络	Computer Networks	专业必修	4	93.5	3.92
-	新时代劳动者十讲	Ten Talks on New Era Workers	全校任选	0	合格	

22-23学年度2学期
+	前沿计算研究实践（II）	Study and Practice on Topics of Frontier Computing (II)	专业必修	3	97	3.98
+	算法设计与分析（实验班）	Algorithm Design and Analysis (Honor Track)	专业必修	5	98	3.99
+	并行与分布式计算导论	Introduction to Parallel and Distributed Computing	全校任选	3	98.5	4
+	操作系统（实验班）	Operating Systems (Honor Track)	全校任选	4	94	3.93
+	JavaScript语言Web程序设计	JavaScript Web Programming	全校任选	2	98	3.99

22-23学年度1学期
-	数学分析 (III)	Mathematical Analysis (III)	专业必修	4	92	3.88
-	离散数学与结构（I）	Discrete Mathematics and Structures (I)	专业必修	3	93	3.91
+	数据结构与算法 (A) (实验班)	Data Structure and Algorithms(A)(Honor Track)	全校必修	3	96	3.97
-	新时代劳动理论	Labor Theory	全校任选	1	合格	
-	实用英语：从听说到演讲	Practical English Skills: From Listening to Public Speaking	全校任选	2	合格	
-	经济学原理	Principles of Economics	全校必修	4	94	3.93
+	前沿计算研究实践（I）	Study and Practice on Topics of Frontier Computing(I)	专业必修	3	99	4
+	计算机系统导论	Introduction to Computer Systems	专业必修	5	97	3.98

21-22学年度2学期
+	电子系统基础训练	Basic training of Electronics system	任选	1	93	3.91
+	程序设计实习	Practice of Programming in C&C++	专业必修	3	99	4
-	数学分析（II）	Mathematical Analysis (II)	专业必修	5	85	3.58
+	人工智能引论	Introduction to Artificial Intelligence	专业必修	3	93	3.91
+	Rust程序设计	Programming in Rust	全校任选	2	99.5	4
+	微电子与电路基础	An Introduction to Microelectronics and Circuits	任选	2	合格	
-	中国近现代史纲要	Outline of Chinese Modern History	全校必修	3	合格	
-	习近平新时代中国特色社会主义思想概论	Introduction to Xi Jinping Thought on Socialism with Chinese Characteristics for a New Era	全校必修	2	合格	
-	思想政治实践（下）	Social practice and service learning, Part II	全校必修	1	合格	

21-22学年度1学期
-	形势与政策	Events and Policies	全校必修	2	合格	
-	思想政治实践（上）	Social practice and service learning, Part I	全校必修	1	合格	
+	信息科学技术概论	Introduction to Information Science and Technique	专业必修	1	合格	
-	柔道	JUDO	全校任选	1	80	3.25
-	军事理论	Military Theory	全校任选	2	85	3.58
-	思想道德修养与法律基础	An Introduction to Ideological & Moral Culture and Laws	全校必修	3	86	3.63
-	地震概论	Introduction to Seismology	全校必修	2	95	3.95
-	数学分析（I）	Mathematical Analysis (I)	专业必修	5	80	3.25
-	信息科学中的物理学（上）	Physics for Information Sciences (1)	任选	3	93	3.91
-	高等代数（I）	Advanced Algebra (I)	专业必修	5	93	3.91
+	计算概论A（实验班）	Introduction to Computing (A) (Honor Track)	全校必修	3	92	3.88
"""

@dataclasses.dataclass
class Course:
	name: str
	score: float
	credit: float
	semester: int	# 1 ~ 6
	is_critical_course: bool

def process_raw_data(raw_data: str) -> list[Course]:
	re1 = re.compile(r'(\d{2})-(\d{2})学年度(\d)学期')
	cur_semester = -1
	result = []
	for line in raw_data.split('\n'):
		line = line.strip()
		if line == '':
			# Empty line
			continue
		elif re1.match(line):
			# Semester line
			cur_semester = (int(line[0:2]) - 21)*2 + int(line[8])
			# print(line, cur_semester)
		elif line.endswith('合格'):
			# P/F course
			assert cur_semester != -1
			continue
		else:
			components = line.split('\t')
			assert len(components) == 7
			assert cur_semester != -1
			assert components[0] in ['+', '-']
			result.append(Course(
				name=components[0],
				score=float(components[-2]),
				credit=float(components[-3]),
				semester=cur_semester,
				is_critical_course=components[0] == '+'
			))
	
	return result

def calculate_gpa(courses: list[Course]) -> float:
	def score2gpa(x):
		# It seems that PKU's system round the GPA of each course to 2 decimal places
		# for the final GPA calculation, so we do the same here
		# However, I'm not really sure about this
		return 0 if x < 60 else round(4 - 3*(100-x)**2 / 1600, 2)
	total_credits = sum(course.credit for course in courses)
	total_gpa = sum(course.credit * score2gpa(course.score) for course in courses)
	return total_gpa / total_credits

if __name__ == '__main__':
	courses = process_raw_data(raw_data)

	print(f"Total GPA: {calculate_gpa(courses):.6f}")
	print(f"Junior year GPA: {calculate_gpa([course for course in courses if course.semester in [5, 6]]):.6f}")
	print(f"Major course GPA: {calculate_gpa([course for course in courses if course.is_critical_course]):.6f}")
	