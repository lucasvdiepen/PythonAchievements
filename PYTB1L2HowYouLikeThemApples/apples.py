import math

trees = 333

shadedTrees = math.ceil((2 / 3) * trees)
sunnyTrees = trees - shadedTrees

shadeOutputModifier = 80

normalTreeOutput = 146

sunnyOutput = sunnyTrees * normalTreeOutput
shadedOutput = ((shadedTrees * normalTreeOutput) / 100) * shadeOutputModifier

totalOutput = sunnyOutput + shadedOutput

owners = 4

eatCount = totalOutput % owners

sellableOutput = totalOutput - eatCount

cut = sellableOutput / owners

print(cut)

