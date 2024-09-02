# HEC-RAS RASController Methods and Attributes Overview

## Project Management

- **Project_Open(projectFilename)**: Opens an existing HEC-RAS project.
- **Project_Save()**: Saves the current project.
- **Project_SaveAs(newProjectName)**: Saves the project under a new name.
- **Project_Close()**: Closes the current project.
- **Project_Current()**: Returns information about the current project.

## Geometry Management

- **Geometry()**: Handles general geometry operations.
- **Geometry_GISImport(title, Filename)**: Imports geometry data from a GIS file.
- **Geometry_Get2DFlowAreas(Count, D2Names)**: Retrieves 2D flow areas from the geometry.
- **Geometry_GetNode(riv, rch, RS)**: Gets a specific node in the geometry.

## Flow Data

- **SteadyFlow_SetFlow(River, Reach, RS, Flow)**: Sets the steady flow data.
- **UnsteadyFlow_SetGateOpening_Constant(River, Reach, RS, GateName, OpenHeight, errMsg)**: Sets the gate opening in unsteady flow conditions.

## Plan Management

- **Plan_Names(PlanCount, PlanNames, IncludeOnlyPlansInBaseDirectory)**: Retrieves the names of plans in the project.
- **Plan_SetCurrent(PlanTitleToSet)**: Sets the current plan.

## Output and Reporting

- **Output_GetNode(riv, rch, RS)**: Retrieves output data for a specific node.
- **OutputDSS_GetStageFlow(River, Reach, RS, nValue, ValueDateTime, Stage, Flow, errMsg)**: Retrieves stage and flow data from DSS output.

## Visualization and Plotting

- **PlotXS(River, Reach, RS)**: Plots cross-sections.
- **PlotStageFlow(River, Reach, RS)**: Plots stage versus flow.

## Computation Control

- **Compute_CurrentPlan(nmsg, Msg, BlockingMode=True)**: Runs the current plan in blocking mode.
- **Compute_ShowComputationWindow()**: Displays the computation window.
- **Compute_Cancel()**: Cancels the ongoing computation.

## Schematic Handling

- **Schematic_ReachPoints(RiverName_0, ReachName_0, ReachStartIndex_0, ReachPointCount_0, ReachPointX_0, ReachPointY_0)**: Retrieves schematic reach points.

## Miscellaneous

- **HECRASVersion()**: Retrieves the version of the HEC-RAS software.
- **ShowRas()**: Displays the main HEC-RAS window.
- **QuitRas()**: Quits the HEC-RAS application.


# Full Methods List

- CLSID
- ComputeStartedFromController
- Compute_Cancel
- Compute_Complete
- Compute_CurrentPlan
- Compute_HideComputationWindow
- Compute_ShowComputationWindow
- Compute_WATPlan
- Create_WATPlanName
- CurrentGeomFile
- CurrentGeomHDFFile
- CurrentPlanFile
- CurrentProjectFile
- CurrentProjectTitle
- CurrentSteadyFile
- CurrentUnSteadyFile
- Edit_AddBC
- Edit_AddIW
- Edit_AddLW
- Edit_AddXS
- Edit_BC
- Edit_GeometricData
- Edit_IW
- Edit_LW
- Edit_MultipleRun
- Edit_PlanData
- Edit_QuasiUnsteadyFlowData
- Edit_SedimentData
- Edit_SteadyFlowData
- Edit_UnsteadyFlowData
- Edit_WaterQualityData
- Edit_XS
- ExportGIS
- Geometry
- Geometry_GISImport
- Geometry_Get2DFlowAreas
- Geometry_GetGML
- Geometry_GetGateNames
- Geometry_GetMann
- Geometry_GetNode
- Geometry_GetNodes
- Geometry_GetReaches
- Geometry_GetRivers
- Geometry_GetStorageAreas
- Geometry_RatioMann
- Geometry_SetMann
- Geometry_SetMann_LChR
- Geometry_SetSAArea
- GetDataLocations_Output
- HECRASVersion
- OutputDSS_GetStageFlow
- OutputDSS_GetStageFlowSA
- Output_ComputationLevel_Export
- Output_GetNode
- Output_GetNodes
- Output_GetProfiles
- Output_GetReach
- Output_GetReaches
- Output_GetRiver
- Output_GetRivers
- Output_Initialize
- Output_NodeOutput
- Output_ReachOutput
- Output_Variables
- Output_VelDist
- PlanOutput_IsCurrent
- PlanOutput_SetCurrent
- PlanOutput_SetMultiple
- Plan_BreachesGetXML
- Plan_BreachesSetXML
- Plan_GetFilename
- Plan_GetParameterUncertaintyXML
- Plan_InformationXML
- Plan_Names
- Plan_Reports
- Plan_SetCurrent
- Plan_SetParameterUncertaintyXML
- PlotHydraulicTables
- PlotPF
- PlotPFGeneral
- PlotRatingCurve
- PlotStageFlow
- PlotStageFlow_SA
- PlotXS
- PlotXYZ
- Project_Close
- Project_Current
- Project_New
- Project_Open
- Project_Save
- Project_SaveAs
- ProjectionSRSFilename
- QuitRas
- Schematic_D2FlowAreaPolygon
- Schematic_ReachCount
- Schematic_ReachPointCount
- Schematic_ReachPoints
- Schematic_StorageAreaPolygon
- Schematic_XSCount
- Schematic_XSPointCount
- Schematic_XSPoints
- ShowRas
- ShowRasMapper
- SteadyFlow_ClearFlowData
- SteadyFlow_FixedWSBoundary
- SteadyFlow_SetFlow
- SteadyFlow_nProfile
- TablePF
- TableXS
- UnsteadyFlow_SetGateOpening_Constant
- _ApplyTypes_
- __class__
- __delattr__
- __dict__
- __dir__
- __doc__
- __eq__
- __format__
- __ge__
- __getattr__
- __getattribute__
- __gt__
- __hash__
- __init__
- __init_subclass__
- __iter__
- __le__
- __lt__
- __module__
- __ne__
- __new__
- __reduce__
- __reduce_ex__
- __repr__
- __setattr__
- __sizeof__
- __str__
- __subclasshook__
- __weakref__
- _get_good_object_
- _get_good_single_object_
- _oleobj_
- _prop_map_get_
- _prop_map_put_
- coclass_clsid
- wcf_ComputePlan
- wcf_CreateNewPlan
- wcf_InputDataLocations_Get
- wcf_InputDataLocations_Set
- wcf_OutputDataLocations
- wcf_SetOutputPlans
