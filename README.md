This project is a proof of concept for linking a locally hosted backend AI to a frontend and attempting to mitigate prompt manipulation.
Development notes and install instructions:

To run this, the steps are as follows:

Make sure to have python installed. The version that I used for this personally was 3.13.3. If python is not installed, go to python.org and download python from there.

Make sure pip is installed. Run either:
python get-pip.py
or
py get-pip.py
Depending on your system in powershell or the command prompt

Make sure LM Studio is installed, and install the model you want. This does not have to be the same model that I ran but, if you do a different model, make sure to update the code with the name of the new model accordingly.

In a command prompt or powershell, run the command:
lms server start

Though this is not strictly necessary as the launch file should do this on execution, I normally do it just to make sure. I also open LM Studio to make sure the model is loaded every time

Make sure to download tesseract from https://github.com/UB-Mannheim/tesseract/wiki and run tesseract.exe, then copy the path to tesseract.exe and put that where the tesseract line in the script is: 
pytesseract.pytesseract.tesseract_cmd = [your path]

Once that is finished, follow the next steps to get this code on your device and working:

Go to CMD or powershell and copy paste:
git clone https://github.com/Collatdmg/aiTest/

then you should be able to run:
cd aiTest

then:
pip install -r requirements.txt

then:
python launch.py should launch the application if you are in the correct directory.
