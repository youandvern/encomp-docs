.. _examples:

Calculation Object Examples
===========================

This section will show fully featured examples of each object type with the resulting calculation 
report and design portal view.

Examples Of Each object
-----------------------

Assumption
~~~~~~~~~~

Code Example:

.. image:: /_static/examples/assumption_code.png
    :scale: 40%
    :alt: Examples of creating the assumption object in code
    :align: center

Calculation Report:

.. image:: /_static/examples/assumption_report.png
    :scale: 40%
    :alt: Examples of the assumption object in the calculation report
    :align: center

Design Portal: Not Displayed


Calculation
~~~~~~~~~~~

Code Example:

.. image:: /_static/examples/calculation_code.png
    :scale: 40%
    :alt: Examples of creating the calculation object in code
    :align: center

Calculation Report:

.. image:: /_static/examples/calculation_report.png
    :scale: 40%
    :alt: Examples of the calculation object in the calculation report
    :align: center

Design Portal:

.. image:: /_static/examples/calculation_design.png
    :scale: 40%
    :alt: Examples of the calculation object in the design portal
    :align: center


Comparison
~~~~~~~~~~

Code Example:

.. image:: /_static/examples/comparison_code.png
    :scale: 40%
    :alt: Examples of creating the comparison object in code
    :align: center

Calculation Report:

.. image:: /_static/examples/comparison_report.png
    :scale: 40%
    :alt: Examples of the comparison object in the calculation report
    :align: center

Design Portal:

.. image:: /_static/examples/comparison_design.png
    :scale: 40%
    :alt: Examples of the comparison object in the design portal
    :align: center


ComparisonForced
~~~~~~~~~~~~~~~~

.. warning::
    This has been renamed to ComparisonStatement. The api is largely the same, but for details see https://youandvern.github.io/efficalc/base_classes.html#efficalc.ComparisonStatement

Code Example:

.. image:: /_static/examples/comparison_forced_code.png
    :scale: 40%
    :alt: Examples of creating the comparison_forced object in code
    :align: center

Calculation Report:

.. image:: /_static/examples/comparison_forced_report.png
    :scale: 40%
    :alt: Examples of the comparison_forced object in the calculation report
    :align: center

Design Portal: Not Displayed


Heading
~~~~~~~

Code Example:

.. image:: /_static/examples/heading_code.png
    :scale: 40%
    :alt: Examples of creating the heading object in code
    :align: center

Calculation Report:

.. image:: /_static/examples/heading_report.png
    :scale: 40%
    :alt: Examples of the heading object in the calculation report
    :align: center

Design Portal: Not Displayed


Input
~~~~~

Code Example:

.. image:: /_static/examples/input_code.png
    :scale: 40%
    :alt: Examples of creating the input object in code
    :align: center

Calculation Report:

.. image:: /_static/examples/input_report.png
    :scale: 40%
    :alt: Examples of the input object in the calculation report
    :align: center

Design Portal:

.. image:: /_static/examples/input_design.png
    :scale: 40%
    :alt: Examples of the input object in the design portal
    :align: center


TextBlock
~~~~~~~~~

Code Example:

.. image:: /_static/examples/text_code.png
    :scale: 40%
    :alt: Examples of creating the text_block object in code
    :align: center

Calculation Report:

.. image:: /_static/examples/text_report.png
    :scale: 40%
    :alt: Examples of the text_block object in the calculation report
    :align: center

Design Portal: Not Displayed


Title
~~~~~

Code Example:

.. image:: /_static/examples/title_code.png
    :scale: 40%
    :alt: Examples of creating the title object in code
    :align: center

Calculation Report:

.. image:: /_static/examples/title_report.png
    :scale: 40%
    :alt: Examples of the title object in the calculation report
    :align: center

Design Portal: Not Displayed



Full Example
------------

.. warning::
    Some aspects of this example may be using deprecated class and function names. For up-to-date examples, 
    view the efficalc library examples: https://github.com/youandvern/efficalc/tree/main/examples

Code
~~~~

.. code-block:: python 
    :linenos:

    from templates.encomp_utils import *


    def calculation():
        
        Title("Example Calculation Title")

        TextBlock(text="This can be a description of the calculation, and introduction to the author, or any other text.", reference="Author")


        Heading(text="Inputs", head_level=4, numbered=False, reference="")

        s1 = Input('l_1', 4, 'in', "The length of one side of the rectangle", min_value=0.001, max_value=100)

        a = Input(variable_name="A", default_value=16, unit="in^2", description="Area of a real life small rectangle", reference="AIHM 17.3.5", 
                input_type="number", select_options=None, min_value=0, max_value=100, num_step=1)
        
        c = Input("color", "Blue", "", "Color of the rectangle", input_type="select", select_options=["Red", "Green", "Blue", "Purple"])


        Heading("Assumptions", 4, False)

        Assumption("The rectangle in question is 2-dimensional planar")
        Assumption("Both side lengths are greater than 0")
        Assumption("This is a third important assumption")


        Heading("Calculations")

        TextBlock("Text blocks can add text anywhere you might need it.")

        Heading("Important Calculations", 2)

        s2 = Calculation("l_2", a / s1, "in", "The length of the other side of the rectangle")

        h = Calculation("h", SQRT(s1**2 + s2**2), "in", "The length of the hypotenuse (rectangle diagonal)", "Pythagoras ~500BC", True)

        Heading("Other Calculations", 2)
        a_s = Calculation(variable_name="A_{square}", expression=s1**2, unit="in^2", description="The area of a small imaginary square", 
                        reference="", result_check=True)

        
        Heading("Design Checks")
        Comparison(a=s1, comparator="=", b=s2, true_message="Square", false_message="Non-square", description="What type of rectangle is it?", 
                reference="", result_check=False)
        
        Comparison(h, ">", s2, description="The hypotenuse should always be larger than the side", result_check=True)
        Comparison(a, "<", a_s, description="I hope the square with side 1 is bigger than te rectangle", result_check=True)

        if c.get_value() == "Green":
            ComparisonForced(a=c, comparator="=", b="Green", comparator2=None, c=None, description="This is great, green is my favorite")
        else:
            ComparisonForced(c, "!=", "Green", description="Other colors are cool too", reference="Said Nobody")

        Heading("Placeholder for future section")
        Heading("A Sub-section", 2)
        Heading("A sub-sub-section", 3)
        Heading("Another sub-sub-section", 3)
        Heading("Another sub-section", 2)


Report
~~~~~~

This is the complete |location_link| for the above example.

|pdf_embed|


.. |location_link| raw:: html

   <a href="_static/example_calc.pdf" target="_blank">Calculation Report</a>


.. |pdf_embed| raw:: html

   <iframe src="_static/example_calc.pdf" width="100%" height="600px"></iframe>


Design Portal
~~~~~~~~~~~~~

.. image:: /_static/example_design_portal.png
    :alt: The complete design portal for this example
    :align: center

