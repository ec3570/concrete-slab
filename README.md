# Concrete Slab Design Program

**NOTE:** The program is meant to be used in conjunction with this [textbook](https://www.pearson.com/us/higher-education/program/Aghayere-Reinforced-Concrete-Design-9th-Edition/PGM1654203.html).

This program helps the user design a concrete slab by automating calculations for minimum depth h, k , areas of steel needed, checks for spacing, and directing the user to the correct tables.

Assumptions:
* the slab is a one-way slab
* the loads are uniformly distributed loads
* the cover is assumed to be 3/4 in
* the minimum h is used as h (unless otherwise specified by the user)
* dead load is 0 (unless otherwise specified by the user)
* normal weight conrcrete (150 lb/ft^3) is used (unless otherwise specified by the user)
* #6 bars are used to calculate the estimated effective depth d (unless otherwise specified by the user)
* standard LRFD load factors of: 1.2D + 1.6L
* φ=0.90 (unless otherwise specified by the user)

Inputs:
* span length
* compressive strength of the conrete
* grade of steel reinforcement
* live load
* dead load
* values in which the default values are unwanted (if available)
* values referenced from the tables

Outputs:
* minimum depth h as h (unless otherwise specified by the user)
* k
* areas of steel A_s
* adequacy of bar spacing
* tables to use


## Setup

In order to use the program, you have to clone/download this repository,
navigate to the local directory and create a virtual environment with:

```
$ python3 -m venv venv
```

Then, activate the virtual environment:

```
For Linux/Mac OS:
$ source venv/bin/activate

For Windows:
> venv\Scripts\activate
```

Finally, install the required libraries for this program with:

```
$ pip install -r requirements.txt
```


## How to use the program

<img src="https://i.gyazo.com/2cbbe7b9515a171d9f977cccb72ae7a3.png" alt="Problem 2-30" style="max-height:100px">

Here is how we can deisgn the slab above.

First instantiate a new object of ``ConcreteSlab`` with the respective inputs:

```python
>>> slab=ConcreteSlab(8, 3000, 60000, 300)
```

Next, we calculate k:

```python
>>> slab.k_required()
```

Depth h is 5".

Using Table A-8 with k=0.3277 ksi, ρ was found to be 0.0059.

To find the area of steel needed for the main steel:

```python
>>> slab.main_steel(0.0059)
```

From Table A-4, use #6 bars at 18" on center (A_s=0.29 in^2)

Check the bar spacing for the main steel:
```python
>>> slab.main_steel_spacing(18)
```

&#35;6 bars at 18" on center is inadequate...

Change to #5 bars at 14" on center (A_s=0.27 in^2):

```python
>>> slab.main_steel_spacing(15)
```

The spacing is now adequate.

Calculate effective depth d with the #5 bars:
```python
>>> slab.new_effective_depth(5)
```

Effective depth is 3.94".

To find the area of steel needed for the shrinkage and temperature steel:
```python
>>> slab.st_steel()
```

From Table A-4, use #3 bars at 12" on center (A_s=0.11 in^2).

Check the bar spacing for the shrinkage and temperature steel:
```python
>>> slab.st_steel_spacing(12)
```

Spacing is adequate.

Summary of results:
* h = 5 inches
* d = 3.94 inches
* for main steel, use #5 bars at 14 inches on center
* for shrinkage and temperature steel, use #3 bars at 12" on center

*This specific example is shown in the first portion of test.py.*

*There is a second example using Problem 2-32 in the second portion of test.py.
An image of Problem 2-32 is attached below.*

<img src="https://i.gyazo.com/cb5824277eac0706cd1c3e0a64111ed6.png" alt="Problem 2-32" style="max-height:100px">

## Tables

[Table A-4](https://i.gyazo.com/d62ef75b959586dafc23c8b4ff9fe8e0.png)

[Table A-7 Page 1](https://i.gyazo.com/be917cca7540b963d60e74128c5a88e4.png)

[Table A-7 Page 2](https://i.gyazo.com/1f81faeab24d6015341324b37eb82c4d.png)

[Table A-8](https://i.gyazo.com/bb93230525c796d0e71b02c067e9b39f.png)

[Table A-9 Page 1](https://i.gyazo.com/b40d01b8b60b879e2bc1773b69bb7adb.png)

[Table A-9 Page 2](https://i.gyazo.com/cc52173de9f8dc66e44ca24f41a77e96.png)

[Table A-10 Page 1](https://i.gyazo.com/8b1b52d4bea262ba6dd3713fd551d8c9.png)

[Table A-10 Page 2](https://i.gyazo.com/4d0a0a2614090eab83235f49273d20c7.png)

[Table A-11 Page 1](https://i.gyazo.com/fd9ab9c0bd1f6a5a5795b0b325a44c69.png)

[Table A-11 Page 2](https://i.gyazo.com/5d9b8239d916f8e70b95c33c29a44821.png)
