import re

# Đọc file template
with open('app/templates/site/order_detail.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Đếm các thẻ
if_count = len(re.findall(r'{%\s*if\s+', content))
elif_count = len(re.findall(r'{%\s*elif\s+', content))  
else_count = len(re.findall(r'{%\s*else\s*%}', content))
endif_count = len(re.findall(r'{%\s*endif\s*%}', content))

print(f'if tags: {if_count}')
print(f'elif tags: {elif_count}')
print(f'else tags: {else_count}')
print(f'endif tags: {endif_count}')
print(f'Cần có {if_count} endif, hiện tại có {endif_count}')

# Kiểm tra cặp thẻ
if if_count == endif_count:
    print('✅ Số lượng if và endif khớp!')
else:
    print('❌ Số lượng if và endif không khớp!')
    
# Kiểm tra từng dòng có vấn đề
lines = content.split('\n')
for i, line in enumerate(lines, 1):
    if 'endif' in line and line.strip().count('{%') > 1:
        print(f'Dòng {i} có thể có vấn đề: {line.strip()}')