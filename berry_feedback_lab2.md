# Berry's feedback Lab 2

## if (x) { y = true } else { y = false }

Maybe it's a pet peeve, but I try to avoid any kind of if/else statement where I end up setting the same variable to true or false on separate branches. Usually you can just assign the value based on the evaluation of a boolean expression. For example:

```
    def set_special():
        """Ask the user if the password should use special characters"""
        while True:
            special = input("Use special characters? (y/n) ").lower()
            if (special in ['y','n']):
                options["special"] = (special == 'y')
                break
            else:
                print("'y' or 'n' only.")
```

That ends up being fewer lines, and arguably more complex. But I think it's also simpler once you know what you're looking at.

## Separate concerns

You also do the same job (poll the user multiple times in the same manner). I would extract out the job of polling the user for a y/n input into a utility function, and pass in the prompt and then return the value and assign it where you want in the function that calls it.

```
    def set_lowercase():
        """Ask the user if the password should use lowercase characters"""
        options["lower"] = _prompt_yn("Use lowercase letters?")

    def set_numbers():
        """Ask the user if the password should use numbers"""
        options["numbers"] = _prompt_yn("Use numbers?")

    def _prompt_yn(prompt: string) -> bool:
         while True:
            result = input(prompt + " (y/n) ").lower()
            if (result in ['y','n']):
                return (result == 'y')
            else:
                print("'y' or 'n' only.")
```

## Smelly stringify

The part where you stringify something and then split the string and parse it make me curious if there wasn't a better way...

Dropped into a repl, and did a `dir` on the result of that operation:

```
>>> dir(datetime.date(2025, 7, 4) - datetime.date.today())
['__abs__', '__add__', '__bool__', '__class__', '__delattr__', '__dir__', '__divmod__', '__doc__', '__eq__', '__floordiv__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__mod__', '__mul__', '__ne__', '__neg__', '__new__', '__pos__', '__radd__', '__rdivmod__', '__reduce__', '__reduce_ex__', '__repr__', '__rfloordiv__', '__rmod__', '__rmul__', '__rsub__', '__rtruediv__', '__setattr__', '__sizeof__', '__str__', '__sub__', '__subclasshook__', '__truediv__', 'days', 'max', 'microseconds', 'min', 'resolution', 'seconds', 'total_seconds']
```

Huh, `days`, what does that do?

```
>>> (datetime.date(2025, 7, 4) - datetime.date.today()).days
1553
```

Nifty.

```
        date_delta = (datetime.date(2025, 7, 4) - datetime.date.today()).days
```

## Line break style

Very much a personal thing, but I find if you have to break an expression into more than one line, it's often better to do more than two lines, so you can scan the different parts of the expression. Ex:

```
            side_c = math.sqrt(
                (side_a * side_a) 
                + (side_b * side_b) 
                - (2 * side_a * side_b * math.cos(math.radians(angle_c)))
            )
```

Note the opening brace on its own line, and the closing brace on its own line as well, left-aligned with the line where the block was opened. In this way it's very easy to see where the pieces begin and end. This even nests well:

```
            side_c = math.sqrt(
                (side_a * side_a) 
                + (side_b * side_b) 
                - (
                    2 
                    * side_a 
                    * side_b 
                    * math.cos(math.radians(angle_c))
                )
            )
```

Or taking it to the point of absurdity

```
 side_c = math.sqrt(
            (side_a * side_a) 
            + (side_b * side_b) 
            - (
                2 
                * side_a 
                * side_b 
                * math.cos(
                    math.radians(angle_c)
                )
            )
        ) 
```


Especially for complicated lines, it's also not a bad thing to have things broken out over multiple lines like this for git diffing. This way you can see which part of the complex expression a given commit changed, instead of just knowing that it was one of the three or four things on a single line.

## Internal methods

In Python, methods with __ before and after them are generally not meant to be used by external code. For example, you call \_\_round__ on a few floats, but the "Python way" of doing this is to call the `round` function on that float:

```

round(volume, 2)

```
instead of

```

volume.__round__(2)

```
## Breaking long lines
Generally, when breaking long lines to meet a line length requirement, rather than just breaking it in the middle, I tend to try to break the line down into components, usually named variables that help to simplify what's being done at each step and label them.

Also, I tend to try not to do too many things at a time in a line of code. If if I have to do math and then print out the result, I want to do the math on one line, and do the printing on a second line. They are fundamentally two different operations and combining them just makes everything harder to follow.

For example, this line


```
 return "\nPercentage:\t" + \
            str((numerator / denominator * 100).__round__(decimal_spaces)) + "%\n" 
```

I would refactor to


```
 percentage = str(round((numerator / denominator * 100), decimal_spaces))
        return ("\nPercentage:\t" + percentage + "%\n") 
```
