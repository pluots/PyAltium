from dataclasses import dataclass
from enum import Enum


class HierarchyMode(Enum):
    automatic = 0


_key_map = {
"version":"Version",
"hierarchy_mode":"HierarchyMode",
"channel_rm_naming_style":"ChannelRoomNamingStyle",
"releases_folder":"ReleasesFolder",
"channel_des_fmt_style":"ChannelDesignatorFormatString",
"channel_room_level_sep":"ChannelRoomLevelSeperator",
"open_outputs":"OpenOutputs",
"":"ArchiveProject",
"":"TimestampOutput",
"":"SeparateFolders",
"":"TemplateLocationPath",
"":"PinSwapBy_Netlabel",
"":"PinSwapBy_Pin",
"":"AllowPortNetNames",
"":"AllowSheetEntryNetNames",
"":"AppendSheetNumberToLocalNets",
"":"NetlistSinglePinNets",
"":"DefaultConfiguration",
"":"UserID",
"":"DefaultPcbProtel",
"":"DefaultPcbPcad",
"":"ReorderDocumentsOnCompile",
"":"NameNetsHierarchically",
"":"PowerPortNamesTakePriority",
"":"AutoSheetNumbering",
"":"AutoCrossReferences",
"":"NewIndexingOfSheetSymbols",
"":"PushECOToAnnotationFile",
"":"DItemRevisionGUID",
"":"ReportSuppressedErrorsInMessages",
"":"FSMCodingStyle",
"":"FSMEncodingStyle",
"":"IsProjectConflictPreventionWarningsEnabled",
"":"IsVirtualBomDocumentRemoved",
"":"OutputPath",
"":"LogFolderPath",
"":"ManagedProjectGUID",
"":"IncludeDesignInRelease",
"":"CrossRefSheetStyle",
"":"CrossRefLocationStyle",
"":"CrossRefPorts",
"":"CrossRefCrossSheets",
"":"CrossRefSheetEntries",
"":"CrossRefFollowFromMainSettings",
}

@dataclass
class Design:
    version:str="1.0"
    hierarchy_mode:HierarchyMode|int = HierarchyMode.automatic
    channel_room_naming_style:int=0
    # releases_folder
