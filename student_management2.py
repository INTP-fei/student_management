import json
import os
# json 模块：用于处理 JSON 数据的读取和写入，可以将数据保存为 JSON 格式（易于存储和交换）。
# os 模块：用于与操作系统交互，这里用它来检查文件是否存在。

DATA_FILE = 'data.json' 
#加载数据
def load_data():
    """
    如果数据文件不存在，则返回一个包含空用户列表和空学生列表的字典
    如果文件存在，则读取并解析JSON文件内容
    """
    # 检查数据文件是否存在
    if not os.path.exists(DATA_FILE): # os.path.exists(path)函数，检查指定的路径（path）所对应的文件或者目录是否存在。
        return {'users': [], 'students': []}
    # 以只读模式打开数据文件，使用UTF-8编码
    with open(DATA_FILE, 'r', encoding='utf-8') as f:# 将打开的文件对象赋值给变量 f
        # 解析JSON文件内容并返回
        return json.load(f)# json.load()函数将JSON格式的数据解析为Python对象。
# 保存数据到文件
def save_data(data):
    """
    将数据以JSON格式写入数据文件，确保非ASCII字符正确显示，使用4个空格缩进
    """
    # 以写入模式打开数据文件，使用UTF-8编码
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        # 将数据以JSON格式写入文件
        json.dump(data, f, ensure_ascii=False, indent=4)
    # json.dump() 用于把 Python 对象（如字典、列表等）转换为 JSON 字符串，然后将这个字符串写入指定的文件对象。
    # ensure_ascii=False 确保中文字符不会被转义
    # 每行缩进 indent 个空格
#用户注册
def register():
    """
    用户注册功能
    提示用户输入用户名、密码和角色，进行必要的验证，然后将用户信息添加到数据中并保存
    """
    # 加载数据
    data = load_data()
  
    print("\n--- 注册 ---")
    # 提示用户输入用户名
    username = input("请输入用户名: ")
    # 提示用户输入密码
    password = input("请输入密码: ")
    # 提示用户选择角色，并将输入转换为小写
    role = input("请选择角色 (teacher/student): ").lower()

    # 检查用户名是否已经存在
    if any(u['username'] == username for u in data['users']): # 一个生成器表达式
        print("用户名已存在!")
        return
    """
    any() 函数会遍历可迭代对象中的每个元素，如果其中有任何一个元素的值为 True，则返回 True；
    只有当所有元素的值都为 False 时，才返回 False。
    u 是在遍历 data['users'] 列表时，代表列表中每个用户信息字典的临时变量。
    总体：检查 data['users'] 列表中是否存在某个用户的用户名和传入的 username 相同。
    """

    # 学生角色需要验证学号
    student_id = None #不管是学生还是老师首先默认学号不存在，这样老师就不用输入学号了
    if role == 'student':
        # 提示学生输入学号
        student_id = input("请输入你的学号: ")
        # 检查学号是否存在
        if not any(s['id'] == student_id for s in data['students']):
            print("该学号不存在，请联系教师注册!")
            return

    # 创建用户信息字典
    user = {
        'username': username,
        'password': password,
        'role': role,
        'student_id': student_id
    }
    # 将用户信息添加到用户列表中
    data['users'].append(user)
    # 保存更新后的数据
    save_data(data)
    print("注册成功!")
#   用户登录功能
def login():
    """
    提示用户输入用户名和密码，验证用户信息，若验证通过则返回用户信息，否则提示错误
    """
    # 加载数据
    data = load_data()
  
    print("\n--- 登录 ---")
    # 提示用户输入用户名
    username = input("用户名: ")
    # 提示用户输入密码
    password = input("密码: ")

    # 查找匹配的用户信息
    user = next((u for u in data['users'] if u['username'] == username and u['password'] == password), None)
    #next(iterator, default)一个迭代器对象，默认值设置为 None。
    if user:
        print(f"登录成功! 欢迎 {username} ({user['role']})")
        return user
    else:
        print("用户名或密码错误!")
        return None
    
