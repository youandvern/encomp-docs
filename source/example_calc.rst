.. _example-calc:

Example Calculation
===================

TODO
====

TODO: break this into a new "Advanced Features" page. This page can just be the full example that references each 
section on the new page. 

This full example will take you through some of the more intermediate/advanced features of efficalc templates. 
If this is your first time on the site, take a look at :ref:`start` for a more introductory example. 

This example will break down
    * Efficalc provided section properties
    * Conditional logic with if/else statements
    * Design checks using :code:`Comparison`
    * Unit conversions
    * Adding code references to calculations 

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

Step-By-Step
^^^^^^^^^^^^

In this example 

Complete Code
^^^^^^^^^^^^^

    .. code-block:: python
        :linenos:

        from templates.encomp_utils import *

        all_wf_sections = get_all_steel_section_sizes("WF")
        relevant_sizes = all_wf_sections[150:200]

        def calculation():

            Heading("Inputs", numbered=False)

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


Using if/else statements for conditional calculations -- TODO
-----------------------------------------------------

Often in codified calculations, some design equations will only be applicable under specific conditions. This is an ideal
scenario for using conditional logic and if/else statements. Efficalc is designed to support conditional rendering of 
calculations in your calculation reports or design interface.

Step-By-Step
^^^^^^^^^^^^

There are three simple set up steps

Complete Code
^^^^^^^^^^^^^

    .. code-block:: python
        :linenos:

        from templates.encomp_utils import *

        all_wf_sections = get_all_steel_section_sizes("WF")
        relevant_sizes = all_wf_sections[150:200]

        def calculation():

            Heading("Inputs", numbered=False)

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
