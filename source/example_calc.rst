.. _example-calc:

Example Calculation
===================

This full example will display some of the more powerful features of efficalc templates that are displayed in :ref:`next-steps`.

To explore the different elements we use here, you can copy and paste this code into your own template and modify it as you like.


Design Portal
-------------

.. image:: /_static/example_calc/example_design.png
    :alt: Design portal for steel beam example
    :align: center


Calculation Report 
------------------

Here is the complete |location_link| for this example.

|pdf_embed|


.. |location_link| raw:: html

   <a href="_static/simple_steel_beam_report.pdf" target="_blank">Calculation Report</a>


.. |pdf_embed| raw:: html

   <iframe src="_static/simple_steel_beam_report.pdf" width="100%" height="600px"></iframe>


Complete Code 
-------------

.. code-block:: python
        :linenos:

        from templates.encomp_utils import *

        all_wf_sections = get_all_steel_section_sizes("WF")

        def calculation():
            Title("Steel Beam Moment Strength")

            TextBlock("Flexural strength of a steel wide-flange beam section.")

            Heading("Assumptions", numbered=False)
            Assumption("AISC 14th Edition controls design")
            Assumption("Beam web is unstiffened")

            Heading("Inputs", numbered=False)

            Mu = Input("M_u", 30, "kip-ft", "Beam ultimate moment demand")
            Lbu = Input("L_b", 20, "ft", "Beam unbraced length")

            section = Input("section", "W18X40", description="Beam section size",
                            input_type="select", select_options=all_wf_sections[150:200])

            Fy = Input("F_y", 50, "ksi", "Steel yield strength")
            Fu = Input("F_u", 65, "ksi", "Steel ultimate strength")
            Es = Input("E", 29000, "ksi", "Modulus of elasticity")

            Cb = Input("C_b", 1.0, "", "Lateral-torsional buckling modification factor", reference="AISC F1(3)")

            Heading("Section Properties", numbered=False)
            section_properties = get_steel_section_properties("WF", section.get_value())
            b = Calculation("b", section_properties.get("bf"), "in")
            d = Calculation("d", section_properties.get("d"), "in")
            Sx = Calculation("S_x", section_properties.get("Sx"), "in^3")
            Zx = Calculation("Z_x", section_properties.get("Zx"), "in^3")
            ry = Calculation("r_{y}", section_properties.get("ry"), "in")
            rts = Calculation("r_{ts}", section_properties.get("rts"), "in")
            J = Calculation("J", section_properties.get("J"), "in^4")
            ho = Calculation("h_o", section_properties.get("ho"), "in")
            bfl2tf = Calculation("b_f/2t_f", section_properties.get("bfl2tf"), "")
            hltw = Calculation("h/t_w", section_properties.get("hltw"), "")


            Heading("Beam Flexural Capacity", head_level=1)
            Pb = Calculation("\phi_{b}", 0.9, "", "Flexural resistance factor", reference="AISC F1(1)")

            Heading("Section Compactness", head_level=2)
            ypf = Calculation("\lambda_{pf}", 0.38 * SQRT(E / Fy), "", reference="AISC Table B4.1b(10)")
            Comparison(bfl2tf, "<=", ypf, true_message="CompactFlange", false_message="ERROR:NotCompactFlange", result_check=False)

            ypw = Calculation("\lambda_{pw}", 3.76 * SQRT(E / Fy), "", reference="AISC Table B4.1b(15)")
            Comparison(hltw, "<=", ypw, true_message="CompactWeb", false_message="ERROR:NotCompactWeb", result_check=False)

            Heading("Plastic Moment Strength", head_level=2)
            Mp = Calculation("M_{p}", Fy * Zx / ft_to_in, "kip-ft", "Nominal plastic moment strength",
                            reference="AISC Eq. F2-1")

            Heading("Yielding Strength", head_level=2)
            Mny = Calculation("M_{ny}", Mp, "kip-ft", reference="AISC Eq. F2-1")

            Heading("Lateral-Torsional Buckling", head_level=2)
            Lp = Calculation("L_{p}", 1.76 * ry * SQRT(E / Fy) / ft_to_in, "ft", reference="AISC Eq. F2-5")
            cc = Calculation("c", 1.0, "", reference="AISC Eq. F2-8a")
            Lr = Calculation("L_{r}", 1.95 * rts / ft_to_in * Es / (0.7 * Fy) * SQRT(
                J * cc / (Sx * ho) + SQRT((J * cc / (Sx * ho)) ** 2 + 6.76 * (0.7 * Fy / E) ** 2)), "ft",
                            reference="AISC Eq. F2-6")

            if Lbu.result() <= Lp.result():
                ComparisonForced(Lbu, "<=", Lp)
                Mnl = Calculation("M_{nltb}", Mp, "kip-ft", "The limit state of lateral-torsional buckling does not apply",
                                reference="AISC F2.2(a)")
            elif Lbu.result() > Lr.result():
                ComparisonForced(Lbu, ">", Lr)
                Fcr = Calculation("F_{cr}", Cb * PI ** 2 * Es / (Lbu * ft_to_in / rts) ** 2 + SQRT(
                    1 + 0.078 * J * cc / (Sx * ho) * (Lbu * ft_to_in / rts) ** 2), "ksi", reference="AISC Eq. F2-4")
                Mncr = Calculation("M_{ncr}", Fcr * Sx / ft_to_in, "kip-ft", reference="AISC F2.2(c)")
                Mnl = Calculation("M_{nltb}", MIN(Mncr, Mp), "kip-ft", reference="AISC Eq. F2-3")
            else:
                ComparisonForced(Lp, "<", Lbu, "<=", Lr)
                Mncr = Calculation("M_{ncr}",
                                Cb * BRACKETS(Mp - BRACKETS(Mp - 0.7 * Fy * Sx / ft_to_in) * (Lbu - Lp) / (Lr - Lp)),
                                "kip-ft", reference="AISC F2.2(b)")
                Mnl = Calculation("M_{nltb}", MIN(Mncr, Mp), "kip-ft", reference="AISC Eq. F2-2")

            Heading("Controlling Strength", head_level=2)
            PMn = Calculation("\phi M_n", Pb * MIN(Mny, Mnl), "kip-ft", "Design flexural strength of the section", result_check=True)
            Comparison(Mu, "<=", PMn)
