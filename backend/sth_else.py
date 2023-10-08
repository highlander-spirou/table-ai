from networkx import DiGraph

a = DiGraph()


print('before', len(a.nodes))

a.add_node('a')

print('after', len(a.nodes))