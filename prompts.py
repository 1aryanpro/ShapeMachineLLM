

def combinator(inputs, output):
	return [(inp, output) for inp in inputs]

def lookupPrompt(shape):
	inputs = [
		f"Create a ShapeMachine rule that counts the number of {shape}s.",
    	f"How do I count the number of {shape}s using ShapeMachine?",
		f"I want to use shape machine to count the number of {shape}s in my drawing."
	]

	output = f"To count the number of a shape, we have to create a rule that transforms a shape to itself. This will allow us to not make any modifcations to the drawing but still count the number of matches to the rule we find. In this case with want to find the number of istances of {shape} so we will have 1 {shape} on both the left and right hand side."

	return combinator(inputs, output)



def conversionPrompt(shape1, shape2):
	if shape1 == shape2: return lookupPrompt(shape1)

	inputs = [
		f"Create a ShapeMachine rule that coverts all {shape1}s into {shape2}s",
		f"How do I use ShapeMachine to convert all {shape1}s into {shape2}s?"
	]

	output = f"To convert one shape into another shape we have to create a rule that has the input shape on the left side and the output shape on the right side. In this case, we want to convert all {shape1} to {shape2} so the left hand side will contain a {shape1} and the right hand side will contain a {shape2}."
	return combinator(inputs, output)

def rotationPrompt(shape, deg):
	inputs = [
		f"Create a ShapeMachine rule that rotates a {shape} by {deg} degrees.",
		f"How do I use ShapeMachine to rotate all {shape}s by {deg} degrees?"
	]

	output = f"To roate a shape we have to create a rule that has the input shape on the left side and a rotated version of that shape on the right side. In this case, we want to rotate all {shape}s by {deg} degrees, so the left hand side will contain a {shape} and the right hand side will contain the {shape} rotated by {deg} degrees."

	return combinator(inputs, output)

def deletePrompt(shape):
	inputs = [
		f"Create a ShapeMachine rule that deletes all {shape}s.",
		f"How do I use ShapeMachine to delete all the {shape}s in my drawing?"
	]

	output = f"Since we want to delete a specific object, we should make a rule with the object on the left side and nothing on the right side, this will effectively delete object in question. In this case we want to delete all {shape} so we will put a {shape} on the left side and nothing on the right side."
	
	return combinator(inputs, output)

def duplicationPrompt(shape, dir):

	particple = 'below' if dir == 'down' else 'to the right of'

	inputs = [
		f"Create a ShapeMachine rule that duplicates all {shape}s {'down' if dir == 'down' else 'to the right'}.",
		f"How do I create a ShapeMachine rule that duplicates all {shape}s {dir}."
	]

	output = f"Since we want to duplicate something, that requires us to have one copy of the object on the left side of the rule, and two copies of the object on the right side of the rule. Here we want to duplicate {dir} so the new copy should be {particple} the original one. The object in question in here is a {shape}. So the left hand side will contain one {shape} and the right hand side will contain two {shape}s with the new one {particple} the original."

	return combinator(inputs, output)