import geo,numpy as np

x_axis_unit = (1, 0, 0)
y_axis_unit = (0, 1, 0)
z_axis_unit = (0, 0, 1)
r1 = geo.axisangle_to_q(x_axis_unit, np.radians(90) ) #90 deg
r2 = geo.axisangle_to_q(y_axis_unit, np.radians(180) ) #180deg
#r3 = axisangle_to_q(z_axis_unit, numpy.pi / 2)

v = geo.qv_mult(r1, x_axis_unit) #start with x vector?
v = geo.qv_mult(r2, v)
#v = qv_mult(r3, v)

print(v)

r = geo.q_mult(r1,r2)
v = geo.qv_mult(r, x_axis_unit)

print(r,v)

r1 = geo.axisangle_to_q(x_axis_unit, np.radians(90) ) #90 deg
r2 = geo.axisangle_to_q(y_axis_unit, np.radians(-180) ) #180deg

r = geo.q_mult(r1,r2)
v = geo.qv_mult(r, x_axis_unit)

print(r,v)
