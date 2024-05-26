from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UploadFileForm
from .models import File
from django.contrib.auth.models import User
from .encryption import encrypt_file, decrypt_file
from django.http import HttpResponse
import os
from .fileManagement import shareFile, share_file_path, user_directory_path, file_exists_in_folder
from .hash import cal_file_hash

# Temporary Fernet key:
temp_fernet_key  = b'zdnoc4dAbhI4fZbcSdDMuBPvntPcY7DwHaSsVwAL5js='

@login_required
def home(request):
    file = File.objects.filter(owner=request.user)
    #file = request.user.ownedFiles.all()
    return render(request, 'share/index.html', {'user_files':file})


@login_required
def upload(request):
    
    if request.method == "POST":

        # User only inputs 2 data: file name and the file.
        form = UploadFileForm(request.POST, request.FILES)
        
        # Remaining columns will be filled here.
        if form.is_valid():
            #file_name = form.cleaned_data['fileName']

            # Save the form data without committing to the database.(similar to add in git!)
            File = form.save(commit=False)

            File.fileSize = round(request.FILES['fileDir'].size / (1024 ** 2), 2)
            File.owner = request.user
            # File.shared = False  
            File.sender = None  

            File.save()

            ############ Hash ############# 
            File.fileHash = cal_file_hash(open(File.fileDir.path, 'rb')) #read bits

            #File.save()

            # Encryption (we first save the file and then encrypt)
            key = temp_fernet_key
            encrypt_file(File.fileDir.path, key) # .path gives the actual route of the file

            File.save()

            #File.fileHash = cal_file_hash(open(File.fileDir.path, 'rb'))

            # print(File.fileHash)
            # print(cal_file_hash(request.FILES['fileDir']))
            # print(File.fileHash)
            # File.save()
            # print(cal_file_hash(request.FILES['fileDir']))
        else:
            pass

    else:
        form = UploadFileForm()


    return render(request, 'share/uploadFile.html', {'form':form})
'''
Documentation: hash the original data not the encrypted data.
upload
1. hash
2. encrypt
download
3. decrypt
4. compare
5. encrypt
'''

