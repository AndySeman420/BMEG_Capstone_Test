
import matplotlib.pyplot as plt
x=[1,3,5,7]
y=[2,4,6,1]
plt.plot(x,y)
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title("A simple line graph")

plt.savefig("Test_Graph.pdf")
plt.show()
