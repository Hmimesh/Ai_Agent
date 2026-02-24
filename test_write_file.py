from functions.write_in_file import write_file

result1 = write_file("calculator", "lorem.txt", "wait, this isent lorem ipsum")
print(result1)

result2 = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
print(result2)

result3 = write_file("calculator", "/tmp/temp.txt", "this shouldnt be allowed")
print(result3)