.. _next-steps:

Next Steps: Superpowered Features
=================================

These are some of efficalc's features that will take your calculations to the next level.

These short examples will take you through some of some of efficalc's features that will take your calculations 
to the next level. If this is your first time on the site, take a look at :ref:`start` for the basics of creating 
efficalc templates. 

These example will break down
    * Efficalc provided section properties
    * Conditional logic with if/else statements
    * Design checks using :code:`Comparison`

Using efficalc provided section properties
------------------------------------------

This example calculation will be a simple wide flange beam design for someone trying to find the optimal section 
size for their beam. By using the provided section properties, we can easily select different sections we want to 
try in the design portal:

.. image:: /_static/example_calc/section_select.png
    :alt: Design portal results with large triangle
    :align: center

Step-By-Step
^^^^^^^^^^^^

There are three simple set up steps for selecting and using sections in a template:

    #. Get the size options
    #. Create a selector input
    #. Get section properties from the selected option

We can use the functions described in :ref:`sections` to get a complete list of available sizes:

    :code:`all_wf_sections = get_all_steel_section_sizes("WF")`

Then we can create a selector input named "section" with our sizes:

    :code:`section = Input("section", "W18X40", input_type="select", select_options=all_wf_sections)`

.. note:: 
    The default value for the selector input must be one of the available size names in :ref:`steel-sections` i.e. "W18X40"

Finally, to get a section property (see all available properties in :ref:`steel-sections`) we take two steps:

    #. Get all properties for the selected section: 
    
        :code:`section_properties = get_steel_section_properties("WF", section.get_value())`

    #. Get each required property in a `Calculation` object: 
    
        :code:`d = Calculation("d", section_properties.get("d"), "in")`
        
        :code:`Zx = Calculation("Z_x", section_properties.get("Zx"), "in^3")`

Now, anytime you choose a section, the right property will be used in the calculations. Whenever we need to reference the 
property, we can use it just like any variable:

    :code:`Mp = Calculation("M_p", Fy * Zx, "kip-in")`

.. note:: 
    For steel wide flange sections, efficalc has over 350 options to choose from. Instead of providing all options to the selector
    input, you can provide (1) your own list of sizes or (2) a sub-list of all sizes 
       
        1. :code:`["W18X40", "W18X46", "W18X50"]`
        2. :code:`relevant_sizes = all_wf_sections[150:200]`

Putting this together with some headings and descriptions, we will have:

Complete Code
^^^^^^^^^^^^^

    .. code-block:: python
        :linenos:

        from templates.encomp_utils import *

        all_wf_sections = get_all_steel_section_sizes("WF")
        relevant_sizes = all_wf_sections[150:200]

        def calculation():

            Heading("Inputs", numbered=False)
            section = Input("section", "W18X40", input_type="select", select_options=relevant_sizes, description="Steel beam section size")
            Fy = Input("F_y", 50, "ksi", "Steel yield strength")

            Heading("Section Properties", numbered=False)
            section_properties = get_steel_section_properties("WF", section.get_value())
            d = Calculation("d", section_properties.get("d"), "in")
            Zx = Calculation("Z_x", section_properties.get("Zx"), "in^3")
            
            Heading("Calculations", numbered=False)
            Mp = Calculation("M_p", Fy * Zx, "kip-in", "Nominal plastic moment strength", result_check=True)
            

Calculation Report
^^^^^^^^^^^^^^^^^^

.. image:: /_static/example_calc/section_report.png
    :alt: Calculation report with section size
    :align: center

Design Portal
^^^^^^^^^^^^^

.. image:: /_static/example_calc/section_design.png
    :alt: Design portal with section size
    :align: center


Using if/else statements for conditional calculations
-----------------------------------------------------

Often in codified calculations, some design equations will only be applicable under specific conditions. This is an ideal
scenario for using conditional logic and if/else statements. Efficalc is designed to support conditional rendering of 
calculations in your calculation reports or design interface.

For example, ACI 318-14 section 9.7.6.2.2 has different requirements for the maximum spacing of shear reinforcement depending on 
the proportion of steel reinforcement strength (V\ :sub:`s`) vs limiting stel reinforcement strength based on concrete section 
strength (V\ :sub:`s-lim`):

    if V\ :sub:`s` :math:`\leq` V\ :sub:`s-lim` then use the lesser of d/2 or 24 inches

    otherwise use the lesser of d/4 or 12 inches

.. image:: /_static/example_calc/condition_code.png
    :alt: ACI 318-14 Section 9.7.6.22
    :align: center


Step-By-Step
^^^^^^^^^^^^

Conditional logic in efficalc uses native python syntax. Calculations in conditional blocks are only rendered in the 
design portal and calculation reports when they are in the executed branch. In the reinforcement steel example above, 
we want to display the constant limit as 24 inches OR 12 inches; not both.

First we calculate V\ :sub:`s-lim` according to table 9.7.6.2.2

    :code:`Vs_lim = Calculation('V_{s-lim}', 4 * SQRT(fc) * bw * d, "lbs")`

