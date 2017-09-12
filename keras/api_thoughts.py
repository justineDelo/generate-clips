
''' Simple model with 2 branches merging into one

    left   right
      |      |
       \    /
        model
          |
'''

left = Sequential()
left.add(Dense(10, 64))
left.add(Dense(10, 64))

right = Sequential()
right.add(Dense(20, 64))

model = Merge([left, right], merge_mode="concat", concat_dim=-1)
model.add(Dense(128, 64))
model.compile(optimizer, objective)

model.fit([Xleft, Xright], y)


''' Recursivity of Merge structures

    left   right
      |      |
       \    /    
    intermediate
         |       far_right
          \       /
            model
              |
'''

left = Sequential()
left.add(Dense(10, 64))
left.add(Dense(10, 64))

right = Sequential()
right.add(Dense(20, 64))

intermediate = Merge([left, right], merge_mode="concat", concat_dim=-1)
intermediate.add(Dense(128, 128))

far_right = Sequential()
far_right.add(Embedding(10000, 128))

model = Merge([intermediate, far_right], merge_mode="sum")
model.add(Dense(128, 10))
model.compile(optimizer, objective)

model.fit([[Xleft, Xright], Xembed], y)


''' Simple model with one sequence branching into 2

            model
            /   \
        two_head_model
            |   |
'''

model = Sequential()
model.add(Dense(10, 128))

two_headed_model = Fork(n=2)
two_headed_model.add(Dense(128, 64), position=0)
two_headed_model.add(Dense(128, 1), position=1)

two_headed_model.compile(optimizer, objective)

two_headed_model.fit(X, [y1, y2])


''' "Adding" models
'''

model = Sequential()
model.add(Dense(10, 128))

upper_section = Sequential()
upper_section.add(Dense(128, 256))

model.add(upper_section)
model.compile(optimizer, objective)
model.fit(X, y)