#教师功能菜单
def teacher_menu():
    """
    提供添加学生、删除学生、修改学生信息、查看所有学生和退出等功能
    """
    # 加载数据
    data = load_data()
  
    while True:
        print("\n--- 教师菜单 ---")
        print("1. 添加学生")
        print("2. 删除学生")
        print("3. 修改学生信息")
        print("4. 查看所有学生")
        print("5. 退出")
      
        # 提示教师选择操作
        choice = input("请选择操作: ")
      
        if choice == '1':
            # 创建学生信息字典
            student = {
                'id': input("学号: "),
                'name': input("姓名: "),
                'class': input("班级: "),
                'age': input("年龄: "),
                'score': input("成绩: ")
            }
          
            # 检查学号是否已经存在
            if any(s['id'] == student['id'] for s in data['students']):
                print("该学号已存在!")
                continue
              
            # 将学生信息添加到学生列表中
            data['students'].append(student)
            # 保存更新后的数据
            save_data(data)
            print("学生添加成功!")
          
        elif choice == '2':
            # 提示教师输入要删除的学生学号
            student_id = input("请输入要删除的学号: ")
            # 过滤掉要删除的学生信息
            data['students'] = [s for s in data['students'] if s['id'] != student_id]
            # 过滤掉与要删除学生关联的用户信息
            data['users'] = [u for u in data['users'] if u.get('student_id') != student_id]
            #get()方法用于返回字典中指定的键对应的值，如果键不存在，则返回指定的默认值。
            # 保存更新后的数据
            save_data(data)
            print("删除成功!" if len(data['students']) else "未找到该学生")
          
        elif choice == '3':
            # 提示教师输入要修改的学生学号
            student_id = input("请输入要修改的学号: ")
            # 查找要修改的学生信息
            student = next((s for s in data['students'] if s['id'] == student_id), None)
          
            if student:
                print(f"当前信息: {student}")
                # 提示教师输入新的学生信息，若不输入则使用原信息
                student['name'] = input(f"新姓名 ({student['name']}): ") or student['name']
                student['class'] = input(f"新班级 ({student['class']}): ") or student['class']
                student['age'] = input(f"新年龄 ({student['age']}): ") or student['age']
                student['score'] = input(f"新成绩 ({student['score']}): ") or student['score']
                # 保存更新后的数据
                save_data(data)
                print("修改成功!")
            else:
                print("未找到该学生")
        elif choice == '4':
            print("\n--- 学生列表 ---")
            # 遍历学生列表并打印学生信息
            for student in data['students']:
                print(f"学号: {student['id']} | 姓名: {student['name']} | 班级: {student['class']} |年龄: {student['age']} | 成绩: {student['score']}")
              
        elif choice == '5':
            break
          
        else:
            print("无效的选项!")
#学生功能菜单
def student_menu(student_id):
    """
    提供查看学生自身信息和退出等功能
    """
    # 加载数据
    data = load_data()
  
    while True:
        print("\n--- 学生菜单 ---")
        print("1. 查看我的信息")
        print("2. 退出")
      
        # 提示学生选择操作
        choice = input("请选择操作: ")
      
        if choice == '1':
            # 查找学生自身信息
            student = next((s for s in data['students'] if s['id'] == student_id), None)
            if student:
                print("\n--- 我的信息 ---")
                print(f"学号: {student['id']}")
                print(f"姓名: {student['name']}")
                print(f"班级: {student['class']}")
                print(f"年龄: {student['age']}")
                print(f"成绩: {student['score']}")
            else:
                print("未找到学生信息!")
              
        elif choice == '2':
            break
          
        else:
            print("无效的选项!")

def main():
    """
    主程序
    提供注册、登录和退出等功能，根据用户角色显示不同的菜单
    """
    while True:
        print("\n=== 学生管理系统 ===")
        print("1. 注册")
        print("2. 登录")
        print("3. 退出")
      
        # 提示用户选择操作
        choice = input("请选择操作: ")
      
        if choice == '1':
            # 调用注册功能
            register()
        elif choice == '2':
            # 调用登录功能
            user = login()
            if user:
                if user['role'] == 'teacher':
                    # 教师角色调用教师菜单
                    teacher_menu()
                else:
                    # 学生角色调用学生菜单
                    student_menu(user['student_id'])
        elif choice == '3':
            print("感谢使用，再见!")
            break
        else:
            print("无效的选项!")

if __name__ == '__main__':
    # 程序入口，调用主程序
    main()