query = str(input("Enter a query (enter blank if you want to quit): "))

while query != "":
  hits_matrix = eval(rewrite_query(query))
else:
  print("Goodbye!")
  
