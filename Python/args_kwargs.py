# 16 May 2020
# Nishant Tharani
# Playing around with args and kwargs in the context of function decorating

import sys
import traceback


###################### *args doesn't handle keyword arguments #############################
def f_args_only(*args):
    print(args)


try:
    # TypeError because *args doesn't handle keyword arguments
    f_args_only(0, 1, 2, x=42)
except TypeError:
    print("f_args_only only accepts *args, but that doesn't handle keyword arguments")
    print("Type error exception raised by f_args_only:")
    print("-"*70)
    traceback.print_exc(file=sys.stdout)
    print("-"*70)
    print()


####################### but **kwargs does ###########################
def f_args_kwargs(*args, **kwargs):
    print(args)
    print(kwargs)


# Prints (0,1,2) and {'x': 42}
print("If we add **kwargs as a parameter, it works:")
f_args_kwargs(0, 1, 2, x=42)
print()


############################### A decorator which returns nothing... #########################
def d_empty(func):
    pass

# ... Leads to f_empty being a None type object
@d_empty
def f_empty(*args, **kwargs):
    print(args)
    print(kwargs)


try:
    # TypeError raised as f_empty is now a None type object
    f_empty(0, 1, 2, x=42)
except TypeError:
    print("Now if we use a decorator that does nothing on f, f becomes None type")
    print("Type error exception raised by f_empty:")
    print("-"*70)
    traceback.print_exc(file=sys.stdout)
    print("-"*70)
    print()


##################### Adding a wrapper function that does nothing... ################
def d_empty_wrapper(func):
    def w():
        pass
    pass

# Doesn't change anything
@d_empty_wrapper
def f_empty_wrapper(*args, **kwargs):
    print(args)
    print(kwargs)


try:
    # TypeError raised as f_empty_wrapper is still a None type object
    f_empty_wrapper(0, 1, 2, x=42)
except TypeError:
    print("If we add an empty wrapper, f is still None type")
    print("Type error exception raised by f_empty_wrapper:")
    print("-"*70)
    traceback.print_exc(file=sys.stdout)
    print("-"*70)
    print()

###################### Even if that wrapper function runs correctly, we still need to return it #############


def d_empty_wrapper_a(func):
    def w(*args, **kwargs):
        func(*args, **kwargs)
    pass

# f_empty_wrapper_a still is a None object here
@d_empty_wrapper_a
def f_empty_wrapper_a(*args, **kwargs):
    print(args)
    print(kwargs)


try:
    # TypeError raised as f_empty_wrapper_a is still a None type object
    f_empty_wrapper_a(0, 1, 2, x=42)
except TypeError:
    print("Even if that wrapper does its job internally, with nothing returned by the decorator, f is still None type")
    print("Type error exception raised by f_empty_wrapper_a:")
    print("-"*70)
    traceback.print_exc(file=sys.stdout)
    print("-"*70)
    print()


#################### Once we actually return the wrapper function, decoration works ############

def d_wrapped(func):
    def w(*args, **kwargs):
        func(*args, **kwargs)
    return w

# f_wrapped works now
@d_wrapped
def f_wrapped(*args, **kwargs):
    print(args)
    print(kwargs)


print("Once we actually return the wrapper function from the decorator, decoration works")
f_wrapped(0, 1, 2, x=42)
print()

######## If f stops accepting *args, our wrapper function still tries to pass them and it doesn't work #########
@d_wrapped
def f_no_args(**kwargs):
    print(kwargs)


try:
    f_no_args(0, 1, 2, x=42)
except TypeError:
    print("If f stops accepting *args, our wrapper function still gets called but then calling f from inside it throws an error")
    print("Type error exception raised by f_no_args:")
    print("-"*70)
    traceback.print_exc(file=sys.stdout)
    print("-"*70)
    print()

###### And if our wrapper function doesn't accept them either then the error is thrown by w, not f ######


def d_wrapped_no_args(func):
    def w():
        func()
    return w

# f_wrapped works now
@d_wrapped_no_args
def f_no_args_a():
    print("f runs but does nothing")


try:
    f_no_args_a(0, 1, 2, x=42)
except TypeError:
    print("And if our wrapper function doesn't accept them either, then the error is thrown by the wrapper function itself")
    print("Type error exception raised by f_no_args_a:")
    print("-"*70)
    traceback.print_exc(file=sys.stdout)
    print("-"*70)
    print()
