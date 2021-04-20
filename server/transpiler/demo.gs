MODE:2D 

%%
#import ./json/demo.json as mod
#e_import = mod.test_element

e1 = Rect(
)
e2 = Circle(
    {
    }
)

scale(e1, 1.1)
move(e2, [1,0])
mirror(e1)

result = diff(e1, e2)

%%
build result
# save e1