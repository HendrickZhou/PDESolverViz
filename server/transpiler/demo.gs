MODE:2D 

%%
#import ./json/demo.json as mod
#e_import = mod.test_element

e1 = Rectangle(
    [0,0],
    [1,1]
)

e2 = Disk(
    [0,0],
    1
)

e1

ei1 = Interval(0,1)
ei2 = Interval(0.5, 1.5)
eix = ei1 - ei2
eixx = eix - ei2
ey = eixx & eix

e = union(e1, e2) 
result = e & e1

%%
build(result)