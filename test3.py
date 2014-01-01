from PythonMagick import Image
#Image("clipboard:").write("IMG_0233.PNG")  # clipboard -> file
Image("IMG_0233.PNG").write("clipboard:")  # file -> clipboard
