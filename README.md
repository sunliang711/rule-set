## 脚本作用
把clash的yaml文件转成surge的list文件

# 两个脚本
convert.sh的优点是可以保留注释,但是生成的surge规则中要求注释要顶格写!

## convert.py
pip3 install pyyaml
python3 convert.py

## convert.sh
bash convert.sh convert
