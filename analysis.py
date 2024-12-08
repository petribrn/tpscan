import json

with open('./output_data.json', 'r') as file:
  file_content = json.loads(file.read())
  del file_content['access_points']['url']
  del file_content['switches']['url']
  del file_content['routers']['url']
  del file_content['controllers']['url']

total_products = 0
total_attributes = 0

for key in file_content:
  for i in file_content[key]:
    products = file_content[key][i]['products']
    for p in products:
      for j in p.keys():
        if len(p[j]) < 1 or (type(p[j]) == list and not all(p[j])): # remove empty strings and arrays containing only empty strings
          continue
        total_attributes += 1 if type(p[j]) != list else len(p[j])
    total_products += len(products)

print(f'\nQuantidade de produtos: {total_products}')
print(f'Quantidade de atributos coletados com sucesso: {total_attributes}\n')
