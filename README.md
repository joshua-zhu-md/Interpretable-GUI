# Interpretable_GUI

In this project, we make plotting clustermaps easy for those who don't have prior Python experience by implementing a variety of features: a CLI tool that allows you to drag and drop files on the terminal and a GUI that allows for more specification as well as plotting the wanted clustermap. An NPY and CSV file is required for this map to be made. The guidelines (shown currently below) and the examples of these files will also appear in a new window after clicking the "Help" button in the Clustermap_GUI. 

NPY File:

Your NPY file is the file that'll be clustered. It's the file that contains your patients and features. It should be an array without any holes. It will be normalized in this code.
 
CSV File:

Your CSV file will be shown in row(s) beside the NPY file (the map). The CSV file contains the patients and the categories. Its rows should be one more than the NPY file's rows. The values shouldn't have any holes and can be edited on the main page. It will be normalized by columns in this code. The first row should be the label names.

How to Run:
1. Clone repository from GitHub
   
2. Install necessary dependencies python (pip3 install -r Requirements.txt)
   
3. Access the directory using cd Aneja-Lab-Yale/Interpretable_GUI
   
4. Type python3 Clustermap_GUI.py onto terminal
   
    a. OPTIONAL: Drag and drop the necessary files with spaces between each file (py .csv .npy or .py .npy .csv)
  
5. Run the .py file, find the other files by clicking "Browse" in the GUI (if you didn't do 4a), and generate the clustermap