Then we can handle the conditional check. To compare variables (Input, Calculation, etc.) in a python if statement, we can get the
value using the :code:`.get_value()` method. This gets the value of the variable in a number that can also be compared with plain
numbers (i.e. 2, 0.34, etc.), not just variables.

    :code:`if Vs.get_value() \<= Vs_lim.get_value():`

Then if this statement is true, we want the maximum allowed reinforcement spacing to be the lesser of d/2 and 24:

    :code:`Calculation('s_{max}', MIN(d / 2, 24), "in")`

To handle the case where the above check is not true and we should use the lesser of d/4 and 12, we can add an else block with:

    :code:`Calculation('s_{max}', MIN(d / 4, 12), "in")`

Putting this together with some headings, comparison text, and descriptions, we will have:

Complete Code
^^^^^^^^^^^^^

    .. code-block:: python
        :linenos:

        from templates.encomp_utils import *

        def calculation():

            Heading("Inputs", numbered=False)
            bw = Input('b_w', 12, 'in', 'Effective section width')
            d = Input('d', 20, 'in', 'Depth to reinforcement steel centroid')
            fc = Input("f'_c", 4000, 'psi', 'Compressive strength of concrete')
            Vs = Input("V_s", 50000, "lbs", "Shear capacity of reinforcement steel")

            Heading("Calculations", numbered=False)
            Vs_lim = Calculation('V_{s-lim}', 4 * SQRT(fc) * bw * d, "lbs", 'Limiting shear reinforcement steel capacity', reference="ACI 318-14 Table 9.7.6.2.2")

            if Vs.get_value() <= Vs_lim.get_value():
                ComparisonForced(Vs, "<=", Vs_lim)
                Calculation('s_{max}', MIN(d / 2, 24), "in", "Maximum allowed spacing of shear reinforcement", reference="ACI 318-14 9.7.6.2.2", result_check=True)
            
            else:
                ComparisonForced(Vs, ">", Vs_lim)
                Calculation('s_{max}', MIN(d / 4, 12), "in", "Maximum allowed spacing of shear reinforcement", reference="ACI 318-14 9.7.6.2.2", result_check=True)


Calculation Report
^^^^^^^^^^^^^^^^^^

Full report with the first conditional check true:

.. image:: /_static/example_calc/condition_report1.png
    :alt: Calculation report with conditional logic first block executed
    :align: center

Calculations only with the first conditional check false (b reduced to 8 in):

.. image:: /_static/example_calc/condition_report2.png
    :alt: Calculation report with conditional logic second block executed
    :align: center


Design Portal
^^^^^^^^^^^^^

.. image:: /_static/example_calc/condition_design.png
    :alt: Design portal with a single conditional result displayed
    :align: center


Design checks using :code:`Comparison`
--------------------------------------

Whether it's a final result or mid-calculation, you may want to perform a design check to compare a calculation 
result against a target value. For example, you may want a clear display that let's you know the capacity is less 
than the demand. 

Efficalc's :code:`Comparison` object is designed to make design checks easy and useful. The design portal will highlight
your checks green or red depending on whether they are passing or failing with the current inputs. The calculation report
will also clearly display the check with variables, substituted values, and a customizable description.

Step-By-Step
^^^^^^^^^^^^

The complete list of options for a :code:`Comparison` object are given in :ref:`objects` and :ref:`examples`. This example 
will hightlight on basic usage with custom messages.

For a design check to confirm that the design moment strength is greater than the moment demand, we can add the following 
line after our calculation:

    :code:`Comparison(Mu, "<=", PMn, true_message="Pass", false_message="Fail")`

This will show a comparison of the variables Mu and PMn and the resulting true_message or false_message depending on the result.

Complete Code
^^^^^^^^^^^^^

    .. code-block:: python
        :linenos:

        from templates.encomp_utils import *


        def calculation():

            Heading("Inputs", numbered=False)
            Zx = Input("Z_x", 82.3, "in^3", "Plastic section modulus of the beam")
            Fy = Input("F_y", 50, "ksi", "Steel yield strength")
            Mu = Input("M_u", 200, "kip-ft", "Beam moment demand")
            P = Input("\phi", 0.9, "", "Flexural resistance factor")

            Heading("Calculations", numbered=False)
            Mp = Calculation("M_p", Fy * Zx / ft_to_in, "kip-ft", reference="AISC Eq. F2-1")
            
            PMn = Calculation("\phi M_n", P * Mp, "kip-ft", "Design flexural strength of the section", result_check=True)
            Comparison(Mu, "<=", PMn, true_message="Pass", false_message="Fail")
            

Calculation Report
^^^^^^^^^^^^^^^^^^

.. image:: /_static/example_calc/comparison_report.png
    :alt: Calculation report with a comparison
    :align: center

Design Portal
^^^^^^^^^^^^^

.. image:: /_static/example_calc/comparison_design1.png
    :alt: Design portal with a passing comparison
    :align: center

.. image:: /_static/example_calc/comparison_design2.png
    :alt: Design portal with a failing comparison
    :align: center
