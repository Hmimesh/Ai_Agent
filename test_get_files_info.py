from functions.get_files_info import get_files_info

result1 = get_files_info("calculator", ".")
print("result for current directrory:")
print(result1)

result2 = get_files_info("calculator", "pkg")
print("result for current directrory:")
print(result2)

result3 = get_files_info("calculator", "/bin")
print("result for current directrory:")
print(result3)

result4 = get_files_info("calculator", "../")
print("result for current directrory:")
print(result4)


