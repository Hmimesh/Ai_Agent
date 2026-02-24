from functions.get_file_contents import get_file_contents

result1 = get_file_contents("calculator", "lorem.txt")
pass

result2 = get_file_contents("calculator", "main.py")
print(result2)

result3 = get_file_contents("calculator", "pkg/calculator.py")
print(result3)

result4 = get_file_contents("calculator", "/bin/cat")
print(result4)

result5 = get_file_contents("calculator", "pkg/does_not_exist.py")
print(result5)