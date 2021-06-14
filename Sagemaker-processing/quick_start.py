# Vehicle Routing Problem with Time Window

from flowty import Model, xsum
from or_datasets import vrp_rep

bunch = vrp_rep.fetch_vrp_rep("solomon-1987-r1", instance="R102_025")
name, n, E, c, d, Q, t, a, b, x, y = bunch["instance"]

m = Model()

# one graph, it is identical for all vehicles
g = m.addGraph(obj=c, edges=E, source=0, sink=n - 1, L=1, U=n - 2, type="B")

# adds resources variables to the graph.
# travel time and customer tine windows
m.addResourceDisposable(
    graph=g, consumptionType="E", weight=t, boundsType="V", lb=a, ub=b, name="t"
)

# demand and capacity
m.addResourceDisposable(
    graph=g, consumptionType="V", weight=d, boundsType="V", lb=0, ub=Q, name="d"
)

# set partition constriants
for i in range(n)[1:-1]:
    m += xsum(x * 1 for x in g.vars if i == x.source) == 1

# packing set
for i in range(n)[1:-1]:
    m.addPackingSet([x for x in g.vars if i == x.source])

status = m.optimize()
print(f"ObjectiveValue {m.objectiveValue}")

# get the variable values
for var in m.vars:
    if var.x > 0:
        print(f"{var.name} = {var.x}")

import math
import networkx
import matplotlib
import matplotlib.pyplot as plt

edges = [x.edge for x in g.vars if not math.isclose(x.x, 0, abs_tol=0.001)]
gx = networkx.DiGraph()
gx.add_nodes_from([i for i in range(n)])
gx.add_edges_from(edges)
pos = {i: (x[i], y[i]) for i in range(n)} # for lists of x,y coordinates
# pos = networkx.spring_layout(gx) # alternative layout
networkx.draw_networkx_nodes(gx, pos, nodelist=gx.nodes)
networkx.draw_networkx_labels(gx, pos, labels={i: i for i in gx.nodes})
networkx.draw_networkx_edges(gx, pos, nodelist=gx.edges)
#plt.show() # if gui backend is supported
#plt.savefig("mygraph.png")

### output variable_values as json file in s3 bucket subfolder###
import json
#create dict populate dict
variable_values = {}
for var in m.vars:
    if var.x > 0:
        variable_values[var.name] = var.x

data = {"objective value":m.objectiveValue, "variable values":variable_values}

#save dict
with open(name+'.json', 'w') as fp:
    json.dump(data, fp, indent=4)

#upload json object to s3 bucket in output subfolder
bucket_name = "flowty-sagemaker"
key = name+".json"  #filename

s3_client = s3.boto3.client('s3')

s3_client.put_object(
     Body=str(json.dumps(data, indent=4)),
     Bucket=bucket_name,
     Key="output/"+key
)