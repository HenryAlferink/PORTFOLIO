''' Classes are objects in Python. So, just as all objects have a class that defines their scope,
which class defines the scope of "class"?

Why am I interested in this topic? Because I like understanding how Python works under the hood.
'''

class A:
    pass

a = A()

# the following prints:
# >> <class '__main__.A>
# >> <class 'type'>
#
# so we see that the 'class' object is of type 'type'.
print(type(a))  
print(type(A))   


def add_attribute(self, val):
    self.value = val

# we can actually create a class by using the type function.
# the first arg is the name of the class, the second arg is a list
# of classes to inherit from, and the third arg are the object attributes
B = type('MyClass', (), {
    'attr1': 'hello', 
    'attr2': 'world',
    'add_val_attribute': add_attribute  # can add methods like this
    }
)

b = B()

print()
print(type(b))
print(type(B))

print()
################################
# So, how can we create metaclasses?


class Meta(type):
    # note that the __new__ special dunder method always runs before __init__
    # It can be used to modify the construction of the object.
    def __new__(self, class_name, bases, attrs):
        ''' recall from above: type('class_name', (), {})'''
        print(attrs)

        # this return statement returns the new class
        return type(class_name, bases, attrs)

    def __init__():
        pass


# now if we define a new class and pass it the above metaclass, the __new__
# method will automatically take in the class name, inheritances, and attributes.
class FooClass1(metaclass=Meta):
    ''' As soon as this class is defined (even before it's instantiated!) it will
    run the __new__ method from the metaclass. '''
    x = 1
    y = 2


# So what's an example of what we can do with all of this?
# We can use a metaclass to automatically set all the class attributes to have 
# a '__' before them. 

print()

# let's add this functionality to the __new__ method:
def updated__new__(self, class_name, bases, attr):
    print('attr before: {}'.format(attr))
    
    new_attr = {}
    for name, value in attr.items():
        new_attr["__" + name] = value
    
    print('attr after: {}'.format(new_attr))

    return type(class_name, bases, new_attr)

Meta.__new__ = updated__new__


class FooClass2(metaclass=Meta):
    x = 1
    y = 2


# print(FooClass2.x)  # this returns an error
print(FooClass2.__x)  # this one works!