@login_required
# Instead of using the build in download funtion we will make a custom one.
def download(request, file_id):

    #find the file:(one file so no need to use filter)
    file_inst = File.objects.get(id=file_id)

    # File path:(fileDir.path)
    file_path = file_inst.fileDir.path

    # encrypt_file(file_path, temp_fernet_key)


    #decrypt:
    decrypt_file(file_path, temp_fernet_key)


    # Calculate hash of the file content
    calculated_hash = cal_file_hash(open(file_path, 'rb'))
    # print(calculated_hash)

    # #encrypt file again:
    # encrypt_file(file_path, temp_fernet_key)


    if calculated_hash == file_inst.fileHash:
        # Check if the user has permission to download the file
        if request.user == file_inst.owner:

            # # File path:(fileDir.path)
            # file_path = file_inst.fileDir.path

            # #decrypt:
            # decrypt_file(file_path, temp_fernet_key)


            # calculated_hash = cal_file_hash(open(file_inst.fileDir.path, 'rb'))
            # print(calculated_hash)

            # download:
            with open(file_path, 'rb') as file:
                file_content = file.read()

            #encrypt file again:
            encrypt_file(file_path, temp_fernet_key)


            # calculated_hash = cal_file_hash(open(file_inst.fileDir.path, 'rb'))
            # print(calculated_hash)

            # Extract the file extension using os.path.splitext() on the full path


            _ , file_extension = os.path.splitext(file_path)
            print(file_extension)

            # calculated_hash = cal_file_hash(open(file_inst.fileDir.path, 'rb'))
            # print(calculated_hash)

            #download file :
            response = HttpResponse(file_content, content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{file_inst.fileName}{file_extension}"'

            #hash changes!!!!
            # calculated_hash = cal_file_hash(open(file_inst.fileDir.path, 'rb'))
            # print(calculated_hash)

            # return the response
            return response
        
        else:
            #encrypt file again:
            encrypt_file(file_path, temp_fernet_key)

            # Generate a JavaScript script to show a pop-up
            pop_up_script = """
                <script>
                    alert("You do not have permission to download this file.");
                    window.location.replace("{0}");
                </script>
            """.format(reverse('sharing:home'))

            return HttpResponse(pop_up_script)
    else:
        #encrypt file again:
        encrypt_file(file_path, temp_fernet_key)

        pop_up_script = """
            <script>
                alert("Integrity error, try again.");
                window.location.replace("{0}");
            </script>
        """.format(reverse('sharing_app:home'))
        
        return HttpResponse(pop_up_script)
    
    

@login_required
def share(request, file_id):
    errorMessage = None
    file_to_share = File.objects.get(id=file_id)

    if request.method == 'POST':
        try:

            # Get the user to share with.
            userName = request.POST.get('username')
            user = User.objects.get(username=userName)
            
            # Get the file we want to share:
            file_to_share = File.objects.get(id=file_id)

            #print(f"file_to_share----{file_to_share}")

            # create a new instance in the File table for the reciever (file directory is yet to set)
            shared_File = file_to_share.make_share_file(user)

########################################## if shared file is None ###############################################################
# django buil in u dont have to pass in dict:(no pop up)
            if shared_File is None:
               # messages.error(request, "Please check the username. You are using your username!")
                errorMessage = "Please check the username. You are using your username!"

            else:
########################################## Hash check ###############################################################
                decrypt_file(file_to_share.fileDir.path, temp_fernet_key)
                calculated_hash = cal_file_hash(open(file_to_share.fileDir.path, 'rb'))
                encrypt_file(file_to_share.fileDir.path, temp_fernet_key)

                # The file is not tempered (hopefully)
                if calculated_hash == file_to_share.fileHash:


########################################## Dir for table ###############################################################
                    
                    # set the file dir in the File table :

                    # original file dir from db:
                    og_file_dir = file_to_share.fileDir.path
                    og_file_name = os.path.basename(og_file_dir) # This is also the shared file name.(file name)
                    shared_File.fileDir =  user_directory_path(shared_File, og_file_name)

                    print(shared_File.fileDir)

########################################## Move File (different dir) #########################################################
                    # Get the path for the shared file (to save in the table):
                    shared_File_Dir = share_file_path(shared_File)

                    # Check if the directory exists, and create it if not
                    if not os.path.exists(shared_File_Dir):
                        os.makedirs(shared_File_Dir)


    # ##########
    #                 counter = 0
    #                 while os.path.exists(os.path.join(shared_File_Dir, new_file_name)):
    #                     counter += 1
    #                     base_name, extension = os.path.splitext(og_file_dir)
    #                     print(f"extension === {extension}")
    #                     new_file_name = f"{base_name}_copy{counter}{extension}"


    ############################

                    # check if any file exists with the same name:(chnage the file name)
                    if file_exists_in_folder(shared_File_Dir, og_file_name):

                        og_file_name = os.path.basename(og_file_dir)
                        counter = 0
                        new_file_name = og_file_name
                        
                        # print(os.path.join(shared_File_Dir, new_file_name))
                        while os.path.exists(os.path.join(shared_File_Dir, new_file_name)):
                            counter += 1
                            _, extension = os.path.splitext(og_file_dir)
                            # base_name, _ = os.path.splitext(shared_File_Dir)
                            new_file_name = f"_copy{counter}{extension}"
                            print(new_file_name)

                        
                        #destination_path = os.path.join(shared_File_Dir, new_file_name)
                        destination_path = user_directory_path(shared_File, new_file_name)

                        print(destination_path)
                        print(f"shared file dir == {shared_File_Dir}")

                        shared_File.fileDir = destination_path

                        print(f"shared_File == {destination_path}")
                                    
                    # move the actual file: #shared_File_Dir
                    shareFile(file_to_share.fileDir.path, shared_File.fileDir.path)

                    print(shared_File.fileDir.path)


                    shared_File.save()


########################################## Re Hash check after transfer ###############################################################

                    # calculated_hash = cal_file_hash(open(shared_File.fileDir.path, 'rb'))

                    # if calculated_hash == file_to_share.fileHash:
                    #     shared_File.fileHash = calculated_hash

########################################## Save ########################################################################
                    shared_File.save()

        except User.DoesNotExist:
            errorMessage = "User does not exit, Please put in the correct user name."
           


    return render(request, 'share/shareFile.html', {'errorMessage':errorMessage, 'file_to_share':file_to_share} )



