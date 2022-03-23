class TypesXML:
    CORE = """<Entity Id="00000000-0000-0000-0000-000000000000" TypeId="27d70fdc-4c4e-4774-bfac-7efbb48cde47" RevisionId="00000000-0000-0000-0000-000000000001" RevisionDate="2022-02-02T16:40:30.765432Z">
      <Property Name="Constructions" Type="String">1080</Property>
      <Property Name="Resin" Type="DimValue" Dimension="Relative">40%</Property>
      <Property Name="Frequency" Type="DimValue" Dimension="Frequency">1GHz</Property>
      <Property Name="DielectricConstant" Type="DimValue" Dimension="Dimensionless">4.0</Property>
      <Property Name="LossTangent" Type="DimValue" Dimension="Dimensionless">0.01</Property>
      <Property Name="GlassTransTemp" Type="DimValue" Dimension="Temperature">180C</Property>
      <Property Name="Manufacturer" Type="String">Manufacturer Name</Property>
      <Property Name="Name" Type="String">Core Name</Property>
      <Property Name="Thickness" Type="DimValue" Dimension="Length">0.1mm</Property>
    </Entity>"""

    PREPREG = """<Entity Id="00000000-0000-0000-0000-000000000000" TypeId="e04a4e7f-10f0-42df-add7-587710efd89e" RevisionId="00000000-0000-0000-0000-000000000001" RevisionDate="2022-02-02T16:40:30.765432Z">
      <Property Name="Constructions" Type="String">1x1080</Property>
      <Property Name="Resin" Type="DimValue" Dimension="Relative">40%</Property>
      <Property Name="Frequency" Type="DimValue" Dimension="Frequency">1GHz</Property>
      <Property Name="DielectricConstant" Type="DimValue" Dimension="Dimensionless">4.0</Property>
      <Property Name="LossTangent" Type="DimValue" Dimension="Dimensionless">0.01</Property>
      <Property Name="GlassTransTemp" Type="DimValue" Dimension="Temperature">180C</Property>
      <Property Name="Manufacturer" Type="String">Manufacturer Name</Property>
      <Property Name="Name" Type="String">Prepreg Name</Property>
      <Property Name="Thickness" Type="DimValue" Dimension="Length">0.1mm</Property>
    </Entity>"""
