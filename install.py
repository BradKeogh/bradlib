
# coding: utf-8

# # Script to copy files to Anaconda paths so can import and use scripts

# In[1]:

module_name = 'bradlib'


# #### find main path for install

# In[2]:

from distutils.sysconfig import get_python_lib #; print(get_python_lib())


# In[3]:

path_main = get_python_lib()


# In[4]:

path_main


# In[5]:

path_main.split('Anaconda3')


# #### make list of paths need to copy files to & add main path

# In[ ]:




# In[6]:

dest_paths_list = []


# In[7]:

dest_paths_list.append(path_main + '\\' + module_name)


# In[8]:

dest_paths_list


# #### add paths to list for conda environments currently available

# MAKE SURE HAS 'module name' AT END OF PATH!!

# In[9]:

x = get_ipython().getoutput('conda env list')


# In[10]:

#x[2:-2]


# In[11]:

print('------------------------------------------------')
print('Conda envrionments found which will install to:')
for i in x[2:-2]:
    y = i.split(' ')
    print(y[0])
    new_path = path_main.split('Anaconda3')[0] +'Anaconda3\\envs\\'+y[0]+'\\Lib\\site-packages\\' + module_name
    #print(new_path)
    dest_paths_list.append(new_path)


# In[12]:

dest_paths_list


# #### function to  copy files to list of paths 

# In[13]:

import os


# In[14]:

def copy_to_paths(source,dest):
    """
    Function takes source and destination folders and copies files.
    #Source and dest needed in fomrat below: 
    #source = ".\\bradlib"
    #dest = "C:\\Users\\bjk1y13\\dev\\garbage\\bradlib"
    """
    #### Remove __pycache__ folder as is not required
    pycache_loc = source + "\\__pycache__"
    if os.path.isdir(pycache_loc) == True:
        print("__pycache__ found in source and being deleted...")
        get_ipython().system('rmdir $pycache_loc /S /Q')
                
    #### Copy files to new destination
    
    print('------------------------')
    print('Destination: ', dest)
    print('---------')
    folder_exists = os.path.isdir(dest)
    if folder_exists == True:
        print('Folder exists')
        ### delete older version folder
        print('Deleting old folder...')
        get_ipython().system('rmdir $dest /S /Q')
        print('Copying new folder...')
        get_ipython().system('xcopy $source $dest /E /I')
        
    elif folder_exists == False:
        print('Folder does not exist')
        print('Copying new folder...')
        get_ipython().system('xcopy $source $dest /E /I')
    else:
        print('Something has gone wrong!!')
    
    print('COMPLETE')
    print('------------------------')
    return


# In[15]:

source = ".\\" + module_name


# In[ ]:




# #### Run code for each location

# In[16]:

for destination in dest_paths_list:
    print(destination)
    copy_to_paths(source, destination)


# In[ ]:



