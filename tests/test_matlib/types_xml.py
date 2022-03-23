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

    FINISH_ENIG = """<Entity Id="00000000-0000-0000-0000-000000000000" TypeId="b6b5d288-d4b3-4b60-857f-b949da02a37a" RevisionId="00000000-0000-0000-0000-000000000001" RevisionDate="2022-02-02T16:40:30.765432Z">
      <Property Name="Thickness" Type="DimValue" Dimension="Length">0.004mm</Property>
      <Property Name="Process" Type="String">Electroless nickle immersion gold</Property>
      <Property Name="Material" Type="String">Nickel, gold</Property>
      <Property Name="Color" Type="System.Windows.Media.Color, PresentationCore, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35">#FFFFFFFF</Property>
    </Entity>"""

    SOLDERMASK = """<Entity Id="00000000-0000-0000-0000-000000000000" TypeId="968469a9-c799-46e2-bc61-c05b2553ab48" RevisionId="00000000-0000-0000-0000-000000000001" RevisionDate="2022-02-02T16:40:30.765432Z">
      <Property Name="Solid" Type="DimValue" Dimension="Relative">4%</Property>
      <Property Name="Color" Type="System.Windows.Media.Color, PresentationCore, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35">#008800FF</Property>
      <Property Name="Frequency" Type="DimValue" Dimension="Frequency">1GHz</Property>
      <Property Name="DielectricConstant" Type="DimValue" Dimension="Dimensionless">3</Property>
      <Property Name="LossTangent" Type="DimValue" Dimension="Dimensionless">0.1</Property>
      <Property Name="Manufacturer" Type="String">Manufacturer</Property>
      <Property Name="Name" Type="String">Test Soldermask</Property>
      <Property Name="Thickness" Type="DimValue" Dimension="Length">0.05mm</Property>
    </Entity>"""
