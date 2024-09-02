import pyHMT2D
import inspect

def explore_ras_controller(inspect_methods=False, inspect_docstrings=False):
    # Initialize the HEC-RAS model
    version = "6.1.0"  # Replace with your HEC-RAS version
    faceless = True  # Run HEC-RAS without GUI

    # Create a HEC-RAS model instance
    hec_ras_model = pyHMT2D.RAS_2D.HEC_RAS_Model(version, faceless)

    # Initialize the HEC-RAS model (start the HEC-RAS process)
    hec_ras_model.init_model()

    # Access the RASController
    ras_controller = hec_ras_model._RASController

    # Get the list of methods and attributes
    methods = dir(ras_controller)

    # Iterate through each method and print its signature
    print("Methods and their input parameters in RASController:")
    for method_name in methods:
        if inspect_methods:
            # Skip special methods and attributes
            if method_name.startswith('__'):
                continue
            
            # Get the method from the object
            method = getattr(ras_controller, method_name)
            
            # Check if the attribute is callable (i.e., a method)
            if callable(method):
                try:
                    # Get the signature of the method
                    signature = inspect.signature(method)
                    print(f"{method_name}{signature}")
                    
                    # Optionally print the docstring for more insight
                    if inspect_docstrings:
                        docstring = inspect.getdoc(method)
                        print(f"    Docstring: {docstring}")
                
                except ValueError:
                    # If we can't get the signature, just print the method name
                    print(f"{method_name} (signature not available)")
            
            else:
                print(f"{method_name} (not a method)")
        else:
            print(method_name)

    # Close the project and exit the model
    hec_ras_model.close_project()
    hec_ras_model.exit_model()
    
if __name__ == "__main__":
    explore_ras_controller(inspect_methods=True, inspect_docstrings=True)
