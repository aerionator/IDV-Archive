import plistlib
import os
import sys

# Get input directory from command line arguments
input_dir = sys.argv[1]

# loop over all the files in the folder
for filename in os.listdir(input_dir):
    if filename.endswith(".xml"):
        # Construct input and output file paths
        input_path = os.path.join(input_dir, filename)
        output_file = os.path.splitext(filename)[0] + ".plist"
        output_path = os.path.join(input_dir, output_file)

        try:
            # Read XML file and convert to dictionary
            with open(input_path, 'rb') as f:
                xml_data = f.read()
            plist_data = plistlib.loads(xml_data)

            # Write dictionary to binary plist file
            with open(output_path, 'wb') as f:
                plistlib.dump(plist_data, f)

            # Print success message and delete XML file
            os.remove(input_path)
            print(f"Conversion of {filename} is successful. XML file deleted.")

            # check if the "realTextureFileName" key exists in the plist file
            if 'realTextureFileName' in plist_data['metadata']:
                # get the value of the "realTextureFileName" key
                new_name = plist_data['metadata']['realTextureFileName']
                # remove the ".png" extension from the new filename
                new_name = os.path.splitext(new_name)[0]
                # add the ".plist" extension to the new filename
                new_name = new_name + ".plist"

                # check if the new filename already exists in the folder
                new_file_path = os.path.join(input_dir, new_name)
                count = 1
                while os.path.exists(new_file_path):
                    # if the new filename already exists, add a number to the filename
                    new_name = f"{os.path.splitext(new_name)[0]}_{count}.plist"
                    new_file_path = os.path.join(input_dir, new_name)
                    count += 1

                # rename the file with the new name
                os.rename(output_path, new_file_path)
                print(f"Renamed {output_file} to {new_name}")

        except Exception as e:
            # Print error message with input file name
            print(f"Error converting {filename}: {str(e)}")

# How to run the script
# cd /d  <Folder of the script>
# The XML folder should be inside the script folder
# python convert.py "<Folder of XML>"
