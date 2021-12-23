
import fp

@fp.curry
def create_board(dimensions, mapping_fn):
  return fp.head(dimensions).chain(
    lambda x_size: fp.second(dimensions).map(fp.flow(
      fp.fill(x_size), 
      fp.map(fp.fillWithIndex)
    )
  )).map(fp.withIndex)


@fp.curry
def add(a,b):
  return a + b


print(create_board(fp.Array(3, 5), print))