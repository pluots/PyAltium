Materials Library
=================

Altium materials libraries are stored in an XML format that can be loaded and 

.. code-block:: python

    from pyaltium.matlib.types import PrePreg, FinishENIG

    e = PrePreg(
        name="Prepreg Name",
        dielectric_constant=4.0,
        thickness=0.1,
        glass_trans_temp=180,
        manufacturer="Manufacturer Name",
        construction="1x1080",
        resin_pct=40,
        frequency=1e9,
        loss_tangent=0.01,
    )

    e = FinishENIG(
        process="Electroless nickle immersion gold",
        material="Nickel, gold",
        thickness=0.004,
        color="#FFFFFFFF",
    )
