.. Encomp documentation master file, created by
   sphinx-quickstart on Thu Dec  1 21:08:48 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Encomp's documentation!
==================================

.. toctree::
   :maxdepth: -1
   :tocdepth: -1
   :caption: Contents:


Styling Variable Names and Units
================================

Variable names and units are styled with using LaTex mathematical notation, which in some ways is 
intuitive but here are some helpful tips for common use cases.

Subscripts
----------

Single character subscripted variable names or units can be created with a simple underscore "_1". For example, 
the following Input object shows how a single character underscore is coded and displayed.

   Coded Definition: :code:`Input("min_a", 1, "m_2")` 

   Display Result:   min\ :sub:`a`\ = 1 m\ :sub:`2`\  

Multiple character subsripts must be wrapped in the curly braces after the underscore character "_{more}". For example, 
the following Input object shows how a multiple character underscore is coded and displayed.

   Coded Definition: :code:`Input("min_{abc}", 1, "m_{123}")` 

   Display Result:   min\ :sub:`abc`\ = 1 m\ :sub:`123`\  

Superscripts
------------

Single character superscripted variable names or units can be created with a simple caret (circumflex) "^2". For example, 
the following Input object shows how a single character with caret is coded and displayed.

   Coded Definition: :code:`Input("min^a", 1, "m^2")` 

   Display Result:   min\ :sup:`a`\ = 1 m\ :sup:`2`\  

Multiple character supersripts must be wrapped in the curly braces after the caret character "^{more}". For example, 
the following Input object shows how a multiple character caret is coded and displayed.

   Coded Definition: :code:`Input("min^{abc}", 1, "m^{123}")` 

   Display Result:   min\ :sup:`abc`\ = 1 m\ :sup:`123`\  


Adding Spaces
-------------

LaTex mathematical formatting naturally squashes spaces in text elements. If spaces are needed in units or 
variable names, then an "escape sequence" can be used with a forward slash before the space "\ ". For example, 
the following Input object shows how a space is coded and displayed for variable names and units.

   Coded Definition: :code:`Input("min\\ abc", 1, "m\\ 123")` 

   Display Result:   min abc = 1 m 123


Calculation Objects
===================

.. automodule:: base_definitions
   :members:


Section Methods
===============

.. automodule:: section_helpers
   :members:


Unit Conversions and Constants
==============================

.. automodule:: unit_conversions
   :members:

   
Calculation Utilities
=====================

The following are helpful utilites for building calculations using the `LatexExpr <https://github.com/youandvern/latexexpr_encomp>`_ library.

.. automodule:: latexexpr_docs
   :members:


Using Python with Encomp
========================

Positional vs. Keyword Arguments
--------------------------------

Encomp's calculation objects can be created using either positional or keyword arguments. There are some cases 
where using positional arguments might make more sense and others where keyword arguments will be very useful. 

Positional
~~~~~~~~~~

Positional arguments refer to creating a class or calling a function without using the parameter keywords but 
relying on the fact that the order of your parameters matches the order of the class/function parameters. 

The following examples show positional arguments in action. Note that all of the parameters used must be in order, 
but not all of the class or function parameters must be used. The :code:`Heading` object has 4 parameters 
(text, head_level, numbered, reference), but we have only used 2 of them. The default values will be used for 
the remaining parameters.

   Class creation: :code:`Heading("This is the text", 2)`

   Function call: :code:`section_properties = get_steel_section_properties("WF", "W14X109")`

Keyword
~~~~~~~

Keyword arguments do not have to match the order of the class/function parameters, but instead rely on explicitly 
defining which parameter is being added to. Required parameters must still be defined. 

The following examples show keyword arguments in action. Note that the parameters used do not have to be in order
and that we can access the last parameter of the :code:`Heading` class (reference) without defining every one before 
it. The :code:`Heading` object has 4 parameters (text, head_level, numbered, reference), but we have only used the 
first and last. The default values will be used for the remaining parameters.

   Class creation: :code:`Heading(text="This is the text", reference="REF")`

   Function call: :code:`section_properties = get_steel_section_properties(section_type="WF", section_size="W14X109")`

Mixing Positional and Keyword
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Positional and keyword arguments can be mixed as needed as long as your positional arguments are first. This can 
be very useful to take advantages of both ways to define arguments. The positional arguments will help you avoid 
typing out each argument name, but the keyword arguments can help access a other couple arguments you need out of 
a long list of optional arguments. 

The following examples show mixed positional and keyword arguments in action.

   Class creation: :code:`Heading("This is the text", reference="REF")`

   Function call: :code:`section_properties = get_steel_section_properties("WF", section_size="W14X109")`


Python's Math Module
--------------------

Some calculations may benefit from funtionality defined in Python's math module, so this has already been imported 
within encomp_utils import that should already be at the top of every template file. When building your template, you 
can access the math module by calling :code:`math.<method name>`. For example:

   .. code-block:: python

        >>> a = Input("a", math.floor(10.85))
        >>> print(a.get_value())
        10


Importing Other Modules
-----------------------

For security of the application, we have restricted users from importing other modules for their calculation templates. 
If you need to use a module that is not provided, please contact us and let us know what module you need and why it 
would be useful. We're happy to add other safe modules to the standard imports.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
