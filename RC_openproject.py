import win32com.client as win32

def open_ras_project():
    """
    Demonstrates how to open a HEC-RAS project using the HEC-RAS controller.
    """
    # Change the cursor to the 'Wait' state (Rotating Circle)
    print("Please wait...")

    # Initialize the HEC-RAS controller
    rc = win32.Dispatch("RAS610.HECRASController")

    str_filename = r"C:\ATD\Hydraulic Models\Bennett_Test\MW_Valleys.prj"

    print(f"Opening the HEC-RAS project {str_filename}...")
    # Open the HEC-RAS project
    rc.Project_Open(str_filename)

    # Show the HEC-RAS interface
    rc.ShowRas()

    # Display a message box indicating the project is open
    print(f"The HEC-RAS project {str_filename} is open.")
    try:
        plans = rc.Plan_Names()
    except Exception as e:
        print(f"Error retrieving plan names: {e}")
    
    # Change the cursor back to default
    print(f"Plans in the project: {plans}")

    # Close HEC-RAS
    rc.QuitRas()

# Call the function
open_ras_project()
