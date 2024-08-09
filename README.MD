
#Follow the nstruction to install and run code
This code has been written and tested in Ububto 20.04. 



### Istalling Python and Virtual Environments:
open a terminal and run the following script: 


>> $ ./run.sh

You need to be a sudo user to be able to run this code, as it is going to install python 3.8.

If the installation is successfull, you will see the following message:


>> echo "Virtual environment 'vorto_v_env' created and activated with Python 3.8."


### Activation the virtual environment: 
Open a terminal in the current directory, and run the following:

>> source ./vorto_v_env/bin/activate


### Testing the virtual environemt:
After sourcing the virtual environment, run the following code to see if everything works correctly:

>> which python

The result should be "./vorto_v_env/bin/python".

At this step, you can run the code using:

>> python main.py

